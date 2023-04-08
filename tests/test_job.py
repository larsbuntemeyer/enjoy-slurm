from enjoy_slurm import Job
from enjoy_slurm.tutorial import test_script


def test_job():
    job = Job(test_script)
    expect_config = {
        "job-name": "tutorial",
        "time": "00:30:00",
        "nodes": 1,
        "output": "tutorial.%j.out",
        "partition": "main",
        "account": 1234,
    }
    expect_header = (
        "#SBATCH --job-name=tutorial\n"
        "#SBATCH --time=00:30:00\n"
        "#SBATCH --nodes=1\n"
        "#SBATCH --output=tutorial.%j.out\n"
        "#SBATCH --partition=main\n"
        "#SBATCH --account=1234\n"
    )
    expect_command = 'echo "Hello World from $(hostname)"\n'

    expect_job = "#!/bin/bash\n\n" + expect_header + "\n" + expect_command

    assert job.header == expect_header
    assert job.config == expect_config
    assert job.command == expect_command
    assert job.job == expect_job

    script = "#SBATCH --account=my_account\n" "print('Hello World from python')"
    job = Job(script, interpreter="python", partition="shared")
    expect_config = {"account": "my_account", "partition": "shared"}
    assert job.config == expect_config
    assert job.shebang == "#!/usr/bin/env python"
    assert job.interpreter == "python"
