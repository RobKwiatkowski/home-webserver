# Home Webserver

This repository contains an educational project focused on building a simple home server step by step.

* repo contains a simple backend API behind Nginx
* runs locally with Docker Compose
* current phase is completed / in progress

## Current goal

The current phase focuses on preparing the basic application skeleton:

- a simple backend API,
- a reverse proxy,
- local containerized setup.

The goal is to create a minimal working system that will serve as a solid foundation for further development.

## Current phase architecture

[Browser] --> [Nginx / Reverse Proxy] --> [FastAPI Backend]

## Future direction

In later stages, the project may be extended with:

- a database,
- a simple user-facing frontend,
- CRUD functionality,
- deployment on Raspberry Pi,
- additional home server infrastructure components.

## Status

The project is currently in an early development phase.

## Planned tech stack

The planned technology stack includes:

- Python
- FastAPI
- Nginx
- Docker
- Docker Compose

## Run locally

```bash
docker compose up --build