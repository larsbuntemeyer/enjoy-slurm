import pytest

from enjoy_slurm.utils import parse_dependency, kwargs_to_list


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
