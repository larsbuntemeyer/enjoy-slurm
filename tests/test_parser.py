from enjoy_slurm.config import default_sacct_format
from enjoy_slurm.parser import (
    _parse_dependency,
    args_to_list,
    create_header,
    handle_sacct_format,
    kwargs_to_list,
    kwargs_to_slurm,
    parse_header,
    split_script,
)


def test_parse_dependency():
    assert _parse_dependency([1, 2, 3]) == "afterok:1:2:3"
    assert _parse_dependency((None, [1, 2, 3])) == "afterok:1:2:3"
    assert _parse_dependency(("afterany", [1, 2, 3])) == "afterany:1:2:3"
    assert _parse_dependency("afterany:1:2:3") == "afterany:1:2:3"


def test_kwargs_to_list():
    assert kwargs_to_list({"hello": True}) == ["--hello"]
    assert kwargs_to_list({"hello": False}) == []
    assert kwargs_to_list({"hello": 1}) == ["--hello", "1"]

    kwargs = {"partition": "test", "dependency": [1, 2, 3]}
    assert kwargs_to_list(kwargs) == [
        "--partition",
        "test",
        "--dependency",
        "afterok:1:2:3",
    ]
    kwargs = {"partition": "test", "dependency": ("afterany", [1, 2, 3])}
    assert kwargs_to_list(kwargs) == [
        "--partition",
        "test",
        "--dependency",
        "afterany:1:2:3",
    ]
    kwargs = {
        "partition": "test",
        "dependency": ("afterany", [1, 2, 3]),
        "kill_on_invalid_dep": True,
    }
    assert kwargs_to_list(kwargs) == [
        "--partition",
        "test",
        "--dependency",
        "afterany:1:2:3",
        "--kill-on-invalid-dep",
        "yes",
    ]
    kwargs = {"kill_on_invalid_dep": False}
    assert kwargs_to_list(kwargs) == ["--kill-on-invalid-dep", "no"]
    kwargs = {"kill_on_invalid_dep": True}
    assert kwargs_to_list(kwargs) == ["--kill-on-invalid-dep", "yes"]
    kwargs = {"kill_on_invalid_dep": "no"}
    assert kwargs_to_list(kwargs) == ["--kill-on-invalid-dep", "no"]
    kwargs = {"kill_on_invalid_dep": "yes"}
    assert kwargs_to_list(kwargs) == ["--kill-on-invalid-dep", "yes"]
    kwargs = {"kill_on_invalid_dep": None}
    assert kwargs_to_list(kwargs) == []


def test_kwargs_to_slurm():
    kwargs = {
        "partition": "test",
        "dependency": ("afterany", [1, 2, 3]),
        "kill_on_invalid_dep": True,
        "hold": True,
    }
    expect = {
        "--partition": "test",
        "--dependency": "afterany:1:2:3",
        "--kill-on-invalid-dep": "yes",
        "--hold": "",
    }
    assert kwargs_to_slurm(kwargs) == expect


def test_args_to_list():
    assert args_to_list(("--partition=shared",)) == ["--partition", "shared"]
    assert args_to_list(("--partition shared",)) == ["--partition", "shared"]
    assert args_to_list(("--partition shared", "--dependency=afterok:1:2:3")) == [
        "--partition",
        "shared",
        "--dependency",
        "afterok:1:2:3",
    ]
    assert args_to_list(("--partition shared", ["--dependency", "afterok:1:2:3"])) == [
        "--partition",
        "shared",
        "--dependency",
        "afterok:1:2:3",
    ]


def test_sacct_format():
    assert handle_sacct_format() == ["--format"] + [",".join(default_sacct_format)]
    assert handle_sacct_format(None, {"brief": True}) == ["--brief"]

    test_format = ["jobid", "state"]
    assert handle_sacct_format(test_format) == ["--format"] + [",".join(test_format)]
    # brief overwrites format
    assert handle_sacct_format(test_format, {"brief": True}) == ["--brief"]


def test_split():
    shebang = "#!/usr/bin/env python          \n"
    header = (
        "#SBATCH --partition=compute    \n"
        "#SBATCH --nodes 1              \n"
        "#SBATCH--ntasks 12             \n"
        "#SBATCH    --time    01:00:00  \n"
        "#SBATCH --mem-per-cpu=1920     \n"
        "                               \n"
        "#comment                       \n"
        "#SBATCH --account       1234   \n"
        "       \n"
        "          \n"
    )
    command = "echo Hello World\n"

    h, c, s = split_script(shebang + header + command, strip=False)
    assert h == header
    assert c == command
    assert s == shebang.strip()
    h, c, s = split_script(shebang + header + command, strip=True)
    assert c == command
    assert s == shebang.strip()


def test_parse_header():
    header = (
        "#!/usr/bin/env python          \n"
        "#SBATCH --partition=compute  # this is the partition   \n"
        "#SBATCH --nodes 1              \n"
        "#SBATCH--ntasks 12             \n"
        "#SBATCH    --time    01:00:00  \n"
        "#SBATCH --mem-per-cpu=1920     \n"
        "                               \n"
        "#comment                       \n"
        "#SBATCH --account       1234   \n"
        "       \n"
        "          \n"
    )

    expect = {
        "partition": "compute",
        "nodes": "1",
        "ntasks": "12",
        "time": "01:00:00",
        "mem-per-cpu": "1920",
        "account": "1234",
    }
    args = parse_header(header, eval_types=False)
    assert args == expect

    expect = {
        "partition": "compute",
        "nodes": 1,
        "ntasks": 12,
        "time": "01:00:00",
        "mem-per-cpu": 1920,
        "account": 1234,
    }
    args = parse_header(header, eval_types=True)
    assert args == expect


def test_create_header():
    kwargs = {
        "partition": "test",
        "dependency": ("afterany", [1, 2, 3]),
        "kill_on_invalid_dep": True,
        "hold": True,
    }
    expect = (
        "#SBATCH --partition=test\n"
        "#SBATCH --dependency=afterany:1:2:3\n"
        "#SBATCH --kill-on-invalid-dep=yes\n"
        "#SBATCH --hold\n"
    )
    header = create_header(kwargs_to_slurm(kwargs))
    assert header == expect
