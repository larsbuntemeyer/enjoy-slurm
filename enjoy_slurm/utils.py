import pandas as pd
from io import StringIO
from itertools import groupby
import subprocess
from .config import default_sacct_format

delimiter = "|"

own_kwargs = ["how"]


def handle_sacct_format(format=None, kwargs={}):
    if format == "brief" or "brief" in kwargs:
        return ["--brief"]  # + jobsteps * ["--format", "jobname"]
    format = format or default_sacct_format
    if format:
        if not isinstance(format, list):
            format = [format]
        return ["--format"] + [",".join(format)]
    return []


def parse_sacct(csv, jobsteps=None):
    """convert parsable sacct output to dataframe"""
    df = pd.read_csv(StringIO(csv), delimiter=delimiter)
    if jobsteps == "minimal":
        df = df[df["JobID"].str.isnumeric()].reset_index()
    return df


def parse_dependency(ids, how=None):
    """parse dependency arguments to sbatch command line"""
    if isinstance(ids, str):
        return [ids]
    if how is None:
        how = "afterok"
    if not isinstance(ids, list):
        ids = [ids]
    return [":".join([how] + [str(id) for id in ids])]


def parse_slurm_arg(a):
    """parse slurm arguments to str or list of str with colons"""
    if isinstance(a, list):
        return ":".join([str(x) for x in a])
    return [str(a)]


def kwargs_to_list(d):
    """parse arguments to command line arguments for sbatch"""
    r = []
    for k, v in d.items():
        # ignore own kwargs
        if k in own_kwargs:
            continue
        flag = "--" + k.replace("_", "-")
        r += [flag]
        if k == "dependency" and v is not None:
            r += parse_dependency(v, d.get("how", None))
            continue
        if k == "kill_on_invalid_dep" and not isinstance(v, str):
            r += ["no"] if v is False else ["yes"]
            continue
        if v is not True:
            r += parse_slurm_arg(v)
        # r += [flag]
    return r


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


def create_scontrol_func(name):
    def func(*args, **kwargs):
        command = ["scontrol", name] + list(args)  # + kwargs_to_list(kwargs)
        for (
            k,
            v,
        ) in kwargs.items():
            command += [str(k), str(v)]
        return parse_scontrol_show(execute(command))

    return func


def execute(command, return_type="stdout", decode=True):
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if output.returncode != 0:
        raise Exception(output.stderr.decode("utf-8"))
    if return_type == "output":
        return output
    if return_type == "stdout":
        return output.stdout.decode("utf-8")
