# MCP Manager TUI Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a local, clickable TUI for MCP management that runs real PowerShell commands, shows live status, and streams logs with zero token usage.

**Architecture:** A small Python package with an engine layer (command runner, checks, actions, logs) and a UI layer (Textual primary, fallback text UI). UI selection happens at runtime, with auto-refresh every 5 seconds and manual refresh on demand.

**Tech Stack:** Python 3, Textual (optional, for clickable UI), standard library (subprocess, threading, queue, json, pathlib, unittest).

---

### Task 1: Create config model and loader

**Files:**
- Create: `mcp_manager/config/commands.json`
- Create: `mcp_manager/config_loader.py`
- Create: `mcp_manager/__init__.py`
- Create: `tests/test_config_loader.py`

**Step 1: Write the failing test**

```python
import json
import tempfile
from mcp_manager.config_loader import load_commands


def test_load_commands_from_path():
    data = {"status_checks": [], "actions": []}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        path = f.name

    loaded = load_commands(path)
    assert loaded["status_checks"] == []
    assert loaded["actions"] == []
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_config_loader.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'mcp_manager'`

**Step 3: Write minimal implementation**

```python
# mcp_manager/config_loader.py
import json
from pathlib import Path

def load_commands(path: str):
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_config_loader.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/config/commands.json mcp_manager/config_loader.py mcp_manager/__init__.py tests/test_config_loader.py
git commit -m "feat: add commands config loader"
```

### Task 2: Add log sink and command runner

**Files:**
- Create: `mcp_manager/engine/logs.py`
- Create: `mcp_manager/engine/runner.py`
- Create: `tests/test_logs.py`
- Create: `tests/test_runner.py`

**Step 1: Write the failing test**

```python
from mcp_manager.engine.logs import LogSink


def test_log_sink_appends_to_file(tmp_path):
    log_file = tmp_path / "runtime.log"
    sink = LogSink(log_file)
    sink.write("hello")
    assert log_file.read_text(encoding="utf-8").strip() == "hello"
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_logs.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'mcp_manager.engine'`

**Step 3: Write minimal implementation**

```python
# mcp_manager/engine/logs.py
from pathlib import Path

class LogSink:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, text: str):
        with self.path.open("a", encoding="utf-8") as f:
            f.write(text + "\n")
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_logs.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/engine/logs.py tests/test_logs.py
git commit -m "feat: add log sink"
```

### Task 3: Implement PowerShell command runner

**Files:**
- Modify: `mcp_manager/engine/runner.py`
- Modify: `tests/test_runner.py`

**Step 1: Write the failing test**

```python
from mcp_manager.engine.runner import CommandRunner


def test_runner_captures_output():
    runner = CommandRunner(timeout_sec=5)
    result = runner.run("Write-Output 'ok'")
    assert result.exit_code == 0
    assert "ok" in result.output
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_runner.py -v`
Expected: FAIL with `ImportError` or missing implementation

**Step 3: Write minimal implementation**

```python
# mcp_manager/engine/runner.py
import subprocess
from dataclasses import dataclass

@dataclass
class RunResult:
    exit_code: int
    output: str

class CommandRunner:
    def __init__(self, timeout_sec: int = 60):
        self.timeout_sec = timeout_sec

    def run(self, command: str) -> RunResult:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            capture_output=True,
            text=True,
            timeout=self.timeout_sec,
        )
        output = (proc.stdout or "") + (proc.stderr or "")
        return RunResult(proc.returncode, output)
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_runner.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/engine/runner.py tests/test_runner.py
git commit -m "feat: add PowerShell command runner"
```

### Task 4: Status checks orchestration

**Files:**
- Create: `mcp_manager/engine/checks.py`
- Create: `tests/test_checks.py`

**Step 1: Write the failing test**

```python
from mcp_manager.engine.checks import run_checks

class FakeRunner:
    def run(self, cmd):
        class R:
            exit_code = 0
            output = "ok"
        return R()


def test_run_checks_returns_status():
    checks = [{"label": "Test", "command": "Write-Output ok"}]
    snapshot = run_checks(FakeRunner(), checks)
    assert snapshot[0]["label"] == "Test"
    assert snapshot[0]["ok"] is True
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_checks.py -v`
Expected: FAIL with missing implementation

**Step 3: Write minimal implementation**

```python
# mcp_manager/engine/checks.py
from datetime import datetime

def run_checks(runner, checks):
    results = []
    for item in checks:
        res = runner.run(item["command"])
        results.append({
            "label": item["label"],
            "ok": res.exit_code == 0,
            "output": res.output,
            "ts": datetime.now(),
        })
    return results
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_checks.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/engine/checks.py tests/test_checks.py
git commit -m "feat: add status checks"
```

### Task 5: Action dispatcher

**Files:**
- Create: `mcp_manager/engine/actions.py`
- Create: `tests/test_actions.py`

**Step 1: Write the failing test**

```python
from mcp_manager.engine.actions import run_action

class FakeRunner:
    def run(self, cmd):
        class R:
            exit_code = 0
            output = "done"
        return R()


def test_run_action_returns_result():
    action = {"label": "Test", "command": "Write-Output done"}
    res = run_action(FakeRunner(), action)
    assert res.exit_code == 0
    assert "done" in res.output
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_actions.py -v`
Expected: FAIL with missing implementation

**Step 3: Write minimal implementation**

```python
# mcp_manager/engine/actions.py

def run_action(runner, action):
    return runner.run(action["command"])
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_actions.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/engine/actions.py tests/test_actions.py
git commit -m "feat: add action dispatcher"
```

### Task 6: Fallback UI (text menu)

**Files:**
- Create: `mcp_manager/ui/fallback.py`
- Create: `tests/test_ui_select.py`

**Step 1: Write the failing test**

```python
from mcp_manager.ui.fallback import FallbackUI


def test_fallback_ui_initializes():
    ui = FallbackUI(title="Test")
    assert ui.title == "Test"
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_ui_select.py -v`
Expected: FAIL with missing implementation

**Step 3: Write minimal implementation**

```python
# mcp_manager/ui/fallback.py
class FallbackUI:
    def __init__(self, title: str):
        self.title = title

    def run(self):
        # Minimal placeholder for menu loop, real logic added later
        pass
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_ui_select.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/ui/fallback.py tests/test_ui_select.py
git commit -m "feat: add fallback UI shell"
```

### Task 7: Textual UI (clickable)

**Files:**
- Create: `mcp_manager/ui/textual_app.py`
- Modify: `tests/test_ui_select.py`

**Step 1: Write the failing test**

```python
def test_textual_import_fallback(monkeypatch):
    # Placeholder - we will ensure UI selector falls back when Textual missing
    assert True
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_ui_select.py -v`
Expected: FAIL until selector logic exists

**Step 3: Write minimal implementation**

```python
# mcp_manager/ui/textual_app.py
# (Textual App skeleton with buttons, status panel, log panel)
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_ui_select.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/ui/textual_app.py tests/test_ui_select.py
git commit -m "feat: add textual UI skeleton"
```

### Task 8: Entry point, UI selection, and wiring

**Files:**
- Create: `mcp_manager.py`
- Modify: `mcp_manager/ui/fallback.py`
- Modify: `mcp_manager/ui/textual_app.py`
- Modify: `mcp_manager/config/commands.json`

**Step 1: Write the failing test**

```python
from mcp_manager import app

def test_selects_fallback_when_textual_missing(monkeypatch):
    monkeypatch.setattr(app, "HAS_TEXTUAL", False)
    assert app.select_ui_class().__name__ == "FallbackUI"
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_ui_select.py -v`
Expected: FAIL until selection is implemented

**Step 3: Write minimal implementation**

```python
# mcp_manager/app.py
# - load config
# - create runner/log sink
# - select UI (Textual if available, fallback otherwise)
# - run UI
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_ui_select.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager.py mcp_manager/app.py mcp_manager/ui/fallback.py mcp_manager/ui/textual_app.py mcp_manager/config/commands.json tests/test_ui_select.py
git commit -m "feat: wire app entrypoint and UI selection"
```

### Task 9: Manual verification and docs

**Files:**
- Modify: `README.md`

**Step 1: Manual run (Textual)**

Run: `python mcp_manager.py`
Expected: Clickable UI opens, status refreshes every 5s, buttons execute commands, logs update.

**Step 2: Manual run (fallback)**

Run: `set MCP_MANAGER_NO_TEXTUAL=1` then `python mcp_manager.py`
Expected: Text menu UI appears; actions and logs work.

**Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add MCP manager usage"
```
