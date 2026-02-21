# AI-Hub Confirm-Only UI (Simple + Theme) Design

Date: 2026-02-21

## Goal
Provide a simple, high‑efficiency confirm-only UI with search, filters, batch selection, and a readable detail panel. Add theme switching that persists between sessions.

## Scope
- Web UI only (`web/static/*`)
- Confirm-only flow remains enforced
- No changes to backend API shape (reuse `/api/plan`, `/api/scan`, `/api/confirm`)
- Themes stored in `localStorage`

## UX Principles
- Keep primary actions obvious and grouped
- Keep table minimal (category, name, size, family)
- Put full details in a side panel
- Avoid nested navigation or hidden controls

## Layout
Top bar:
- `Scan`
- `Confirm Selected`
- `Select All (Filtered)`
- `Clear Selection`
- Search input
- Category filter
- Family filter
- Size range (min/max)
- Theme selector

Main:
- Left: table with columns `Category`, `Name`, `Size`, `Family`
- Right: details panel showing full path, matched rules, family, size, category

Footer:
- Status bar with last action result and selected count

## Data Flow
- On load: `GET /api/plan` → render table + details
- On Scan: `POST /api/scan` → refresh plan
- On Confirm: collect checked paths → `POST /api/confirm`
- On theme change: save to `localStorage` and apply class

## Filtering Logic
Client-side filters:
- Search matches file name and path
- Category filter matches item.category
- Family filter matches item.family
- Size min/max uses file size (if available)

## Error Handling
- API errors displayed in status bar
- Empty list shows “No items to confirm”
- Confirm without selection shows a warning in status bar

## Testing
- UI tests for presence of table headers and theme selector
- API tests already cover scan/confirm endpoints
- Manual: verify theme persists after refresh

## Non-Goals
- No drag-and-drop
- No server-side search
- No auto-move
