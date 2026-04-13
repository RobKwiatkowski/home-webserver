# Home Webserver

Educational home server project built step by step with Docker.

## Current stage

Phase 3: simple notes app with:
- FastAPI backend
- PostgreSQL database
- Nginx reverse proxy
- HTML/CSS/JavaScript frontend

## Architecture

Browser -> Nginx -> FastAPI -> PostgreSQL

## Features

- create notes
- list notes
- delete notes

## Run locally

```bash
docker compose up --build
```