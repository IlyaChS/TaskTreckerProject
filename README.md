# Task Manager API

A RESTful Task Manager API built with FastAPI and SQLAlchemy.

## Technologies

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- Docker
- Docker Compose

## Features

- Create tasks
- Get all tasks
- Get task by ID
- Update tasks
- Partially update tasks
- Delete completed tasks
- Count tasks
- Input validation
- Database error handling
- Logging
- Automated tests
- Docker support

## Project Structure

```text
app/
├── api/
├── database/
├── models/
├── repositories/
├── schemas/
├── config.py
├── logging_config.py
└── main.py

tests/
└── test_tasks.py

Dockerfile
docker-compose.yml
requirements.txt
.env.example