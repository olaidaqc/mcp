import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from web_mcp_manager.server import app


class TestApi(unittest.TestCase):
    def test_status_endpoint(self):
        client = TestClient(app)
        with patch("web_mcp_manager.server.run_checks") as mock_checks:
            mock_checks.return_value = [{"label": "Test", "ok": True, "output": "ok", "ts": "now"}]
            resp = client.get("/api/status")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("status", resp.json())


if __name__ == "__main__":
    unittest.main()
