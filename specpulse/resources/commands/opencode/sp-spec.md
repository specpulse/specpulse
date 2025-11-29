---
name: sp-spec
description: Create and manage specifications without SpecPulse CLI
version: "1.0"
agent: specpulse-assistant
workflow_type: specification_management
---

# SpecPulse Specification Management Workflow

This workflow implements complete CLI-independent specification creation and management with AI-enhanced content generation.

## Agent Capabilities Required

- File operations: Read, Write, Edit, Bash, Glob, TodoWrite
- Directory traversal protection
- Atomic file operation handling
- AI content generation and analysis
- Error recovery and rollback mechanisms

## Workflow Steps

### Step 1: Argument Parsing and Action Determination

**Parse input arguments:**
```yaml
inputs:
  action: enum [create, update, validate, clarify]
  description: string
  feature_name: string
```

**Action logic:**
- Parse the command arguments:
  - If first argument is create, update, validate, or clarify → Use that action
  - If no action specified → Default to create
  - For create → All remaining text becomes the description
  - For other actions → Look for feature name or use current feature

### Step 2: Current Feature Context Detection

**Feature context algorithm:**
1. Check `.specpulse/memory/context.md` for active feature
2. Look for most recently modified spec/plan/task directory
3. Validate feature directory exists and is properly structured
4. Extract feature ID and name from directory structure
5. Set working context for subsequent operations

### Step 3: Specification Creation (Action: create)

**Universal ID System Implementation:**
```yaml
spec_id_generation:
  scan_directory: ".specpulse/specs/[feature]/"
  file_pattern: "spec-(\\d+)\\.md"
  algorithm: |
    1. Use Glob tool to scan directory
    2. Parse existing spec-###.md files to extract numbers
    3. Convert to integers and find the maximum value
    4. Generate next sequential: next_num = max_num + 1
    5. Zero-pad: format(next_num, '03d') → 001, 002, 003
    6. Validate no conflicts exist before using the number
```

**Template Processing:**
```yaml
template_handling:
  primary_template: ".specpulse/templates/spec.md"
  fallback_structure: |
    ---
    title: [Generated Title]
    feature_id: [Feature ID]
    spec_id: [Generated Spec ID]
    created_at: [Timestamp]
    status: draft
    ---

    # Executive Summary
    [AI-generated summary]

    # Functional Requirements
    [Detailed requirements breakdown]

    # User Stories
    [Given-When-Then format stories]

    # Acceptance Criteria
    [Measurable completion criteria]

    # Technical Constraints
    [Performance, security, scalability]

    # Risk Assessment
    [Potential risks and mitigations]
```

**AI Content Enhancement:**
```yaml
content_generation:
  project_type_detection:
    - Web Application: React/Vue/Angular + API
    - API Service: REST/GraphQL microservice
    - Mobile App: React Native/Flutter
    - CLI Tool: Command-line interface
    - Data Pipeline: ETL/ELT processing
    - Library/SDK: Reusable component

  complexity_assessment:
    - Simple (2-4 hours): Single feature, minimal dependencies
    - Standard (8-12 hours): Multiple features, some integrations
    - Complex (16-24 hours): Multiple services, complex workflows

  required_sections:
    - Executive Summary ✓
    - Functional Requirements ✓
    - User Stories ✓
    - Acceptance Criteria ✓
    - Technical Constraints ✓
    - Risk Assessment ✓
    - Success Metrics ✓
```

### Step 4: Specification Update (Action: update)

**Update workflow:**
```yaml
update_process:
  1. List all specification files in current feature
  2. Present selection interface for user choice
  3. Parse existing content and identify sections
  4. Generate updated content based on new requirements
  5. Preserve existing structure while enhancing content
  6. Maintain version history and change tracking
```

### Step 5: Specification Validation (Action: validate)

**Comprehensive validation:**
```yaml
validation_checks:
  file_structure:
    - Specification file exists and is readable
    - File naming follows spec-[###].md pattern
    - Proper markdown structure and formatting

  content_completeness:
    - Executive Summary present and complete
    - Functional Requirements detailed and testable
    - User Stories follow Given-When-Then format
    - Acceptance Criteria are measurable
    - Technical Constraints specified
    - Risk Assessment included

  quality_metrics:
    - Count [NEEDS CLARIFICATION] markers
    - Calculate completeness percentage
    - Identify missing or incomplete sections
    - Verify requirement traceability
```

### Step 6: Clarification Resolution (Action: clarify)

**Clarification workflow:**
```yaml
clarification_process:
  pattern_scanning:
    - Scan for [NEEDS CLARIFICATION:...] patterns
    - Extract each question with surrounding context
    - Organize by priority and dependency

  resolution_handling:
    - Present clarifications to user interactively
    - Collect resolutions for each item
    - Replace markers with ✅ **CLARIFIED**: [answer] format
    - Update specification with resolved clarifications
    - Track clarification history
```

### Step 7: SDD Gates Compliance

**Compliance validation:**
```yaml
sdd_gates:
  specification_first:
    requirement: Clear requirements before implementation
    validation: All functional requirements are defined and testable

  traceable:
    requirement: Each requirement maps to user stories and acceptance criteria
    validation: Bidirectional tracing between requirements and stories

  testable:
    requirement: Acceptance criteria can be verified through testing
    validation: All acceptance criteria are measurable and verifiable

  complete:
    requirement: All necessary sections for implementation
    validation: All required sections present and complete
```

## Output Format

**Success response:**
```yaml
specification:
  id: "002"
  feature_id: "003"
  file_path: ".specpulse/specs/003-user-management/spec-002.md"
  status: "created"
  created_at: "2025-01-11T16:30:00Z"
  completeness: 100%

content_analysis:
  project_type: "Web Application"
  complexity: "Standard (8-12 hours)"
  requirements_generated: 12
  user_stories_created: 8
  acceptance_criteria: 24

validation_results:
  total_sections: 14/14
  clarifications_needed: 0
  sdd_gates_compliance: true

next_steps:
  - "Generate implementation plan: /sp-plan"
  - "Break down into tasks: /sp-task"
  - "Begin implementation: /sp-execute"
```

## Error Handling and Recovery

**Comprehensive error scenarios:**
```yaml
error_handling:
  context_errors:
    no_active_feature:
      action: Prompt to run /sp-pulse first
      recovery: Guide through feature initialization

    invalid_feature_structure:
      action: Validate and fix directory structure
      recovery: Rebuild structure from available data

  file_system_errors:
    permission_denied:
      action: Guide user to check file permissions
      recovery: Provide specific chmod commands

    template_missing:
      action: Use built-in fallback structure
      recovery: Create comprehensive specification manually

  content_errors:
    vague_description:
      action: Ask clarifying questions
      recovery: Guide user through requirement refinement

    conflicting_requirements:
      action: Identify and request resolution
      recovery: Facilitate requirement reconciliation
```

## Safety Constraints

- **Path validation**: Only operate within `.specpulse/` directory
- **Protected directories**: Never modify `templates/`, `specpulse/`, AI configs
- **Atomic operations**: Prevent partial updates and corruption
- **Rollback capability**: Restore original state on failures
- **Input validation**: Comprehensive sanitization of all inputs

## Integration Features

- **AI-Enhanced Generation**: Advanced content analysis and generation
- **Project Type Detection**: Automatic template adaptation
- **Complexity Assessment**: Realistic timeline and effort estimation
- **Universal ID System**: Conflict-free file numbering
- **Context Management**: File-based project memory
- **Progress Monitoring**: Real-time completeness tracking