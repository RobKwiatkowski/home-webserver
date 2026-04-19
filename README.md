# Home Webserver

A small home webserver project for learning Docker, FastAPI, PostgreSQL, Nginx, Alembic migrations, 
and basic file upload handling before deployment on Raspberry Pi.

## Architecture

This project is a small containerized web application built for learning backend development, Docker, 
networking, and service-based architecture before deploying to Raspberry Pi.

### Components

- **Nginx**
  - serves the frontend
  - acts as the entry point to the application
  - forwards API requests to the backend

- **FastAPI**
  - provides the backend API
  - handles notes and file operations
  - connects to PostgreSQL through SQLAlchemy

- **PostgreSQL**
  - stores application data
  - keeps notes and file metadata
  - runs as a separate container

- **Alembic**
  - manages database schema changes
  - keeps schema evolution versioned and reproducible

- **Local file storage**
  - stores uploaded files on disk
  - is separated from database metadata

### Request flow

1. The browser connects to **Nginx**
2. Nginx serves the frontend
3. The frontend sends API requests to **FastAPI**
4. FastAPI reads and writes metadata in **PostgreSQL**
5. Uploaded files are stored on disk in the uploads directory

### Database management

The database schema is managed through **Alembic migrations**.

This means schema changes are versioned and applied explicitly, instead of being created automatically when the application starts.

### Current scope

The application currently includes:

- a frontend served by Nginx
- a backend API built with FastAPI
- PostgreSQL for persistence
- a notes feature with CRUD operations
- a file upload feature with basic validation
- health and database check endpoints

### Why this setup

This architecture keeps the project simple while introducing the core building blocks of modern web applications:

- reverse proxy
- backend API
- relational database
- migrations
- local file storage
- containerized services

It also creates a solid base for future steps such as linking files to notes, background jobs, additional services, and Raspberry Pi deployment.

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

- create, list, update, and delete notes
- upload files through the web interface
- list uploaded files
- download uploaded files
- delete uploaded files
- store file metadata in PostgreSQL
- store uploaded files on disk
- validate file size and allowed file types
- manage database schema with Alembic migrations


## File uploads

Uploaded files are stored on disk, while file metadata is stored in PostgreSQL.

Current implementation includes:

- file upload from the frontend
- file listing
- file download
- file deletion
- basic file size validation
- basic content type validation

This is an MVP implementation intended for learning and further extension.

## Upload limits

The upload flow currently uses two layers of protection:

- **Nginx** limits the maximum request body size
- **FastAPI backend** validates the allowed file size and content type

This makes error handling clearer and protects the application from oversized uploads.

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