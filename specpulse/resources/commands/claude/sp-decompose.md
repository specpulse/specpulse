---
name: sp-decompose
description: Decompose large specifications into microservices, APIs, and smaller components
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-decompose Command

Decompose large specifications into smaller, manageable components with microservice boundaries, API contracts, and interface specifications.

## CRITICAL: File Edit Restrictions
- **NEVER EDIT**: templates/, scripts/, commands/, .claude/, .gemini/
- **ONLY EDIT**: specs/, plans/, tasks/, memory/
- Decomposition templates are COPIED to specs/XXX-feature/decomposition/, then edited there

## Usage
```
/sp-decompose [spec-id] [options]
```

Options: `--microservices`, `--apis`, `--interfaces`, `--all` (defaults to `--all`)

## Implementation

When called with `/sp-decompose $ARGUMENTS`, I will:

1. **Parse specification to decompose**:
   - If spec-id provided (e.g., `001` or `001-authentication`), use that specification
   - Otherwise, detect current feature from `memory/context.md` or git branch
   - Read the target specification file from `specs/XXX-feature/spec-YYY.md`
   - Analyze complexity and identify decomposition opportunities

2. **Analyze decomposition strategy**:
   - **Domain Analysis**: Identify bounded contexts and aggregate roots
   - **Responsibility Mapping**: Group related functionalities
   - **Data Flow Analysis**: Understand data dependencies
   - **Integration Points**: Identify communication needs between components
   - **Complexity Assessment**: Measure cognitive load and cyclomatic complexity

3. **Generate microservice boundaries**:
   - Apply Domain-Driven Design (DDD) principles
   - Create service definitions with clear responsibilities:
     ```yaml
     service: user-authentication
     responsibility: Handle user identity and access control
     bounded_context: Identity Management
     capabilities:
       - User registration
       - Authentication (OAuth2, JWT)
       - Session management
       - Password reset
     data_ownership:
       - users table
       - sessions table
       - tokens table
     ```
   - Define inter-service communication patterns
   - Specify data consistency requirements

4. **Create API contracts**:
   - Generate OpenAPI 3.0 specifications for each service
   - Define RESTful endpoints with clear semantics:
     ```yaml
     /api/v1/users:
       post:
         summary: Create new user
         requestBody:
           $ref: '#/components/schemas/UserCreateRequest'
         responses:
           201:
             $ref: '#/components/schemas/UserResponse'
     ```
   - Specify request/response schemas
   - Include authentication and authorization requirements
   - Define rate limiting and caching strategies

5. **Design interface specifications**:
   - Create abstract interfaces for each component:
     ```typescript
     interface IAuthenticationService {
       authenticate(credentials: Credentials): Promise<AuthToken>
       validateToken(token: string): Promise<TokenValidation>
       refreshToken(refreshToken: string): Promise<AuthToken>
       revokeToken(token: string): Promise<void>
     }
     ```
   - Define data transfer objects (DTOs)
   - Specify event contracts for event-driven communication
   - Create adapter patterns for external integrations

6. **Generate decomposition artifacts using templates**:
   - COPY templates from `templates/decomposition/` to `specs/XXX-feature/decomposition/`
   - Use template variables for AI processing in the COPIED files
   - **IMPORTANT**: Can EDIT files in specs/decomposition/ folder, but NEVER modify templates/, scripts/, or commands/ folders
   - Create structured output in `specs/XXX-feature/decomposition/`:
     - **`microservices.md`**: From template with service boundaries
     - **`api-contracts/`**: From OpenAPI template
     - **`interfaces/`**: From interface template
     - **`integration-map.md`**: Service communication
   - Update `memory/context.md` with decomposition status

7. **Validate decomposition**:
   - Check for circular dependencies
   - Verify data consistency boundaries
   - Ensure single responsibility principle
   - Validate against constitutional principles:
     - Simplicity (≤3 modules per service)
     - Clear boundaries
     - Testability

8. **Update workflow context**:
   - Add decomposition results to `memory/context.md`
   - Create feature-specific plan template with services
   - Prepare for `/sp-plan generate` with service context
   - Enable `/sp-task breakdown` per service
   - Run validation: `bash scripts/sp-pulse-decompose.sh validate`

## Examples

### Basic decomposition
```
User: /sp-decompose 001
```
I will analyze spec 001 and create a complete decomposition with microservices, APIs, and interfaces.

### Microservices only
```
User: /sp-decompose 002-ecommerce --microservices
```
I will focus on identifying microservice boundaries for the e-commerce specification.

### API contracts focus
```
User: /sp-decompose --apis
```
I will generate detailed API contracts for the current feature specification.

## Decomposition Principles

### Domain-Driven Design
- Bounded contexts define service boundaries
- Aggregates determine data ownership
- Ubiquitous language for clear communication

### SOLID Principles
- **S**ingle Responsibility: Each service has one reason to change
- **O**pen/Closed: Services extensible without modification
- **L**iskov Substitution: Interfaces are substitutable
- **I**nterface Segregation: Focused, specific interfaces
- **D**ependency Inversion: Depend on abstractions

### Communication Patterns
- **Synchronous**: REST APIs for request-response
- **Asynchronous**: Events for decoupled communication
- **Hybrid**: Command Query Responsibility Segregation (CQRS)

## Output Structure

```
specs/001-authentication/decomposition/
├── microservices.md          # Service definitions
├── api-contracts/
│   ├── auth-service.yaml     # OpenAPI spec
│   ├── user-service.yaml     # OpenAPI spec
│   └── session-service.yaml  # OpenAPI spec
├── interfaces/
│   ├── IAuthService.ts       # TypeScript interface
│   ├── IUserRepository.ts    # Repository pattern
│   └── IEventBus.ts         # Event bus interface
├── data-models/
│   ├── user.schema.json     # JSON Schema
│   ├── session.proto        # Protocol Buffers
│   └── events.avsc          # Avro schema
├── integration-map.md        # Service communication
└── migration-plan.md         # Decomposition strategy
```

## Constitutional Compliance

**Article I: Simplicity**
- Each service limited to 3 core modules
- Clear, focused responsibilities
- Minimal inter-service dependencies

**Article V: Single Responsibility**
- Services own their data
- Clear aggregate boundaries
- Independent deployment capability

**Article VIII: Framework Selection**
- Choose appropriate tech stack per service
- Leverage existing libraries
- Standardize communication protocols

## Integration with SpecPulse Workflow

1. **After `/sp-spec create`**: 
   - AI analyzes spec complexity
   - Suggests decomposition if >3 modules detected
   - User confirms with `/sp-decompose`

2. **During decomposition**:
   - AI reads spec from `specs/XXX-feature/spec-YYY.md`
   - Applies DDD analysis using spec content
   - Generates artifacts using templates
   - Updates memory/context.md

3. **Before `/sp-plan generate`**: 
   - Plan command detects decomposition
   - Uses service boundaries for architecture
   - Creates service-specific phases

4. **During `/sp-task breakdown`**: 
   - Tasks created per service
   - Inter-service dependencies mapped
   - Integration tasks generated

5. **With `/sp-validate`**: 
   - Validates service boundaries
   - Checks circular dependencies
   - Ensures constitutional compliance

## Error Handling

- Specification not found: Guide user to create spec first
- Circular dependencies detected: Suggest refactoring
- Too many services (>7): Recommend consolidation
- Missing bounded contexts: Apply DDD analysis