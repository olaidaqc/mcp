from mcp_manager import paths

def test_paths_resolve_repo_and_user_dirs():
    p = paths.ProjectPaths()
    assert p.repo_root is not None
    assert p.user_home is not None


def test_start_scripts_exist():
    from pathlib import Path

    assert Path("start-web.bat").exists()
    assert Path("start-tui.bat").exists()


def test_ai_hub_root_documented():
    from pathlib import Path

    text = Path("README.md").read_text(encoding="utf-8")
    assert "AI-Hub" in text


def test_ai_only_mode_documented():
    from pathlib import Path

    text = Path("README.md").read_text(encoding="utf-8")
    assert "confirm-only" in text.lower()


import sys
import unittest


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
