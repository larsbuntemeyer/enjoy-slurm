import pytest

from enjoy_slurm.utils import parse_dependency, kwargs_to_list, handle_sacct_format
from enjoy_slurm.config import default_sacct_format


def test_parse_dependency():
    assert parse_dependency([1, 2, 3]) == ["afterok:1:2:3"]
    assert parse_dependency([1, 2, 3], how="afterany") == ["afterany:1:2:3"]
    assert parse_dependency([1, 2, 3], how="afterany") == ["afterany:1:2:3"]
    assert parse_dependency("afterany:1:2:3") == ["afterany:1:2:3"]


def test_kwargs_to_list():
    kwargs = {"partition": "test", "dependency": [1, 2, 3]}
    assert kwargs_to_list(kwargs) == [
        "--partition",
        "test",
        "--dependency",
        "afterok:1:2:3",
    ]
    kwargs = {"partition": "test", "dependency": [1, 2, 3], "how": "afterany"}
    assert kwargs_to_list(kwargs) == [
        "--partition",
        "test",
        "--dependency",
        "afterany:1:2:3",
    ]


def test_sacct_format():
    assert handle_sacct_format() == ["--format"] + [",".join(default_sacct_format)]
    assert handle_sacct_format(None, {"brief": True}) == ["--brief"]

    test_format = ["jobid", "state"]
    assert handle_sacct_format(test_format) == ["--format"] + [",".join(test_format)]
    # brief overwrites format
    assert handle_sacct_format(test_format, {"brief": True}) == ["--brief"]
