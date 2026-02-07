
from fastapi import FastAPI

from app.api.routes import sessions
from app.core.db import init_models

app = FastAPI(title="DevSprint API", version="0.1.0")

@app.on_event("startup")
async def on_startup() -> None:
    await init_models()

app.include_router(sessions.router, prefix="/api/v1")

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "DevSprint API running"}
