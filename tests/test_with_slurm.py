from . import requires_slurm

import enjoy_slurm as slurm


@requires_slurm
def test_sbatch():
    pass
