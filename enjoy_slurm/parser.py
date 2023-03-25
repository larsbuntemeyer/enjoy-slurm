import pandas as pd
from io import StringIO
from .config import delimiter, default_sacct_format, skip_args
import numpy as np
import re
import pandas as pd


def handle_sacct_format(format=None, kwargs={}):
    if format == "brief" or "brief" in kwargs:
        return ["--brief"]  # + jobsteps * ["--format", "jobname"]
    format = format or default_sacct_format
    if format:
        if not isinstance(format, list):
            format = [format]
        return ["--format"] + [",".join(format)]
    return []


def args_to_list(args):
    """parse sbatch arguments to list"""
    args_list = []
    for a in args:
        if isinstance(a, list):
            args_list += a
        elif "=" in a:
            args_list += a.split("=")
        elif " " in a:
            args_list += a.split()
        else:
            args_list.append(a)
    return args_list


def kwargs_to_list(d):
    """parse arguments to command line arguments for sbatch"""
    kwargs = kwargs_to_slurm(d)
    r = []
    for k, v in kwargs.items():
        r.append(k),
        if v:
            r.append(v)
    return r


def _maybe_eval_types(d, only_values=False):
    """parse a dictionary with strings to python types using pandas"""
    df = pd.DataFrame(d, index=[0])
    cols = df.columns
    df[cols] = df[cols].apply(pd.to_numeric, errors="ignore")
    return df.iloc[0].to_dict()


def parse_sacct(csv, jobsteps=None):
    """convert parsable sacct output to dataframe"""
    df = pd.read_csv(StringIO(csv), delimiter=delimiter)
    if jobsteps == "minimal":
        # ensure str
        df["JobID"] = df.JobID.astype(str)
        df = df[df["JobID"].str.isnumeric()].reset_index(drop=True)
        df["JobID"] = df.JobID.astype(np.int64)
        df = df.convert_dtypes()
    return df


def parse_dependency(ids):
    """parse dependency arguments to sbatch command line"""
    how = None
    if isinstance(ids, str):
        return ids
    if isinstance(ids, tuple):
        how, ids = ids
    if not how:
        how = "afterok"
    if not isinstance(ids, list):
        ids = [ids]
    return ":".join([how] + list(map(str, ids)))


def parse_slurm_arg(a, list_concat=","):
    """parse slurm arguments to str or list of str with colons"""
    if isinstance(a, (list, tuple)):
        return [list_concat.join(map(str, a))]
    if a is True:
        return ""
    return str(a)


def parse_scontrol_show(output):
    """try to parse scontrol output"""
    try:
        entries = [
            "".join(list(g)) for k, g in groupby(output.splitlines(), key=bool) if k
        ]
        results = {}
        for e in entries:
            attrs_list = e.split()
            attrs = {}
            for a in attrs_list:
                try:
                    split = a.split("=")
                    attrs[split[0]] = split[1]
                except:
                    pass
            results[list(attrs.values())[0]] = attrs
            # results.append({a.split("=")[0]:a.split("=")[1] for a in attrs})
    except Exception:
        results = output
    return results


def kwargs_to_slurm(d):
    """parse arguments to command line arguments for sbatch"""
    r = {}
    list_concat = ","
    for k, v in d.items():
        # ignore own kwargs
        if k in skip_args:
            continue
        flag = "--" + k.replace("_", "-")
        if k == "dependency" and v is not None:
            r[flag] = parse_dependency(v)
            continue
        if k == "kill_on_invalid_dep" and not isinstance(v, str):
            if v is not None:
                r[flag] = "no" if v is False else "yes"
            continue
        if v:
            r[flag] = parse_slurm_arg(v, list_concat)
            continue
        if v is False:
            continue
    return r


def parse_header_kwarg(line):
    """parses a Slurm header line into a dict"""
    if line.startswith("--"):
        line = line[2:]
    # split either by space or =
    k, v = re.split(r"\s|=", line, 1)
    # remove comments after SBATCH #
    v = v.split("#", 1)[0]
    return {k.strip(): v.strip()}


def parse_header(header, eval_types=True):
    """Parses Slurm header into dict

    Parameters
    ----------
    header : str
        Jobscript containing a Slurm header.
    eval_types : bool
        Evaluate strings in dictionary

    Returns
    -------
    Slurm config : dict
        A dictionary containing the slurm configuration.

    """
    lines = header.splitlines()
    header = None
    # ignore shebang
    if lines[0].startswith("#!"):
        header = lines[0]
        lines = lines[1:]
    kwargs = {}
    for l in lines:
        if l.startswith("#SBATCH"):
            kwargs.update(parse_header_kwarg(l.replace("#SBATCH", "").strip()))
    if eval_types is True:
        return _maybe_eval_types(kwargs)
    return kwargs


def split_script(script, strip=True):
    """Split a script into Slurm header, commands and interpreter

    The split is defined by the first non-comment non-whitespace line.

    Parameters
    ----------
    strip : bool
        Remove blank lines from header.

    Returns
    -------
    Slurm header, command part and interpreter of a Slurm jobscript.

    """
    header = ""
    shebang = ""
    lines = script.splitlines(keepends=True)
    if lines[0].startswith("#!"):
        shebang = lines[0].strip()
        lines = lines[1:]
    for i, line in enumerate(lines):
        if not line.startswith("#") and line.strip():
            break
        header += "" if not line.strip() and strip else line

    return header, "".join(lines[i:]), shebang
