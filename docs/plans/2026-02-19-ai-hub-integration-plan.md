# AI Hub Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Integrate AI Hub scanning, planning, confirmation, and apply flows with CLI and Web UI.

**Architecture:** Organize module orchestrates scanning and planning, rules are loaded from AI-Hub, apply writes sidecars and index, and FastAPI routes expose status/plan/confirm/scan. Web UI calls API endpoints.

**Tech Stack:** Python 3, FastAPI, Standard Library unittest

---

### Task 1: Plan persistence + status helpers

**Files:**
- Modify: `mcp_manager/organize.py`
- Create: `tests/test_organize_plan.py`

**Step 1: Write the failing test**

```python
# tests/test_organize_plan.py
import sys
import unittest
from pathlib import Path

from mcp_manager.organize import save_plan, load_plan


def test_save_and_load_plan(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    plan = {"auto": [{"path": "a"}], "confirm": []}
    save_plan(tmp_path, plan)
    loaded = load_plan(tmp_path)
    assert loaded["auto"][0]["path"] == "a"


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_organize_plan.py -v`
Expected: FAIL with "save_plan not defined"

**Step 3: Write minimal implementation**

```python
# mcp_manager/organize.py
import json
from pathlib import Path


def _reports_dir(root):
    return Path(root) / "_reports"


def save_plan(root, plan):
    _reports_dir(root).mkdir(parents=True, exist_ok=True)
    path = _reports_dir(root) / "plan.json"
    path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")


def load_plan(root):
    path = _reports_dir(root) / "plan.json"
    if not path.exists():
        return {"auto": [], "confirm": []}
    return json.loads(path.read_text(encoding="utf-8"))
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_organize_plan.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/organize.py tests/test_organize_plan.py
git commit -m "feat: add plan persistence"
```

### Task 2: Build plan with confirm split

**Files:**
- Modify: `mcp_manager/organize.py`
- Create: `tests/test_plan_split.py`

**Step 1: Write the failing test**

```python
# tests/test_plan_split.py
import sys
import unittest
from pathlib import Path

from mcp_manager.organize import split_plan


def test_split_plan_marks_confirm_for_core(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    plan = [
        {"path": str(tmp_path / "a.gguf"), "category": "Models"},
        {"path": str(tmp_path / "b.pdf"), "category": "Docs"},
    ]
    rules = {"core_exts": [".gguf"], "large_threshold_bytes": 1}
    auto, confirm = split_plan(plan, rules)
    assert len(confirm) == 1
    assert confirm[0]["path"].endswith("a.gguf")


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_plan_split.py -v`
Expected: FAIL with "split_plan not defined"

**Step 3: Write minimal implementation**

```python
# mcp_manager/organize.py
from mcp_manager.aihub_rules import is_core_file, is_large_file


def split_plan(plan, rules):
    auto, confirm = [], []
    for item in plan:
        path = item["path"]
        if is_core_file(path, rules) or is_large_file(path, rules):
            confirm.append(item)
        else:
            auto.append(item)
    return auto, confirm
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_plan_split.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/organize.py tests/test_plan_split.py
git commit -m "feat: add plan split confirmation"
```

### Task 3: Scan roots + build plan + persist

**Files:**
- Modify: `mcp_manager/organize.py`
- Create: `tests/test_scan_flow.py`

**Step 1: Write the failing test**

```python
# tests/test_scan_flow.py
import sys
import unittest
from pathlib import Path

from mcp_manager.organize import run_scan


def test_run_scan_saves_plan(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    sample = tmp_path / "qwen.gguf"
    sample.write_bytes(b"x")
    env = {
        "AI_HUB_ROOT": str(tmp_path),
        "AI_SCAN_ROOTS": str(tmp_path),
    }
    plan = run_scan(env)
    assert plan["confirm"][0]["path"].endswith("qwen.gguf")


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_scan_flow.py -v`
Expected: FAIL with "run_scan not defined"

**Step 3: Write minimal implementation**

```python
# mcp_manager/organize.py
import os
from pathlib import Path
from mcp_manager.aihub_structure import ensure_structure
from mcp_manager.aihub_rules import load_rules
from mcp_manager.aihub_scan import build_plan


def _parse_roots(env, user_home):
    if env.get("AI_SCAN_ROOTS"):
        return env["AI_SCAN_ROOTS"].split(";")
    return get_default_roots(user_home)


def run_scan(env=None):
    env = env or os.environ
    hub = get_ai_hub_root()
    ensure_structure(hub)
    rules = load_rules(hub)
    roots = _parse_roots(env, str(Path.home()))
    files = []
    for root in roots:
        for p in Path(root).rglob("*"):
            if p.is_file():
                files.append(p)
    plan = build_plan(files, rules, hub)
    auto, confirm = split_plan(plan, rules)
    data = {"auto": auto, "confirm": confirm}
    save_plan(hub, data)
    return data
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_scan_flow.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/organize.py tests/test_scan_flow.py
git commit -m "feat: add scan flow"
```

### Task 4: Apply auto + confirm

**Files:**
- Modify: `mcp_manager/organize.py`
- Create: `tests/test_apply_flow.py`

**Step 1: Write the failing test**

```python
# tests/test_apply_flow.py
import sys
import unittest
from pathlib import Path

from mcp_manager.organize import apply_auto


def test_apply_auto_moves_files(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    src = tmp_path / "tool.zip"
    src.write_text("x", encoding="utf-8")
    plan = {"auto": [{"path": str(src), "category": "Tools"}], "confirm": []}
    moved = apply_auto(tmp_path, plan)
    assert (tmp_path / "Tools" / "tool.zip").exists()
    assert moved == 1


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_apply_flow.py -v`
Expected: FAIL with "apply_auto not defined"

**Step 3: Write minimal implementation**

```python
# mcp_manager/organize.py
from mcp_manager.aihub_apply import apply_plan


def apply_auto(root, plan):
    apply_plan(plan["auto"], root)
    return len(plan["auto"])
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_apply_flow.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/organize.py tests/test_apply_flow.py
git commit -m "feat: add apply auto"
```

### Task 5: Confirm apply flow

**Files:**
- Modify: `mcp_manager/organize.py`
- Create: `tests/test_confirm_flow.py`

**Step 1: Write the failing test**

```python
# tests/test_confirm_flow.py
import sys
import unittest
from pathlib import Path

from mcp_manager.organize import apply_confirm


def test_apply_confirm_moves_selected(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    src = tmp_path / "model.gguf"
    src.write_bytes(b"x")
    plan = {"auto": [], "confirm": [{"path": str(src), "category": "Models"}]}
    moved = apply_confirm(tmp_path, plan, [str(src)])
    assert (tmp_path / "Models" / "model.gguf").exists()
    assert moved == 1


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_confirm_flow.py -v`
Expected: FAIL with "apply_confirm not defined"

**Step 3: Write minimal implementation**

```python
# mcp_manager/organize.py

def apply_confirm(root, plan, selected_paths):
    selected = [p for p in plan["confirm"] if p["path"] in set(selected_paths)]
    apply_plan(selected, root)
    return len(selected)
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_confirm_flow.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/organize.py tests/test_confirm_flow.py
git commit -m "feat: add confirm apply"
```

### Task 6: Web endpoints wiring

**Files:**
- Modify: `web/routes.py`
- Modify: `tests/test_api.py`

**Step 1: Write the failing test**

```python
# tests/test_api.py (extend)

def test_scan_endpoint():
    client = TestClient(app)
    resp = client.post("/api/scan")
    assert resp.status_code == 200
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_api.py -v`
Expected: FAIL if endpoint not wired

**Step 3: Write minimal implementation**

```python
# web/routes.py
from mcp_manager.organize import run_scan, load_plan, apply_auto, apply_confirm, get_ai_hub_root

@router.post("/api/scan")
def scan():
    plan = run_scan()
    return {"ok": True, "plan": plan}

@router.get("/api/plan")
def plan():
    return load_plan(get_ai_hub_root())

@router.post("/api/confirm")
def confirm(payload: dict):
    plan = load_plan(get_ai_hub_root())
    moved = apply_confirm(get_ai_hub_root(), plan, payload.get("paths", []))
    return {"moved": moved}
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add web/routes.py tests/test_api.py
git commit -m "feat: wire scan endpoints"
```

### Task 7: Web UI buttons

**Files:**
- Modify: `web/static/index.html`
- Modify: `web/static/app.js`

**Step 1: Write the failing test**

```python
# tests/test_api.py (extend)

def test_index_has_buttons():
    client = TestClient(app)
    resp = client.get("/")
    assert "Scan" in resp.text
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_api.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```html
<button id="scan">Scan</button>
<button id="apply">Apply Auto</button>
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add web/static/index.html web/static/app.js tests/test_api.py
git commit -m "feat: add UI buttons"
```

---

Plan complete and saved to `docs/plans/2026-02-19-ai-hub-integration-plan.md`. Two execution options:

1. Subagent-Driven (this session) - I dispatch fresh subagent per task, review between tasks, fast iteration
2. Parallel Session (separate) - Open new session with executing-plans, batch execution with checkpoints

Which approach?
