from pathlib import Path
import os
import json

from mcp_manager.aihub_rules import is_core_file, is_large_file


def get_default_roots(user_home):
    user_home = Path(user_home)
    roots = [str(user_home / "Downloads"), str(user_home / "Desktop"), str(user_home / "Documents")]
    exclude = str(user_home / "Desktop" / "claude").replace("\\", "/")
    return [r for r in roots if r.replace("\\", "/") != exclude]


def get_ai_hub_root():
    return Path(os.environ.get("AI_HUB_ROOT", "C:/Users/11918/AI-Hub"))


def _reports_dir(root):
    return Path(root) / "_reports"


def save_plan(root, plan):
    _reports_dir(root).mkdir(parents=True, exist_ok=True)
    path = _reports_dir(root) / "plan.json"
    path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")


def load_plan(root):
    path = _reports_dir(root) / "plan.json"
    if not path.exists():
        return {"auto": [], "confirm": []}
    return json.loads(path.read_text(encoding="utf-8"))


def split_plan(plan, rules):
    auto, confirm = [], []
    for item in plan:
        path = item["path"]
        if is_core_file(path, rules) or is_large_file(path, rules):
            confirm.append(item)
        else:
            auto.append(item)
    return auto, confirm
