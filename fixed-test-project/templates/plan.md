<!-- SpecPulse Implementation Plan Template v4.0 - AI-Optimized -->
<!-- AI Instructions: Generate plan from specification following constitutional gates -->

# Implementation Plan: {{ feature_name }}

## Specification Reference
- **Spec ID**: SPEC-{{ feature_id }}
- **Branch**: {{ branch_name }}
- **Generated**: {{ date }}
- **Optimization Focus**: {{ optimization_focus | default("SIMPLICITY") }}

## Phase -1: Pre-Implementation Gates

### Constitutional Compliance Check
**THIS SECTION MUST BE COMPLETED BEFORE ANY IMPLEMENTATION**

#### Simplicity Gate (Article VII)
- [ ] Using ≤3 projects/modules for initial implementation?
- [ ] No future-proofing without documented need?
- [ ] Direct framework usage (no unnecessary wrappers)?
- [ ] Single model representation per concept?

#### Anti-Abstraction Gate (Article VII)
- [ ] Using framework features directly?
- [ ] No unnecessary abstraction layers?
- [ ] Clear, simple interfaces?
- [ ] Avoiding premature optimization?

#### Test-First Gate (Article III)
- [ ] Test specifications written?
- [ ] Tests reviewed and approved?
- [ ] Tests confirmed to FAIL before implementation?
- [ ] TDD cycle planned (Red-Green-Refactor)?

#### Integration-First Gate (Article VIII)
- [ ] Contract tests defined?
- [ ] Using real services over mocks?
- [ ] Production-like test environment planned?
- [ ] End-to-end test scenarios identified?

#### Research Gate (Article VI)
- [ ] Library options researched?
- [ ] Performance implications documented?
- [ ] Security considerations analyzed?
- [ ] Trade-offs documented?

**Gate Status**: {{ gate_status | default("[ ] PENDING") }}

## Complexity Tracking
{% if complexity_exceptions %}
{% for exception in complexity_exceptions %}
### Exception {{ loop.index }}
- **Article**: {{ exception.article }}
- **Violation**: {{ exception.violation }}
- **Justification**: {{ exception.justification }}
- **Mitigation**: {{ exception.mitigation }}
{% endfor %}
{% else %}
No complexity exceptions documented.
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
**Constitutional Gates**: {{ gate_status | default("PENDING") }}
**Next Steps**: Use `/task` to break down into executable tasks