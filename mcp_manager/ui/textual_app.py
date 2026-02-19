import threading
from collections import deque
from datetime import datetime
from typing import List

from ..engine.checks import run_checks

try:
    from textual.app import App, ComposeResult
    from textual.containers import Container, Horizontal
    from textual.widgets import Button, Footer, Header, Static
    HAS_TEXTUAL = True
except Exception:
    App = object
    ComposeResult = object
    Container = object
    Horizontal = object
    Button = object
    Footer = object
    Header = object
    Static = object
    HAS_TEXTUAL = False


if HAS_TEXTUAL:
    class TextualApp(App):
        BINDINGS = [("q", "quit", "Quit"), ("r", "refresh", "Refresh")]

        def __init__(self, title: str, context, **kwargs):
            super().__init__(**kwargs)
            self.title = title
            self.context = context
            self.logs = deque(maxlen=200)
            self.status = []

        def compose(self) -> ComposeResult:
            yield Header()
            yield Static("", id="status")
            actions = self.context.commands.get("actions", [])
            buttons = [Button("Refresh", id="refresh")]
            for idx, action in enumerate(actions):
                buttons.append(Button(action.get("label", f"Action {idx+1}"), id=f"action-{idx}"))
            yield Container(Horizontal(*buttons), id="actions")
            yield Static("", id="logs")
            yield Footer()

        def on_mount(self) -> None:
            self.refresh_status()
            self.set_interval(self.context.refresh_interval, self.refresh_status)

        def _append_log(self, line: str) -> None:
            ts = datetime.now().strftime("%H:%M:%S")
            entry = f"[{ts}] {line}"
            self.logs.append(entry)
            self.context.log_sink.write(entry)
            self.call_from_thread(self._render_logs)

        def _render_logs(self) -> None:
            widget = self.query_one("#logs", Static)
            widget.update("\n".join(list(self.logs)[-20:]))

        def _format_status(self) -> List[str]:
            lines = []
            for item in self.status:
                flag = "OK" if item.get("ok") else "ERR"
                lines.append(f"[{flag}] {item.get('label')}")
            return lines

        def _set_status(self, snapshot):
            self.status = snapshot
            widget = self.query_one("#status", Static)
            widget.update("\n".join(self._format_status()))

        def refresh_status(self):
            def work():
                snapshot = run_checks(self.context.runner, self.context.commands.get("status_checks", []))
                self.call_from_thread(self._set_status, snapshot)
            threading.Thread(target=work, daemon=True).start()

        def on_button_pressed(self, event: Button.Pressed) -> None:
            if event.button.id == "refresh":
                self.refresh_status()
                return
            if event.button.id and event.button.id.startswith("action-"):
                idx = int(event.button.id.split("-")[-1])
                actions = self.context.commands.get("actions", [])
                if 0 <= idx < len(actions):
                    action = actions[idx]
                    self._run_action(action)

        def _run_action(self, action):
            def work():
                self._append_log(f"Running: {action.get('label')}")
                result = self.context.runner.run_stream(action.get("command", ""), self._append_log)
                if result.exit_code != 0:
                    self._append_log(f"Error: exit {result.exit_code}")
            threading.Thread(target=work, daemon=True).start()

        def action_refresh(self) -> None:
            self.refresh_status()
else:
    class TextualApp:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Textual is not available")
