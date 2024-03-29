import tempfile
from os import path as op

from .parser import create_header, kwargs_to_slurm


def job(shebang=None, command=None, **kwargs):
    """Creates a tutorial job"""

    if shebang is None:
        shebang = "#!/bin/bash"
    if command is None:
        command = 'echo "Hello World from $(hostname)"\n'

    config = {
        "job_name": "tutorial",
        "time": "00:30:00",
        "nodes": 1,
        "output": "tutorial.%j.out",
    }
    config.update(kwargs)

    slurm_args = kwargs_to_slurm(config)
    header = create_header(slurm_args)

    return shebang + "\n\n" + header + "\n" + command


def jobscript(shebang="#!/bin/bash", filename=None, **kwargs):
    if filename is None:
        filename = op.join(tempfile.mkdtemp(), "jobscript.sh")

    content = job(shebang, **kwargs)

    with open(filename, "w") as f:
        f.write(content)

    return filename


test_script = jobscript(partition="main", account="1234")
