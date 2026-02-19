# AI Hub Auto-Organizer Design

Date: 2026-02-19

## Goal
Create a sustainable, rule-driven AI file organizer that automatically classifies AI models/tools/docs into a global hub, supports daily scans, produces reports, and provides a lightweight web UI for review and confirmations. The system must not modify original file contents and must be safe for large or core files by requiring confirmation.

## Scope
- Global AI hub at `C:\Users\11918\AI-Hub`.
- Scan scope: `Downloads`, `Desktop`, `Documents` under `C:\Users\11918`, excluding `C:\Users\11918\Desktop\claude` and system/app directories.
- Classify by type: `Models`, `Tools`, `Plugins`, `Datasets`, `Docs`, `Code`.
- Daily scheduled scan + manual trigger.
- V1 web UI: status, plan, confirmations, latest report, trigger scan.

## Directory Structure
```
C:\Users\11918\AI-Hub\
  Models\
  Tools\
  Plugins\
  Datasets\
  Docs\
  Code\
  _incoming\
  _reports\
  _rules\
```
Each directory contains a `README.md` describing purpose and rules. For each moved file, write a sidecar note `<filename>.aiinfo.txt` with metadata (no changes to original file).

## Classification Rules (Priority Order)
1. **Explicit path rules** (whitelist/blacklist) from `AI-Hub\_rules`.
2. **Core model file rules** by extension: `.gguf .safetensors .bin .pth .pt .ckpt .onnx .tflite .ggml`.
3. **Keyword rules** (model families and AI tooling keywords): `llama, qwen, mistral, mixtral, gemma, phi, deepseek, stable-diffusion, sdxl, diffusion, lora, embedding, tokenizer, clip, t2i, whisper, tts, asr, ollama, lmstudio, comfyui`.
4. **File type rules** for Docs/Code/Tools/Plugins/Datasets.
5. **Fallback** to `_incoming` if no confident match.

## Confirmation Policy
- **Always confirm** for core model files.
- **Confirm** any file >= 1 GB.
- Others auto-move.
All actions recorded in `AI-Hub\_reports\index.jsonl`.

## Reports and Index
- `AI-Hub\_reports\index.jsonl`: append-only move/confirm/skip entries.
- `AI-Hub\_reports\last_run.json`: timestamp and summary.
- `AI-Hub\_reports\errors.log`: non-fatal errors.

## Sidecar Metadata (aiinfo)
Fields:
- original_path
- target_path
- size_bytes
- sha256
- matched_rules
- detected_family
- moved_at

## Web UI (V1)
- `GET /api/status`: last run, counts, scope.
- `GET /api/plan`: auto-move list + confirm list.
- `POST /api/confirm`: approve selected moves.
- `POST /api/scan`: trigger scan.
- `GET /api/report/latest`: recent summary.

## CLI
- `python -m mcp_manager.organize --scan` (run scan)
- `python -m mcp_manager.organize --plan` (print plan)
- `python -m mcp_manager.organize --apply` (apply auto moves)

## Error Handling
- Skip unreadable files, log to `errors.log`.
- Name collisions: append `_dupN`.
- Never modify original file contents.

## Testing
- Unit tests: rule matching, classification, confirmation thresholds, index writing, collision handling.
- API tests: status, plan, confirm, scan endpoints.

## Upgrade Path
- Rules are data-driven in `AI-Hub\_rules` and can be edited without code changes.
- Future v2: drag-and-drop UI for manual reclassification.
