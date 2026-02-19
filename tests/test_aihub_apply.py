import sys
import unittest
from pathlib import Path

from mcp_manager.aihub_apply import apply_plan


def test_apply_plan_moves_and_writes_sidecar(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    src = tmp_path / "qwen.gguf"
    src.write_bytes(b"x")
    plan = [{"path": str(src), "category": "Models", "confirm": False}]
    apply_plan(plan, tmp_path)
    moved = tmp_path / "Models" / "qwen.gguf"
    assert moved.exists()
    assert (tmp_path / "Models" / "qwen.gguf.aiinfo.txt").exists()
    assert (tmp_path / "_reports" / "index.jsonl").exists()


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
