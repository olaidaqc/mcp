from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pathlib import Path

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


@app.get("/api/status")
def api_status():
    status = run_checks(runner, commands.get("status_checks", []))
    return {"status": status}


@app.post("/api/action/{idx}")
def api_action(idx: int):
    actions = commands.get("actions", [])
    if idx < 0 or idx >= len(actions):
        return JSONResponse({"error": "invalid action"}, status_code=400)
    res = run_action(runner, actions[idx])
    return {"exit_code": res.exit_code, "output": res.output[-2000:]}


@app.get("/api/logs")
def api_logs(limit: int = 200):
    return {"lines": []}
