import sys
import unittest
from pathlib import Path

from mcp_manager.aihub_learn import learn_from_confirmed, load_learned


def test_learned_keywords_updated(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    items = [{"path": str(tmp_path / "new-ollama-tool.exe"), "category": "Tools"}]
    learn_from_confirmed(tmp_path, items)
    learned = load_learned(tmp_path)
    assert "ollama" in learned["Tools"]


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
