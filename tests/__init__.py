"""Unit test package for enjoy-slurm."""

import pytest

import subprocess
import socket


def _cmlorskip(command):
    try:
        commands = [command, "-V"]
        output = subprocess.run(
            commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        has = True
    except FileNotFoundError:
        has = False
    func = pytest.mark.skipif(not has, reason=f"requires slurm")
    return has, func


def _machine(machine):
    try:
        host = socket.gethostname().split(".", 1)[1]
        on = host == machine
    except Exception:
        on = False
    func = pytest.mark.skipif(not on, reason=f"no on {machine}")
    return on, func


has_slurm, requires_slurm = _cmlorskip("sinfo")
on_levante, requires_levante = _machine("lvt.dkrz.de")
hostname = socket.gethostname()
