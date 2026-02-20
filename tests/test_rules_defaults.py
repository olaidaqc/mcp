import sys
import unittest
from pathlib import Path

from mcp_manager.aihub_rules import load_rules, ensure_rules


def test_ensure_rules_creates_rules_file(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    ensure_rules(tmp_path)
    assert (tmp_path / "_rules" / "rules.json").exists()


def test_load_rules_includes_ai_only_defaults(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    ensure_rules(tmp_path)
    rules = load_rules(tmp_path)
    assert "exclude_exts" in rules
    assert "ai_keywords" in rules


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
