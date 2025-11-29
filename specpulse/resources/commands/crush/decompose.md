---
name: SpecPulse: Decompose
description: Decompose specifications into microservices without SpecPulse CLI
category: SpecPulse
tags: [specpulse, decompose, microservices]
---

# SpecPulse Microservice Decomposition

Decompose specifications into microservices using Domain-Driven Design without requiring SpecPulse CLI installation.

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to decomposition analysis and documentation
- Only edit files in specs/ and memory/ directories
- Favor straightforward, minimal implementations first

**Steps**
Track these steps as TODOs and complete them one by one.
1. Parse arguments and determine target specification
2. Detect current feature context from memory/context.md
3. Load and analyze specification content
4. Perform Domain-Driven Design (DDD) analysis
5. Identify bounded contexts and service boundaries
6. Design microservice architecture and interactions
7. Create service specifications and integration patterns
8. Generate decomposition documentation structure
9. Validate architectural consistency and feasibility
10. Create comprehensive decomposition output

**Reference**
- Use DDD principles for bounded context identification
- Check specification files for domain analysis
- Refer to memory/context.md for feature context
- Follow microservice design best practices

**Usage**
Arguments should be provided as: `[spec-id] [--auto] [--validate]`

**Decomposition Process:**

### Phase 1: Domain Analysis and DDD
- **Domain Discovery**: Identify core domain concepts and entities
- **Business Process Mapping**: Map workflows and value chains
- **Bounded Context Identification**: Find natural service boundaries
- **Context Relationships**: Define integration patterns between contexts

### Phase 2: Microservice Design
- **Service Boundary Definition**: Define clear service responsibilities
- **API Contract Design**: Specify service interfaces and data models
- **Data Ownership**: Assign data responsibilities per service
- **Interaction Patterns**: Design communication and event patterns

### Phase 3: Integration Architecture
- **API Gateway Design**: Centralized access management
- **Event-Driven Architecture**: Domain events and message routing
- **Data Consistency**: Eventual consistency and synchronization
- **Service Discovery**: Registration and lookup mechanisms

**Decomposition Output Template:**
```markdown
# Microservice Decomposition: [Feature Name]
**Specification ID:** [spec-id]
**Decomposition Date:** [timestamp]

## 📊 Specification Analysis
### Business Requirements Overview
**Total Requirements:** [count]
**Functional Requirements:** [count]
**Non-Functional Requirements:** [count]
**User Stories:** [count]

### Complexity Assessment
**Domain Complexity:** [Low/Medium/High]
**Integration Complexity:** [Low/Medium/High]
**Technical Complexity:** [Low/Medium/High]
**Overall Complexity:** [Low/Medium/High]

## 🔍 Domain-Driven Design Analysis

### Domain Discovery
#### Core Domain Concepts
- **[Domain Concept 1]:** [description and importance]
- **[Domain Concept 2]:** [description and importance]

#### Business Processes
- **[Process 1]:** [workflow and value chain]
- **[Process 2]:** [workflow and value chain]

### Bounded Context Identification
#### [Service Name 1] (Core Domain)
**Responsibilities:**
- Primary business capability 1
- Primary business capability 2
- Core domain value and differentiation

**Domain Model:**
- Core entities and relationships
- Business invariants and rules
- Domain events and state changes

#### [Service Name 2] (Supporting Domain)
**Responsibilities:**
- Supporting capability 1
- Supporting capability 2
- Business process enablement

**Domain Model:**
- Supporting entities and relationships
- Integration with core domain
- Cross-cutting concerns

#### [Service Name 3] (Generic Domain)
**Responsibilities:**
- Common utility capability
- Infrastructure service
- Technical capability

## 🏗️ Microservice Architecture

### Service Catalog
#### 1) [Service Name]
**Domain:** [Core/Supporting/Generic]
**Primary Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

**Domain Model:**
```
[Entity Name] (id, name, properties)
├── [Sub-entity 1] (properties)
├── [Sub-entity 2] (properties)
└── [Value Object] (properties)
```

**API Endpoints:**
```
GET    /[resource]              # List resources
POST   /[resource]              # Create resource
GET    /[resource]/{id}         # Get specific resource
PUT    /[resource]/{id}         # Update resource
DELETE /[resource]/{id}         # Delete resource
```

**Database Schema:**
- Primary tables: [table1], [table2]
- Relationships: [relationship types]
- Indexing strategy: [indexes]

**Business Events:**
- [EventName] (data, timestamp)
- [EventName] (data, timestamp)

**Integration Points:**
- [Service Name]: [integration type and purpose]
- External System: [integration type and purpose]

#### 2) [Service Name]
[Similar detailed structure for each service]

### Service Interaction Design
#### Communication Patterns
- **Synchronous:** REST APIs for real-time requests
- **Asynchronous:** Event-driven for eventual consistency
- **Batch Processing:** Scheduled jobs for bulk operations

#### Event Bus Design
**Domain Events:**
- **UserRegistered:** User service → Notification service
- **PaymentProcessed:** Payment service → Order service
- **OrderShipped:** Order service → Notification service

**Event Routing:**
- Event topics and subscriptions
- Message ordering guarantees
- Dead letter queue handling

#### Data Consistency Strategy
- **Eventual Consistency:** Accept temporary inconsistencies
- **Compensating Transactions:** Undo operations for failures
- **Saga Pattern:** Long-running transaction management

## 🔗 Integration Strategy

### API Gateway Design
#### Routing Configuration
```
/user/*          → user-service
/auth/*          → auth-service
/payment/*       → payment-service
/notification/*  → notification-service
```

#### Cross-Cutting Concerns
- **Authentication:** JWT token validation
- **Authorization:** Role-based access control
- **Rate Limiting:** Per-service rate limits
- **Request Logging:** Centralized request tracking

### Event-Driven Architecture
#### Message Broker Configuration
- **Technology:** RabbitMQ/Apache Kafka
- **Topology:** Topic-based routing
- **Durability:** Persistent message storage
- **Scalability:** Partitioned topics

#### Event Sourcing
- **Event Store:** Immutable event log
- **Snapshot Strategy:** Periodic state snapshots
- **Replay Capability:** System state reconstruction

## 📦 Deployment Architecture

### Container Strategy
#### Service Containers
- **Runtime:** Docker containers
- **Base Images:** Minimal security-focused images
- **Multi-stage Builds:** Optimized image sizes
- **Health Checks:** Liveness and readiness probes

### Orchestration
#### Kubernetes Configuration
- **Service Discovery:** Kubernetes DNS
- **Load Balancing:** Service-level load balancing
- **Configuration:** ConfigMaps and Secrets
- **Monitoring:** Prometheus metrics collection

### Infrastructure Requirements
#### [Service Name]
- **CPU:** [requirements]
- **Memory:** [requirements]
- **Storage:** [requirements]
- **Network:** [bandwidth and latency requirements]

## 📊 Implementation Strategy

### Development Phases
#### Phase 1: Core Services (Weeks 1-4)
- User Service (authentication and profile management)
- Auth Service (security and authorization)
- Basic API Gateway setup

#### Phase 2: Business Services (Weeks 5-8)
- Business logic services
- Service integration
- Event bus implementation

#### Phase 3: Supporting Services (Weeks 9-12)
- Notification Service
- Monitoring and logging
- Performance optimization

### Migration Strategy
- **Strangler Fig Pattern:** Gradual replacement approach
- **Database Migration:** Phase-by-phase data migration
- **API Versioning:** Backward compatibility during transition
- **Feature Flags:** Controlled rollout of new functionality

## ✅ Validation Summary

### Architectural Validation
- ✅ Service boundaries are well-defined
- ✅ Dependencies are properly managed
- ✅ Scalability requirements addressed
- ✅ Performance impact assessed

### Business Validation
- ✅ All business requirements covered
- ✅ Business processes supported
- ✅ User experience maintained
- ✅ Compliance requirements met

### Technical Validation
- ✅ Implementation is feasible
- ✅ Complexity is manageable
- ✅ Team structure alignment confirmed
- ✅ Tool support availability verified

## 📁 Generated Documentation
```
.specpulse/specs/[feature]/decomposition/
├── overview.md                    # This file
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

**Decomposition Complete:** [success/failure]
**Next Steps:** Review service specifications and begin implementation planning
```

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Domain-Driven Design principles with automated pattern recognition
- Comprehensive microservice architecture generation
- Integration-ready output with implementation guidance

**Advanced Features:**
- **Auto-Decomposition**: Pattern recognition for service boundary detection
- **Validation Framework**: Architectural and business consistency checks
- **Integration Strategy**: Complete API gateway and event bus design
- **Deployment Planning**: Container strategy and infrastructure requirements
<!-- SPECPULSE:END -->