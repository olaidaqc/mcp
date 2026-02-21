# AI-Hub Confirm-Only UI Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a simple, efficient confirm-only UI with filters, batch selection, detail panel, and theme selector that persists.

**Architecture:** Keep backend APIs unchanged and implement all UX improvements in `web/static/*`. Use client-side filtering and selection, with a right-side detail panel driven by the current selection. Persist theme choice in `localStorage`.

**Tech Stack:** HTML, CSS, Vanilla JS, Python `unittest` (existing tests)

---

### Task 1: Expand HTML structure for table, filters, and detail panel

**Files:**
- Modify: `web/static/index.html`
- Test: `tests/test_api.py`

**Step 1: Write the failing test**

```python
# tests/test_api.py
def test_index_has_confirm_flow_table_headers():
    client = TestClient(app)
    resp = client.get("/")
    assert "Category" in resp.text
    assert "Name" in resp.text
    assert "Size" in resp.text
    assert "Family" in resp.text

def test_index_has_theme_selector():
    client = TestClient(app)
    resp = client.get("/")
    assert "Theme" in resp.text
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_api.py -v`  
Expected: FAIL with missing header text

**Step 3: Write minimal implementation**

```html
<!-- web/static/index.html -->
<div class="toolbar">
  <label>Theme
    <select id="theme-select">...</select>
  </label>
  ...
</div>
<table id="plan-table">
  <thead>
    <tr><th>Category</th><th>Name</th><th>Size</th><th>Family</th></tr>
  </thead>
  <tbody></tbody>
</table>
<aside id="detail-panel"></aside>
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_api.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add web/static/index.html tests/test_api.py
git commit -m "feat: add confirm-flow layout and theme selector"
```

---

### Task 2: Implement client-side rendering, filtering, and selection

**Files:**
- Modify: `web/static/app.js`
- Test: `tests/test_api.py`

**Step 1: Write the failing test**

```python
# tests/test_api.py
def test_index_has_filter_controls():
    client = TestClient(app)
    resp = client.get("/")
    assert "Search" in resp.text
    assert "Filter" in resp.text
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_api.py -v`  
Expected: FAIL with missing labels

**Step 3: Write minimal implementation**

```js
// web/static/app.js
// Render rows, keep selection set, apply filters, update detail panel
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_api.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add web/static/app.js tests/test_api.py
git commit -m "feat: add table rendering and filters"
```

---

### Task 3: Add theme system with persistence

**Files:**
- Modify: `web/static/styles.css`
- Modify: `web/static/app.js`
- Test: `tests/test_api.py`

**Step 1: Write the failing test**

```python
# tests/test_api.py
def test_index_has_theme_hook():
    client = TestClient(app)
    resp = client.get("/")
    assert "data-theme" in resp.text or "theme-select" in resp.text
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_api.py -v`  
Expected: FAIL if no theme hook

**Step 3: Write minimal implementation**

```css
/* web/static/styles.css */
:root { --bg: ...; --fg: ...; }
[data-theme="dark"] { ... }
[data-theme="sand"] { ... }
```

```js
// web/static/app.js
// Load theme from localStorage and set data-theme on <body>
// Save on change
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests/test_api.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add web/static/styles.css web/static/app.js tests/test_api.py
git commit -m "feat: add themes with persistence"
```

---

### Task 4: Full test pass

**Step 1: Run full test suite**

Run: `python -m unittest discover -s tests -v`  
Expected: PASS

**Step 2: Commit (if any missed changes)**

```bash
git status -sb
```
