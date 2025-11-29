---
name: sp-decompose
description: Decompose specifications into microservices without SpecPulse CLI
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-decompose Command

Decompose specifications into microservices without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-decompose [spec-id]           # Decompose current or specific spec
/sp-decompose [spec-id] --auto    # Auto-decompose with DDD patterns
```

## Implementation

When called with `/sp-decompose {{args}}`, I will:

### 1. Parse Arguments and Determine Target

**I will analyze the arguments:**
- If spec ID provided: Target that specific specification
- If no argument: Use current feature's specification
- Parse options like `--auto`, `--force`, `--validate`

### 2. Detect Current Feature Context

**I will identify the current working feature:**
- Check `.specpulse/memory/context.md` for active feature
- Look for most recent specification files
- Validate feature directory structure
- Extract feature ID and name

### 3. Load and Analyze Specification

**I will read and parse the specification:**
- Locate specification file in `.specpulse/specs/[feature]/`
- Read specification content and structure
- Analyze functional requirements and user stories
- Identify domain boundaries and business concepts
- Extract technical constraints and dependencies

### 4. Domain-Driven Design Analysis

**I will perform comprehensive DDD analysis:**

#### A. Domain Discovery
- Identify core domain concepts and entities
- Map business processes and workflows
- Discover bounded contexts and subdomains
- Analyze domain relationships and dependencies

#### B. Bounded Context Identification
For each potential service, I will analyze:
- **Core Domain**: Primary business value
- **Supporting Domains**: Essential supporting functions
- **Generic Domains**: Common utilities and infrastructure
- **Relationships**: Context mapping and integration patterns

#### C. Service Boundary Definition
Define microservice boundaries based on:
- Business capability alignment
- Data ownership and consistency
- Team autonomy and scaling needs
- Technical architecture considerations

### 5. Microservice Design

**I will design comprehensive microservice architecture:**

#### A. Service Catalog Creation
For each identified service:
- **Service Name**: Clear, business-oriented naming
- **Responsibility**: Primary business capabilities
- **Domain Model**: Core entities and relationships
- **API Contracts**: Service interfaces and data models
- **Data Ownership**: Primary data responsibilities

#### B. Service Interaction Design
- **Communication Patterns**: Synchronous vs asynchronous
- **Event Streams**: Domain events and pub/sub patterns
- **Data Consistency**: Eventual consistency strategies
- **Service Discovery**: Registration and lookup mechanisms

#### C. Technology Stack Recommendations
Based on service requirements:
- **Database Choices**: SQL vs NoSQL per service needs
- **Communication Protocols**: REST, gRPC, message queues
- **Deployment Strategy**: Containerization and orchestration
- **Monitoring**: Observability and health checks

### 6. Decomposition Output Generation

**I will create comprehensive decomposition documentation:**

#### A. Decomposition Directory Structure
```
.specpulse/specs/[feature]/decomposition/
├── overview.md                    # High-level architecture overview
├── services/                      # Individual service specifications
│   ├── user-service.md
│   ├── auth-service.md
│   ├── payment-service.md
│   └── notification-service.md
├── integration/                   # Service integration patterns
│   ├── api-gateway.md
│   ├── event-bus.md
│   └── data-synchronization.md
└── deployment/                    # Deployment and infrastructure
    ├── container-strategy.md
    ├── service-discovery.md
    └── monitoring.md
```

#### B. Service Specification Files
For each service, create detailed specification:
- **Service Overview**: Purpose and responsibilities
- **Domain Model**: Entities and relationships
- **API Specification**: REST/GraphQL endpoints
- **Database Schema**: Data model and relationships
- **Business Events**: Domain events and handling
- **Integration Points**: External dependencies
- **Deployment Requirements**: Infrastructure needs

### 7. Integration Strategy Development

**I will design comprehensive integration patterns:**

#### A. API Gateway Design
- **Routing Rules**: Request routing to services
- **Authentication**: Centralized auth and authorization
- **Rate Limiting**: Service protection policies
- **Request Transformation**: Protocol translation

#### B. Event-Driven Architecture
- **Domain Events**: Business event definitions
- **Event Bus**: Message routing and delivery
- **Event Sourcing**: Audit trail and state reconstruction
- **CQRS**: Command Query Responsibility Segregation

#### C. Data Management
- **Data Ownership**: Clear responsibility boundaries
- **Eventual Consistency**: Conflict resolution strategies
- **Data Synchronization**: Cross-service data sync
- **Backup and Recovery**: Service-specific strategies

### 8. Validation and Refinement

**I will validate the decomposition:**

#### A. Architectural Validation
- **Service Boundaries**: Validate separation of concerns
- **Dependency Analysis**: Check for circular dependencies
- **Scalability Assessment**: Growth and scaling considerations
- **Performance Impact**: Latency and throughput analysis

#### B. Business Validation
- **Capability Coverage**: All business requirements addressed
- **Process Alignment**: Business workflow support
- **User Experience**: Impact on end-user experience
- **Compliance**: Regulatory and security requirements

#### C. Technical Validation
- **Feasibility Assessment**: Implementation practicality
- **Complexity Analysis**: Manageable complexity levels
- **Team Alignment**: Organizational structure fit
- **Tool Support**: Available tools and frameworks

## Output Examples

### Decomposition Overview
```
🏗️  Microservice Decomposition: 001-user-authentication
================================================================

📊 Specification Analysis
   Business Requirements: 8
   User Stories: 6
   Acceptance Criteria: 24
   Complexity: High (Multiple business capabilities)

🔍 DDD Analysis Results
   Core Domain: User Management & Authentication
   Supporting Domains: Notifications, Profile Management
   Generic Domains: Logging, Monitoring, Configuration

📦 Recommended Microservices (4 services)

1) **User Service** (Core Domain)
   - User registration and profile management
   - User preferences and settings
   - User search and discovery
   - Primary Data: Users, Profiles, Preferences

2) **Authentication Service** (Core Domain)
   - Login/logout functionality
   - Password management and recovery
   - Token generation and validation
   - Multi-factor authentication
   - Primary Data: Credentials, Sessions, Tokens

3) **Authorization Service** (Supporting Domain)
   - Role and permission management
   - Access control policies
   - Resource authorization
   - Primary Data: Roles, Permissions, Policies

4) **Notification Service** (Supporting Domain)
   - Email notifications
   - SMS notifications
   - Push notifications
   - Notification preferences
   - Primary Data: Notifications, Templates, Preferences

🔗 Integration Strategy
   - API Gateway for external access
   - Event Bus for service communication
   - Shared database for cross-service queries
   - Centralized authentication service

✅ Decomposition complete with validation results
📁 Documentation created: .specpulse/specs/001-user-authentication/decomposition/
```

### Individual Service Specification
```
📋 Service Specification: Authentication Service
================================================================

**Service Name**: auth-service
**Domain**: Authentication (Core Domain)
**Primary Responsibilities**:
- User authentication and authorization
- Session management and token handling
- Password security and recovery
- Multi-factor authentication

**Domain Model**:
```
User (id, email, username)
│
├── Credentials (password_hash, salt, mfa_secret)
├── Session (id, token, expires_at, user_agent)
├── Token (access_token, refresh_token, type, expires_at)
└── AuthAttempt (timestamp, ip_address, success, method)
```

**API Endpoints**:
```
POST /auth/login          # User authentication
POST /auth/logout         # Session termination
POST /auth/refresh        # Token refresh
POST /auth/forgot-password # Password recovery
POST /auth/reset-password # Password reset
POST /auth/enable-mfa     # MFA setup
POST /auth/verify-mfa     # MFA verification
GET  /auth/profile        # User profile (auth required)
```

**Database Schema**:
- Users table (user_id, email, username, password_hash, created_at)
- Sessions table (session_id, user_id, token_hash, expires_at, user_agent)
- Tokens table (token_id, user_id, token_type, token_hash, expires_at)
- MFA_Secrets table (user_id, secret, backup_codes, enabled_at)

**Business Events**:
- UserLoggedIn (user_id, timestamp, ip_address)
- UserLoggedOut (user_id, timestamp)
- PasswordChanged (user_id, timestamp)
- MFAEnabled (user_id, timestamp)
- MFADisabled (user_id, timestamp)

**Integration Points**:
- User Service: User profile synchronization
- Notification Service: Security alerts and notifications
- API Gateway: Authentication middleware integration

**Deployment Requirements**:
- Container: Docker with health checks
- Database: PostgreSQL with connection pooling
- Cache: Redis for session storage
- Load Balancer: SSL termination
- Monitoring: Health endpoints and metrics

**Security Considerations**:
- Rate limiting on authentication endpoints
- Password strength validation
- Secure token generation (JWT)
- SQL injection protection
- HTTPS enforcement
- Audit logging for security events
```

## Advanced Features

### Auto-Decomposition Mode
Using `--auto` flag enables intelligent automatic decomposition:
- Pattern recognition for common service types
- Automated bounded context detection
- Template-based service specification generation
- Best practices application for integration patterns

### Validation Mode
Comprehensive validation of decomposition results:
- Architectural consistency checks
- Dependency cycle detection
- Performance impact assessment
- Security boundary validation

### Integration with Existing Workflow
- Generate service-specific task breakdowns
- Create implementation plans for each service
- Provide deployment and infrastructure guidance
- Support cross-platform service development

This `/sp-decompose` command provides **comprehensive microservice decomposition** without requiring any SpecPulse CLI installation, using Domain-Driven Design principles and LLM-enhanced architectural analysis.