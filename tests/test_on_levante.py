import pytest
import enjoy_slurm as slurm
from . import hostname, requires_slurm, on_levante, requires_levante


test_kwargs = {
    "lvt.dkrz.de": {"partitions": ["compute", "shared"]},
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


@pytest.mark.parametrize("partition", test_kwargs[hostname]["partitions"])
@requires_slurm
def test_partitions(partition):
    partitions = slurm.scontrol.show(partition=partition)
    assert partition in partitions
