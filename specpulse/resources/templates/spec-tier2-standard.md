<!-- TIER: standard -->
# Feature: {{ feature_name }}

<!-- LLM GUIDANCE:
This is the standard tier for most features. Provide enough detail for planning and implementation.
Include user stories, requirements, and technical approach.
User can expand to complete tier if needed for production-grade specs.
-->

## Executive Summary
{{ executive_summary }}

<!-- LLM GUIDANCE: 2-3 sentences summarizing the feature, its purpose, and expected impact -->

## What
{{ what_description }}

<!-- LLM GUIDANCE: Clear description of what is being built (2-3 sentences) -->

## Why
{{ why_description }}

<!-- LLM GUIDANCE: Business value, user benefit, or problem being solved (2-3 sentences) -->

## User Stories
<!-- LLM GUIDANCE: 2-3 user stories in "As a... I want... So that..." format -->

1. **{{ user_story_1_title }}**
   - As a {{ user_role_1 }}
   - I want {{ user_want_1 }}
   - So that {{ user_benefit_1 }}

2. **{{ user_story_2_title }}**
   - As a {{ user_role_2 }}
   - I want {{ user_want_2 }}
   - So that {{ user_benefit_2 }}

## Functional Requirements
<!-- LLM GUIDANCE: 3-7 specific, testable requirements with FR-XXX identifiers -->

- **FR-001**: {{ requirement_1 }}
- **FR-002**: {{ requirement_2 }}
- **FR-003**: {{ requirement_3 }}
- **FR-004**: {{ requirement_4 }}
- **FR-005**: {{ requirement_5 }}

## Technical Approach
<!-- LLM GUIDANCE: High-level architecture, key technologies, design patterns, data models -->

### Architecture
{{ architecture_overview }}

### Key Technologies
- {{ technology_1 }}
- {{ technology_2 }}
- {{ technology_3 }}

### Data Model
{{ data_model_description }}

## Acceptance Criteria
<!-- LLM GUIDANCE: 3-5 detailed, testable criteria that define "done" -->

- [ ] {{ acceptance_criterion_1 }}
- [ ] {{ acceptance_criterion_2 }}
- [ ] {{ acceptance_criterion_3 }}
- [ ] {{ acceptance_criterion_4 }}
- [ ] {{ acceptance_criterion_5 }}

---
<!-- EXPAND_NEXT: tier3 -->
💡 Need comprehensive spec for production? Run: `specpulse expand {{ feature_id }} --to-tier complete`
