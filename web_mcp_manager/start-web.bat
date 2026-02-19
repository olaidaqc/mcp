@echo off
setlocal
cd /d %~dp0

if not exist .venv (
  python -m venv .venv
)

call .venv\Scripts\activate

pip install -r requirements.txt

python -m uvicorn web_mcp_manager.server:app --host 127.0.0.1 --port 8765
