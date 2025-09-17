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

## SDD Compliance
- [ ] Service specifications clear (Principle 1: Specification First)
- [ ] Phased service rollout planned (Principle 2: Incremental Planning)
- [ ] Service tasks decomposed (Principle 3: Task Decomposition)
- [ ] Test strategy defined per service (Principle 6: Quality Assurance)
- [ ] Architecture decisions documented (Principle 7: Architecture Documentation)

## Next Steps
1. Review service boundaries with team
2. Run `/sp-plan generate` with decomposition context
3. Create tasks per service with `/sp-task breakdown`
4. Validate with `/sp-validate decomposition`