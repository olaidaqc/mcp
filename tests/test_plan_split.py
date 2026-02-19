import sys
import unittest
from pathlib import Path

from mcp_manager.organize import split_plan


def test_split_plan_marks_confirm_for_core(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    core = tmp_path / "a.gguf"
    core.write_bytes(b"x")
    doc = tmp_path / "b.pdf"
    doc.write_text("x", encoding="utf-8")
    plan = [
        {"path": str(core), "category": "Models"},
        {"path": str(doc), "category": "Docs"},
    ]
    rules = {"core_exts": [".gguf"], "large_threshold_bytes": 1024}
    auto, confirm = split_plan(plan, rules)
    assert len(confirm) == 1
    assert confirm[0]["path"].endswith("a.gguf")


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
