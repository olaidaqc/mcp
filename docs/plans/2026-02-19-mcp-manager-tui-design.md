# MCP Manager TUI Design

Date: 2026-02-19

## Overview
Build a real, interactive MCP management tool that executes local system commands and shows live status, without any model/token usage. The primary UI is a clickable Textual TUI. If Textual is unavailable, the app falls back to a minimal terminal UI (Rich/text) so the tool remains usable.

## Goals
- Real command execution (no mock data).
- Live status for MCP/Skill/config/Git/MCP-startability.
- Clickable buttons for common actions.
- Real-time logs from command output.
- Stable on Windows PowerShell with zero token cost.
- Easy to extend without code changes.

## Non-goals
- Web UI in browser.
- Electron app.
- Cloud services or remote telemetry.

## Architecture
Layered design to maximize stability and extensibility:
- engine: command runner, status checks, action dispatcher, log handling.
- config: JSON defining checks and actions.
- ui: Textual app (primary), fallback UI (secondary).

## Components
- engine/runner.py
  - Executes commands with PowerShell.
  - Captures stdout/stderr/exit code.
  - Enforces timeout (default 60s).
  - Streams output into log queue.

- engine/checks.py
  - Periodic status checks (every 5s by default).
  - Produces a status snapshot for UI.

- engine/actions.py
  - Button-triggered commands (health check, sync, edit config, open project, restart services).

- engine/logs.py
  - In-memory log queue + append to runtime.log.

- ui/textual_app.py
  - Clickable buttons, status panel, logs panel.
  - Manual refresh button.
  - Visual error states (red) and success states (green).

- ui/fallback.py
  - Text-based menu and log tail view.
  - Number-based actions for minimal usability.

## Data Flow
- Timer -> checks -> status snapshot -> UI render.
- Button click -> actions -> runner -> log queue -> UI logs panel.

## Config Model (config/commands.json)
Defines:
- status_checks: list of commands with labels.
- actions: list of commands with labels and optional confirm prompts.
- paths: important files to open/edit.
This allows adding new buttons or checks without code changes.

## Command Mapping (Windows PowerShell)
Status checks (PowerShell equivalents):
- MCP config: Get-Content $env:USERPROFILE\.claude\mcp-config.json
- Skill directory: Get-ChildItem -Force $env:USERPROFILE\my-skills\superpowers
- Git status: git -C $env:USERPROFILE\my-skills status
- MCP startability: npx -y @modelcontextprotocol/server-filesystem --help

Actions:
- Health check: $env:USERPROFILE\my-skills\auto-check-notify.bat
- Sync config: $env:USERPROFILE\my-skills\sync-and-push.sh
- Edit config: code $env:USERPROFILE\.claude\mcp-config.json
- Open project: code $env:USERPROFILE\my-skills

## Refresh Strategy
- Auto refresh every 5 seconds.
- Manual refresh button triggers immediate status checks.
- UI keeps last known good state when a check fails.

## Error Handling
- Any non-zero exit code is marked as failed.
- Error output is shown in the log panel and status is colored red.
- Timeouts are reported with a clear message.

## Extensibility
- New commands are added to config/commands.json.
- UI reads config at startup; no code change required for new actions.

## Testing and Verification
- Manual run verifies status checks and button actions.
- Ensure runtime.log is appended with each command execution.
- Verify fallback UI triggers on missing Textual.

## Delivery
- A runnable Python entrypoint (mcp_manager.py) in repo root.
- Minimal dependencies; auto-install Textual if allowed; otherwise fallback UI.
