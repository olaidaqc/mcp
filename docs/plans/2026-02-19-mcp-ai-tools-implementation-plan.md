# MCP AI Tools Manager Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a local MCP manager with Web+TUI UIs that can execute real commands, scan/classify AI tools, recommend better options per domain, and maintain real-time logs without any token usage.

**Architecture:** A shared Python backend (command runner, config manager, scanners, organizer, scheduler) exposes HTTP + SSE for a Web UI and a Textual TUI that both call the same backend functions.

**Tech Stack:** Python 3, FastAPI, Uvicorn, Textual, Requests, Standard Library unittest

---

### Task 1: Base package skeleton and shared paths

**Files:**
- Create: `mcp_manager/__init__.py`
- Create: `mcp_manager/paths.py`
- Create: `tests/test_paths.py`

**Step 1: Write the failing test**

```python
# tests/test_paths.py
from mcp_manager import paths

def test_paths_resolve_repo_and_user_dirs():
    p = paths.ProjectPaths()
    assert p.repo_root is not None
    assert p.user_home is not None
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_paths.py -v`
Expected: FAIL with "No module named 'mcp_manager'"

**Step 3: Write minimal implementation**

```python
# mcp_manager/paths.py
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ProjectPaths:
    repo_root: Path = Path(__file__).resolve().parents[1]
    user_home: Path = Path.home()
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_paths.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/__init__.py mcp_manager/paths.py tests/test_paths.py
git commit -m "feat: add base paths helper"
```

### Task 2: Command runner with logging

**Files:**
- Create: `mcp_manager/runner.py`
- Create: `mcp_manager/logs.py`
- Modify: `mcp_manager/paths.py`
- Create: `tests/test_runner.py`

**Step 1: Write the failing test**

```python
# tests/test_runner.py
from mcp_manager.runner import CommandRunner

def test_runner_captures_exit_code_and_output():
    runner = CommandRunner()
    result = runner.run(["cmd", "/c", "echo", "ok"])
    assert result.exit_code == 0
    assert "ok" in result.stdout.lower()
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_runner.py -v`
Expected: FAIL with "No module named 'mcp_manager.runner'"

**Step 3: Write minimal implementation**

```python
# mcp_manager/runner.py
from dataclasses import dataclass
import subprocess

@dataclass
class CommandResult:
    exit_code: int
    stdout: str
    stderr: str

class CommandRunner:
    def run(self, args, timeout=60):
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout, errors="replace")
        return CommandResult(proc.returncode, proc.stdout, proc.stderr)
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_runner.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/runner.py mcp_manager/logs.py mcp_manager/paths.py tests/test_runner.py
git commit -m "feat: add command runner"
```

### Task 3: Config manager with JSON + Chinese comments

**Files:**
- Create: `mcp_manager/config.py`
- Create: `mcp_manager/config_defaults.py`
- Create: `config/commands.json`
- Create: `config/tool_rules.json`
- Create: `config/scan_schedule.json`
- Create: `tests/test_config.py`

**Step 1: Write the failing test**

```python
# tests/test_config.py
from mcp_manager.config import load_json_config


def test_load_config_supports_utf8_bom(tmp_path):
    p = tmp_path / "cfg.json"
    p.write_text("\ufeff{\"name\":\"test\"}", encoding="utf-8")
    data = load_json_config(p)
    assert data["name"] == "test"
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_config.py -v`
Expected: FAIL with "No module named 'mcp_manager.config'"

**Step 3: Write minimal implementation**

```python
# mcp_manager/config.py
import json

def load_json_config(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_config.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/config.py mcp_manager/config_defaults.py config/commands.json config/tool_rules.json config/scan_schedule.json tests/test_config.py
git commit -m "feat: add config loader and defaults"
```

### Task 4: AI tools local scanner (VSCode, pip, npm, winget)

**Files:**
- Create: `mcp_manager/scanners/local.py`
- Create: `mcp_manager/scanners/__init__.py`
- Create: `tests/test_local_scanner.py`

**Step 1: Write the failing test**

```python
# tests/test_local_scanner.py
from mcp_manager.scanners.local import classify_tool

def test_classify_tool_assigns_single_domain():
    rules = {"domains": {"dev": ["copilot"]}}
    tool = {"name": "github.copilot"}
    assert classify_tool(tool, rules) == "dev"
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_local_scanner.py -v`
Expected: FAIL with "No module named 'mcp_manager.scanners.local'"

**Step 3: Write minimal implementation**

```python
# mcp_manager/scanners/local.py
import re

def classify_tool(tool, rules):
    name = tool.get("name", "").lower()
    for domain, patterns in rules.get("domains", {}).items():
        for p in patterns:
            if re.search(p, name):
                return domain
    return "general"
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_local_scanner.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/scanners/local.py mcp_manager/scanners/__init__.py tests/test_local_scanner.py
git commit -m "feat: add local AI tool classifier"
```

### Task 5: Online catalog fetcher (no token) + recommendation engine

**Files:**
- Create: `mcp_manager/scanners/catalog.py`
- Create: `mcp_manager/recommender.py`
- Create: `tests/test_recommender.py`

**Step 1: Write the failing test**

```python
# tests/test_recommender.py
from mcp_manager.recommender import score_tool

def test_score_tool_prefers_recent_and_free():
    tool = {"last_update_days": 10, "price": 0}
    assert score_tool(tool) > 0
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_recommender.py -v`
Expected: FAIL with "No module named 'mcp_manager.recommender'"

**Step 3: Write minimal implementation**

```python
# mcp_manager/recommender.py

def score_tool(tool):
    score = 0
    score += max(0, 100 - tool.get("last_update_days", 999))
    score += 50 if tool.get("price", 0) == 0 else 0
    return score
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_recommender.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/scanners/catalog.py mcp_manager/recommender.py tests/test_recommender.py
git commit -m "feat: add catalog fetcher and recommender"
```

### Task 6: File organizer

**Files:**
- Create: `mcp_manager/organizer.py`
- Create: `tests/test_organizer.py`

**Step 1: Write the failing test**

```python
# tests/test_organizer.py
from mcp_manager.organizer import classify_path


def test_classify_path_scripts():
    assert classify_path("tool.bat") == "scripts"
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_organizer.py -v`
Expected: FAIL with "No module named 'mcp_manager.organizer'"

**Step 3: Write minimal implementation**

```python
# mcp_manager/organizer.py
from pathlib import Path

def classify_path(path):
    ext = Path(path).suffix.lower()
    if ext in {".bat", ".sh", ".ps1"}:
        return "scripts"
    if ext in {".json", ".yml", ".yaml"}:
        return "config"
    if ext in {".log", ".txt"}:
        return "logs"
    return "other"
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_organizer.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/organizer.py tests/test_organizer.py
git commit -m "feat: add file organizer classification"
```

### Task 7: Scheduler for periodic scans

**Files:**
- Create: `mcp_manager/scheduler.py`
- Create: `tests/test_scheduler.py`

**Step 1: Write the failing test**

```python
# tests/test_scheduler.py
from mcp_manager.scheduler import should_run

def test_should_run_daily():
    assert should_run("daily", last_run_days=2)
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_scheduler.py -v`
Expected: FAIL with "No module named 'mcp_manager.scheduler'"

**Step 3: Write minimal implementation**

```python
# mcp_manager/scheduler.py

def should_run(freq, last_run_days):
    if freq == "daily":
        return last_run_days >= 1
    if freq == "weekly":
        return last_run_days >= 7
    return False
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_scheduler.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/scheduler.py tests/test_scheduler.py
git commit -m "feat: add scan scheduler"
```

### Task 8: Web API (FastAPI + SSE)

**Files:**
- Create: `web/server.py`
- Create: `web/routes.py`
- Create: `tests/test_api.py`
- Create: `requirements.txt`

**Step 1: Write the failing test**

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from web.server import app

def test_status_endpoint():
    client = TestClient(app)
    resp = client.get("/api/status")
    assert resp.status_code == 200
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_api.py -v`
Expected: FAIL with "No module named 'web.server'"

**Step 3: Write minimal implementation**

```python
# web/server.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/status")
def status():
    return {"ok": True}
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add web/server.py web/routes.py tests/test_api.py requirements.txt
git commit -m "feat: add web API skeleton"
```

### Task 9: Web UI (real-time + config editor + tools view)

**Files:**
- Create: `web/static/index.html`
- Create: `web/static/app.js`
- Create: `web/static/styles.css`

**Step 1: Write the failing test**

```python
# tests/test_api.py
# Add a check that static index loads
resp = client.get("/")
assert resp.status_code == 200
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_api.py -v`
Expected: FAIL with "404"

**Step 3: Write minimal implementation**

```html
<!-- web/static/index.html -->
<h1>MCP Manager</h1>
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add web/static/index.html web/static/app.js web/static/styles.css tests/test_api.py
git commit -m "feat: add web UI skeleton"
```

### Task 10: TUI app (Textual)

**Files:**
- Create: `tui/app.py`
- Create: `tests/test_tui.py`

**Step 1: Write the failing test**

```python
# tests/test_tui.py
from tui.app import build_app

def test_tui_builds():
    app = build_app()
    assert app is not None
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_tui.py -v`
Expected: FAIL with "No module named 'tui.app'"

**Step 3: Write minimal implementation**

```python
# tui/app.py
from textual.app import App

class MCPApp(App):
    pass

def build_app():
    return MCPApp()
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_tui.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tui/app.py tests/test_tui.py
git commit -m "feat: add TUI skeleton"
```

### Task 11: Wire real features into Web + TUI

**Files:**
- Modify: `web/server.py`
- Modify: `web/routes.py`
- Modify: `web/static/app.js`
- Modify: `tui/app.py`
- Modify: `mcp_manager/*`

**Step 1: Write the failing test**

```python
# tests/test_api.py
resp = client.get("/api/tools")
assert resp.status_code == 200
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_api.py -v`
Expected: FAIL with "404"

**Step 3: Write minimal implementation**

```python
# web/routes.py
from fastapi import APIRouter
router = APIRouter()

@router.get("/api/tools")
def tools():
    return {"items": []}
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add web/server.py web/routes.py web/static/app.js tui/app.py mcp_manager/* tests/test_api.py
git commit -m "feat: wire scanning to UI"
```

### Task 12: Start scripts + docs

**Files:**
- Create: `start-web.bat`
- Create: `start-tui.bat`
- Modify: `README.md`

**Step 1: Write the failing test**

```python
# tests/test_paths.py
from pathlib import Path

def test_start_scripts_exist():
    assert Path("start-web.bat").exists()
    assert Path("start-tui.bat").exists()
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_paths.py -v`
Expected: FAIL with "False is not true"

**Step 3: Write minimal implementation**

```bat
@echo off
python web/server.py
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_paths.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add start-web.bat start-tui.bat README.md tests/test_paths.py
git commit -m "feat: add start scripts and docs"
```

---

Plan complete and saved to `docs/plans/2026-02-19-mcp-ai-tools-implementation-plan.md`. Two execution options:

1. Subagent-Driven (this session) - I dispatch fresh subagent per task, review between tasks, fast iteration
2. Parallel Session (separate) - Open new session with executing-plans, batch execution with checkpoints

Which approach?
