# AI Hub Auto-Organizer Integration Design

Date: 2026-02-19

## Goal
Integrate the AI Hub organizer end-to-end: scan user folders daily, build a plan, require confirmation for core/large files, apply moves with sidecar metadata and reports, and expose a lightweight web UI + CLI to view/confirm/trigger scans.

## Scope
- Global AI hub root: `C:\Users\11918\AI-Hub` (override with `AI_HUB_ROOT` env var)
- Scan roots: `Downloads`, `Desktop`, `Documents` under `C:\Users\11918` (exclude `Desktop\claude`)
- Classification by type: `Models/Tools/Plugins/Datasets/Docs/Code`
- Daily scan + manual scan trigger
- Web UI for status, plan, confirmation, and scan trigger

## Data Flow
1. Ensure AI Hub structure exists (create folders + README.md)
2. Scan configured roots for AI-related files
3. Build plan: classify, mark `confirm` for core files or >=1GB
4. Persist plan to `AI-Hub\_reports\plan.json`
5. Apply auto moves immediately; confirm items only when approved
6. Write sidecar `<filename>.aiinfo.txt` and append to `index.jsonl`

## Confirmation Rules
- Always confirm core model files by extension
- Always confirm files >= 1 GB

## Web UI (V1)
- `/` shows status + plan
- Buttons: `Scan`, `Apply Auto`, `Confirm Selected`

## Safety
- Never modify original file contents
- Name collisions get `_dupN`
- Errors logged to `AI-Hub\_reports\errors.log`

## Extensibility
- Rules in `AI-Hub\_rules\rules.json`
- Keywords and thresholds editable without code changes

## Demo / Visual Flow
- Web UI at `http://127.0.0.1:8000/`
- CLI: `python -m mcp_manager.organize --scan` / `--apply`
- Demo runs can use `AI_HUB_ROOT` + `AI_SCAN_ROOTS` env vars to avoid moving real files
