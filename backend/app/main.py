from fastapi import FastAPI

app = FastAPI(title="Home Webserver API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/message")
def message() -> dict:
    return {"message": "Home Webserver API is running"}