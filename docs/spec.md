# Home Webserver Specification

This document is the main project specification. Keep it updated when a change affects architecture, service behavior, deployment flow, or planned scope.

## Purpose

Home Webserver is a small self-hosted web application for learning and running a simple home server stack before Raspberry Pi deployment.

The project is intentionally compact. It focuses on:

- Docker-based service orchestration
- FastAPI backend development
- PostgreSQL persistence
- SQLAlchemy models with Alembic migrations
- Nginx as a reverse proxy and static frontend server
- basic note management
- basic file upload, listing, download, and deletion

## Current Architecture

The application is composed of three Docker services:

- `nginx`: public entry point, static frontend server, and reverse proxy for API requests
- `backend`: FastAPI application with SQLAlchemy database access
- `db`: PostgreSQL database with persistent volume storage

Request flow:

1. Browser connects to Nginx on port 80.
2. Nginx serves files from `frontend/html/`.
3. Requests under `/api/` are proxied to the backend service.
4. FastAPI handles API routes and uses SQLAlchemy sessions.
5. PostgreSQL stores notes and file metadata.
6. Uploaded file bytes are stored on disk in `/app/uploads`.

## Backend

Backend source lives in `backend/app/`.

Main responsibilities:

- expose health and diagnostic endpoints
- expose notes CRUD endpoints
- expose file metadata and file transfer endpoints
- validate request and response payloads with Pydantic schemas
- map database tables through SQLAlchemy models

Current route groups:

- `/notes`: create, list, read, update, and delete notes
- `/files`: upload, list, read metadata, download, and delete files
- `/health`: simple process health check
- `/db-check`: database connectivity check
- `/tables-check`: public-schema table listing for diagnostics

## Frontend

Frontend files live in `frontend/html/` and are served by Nginx.

The frontend currently provides:

- note creation and editing form
- note list with edit and delete actions
- manual note refresh button
- file upload control
- file list with download and delete actions

The frontend expects the backend to be available through Nginx under `/api/`.

## Database

PostgreSQL stores application metadata. The current schema includes:

- `notes`
  - `id`
  - `title`
  - `content`
  - `created_at`
  - `updated_at`
  - `category`
- `files`
  - `id`
  - `original_name`
  - `stored_name`
  - `content_type`
  - `size`
  - `created_at`

Application code must not rely on `Base.metadata.create_all()` for schema evolution. Schema changes must be represented as Alembic migrations.

## Migrations

Alembic files live in:

- `backend/alembic.ini`
- `backend/alembic/`
- `backend/alembic/versions/`

The backend container must include these files. The backend startup command applies pending migrations before starting Uvicorn.

Expected startup sequence:

1. Wait until PostgreSQL is healthy.
2. Run `python -m alembic -c /app/alembic.ini upgrade head`.
3. Start `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

When models change, create a matching migration and commit it with the code change.

## File Uploads

Uploaded file bytes are stored in `/app/uploads`, mounted from `backend/uploads/`.

Metadata is stored in PostgreSQL through the `files` table.

Current validation:

- maximum backend file size: 5 MB
- Nginx request body limit: 10 MB
- allowed content types:
  - `image/jpeg`
  - `image/png`
  - `application/pdf`
  - `text/plain`

Files in `backend/uploads/` are local runtime data and must not be committed.

## Deployment And Runtime

Normal local or Raspberry Pi startup:

```bash
docker compose up --build
```

Useful operational commands:

```bash
docker compose config --quiet
docker compose build backend
docker compose up -d
docker logs -f home-webserver-backend
```

PostgreSQL data is stored in the `postgres_data` Docker volume. Removing that volume deletes the database.

## Design Decisions

Current decisions:

- Use Docker Compose for the whole stack.
- Use Nginx as the public entry point.
- Keep static frontend files simple and framework-free for now.
- Keep uploaded file bytes on disk and store only metadata in PostgreSQL.
- Use Alembic as the only schema evolution mechanism.
- Run migrations during backend startup to keep deployments simple.
- Do not mount the whole backend directory into `/app` in the main Compose file, because that can hide files copied into the Docker image.

## Roadmap

Likely next steps:

- improve frontend text encoding and UI consistency
- add better user-facing upload and API error handling
- link uploaded files to notes
- add authentication before exposing the app outside a trusted home network
- add automated backend tests for notes, files, and migrations
- add backups for PostgreSQL data and uploaded files
- document Raspberry Pi deployment and restore procedures

## Agent Maintenance Rules

Agents changing this repository should:

- read this file before larger changes
- keep this file accurate when architecture, deployment, schema, or scope changes
- keep README focused on user-facing run instructions
- keep implementation details in code, migrations, and this specification aligned
