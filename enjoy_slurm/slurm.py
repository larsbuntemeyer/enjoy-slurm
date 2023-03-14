import logging
import subprocess

from .utils import kwargs_to_list, parse_sacct, execute, create_scontrol_func


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
    logging.info(f"jobid: {jobid}")
    return jobid


def sacct(jobid=None, format=None, **kwargs):
    """
    Accounting data for all jobs and job steps in the Slurm job accounting log or Slurm database

    Parameters
    ----------
    jobid : int
        If provided, displays information about the specified job.
    format : list
        List of columns that can be specified.

    Returns
    -------
    sacct info : DataFrame
        Slurm accounting data.

    """
    if format is None and not kwargs:
        format = ["jobid", "elapsed", "ncpus", "ntasks", "state", "end", "jobname"]
    command = ["sacct", "--parsable2"] + kwargs_to_list(kwargs)
    if format:
        if not isinstance(format, list):
            format = [format]
        command += ["--format=" + ",".join(format)]
    if jobid is not None:
        command += ["-j", str(jobid)]
    output = execute(command)
    return parse_sacct(output)


class SControl(type):
    def __getattr__(cls, key):
        return create_scontrol_func(key)


class scontrol(metaclass=SControl):
    pass
