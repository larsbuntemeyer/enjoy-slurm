import pytest
import enjoy_slurm as slurm
from . import requires_levante


@requires_levante
def test_sbatch():
    jobid = slurm.sbatch(wrap="echo Hello World", partition="shared", account="ch0636")
    print(jobid)


@pytest.mark.parametrize("partition", ["compute", "shared"])
@requires_levante
def test_partitions(partition):
    partitions = slurm.scontrol.show(partition=partition)
    assert partition in partitions
