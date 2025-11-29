---
name: sp-decompose
description: Decompose specifications into microservices without SpecPulse CLI
version: "1.0"
agent: specpulse-assistant
workflow_type: microservice_decomposition
---

# SpecPulse Microservice Decomposition Workflow

This workflow implements comprehensive CLI-independent microservice decomposition using Domain-Driven Design principles and LLM-enhanced architectural analysis.

## Agent Capabilities Required

- File operations: Read, Write, Edit, Bash, TodoWrite, Grep
- Directory traversal protection
- Atomic file operation handling
- Domain analysis and DDD pattern recognition
- Microservice architecture design
- Service boundary identification
- Integration strategy development

## Workflow Steps

### Step 1: Argument Parsing and Target Detection

**Parse input arguments:**
```yaml
inputs:
  spec_id: string
  options:
    auto: boolean
    force: boolean
    validate: boolean
```

**Target detection algorithm:**
```yaml
target_detection:
  current_feature:
    condition: No spec_id provided
    action: Use current feature's specification
    context:
      - Check .specpulse/memory/context.md for active feature
      - Look for most recent specification files
      - Validate feature directory structure
      - Extract feature ID and name

  specific_specification:
    condition: spec_id argument provided
    action: Target that specific specification
    validation:
      - Validate spec_id format (XXX or full name)
      - Locate specification file in feature directory
      - Confirm file accessibility and readability
```

### Step 2: Current Feature Context Detection

**Feature context algorithm:**
1. Check `.specpulse/memory/context.md` for active feature
2. Look for most recent specification files
3. Validate feature directory structure
4. Extract feature ID and name from directory naming convention
5. Set working context for subsequent operations

### Step 3: Specification Loading and Analysis

**Comprehensive specification analysis:**
```yaml
specification_loading:
  file_location:
    path: ".specpulse/specs/[feature]/"
    patterns:
      - spec-{spec_id}.md (if spec_id provided)
      - spec-*.md (most recent if no spec_id)
    validation: Confirm file exists and is readable

  content_analysis:
    structure_validation:
      - Read specification content and structure
      - Validate markdown formatting and organization
      - Check YAML frontmatter if present

    requirements_analysis:
      - Analyze functional requirements and user stories
      - Extract acceptance criteria and success metrics
      - Identify business capabilities and processes

    technical_analysis:
      - Identify technical constraints and dependencies
      - Extract architectural considerations
      - Analyze scalability and performance requirements
      - Detect integration points and external dependencies

  domain_identification:
    - Identify domain boundaries and business concepts
    - Map business processes and workflows
    - Discover bounded contexts and subdomains
    - Analyze domain relationships and dependencies
```

### Step 4: Domain-Driven Design Analysis

**Comprehensive DDD implementation:**
```yaml
ddd_analysis:
  domain_discovery:
    core_domain_identification:
      - Identify primary business value and competitive advantage
      - Map core business entities and relationships
      - Discover essential business processes
      - Analyze revenue-generating capabilities

    supporting_domain_identification:
      - Identify essential supporting functions
      - Map administrative and operational processes
      - Discover supporting business capabilities
      - Analyze dependency relationships with core domain

    generic_domain_identification:
      - Identify common utilities and infrastructure
      - Map technical and system capabilities
      - Discover shared services and platforms
      - Analyze commodity functionality

  bounded_context_identification:
    service_boundary_analysis:
      business_capability_alignment:
        - Group related capabilities into cohesive services
        - Ensure single responsibility principle
        - Define clear service ownership
        - Align with team autonomy principles

      data_ownership_considerations:
        - Identify primary data responsibilities
        - Analyze data consistency requirements
        - Define data access patterns
        - Consider data sovereignty and compliance

      scaling_architecture_impact:
        - Analyze scaling requirements per service
        - Consider team coordination overhead
        - Evaluate deployment independence
        - Assess technical complexity management

    context_mapping:
      relationship_identification:
        - Map service dependencies and interactions
        - Identify integration patterns
        - Define communication boundaries
        - Analyze data flow patterns

      integration_patterns:
        - Determine synchronous vs asynchronous communication
        - Identify event-driven opportunities
        - Define API contracts and interfaces
        - Plan service discovery and registration

  service_boundary_definition:
    microservice_architecture_principles:
      single_responsibility:
        - Ensure each service has one clear business purpose
        - Define focused responsibility boundaries
        - Avoid creating monolithic services
        - Maintain service autonomy

      high_cohesion:
        - Group related functionality together
        - Ensure internal consistency
        - Minimize cross-service dependencies
        - Maximize service independence

      loose_coupling:
        - Design service interfaces with minimal dependencies
        - Implement asynchronous communication patterns
        - Use event-driven architecture where appropriate
        - Define clear service contracts

      bounded_context_compliance:
      - Align with Domain-Driven Design principles
      - Implement Ubiquitous Language within services
      - Maintain context-specific models
      - Ensure domain model consistency
```

### Step 5: Microservice Design

**Comprehensive service architecture:**
```yaml
microservice_design:
  service_catalog_creation:
    service_specification_template:
      service_overview:
        - Service name and business purpose
        - Primary responsibilities and capabilities
        - Business value and competitive advantage
        - Success metrics and KPIs

      domain_model:
        - Core entities and value objects
        - Aggregates and aggregate roots
        - Domain services and repositories
        - Business events and event handlers

      api_contracts:
        - REST API endpoint specifications
        - GraphQL schema definitions if applicable
        - Request/response data models
        - API versioning strategy

      data_ownership:
        - Primary data responsibilities
        - Data consistency requirements
        - Data access patterns and permissions
        - Integration data synchronization

  service_interaction_design:
    communication_patterns:
      synchronous_communication:
        - REST API direct calls for immediate responses
        - gRPC for high-performance internal communication
        - GraphQL for flexible data querying
        - Request/response patterns for critical operations

      asynchronous_communication:
        - Event-driven architecture for loose coupling
        - Message queuing for reliable delivery
        - Event streaming for real-time updates
        - CQRS for read/write optimization

      service_discovery:
        - Service registry and registration
        - Health check and monitoring
        - Load balancing and failover
        - API gateway integration

    event_architecture:
      domain_events:
        - Business event identification and definition
        - Event payload design and structure
        - Event sourcing implementation strategies
        - Event versioning and evolution

      event_bus_implementation:
        - Message routing and delivery patterns
        - Event serialization and deserialization
        - Dead letter queue handling
        - Monitoring and observability

  technology_stack_recommendations:
    database_choices:
      relational_databases:
        criteria: ACID requirements, complex relationships
        options: PostgreSQL, MySQL, SQL Server
        recommendations: Based on consistency needs

      nosql_databases:
        criteria: Scalability, flexibility requirements
        options: MongoDB, Cassandra, DynamoDB
        recommendations: Based on access patterns

      document_databases:
        criteria: Schema flexibility, semi-structured data
        options: MongoDB, Couchbase, Elasticsearch
        recommendations: Based on query requirements

    communication_protocols:
      rest_apis:
        usage: External communication, web interfaces
        frameworks: Express.js, Spring Boot, FastAPI
        authentication: OAuth2, JWT, API keys

      graphql_apis:
        usage: Flexible data querying, frontend interfaces
        frameworks: Apollo Server, GraphQL Java, Hasura
        subscriptions: Real-time updates, websockets

      grpc:
        usage: High-performance internal communication
        frameworks: gRPC, grpc-go, grpc-java
        serialization: Protocol Buffers

    deployment_strategy:
      containerization:
        platform: Docker, Kubernetes
        orchestration: K8s, Docker Swarm
        registry: Docker Hub, AWS ECR, GCR

      orchestration:
        platform: Kubernetes, ECS, AKS
        service_mesh: Istio, Linkerd, Consul
        monitoring: Prometheus, Grafana, Jaeger

      monitoring:
        health_checks: readiness/liveness probes
        metrics: Prometheus format, custom dashboards
        tracing: OpenTelemetry, Zipkin, Jaeger
        logging: ELK stack, structured logging
```

### Step 6: Decomposition Output Generation

**Comprehensive output structure:**
```yaml
output_generation:
  directory_structure_creation:
    base_directory: ".specpulse/specs/[feature]/decomposition/"
    subdirectories:
      - services/ "Individual service specifications"
      - integration/ "Service integration patterns"
      - deployment/ "Deployment and infrastructure"

  service_specification_files:
    template_structure:
      service_overview_section:
        - Service name and business purpose
        - Primary responsibilities and capabilities
        - Business value and competitive advantage
        - Success metrics and KPIs

      domain_model_section:
        - Core entities and relationships
        - Aggregates and aggregate roots
        - Business rules and invariants
        - Domain services and repositories

      api_specification_section:
        - REST API endpoint documentation
        - Request/response data models
        - Authentication and authorization
        - Error handling and status codes

      database_schema_section:
        - Table definitions and relationships
        - Indexes and performance optimization
        - Data migration strategies
        - Backup and recovery procedures

      business_events_section:
        - Domain event definitions and purposes
        - Event payload structures
        - Event handlers and side effects
        - Event versioning strategies

      integration_points_section:
        - External dependencies and interfaces
        - API contracts and SLA requirements
        - Data synchronization patterns
        - Error handling and recovery

      deployment_requirements_section:
        - Container configuration and requirements
        - Resource needs and scaling strategies
        - Environment variables and configuration
        - Monitoring and observability needs

  integration_strategy_documentation:
    api_gateway_design:
      routing_rules: "Request routing to services"
      authentication: "Centralized auth and authorization"
      rate_limiting: "Service protection policies"
      request_transformation: "Protocol translation"
      monitoring: "Gateway health and performance"

    event_driven_architecture:
      domain_events: "Business event definitions"
      event_bus_implementation: "Message routing and delivery"
      event_sourcing: "Audit trail and state reconstruction"
      cqrs_implementation: "Command Query Responsibility Segregation"

    data_management:
      data_ownership: "Clear responsibility boundaries"
      eventual_consistency: "Conflict resolution strategies"
      data_synchronization: "Cross-service data sync"
      backup_recovery: "Service-specific strategies"

  deployment_documentation:
    container_strategy:
      image_optimization: "Layer optimization and caching"
      health_checks: "Readiness and liveness probes"
      resource_limits: "CPU, memory, storage constraints"
      security_hardening: "Container security best practices"

    service_discovery:
      registration_mechanism: "Service registry patterns"
      health_monitoring: "Service health detection"
      load_balancing: "Traffic distribution strategies"
      failover_handling: "High availability patterns"

    monitoring_setup:
      application_metrics: "Business and technical metrics"
      infrastructure_monitoring: "System health and performance"
      distributed_tracing: "Request flow across services"
      alerting_strategies: "Proactive issue detection"
```

### Step 7: Integration Strategy Development

**Comprehensive integration patterns:**
```yaml
integration_strategy:
  api_gateway_design:
    routing_configuration:
      request_routing:
        - Path-based routing to appropriate services
        - Header-based routing for version control
        - Load balancing across service instances
        - Circuit breaker patterns for fault tolerance

      authentication_integration:
        - Centralized authentication service
        - Token validation and refresh mechanisms
        - Role-based access control integration
        - Session management and SSO support

      rate_limiting_implementation:
        - Per-service rate limiting policies
        - Global rate limiting thresholds
        - Client-based rate limiting
        - Dynamic rate adjustment based on load

    event_driven_architecture:
      domain_events:
        event_identification:
          - Business event extraction from requirements
          - Event granularity and scope definition
          - Event naming conventions and standards

        event_design:
          payload_structure:
            - Consistent event format across services
            - Metadata inclusion for routing and filtering
            - Version information for compatibility
            - Timestamps and causality information

        event_handling:
          - Event handler implementation patterns
          - Idempotent event processing
          - Error handling and retry mechanisms
          - Side effect management and transaction boundaries

      event_bus_implementation:
        message_routing:
          - Topic-based routing patterns
          - Event filtering and transformation
          - Dynamic subscription management
          - Dead letter queue handling

        event_delivery:
          - At-least-once delivery guarantees
          - Event ordering and consistency
          - Retry mechanisms and backpressure handling
          - Monitoring and observability

    data_management:
      data_ownership_strategy:
        ownership_boundaries:
          - Clear data responsibility assignment
          - Service-specific data ownership patterns
          - Data sovereignty considerations
          - Compliance and regulatory requirements

      consistency_management:
        eventual_consistency:
          - Conflict detection and resolution strategies
          - Eventual consistency patterns implementation
          - Compensation transaction patterns
          - Consistency validation and monitoring

        data_synchronization:
          - Cross-service data sync patterns
          - Change detection and propagation
          - Conflict resolution mechanisms
          - Synchronization scheduling and optimization

      backup_recovery:
        service_specific_strategies:
          - Database backup procedures
          - Application state backup patterns
          - Disaster recovery planning
          - Testing recovery procedures

        cross_service_coordination:
          - Distributed transaction coordination
          - Multi-service backup strategies
          - Recovery point synchronization
          - Rollback coordination across services
```

### Step 8: Validation and Refinement

**Comprehensive validation framework:**
```yaml
validation_framework:
  architectural_validation:
    service_boundary_validation:
      separation_of_concerns:
        - Validate clear service responsibilities
        - Check for overlap or duplication
        - Ensure single responsibility principle compliance
        - Assess domain alignment

      dependency_analysis:
        - Dependency mapping and validation
        - Circular dependency detection
        - Critical path identification
        - Dependency optimization opportunities

      scalability_assessment:
        - Growth and scaling considerations
        - Performance impact analysis
        - Resource bottleneck identification
        - Scaling strategy validation

  business_validation:
    capability_coverage:
      requirement_coverage_validation:
        - All business requirements addressed
        - Functional completeness verification
        - Acceptance criteria coverage assessment

      process_alignment:
        - Business workflow support validation
        - User experience impact assessment
        - Operational efficiency analysis
        - Stakeholder requirement satisfaction

      compliance_validation:
        - Regulatory requirement compliance
        - Security and privacy considerations
        - Data protection compliance
        - Audit trail and logging requirements

  technical_validation:
    feasibility_assessment:
      implementation_practicality:
        - Technical approach feasibility
        - Resource requirement evaluation
        - Timeline achievability assessment
        - Risk factor identification

    complexity_analysis:
      manageable_complexity_levels:
        - Service interaction complexity assessment
        - Integration complexity validation
        - Operational complexity evaluation
        - Maintenance overhead assessment

      tool_support_evaluation:
        - Available tools and frameworks assessment
        - Technology stack compatibility
        - Development tool support analysis
        - Operational tool requirements

    team_alignment:
      organizational_structure_fit:
        - Team size and structure analysis
        - Skill requirements assessment
        - Training and development needs
        - Cross-functional coordination requirements
```

## Output Format

**Decomposition completion response:**
```yaml
decomposition_results:
  status: "success"
  specification_id: "001"
  specification_file: ".specpulse/specs/001-user-authentication/spec-001.md"
  complexity_assessment: "high"

  ddd_analysis:
    core_domain: "User Management & Authentication"
    supporting_domains: "Notifications, Profile Management"
    generic_domains: "Logging, Monitoring, Configuration"
    bounded_contexts_identified: 4

  microservices_design:
  recommended_services:
    - service_name: "user-service"
      domain: "Core Domain"
      responsibilities: "User registration, profile management, user search"
      data_ownership: "Users, Profiles, Preferences"

    - service_name: "authentication-service"
      domain: "Core Domain"
      responsibilities: "Login/logout, session management, MFA"
      data_ownership: "Credentials, Sessions, Tokens"

    - service_name: "authorization-service"
      domain: "Supporting Domain"
      responsibilities: "Role management, access control"
      data_ownership: "Roles, Permissions, Policies"

    - service_name: "notification-service"
      domain: "Supporting Domain"
      responsibilities: "Email, SMS, push notifications"
      data_ownership: "Notifications, Templates"

  integration_strategy:
    api_gateway: "Centralized routing and authentication"
    event_bus: "Service communication and coordination"
    data_management: "Eventual consistency and synchronization"

  deployment_strategy:
    containerization: "Docker with health checks"
    orchestration: "Kubernetes with service mesh"
    monitoring: "Comprehensive observability stack"

  validation_results:
    architectural_validation: "Passed"
    business_validation: "Passed"
    technical_validation: "Passed"
    overall_quality_score: "92%"

  next_steps:
    implementation_planning: "Ready for /sp-plan"
    task_breakdown: "Proceed with /sp-task"
    validation: "Run /sp-validate for quality assurance"
```

## Error Handling and Recovery

**Comprehensive error scenarios:**
```yaml
error_handling:
  specification_errors:
    specification_not_found:
      action: Guide user to create specification with /sp-spec
      recovery: Provide specification creation guidance

    insufficient_complexity:
      action: Recommend monolithic approach
      recovery: Explain complexity thresholds and alternatives

    corruption_detected:
      action: Report file corruption and suggest recovery
      recovery: Recommend backup restoration

  validation_errors:
    architectural_failures:
      action: Provide specific recommendations
      recovery: Detail remediation steps

    business_validation_failures:
      action: Identify gaps and improvements
      recovery: Suggest requirement clarification

    technical_validation_failures:
      action: Suggest alternative approaches
      recovery: Provide technical guidance

  operational_errors:
    permission_issues:
      action: Guide through directory creation
      recovery: Provide permission commands

    resource_constraints:
      action: Suggest resource optimization
      recovery: Provide alternative approaches
```

## Safety Constraints

- **Path validation**: Only operate within `.specpulse/` directory
- **Protected directories**: Never modify `templates/`, `specpulse/`, AI configs
- **Atomic operations**: Prevent partial updates and corruption
- **Rollback capability**: Restore original state on failures
- **Input validation**: Comprehensive sanitization of all inputs

## Integration Features

- **DDD Principles**: Complete Domain-Driven Design implementation
- **Pattern Recognition**: Automated microservice pattern detection
- **Technology Mapping**: Database, communication, and deployment recommendations
- **Integration Ready**: Complete service specifications for implementation
- **Validation Framework**: Multi-layer validation with specific recommendations
- **Template System**: Consistent structure and formatting across services