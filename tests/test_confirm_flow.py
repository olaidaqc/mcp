import sys
import unittest
from pathlib import Path

from mcp_manager.organize import apply_confirm


def test_apply_confirm_moves_selected(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    src = tmp_path / "model.gguf"
    src.write_bytes(b"x")
    plan = {"auto": [], "confirm": [{"path": str(src), "category": "Models"}]}
    moved = apply_confirm(tmp_path, plan, [str(src)])
    assert (tmp_path / "Models" / "model.gguf").exists()
    assert moved == 1
    assert plan["confirm"] == []


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
