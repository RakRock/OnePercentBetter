"""AI Forge — FastAPI application entrypoint."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.database import init_db
from app.scripts.seed import seed_if_empty


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("TESTING") != "1":
        await init_db()
        await seed_if_empty()
    yield


settings = get_settings()
app = FastAPI(
    title="AI Forge API",
    description="AI Engineering Learning Platform — Phase 1",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "ai-forge", "phase": 1}
