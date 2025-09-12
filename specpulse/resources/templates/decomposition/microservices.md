# Microservice Decomposition: {{ feature_name }}

## Metadata
- **Spec ID**: {{ spec_id }}
- **Decomposed**: {{ date }}
- **Version**: {{ version }}

## Service Boundaries

{{ services }}

## Communication Matrix

{{ communication_patterns }}

## Data Ownership

{{ data_boundaries }}

## Integration Points

{{ integration_points }}

## Constitutional Compliance
- [ ] Each service ≤ 3 core modules (Article I: Simplicity)
- [ ] Single responsibility per service (Article V)
- [ ] Clear test boundaries defined (Article III)
- [ ] Framework selection documented (Article VIII)

## Next Steps
1. Review service boundaries with team
2. Run `/sp-plan generate` with decomposition context
3. Create tasks per service with `/sp-task breakdown`
4. Validate with `/sp-validate decomposition`