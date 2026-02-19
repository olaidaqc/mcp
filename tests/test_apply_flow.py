import sys
import unittest
from pathlib import Path

from mcp_manager.organize import apply_auto


def test_apply_auto_moves_files(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    src = tmp_path / "tool.zip"
    src.write_text("x", encoding="utf-8")
    plan = {"auto": [{"path": str(src), "category": "Tools"}], "confirm": []}
    moved = apply_auto(tmp_path, plan)
    assert (tmp_path / "Tools" / "tool.zip").exists()
    assert moved == 1


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
