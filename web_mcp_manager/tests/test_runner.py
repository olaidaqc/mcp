import unittest

from web_mcp_manager.engine.runner import CommandRunner


class TestCommandRunner(unittest.TestCase):
    def test_runner_captures_output(self):
        runner = CommandRunner(timeout_sec=5)
        result = runner.run("Write-Output 'ok'")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("ok", result.output)

    def test_runner_streams_output(self):
        runner = CommandRunner(timeout_sec=5)
        lines = []
        result = runner.run_stream("Write-Output 'one'; Write-Output 'two'", lines.append)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(any("one" in line for line in lines))
        self.assertTrue(any("two" in line for line in lines))


if __name__ == "__main__":
    unittest.main()
