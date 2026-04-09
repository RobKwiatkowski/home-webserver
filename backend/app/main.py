from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from .database import Base, check_database_connection, engine, get_db
from .models import Note
from .schemas import NoteCreate, NoteResponse, NoteUpdate

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


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = note_update.title
    note.content = note_update.content

    db.commit()
    db.refresh(note)

    return note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    return {"message": f"Note {note_id} deleted"}