import uuid
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class SessionCreate(BaseModel):
    session_type: str = Field(..., max_length=50)
    duration_minutes: int = Field(..., gt=0)
    topic: str = Field(..., max_length=255)
    notes: str | None = None

    @field_validator("session_type")
    @classmethod
    def validate_session_type(cls, v: str) -> str:
        allowed = {"study", "coding", "leetcode"}
        if v not in allowed:
            raise ValueError(f"session_type must be one of {sorted(allowed)}")
        return v


class SessionRead(BaseModel):
    id: uuid.UUID
    session_type: str
    duration_minutes: int
    topic: str
    notes: str | None
    created_at: datetime

    class Config:
        from_attributes = True
