try:
    from textual.app import App
    from textual.widgets import Static
    HAS_TEXTUAL = True
except Exception:
    App = object
    Static = object
    HAS_TEXTUAL = False


if HAS_TEXTUAL:
    class TextualApp(App):
        def __init__(self, title: str = "MCP Manager", **kwargs):
            super().__init__(**kwargs)
            self.title = title

        def compose(self):
            yield Static("Textual UI placeholder")
else:
    class TextualApp:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Textual is not available")
