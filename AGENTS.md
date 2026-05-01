# AGENTS.md

Guidance for coding agents working in this repository.

## Project Context

This is a Docker-based home webserver project with:

- FastAPI backend in `backend/`
- PostgreSQL database
- Alembic migrations in `backend/alembic/`
- Nginx-served frontend in `frontend/html/`
- Docker Compose orchestration in `docker-compose.yaml`

Before making larger changes, read the project specification:

- `docs/spec.md` for architecture, service boundaries, database rules, deployment flow, decisions, and roadmap

If a change affects architecture, long-term design, deployment, schema, or planned scope, update `docs/spec.md` together with the code change.

## Development Rules

- Prefer small, focused changes that match the existing project structure.
- Keep database schema changes in Alembic migrations. Do not rely on `Base.metadata.create_all()` for schema evolution.
- Keep backend API behavior and frontend expectations aligned when changing endpoints or response shapes.
- Do not commit local uploaded files from `backend/uploads/`.
- Keep secrets and local environment values out of Git. Use `.env.example` for documented configuration.

## Docker And Database

- The backend image must include `backend/alembic.ini` and `backend/alembic/`.
- The backend startup path should run pending Alembic migrations before starting Uvicorn.
- If the database schema differs from SQLAlchemy models, create or fix an Alembic migration instead of patching the live database manually.

## Verification

When possible, verify changes with:

- `docker compose config --quiet`
- `docker compose build backend`
- `docker compose up -d`
- API or browser checks for affected flows

If Docker is unavailable, state that clearly and still perform static checks where possible.
