import logging
import subprocess

from .utils import kwargs_to_list, parse_sacct

# define job states
UNKNOWN = -2
FAILED = -1
COMPLETED = 0
RUNNING = 1
PENDING = 2

LOGLEV = {
    COMPLETED: logging.getLevelName("INFO"),
    FAILED: logging.getLevelName("ERROR"),
    UNKNOWN: logging.getLevelName("WARNING"),
    PENDING: logging.getLevelName("INFO"),
    RUNNING: logging.getLevelName("INFO"),
}

### SLURM definitions ####
SLURM_STATES = {
    "FAILED": FAILED,
    "COMPLETED": COMPLETED,
    "RUNNING": RUNNING,
    "PENDING": PENDING,
}

### known Schedulers ####
SCHEDULER = {
    "SLURM": {
        "batch": "sbatch --parsable",
        "accounting": "sacct --parsable2 --format=jobid,elapsed,ncpus,ntasks,state,end,jobname -j",
        "control": "scontrol show jobid -dd",
        # "tpl": SLURM_TEMPLATE,
        # "states": SLURM_STATES,
        # "comment": SLURM_COMMENT,
        # "ctr_list": SLURM_CONTROL,
        # "defaults": SLURM_DEFAULTS,
    }
}


def execute(command, return_type="stdout", decode=True):
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if output.returncode != 0:
        raise Exception(output.stderr)
    if return_type == "output":
        return output
    if return_type == "stdout":
        return output.stdout.decode("utf-8")


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
