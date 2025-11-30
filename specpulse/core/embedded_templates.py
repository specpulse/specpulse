"""
Embedded Templates - Default template content for SpecPulse

This module contains all embedded template strings that were previously
inline in specpulse.py. Separating them improves maintainability and
reduces the main orchestrator's complexity.

These templates are used as fallbacks when resource templates are not found.
"""

from pathlib import Path
from typing import Dict


# ============================================================================
# CORE TEMPLATES
# ============================================================================

SPEC_TEMPLATE = """# Specification: [DESCRIPTION]

<!-- FEATURE_DIR: {{feature_directory}} -->
<!-- FEATURE_ID: {{feature_id}} -->
<!-- SPEC_NUMBER: {{spec_number}} -->
<!-- STATUS: pending -->
<!-- CREATED: {{current_timestamp}} -->

## Description

[Clear description of the feature to be implemented]

## Requirements

### Functional Requirements

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Non-Functional Requirements

- **Performance**: [Performance requirements]
- **Security**: [Security requirements]
- **Scalability**: [Scalability requirements]

## Acceptance Criteria

- [ ] Given [precondition], when [action], then [expected outcome]
- [ ] [Second acceptance criteria]
- [ ] [Third acceptance criteria]

## Technical Considerations

### Dependencies

- **External APIs**: [List any external API dependencies]
- **Database Changes**: [Any database schema changes required]
- **Third-party Libraries**: [New libraries needed]

### Implementation Notes

[Technical notes and considerations for implementation]

## Testing Strategy

- **Unit Tests**: [What needs unit testing]
- **Integration Tests**: [What needs integration testing]
- **End-to-End Tests**: [What needs E2E testing]

## Definition of Done

- [ ] All requirements implemented
- [ ] All acceptance criteria met
- [ ] Code reviewed and approved
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Deployed to production

## Additional Notes

[Any additional context, constraints, or notes]
"""

PLAN_TEMPLATE = """# Implementation Plan: [DESCRIPTION]

<!-- FEATURE_DIR: {{feature_directory}} -->
<!-- FEATURE_ID: {{feature_id}} -->
<!-- PLAN_NUMBER: {{plan_number}} -->
<!-- STATUS: pending -->
<!-- CREATED: {{current_timestamp}} -->

## Specification Reference

- **Spec ID**: SPEC-{{feature_id}}
- **Spec Version**: 1.0
- **Plan Version**: 1.0
- **Generated**: {{current_date}}

## Architecture Overview

### High-Level Design

[High-level description of the solution approach]

### Technical Stack

- **Frontend**: [Technologies and frameworks]
- **Backend**: [Technologies and frameworks]
- **Database**: [Database technologies]
- **Infrastructure**: [Infrastructure components]

## Implementation Phases

### Phase 1: Foundation [Priority: HIGH]

**Timeline**: [X days/weeks]
**Dependencies**: None

#### Tasks

1. [ ] Set up project structure
2. [ ] Initialize database schema
3. [ ] Create basic API endpoints
4. [ ] Set up authentication framework

#### Deliverables

- [ ] Project structure created
- [ ] Database schema implemented
- [ ] Basic API endpoints functional
- [ ] Authentication system in place

### Phase 2: Core Features [Priority: HIGH]

**Timeline**: [X days/weeks]
**Dependencies**: Phase 1 complete

#### Tasks

1. [ ] Implement main business logic
2. [ ] Create user interface components
3. [ ] Integrate with external services
4. [ ] Implement data validation

#### Deliverables

- [ ] Core functionality working
- [ ] User interface complete
- [ ] External integrations functional
- [ ] Data validation implemented

### Phase 3: Enhancement & Polish [Priority: MEDIUM]

**Timeline**: [X days/weeks]
**Dependencies**: Phase 2 complete

#### Tasks

1. [ ] Add advanced features
2. [ ] Optimize performance
3. [ ] Improve user experience
4. [ ] Add comprehensive error handling

#### Deliverables

- [ ] Advanced features implemented
- [ ] Performance optimized
- [ ] UX improvements complete
- [ ] Error handling robust

### Phase 4: Testing & Deployment [Priority: MEDIUM]

**Timeline**: [X days/weeks]
**Dependencies**: Phase 3 complete

#### Tasks

1. [ ] Write comprehensive tests
2. [ ] Performance testing
3. [ ] Security audit
4. [ ] Deployment preparation

#### Deliverables

- [ ] Test coverage > 90%
- [ ] Performance benchmarks met
- [ ] Security audit passed
- [ ] Deployment ready

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High/Medium/Low | High/Medium/Low | [Mitigation strategy] |
| [Risk 2] | High/Medium/Low | High/Medium/Low | [Mitigation strategy] |

### Dependencies

| Dependency | Risk | Contingency |
|------------|------|-------------|
| [External service/API] | High/Medium/Low | [Backup plan] |
| [Third-party library] | High/Medium/Low | [Alternative solution] |

## Resource Requirements

### Development Team

- **Backend Developer**: [Number] developers
- **Frontend Developer**: [Number] developers
- **DevOps Engineer**: [Number] engineers
- **QA Engineer**: [Number] engineers

### Infrastructure

- **Development Environment**: [Required resources]
- **Testing Environment**: [Required resources]
- **Production Environment**: [Required resources]

## Success Metrics

- **Performance**: [Performance benchmarks]
- **User Satisfaction**: [Target metrics]
- **Business Impact**: [Expected business outcomes]
- **Technical Debt**: [Acceptable levels]

## Rollout Plan

### Phase Rollout Strategy

1. **Alpha**: Internal testing with core team
2. **Beta**: Limited user group testing
3. **GA**: General availability release

### Monitoring & Observability

- **Application Metrics**: [Key metrics to monitor]
- **Business Metrics**: [Business KPIs to track]
- **Error Monitoring**: [Error tracking setup]
- **Performance Monitoring**: [Performance tracking setup]

## Definition of Done

- [ ] All implementation phases complete
- [ ] All acceptance criteria met
- [ ] Comprehensive testing completed
- [ ] Documentation complete
- [ ] Team training conducted
- [ ] Production deployment successful

## Additional Notes

[Any additional context, constraints, or considerations]
"""

TASK_TEMPLATE = """# Task Breakdown: [FEATURE_NAME]

<!-- FEATURE_DIR: {{feature_directory}} -->
<!-- FEATURE_ID: {{feature_id}} -->
<!-- TASK_LIST_ID: {{task_list_id}} -->
<!-- STATUS: pending -->
<!-- CREATED: {{current_timestamp}} -->
<!-- LAST_UPDATED: {{current_timestamp}} -->

## Progress Overview

- **Total Tasks**: [number]
- **Completed Tasks**: [number] ([percentage]%)
- **In Progress Tasks**: [number]
- **Blocked Tasks**: [number]

## Task Categories

### [CATEGORY 1] - [Priority: HIGH/MEDIUM/LOW]

#### Phase 1: [Phase Name]

- [ ] **T001**: [S] [Task description] - [Hours]
- [ ] **T002**: [M] [Task description] - [Hours]
- [ ] **T003**: [L] [Task description] - [Hours]

#### Phase 2: [Phase Name]

- [ ] **T004**: [S] [Task description] - [Hours]
- [ ] **T005**: [M] [Task description] - [Hours]

### [CATEGORY 2] - [Priority: HIGH/MEDIUM/LOW]

#### Testing Tasks

- [ ] **T010**: [S] Unit tests for [module] - [Hours]
- [ ] **T011**: [M] Integration tests for [feature] - [Hours]
- [ ] **T012**: [L] E2E tests for [workflow] - [Hours]

#### Documentation Tasks

- [ ] **T015**: [S] API documentation update - [Hours]
- [ ] **T016**: [M] User guide update - [Hours]

## Task Details

### High Priority Tasks [P]

- **T001**: [Task title]
  - **Description**: [Detailed description]
  - **Acceptance Criteria**:
    - [ ] [Criteria 1]
    - [ ] [Criteria 2]
  - **Dependencies**: None
  - **Assignee**: [Team member]
  - **Estimated Time**: [X hours/days]

### Medium Priority Tasks

- **T002**: [Task title]
  - **Description**: [Detailed description]
  - **Acceptance Criteria**:
    - [ ] [Criteria 1]
    - [ ] [Criteria 2]
  - **Dependencies**: T001
  - **Assignee**: [Team member]
  - **Estimated Time**: [X hours/days]

### Low Priority Tasks

- **T003**: [Task title]
  - **Description**: [Detailed description]
  - **Acceptance Criteria**:
    - [ ] [Criteria 1]
    - [ ] [Criteria 2]
  - **Dependencies**: T002
  - **Assignee**: [Team member]
  - **Estimated Time**: [X hours/days]

## Dependencies

### Task Dependencies

```
T001 → T002 → T003 → T004
     ↘ T005 → T006
```

### External Dependencies

- **API Changes**: [Required API changes]
- **Database Updates**: [Required database changes]
- **Third-party Services**: [External dependencies]

## Parallel Execution Opportunities

### Can Be Done In Parallel

- [Tasks that can be executed simultaneously]
- [Other parallel tasks]

### Must Be Sequential

- [Tasks that must follow specific order]
- [Critical path tasks]

## Risk Assessment

### Blocker Risks

| Risk | Tasks Affected | Probability | Impact | Mitigation |
|------|----------------|-------------|--------|------------|
| [Risk description] | [Task IDs] | High/Med/Low | High/Med/Low | [Mitigation] |

### Resource Constraints

| Resource | Bottleneck | Impact | Mitigation |
|----------|------------|--------|------------|
| [Team member] | [Task type] | [Impact] | [Backup plan] |

## Completion Criteria

### Definition of Done for Each Task

- [ ] Code implemented and reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests updated
- [ ] Documentation updated
- [ ] Acceptance criteria met
- [ ] No regressions introduced

### Feature Definition of Done

- [ ] All tasks completed
- [ ] Feature tested end-to-end
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] Documentation complete
- [ ] Stakeholder approval received

## Progress Tracking

### Daily Standup Notes

- **Date**: [Current date]
- **Completed Yesterday**: [Tasks completed]
- **Focus Today**: [Today's priority tasks]
- **Blockers**: [Any blocking issues]

### Weekly Progress Updates

- **Week of**: [Week start date]
- **Tasks Completed**: [Number and list]
- **Tasks In Progress**: [Number and list]
- **Planned for Next Week**: [Upcoming tasks]
- **Issues/Blockers**: [Current issues]

## Notes & Decisions

[Record important decisions, changes, and observations during development]

---

**Legend:**

- [S] = Small (< 4 hours), [M] = Medium (4-8 hours), [L] = Large (> 8 hours)
- [P] = Priority tasks, [D] = Deferred tasks, [B] = Blocked tasks
- **Status**: [ ] Pending, [>] In Progress, [x] Completed, [!] Blocked
"""


# ============================================================================
# DECOMPOSITION TEMPLATES
# ============================================================================

MICROSERVICES_TEMPLATE = """# Microservices Decomposition Template

## Service Identification

### Business Capability Mapping

| Business Capability | Proposed Service | Bounded Context |
|---------------------|------------------|-----------------|
| [Capability 1] | [Service Name] | [Context] |
| [Capability 2] | [Service Name] | [Context] |

### Service Catalog

#### [Service Name 1]

- **Description**: [Service purpose and responsibilities]
- **Domain Model**: [Key entities and relationships]
- **API Endpoints**: [REST/GraphQL endpoints]
- **Database**: [Data store requirements]
- **Dependencies**: [External service dependencies]

#### [Service Name 2]

- **Description**: [Service purpose and responsibilities]
- **Domain Model**: [Key entities and relationships]
- **API Endpoints**: [REST/GraphQL endpoints]
- **Database**: [Data store requirements]
- **Dependencies**: [External service dependencies]

## Service Boundaries

### Context Mapping

```
[Service A] ←→ [Service B]
    ↓              ↓
[Service C] ←→ [Service D]
```

### Data Ownership

| Data Domain | Owner Service | Access Pattern |
|-------------|---------------|----------------|
| [Customer Data] | [Customer Service] | Read/Write |
| [Order Data] | [Order Service] | Read/Write |

## Communication Patterns

### Synchronous Communication

- **REST APIs**: [When to use]
- **GraphQL**: [When to use]
- **gRPC**: [When to use]

### Asynchronous Communication

- **Message Queues**: [RabbitMQ, Kafka]
- **Event Streams**: [Apache Kafka, AWS Kinesis]
- **Event Sourcing**: [When to implement]

## Infrastructure Considerations

### Service Mesh

- **Technology**: [Istio, Linkerd, Consul]
- **Traffic Management**: [Load balancing, routing]
- **Security**: [mTLS, policies]

### Observability

- **Logging**: [ELK stack, Fluentd]
- **Metrics**: [Prometheus, Grafana]
- **Tracing**: [Jaeger, Zipkin]

## Deployment Strategy

### Container Orchestration

- **Platform**: [Kubernetes, ECS, AKS]
- **Service Discovery**: [Consul, Eureka]
- **Configuration**: [Spring Cloud Config, Consul K/V]

### CI/CD Pipeline

- **Build**: [Docker build process]
- **Test**: [Testing strategy]
- **Deploy**: [Blue/Green, Canary, Rolling]
"""

API_CONTRACT_TEMPLATE = """openapi: 3.0.3
info:
  title: [Service Name] API
  description: API contract for [Service Name]
  version: 1.0.0
  contact:
    name: [Team Name]
    email: [team@example.com]

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

paths:
  /[resource]:
    get:
      summary: List [resources]
      description: Retrieve a paginated list of [resources]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/[Resource]'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

    post:
      summary: Create [resource]
      description: Create a new [resource]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Create[Resource]'
      responses:
        '201':
          description: Resource created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

  /[resource]/{id}:
    get:
      summary: Get [resource] by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]'
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      summary: Update [resource]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Update[Resource]'
      responses:
        '200':
          description: Resource updated successfully

    delete:
      summary: Delete [resource]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Resource deleted successfully
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    '[Resource]':
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    'Create[Resource]':
      type: object
      required:
        - name
      properties:
        name:
          type: string

    'Update[Resource]':
      type: object
      properties:
        name:
          type: string

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string

    Unauthorized:
      description: Unauthorized

    NotFound:
      description: Resource not found

    InternalError:
      description: Internal server error

security:
  - BearerAuth: []
"""


# ============================================================================
# TEMPLATE REGISTRY
# ============================================================================

TEMPLATE_MAP: Dict[str, str] = {
    "spec.md": SPEC_TEMPLATE,
    "plan.md": PLAN_TEMPLATE,
    "task.md": TASK_TEMPLATE,
    "microservices.md": MICROSERVICES_TEMPLATE,
    "api-contract.yaml": API_CONTRACT_TEMPLATE,
}


def get_embedded_template(template_type: str) -> str:
    """
    Get an embedded template by type.

    Args:
        template_type: Template filename (e.g., 'spec.md', 'plan.md')

    Returns:
        Template content string

    Raises:
        KeyError: If template type not found
    """
    if template_type not in TEMPLATE_MAP:
        raise KeyError(f"Unknown template type: {template_type}")
    return TEMPLATE_MAP[template_type]


def write_embedded_template(dst_path: Path, template_type: str) -> None:
    """
    Write an embedded template to a file.

    Args:
        dst_path: Destination path for the template
        template_type: Template type to write
    """
    content = get_embedded_template(template_type)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)


def write_decomposition_templates(decomp_dir: Path) -> None:
    """
    Write all decomposition templates to a directory.

    Args:
        decomp_dir: Directory for decomposition templates
    """
    decomp_dir.mkdir(parents=True, exist_ok=True)

    # Write microservices template
    write_embedded_template(decomp_dir / "microservices.md", "microservices.md")

    # Write API contract template
    write_embedded_template(decomp_dir / "api-contract.yaml", "api-contract.yaml")
