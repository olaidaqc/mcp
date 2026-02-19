import sys
import unittest
from mcp_manager.organize import get_default_roots


def test_default_roots_excludes_claude():
    roots = get_default_roots("C:/Users/11918")
    assert "C:/Users/11918/Desktop/claude" not in roots


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
