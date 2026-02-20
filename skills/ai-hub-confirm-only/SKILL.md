---
name: ai-hub-confirm-only
description: Use when managing AI-Hub confirm-only organizing (AI-only scans, rule/keyword updates, confirm moves) or restoring non-AI files that were moved into AI-Hub.
---

# AI Hub Confirm-Only

## Overview

Operate AI-Hub in confirm-only mode: scan for AI-only matches, review the plan, confirm selected moves, and keep rules and learned keywords accurate. Non-AI files must never move.

## Quick Start

1. Scan: `python -m mcp_manager.organize --scan`
2. Open UI: `start-web.bat` then `http://127.0.0.1:8000/`
3. Review plan: `C:\Users\11918\AI-Hub\_reports\plan.json`
4. Confirm moves: UI `Confirm Selected` (no auto)
5. Verify learning: `C:\Users\11918\AI-Hub\_rules\learned_keywords.json`

## Workflow (Confirm-Only)

### 1. Scan (AI-only)
- Default scan roots: `Downloads`, `Desktop`, `Documents` (excludes `Desktop\claude`)
- Env override `AI_HUB_ROOT` to change hub location
- Env override `AI_SCAN_ROOTS` (semicolon-separated) to control scan paths

### 2. Review Plan
- `C:\Users\11918\AI-Hub\_reports\plan.json` contains **confirm-only** items.
- `auto` should always be empty in confirm-only mode.

### 3. Confirm Selected
- Use the Web UI `Confirm Selected` button to move files.
- Each confirm updates `learned_keywords.json` for future matching.

### 4. Update Rules
- Rules file: `C:\Users\11918\AI-Hub\_rules\rules.json`
- Add keywords only if they are truly AI-specific.
- See `references/rules-keys.md` for key meanings.

### 5. Restore Non-AI (if needed)
- Use `scripts/restore_non_ai.py` to move non-AI items back to original paths.
- Script writes a restore report in `AI-Hub\_reports\`.

## Safety Guards

- **No auto-move**: confirm-only is mandatory.
- **Media excluded**: images/videos should never be moved.
- **Excluded paths**: games and system folders are ignored.

## Verification

- Tests: `python -m unittest discover -s tests -v`
- UI sanity check: `http://127.0.0.1:8000/` shows "Confirm Only"

## Common Mistakes

- Editing rules but not re-running a scan
- Confirming without reviewing the plan list
- Adding overly generic keywords that cause false positives

## References

- Rules reference: `references/rules-keys.md`
- Testing notes: `references/testing-notes.md`
