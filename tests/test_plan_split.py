import sys
import unittest
from pathlib import Path

from mcp_manager.organize import split_plan


def test_split_plan_is_confirm_only():
    plan = [{"path": "x.gguf", "category": "Models"}]
    auto, confirm = split_plan(plan, {"core_exts": [".gguf"], "large_threshold_bytes": 0})
    assert auto == []
    assert len(confirm) == 1


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
