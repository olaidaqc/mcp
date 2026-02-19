import os
import time
from collections import deque
from datetime import datetime
from typing import List

from ..engine.checks import run_checks


class FallbackUI:
    def __init__(self, title: str, context):
        self.title = title
        self.context = context
        self.logs = deque(maxlen=200)
        self.status = []

    def _append_log(self, line: str):
        ts = datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}] {line}"
        self.logs.append(entry)
        self.context.log_sink.write(entry)

    def _refresh_status(self):
        self.status = run_checks(self.context.runner, self.context.commands.get("status_checks", []))

    def _format_status(self) -> List[str]:
        lines = []
        for item in self.status:
            flag = "OK" if item.get("ok") else "ERR"
            lines.append(f"[{flag}] {item.get('label')}")
        return lines

    def _render(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(self.title)
        print("=" * len(self.title))
        print("Status")
        for line in self._format_status():
            print(f"  {line}")
        print("\nActions")
        print("  r) Refresh   q) Quit")
        actions = self.context.commands.get("actions", [])
        for idx, action in enumerate(actions, start=1):
            print(f"  {idx}) {action.get('label')}")
        print("\nLogs")
        for line in list(self.logs)[-10:]:
            print(f"  {line}")

    def run(self):
        self._refresh_status()
        while True:
            self._render()
            choice = input("Select: ").strip().lower()
            if choice in ("q", "quit"):
                break
            if choice in ("r", "refresh"):
                self._refresh_status()
                continue
            if choice.isdigit():
                idx = int(choice) - 1
                actions = self.context.commands.get("actions", [])
                if 0 <= idx < len(actions):
                    action = actions[idx]
                    self._append_log(f"Running: {action.get('label')}")
                    result = self.context.runner.run_stream(action.get("command", ""), self._append_log)
                    if result.exit_code != 0:
                        self._append_log(f"Error: exit {result.exit_code}")
                    time.sleep(0.2)
                else:
                    self._append_log("Invalid selection")
            else:
                self._append_log("Invalid selection")
