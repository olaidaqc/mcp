import sys
import unittest

from mcp_manager.scanners.local import classify_tool


def test_classify_tool_assigns_single_domain():
    rules = {"domains": {"dev": ["copilot"]}}
    tool = {"name": "github.copilot"}
    assert classify_tool(tool, rules) == "dev"


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
