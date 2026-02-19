import sys
import unittest

from tui.app import build_app


def test_tui_builds():
    app = build_app()
    assert app is not None


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
