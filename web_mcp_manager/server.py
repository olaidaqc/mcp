from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from collections import deque
import threading

from web_mcp_manager.config_loader import load_commands
from web_mcp_manager.engine.runner import CommandRunner
from web_mcp_manager.engine.logs import LogSink
from web_mcp_manager.engine.checks import run_checks
from web_mcp_manager.engine.actions import run_action

app = FastAPI()
BASE = Path(__file__).resolve().parent
CONFIG = BASE / "config" / "commands.json"
commands = load_commands(str(CONFIG))
runner = CommandRunner()
log_path = Path.home() / "my-skills" / "runtime.log"
log_sink = LogSink(log_path)
log_buffer = deque(maxlen=2000)


def append_log(line: str):
    log_buffer.append(line)
    log_sink.write(line)


@app.get("/api/status")
def api_status():
    status = run_checks(runner, commands.get("status_checks", []))
    return {"status": status}


@app.get("/api/actions")
def api_actions():
    return {"actions": commands.get("actions", [])}


@app.post("/api/action/{idx}")
def api_action(idx: int):
    actions = commands.get("actions", [])
    if idx < 0 or idx >= len(actions):
        return JSONResponse({"error": "invalid action"}, status_code=400)

    def work():
        append_log(f"Running: {actions[idx].get('label')}")
        result = runner.run_stream(actions[idx].get("command", ""), append_log)
        if result.exit_code != 0:
            append_log(f"Error: exit {result.exit_code}")

    threading.Thread(target=work, daemon=True).start()
    return {"ok": True}


@app.get("/api/logs")
def api_logs(limit: int = 200):
    lines = list(log_buffer)[-limit:]
    return {"lines": lines}


app.mount("/", StaticFiles(directory=str(BASE / "web"), html=True), name="web")
