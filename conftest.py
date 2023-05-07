# content of conftest.py
import warnings

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "-E",
        action="store",
        metavar="NAME",
        help="only run tests matching the environment NAME.",
    )


def pytest_configure(config):
    # register additional markers
    config.addinivalue_line(
        "markers", "env(NAME): only run test if environment NAME matches"
    )
    config.addinivalue_line(
        "markers", "xfail_env(NAME): known failure for environment NAME"
    )


def pytest_runtest_setup(item):
    warnings.filterwarnings(
        "ignore", message="Port 8787 is already in use", category=UserWarning
    )
    env = item.config.getoption("-E")
    envnames = sum(
        [
            mark.args[0] if isinstance(mark.args[0], list) else [mark.args[0]]
            for mark in item.iter_markers(name="env")
        ],
        [],
    )
    if (
        None not in envnames
        and (env is None and envnames)
        or (env is not None and env not in envnames)
    ):
        pytest.skip("test requires env in %r" % envnames)
    else:
        xfail = {}
        [xfail.update(mark.args[0]) for mark in item.iter_markers(name="xfail_env")]
        if env in xfail:
            item.add_marker(pytest.mark.xfail(reason=xfail[env]))
