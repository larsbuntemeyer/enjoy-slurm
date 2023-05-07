enjoy-slurm
==============================
[![Build Status](https://github.com/larsbuntemeyer/enjoy-slurm/workflows/Tests/badge.svg)](https://github.com/larsbuntemeyer/enjoy-slurm/actions)
[![codecov](https://codecov.io/gh/larsbuntemeyer/enjoy-slurm/branch/main/graph/badge.svg)](https://codecov.io/gh/larsbuntemeyer/enjoy-slurm)
[![License:MIT](https://img.shields.io/badge/License-MIT-lightgray.svg?style=flt-square)](https://opensource.org/licenses/MIT)
[![pypi](https://img.shields.io/pypi/v/enjoy-slurm.svg)](https://pypi.org/project/enjoy-slurm)
[![Documentation Status](https://readthedocs.org/projects/enjoy-slurm/badge/?version=latest)](https://enjoy-slurm.readthedocs.io/en/latest/?badge=latest)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/larsbuntemeyer/enjoy-slurm/main.svg)](https://results.pre-commit.ci/latest/github/larsbuntemeyer/enjoy-slurm/main)

`enjoy-slurm` is a naive slurm control package for python. It does interact with Slurm exactly as any user would do, simply through the command
line tools and arguments. That's why we call it *naive*. However, it should avoid having to rewrite some scripts required to submit and control many
Slurm jobs on an HPC computer. This package is a successor of the retired [HPC scheduler package](https://github.com/larsbuntemeyer/hpc-scheduler).

## Features

* Use `sbatch`, `sacct`, `scontrol` etc. directly from python with a pythonic API.
* Parse command outputs into python objects like pandas DataFrames or dictionaries.

## Examples

```python
import enjoy_slurm as slurm

jobid = slurm.sbatch("job.sh", partition="compute", account="my_account")
acct = slurm.sacct(jobid=jobid)

# run another job that depends on the first
jobid1 = slurm.sbatch(
    "another_job.sh", dependency=jobid, partition="shared", account="my_account"
)
acct1 = slurm.sacct(jobid=jobid1)
```

## Related projects

* [pyslurm](https://github.com/PySlurm/pyslurm)
* [simple_slurm](https://github.com/amq92/simple_slurm)
* [ipyslurm](https://github.com/auneri/ipyslurm)

--------

<p><small>Project based on the <a target="_blank" href="https://github.com/jbusecke/cookiecutter-science-project">cookiecutter science project template</a>.</small></p>
