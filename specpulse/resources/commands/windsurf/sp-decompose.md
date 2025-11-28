---
description: Decompose large specifications into microservices, APIs, and smaller components with DDD principles
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the specification decomposition outcome
- Only edit files in specs/ directory - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse decompose <spec-id>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/
- **EDITABLE ONLY**: specs/ (specifically decomposition subdirectories)

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse specification to decompose**:
   - If spec-id provided (e.g., `001` or `001-authentication`), use that specification
   - Otherwise, detect current feature from `memory/context.md` or git branch
   - Read the target specification file from `specs/XXX-feature/spec-YYY.md`
   - Analyze complexity and identify decomposition opportunities

2. **Try CLI First**:
   ```bash
   specpulse decompose <spec-id> --microservices --apis --interfaces
   ```
   If CLI succeeds, STOP HERE.

3. **Analyze decomposition strategy** using File Operations:
   - **Domain Analysis**: Identify bounded contexts and aggregate roots
   - **Responsibility Mapping**: Group related functionalities
   - **Data Flow Analysis**: Understand data dependencies
   - **Integration Points**: Identify communication needs between components
   - **Complexity Assessment**: Measure cognitive load and cyclomatic complexity

4. **Generate microservice boundaries**:
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

5. **Create API contracts**:
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

6. **Design interface specifications**:
   - Create abstract interfaces for each component:
     ```typescript
     interface IAuthenticationService {
       authenticate(credentials: Credentials): Promise<AuthToken>
       validateToken(token: string): Promise<TokenValidation>
       refreshToken(refreshToken: string): Promise<AuthToken>
       revokeToken(token: string): Promise<void>
     }
     ```
   - Define method signatures and contracts
   - Specify error handling patterns
   - Document integration requirements

7. **Create decomposition directory structure**:
   ```
   specs/XXX-feature/decomposition/
   ├── microservices.md
   ├── api-contracts/
   │   ├── auth-service.yaml
   │   ├── user-service.yaml
   │   └── shared-types.yaml
   └── interfaces/
       ├── IAuthService.ts
       ├── IUserService.ts
       └── IEmailService.ts
   ```

8. **Write decomposition artifacts**:
   - **microservices.md**: Service definitions and boundaries
   - **api-contracts/**: OpenAPI specifications for each service
   - **interfaces/**: Abstract interface definitions
   - **integration-patterns.md**: Service communication patterns

9. **Validate decomposition completeness**:
   - Verify all requirements are covered by services
   - Check for missing integration points
   - Validate data ownership conflicts
   - Ensure consistency across artifacts

**Usage**
```
/sp-decompose [spec-id] [options]
```

Options: `--microservices`, `--apis`, `--interfaces`, `--all` (defaults to `--all`)

**Decomposition Output Structure**

**Directory Creation:**
```
specs/001-user-authentication/decomposition/
├── microservices.md              # Service definitions and boundaries
├── api-contracts/                 # OpenAPI specifications
│   ├── auth-service.yaml         # Authentication service API
│   ├── user-service.yaml         # User management API
│   └── shared-types.yaml         # Shared data models
├── interfaces/                   # Abstract interface definitions
│   ├── IAuthService.ts          # Authentication service interface
│   ├── IUserService.ts          # User service interface
│   └── IEmailService.ts         # Email service interface
├── integration-patterns.md       # Service communication patterns
└── deployment-order.md           # Service deployment sequence
```

**Examples**

**Decompose current feature:**
```
/sp-decompose
```
Output:
```
## Decomposing: 001-user-authentication

### Analysis Results
- **Specification Complexity**: High (23 requirements, 12 user stories)
- **Recommended Decomposition**: Microservices architecture
- **Identified Services**: 3 services

### Creating Service Boundaries
1. **Authentication Service** (auth-service)
   - Responsibility: Identity verification and token management
   - Bounded Context: Security & Authentication
   - APIs: /auth/* endpoints

2. **User Service** (user-service)
   - Responsibility: User profile and preferences management
   - Bounded Context: User Management
   - APIs: /users/* endpoints

3. **Notification Service** (notification-service)
   - Responsibility: Email and SMS notifications
   - Bounded Context: Communication
   - APIs: /notifications/* endpoints

### Generated Artifacts
✓ microservices.md
✓ api-contracts/auth-service.yaml
✓ api-contracts/user-service.yaml
✓ api-contracts/notification-service.yaml
✓ interfaces/IAuthService.ts
✓ interfaces/IUserService.ts
✓ interfaces/INotificationService.ts

### Next Steps
1. Review service boundaries with team
2. Create implementation plans: /sp-plan
3. Generate tasks: /sp-task
```

**Decompose specific specification:**
```
/sp-decompose 002 --microservices
```
Output: Decomposes spec 002 into microservices only.

**Decompose with API focus:**
```
/sp-decompose payment-system --apis
```
Output: Focuses only on API contract generation.

**Microservice Definition Template**
```yaml
# microservices.md

## Service: user-authentication

### Responsibility
Handle user identity and access control including registration, authentication, and session management.

### Bounded Context
Identity Management - Core domain for user security and access patterns.

### Capabilities
- **User Registration**: New user account creation with validation
- **Authentication**: OAuth2, JWT, and traditional password authentication
- **Session Management**: Active session tracking and lifecycle
- **Password Reset**: Secure password recovery workflows
- **Multi-factor Authentication**: 2FA and device verification

### Data Ownership
**Primary Tables:**
- `users` - User profiles and credentials
- `sessions` - Active user sessions
- `tokens` - JWT refresh tokens and OAuth tokens
- `audit_logs` - Security audit trail

**Integration Dependencies:**
- **User Service**: Read user profile data
- **Notification Service**: Send authentication emails/SMS

### Service Metrics
- **Load Factor**: High (every request requires auth)
- **Data Volume**: Medium (user data grows linearly)
- **Criticality**: Maximum (security-critical component)
- **Availability Target**: 99.9% uptime
```

**API Contract Template**
```yaml
# api-contracts/auth-service.yaml

openapi: 3.0.0
info:
  title: Authentication Service API
  version: 1.0.0
  description: User authentication and authorization endpoints

paths:
  /api/v1/auth/login:
    post:
      summary: Authenticate user credentials
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
      responses:
        '200':
          description: Successful authentication
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '401':
          description: Invalid credentials
```

**Interface Template**
```typescript
// interfaces/IAuthService.ts

export interface IAuthService {
  // Core authentication
  authenticate(credentials: Credentials): Promise<AuthResult>;
  validateToken(token: string): Promise<TokenValidation>;
  refreshToken(refreshToken: string): Promise<AuthResult>;

  // User management
  register(userData: UserRegistrationData): Promise<User>;
  updateProfile(userId: string, updates: UserProfileUpdate): Promise<User>;

  // Session management
  createSession(userId: string, metadata?: SessionMetadata): Promise<Session>;
  invalidateSession(sessionId: string): Promise<void>;
  invalidateUserSessions(userId: string): Promise<void>;

  // Security
  enforcePasswordPolicy(password: string): PasswordValidationResult;
  detectSuspiciousActivity(userId: string, activity: UserActivity): SecurityRisk;
}
```

**CLI Integration**

**Try CLI First:**
```bash
specpulse decompose <spec-id>
specpulse decompose <spec-id> --microservices
specpulse decompose <spec-id> --apis
specpulse decompose <spec-id> --interfaces
specpulse decompose <spec-id> --all
```

**Fallback to Manual Decomposition if CLI Fails:**
1. Read specification file manually
2. Analyze complexity and domain boundaries
3. Generate service definitions
4. Create API contracts and interfaces
5. Validate decomposition completeness

**Decomposition Validation**

**Completeness Checks:**
- All requirements mapped to services
- No service responsibility conflicts
- Clear data ownership boundaries
- Comprehensive API coverage
- Complete interface definitions

**Quality Gates:**
- Service cohesion: High within, low between
- Interface stability: Stable contracts
- Integration simplicity: Clear communication patterns
- Deployment independence: Service can be deployed separately

**Reference**
- Use `specpulse decompose --help` if you need additional CLI options
- Check `memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- After decomposition, use `/sp-plan` to create service-specific implementation plans
- Use `/sp-task` to generate tasks for each service
<!-- SPECPULSE:END -->