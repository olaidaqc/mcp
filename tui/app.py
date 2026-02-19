try:
    from textual.app import App as TextualApp
except Exception:  # pragma: no cover - fallback when textual isn't installed
    class TextualApp:
        pass


class MCPApp(TextualApp):
    pass


def build_app():
    return MCPApp()
