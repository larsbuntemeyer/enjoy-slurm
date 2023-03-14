import pandas as pd
from io import StringIO

delimiter = "|"


def parse_sacct(csv):
    """convert parsable sacct output to dataframe"""
    return pd.read_csv(StringIO(csv), delimiter=delimiter)


def parse_dependency(ids, how=None):
    if how is None:
        how = "afterok"
    if not isinstance(ids, list):
        ids = [ids]
    return ":".join([how] + [str(id) for id in ids])


def parse_slurm_arg(a):
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
