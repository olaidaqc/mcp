from fastapi import APIRouter

router = APIRouter()


@router.get("/api/tools")
def tools():
    return {"items": []}
