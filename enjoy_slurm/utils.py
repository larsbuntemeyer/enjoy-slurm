import pandas as pd
from io import StringIO
from itertools import groupby
import subprocess
from .config import default_sacct_format
import numpy as np

from .parser import parse_dependency

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
    r = []
    list_concat = ","
    for k, v in d.items():
        # ignore own kwargs
        if k in own_kwargs:
            continue
        flag = "--" + k.replace("_", "-")
        if k == "dependency" and v is not None:
            r += [flag]
            r += parse_dependency(v)
            continue
        if k == "kill_on_invalid_dep" and not isinstance(v, str):
            if v is not None:
                r += [flag]
                r += ["no"] if v is False else ["yes"]
            continue
        if v:
            r += [flag]
            r += parse_slurm_arg(v, list_concat)
            continue
        if v is False:
            continue
        # r += [flag]
    return r


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


def execute(command, return_type="stdout", decode=True, verbose=False):
    if verbose is True:
        print(f"executing: {' '.join(command)}")
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if output.returncode != 0:
        raise Exception(output.stderr.decode("utf-8"))
    if return_type == "output":
        return output
    if return_type == "stdout":
        return output.stdout.decode("utf-8")
