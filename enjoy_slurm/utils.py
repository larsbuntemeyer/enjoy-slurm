import pandas as pd
from io import StringIO
from itertools import groupby
import subprocess

delimiter = "|"


def parse_sacct(csv):
    """convert parsable sacct output to dataframe"""
    try:
        return pd.read_csv(StringIO(csv), delimiter=delimiter)
    except:
        return csv


def parse_dependency(ids, how=None):
    """parse dependency arguments to sbatch command line"""
    if how is None:
        how = "afterok"
    if not isinstance(ids, list):
        ids = [ids]
    return ":".join([how] + [str(id) for id in ids])


def parse_slurm_arg(a):
    """parse slurm arguments to str or list of str with colons"""
    if isinstance(a, list):
        return ":".join([str(x) for x in a])
    return str(a)


def kwargs_to_list(d):
    """parse arguments to command line arguments for sbatch"""
    r = []
    for k, v in d.items():
        flag = "--" + k.replace("_", "-")
        if k == "dependency" and v is not None:
            flag += "=" + parse_dependency(v, d.get("how", None))
        elif v is not True:
            flag += "=" + parse_slurm_arg(v)
        r += [flag]
    return r


def parse_scontrol_show(output):
    """parse scontrol output"""
    # create list of entries
    entries = ["".join(list(g)) for k, g in groupby(output.splitlines(), key=bool) if k]
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
    return results


def create_scontrol_func(name):
    def func(*args, **kwargs):
        command = (
            ["scontrol", name]
            + list(args)
            + [str(k) + "=" + str(v) for k, v in kwargs.items()]
        )  # + kwargs_to_list(kwargs)
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
