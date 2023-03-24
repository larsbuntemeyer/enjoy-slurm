import pandas as pd
from io import StringIO
from .config import delimiter
import numpy as np


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
