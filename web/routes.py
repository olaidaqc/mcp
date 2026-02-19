from fastapi import APIRouter

router = APIRouter()


@router.get("/api/tools")
def tools():
    return {"items": []}


@router.get("/api/plan")
def plan():
    return {"auto": [], "confirm": []}


@router.post("/api/scan")
def scan():
    return {"ok": True}
