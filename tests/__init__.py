"""Unit test package for enjoy-slurm."""

import pytest

import subprocess


def _cmlorskip(command):
    try:
        commands = [command, "-V"]
        output = subprocess.run(
            commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        has = True
    except ImportError:  # pragma: no cover
        has = False
    func = pytest.mark.skipif(not has, reason=f"requires slurm")
    return has, func


has_slurm, requires_slurm = _cmlorskip("sinfo")
