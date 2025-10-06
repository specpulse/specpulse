<!-- TIER: complete -->
# Feature: {{ feature_name }}

<!-- LLM GUIDANCE:
This is the complete tier for production-grade features. Provide comprehensive details covering
all aspects: functional, non-functional, security, testing, and deployment.
This is the most detailed tier - no further expansion available.
-->

## Executive Summary
{{ executive_summary }}

<!-- LLM GUIDANCE: 2-3 sentences summarizing the feature, its purpose, and expected impact -->

## What
{{ what_description }}

<!-- LLM GUIDANCE: Clear, comprehensive description of what is being built (3-5 sentences) -->

## Why
{{ why_description }}

<!-- LLM GUIDANCE: Business value, user benefit, or problem being solved (3-5 sentences) -->

## User Stories
<!-- LLM GUIDANCE: 3-5 detailed user stories in "As a... I want... So that..." format -->

1. **{{ user_story_1_title }}**
   - As a {{ user_role_1 }}
   - I want {{ user_want_1 }}
   - So that {{ user_benefit_1 }}

2. **{{ user_story_2_title }}**
   - As a {{ user_role_2 }}
   - I want {{ user_want_2 }}
   - So that {{ user_benefit_2 }}

3. **{{ user_story_3_title }}**
   - As a {{ user_role_3 }}
   - I want {{ user_want_3 }}
   - So that {{ user_benefit_3 }}

## Functional Requirements
<!-- LLM GUIDANCE: 5-10 specific, testable requirements with FR-XXX identifiers -->

- **FR-001**: {{ requirement_1 }}
- **FR-002**: {{ requirement_2 }}
- **FR-003**: {{ requirement_3 }}
- **FR-004**: {{ requirement_4 }}
- **FR-005**: {{ requirement_5 }}
- **FR-006**: {{ requirement_6 }}
- **FR-007**: {{ requirement_7 }}

## Non-Functional Requirements
<!-- LLM GUIDANCE: Performance, scalability, reliability, usability requirements with NFR-XXX identifiers -->

- **NFR-001**: {{ nfr_performance }}
- **NFR-002**: {{ nfr_scalability }}
- **NFR-003**: {{ nfr_reliability }}
- **NFR-004**: {{ nfr_usability }}

## Technical Approach
<!-- LLM GUIDANCE: Detailed architecture, key technologies, design patterns, data models, APIs -->

### Architecture
{{ architecture_overview }}

### Key Technologies
- {{ technology_1 }}
- {{ technology_2 }}
- {{ technology_3 }}
- {{ technology_4 }}

### Design Patterns
{{ design_patterns }}

### Data Model
{{ data_model_description }}

### API Design
{{ api_design }}

## Edge Cases
<!-- LLM GUIDANCE: Error conditions, boundary cases, exceptional scenarios -->

1. **{{ edge_case_1_title }}**: {{ edge_case_1_description }}
2. **{{ edge_case_2_title }}**: {{ edge_case_2_description }}
3. **{{ edge_case_3_title }}**: {{ edge_case_3_description }}

## Security Considerations
<!-- LLM GUIDANCE: Authentication, authorization, data protection, compliance requirements -->

### Authentication & Authorization
{{ auth_approach }}

### Data Protection
{{ data_protection }}

### Compliance
{{ compliance_requirements }}

### Security Testing
{{ security_testing }}

## Performance Requirements
<!-- LLM GUIDANCE: Specific, measurable performance targets -->

- **Latency**: {{ latency_target }}
- **Throughput**: {{ throughput_target }}
- **Resource Limits**: {{ resource_limits }}
- **Scalability**: {{ scalability_target }}

## Testing Strategy
<!-- LLM GUIDANCE: Comprehensive testing approach covering all test types -->

### Unit Tests
{{ unit_test_strategy }}

### Integration Tests
{{ integration_test_strategy }}

### End-to-End Tests
{{ e2e_test_strategy }}

### Performance Tests
{{ performance_test_strategy }}

### Security Tests
{{ security_test_strategy }}

## Deployment Considerations
<!-- LLM GUIDANCE: Deployment strategy, rollout plan, rollback procedures, monitoring -->

### Deployment Strategy
{{ deployment_strategy }}

### Rollout Plan
{{ rollout_plan }}

### Rollback Procedures
{{ rollback_procedures }}

### Monitoring & Alerts
{{ monitoring_alerts }}

## Acceptance Criteria
<!-- LLM GUIDANCE: 5-10 comprehensive, testable criteria that define "done" -->

- [ ] {{ acceptance_criterion_1 }}
- [ ] {{ acceptance_criterion_2 }}
- [ ] {{ acceptance_criterion_3 }}
- [ ] {{ acceptance_criterion_4 }}
- [ ] {{ acceptance_criterion_5 }}
- [ ] {{ acceptance_criterion_6 }}
- [ ] {{ acceptance_criterion_7 }}

---
✅ **Specification Complete**: This is the most comprehensive tier.
💡 Ready to create implementation plan: `specpulse plan generate {{ feature_id }}`
