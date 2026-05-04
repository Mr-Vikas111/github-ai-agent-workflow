# FastAPI Todo Service

Async FastAPI todo CRUD APIs with JWT authentication, SQLAlchemy, Alembic, Docker, and pytest.

## Features

- Versioned REST API under `/api/v1`
- Async-first FastAPI and SQLAlchemy setup
- Repository and service layers
- PostgreSQL-ready configuration
- Alembic migration for the `todos` table
- JWT-based user authentication
- User-scoped protected todo APIs
- Explicit user-wise task CRUD endpoints
- Pagination and filtering on the list endpoint
- Soft deactivation support for todos
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

   Set a secure `JWT_SECRET_KEY` before running outside local development.

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

## Environment variables

| Variable | Required | Description | Example |
| --- | --- | --- | --- |
| `APP_NAME` | No | FastAPI application title shown in OpenAPI docs | `Todo Service` |
| `APP_ENV` | No | Runtime environment label | `development` |
| `APP_HOST` | No | Host interface for the API server | `0.0.0.0` |
| `APP_PORT` | No | API server port | `8000` |
| `DATABASE_URL` | Yes | Async PostgreSQL connection string used by the app | `postgresql+asyncpg://postgres:postgres@db:5432/todo_db` |
| `JWT_SECRET_KEY` | Yes | Secret used to sign JWT access tokens | `replace-with-a-secure-random-value` |
| `JWT_ALGORITHM` | No | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Access token lifetime in minutes | `60` |

## Local development

### Run locally without Docker

1. Start a PostgreSQL instance and set `DATABASE_URL`
2. Install dependencies and copy `.env.example` to `.env`
3. Apply migrations:

   ```bash
   alembic upgrade head
   ```

4. Start the API:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Run with Docker Compose

```bash
docker compose up --build
```

The Compose setup starts:

| Service | Purpose | Port |
| --- | --- | --- |
| `db` | PostgreSQL 16 database | `5432` |
| `api` | FastAPI application | `8000` |

Apply migrations after the services are up:

```bash
alembic upgrade head
```

## Database migrations

The project currently includes migrations for:

1. creating the `todos` table
2. adding `is_active` soft-deactivation support
3. creating the `users` table
4. associating todos with `owner_id`

Common commands:

```bash
alembic upgrade head
alembic downgrade -1
```

## Ownership and access model

- All todo and task endpoints require a valid JWT bearer token except registration and login
- Todos are owned by the authenticated user through `owner_id`
- `/api/v1/todos/*` and `/api/v1/users/me/tasks/*` only operate on records owned by the current user
- Accessing another user's resource returns `403`
- Login, registration, and profile endpoints are exposed under `/api/v1/auth/*`

## Health endpoint

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## API overview

### Authentication flow

1. Register a user with `POST /api/v1/auth/register`
2. Exchange credentials for a bearer token with `POST /api/v1/auth/login`
3. Send `Authorization: Bearer <access-token>` on all protected todo and task endpoints

### API reference

| Area | Endpoint | Purpose | Auth |
| --- | --- | --- | --- |
| Auth | `POST /api/v1/auth/register` | Register a new user | No |
| Auth | `POST /api/v1/auth/login` | Get JWT access token | No |
| Auth | `GET /api/v1/auth/me` | Get current authenticated user | Yes |
| Todos | `POST /api/v1/todos` | Create a todo for current user | Yes |
| Todos | `GET /api/v1/todos` | List current user's todos | Yes |
| Todos | `GET /api/v1/todos/{todo_id}` | Get one owned todo | Yes |
| Todos | `PATCH /api/v1/todos/{todo_id}` | Update one owned todo | Yes |
| Todos | `PATCH /api/v1/todos/{todo_id}/inactive` | Soft-deactivate one owned todo | Yes |
| Todos | `DELETE /api/v1/todos/{todo_id}` | Delete one owned todo | Yes |
| Tasks | `POST /api/v1/users/me/tasks` | Create a current-user task | Yes |
| Tasks | `GET /api/v1/users/me/tasks` | List current-user tasks | Yes |
| Tasks | `GET /api/v1/users/me/tasks/{task_id}` | Get one current-user task | Yes |
| Tasks | `PATCH /api/v1/users/me/tasks/{task_id}` | Update one current-user task | Yes |
| Tasks | `DELETE /api/v1/users/me/tasks/{task_id}` | Delete one current-user task | Yes |

### Common response codes

| Code | Meaning |
| --- | --- |
| `201` | Resource created |
| `200` | Request succeeded |
| `204` | Resource deleted |
| `401` | Missing, invalid, or expired bearer token |
| `403` | Authenticated user does not own the requested resource |
| `404` | Resource not found |
| `409` | Duplicate user registration |
| `422` | Request validation failed |

### Resource model notes

- **Todo endpoints** expose the direct protected todo CRUD surface
- **Task endpoints** provide the same ownership-safe operations under the explicit current-user namespace
- Responses include `owner_id`, `is_active`, timestamps, and completion state for client-side filtering

### Register a user

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "Example User",
    "password": "Str0ngPassw0rd!"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Str0ngPassw0rd!"
  }'
```

### Get current user

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <access-token>"
```

### Create a todo

```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ship FastAPI CRUD service",
    "description": "Finish the first production-ready todo API.",
    "is_completed": false
  }'
```

### Create a user task

```bash
curl -X POST http://localhost:8000/api/v1/users/me/tasks \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Finish assigned task",
    "description": "This task belongs to the authenticated user.",
    "is_completed": false
  }'
```

### List current user tasks

```bash
curl "http://localhost:8000/api/v1/users/me/tasks?limit=10&offset=0" \
  -H "Authorization: Bearer <access-token>"
```

### Update current user task

```bash
curl -X PATCH http://localhost:8000/api/v1/users/me/tasks/<task-id> \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated user task",
    "is_completed": true
  }'
```

### Delete current user task

```bash
curl -X DELETE http://localhost:8000/api/v1/users/me/tasks/<task-id> \
  -H "Authorization: Bearer <access-token>"
```

### List todos

```bash
curl "http://localhost:8000/api/v1/todos?limit=10&offset=0&search=ship" \
  -H "Authorization: Bearer <access-token>"
```

### Mark a todo inactive

```bash
curl -X PATCH http://localhost:8000/api/v1/todos/<todo-id>/inactive \
  -H "Authorization: Bearer <access-token>"
```

### List inactive todos

```bash
curl "http://localhost:8000/api/v1/todos?is_active=false&limit=10&offset=0" \
  -H "Authorization: Bearer <access-token>"
```

### Update a todo

```bash
curl -X PATCH http://localhost:8000/api/v1/todos/<todo-id> \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ship updated FastAPI CRUD service",
    "is_completed": true
  }'
```

### Delete a todo

```bash
curl -X DELETE http://localhost:8000/api/v1/todos/<todo-id> \
  -H "Authorization: Bearer <access-token>"
```

## Running checks

```bash
ruff check .
pytest
```
