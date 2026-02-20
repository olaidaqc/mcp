import sys
import unittest
from pathlib import Path

from mcp_manager.aihub_scan import build_plan


def test_non_ai_file_is_ignored(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    file_path = tmp_path / "game.exe"
    file_path.write_bytes(b"x")
    rules = {"core_exts": [], "ai_keywords": ["llama"], "tool_keywords": [], "exclude_exts": [], "exclude_paths": []}
    plan = build_plan([file_path], rules, tmp_path)
    assert plan == []


def test_ai_file_is_classified(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    file_path = tmp_path / "ollama.exe"
    file_path.write_bytes(b"x")
    rules = {"core_exts": [], "ai_keywords": ["ollama"], "tool_keywords": ["ollama"], "exclude_exts": [], "exclude_paths": []}
    plan = build_plan([file_path], rules, tmp_path)
    assert plan[0]["category"] == "Tools"


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
