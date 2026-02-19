import json
import tempfile
import unittest

from web_mcp_manager.config_loader import load_commands


class TestConfigLoader(unittest.TestCase):
    def test_load_commands_from_path(self):
        data = {"status_checks": [], "actions": []}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            path = f.name

        loaded = load_commands(path)
        self.assertEqual(loaded["status_checks"], [])
        self.assertEqual(loaded["actions"], [])

    def test_load_commands_with_bom(self):
        data = {"status_checks": [], "actions": []}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8-sig") as f:
            json.dump(data, f)
            path = f.name

        loaded = load_commands(path)
        self.assertEqual(loaded["status_checks"], [])
        self.assertEqual(loaded["actions"], [])


if __name__ == "__main__":
    unittest.main()
