import os
from dataclasses import dataclass
from pathlib import Path

from .config_loader import load_commands
from .engine.runner import CommandRunner
from .engine.logs import LogSink
from .ui.fallback import FallbackUI
from .ui.textual_app import TextualApp, HAS_TEXTUAL


@dataclass
class AppContext:
    commands: dict
    runner: CommandRunner
    log_sink: LogSink
    log_path: Path
    refresh_interval: int = 5


def select_ui_class():
    if os.getenv("MCP_MANAGER_NO_TEXTUAL") == "1":
        return FallbackUI
    return TextualApp if HAS_TEXTUAL else FallbackUI


def load_default_commands() -> dict:
    config_path = Path(__file__).resolve().parent / "config" / "commands.json"
    return load_commands(str(config_path))


def build_context() -> AppContext:
    commands = load_default_commands()
    log_path = Path(os.getenv("MCP_MANAGER_LOG", str(Path.home() / "my-skills" / "runtime.log")))
    runner = CommandRunner()
    log_sink = LogSink(log_path)
    return AppContext(commands=commands, runner=runner, log_sink=log_sink, log_path=log_path)


def main():
    ctx = build_context()
    ui_class = select_ui_class()
    ui = ui_class(title="MCP Manager Console", context=ctx)
    ui.run()
