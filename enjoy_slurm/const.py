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
