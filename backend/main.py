"""
AdGenAI — FastAPI Application Entry Point.

Initializes the application with structured logging, CORS, static file
serving, database setup, and the pipeline health check endpoint.
"""
from __future__ import annotations

import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.routes import router
from backend.config import settings
from backend.models.database import init_db
from backend.models.schemas import HealthResponse
from backend.pipeline.orchestrator import PipelineOrchestrator
from backend.utils.logging_config import configure_logging

# ── Logging setup ────────────────────────────────────────────

configure_logging(
    level=settings.log_level,
    json_mode=settings.log_json,
    log_file=settings.log_file,
)

logger = logging.getLogger(__name__)


# ── Lifespan (replaces deprecated on_event) ──────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup → yield → shutdown."""
    logger.info("[STARTUP] Initializing database...")
    await init_db()
    logger.info("[STARTUP] AdGenAI ready.")
    yield
    logger.info("[SHUTDOWN] AdGenAI shutting down.")


# ── FastAPI Application ──────────────────────────────────────

app = FastAPI(
    title="AdGenAI",
    description="AI-powered advertising video generation pipeline. "
                "Executes the client's creative vision with professional precision.",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for output videos
app.mount("/outputs", StaticFiles(directory=str(settings.output_dir)), name="outputs")

# API routes
app.include_router(router, prefix="/api/v1")


# ── Health Check ─────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
async def health():
    """Full health check including API key and FFmpeg validation."""
    checks = PipelineOrchestrator.health_check()
    all_ok = all(v for v in checks.values() if isinstance(v, bool))
    return HealthResponse(
        status="ok" if all_ok else "degraded",
        service="adgenai",
        checks=checks,
    )
