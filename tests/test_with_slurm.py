import pytest
import enjoy_slurm as slurm
from . import hostname, requires_slurm, on_levante, requires_levante


test_kwargs = {
    "levante": {"partitions": ["compute", "shared"]},
    "docker": {"partitions": ["debug", "normal"]},
}

print(hostname)


@requires_slurm
def test_sbatch():
    if on_levante:
        kwargs = {"partition": "shared", "account": "ch0636"}
    else:
        kargs = {}
    jobid = slurm.sbatch(wrap="echo Hello World", **kwargs)
    print(jobid)


@requires_slurm
def test_partitions():
    if on_levante:
        partitions = test_kwargs["levante"]["partitions"]
    else:
        partitions = test_kwargs["docker"]["partitions"]
    for p in partitions:
        pdict = slurm.scontrol.show(partition=p)
        assert p in pdict
