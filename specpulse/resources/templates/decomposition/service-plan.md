# Service Plan: {{ service_name }}

## Metadata
- **Service**: {{ service_name }}
- **Bounded Context**: {{ bounded_context }}
- **Spec Reference**: {{ spec_id }}
- **Generated**: {{ date }}
- **Version**: {{ version }}

## Service Overview

### Responsibility
{{ service_responsibility }}

### Capabilities
{{ service_capabilities }}

### Data Ownership
{{ data_ownership }}

## Architecture

### Internal Structure
```
{{ service_name }}/
├── domain/          # Business logic
├── application/     # Use cases
├── infrastructure/  # External interfaces
└── presentation/    # API layer
```

### Technology Stack
- **Language**: {{ language }}
- **Framework**: {{ framework }}
- **Database**: {{ database }}
- **Cache**: {{ cache }}
- **Message Queue**: {{ queue }}

## API Design

### REST Endpoints
{{ rest_endpoints }}

### Event Publications
{{ event_publications }}

### Event Subscriptions
{{ event_subscriptions }}

## Data Model

### Entities
{{ entities }}

### Value Objects
{{ value_objects }}

### Aggregates
{{ aggregates }}

## Implementation Phases

### Phase 1: Domain Layer
**Duration**: {{ phase1_duration }}
- Domain entities
- Business rules
- Domain events
- Value objects

### Phase 2: Application Layer
**Duration**: {{ phase2_duration }}
- Use cases
- Application services
- DTOs
- Mappers

### Phase 3: Infrastructure Layer
**Duration**: {{ phase3_duration }}
- Database repositories
- External service clients
- Message handlers
- Cache implementation

### Phase 4: API Layer
**Duration**: {{ phase4_duration }}
- REST controllers
- Request/Response models
- Validation
- Error handling

## Testing Strategy

### Unit Tests
- Domain logic: {{ domain_coverage }}%
- Use cases: {{ usecase_coverage }}%
- Infrastructure: {{ infra_coverage }}%

### Integration Tests
{{ integration_tests }}

### Contract Tests
{{ contract_tests }}

## Service Configuration

### Environment Variables
```yaml
{{ env_variables }}
```

### Feature Flags
{{ feature_flags }}

### Secrets Management
{{ secrets }}

## Deployment

### Container Configuration
```dockerfile
{{ dockerfile_snippet }}
```

### Resource Requirements
- CPU: {{ cpu_requirements }}
- Memory: {{ memory_requirements }}
- Storage: {{ storage_requirements }}

### Scaling Strategy
{{ scaling_strategy }}

## Monitoring

### Metrics
{{ metrics }}

### Logs
{{ logging_strategy }}

### Alerts
{{ alert_rules }}

## Dependencies

### Internal Services
{{ internal_dependencies }}

### External Services
{{ external_dependencies }}

### Libraries
{{ libraries }}

## Constitutional Compliance
- [ ] Service has single responsibility (Article V)
- [ ] ≤ 3 core modules (Article I: Simplicity)
- [ ] Tests before implementation (Article III)
- [ ] Direct framework usage (Article VIII)

## Risk Assessment
{{ risks }}

## Success Criteria
- [ ] All endpoints functional
- [ ] Test coverage > {{ test_target }}%
- [ ] Performance targets met
- [ ] Zero security vulnerabilities
- [ ] Documentation complete