# AI-Hub AI-Only + Confirm + Learning Design

Date: 2026-02-19

## Goal
Make AI-Hub move **only AI-related files**, require **explicit confirmation for all AI moves**, and enable **continuous rule learning** from confirmed moves without touching non-AI content.

## Scope
- Global hub: `C:\Users\11918\AI-Hub`
- Scan scope: `Downloads`, `Desktop`, `Documents` under `C:\Users\11918` (excluding `C:\Users\11918\Desktop\claude`)
- Categories: `Models`, `Tools`, `Plugins`, `Datasets`, `Docs`, `Code`
- Non-AI files are never moved
- All AI files require user confirmation (no auto-move)
- Continuous rule learning from confirmed items

## Behavior Changes
1. **AI-Only Move**: If a file does not match AI rules, it is ignored (not moved).
2. **All Confirm**: The scan produces only a `confirm` list; `auto` is always empty.
3. **Media Exclusion**: Common image/video extensions are never moved, even if keywords match.
4. **Detailed Classification**: AI files are routed to a richer taxonomy, but stored under existing top-level categories.

## Detailed Classification Taxonomy
Top-level categories remain:
- `Models`, `Tools`, `Plugins`, `Datasets`, `Docs`, `Code`

Sub-classification (used for rule matching and metadata, but stored in top-level folders):
- Models:
  - `LLM`, `Vision`, `Audio`, `Embeddings`, `Rerankers`
- Tools:
  - `Runtime`, `UI`, `Workflow`, `VectorDB`, `Finetune`, `Eval`, `Convert`
- Plugins:
  - `MCP`, `IDE`
- Datasets:
  - `text`, `vision`, `audio`, `multimodal`
- Docs:
  - `papers`, `tutorials`, `manuals`
- Code:
  - `projects`, `scripts`, `notebooks`

The sub-class is stored in metadata (`detected_family`) and optionally used as a suffix in the rule match report, but files remain inside the existing top-level category directories.

## Rule System
Rules live in `C:\Users\11918\AI-Hub\_rules\rules.json` and include:
- `core_exts`: known model extensions (LLM weights, etc.)
- `ai_keywords`: AI model/tool keywords
- `tool_keywords`: tool/framework keywords
- `plugin_keywords`: MCP/IDE plugin keywords
- `dataset_keywords`: dataset signals
- `doc_keywords`: paper/tutorial signals
- `code_keywords`: code/project signals
- `exclude_exts`: media extensions to ignore
- `exclude_paths`: glob/prefix patterns to skip (games, system folders, etc.)

Classification is **positive-only**:
- A file must match at least one AI rule to be considered AI.
- If no match, it is ignored.

## Confirmation Policy
- **All AI matches require confirmation** (no auto-move).
- `auto` list remains empty.
- Confirmation UI remains the only way to move files.

## Learning Loop (Continuous Updates)
When a user confirms moves:
1. Capture tokens from file names and parent folders.
2. Add new tokens to `learned_keywords.json` (separate from base rules).
3. Use `learned_keywords.json` in future scans (merged into rules at runtime).

Safety:
- Only learn from confirmed items.
- Never auto-move; learning only improves classification recall.
- Learning file is append-only with de-duplication.

## UI/UX
- `Apply Auto` button is disabled or hidden.
- `Confirm Selected` is required for moves.
- Status shows “AI-only scan” mode and “confirm required”.

## Reports
Existing reports remain:
- `AI-Hub\_reports\index.jsonl`
- `AI-Hub\_reports\plan.json`
- `AI-Hub\_reports\last_run.json`

## Testing
- Unit tests:
  - AI-only: non-AI files produce no plan entries
  - confirm-only: `auto` always empty
  - media exclusion: image/video never planned
  - learning: confirmed items update `learned_keywords.json`
- API tests:
  - `/api/plan` returns confirm-only list
  - `Apply Auto` does nothing / returns 0

## Non-Goals
- No auto-categorization of non-AI files
- No destructive cleanup of user folders
- No background daemon beyond existing scan triggers
