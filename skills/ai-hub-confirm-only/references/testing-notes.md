# Testing Notes (Manual)

## Baseline Failure Observed
- Non-AI files were previously moved into `AI-Hub\_incoming` during broad scans.
- Restoration was required to move files back to original locations.

## Manual Test Checklist
1. Run scan and confirm only AI files appear in `plan.json`.
2. Verify `auto` list remains empty.
3. Confirm selected items and verify `learned_keywords.json` updates.
4. Use `scripts/restore_non_ai.py` on a test hub to verify safe restoration.
