from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from .database import Base, check_database_connection, engine, get_db
from .models import Note
from .schemas import NoteCreate, NoteResponse

app = FastAPI(title="Home Webserver API")

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/message")
def message() -> dict:
    return {"message": "Home Webserver API is running"}


@app.get("/db-check")
def db_check() -> dict:
    is_connected = check_database_connection()

    if is_connected:
        return {"database": "connected"}

    return {"database": "not connected"}

@app.get("/tables-check")
def tables_check() -> dict:
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return {"tables": tables}

@app.get("/tables-check")
def tables_check() -> dict:
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return {"tables": tables}

@app.post("/notes", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.get("/notes", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return notes