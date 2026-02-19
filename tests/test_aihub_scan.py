import sys
import unittest
from pathlib import Path

from mcp_manager.aihub_scan import build_plan


def test_build_plan_classifies_model_and_doc(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    model = tmp_path / "llama.gguf"
    model.write_bytes(b"x")
    doc = tmp_path / "llama_guide.pdf"
    doc.write_text("x", encoding="utf-8")
    rules = {
        "core_exts": [".gguf"],
        "keywords": ["llama"],
        "large_threshold_bytes": 1024,
    }
    plan = build_plan([model, doc], rules, tmp_path)
    assert plan[0]["category"] == "Models"
    assert plan[1]["category"] == "Docs"


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
