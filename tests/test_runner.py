import sys
import unittest

from mcp_manager.runner import CommandRunner


def test_runner_captures_exit_code_and_output():
    runner = CommandRunner()
    result = runner.run(["cmd", "/c", "echo", "ok"])
    assert result.exit_code == 0
    assert "ok" in result.stdout.lower()


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
