from fastapi import APIRouter

from mcp_manager.organize import run_scan, load_plan, apply_auto, apply_confirm, get_ai_hub_root

router = APIRouter()


@router.get("/api/tools")
def tools():
    return {"items": []}


@router.get("/api/plan")
def plan():
    return load_plan(get_ai_hub_root())


@router.post("/api/scan")
def scan():
    plan = run_scan()
    return {"ok": True, "plan": plan}


@router.post("/api/apply-auto")
def apply_auto_endpoint():
    plan = load_plan(get_ai_hub_root())
    moved = apply_auto(get_ai_hub_root(), plan)
    return {"moved": moved}


@router.post("/api/confirm")
def confirm(payload: dict):
    plan = load_plan(get_ai_hub_root())
    moved = apply_confirm(get_ai_hub_root(), plan, payload.get("paths", []))
    return {"moved": moved}
