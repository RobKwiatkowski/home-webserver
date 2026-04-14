# Home Webserver

Educational home server project built step by step with Docker and hosted on Raspberry Pi 3.

## Architecture

The project is a small containerized web application built for learning Docker, networking, backend basics, and service separation before deployment on Raspberry Pi.

### Main components

- **Nginx**
  - serves the frontend files
  - acts as the entry point to the application
  - can forward API traffic to the backend service

- **FastAPI backend**
  - exposes the REST API
  - handles note operations
  - connects to PostgreSQL using SQLAlchemy
  - includes health and database check endpoints

- **PostgreSQL**
  - stores application data
  - runs in a separate container
  - keeps data in a Docker volume

- **Alembic**
  - manages database schema changes
  - creates and applies migrations
  - is now the source of truth for schema evolution

### Current request flow

1. The browser connects to **Nginx**
2. Nginx serves the frontend
3. Frontend sends API requests to the **FastAPI backend**
4. Backend reads and writes data in **PostgreSQL**

### Database lifecycle

Database tables are no longer created automatically by the application at startup.

Instead, schema changes are managed with **Alembic migrations**, which makes the project easier to evolve, rebuild, and deploy in a controlled way.

Typical flow:

1. Update SQLAlchemy models
2. Generate a migration with Alembic
3. Apply the migration to the database
4. Start or restart the application

### Containers

The project currently uses three main services:

- `nginx`
- `backend`
- `db`

PostgreSQL data is stored in a persistent Docker volume, while the backend and frontend are developed as application code mounted or copied into containers depending on the environment. The database configuration is provided through environment variables. :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}


## Features

- create notes
- list notes
- delete notes

## Run locally

```bash
docker compose up --build
```

## Database migrations

Generate a new migration:
```bash
docker compose run --rm backend python -m alembic -c alembic.ini revision --autogenerate -m "change_name"
```

Apply migrations:
```bash
docker compose run --rm backend python -m alembic -c alembic.ini upgrade head
```

Rollback last migration:
```bash
docker compose run --rm backend python -m alembic -c alembic.ini downgrade -1
```

Start clean database:
```bash
docker compose down -v
docker compose up -d db
```