from pathlib import Path
import os
import json

from mcp_manager.aihub_rules import load_rules
from mcp_manager.aihub_structure import ensure_structure
from mcp_manager.aihub_scan import build_plan
from mcp_manager.aihub_apply import apply_plan
from mcp_manager.aihub_learn import learn_from_confirmed
from mcp_manager.scan_filters import iter_scan_files


def get_default_roots(user_home):
    user_home = Path(user_home)
    roots = [str(user_home / "Downloads"), str(user_home / "Desktop"), str(user_home / "Documents")]
    exclude = str(user_home / "Desktop" / "claude").replace("\\", "/")
    return [r for r in roots if r.replace("\\", "/") != exclude]


def get_ai_hub_root(env=None):
    env = env or os.environ
    return Path(env.get("AI_HUB_ROOT", "C:/Users/11918/AI-Hub"))


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
    return [], list(plan)


def _parse_roots(env, user_home):
    if env.get("AI_SCAN_ROOTS"):
        return env["AI_SCAN_ROOTS"].split(";")
    return get_default_roots(user_home)


def _resolve_user_home(env):
    if env.get("AI_USER_HOME"):
        return env["AI_USER_HOME"]
    return str(Path.home())


def run_scan(env=None):
    env = env or os.environ
    hub = get_ai_hub_root(env)
    ensure_structure(hub)
    rules = load_rules(hub)
    user_home = _resolve_user_home(env)
    roots = _parse_roots(env, user_home)
    files = list(iter_scan_files(roots, rules, user_home=Path(user_home)))
    plan = build_plan(files, rules, hub)
    data = {"auto": [], "confirm": list(plan)}
    save_plan(hub, data)
    return data


def apply_auto(root, plan):
    apply_plan(plan["auto"], root)
    moved = len(plan["auto"])
    plan["auto"] = []
    save_plan(root, plan)
    return moved


def apply_confirm(root, plan, selected_paths):
    selected_set = set(selected_paths)
    selected = [p for p in plan["confirm"] if p["path"] in selected_set]
    apply_plan(selected, root)
    learn_from_confirmed(root, selected)
    plan["confirm"] = [p for p in plan["confirm"] if p["path"] not in selected_set]
    save_plan(root, plan)
    return len(selected)
