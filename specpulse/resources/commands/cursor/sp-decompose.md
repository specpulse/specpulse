---
name: /sp-decompose
id: sp-decompose
category: SpecPulse
description: Decompose specifications into microservices without SpecPulse CLI
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the decomposition outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use file operations (CLI-independent mode)
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments and determine target**:
   - If spec ID provided: Target that specific specification
   - If no argument: Use current feature's specification
   - Parse options like --auto, --force, --validate

2. **Detect current feature context**:
   - Check .specpulse/memory/context.md for active feature
   - Look for most recent specification files
   - Validate feature directory structure
   - Extract feature ID and name

3. **Load and analyze specification**:
   - Locate specification file in .specpulse/specs/[feature]/
   - Read specification content and structure
   - Analyze functional requirements and user stories
   - Identify domain boundaries and business concepts
   - Extract technical constraints and dependencies

4. **Domain-Driven Design analysis**:
   - **Step 1: Domain Discovery**
     - Identify core domain concepts and entities
     - Map business processes and workflows
     - Discover bounded contexts and subdomains
     - Analyze domain relationships and dependencies
   - **Step 2: Bounded Context Identification**
     - For each potential service, analyze Core Domain, Supporting Domains, Generic Domains
     - Define service boundaries based on business capability alignment
     - Map context relationships and integration patterns
   - **Step 3: Service Boundary Definition**
     - Define microservice boundaries based on business capability alignment
     - Analyze data ownership and consistency needs
     - Consider team autonomy and scaling requirements

5. **Microservice design**:
   - **Step 1: Service Catalog Creation**
     - For each service: Service Name, Responsibility, Domain Model, API Contracts, Data Ownership
   - **Step 2: Service Interaction Design**
     - Define Communication Patterns (Synchronous vs asynchronous)
     - Design Event Streams and domain events
     - Plan Service Discovery mechanisms
   - **Step 3: Technology Stack Recommendations**
     - Database Choices (SQL vs NoSQL per service needs)
     - Communication Protocols (REST, gRPC, message queues)
     - Deployment Strategy (containerization and orchestration)

6. **Decomposition output generation**:
   - **Step 1: Create Decomposition Directory Structure**
     - Create .specpulse/specs/[feature]/decomposition/ directory
     - Create subdirectories: services/, integration/, deployment/
   - **Step 2: Generate Service Specification Files**
     - For each service: Service Overview, Domain Model, API Specification, Database Schema
     - Include Business Events, Integration Points, Deployment Requirements
   - **Step 3: Create Integration Strategy Documentation**
     - API Gateway design, Event-driven architecture, Data management strategies

7. **Integration strategy development**:
   - **API Gateway Design**: Routing rules, authentication, rate limiting, request transformation
   - **Event-Driven Architecture**: Domain events, event bus, event sourcing, CQRS
   - **Data Management**: Data ownership, eventual consistency, synchronization strategies

8. **Validation and refinement**:
   - **Architectural Validation**: Service boundaries, dependency analysis, scalability assessment
   - **Business Validation**: Capability coverage, process alignment, user experience impact
   - **Technical Validation**: Feasibility assessment, complexity analysis, team alignment

9. **Validate structure and report comprehensive decomposition results**

**Usage**
```
/sp-decompose [spec-id]           # Decompose current or specific spec
/sp-decompose [spec-id] --auto    # Auto-decompose with DDD patterns
```

**Examples**

**Basic Decomposition:**
```
/sp-decompose
```

Output: Analyze current feature specification and create comprehensive microservice decomposition.

**Auto-Decomposition:**
```
/sp-decompose spec-001 --auto
```

Output: Automatic decomposition using DDD patterns with template-based service generation.

**Validation Mode:**
```
/sp-decompose --validate
```

Output: Validate existing decomposition with architectural consistency checks.

**Decomposition Features:**
- **Domain-Driven Design**: Bounded context identification and service boundary definition
- **Service Catalog**: Comprehensive service specifications with domain models
- **Integration Strategy**: API gateway, event bus, and data management patterns
- **Technology Recommendations**: Database, communication, and deployment strategies
- **Validation Framework**: Architectural, business, and technical validation

**Output Structure:**
```
.specpulse/specs/[feature]/decomposition/
├── overview.md                    # High-level architecture overview
├── services/                      # Individual service specifications
│   ├── user-service.md
│   ├── auth-service.md
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

**Advanced Features:**
- **Auto-Decomposition**: Pattern recognition and template-based generation
- **Validation Mode**: Comprehensive architectural and business validation
- **Integration Ready**: Service-specific task breakdown and implementation plans
- **Technology Mapping**: Database, communication, and deployment recommendations
- **DDD Principles**: Bounded contexts, domain events, and context mapping

**Error Handling**
- Specification not found: Suggest available specifications
- Insufficient complexity: Recommend monolithic approach
- Validation failures: Provide detailed feedback and corrections
- Permission issues: Guide through directory creation and file access

**Reference**
- Check memory/context.md for current feature context
- Use /sp-spec to create or refine specifications before decomposition
- Follow up with /sp-plan for service-specific implementation planning
- Use generated service specifications for task breakdown with /sp-task

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Uses LLM-safe file operations for comprehensive analysis
- Domain-Driven Design principles with automated pattern recognition
- Complete microservice architecture generation and validation
- Integration-ready output with implementation guidance
<!-- SPECPULSE:END -->