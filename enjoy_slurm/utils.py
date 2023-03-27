import pandas as pd
from itertools import groupby
import subprocess
import numpy as np
from .parser import parse_scontrol_show


interp_dict = {
    "bash": ["/bin/sh", "bash"],
    "python": ["python"],
    "python3": ["python3"],
    "python2": ["python2"],
}


def interp_from_shebang(first_line):
    for k, v in interp_dict.items():
        for i in v:
            if i in first_line:
                return k
    return None


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
