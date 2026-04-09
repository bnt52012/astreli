"""
API Routes — AdGenAI Pipeline.

REST endpoints for project CRUD, cost estimation, and WebSocket progress.

Uses the new architecture:
- Enums from models/enums.py
- Pipeline from pipeline/orchestrator.py
- Mode detection from pipeline/mode_detector.py
"""
from __future__ import annotations

import json
import logging
import uuid
from pathlib import Path
from typing import Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.models.database import Project, get_db
from backend.models.enums import JobStatus, PipelineMode, QualityLevel, TargetPlatform
from backend.models.schemas import (
    CostEstimateRequest,
    CostEstimateResponse,
    ProjectResponse,
)
from backend.pipeline.mode_detector import ModeDetector
from backend.pipeline.orchestrator import PipelineOrchestrator

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory state store for running pipelines (replace with Redis in production)
_pipeline_progress: dict[str, dict] = {}
_websocket_connections: dict[str, list[WebSocket]] = {}


# ── Helpers ───────────────────────────────────────────────────


async def _save_upload(file: UploadFile, dest_dir: Path) -> str:
    """Save an uploaded file and return its path."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    path = dest_dir / filename
    content = await file.read()
    path.write_bytes(content)
    return str(path)


async def _broadcast_progress(project_id: str, progress_data: dict):
    """Send pipeline progress to all WebSocket connections for this project."""
    _pipeline_progress[project_id] = progress_data
    conns = _websocket_connections.get(project_id, [])
    payload = json.dumps(progress_data)
    dead = []
    for ws in conns:
        try:
            await ws.send_text(payload)
        except Exception:
            dead.append(ws)
    for ws in dead:
        conns.remove(ws)


# ── Routes ────────────────────────────────────────────────────


@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    scenario: str = Form(...),
    brand_name: Optional[str] = Form(None),
    brand_tone: Optional[str] = Form(None),
    brand_colors: Optional[str] = Form(None),
    quality_level: str = Form("premium"),
    mannequin_images: list[UploadFile] = File(default=[]),
    product_images: list[UploadFile] = File(default=[]),
    decor_images: list[UploadFile] = File(default=[]),
    logo: Optional[UploadFile] = File(None),
    music: Optional[UploadFile] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db),
):
    """Create a new ad generation project and start the pipeline.

    The client's scenario is sacred — the pipeline executes it with
    professional precision without modifying creative intent.
    """
    project_id = str(uuid.uuid4())
    upload_dir = settings.upload_dir / project_id

    # Save uploaded files
    mannequin_paths = [
        await _save_upload(f, upload_dir / "mannequin") for f in mannequin_images
    ]
    product_paths = [
        await _save_upload(f, upload_dir / "product") for f in product_images
    ]
    decor_paths = [
        await _save_upload(f, upload_dir / "decor") for f in decor_images
    ]
    logo_path = await _save_upload(logo, upload_dir) if logo else None
    music_path = await _save_upload(music, upload_dir) if music else None

    # Detect mode using the new ModeDetector
    mode, valid_mannequin = ModeDetector.detect(mannequin_paths or None)

    # Parse brand colors from comma-separated string
    colors = [c.strip() for c in brand_colors.split(",")] if brand_colors else None

    # Save to database
    project = Project(
        id=project_id,
        scenario=scenario,
        brand_name=brand_name,
        brand_config={"tone": brand_tone, "colors": colors},
        mode=mode.value,
        status=JobStatus.PENDING.value,
        mannequin_images=valid_mannequin,
        product_images=product_paths,
        decor_images=decor_paths,
        logo_path=logo_path,
        music_path=music_path,
    )
    db.add(project)
    await db.commit()

    # Start pipeline in background
    background_tasks.add_task(
        _run_pipeline,
        project_id=project_id,
        scenario=scenario,
        mannequin_paths=valid_mannequin,
        product_paths=product_paths,
        decor_paths=decor_paths,
        logo_path=logo_path,
        music_path=music_path,
        brand_name=brand_name,
        brand_tone=brand_tone,
        brand_colors=colors,
        quality_level=QualityLevel(quality_level),
    )

    return ProjectResponse(
        id=project_id,
        status=JobStatus.PENDING,
        mode=mode,
        created_at=project.created_at,
        updated_at=project.updated_at,
        scenes_count=0,
        progress=0.0,
    )


async def _run_pipeline(
    project_id: str,
    scenario: str,
    mannequin_paths: list[str],
    product_paths: list[str],
    decor_paths: list[str],
    logo_path: str | None,
    music_path: str | None,
    brand_name: str | None,
    brand_tone: str | None,
    brand_colors: list[str] | None,
    quality_level: QualityLevel = QualityLevel.PREMIUM,
):
    """Background task to run the full pipeline."""

    async def on_progress(update):
        """Progress callback — broadcast via WebSocket and update DB."""
        progress_data = {
            "project_id": project_id,
            "step": update.step,
            "progress": update.overall_progress,
            "message": update.message,
            "status": update.status.value if update.status else None,
            "scenes": update.scenes or {},
        }
        await _broadcast_progress(project_id, progress_data)

        # Also update database
        from backend.models.database import async_session

        async with async_session() as db:
            result = await db.execute(
                select(Project).where(Project.id == project_id)
            )
            project = result.scalar_one_or_none()
            if project:
                project.status = (
                    update.status.value if update.status else project.status
                )
                project.progress = update.overall_progress
                if update.error:
                    project.error = update.error
                await db.commit()

    orchestrator = PipelineOrchestrator(
        on_progress=on_progress,
        quality_level=quality_level,
    )

    try:
        await orchestrator.run(
            project_id=project_id,
            scenario=scenario,
            mannequin_images=mannequin_paths,
            product_images=product_paths,
            decor_images=decor_paths,
            logo_path=logo_path,
            music_path=music_path,
            brand_name=brand_name,
            brand_tone=brand_tone,
            brand_colors=brand_colors,
        )
    except Exception as e:
        logger.exception("[API] Pipeline failed for project %s", project_id)
        # Update DB with failure
        from backend.models.database import async_session

        async with async_session() as db:
            result = await db.execute(
                select(Project).where(Project.id == project_id)
            )
            project = result.scalar_one_or_none()
            if project:
                project.status = JobStatus.FAILED.value
                project.error = str(e)
                await db.commit()


@router.post("/projects/estimate", response_model=CostEstimateResponse)
async def estimate_cost(request: CostEstimateRequest):
    """Estimate pipeline cost without running generation.

    Runs GPT-4o scenario analysis only and calculates expected API costs.
    """
    orchestrator = PipelineOrchestrator()
    result = await orchestrator.estimate_cost(
        scenario=request.scenario,
        mode=PipelineMode.PRODUIT_UNIQUEMENT,  # Conservative estimate
        brand_name=request.brand_name,
        brand_tone=request.brand_tone,
        quality_check_enabled=request.quality_check_enabled,
    )
    return CostEstimateResponse(**result)


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, db: AsyncSession = Depends(get_db)):
    """Get project status and metadata."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectResponse(
        id=project.id,
        status=JobStatus(project.status),
        mode=PipelineMode(project.mode) if project.mode else None,
        created_at=project.created_at,
        updated_at=project.updated_at,
        scenes_count=len(project.scenes_data) if project.scenes_data else 0,
        progress=project.progress or 0.0,
        video_url=project.video_url,
        error=project.error,
    )


@router.get("/projects/{project_id}/scenes")
async def get_project_scenes(
    project_id: str, db: AsyncSession = Depends(get_db),
):
    """Get detailed scene data for a project."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "project_id": project_id,
        "analysis": project.analysis_result,
        "scenes": project.scenes_data or [],
    }


@router.get("/projects")
async def list_projects(
    user_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List recent projects, optionally filtered by user."""
    query = select(Project).order_by(Project.created_at.desc()).limit(50)
    if user_id:
        query = query.where(Project.user_id == user_id)
    result = await db.execute(query)
    projects = result.scalars().all()
    return [
        ProjectResponse(
            id=p.id,
            status=JobStatus(p.status),
            mode=PipelineMode(p.mode) if p.mode else None,
            created_at=p.created_at,
            updated_at=p.updated_at,
            scenes_count=len(p.scenes_data) if p.scenes_data else 0,
            progress=p.progress or 0.0,
            video_url=p.video_url,
            error=p.error,
        )
        for p in projects
    ]


# ── WebSocket for real-time updates ──────────────────────────


@router.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    """WebSocket endpoint for real-time pipeline progress updates."""
    await websocket.accept()

    if project_id not in _websocket_connections:
        _websocket_connections[project_id] = []
    _websocket_connections[project_id].append(websocket)

    # Send current state if available
    if project_id in _pipeline_progress:
        try:
            await websocket.send_text(
                json.dumps(_pipeline_progress[project_id])
            )
        except Exception:
            pass

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        conns = _websocket_connections.get(project_id, [])
        if websocket in conns:
            conns.remove(websocket)
