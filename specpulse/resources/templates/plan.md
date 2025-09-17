<!-- SpecPulse Implementation Plan Template v4.0 - AI-Optimized -->
<!-- AI Instructions: Generate plan from specification following SDD gates -->

# Implementation Plan: {{ feature_name }}

## Specification Reference
- **Spec ID**: SPEC-{{ feature_id }}
- **Branch**: {{ branch_name }}
- **Generated**: {{ date }}
- **Optimization Focus**: {{ optimization_focus | default("SIMPLICITY") }}

## Phase -1: Pre-Implementation Gates

### SDD Compliance Check
**ENSURE SPECIFICATION-DRIVEN DEVELOPMENT PRINCIPLES ARE FOLLOWED**

#### Principle 1: Specification First
- [ ] Clear specifications written?
- [ ] User stories and acceptance criteria defined?
- [ ] [NEEDS CLARIFICATION] markers for unknowns?
- [ ] Functional and non-functional requirements documented?

#### Principle 2: Incremental Planning
- [ ] Work broken into phases?
- [ ] Each phase delivers value?
- [ ] Milestones and checkpoints defined?
- [ ] Features prioritized by business value?

#### Principle 3: Task Decomposition
- [ ] Tasks are specific and actionable?
- [ ] Effort estimates provided?
- [ ] Definition of Done clear?
- [ ] Tasks can be picked up immediately?

#### Principle 4: Traceable Implementation
- [ ] Code will reference spec requirements?
- [ ] Commits will link to tasks?
- [ ] Bidirectional traceability planned?
- [ ] Spec updates process defined?

#### Principle 5: Continuous Validation
- [ ] Validation checkpoints identified?
- [ ] Acceptance tests planned?
- [ ] Spec-code sync process defined?
- [ ] Regular validation scheduled?

#### Principle 6: Quality Assurance
- [ ] Test strategy appropriate for project type?
- [ ] Acceptance criteria testable?
- [ ] Code review process defined?
- [ ] Quality metrics identified?

#### Principle 7: Architecture Documentation
- [ ] Technology choices documented?
- [ ] Integration points identified?
- [ ] Technical debt tracking planned?
- [ ] ADR process established?

#### Principle 8: Iterative Refinement
- [ ] Feedback loops established?
- [ ] Spec versioning process defined?
- [ ] Learning capture process planned?
- [ ] Refinement triggers identified?

#### Principle 9: Stakeholder Alignment
- [ ] Stakeholders identified?
- [ ] Communication plan established?
- [ ] Approval process defined?
- [ ] Change management process clear?

**Gate Status**: {{ gate_status | default("[ ] PENDING") }}

## Architecture Decisions
{% if architectural_decisions %}
{% for decision in architectural_decisions %}
### Decision {{ loop.index }}
- **Area**: {{ decision.area }}
- **Decision**: {{ decision.decision }}
- **Rationale**: {{ decision.rationale }}
- **Trade-offs**: {{ decision.trade_offs }}
{% endfor %}
{% else %}
No significant architectural decisions documented yet.
{% endif %}

## Technology Stack

### Core Technologies
{% for tech in core_technologies %}
- **{{ tech.name }}**: {{ tech.version }} - {{ tech.purpose }}
{% endfor %}

### Dependencies
{% for dep in dependencies %}
- **{{ dep.name }}**: {{ dep.reason }}
{% endfor %}

## Architecture Overview

### System Components
{% for component in components %}
#### {{ component.name }}
- **Purpose**: {{ component.purpose }}
- **Key Features**: {{ component.features }}
- **Dependencies**: {{ component.dependencies | join(", ") }}
{% endfor %}

### Data Models
{% for model in data_models %}
#### {{ model.name }}
- **Fields**: {{ model.fields | join(", ") }}
- **Relationships**: {{ model.relationships }}
- **Validation**: {{ model.validation }}
{% endfor %}

## Implementation Phases

### Phase 0: Critical Path (Week {{ phase_0.weeks | default(1) }})
{% for task in phase_0.tasks %}
- [ ] {{ task.description }}
{% endfor %}

### Phase 1: Foundation (Week {{ phase_1.weeks | default(2) }})
{% for task in phase_1.tasks %}
- [ ] {{ task.description }}
{% endfor %}

### Phase 2: Core Features (Week {{ phase_2.weeks | default(3) }})
{% for task in phase_2.tasks %}
- [ ] {{ task.description }}
{% endfor %}

### Phase 3: Polish (Week {{ phase_3.weeks | default(1) }})
{% for task in phase_3.tasks %}
- [ ] {{ task.description }}
{% endfor %}

## API Contracts

### Endpoints
{% for endpoint in endpoints %}
#### {{ endpoint.method }} {{ endpoint.path }}
- **Description**: {{ endpoint.description }}
- **Request**: {{ endpoint.request }}
- **Response**: {{ endpoint.response }}
- **Authentication**: {{ endpoint.auth | default("Required") }}
{% endfor %}

### Data Schemas
{% for schema in schemas %}
#### {{ schema.name }}
```json
{{ schema.json | indent(4) }}
```
{% endfor %}

## Testing Strategy

### Test Categories
- **Unit Tests**: {{ testing.unit.target | default("80% coverage") }}
- **Integration Tests**: {{ testing.integration.target | default("Critical paths") }}
- **E2E Tests**: {{ testing.e2e.target | default("Key user workflows") }}
- **Performance Tests**: {{ testing.performance.target | default("Load testing") }}

### Test Environment
- **Database**: {{ testing.environment.database | default("PostgreSQL") }}
- **Services**: {{ testing.environment.services | join(", ") }}
- **Test Data**: {{ testing.environment.data_strategy | default("Seed with realistic data") }}

## Security Considerations

### Authentication & Authorization
- **Method**: {{ security.auth_method | default("JWT tokens") }}
- **Roles**: {{ security.roles | join(", ") }}
- **Permissions**: {{ security.permissions_model | default("Role-based access control") }}

### Data Protection
- **Encryption**: {{ security.encryption.transit | default("TLS 1.3") }} in transit, {{ security.encryption.at_rest | default("AES-256") }} at rest
- **Compliance**: {{ security.compliance | join(", ") }}

## Deployment Strategy

### Environments
{% for env in environments %}
#### {{ env.name }}
- **URL**: {{ env.url }}
- **Auto-deploy**: {{ env.auto_deploy | default("Manual") }}
- **Health Checks**: {{ env.health_checks | default("Basic monitoring") }}
{% endfor %}

### Rollback Plan
- **Strategy**: {{ rollback.strategy | default("Blue-green deployment") }}
- **Triggers**: {{ rollback.triggers | join(", ") }}
- **Recovery Time**: {{ rollback.recovery_time | default("< 5 minutes") }}

## Success Criteria

### Must-Have Metrics
{% for metric in success_criteria.must %}
- {{ metric.name }}: {{ metric.target }} ({{ metric.measurement }})
{% endfor %}

### Should-Have Metrics
{% for metric in success_criteria.should %}
- {{ metric.name }}: {{ metric.target }} ({{ metric.measurement }})
{% endfor %}

## Risk Assessment

| Risk | Probability | Impact | Mitigation | Owner |
|------|------------|--------|------------|-------|
{% for risk in risks %}
| {{ risk.description }} | {{ risk.probability }} | {{ risk.impact }} | {{ risk.mitigation }} | {{ risk.owner }} |
{% endfor %}

## Monitoring & Observability

### Key Metrics
{% for metric in monitoring.metrics %}
- **{{ metric.name }}**: {{ metric.target }} ({{ metric.unit }})
{% endfor %}

### Alerting
- **Critical Alerts**: {{ monitoring.alerts.critical | join(", ") }}
- **Warning Alerts**: {{ monitoring.alerts.warnings | join(", ") }}

---
**Generated by**: {{ ai_assistant }} on {{ date }}
**SDD Gates**: {{ gate_status | default("PENDING") }}
**Next Steps**: Use `/sp-task breakdown` to break down into executable tasks