import unittest
from web_mcp_manager.engine.actions import run_action


class FakeRunner:
    def run(self, cmd):
        class R:
            exit_code = 0
            output = "done"
        return R()


class TestActions(unittest.TestCase):
    def test_run_action_returns_result(self):
        action = {"label": "Test", "command": "Write-Output done"}
        res = run_action(FakeRunner(), action)
        self.assertEqual(res.exit_code, 0)
        self.assertIn("done", res.output)


if __name__ == "__main__":
    unittest.main()
