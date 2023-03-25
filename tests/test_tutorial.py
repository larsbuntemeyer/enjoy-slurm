from enjoy_slurm.tutorial import job, jobscript


def test_job():
    expect = (
        "#!/bin/bash\n\n"
        "#SBATCH --job-name=tutorial\n"
        "#SBATCH --time=00:30:00\n"
        "#SBATCH --nodes=1\n"
        "#SBATCH --output=tutorial.%j.out\n"
        "#SBATCH --partition=test\n"
        "#SBATCH --account=ch0636\n"
        "\n"
        'echo "Hello World from (hostname)"\n'
    )
    script = job(partition="test", account="ch0636")
    assert script == expect
    assert jobscript(partition="test", account="ch0636")
