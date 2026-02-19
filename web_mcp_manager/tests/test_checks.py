import unittest
from web_mcp_manager.engine.checks import run_checks


class FakeRunner:
    def run(self, cmd):
        class R:
            exit_code = 0
            output = "ok"
        return R()


class TestChecks(unittest.TestCase):
    def test_run_checks_returns_status(self):
        checks = [{"label": "Test", "command": "Write-Output ok"}]
        snapshot = run_checks(FakeRunner(), checks)
        self.assertEqual(snapshot[0]["label"], "Test")
        self.assertTrue(snapshot[0]["ok"])


if __name__ == "__main__":
    unittest.main()
