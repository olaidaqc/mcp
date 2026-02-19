from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/api/status")
def status():
    return {"ok": True}


app.mount("/", StaticFiles(directory="web/static", html=True), name="static")
