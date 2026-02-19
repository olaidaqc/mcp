from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from web.routes import router

app = FastAPI()


@app.get("/api/status")
def status():
    return {"ok": True}


app.include_router(router)
app.mount("/", StaticFiles(directory="web/static", html=True), name="static")
