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