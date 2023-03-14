import logging
import subprocess

from .utils import kwargs_to_list, parse_sacct, execute


def sbatch(jobscript, *args, **kwargs):
    logging.info("submitting: " + jobscript)
    command = (
        ["sbatch", "--parsable"] + list(args) + kwargs_to_list(kwargs) + [jobscript]
    )
    jobid = int(execute(command))
    logging.info(f"jobid: {jobid}")
    return jobid


def sacct(jobid=None, format=None, **kwargs):
    if format is None and not kwargs:
        format = ["jobid", "elapsed", "ncpus", "ntasks", "state", "end", "jobname"]
    print(format)
    command = ["sacct", "--parsable2"] + kwargs_to_list(kwargs)
    if format:
        command += ["--format=" + ",".join(format)]
    if jobid is not None:
        command += ["-j", str(jobid)]
    output = execute(command)
    return parse_sacct(output)


class Scheduler:
    def __init__(self):
        pass


class Job:
    def __init__(self):
        pass
