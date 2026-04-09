from fastapi import FastAPI

from .database import check_database_connection

app = FastAPI(title="Home Webserver API")


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