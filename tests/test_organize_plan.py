import sys
import unittest
from pathlib import Path

from mcp_manager.organize import save_plan, load_plan


def test_save_and_load_plan(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    plan = {"auto": [{"path": "a"}], "confirm": []}
    save_plan(tmp_path, plan)
    loaded = load_plan(tmp_path)
    assert loaded["auto"][0]["path"] == "a"


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
