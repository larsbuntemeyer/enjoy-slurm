import logging


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


def submit(jobscript, *args, **kwargs):
    def dict_to_list(x):
        """parse arguments to command line arguments for sbatch"""
        r = []
        for x in zip(x.keys(), x.values()):
            if x[1]:
                r += ["--" + x[0].replace("_", "-") + "=" + str(x[1])]
        return r

    logging.info("submitting: " + jobscript)
    commands = (
        ["sbatch", "--parsable"] + list(args) + dict_to_list(kwargs) + [jobscript]
    )
    output = subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if output.returncode != 0:
        raise Exception(output.stderr)
    jobid = int(output.stdout)
    logging.info(f"jobid: {jobid}")
    return jobid


class Scheduler:
    def __init__(self):
        pass


class Job:
    def __init__(self):
        pass
