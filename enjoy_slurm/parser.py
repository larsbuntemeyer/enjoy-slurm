import pandas as pd
from io import StringIO
from .config import delimiter
import numpy as np
import re
import pandas as pd


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
        return [ids]
    if isinstance(ids, tuple):
        how, ids = ids
    if not how:
        how = "afterok"
    if not isinstance(ids, list):
        ids = [ids]
    return [":".join([how] + list(map(str, ids)))]


def parse_slurm_arg(a, list_concat=","):
    """parse slurm arguments to str or list of str with colons"""
    if isinstance(a, (list, tuple)):
        return [list_concat.join(map(str, a))]
    if a is True:
        return []
    return [str(a)]


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
