@echo off
setlocal
cd /d %~dp0..

if not exist web_mcp_manager\.venv (
  python -m venv web_mcp_manager\.venv
)

call web_mcp_manager\.venv\Scripts\activate

pip install -r web_mcp_manager\requirements.txt

python -m uvicorn web_mcp_manager.server:app --host 127.0.0.1 --port 8765
