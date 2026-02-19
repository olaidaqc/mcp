import unittest

from mcp_manager.ui.fallback import FallbackUI


class TestUISelect(unittest.TestCase):
    def test_fallback_ui_initializes(self):
        ui = FallbackUI(title="Test")
        self.assertEqual(ui.title, "Test")

    def test_textual_module_exposes_flag(self):
        from mcp_manager.ui import textual_app
        self.assertTrue(hasattr(textual_app, "HAS_TEXTUAL"))


if __name__ == "__main__":
    unittest.main()
