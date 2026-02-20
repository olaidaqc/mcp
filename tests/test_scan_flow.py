import sys
import unittest
from pathlib import Path

from mcp_manager.organize import run_scan


def test_run_scan_saves_plan(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    sample = tmp_path / "qwen.gguf"
    sample.write_bytes(b"x")
    env = {
        "AI_HUB_ROOT": str(tmp_path),
        "AI_SCAN_ROOTS": str(tmp_path),
    }
    plan = run_scan(env)
    assert plan["auto"] == []
    assert plan["confirm"][0]["path"].endswith("qwen.gguf")


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
