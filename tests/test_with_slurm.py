from enjoy_slurm import Job, sacct, sbatch

from . import hostname, on_levante, requires_slurm

test_kwargs = {
    "levante": {"partitions": ["compute", "shared"]},
    "docker": {"partitions": ["debug", "normal"]},
}

print(hostname)

if on_levante:
    kwargs = {"partition": "shared", "account": "ch0636"}
else:
    kwargs = {}


@requires_slurm
def test_sbatch():
    if on_levante:
        kwargs = {"partition": "shared", "account": "ch0636"}
    else:
        kwargs = {}
    jobid = sbatch(wrap="echo Hello World", **kwargs)
    print(jobid)


# @requires_slurm
# def test_partitions():
#    if on_levante:
#        partitions = test_kwargs["levante"]["partitions"]
#    else:
#        partitions = test_kwargs["docker"]["partitions"]
#    for p in partitions:
#        pdict = scontrol.show(partition=p)
#        assert p in pdict


@requires_slurm
def test_sacct():
    jobid = sbatch(wrap="echo Hello World", **kwargs)
    sacct(jobid=jobid)
    # scon = scontrol.show(jobid=jobid)
    # assert str(jobid) in scon


@requires_slurm
def test_job():
    import time

    jobid = sbatch(wrap="echo Hello World", **kwargs)
    time.sleep(5)
    job = Job(jobid=jobid)
    assert job.jobid == jobid
    assert job.partition
    assert job.account
