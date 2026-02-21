import sys
import unittest
from pathlib import Path


def test_startup_script_exists():
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "run-startup.ps1"
    assert script.exists()
    assert "mcp_manager.startup" in script.read_text(encoding="utf-8")


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
