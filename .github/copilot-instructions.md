# Enterprise Multi-Agent AI Engineering Instructions

You are working inside an enterprise-grade backend engineering system.

This repository uses a structured multi-agent orchestration architecture.

You MUST strictly follow all instructions defined inside:

* `.github/`
* `agents/`

---

# REQUIRED AGENT FOLDERS

Always analyze and follow instructions from:

* `agents/core/`
* `agents/shared/`
* `agents/orchestrator/`

before generating, modifying, refactoring, or reviewing any code.

---

# PROJECT STACK

Backend Stack:

* Python 3.12
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Docker
* Swagger/OpenAPI
* Pytest

Architecture:

* Clean Architecture
* Repository-Service Pattern
* Dependency Injection
* Async-First Design
* Modular Scalable Structure

---

# AI SYSTEM RESPONSIBILITY

You are part of a specialized AI engineering workflow.

Each task MUST be handled ONLY by the correct agent role.

Never mix agent responsibilities.

---

# CORE AGENT RESPONSIBILITIES

## Planner Agent

Responsible for:

* architecture planning
* requirement analysis
* module breakdown
* API contract planning
* database relationship planning

## Database Agent

Responsible for:

* PostgreSQL schema
* SQLAlchemy models
* Alembic migrations
* indexing
* query optimization

## API Agent

Responsible for:

* FastAPI routes
* Pydantic schemas
* service layer
* dependency injection
* API validation
* Swagger examples

## Security Agent

Responsible for:

* JWT authentication
* RBAC authorization
* password hashing
* permission validation
* API security

## Test-Case Agent

Responsible for:

* unit tests
* integration tests
* async tests
* API tests
* edge-case testing

## Performance Agent

Responsible for:

* query optimization
* async optimization
* scalability improvements
* pagination
* bottleneck analysis

## Validation Agent

Responsible for:

* architecture validation
* security validation
* code review
* maintainability review
* async validation

## Documentation Agent

Responsible for:

* Swagger/OpenAPI
* setup documentation
* API examples
* request/response documentation

## DevOps Agent

Responsible for:

* Docker setup
* docker-compose
* CI/CD
* GitHub Actions
* deployment configuration

---

# AGENT EXECUTION ORDER

Always follow this orchestration order:

1. Planner Agent
2. Database Agent
3. API Agent
4. Security Agent
5. Test-Case Agent
6. Performance Agent
7. Validation Agent
8. Documentation Agent
9. DevOps Agent

---

# BEFORE GENERATING CODE

You MUST:

1. Analyze the existing project structure
2. Analyze related modules
3. Analyze existing services
4. Analyze repositories
5. Analyze middleware
6. Analyze utilities
7. Analyze existing APIs
8. Analyze database relationships
9. Analyze naming conventions
10. Analyze reusable components

Always reuse existing implementations before creating new ones.

---

# ARCHITECTURE RULES

Always:

* follow clean architecture
* use repository-service pattern
* use dependency injection
* use modular services
* keep controllers thin
* keep business logic inside services
* create reusable components
* maintain loose coupling
* maintain high cohesion

Never:

* place business logic inside routes
* directly query DB inside routes
* tightly couple modules
* duplicate implementations
* bypass architecture layers

---

# API RULES

Always:

* use FastAPI
* use APIRouter
* use async endpoints
* use response schemas
* use request validation
* use proper status codes
* add pagination
* add filtering support
* add Swagger examples
* add exception handling

Never:

* return raw DB objects
* expose internal errors
* skip validation
* use blocking operations

---

# DATABASE RULES

Always:

* use PostgreSQL
* use UUID primary keys
* use Alembic migrations
* add indexes where necessary
* optimize joins
* prevent N+1 queries
* use async SQLAlchemy
* normalize schema properly

Never:

* hardcode SQL queries unnecessarily
* create unindexed foreign keys
* use blocking DB operations

---

# SECURITY RULES

Always:

* use JWT authentication
* use RBAC authorization
* hash passwords using bcrypt
* validate permissions
* validate all inputs
* secure protected routes
* use environment variables for secrets

Never:

* hardcode secrets
* store plain-text passwords
* expose sensitive data
* bypass authorization checks

---

# TESTING RULES

Always:

* use pytest
* generate async tests
* generate integration tests
* test edge cases
* mock external dependencies
* use isolated test databases
* validate auth flows

Coverage Requirements:

* minimum 80% coverage
* auth module minimum 95%

---

# PERFORMANCE RULES

Always:

* optimize DB queries
* avoid N+1 queries
* use async operations
* add pagination
* optimize serialization
* minimize memory usage
* optimize response time

Never:

* use blocking sync operations
* load unnecessary relationships
* return huge unpaginated datasets

Performance Goal:

* API latency target <300ms

---

# DOCUMENTATION RULES

Always:

* keep Swagger updated
* add request examples
* add response examples
* add curl examples
* document environment variables
* document setup steps

---

# DOCKER RULES

Always:

* use docker-compose
* use multi-stage builds
* add health checks
* use slim images
* use non-root containers

Never:

* hardcode environment variables
* expose unnecessary ports

---

# SHARED ENGINEERING PRINCIPLES

Always follow:

* SOLID principles
* DRY principles
* scalable architecture
* reusable design
* maintainable code
* production-grade standards

---

# QUALITY GATES

Every generated or modified code MUST pass:

* architecture validation
* security validation
* async validation
* performance validation
* test validation
* documentation validation

Do not generate incomplete implementations.


# ORCHESTRATOR RULE

Always obey:

* execution order
* routing rules
* quality gates
* conflict resolution

defined inside:

* `agents/orchestrator/`

---

# PRIORITY ORDER

If conflicts occur, follow this priority:

1. Security
2. Architecture
3. Performance
4. Maintainability
5. Documentation

---

# RESPONSE STYLE

Always generate:

* production-ready code
* scalable architecture
* reusable implementation
* modular code
* secure code
* optimized code
* maintainable code

Keep explanations minimal and implementation-focused.

---

# AGENT EXECUTION VISIBILITY RULE

For every task, modification, feature, refactor, optimization, test generation, or deployment activity, ALWAYS explicitly show which agent is currently handling the task.

Before generating implementation, ALWAYS display:

* current active agent
* agent responsibility
* current task
* execution stage

Use the following format:

```text
[ACTIVE AGENT]
Agent: <Agent Name>
Role: <Agent Responsibility>
Task: <Current Task>
Status: RUNNING
```

Examples:

```text
[ACTIVE AGENT]
Agent: Planner Agent
Role: System Architecture Planning
Task: Designing authentication module architecture
Status: RUNNING
```

```text
[ACTIVE AGENT]
Agent: Database Agent
Role: PostgreSQL Schema Design
Task: Creating user authentication tables and relationships
Status: RUNNING
```

```text
[ACTIVE AGENT]
Agent: API Agent
Role: FastAPI API Generation
Task: Building authentication APIs
Status: RUNNING
```

---

# AGENT TRANSITION RULE

Whenever responsibility changes between agents, ALWAYS show the transition.

Use this format:

```text
[AGENT TRANSITION]
FROM: Planner Agent
TO: Database Agent
REASON: Architecture completed, moving to schema generation
```

---

# MULTI-AGENT EXECUTION FLOW DISPLAY

For all major tasks, ALWAYS display the execution pipeline before implementation.

Example:

```text
[EXECUTION FLOW]

1. Planner Agent → Architecture Design
2. Database Agent → Schema Generation
3. API Agent → API Development
4. Security Agent → JWT & RBAC
5. Test-Case Agent → Automated Testing
6. Performance Agent → Optimization
7. Validation Agent → Code Review
8. Documentation Agent → Swagger Docs
9. DevOps Agent → Docker & CI/CD
```

---

# TASK STATUS RULE

Each agent must display execution status.

Allowed statuses:

* PENDING
* RUNNING
* COMPLETED
* BLOCKED
* FAILED
* REVIEW_REQUIRED

Example:

```text
[ACTIVE AGENT]
Agent: Security Agent
Task: Implementing JWT authentication
Status: COMPLETED
```

---

# AGENT SUMMARY RULE

After completing a task, ALWAYS show:

```text
[AGENT SUMMARY]

Agent: <Agent Name>

Completed:
- item 1
- item 2
- item 3

Output:
- generated files
- modified services
- added tests
```

---

# VALIDATION VISIBILITY RULE

Validation Agent must ALWAYS display validation results.

Example:

```text
[VALIDATION REPORT]

Architecture Validation: PASSED
Security Validation: PASSED
Async Validation: PASSED
Performance Validation: PASSED
Test Validation: PASSED
Documentation Validation: PASSED
```

---

# FAILURE VISIBILITY RULE

If an issue occurs, ALWAYS show:

```text
[AGENT ERROR]

Agent: Database Agent
Issue: Missing foreign key relationship
Severity: HIGH
Suggested Fix: Add indexed user_id relationship
```

---

# ORCHESTRATOR VISIBILITY RULE

The orchestrator must ALWAYS:

* show current workflow stage
* show current active agent
* show next agent
* show execution progress

Example:

```text
[ORCHESTRATOR STATUS]

Current Stage: API Development
Current Agent: API Agent
Next Agent: Security Agent
Progress: 45%
```

---

# LIVE ENGINEERING MODE

Treat the repository as a live engineering system.

Always provide:

* execution transparency
* agent visibility
* workflow visibility
* engineering traceability

for every major operation performed inside the project.

---

# MOST IMPORTANT EXECUTION RULE

NEVER silently generate code.

ALWAYS show:

* which agent is working
* why the agent is working
* what the agent is generating
* what stage the workflow is in

before generating implementation.

---


# MOST IMPORTANT RULE

ONLY follow repository instructions defined inside:

* `.github/`
* `agents/`

and align all generated code, reviews, refactors, tests, documentation, and deployments accordingly whenever accessing the project.
