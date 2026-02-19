import sys
import unittest

from mcp_manager.recommender import score_tool


def test_score_tool_prefers_recent_and_free():
    tool = {"last_update_days": 10, "price": 0}
    assert score_tool(tool) > 0


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
