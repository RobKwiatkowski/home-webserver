from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine, SessionLocal
from app import models
from app.routers import notes

app = FastAPI(title="Home Webserver API")


app.include_router(notes.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/message")
def message():
    return {"message": "Hello from backend"}


@app.get("/db-check")
def db_check():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    finally:
        db.close()


@app.get("/tables-check")
def tables_check():
    db = SessionLocal()
    try:
        result = db.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
                """
            )
        )
        tables = [row[0] for row in result.fetchall()]
        return {"tables": tables}
    finally:
        db.close()