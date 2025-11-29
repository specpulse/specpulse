---
name: sp-clarify
description: Resolve clarification markers in specifications without SpecPulse CLI
version: "1.0"
agent: specpulse-assistant
workflow_type: clarification_resolution
---

# SpecPulse Clarification Resolution Workflow

This workflow implements comprehensive CLI-independent clarification marker resolution with interactive context-aware question processing.

## Agent Capabilities Required

- File operations: Read, Edit, Bash, Grep, TodoWrite
- Directory traversal protection
- Atomic file operation handling
- Interactive user engagement
- Context analysis and extraction
- SDD compliance validation
- Error recovery and progress tracking

## Workflow Steps

### Step 1: Argument Parsing and Target Detection

**Parse input arguments:**
```yaml
inputs:
  spec_id: string
  action: enum [detect, resolve, validate]
```

**Target detection algorithm:**
```yaml
target_detection:
  context_analysis:
    - Use Read tool to detect current feature context from .specpulse/memory/context.md
    - Extract active feature ID and working directory
    - Validate feature directory structure and accessibility

  specification_location:
    provided_id:
      condition: spec_id argument provided
      action: Look for spec-{spec_id}.md in current feature directory
      validation: Confirm file exists and is readable

    no_id_provided:
      condition: No argument provided
      action: Find the most recent specification in current feature
      fallback: Search across all feature directories if needed
      priority: Use current feature, then scan all features

  file_discovery:
    - Use Glob tool to safely find specification files
    - Validate file naming patterns (spec-###.md)
    - Confirm file permissions and accessibility
    - Build specification inventory for selection
```

### Step 2: Specification File Validation

**Comprehensive specification analysis:**
```yaml
specification_validation:
  content_examination:
    structure_validation:
      - Use Read tool to examine the specification content
      - Check markdown formatting and structure
      - Validate YAML frontmatter if present

    required_sections_check:
      requirements_section:
        requirement: Clear problem and solution definition
        validation: Section exists with comprehensive requirements

      user_stories_section:
        requirement: Given-When-Then format scenarios
        validation: Stories present with proper format

      acceptance_criteria_section:
        requirement: Testable completion conditions
        validation: Criteria defined and measurable

      technical_specification_section:
        requirement: Implementation constraints and approach
        validation: Technical details present and actionable

    issue_identification:
      - Report any structural issues that need addressing
      - Identify missing sections or incomplete content
      - Flag formatting or organization problems
      - Provide specific recommendations for fixes
```

### Step 3: Clarification Marker Discovery

**Systematic marker identification:**
```yaml
clarification_discovery:
  pattern_search:
    - Use Grep tool to search for [NEEDS CLARIFICATION:...] patterns
    - Extract full marker content including question text
    - Count total clarifications needed
    - Build clarification inventory with metadata

  marker_analysis:
    question_extraction:
      - Parse each marker to extract specific questions
      - Identify question types (technical, business, design, etc.)
      - Categorize clarifications by complexity and impact

    context_mapping:
      - Map each clarification to specification section
      - Identify related requirements or user stories
      - Determine clarification dependencies and priorities

  summary_reporting:
    - Display total count of clarifications needed
    - Show breakdown by question type and complexity
    - If none found, report specification is complete
    - Provide detailed summary of clarifications to resolve
```

### Step 4: Interactive Clarification Resolution

**Interactive question processing:**
```yaml
interactive_resolution:
  clarification_loop:
    for_each_clarification:
      context_extraction:
        - Use Read tool to get surrounding context (±200 characters)
        - Extract related specification content
        - Identify relevant requirements or user stories
        - Display context with highlighted question

      question_presentation:
        format: |
          ============================================================
          📍 Clarification {current}/{total}
          ============================================================
          📋 Context:
          {extracted_context_with_highlighted_question}

          ❓ Question: {extracted_question}
          💡 Please provide your answer:

      user_interaction:
        wait_for_input:
          - WAIT for user input (interactive prompt)
          - Accept and process user's answer
          - Validate answer completeness and relevance

        response_processing:
          user_provides_answer:
            action: Use Edit tool to replace marker with resolved format
            format: ✅ **CLARIFIED**: [user_answer]
            validation: Confirm replacement was successful

          no_answer_provided:
            action: Skip current clarification
            reasoning: Allow user to skip difficult questions
            continuation: Move to next clarification

      progress_tracking:
        - Update clarification completion status
        - Track remaining clarifications
        - Provide progress feedback to user

  completion_detection:
    - Loop continues until all clarifications processed
    - Detect when no more markers remain
    - Confirm successful resolution of all processed items
```

### Step 5: Specification File Update

**Atomic specification modification:**
```yaml
specification_update:
  update_operations:
    content_modification:
      - Use Edit tool to update specification with resolved clarifications
      - Ensure all changes are properly formatted
      - Maintain markdown structure and readability
      - Preserve original content context

    format_validation:
      - Verify resolved clarifications use consistent format
      - Check markdown syntax and structure integrity
      - Ensure proper section organization

  success_validation:
    file_integrity:
      - Validate file was updated successfully
      - Confirm all intended changes were applied
      - Check file permissions and accessibility
      - Verify no corruption occurred during update

    change_verification:
      - Use Grep tool to confirm no clarification markers remain
      - Validate replacement format consistency
      - Check for unintended side effects
```

### Step 6: Updated Specification Validation

**Comprehensive validation process:**
```yaml
updated_spec_validation:
  marker_verification:
    - Use Grep tool to confirm no clarification markers remain
    - Scan for any remaining [NEEDS CLARIFICATION] patterns
    - Validate all markers were properly resolved

  sdd_compliance_analysis:
    manual_compliance_checks:
      requirements_documentation:
        requirement: Clear requirements documented
        validation: Requirements section complete and actionable
        status: ✅/❌

      user_stories_defined:
        requirement: User stories properly defined
        validation: Stories present with Given-When-Then format
        status: ✅/❌

      acceptance_criteria_valid:
        requirement: Acceptance criteria are testable
        validation: Criteria measurable and verifiable
        status: ✅/❌

      technical_specification_present:
        requirement: Technical specification included
        validation: Implementation details provided
        status: ✅/❌

      success_metrics_defined:
        requirement: Success metrics established
        validation: Measurable completion criteria defined
        status: ✅/❌

    compliance_calculation:
      - Calculate SDD compliance percentage
      - Count total sections meeting standards
      - Identify areas needing improvement
      - Generate compliance score and recommendations

  quality_assessment:
    - Report overall specification quality
    - Identify strengths and areas for improvement
    - Provide specific recommendations for enhancement
    - Validate readiness for implementation planning
```

### Step 7: Next Steps Generation

**Contextual workflow guidance:**
```yaml
next_steps_generation:
  basic_workflow_guidance:
    display_information:
      - Display updated specification file path
      - Show specification location and accessibility
      - Provide file reference for further work

    recommended_commands:
      implementation_planning:
        command: /sp-plan
        description: Generate implementation plan from clarified specification
        timing: After clarification completion

      task_breakdown:
        command: /sp-task
        description: Create task breakdown for implementation
        timing: After planning phase

      status_checking:
        command: /sp-status
        description: Check overall project status
        timing: Any time for progress tracking

  context_suggestions:
    content_based_recommendations:
      authentication_detected:
        trigger: "authentication" found in specification
        recommendation: /sp-decompose
        reasoning: Authentication features benefit from microservice decomposition

      api_detected:
        trigger: "api" found in specification
        recommendation: /sp-test
        reasoning: API development requires comprehensive testing strategy

      database_detected:
        trigger: "database" found in specification
        recommendation: Migration planning
        reasoning: Database changes need careful migration planning

      microservice_indicators:
        trigger: "service" or "distributed" found
        recommendation: Advanced architectural planning
        reasoning: Distributed systems require specialized approaches

  implementation_readiness:
    readiness_assessment:
      - Evaluate specification completeness
      - Check technical detail sufficiency
      - Validate requirements clarity
      - Assess overall implementation readiness

    barrier_identification:
      - Identify remaining blockers or uncertainties
      - Highlight areas needing additional detail
      - Provide specific recommendations for resolution
```

## Output Format

**Clarification completion response:**
```yaml
clarification_results:
  status: "success"
  specification_id: "001"
  specification_file: ".specpulse/specs/001-user-authentication/spec-001.md"

  clarification_summary:
    total_found: 4
    total_resolved: 4
    success_rate: "100%"

  validation_results:
    markers_remaining: 0
    sdd_compliance:
      requirements_documentation: "✅ Complete"
      user_stories_defined: "✅ Complete"
      acceptance_criteria_valid: "✅ Complete"
      technical_specification_present: "✅ Complete"
      success_metrics_defined: "✅ Complete"
    overall_compliance: "100%"
    overall_quality: "Excellent"

  next_steps:
    immediate:
      - "Review updated specification: .specpulse/specs/001-user-authentication/spec-001.md"
      - "Generate implementation plan: /sp-plan"
      - "Create task breakdown: /sp-task"

    contextual:
      based_on_content: "authentication"
      recommendation: "Consider microservice decomposition: /sp-decompose"
      reasoning: "Authentication features may benefit from service separation"

  user_engagement:
    interaction_type: "interactive"
    questions_presented: 4
    answers_provided: 4
    completion_time: "8 minutes"
```

## Error Handling and Recovery

**Comprehensive error scenarios:**
```yaml
error_handling:
  specification_errors:
    no_spec_found:
      action: Guide user to create specification with /sp-spec
      recovery: Provide specification creation guidance and templates

    file_access_errors:
      action: Provide troubleshooting steps for permission issues
      recovery: Suggest alternative file locations or permission fixes

    corruption_detected:
      action: Report file corruption and suggest recovery
      recovery: Recommend backup restoration or file recreation

  clarification_errors:
    no_clarifications_found:
      action: Report specification is already complete
      recovery: Suggest validation or next workflow steps

    empty_answers:
      action: Allow user to skip or retry difficult questions
      recovery: Continue with next clarification or provide alternative approaches

    partial_completion:
      action: Save progress and enable resumption
      recovery: Allow command restart from same point

  validation_errors:
    sdd_compliance_failures:
      action: Provide specific recommendations for improvement
      recovery: Offer templates and guidance for missing sections

    quality_issues:
      action: Identify specific quality problems
      recovery: Provide enhancement suggestions and best practices
```

## Safety Constraints

- **Path validation**: Only operate within `.specpulse/` directory
- **Protected directories**: Never modify `templates/`, `specpulse/`, AI configs
- **Atomic operations**: Prevent partial updates and corruption
- **Rollback capability**: Restore original content on failures
- **Input validation**: Comprehensive sanitization of user inputs
- **Interactive safety**: Validate user responses before applying changes

## Integration Features

- **Interactive Engagement**: Context-aware question processing
- **SDD Compliance Validation**: Comprehensive specification standards validation
- **Context-Aware Suggestions**: Smart next-step recommendations
- **Progress Tracking**: Complete clarification resolution monitoring
- **Quality Assurance**: Enhanced validation and quality scoring
- **Workflow Integration**: Seamless transition to planning and implementation phases