# Microservice: {{service_name}}

## Service Overview
- **Name**: {{service_name}}
- **Domain**: {{domain}}
- **Type**: [API|Worker|Gateway|Database|Cache]
- **Parent Spec**: SPEC-{{spec_id}}
- **Created**: {{date}}

## Service Responsibilities
### Primary Responsibilities
- {{primary_responsibility_1}}
- {{primary_responsibility_2}}
- {{primary_responsibility_3}}

### Secondary Responsibilities
- {{secondary_responsibility_1}}
- {{secondary_responsibility_2}}

## Boundaries
### What This Service DOES
- Manages {{entity}} lifecycle
- Handles {{operation}} operations
- Provides {{capability}} capabilities

### What This Service DOES NOT DO
- Does not manage {{excluded_entity}}
- Does not handle {{excluded_operation}}
- Delegates {{delegated_capability}} to {{other_service}}

## API Specification

### REST Endpoints
```
GET    /api/v1/{{resource}}          # List all {{resource}}
GET    /api/v1/{{resource}}/{id}     # Get specific {{resource}}
POST   /api/v1/{{resource}}          # Create new {{resource}}
PUT    /api/v1/{{resource}}/{id}     # Update {{resource}}
DELETE /api/v1/{{resource}}/{id}     # Delete {{resource}}
```

### Event Publishing
- `{{entity}}.created` - When new {{entity}} is created
- `{{entity}}.updated` - When {{entity}} is modified
- `{{entity}}.deleted` - When {{entity}} is removed

### Event Subscriptions
- `{{dependency}}.changed` - React to {{dependency}} changes
- `{{trigger}}.occurred` - Handle {{trigger}} events

## Data Model

### Primary Entities
```json
{
  "{{entity}}": {
    "id": "uuid",
    "name": "string",
    "status": "enum",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
}
```

### Database Schema
- **Database Type**: {{database_type}}
- **Collections/Tables**: {{collections}}
- **Indexes**: {{indexes}}

## Dependencies

### Internal Services
- **{{service_1}}**: For {{purpose_1}}
- **{{service_2}}**: For {{purpose_2}}

### External Services
- **{{external_1}}**: {{external_purpose_1}}
- **{{external_2}}**: {{external_purpose_2}}

### Libraries & Frameworks
- {{framework}}: Core framework
- {{library_1}}: {{library_purpose_1}}
- {{library_2}}: {{library_purpose_2}}

## Configuration

### Environment Variables
```bash
SERVICE_NAME={{service_name}}
SERVICE_PORT={{port}}
DATABASE_URL={{database_url}}
CACHE_URL={{cache_url}}
MESSAGE_BROKER_URL={{broker_url}}
```

### Secrets
- `API_KEY`: For external service authentication
- `JWT_SECRET`: For token generation
- `DATABASE_PASSWORD`: Database access

## Scalability Considerations

### Horizontal Scaling
- **Min Instances**: {{min_instances}}
- **Max Instances**: {{max_instances}}
- **Auto-scaling Metric**: {{scaling_metric}}

### Performance Targets
- **Response Time**: < {{response_time}}ms
- **Throughput**: {{throughput}} req/s
- **Availability**: {{availability}}%

## Monitoring & Observability

### Key Metrics
- Request rate and latency
- Error rate and types
- Database query performance
- Cache hit ratio

### Health Checks
- `/health` - Basic liveness check
- `/ready` - Readiness with dependency checks

### Logging
- Structured JSON logging
- Correlation ID tracking
- Error stack traces

## Security Considerations
- Authentication: {{auth_method}}
- Authorization: {{authz_method}}
- Rate Limiting: {{rate_limit}} req/min
- Input Validation: All inputs validated
- Output Sanitization: Prevent data leaks

## Testing Strategy
- Unit Tests: {{unit_test_coverage}}% coverage
- Integration Tests: With mocked dependencies
- Contract Tests: API contract validation
- Load Tests: {{load_test_target}} concurrent users

## Deployment
- **Container**: Docker image
- **Orchestration**: Kubernetes
- **CI/CD**: Automated pipeline
- **Rollback**: Blue-green deployment

## Notes
<!-- Additional implementation notes -->