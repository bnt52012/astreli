"""SQLAlchemy async database models."""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, String, Text, JSON
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.config import settings


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True, index=True)
    status = Column(String, default="pending")
    mode = Column(String, nullable=True)
    scenario = Column(Text, nullable=False)
    brand_name = Column(String, nullable=True)
    brand_config = Column(JSON, nullable=True)
    analysis_result = Column(JSON, nullable=True)
    scenes_data = Column(JSON, nullable=True)
    progress = Column(Float, default=0.0)
    video_url = Column(String, nullable=True)
    error = Column(Text, nullable=True)

    # File paths (JSON arrays)
    mannequin_images = Column(JSON, default=list)
    product_images = Column(JSON, default=list)
    decor_images = Column(JSON, default=list)
    logo_path = Column(String, nullable=True)
    music_path = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


engine = create_async_engine(settings.database_url, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
