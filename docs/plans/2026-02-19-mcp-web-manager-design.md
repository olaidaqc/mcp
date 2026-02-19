# MCP Web Manager Design

Date: 2026-02-19

## Overview
Build a local-only web management UI for MCP that can execute real system commands, display live status, and stream logs. Runs on `http://127.0.0.1:8765` with no authentication, intended for single-machine use.

## Goals
- Real command execution (no mock data)
- Live status for MCP/Skill/config/Git/MCP startability
- Button-based actions for common commands
- Log panel with recent output
- Local-only (localhost) and zero token usage
- Easy to extend via config

## Non-goals
- Public network access
- Cloud deployment
- Complex auth/role management

## Architecture
- Backend: FastAPI server
- Frontend: static HTML/JS/CSS
- Config-driven commands (JSON)
- In-memory log buffer + append to `runtime.log`

## Files/Structure
```
web-mcp-manager/
  server.py
  requirements.txt
  config/commands.json
  web/
    index.html
    app.js
    styles.css
  start-web.bat
```

## Backend Design
### Command Execution
- Use PowerShell via `subprocess.Popen` to stream output line-by-line.
- Timeout default: 60s per command.
- Append each line to in-memory ring buffer and to `runtime.log`.

### API Endpoints
- `GET /api/status`
  - Runs all `status_checks` from config
  - Returns list of {label, ok, output, ts}
- `POST /api/action/{id}`
  - Executes action by index in config
  - Streams output into logs
  - Returns {exit_code, output_tail}
- `GET /api/logs?limit=200`
  - Returns last N log lines

### Config
`web-mcp-manager/config/commands.json`
- `status_checks`: label + PowerShell command
- `actions`: label + PowerShell command

## Frontend Design
- Single page with 3 sections:
  - Status panel (auto refresh every 5s + manual refresh)
  - Action buttons
  - Log panel (poll every 2s)
- UI shows success/failure with color badges
- Shows last update time

## Error Handling
- Non-zero exit codes show red status and log entry
- Command timeout logged as error
- API returns error details in JSON

## Extensibility
- Add commands by editing `config/commands.json`
- UI renders buttons and status from config

## Operations
- `start-web.bat`:
  - create venv if missing
  - install dependencies
  - start server on 127.0.0.1:8765

## Testing
- Unit tests for command runner and config loader
- Manual verification:
  - Open http://127.0.0.1:8765
  - Trigger action and see logs update
  - Verify status refresh
