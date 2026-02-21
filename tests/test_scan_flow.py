import sys
import unittest
from pathlib import Path

from mcp_manager.organize import run_scan


def test_run_scan_respects_user_home_excludes(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    desktop = tmp_path / "Desktop"
    (desktop / "claude").mkdir(parents=True, exist_ok=True)
    (desktop / "claude" / "llama.txt").write_text("llama", encoding="utf-8")
    (desktop / "keep").mkdir(parents=True, exist_ok=True)
    (desktop / "keep" / "llama.txt").write_text("llama", encoding="utf-8")
    env = {
        "AI_HUB_ROOT": str(tmp_path),
        "AI_SCAN_ROOTS": str(desktop),
        "AI_USER_HOME": str(tmp_path),
    }
    plan = run_scan(env)
    paths = [p["path"].replace("\\", "/") for p in plan["confirm"]]
    assert any("keep/llama.txt" in p for p in paths)
    assert all("claude/llama.txt" not in p for p in paths)


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
