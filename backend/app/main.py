from fastapi import FastAPI
from sqlalchemy import inspect

from .database import Base, check_database_connection, engine
from .routers.notes import router as notes_router

app = FastAPI(title="Home Webserver API")

Base.metadata.create_all(bind=engine)

app.include_router(notes_router)


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