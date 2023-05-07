from enjoy_slurm.config import shebang_dict
from enjoy_slurm.utils import interp_from_shebang


def test_shebang():
    assert interp_from_shebang("#!/bin/bin/env python3") == "python3"
    assert interp_from_shebang("#!/bin/bin/env python2") == "python2"
    assert interp_from_shebang("#!/bin/bin/env python") == "python"
    for k, v in shebang_dict.items():
        assert interp_from_shebang(v) == k
