import unittest

from mcp_manager.ui.fallback import FallbackUI


class TestUISelect(unittest.TestCase):
    def test_fallback_ui_initializes(self):
        ui = FallbackUI(title="Test")
        self.assertEqual(ui.title, "Test")


if __name__ == "__main__":
    unittest.main()
