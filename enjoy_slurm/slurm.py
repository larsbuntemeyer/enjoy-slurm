import logging
import subprocess

from .utils import kwargs_to_list, parse_sacct, execute


def sbatch(jobscript, *args, **kwargs):
    """
    Submit a batch script to Slurm

    Parameters
    ----------
    jobscript : str
        Path to jobscript file.

    Returns
    -------
    jobid: int
        Slurm jobid.

    """
    logging.info("submitting: " + jobscript)
    command = (
        ["sbatch", "--parsable"] + list(args) + kwargs_to_list(kwargs) + [jobscript]
    )
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
    format: list
        List of columns that can be specified.

    Returns
    -------
    sacct info: DataFrame
        Slurm accounting data.

    """
    if format is None and not kwargs:
        format = ["jobid", "elapsed", "ncpus", "ntasks", "state", "end", "jobname"]
    command = ["sacct", "--parsable2"] + kwargs_to_list(kwargs)
    if format:
        command += ["--format=" + ",".join(format)]
    if jobid is not None:
        command += ["-j", str(jobid)]
    output = execute(command)
    return parse_sacct(output)
