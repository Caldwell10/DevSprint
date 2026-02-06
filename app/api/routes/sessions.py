"""Session routes: create and list sessions."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db_session
from app.models.session import Session
from app.schemas.session import SessionCreate, SessionRead

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
async def create_session(
    payload: SessionCreate, db: AsyncSession = Depends(get_db_session)
) -> SessionRead:
    new_session = Session(
        session_type=payload.session_type,
        duration_minutes=payload.duration_minutes,
        topic=payload.topic,
        notes=payload.notes,
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return SessionRead.model_validate(new_session)


@router.get("/", response_model=List[SessionRead])
async def list_sessions(db: AsyncSession = Depends(get_db_session)) -> List[SessionRead]:
    result = await db.execute(select(Session).order_by(Session.created_at.desc()))
    rows = result.scalars().all()
    return [SessionRead.model_validate(row) for row in rows]
