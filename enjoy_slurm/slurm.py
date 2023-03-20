import subprocess
import os
from os import path as op
import copy

from .utils import (
    kwargs_to_list,
    parse_sacct,
    execute,
    create_scontrol_func,
    handle_sacct_format,
)


def sbatch(jobscript=None, *args, **kwargs):
    """
    Submit a batch script to Slurm

    Many sbatch command line arguments can be passed via **kwargs. For example,
    the ``partion="compute"`` argument would be translated into the
    ``--partion=compute`` command line argument for sbatch. For all available
    options, please consult the sbatch manpage. However, some of the most useful
    argument are also documented here.


    Parameters
    ----------
    jobscript : str
        Path to jobscript file. If no jobscript is provided, you can use the
        ``wrap`` keyword to directly pass shell commands.

    Returns
    -------
    jobid : int
        Slurm jobid.

    """
    if jobscript is None:
        jobscript = []
    else:
        jobscript = [jobscript]

    command = ["sbatch", "--parsable"] + list(args) + kwargs_to_list(kwargs) + jobscript
    jobid = int(execute(command))

    return jobid


def sacct(jobid=None, format=None, steps=None, **kwargs):
    """
    Accounting data for all jobs and job steps in the Slurm job accounting log or Slurm database

    Parameters
    ----------
    jobid : int
        If provided, displays information about the specified job.
    format : list
        List of columns that should be shown.
    steps : str
        Jobsteps that should be shown. If ``None``, all jobsteps are returned.
        Use ``mininmal`` to return only the main inclusive step.

    Returns
    -------
    sacct info : DataFrame
        Slurm accounting data.

    """
    # return handle_sacct_format(format, kwargs)
    command = (
        ["sacct", "--parsable2"]
        + handle_sacct_format(format, kwargs)
        + kwargs_to_list(kwargs)
    )

    if jobid is not None:
        command += ["-j", str(jobid)]

    output = execute(command)

    return parse_sacct(output, steps)


def jobinfo(jobid=None, format=None, steps="minimal", **kwargs):
    """
    Accounting data for all jobs and job steps.

    Parameters
    ----------
    jobid : int
        If provided, displays information about the specified job.
    format : list
        List of columns that should be shown.
    steps : str
        Jobsteps that should be shown. If ``None``, all jobsteps are returned.
        Use ``mininmal`` to return only the main inclusive step.

    Returns
    -------
    sacct info : dict
        Slurm accounting data.

    """
    if not isinstance(format, list):
        format = [format]
    if format is not None and "JobID" not in format:
        format.append("JobID")
    acct = sacct(jobid, format, steps, **kwargs)

    return acct.set_index("JobID").to_dict(orient="index")


class SControl(type):
    def __getattr__(cls, key):
        return create_scontrol_func(key)


class scontrol(metaclass=SControl):
    """
    View or modify Slurm configuration and state
    """

    def show(*args, **kwargs):
        """
        Display state of identified entity, default is all records.

        Entity may be "aliases", "assoc_mgr", "bbstat", "burstBuffer",
        "config", "daemons", "dwstat", "federation", "frontend",
        "hostlist", "hostlistsorted", "hostnames", "job", "node",
        "partition", "reservation", "slurmd", "step", or "topology".

        """
        return create_scontrol_func("show")(*args, **kwargs)


class Job:
    def __init__(self, job=None, jobid=None, interpreter=None, **kwargs):
        self.job = job
        self.jobid = jobid
        self.interpreter = interpreter
        if interpreter is None:
            self.interpreter = "#!/bin/sh"
        if interpreter == "python":
            self.interpreter = "#!/usr/bin/env python"
        self.wrap = None
        if op.isfile(job):
            self.jobscript = job
        else:
            self.jobscript = None
            self.wrap = job
        if self.interpreter is not None:
            self.wrap = self.interpreter + "\n" + self.wrap
        self.kwargs = kwargs

    def __repr__(self):
        txt = f"job         : {self.job}\n"
        txt += f"jobid       : {self.jobid}\n"
        txt += f"interpreter : {self.interpreter}"
        return txt

    def sbatch(self, **kwargs):
        jobid = sbatch(self.jobscript, wrap=self.wrap, **kwargs)
        if self.jobid is None:
            self.jobid = jobid
            return self
        job = copy.copy(self)
        job.jobid = jobid
        return job
