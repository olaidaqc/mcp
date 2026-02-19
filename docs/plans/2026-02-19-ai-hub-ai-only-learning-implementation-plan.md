# AI-Hub AI-Only + Confirm + Learning Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make AI-Hub move only AI-related files, require confirmation for all AI moves, and learn new keywords from confirmed items.

**Architecture:** Extend the rules system to support AI-only matching, exclusions, and learned keywords. Update scanning to skip non-AI files, route all matches to confirm-only plans, and update the web UI to reflect confirm-only mode.

**Tech Stack:** Python 3, FastAPI, Standard Library `unittest`

---

### Task 1: Rule defaults + rule file bootstrap

**Files:**
- Modify: `mcp_manager/aihub_rules.py`
- Modify: `mcp_manager/aihub_structure.py`
- Test: `tests/test_rules_defaults.py`

**Step 1: Write the failing test**

```python
# tests/test_rules_defaults.py
from pathlib import Path
from mcp_manager.aihub_rules import load_rules, ensure_rules

def test_ensure_rules_creates_rules_file(tmp_path):
    ensure_rules(tmp_path)
    assert (tmp_path / "_rules" / "rules.json").exists()

def test_load_rules_includes_ai_only_defaults(tmp_path):
    ensure_rules(tmp_path)
    rules = load_rules(tmp_path)
    assert "exclude_exts" in rules
    assert "ai_keywords" in rules
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_rules_defaults.py -v`  
Expected: FAIL with "cannot import name 'ensure_rules'" or missing keys

**Step 3: Write minimal implementation**

```python
# mcp_manager/aihub_rules.py
DEFAULT_RULES = {
    "core_exts": [...],
    "exclude_exts": [...],
    "exclude_paths": [...],
    "ai_keywords": [...],
    "tool_keywords": [...],
    "plugin_keywords": [...],
    "dataset_keywords": [...],
    "doc_keywords": [...],
    "code_keywords": [...],
    "model_families": {
        "Vision": [...],
        "Audio": [...],
        "Embeddings": [...],
        "Rerankers": [...],
        "LLM": [...],
    },
    "tool_families": {...},
}

def ensure_rules(root):
    rules_path = Path(root) / "_rules" / "rules.json"
    rules_path.parent.mkdir(parents=True, exist_ok=True)
    if not rules_path.exists():
        rules_path.write_text(json.dumps(DEFAULT_RULES, ensure_ascii=False, indent=2), encoding="utf-8")
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_rules_defaults.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/aihub_rules.py mcp_manager/aihub_structure.py tests/test_rules_defaults.py
git commit -m "feat: add ai-only rule defaults and bootstrap"
```

---

### Task 2: AI-only classification + exclusions

**Files:**
- Modify: `mcp_manager/aihub_scan.py`
- Modify: `mcp_manager/aihub_rules.py`
- Test: `tests/test_ai_only_scan.py`

**Step 1: Write the failing test**

```python
# tests/test_ai_only_scan.py
from pathlib import Path
from mcp_manager.aihub_scan import build_plan

def test_non_ai_file_is_ignored(tmp_path):
    file_path = tmp_path / "game.exe"
    file_path.write_bytes(b"x")
    rules = {"core_exts": [], "ai_keywords": ["llama"], "tool_keywords": [], "exclude_exts": [], "exclude_paths": []}
    plan = build_plan([file_path], rules, tmp_path)
    assert plan == []

def test_ai_file_is_classified(tmp_path):
    file_path = tmp_path / "ollama.exe"
    file_path.write_bytes(b"x")
    rules = {"core_exts": [], "ai_keywords": ["ollama"], "tool_keywords": ["ollama"], "exclude_exts": [], "exclude_paths": []}
    plan = build_plan([file_path], rules, tmp_path)
    assert plan[0]["category"] == "Tools"
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_ai_only_scan.py -v`  
Expected: FAIL with non-AI included or missing logic

**Step 3: Write minimal implementation**

```python
# mcp_manager/aihub_scan.py
def _is_excluded(path, rules): ...
def _match_any(path, keywords): ...
def classify_ai_path(path, rules): ...
def build_plan(files, rules, root):
    plan = []
    for f in files:
        if _is_excluded(f, rules):
            continue
        match = classify_ai_path(f, rules)
        if not match:
            continue
        category, family, matched_rules = match
        plan.append({"path": str(f), "category": category, "family": family, "matched_rules": matched_rules})
    return plan
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_ai_only_scan.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/aihub_scan.py mcp_manager/aihub_rules.py tests/test_ai_only_scan.py
git commit -m "feat: enforce ai-only classification and exclusions"
```

---

### Task 3: Confirm-only plan generation

**Files:**
- Modify: `mcp_manager/organize.py`
- Modify: `tests/test_plan_split.py`
- Modify: `tests/test_scan_flow.py`

**Step 1: Write the failing test**

```python
# tests/test_plan_split.py
def test_split_plan_is_confirm_only():
    plan = [{"path": "x.gguf", "category": "Models"}]
    auto, confirm = split_plan(plan, {"core_exts": [".gguf"], "large_threshold_bytes": 0})
    assert auto == []
    assert len(confirm) == 1
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_plan_split.py -v`  
Expected: FAIL with auto non-empty

**Step 3: Write minimal implementation**

```python
# mcp_manager/organize.py
def split_plan(plan, rules):
    return [], list(plan)

def run_scan(env=None):
    ...
    plan = build_plan(...)
    data = {"auto": [], "confirm": plan}
    save_plan(hub, data)
    return data
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_plan_split.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/organize.py tests/test_plan_split.py tests/test_scan_flow.py
git commit -m "feat: make scans confirm-only"
```

---

### Task 4: Learn keywords from confirmed items

**Files:**
- Create: `mcp_manager/aihub_learn.py`
- Modify: `mcp_manager/organize.py`
- Modify: `mcp_manager/aihub_rules.py`
- Test: `tests/test_learning.py`

**Step 1: Write the failing test**

```python
# tests/test_learning.py
from pathlib import Path
from mcp_manager.aihub_learn import learn_from_confirmed, load_learned

def test_learned_keywords_updated(tmp_path):
    items = [{"path": str(tmp_path / "new-ollama-tool.exe"), "category": "Tools"}]
    learn_from_confirmed(tmp_path, items)
    learned = load_learned(tmp_path)
    assert "ollama" in learned["Tools"]
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_learning.py -v`  
Expected: FAIL with module not found

**Step 3: Write minimal implementation**

```python
# mcp_manager/aihub_learn.py
def load_learned(root): ...
def save_learned(root, data): ...
def extract_tokens(path): ...
def learn_from_confirmed(root, items):
    learned = load_learned(root)
    for item in items:
        learned[item["category"]].update(extract_tokens(item["path"]))
    save_learned(root, learned)
```

Integrate in `organize.apply_confirm`:
```python
from mcp_manager.aihub_learn import learn_from_confirmed
learn_from_confirmed(root, selected)
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_learning.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add mcp_manager/aihub_learn.py mcp_manager/organize.py mcp_manager/aihub_rules.py tests/test_learning.py
git commit -m "feat: learn keywords from confirmed moves"
```

---

### Task 5: UI confirm-only mode + disable Apply Auto

**Files:**
- Modify: `web/static/index.html`
- Modify: `web/static/app.js`
- Test: `tests/test_api.py`

**Step 1: Write the failing test**

```python
# tests/test_api.py
def test_index_has_confirm_only_text():
    client = TestClient(app)
    resp = client.get("/")
    assert "Confirm Only" in resp.text
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_api.py -v`  
Expected: FAIL with missing text

**Step 3: Write minimal implementation**

```html
<!-- web/static/index.html -->
<div id="mode">Confirm Only</div>
<button id="apply" disabled>Apply Auto (disabled)</button>
```

```js
// web/static/app.js
document.getElementById("apply").disabled = true;
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_api.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add web/static/index.html web/static/app.js tests/test_api.py
git commit -m "feat: update UI for confirm-only mode"
```

---

### Task 6: Documentation update

**Files:**
- Modify: `README.md`

**Step 1: Write the failing test**

```python
# tests/test_paths.py
def test_ai_only_mode_documented():
    content = Path("README.md").read_text(encoding="utf-8")
    assert "confirm-only" in content.lower()
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_paths.py -v`  
Expected: FAIL

**Step 3: Write minimal implementation**

```markdown
## AI-Hub Confirm-Only Mode
AI files require confirmation before moving. Non-AI files are ignored.
Rules live in `C:\Users\11918\AI-Hub\_rules\rules.json`.
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_paths.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add README.md tests/test_paths.py
git commit -m "docs: explain confirm-only ai-hub behavior"
```

---

### Task 7: Full test pass

**Step 1: Run full test suite**

Run: `python -m unittest discover -s tests -v`  
Expected: PASS

**Step 2: Commit (if any missed changes)**

```bash
git status -sb
```

