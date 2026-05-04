# FastAPI Todo Service

Async FastAPI todo CRUD APIs with SQLAlchemy, Alembic, Docker, and pytest.

## Features

- Versioned REST API under `/api/v1`
- Async-first FastAPI and SQLAlchemy setup
- Repository and service layers
- PostgreSQL-ready configuration
- Alembic migration for the `todos` table
- Pagination and filtering on the list endpoint
- OpenAPI request and response examples

## Quick start

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy environment settings:

   ```bash
   cp .env.example .env
   ```

3. Run PostgreSQL and the API:

   ```bash
   docker compose up --build
   ```

4. Apply the database migration:

   ```bash
   alembic upgrade head
   ```

5. Open the docs:

   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API overview

### Create a todo

```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ship FastAPI CRUD service",
    "description": "Finish the first production-ready todo API.",
    "is_completed": false
  }'
```

### List todos

```bash
curl "http://localhost:8000/api/v1/todos?limit=10&offset=0&search=ship"
```

### Update a todo

```bash
curl -X PATCH http://localhost:8000/api/v1/todos/<todo-id> \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ship updated FastAPI CRUD service",
    "is_completed": true
  }'
```

### Delete a todo

```bash
curl -X DELETE http://localhost:8000/api/v1/todos/<todo-id>
```

## Running checks

```bash
ruff check .
pytest
```
