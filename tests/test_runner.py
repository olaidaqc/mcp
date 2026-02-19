import unittest

from mcp_manager.engine.runner import CommandRunner


class TestCommandRunner(unittest.TestCase):
    def test_runner_captures_output(self):
        runner = CommandRunner(timeout_sec=5)
        result = runner.run("Write-Output 'ok'")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("ok", result.output)


if __name__ == "__main__":
    unittest.main()
