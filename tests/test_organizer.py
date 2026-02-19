import sys
import unittest

from mcp_manager.organizer import classify_path


def test_classify_path_scripts():
    assert classify_path("tool.bat") == "scripts"


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
