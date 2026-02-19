import unittest
from unittest.mock import patch

from mcp_manager.ui.fallback import FallbackUI


class TestUISelect(unittest.TestCase):
    def test_fallback_ui_initializes(self):
        ui = FallbackUI(title="Test", context=object())
        self.assertEqual(ui.title, "Test")

    def test_textual_module_exposes_flag(self):
        from mcp_manager.ui import textual_app
        self.assertTrue(hasattr(textual_app, "HAS_TEXTUAL"))

    def test_selects_fallback_when_textual_missing(self):
        from mcp_manager import app
        with patch.object(app, "HAS_TEXTUAL", False):
            self.assertEqual(app.select_ui_class().__name__, "FallbackUI")


if __name__ == "__main__":
    unittest.main()
