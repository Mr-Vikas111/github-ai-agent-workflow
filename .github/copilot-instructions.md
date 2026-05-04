# Enterprise Backend Engineering Instructions

You are working as part of an enterprise-grade backend engineering team.

Tech Stack:
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Swagger/OpenAPI
- Pytest

Core Engineering Principles:
- Follow clean architecture
- Follow SOLID principles
- Use repository-service pattern
- Use async-first design
- Build reusable modules
- Generate production-ready code
- Prioritize readability and maintainability

Coding Standards:
- Use type hints everywhere
- Add proper docstrings
- Use dependency injection
- Add structured logging
- Add centralized exception handling
- Avoid duplicated code
- Keep functions small and focused
- Use environment variables
- Never hardcode secrets

API Rules:
- Use RESTful APIs
- Use API versioning (/api/v1/)
- Add request validation
- Add response schemas
- Use proper HTTP status codes
- Add pagination for list APIs
- Add filtering support
- Add Swagger examples

Database Rules:
- Use PostgreSQL only
- Use UUID primary keys
- Add indexes where needed
- Use Alembic migrations
- Avoid N+1 queries
- Use async SQLAlchemy

Security Rules:
- JWT authentication mandatory
- RBAC authorization
- Password hashing using bcrypt
- Input validation mandatory
- Prevent SQL injection
- Prevent privilege escalation
- Validate permissions on every protected API

Testing Rules:
- Use pytest
- Generate async tests
- Add unit tests
- Add integration tests
- Add edge-case tests
- Minimum 80% test coverage

Performance Rules:
- Avoid blocking calls
- Use async database operations
- Optimize serialization
- Add pagination
- Optimize queries
- Target API latency <300ms

Docker Rules:
- Use docker-compose
- Use multi-stage builds
- Add health checks
- Use slim images
- Avoid root containers

Documentation Rules:
- Keep Swagger docs updated
- Add curl examples
- Add setup instructions
- Add request/response examples
