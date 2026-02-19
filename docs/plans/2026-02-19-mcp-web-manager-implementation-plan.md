# MCP Web Manager Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a local FastAPI web UI for MCP management that executes real commands, shows status, and streams logs.

**Architecture:** FastAPI backend serves a static single-page UI and provides JSON APIs for status, actions, and logs. Commands are loaded from a JSON config and executed via PowerShell with streamed output into a log buffer.

**Tech Stack:** Python 3, FastAPI, Uvicorn, standard library (subprocess, threading, queue, json, pathlib, unittest).

---

### Task 1: Add web config and loader

**Files:**
- Create: `web-mcp-manager/config/commands.json`
- Create: `web-mcp-manager/config_loader.py`
- Create: `web-mcp-manager/__init__.py`
- Create: `web-mcp-manager/tests/test_config_loader.py`

**Step 1: Write the failing test**

```python
import json
import tempfile
import unittest

from web_mcp_manager.config_loader import load_commands


class TestConfigLoader(unittest.TestCase):
    def test_load_commands_from_path(self):
        data = {"status_checks": [], "actions": []}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            path = f.name

        loaded = load_commands(path)
        self.assertEqual(loaded["status_checks"], [])
        self.assertEqual(loaded["actions"], [])


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest web-mcp-manager/tests/test_config_loader.py -v`
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write minimal implementation**

```python
import json
from pathlib import Path

def load_commands(path: str):
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest web-mcp-manager/tests/test_config_loader.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add web-mcp-manager/config/commands.json web-mcp-manager/config_loader.py web-mcp-manager/__init__.py web-mcp-manager/tests/test_config_loader.py
git commit -m "feat: add web config loader"
```

### Task 2: Add log sink and PowerShell runner

**Files:**
- Create: `web-mcp-manager/engine/logs.py`
- Create: `web-mcp-manager/engine/runner.py`
- Create: `web-mcp-manager/engine/__init__.py`
- Create: `web-mcp-manager/tests/test_logs.py`
- Create: `web-mcp-manager/tests/test_runner.py`

**Step 1: Write the failing test**

```python
import unittest
from pathlib import Path
import tempfile

from web_mcp_manager.engine.logs import LogSink


class TestLogSink(unittest.TestCase):
    def test_log_sink_appends_to_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "runtime.log"
            sink = LogSink(log_file)
            sink.write("hello")
            self.assertEqual(log_file.read_text(encoding="utf-8").strip(), "hello")


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest web-mcp-manager/tests/test_logs.py -v`
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write minimal implementation**

```python
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

Run: `python -m unittest web-mcp-manager/tests/test_logs.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add web-mcp-manager/engine/logs.py web-mcp-manager/engine/__init__.py web-mcp-manager/tests/test_logs.py
git commit -m "feat: add web log sink"
```

### Task 3: PowerShell runner with streaming

**Files:**
- Modify: `web-mcp-manager/engine/runner.py`
- Modify: `web-mcp-manager/tests/test_runner.py`

**Step 1: Write the failing test**

```python
import unittest

from web_mcp_manager.engine.runner import CommandRunner


class TestCommandRunner(unittest.TestCase):
    def test_runner_captures_output(self):
        runner = CommandRunner(timeout_sec=5)
        result = runner.run("Write-Output 'ok'")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("ok", result.output)

    def test_runner_streams_output(self):
        runner = CommandRunner(timeout_sec=5)
        lines = []
        result = runner.run_stream("Write-Output 'one'; Write-Output 'two'", lines.append)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(any("one" in line for line in lines))
        self.assertTrue(any("two" in line for line in lines))


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest web-mcp-manager/tests/test_runner.py -v`
Expected: FAIL with missing `run_stream`

**Step 3: Write minimal implementation**

```python
import subprocess
import time
from dataclasses import dataclass
from typing import Callable, Optional

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

    def run_stream(self, command: str, on_output: Optional[Callable[[str], None]] = None) -> RunResult:
        proc = subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        output_chunks = []
        start = time.monotonic()
        try:
            while True:
                if proc.stdout is None:
                    break
                line = proc.stdout.readline()
                if line:
                    output_chunks.append(line)
                    if on_output:
                        on_output(line.rstrip("\n"))
                else:
                    if proc.poll() is not None:
                        break
                if time.monotonic() - start > self.timeout_sec:
                    proc.kill()
                    output_chunks.append(f"[timeout after {self.timeout_sec}s]\n")
                    break
        finally:
            if proc.stdout is not None:
                proc.stdout.close()
        exit_code = proc.wait() if proc.returncode is None else proc.returncode
        return RunResult(exit_code, "".join(output_chunks))
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest web-mcp-manager/tests/test_runner.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add web-mcp-manager/engine/runner.py web-mcp-manager/tests/test_runner.py
git commit -m "feat: add web PowerShell runner"
```

### Task 4: Status checks and actions

**Files:**
- Create: `web-mcp-manager/engine/checks.py`
- Create: `web-mcp-manager/engine/actions.py`
- Create: `web-mcp-manager/tests/test_checks.py`
- Create: `web-mcp-manager/tests/test_actions.py`

**Step 1: Write the failing test**

```python
import unittest
from web_mcp_manager.engine.checks import run_checks

class FakeRunner:
    def run(self, cmd):
        class R:
            exit_code = 0
            output = "ok"
        return R()

class TestChecks(unittest.TestCase):
    def test_run_checks_returns_status(self):
        checks = [{"label": "Test", "command": "Write-Output ok"}]
        snapshot = run_checks(FakeRunner(), checks)
        self.assertEqual(snapshot[0]["label"], "Test")
        self.assertTrue(snapshot[0]["ok"])


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest web-mcp-manager/tests/test_checks.py -v`
Expected: FAIL with missing implementation

**Step 3: Write minimal implementation**

```python
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

Run: `python -m unittest web-mcp-manager/tests/test_checks.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add web-mcp-manager/engine/checks.py web-mcp-manager/tests/test_checks.py
git commit -m "feat: add web status checks"
```

**Action dispatcher test/impl**

```python
import unittest
from web_mcp_manager.engine.actions import run_action

class FakeRunner:
    def run(self, cmd):
        class R:
            exit_code = 0
            output = "done"
        return R()

class TestActions(unittest.TestCase):
    def test_run_action_returns_result(self):
        action = {"label": "Test", "command": "Write-Output done"}
        res = run_action(FakeRunner(), action)
        self.assertEqual(res.exit_code, 0)
        self.assertIn("done", res.output)


if __name__ == "__main__":
    unittest.main()
```

```python
# actions.py

def run_action(runner, action):
    return runner.run(action["command"])
```

**Commit**
```bash
git add web-mcp-manager/engine/actions.py web-mcp-manager/tests/test_actions.py
git commit -m "feat: add web action dispatcher"
```

### Task 5: FastAPI server and endpoints

**Files:**
- Create: `web-mcp-manager/server.py`
- Create: `web-mcp-manager/requirements.txt`
- Create: `web-mcp-manager/tests/test_api.py`

**Step 1: Write the failing test**

```python
import unittest
from fastapi.testclient import TestClient
from web_mcp_manager.server import app

class TestApi(unittest.TestCase):
    def test_status_endpoint(self):
        client = TestClient(app)
        resp = client.get("/api/status")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("status", resp.json())


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest web-mcp-manager/tests/test_api.py -v`
Expected: FAIL (FastAPI missing)

**Step 3: Write minimal implementation**

```python
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
    # placeholder to be wired to in-memory buffer
    return {"lines": []}
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest web-mcp-manager/tests/test_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add web-mcp-manager/server.py web-mcp-manager/requirements.txt web-mcp-manager/tests/test_api.py
git commit -m "feat: add FastAPI server"
```

### Task 6: Static UI

**Files:**
- Create: `web-mcp-manager/web/index.html`
- Create: `web-mcp-manager/web/app.js`
- Create: `web-mcp-manager/web/styles.css`

**Step 1: Create UI**
- Status panel + buttons + logs area
- Poll `/api/status` every 5s and `/api/logs` every 2s

**Step 2: Commit**

```bash
git add web-mcp-manager/web/index.html web-mcp-manager/web/app.js web-mcp-manager/web/styles.css
git commit -m "feat: add web UI"
```

### Task 7: Serve static files + start script

**Files:**
- Modify: `web-mcp-manager/server.py`
- Create: `web-mcp-manager/start-web.bat`
- Modify: `web-mcp-manager/requirements.txt`

**Step 1:** serve `/` from `web/` and add `uvicorn` dependency

**Step 2: Commit**

```bash
git add web-mcp-manager/server.py web-mcp-manager/start-web.bat web-mcp-manager/requirements.txt
git commit -m "feat: serve web UI and add start script"
```

### Task 8: Wiring logs + finalize

**Files:**
- Modify: `web-mcp-manager/server.py`
- Modify: `web-mcp-manager/engine/logs.py`

**Step 1:** add in-memory log buffer and `/api/logs`

**Step 2: Commit**

```bash
git add web-mcp-manager/server.py web-mcp-manager/engine/logs.py
git commit -m "feat: wire log buffer and logs API"
```

### Task 9: Manual verification and docs

**Files:**
- Modify: `README.md`

**Step 1:** Run server

```bash
cd web-mcp-manager
start-web.bat
```

**Step 2:** Visit http://127.0.0.1:8765

**Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add web manager usage"
```
