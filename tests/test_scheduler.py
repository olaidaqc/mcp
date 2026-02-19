import sys
import unittest

from mcp_manager.scheduler import should_run


def test_should_run_daily():
    assert should_run("daily", last_run_days=2)


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
