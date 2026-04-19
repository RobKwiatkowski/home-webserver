"""Pydantic schemas for request and response validation used by the FastAPI API."""

from datetime import datetime

from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str
    category: str | None = None


class NoteUpdate(BaseModel):
    title: str
    content: str
    category: str | None = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    category: str | None = None

    class Config:
        from_attributes = True

class FileResponse(BaseModel):
    id: int
    original_name: str
    stored_name: str
    content_type: str | None = None
    size: int
    created_at: datetime

    class Config:
        from_attributes = True