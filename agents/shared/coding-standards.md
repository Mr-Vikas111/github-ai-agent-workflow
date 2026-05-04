# Coding Standards

- Follow PEP8
- Use type hints
- Use meaningful variable names
- Keep functions focused
- Avoid deeply nested logic
- Add docstrings
- Prefer composition over inheritance
- Avoid global state

## Business Logic Design Patterns

Business logic must follow established design patterns. Apply the appropriate pattern based on the use case:

### Builder Pattern
- Use when constructing complex objects step-by-step
- Required for objects with many optional parameters or multi-step initialization
- Example: building query filters, request payloads, or complex domain objects

### Adapter Pattern
- Use when integrating third-party services or external APIs
- Wrap external interfaces to conform to internal contracts
- Example: adapting a payment gateway, email provider, or external data source

### Facade Pattern
- Use to simplify access to complex subsystems
- Expose a single unified interface over multiple services or components
- Example: a notification facade that coordinates email, SMS, and push channels

### Factory Pattern
- Use when object creation logic is complex or varies by condition
- Centralize instantiation and hide concrete implementations
- Example: creating different handler types based on event or role

### Singleton Pattern
- Use sparingly — only for shared stateless resources
- Acceptable for config loaders, logger instances, and DB engine setup
- Never use Singleton for mutable shared state

## Pattern Validation Rules
- Every service class must justify its design pattern choice in its docstring
- Patterns must not be mixed arbitrarily — follow separation of concerns
- Prefer Factory or Builder over direct instantiation in service and repository layers
- Avoid Singleton for business logic — reserve it for infrastructure concerns only
