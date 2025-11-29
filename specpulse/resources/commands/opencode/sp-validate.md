---
name: sp-validate
description: Validate specifications, plans, tasks, and tests without SpecPulse CLI
version: "1.0"
agent: specpulse-assistant
workflow_type: validation_engine
---

# SpecPulse Validation Engine Workflow

This workflow implements comprehensive CLI-independent validation of all project components with quality metrics and SDD Gates compliance.

## Agent Capabilities Required

- File operations: Read, Bash, TodoWrite, Grep, Edit (read-only)
- Directory traversal protection
- Atomic file operation handling
- Quality analysis algorithms
- SDD Gates compliance validation
- Cross-component consistency analysis
- Requirements traceability validation
- Error recovery and reporting

## Workflow Steps

### Step 1: Argument Parsing and Validation Scope Determination

**Parse input arguments:**
```yaml
inputs:
  target: enum [spec, plan, task, test, all]
  feature_name: string
  options:
    fix: boolean
    verbose: boolean
    strict: boolean
```

**Validation scopes:**
```yaml
scope_definitions:
  spec:
    description: Specification structure, content quality, SDD compliance
    validation_areas:
      - File structure and naming conventions
      - Required section completeness
      - Content quality and clarity
      - SDD Gates compliance assessment

  plan:
    description: Implementation plan feasibility and completeness
    validation_areas:
      - Plan file structure and formatting
      - Implementation strategy completeness
      - Technical feasibility assessment
      - Timeline and resource validation

  task:
    description: Task structure, dependencies, quality validation
    validation_areas:
      - Task file structure and organization
      - Task metadata completeness
      - Dependency chain validation
      - Quality and risk assessment

  test:
    description: Test coverage, requirements traceability, quality
    validation_areas:
      - Test file structure and organization
      - Test coverage and completeness
      - Requirements traceability validation
      - Test quality and documentation

  all:
    description: Comprehensive validation across all components
    validation_areas:
      - Cross-component consistency analysis
      - End-to-end requirements traceability
      - Overall project quality assessment
      - SDD Gates compliance evaluation
```

### Step 2: Current Feature Context Detection

**Feature context algorithm:**
1. Check `.specpulse/memory/context.md` for active feature
2. Look for most recently modified spec/plan/task directory
3. Validate feature directory exists and is properly structured
4. Extract feature ID and name from directory structure
5. Set working context for subsequent operations

### Step 3: Specification Validation

**Comprehensive specification analysis:**
```yaml
specification_validation:
  file_structure_validation:
    discovery:
      - Scan .specpulse/specs/[feature]/ for specification files
      - Verify file naming follows spec-[###].md pattern
      - Validate file permissions and readability
      - Ensure proper markdown formatting and structure

    integrity_checks:
      - Verify YAML frontmatter completeness
      - Validate markdown syntax and structure
      - Check for file corruption or encoding issues
      - Ensure directory organization compliance

  content_structure_validation:
    required_sections:
      executive_summary:
        requirement: Problem statement and solution overview
        validation: Clear description of what and why

      functional_requirements:
        requirement: Detailed feature specifications
        validation: Specific, measurable, actionable requirements

      user_stories:
        requirement: Given-When-Then format scenarios
        validation: Complete user journey coverage

      acceptance_criteria:
        requirement: Testable completion conditions
        validation: Measurable, verifiable success conditions

      technical_constraints:
        requirement: Performance and security requirements
        validation: Specific, achievable technical limitations

      non_functional_requirements:
        requirement: Usability and maintainability
        validation: Quality attributes and operational characteristics

      risk_assessment:
        requirement: Potential risks and mitigation strategies
        validation: Comprehensive risk identification and planning

  content_quality_validation:
    clarity_analysis:
      - Count and analyze [NEEDS CLARIFICATION] markers
      - Verify Given-When-Then format in user stories
      - Check for ambiguous or vague language
      - Assess requirement specificity and measurability

    testability_assessment:
      - Verify acceptance criteria are measurable and testable
      - Check success criteria can be objectively verified
      - Validate testing requirements are comprehensive
      - Assess edge case coverage

    feasibility_evaluation:
      - Validate technical constraints are specific and achievable
      - Assess resource requirements are realistic
      - Check timeline expectations are reasonable
      - Evaluate risk assessment completeness

  sdd_gates_compliance:
    specification_first:
      validation:
        - Verify requirements precede implementation
        - Check no implementation details in specifications
        - Validate requirement completeness before planning

    traceable:
      validation:
        - Ensure each requirement maps to user stories
        - Verify user story coverage of all requirements
        - Check acceptance criteria link to requirements

    testable:
      validation:
        - Confirm acceptance criteria can be verified
        - Verify testing requirements are defined
        - Check validation methods are appropriate

    complete:
      validation:
        - Check all necessary sections for implementation
        - Verify requirement coverage is comprehensive
        - Assess specification completeness for development
```

### Step 4: Plan Validation

**Implementation plan analysis:**
```yaml
plan_validation:
  file_structure_validation:
    discovery:
      - Scan .specpulse/plans/[feature]/ for plan files
      - Verify file naming follows plan-[###].md pattern
      - Validate plan file format and readability
      - Ensure proper markdown structure

    organization_checks:
      - Verify phase organization and structure
      - Check task dependency mapping
      - Validate timeline presentation format
      - Ensure resource documentation completeness

  content_completeness_validation:
    strategy_validation:
      implementation_strategy:
        requirement: High-level approach and methodology
        validation: Clear, comprehensive development approach

      phase_breakdown:
        requirement: Structured implementation phases
        validation: Logical phase sequencing and dependencies

      task_dependencies:
        requirement: Dependency mapping and critical path
        validation: Complete dependency graph and critical path analysis

      resource_requirements:
        requirement: Tools, libraries, and external dependencies
        validation: Comprehensive resource identification and planning

      timeline_estimates:
        requirement: Realistic timeframes for each phase
        validation: Justified timeline estimates with risk buffers

      risk_mitigation:
        requirement: Implementation risks and mitigation strategies
        validation: Comprehensive risk identification and mitigation

  technical_feasibility_validation:
    approach_assessment:
      complexity_analysis:
        - Assess implementation approach complexity
        - Validate technical approach soundness
        - Check for architectural consistency

      dependency_validation:
        - Validate dependency relationships are logical
        - Check for circular dependencies
        - Verify critical path accuracy

      timeline_validation:
        - Check timeline estimates are realistic
        - Validate resource allocation adequacy
        - Assess milestone achievability

      resource_validation:
        - Verify resource requirements are achievable
        - Check tool and library availability
        - Assess skill requirement feasibility

    bottleneck_identification:
      - Identify potential implementation bottlenecks
      - Assess resource constraint impacts
      - Evaluate timeline risk factors
```

### Step 5: Task Validation

**Comprehensive task analysis:**
```yaml
task_validation:
  file_structure_validation:
    discovery:
      - Scan .specpulse/tasks/[feature]/ for task files
      - Verify file naming follows task patterns (tasks-*.md, *-tasks.md)
      - Validate task file permissions and format
      - Ensure proper YAML frontmatter structure

    organization_checks:
      - Verify task grouping and categorization
      - Check service-specific task organization
      - Validate task ID uniqueness and formatting
      - Ensure task metadata completeness

  task_structure_validation:
    required_fields_validation:
      task_id:
        requirement: Unique identifier with proper formatting
        validation: Unique, sequential, properly formatted

      title:
        requirement: Clear, actionable task description
        validation: Specific, measurable, achievable description

      status:
        requirement: Valid status (todo, in-progress, blocked, done)
        validation: Proper status tracking and transitions

      description:
        requirement: Detailed implementation guidance
        validation: Clear, complete implementation instructions

      files_touched:
        requirement: List of files to be modified
        validation: Comprehensive file impact assessment

      success_criteria:
        requirement: Testable completion conditions
        validation: Measurable, verifiable success conditions

      dependencies:
        requirement: List of prerequisite tasks
        validation: Valid dependency references

      risk_assessment:
        requirement: Risk level and mitigation notes
        validation: Appropriate risk identification and planning

  task_quality_validation:
    implementation_guidance:
      - Check task descriptions provide clear implementation guidance
      - Verify sufficient detail for independent execution
      - Assess technical accuracy of implementation approach
      - Validate completeness of implementation instructions

    success_criteria_validation:
      - Verify success criteria are specific and measurable
      - Check criteria can be objectively verified
      - Assess success condition completeness
      - Validate testing requirements are defined

    risk_assessment_validation:
      - Assess risk levels match task complexity
      - Verify mitigation strategies are appropriate
      - Check risk identification completeness
      - Validate contingency planning

  dependency_validation:
    reference_validation:
      - Verify all referenced task IDs exist
      - Check for circular dependencies
      - Validate dependency chain completeness
      - Ensure dependency accuracy and relevance

    chain_analysis:
      - Validate critical path identification
      - Assess parallel task availability
      - Check dependency chain optimization
      - Verify sequential chain logic

    consistency_checks:
      - Ensure dependency consistency across tasks
      - Validate dependency relationship reciprocity
      - Check for dependency conflicts or overlaps
```

### Step 6: Test Validation

**Comprehensive test analysis:**
```yaml
test_validation:
  file_discovery:
    test_location:
      - Locate test files in tests/features/[feature]/ directory
      - Check for proper test_*.py naming convention
      - Validate test file structure and imports
      - Ensure test files are executable and accessible

    organization_analysis:
      - Verify test file organization and grouping
      - Check test suite structure and hierarchy
      - Validate test naming conventions
      - Ensure test documentation completeness

  test_content_validation:
    structure_validation:
      proper_imports:
        requirement: pytest, unittest, or other testing framework
        validation: Correct import statements and framework usage

      test_functions:
        requirement: Adequate test function coverage
        validation: Comprehensive test function organization

      test_quality:
        requirement: Clear assertions and edge case handling
        validation: Robust test implementation with error handling

      test_documentation:
        requirement: Descriptive test names and docstrings
        validation: Clear test documentation and comments

  requirements_traceability:
    mapping_validation:
      - Map test files to specification requirements
      - Verify user story test coverage
      - Check acceptance criteria test implementation
      - Identify gaps in test coverage

    coverage_analysis:
      user_story_coverage:
        requirement: Complete user story testing
        validation: All user stories have corresponding tests

      acceptance_criteria_coverage:
        requirement: Complete acceptance criteria testing
        validation: All acceptance criteria have test coverage

      edge_case_coverage:
        requirement: Critical paths and edge cases tested
        validation: Comprehensive edge case and error testing

      integration_coverage:
        requirement: Component integration tested
        validation: Integration points and interfaces tested
```

### Step 7: Comprehensive Validation (All)

**Cross-component analysis:**
```yaml
comprehensive_validation:
  cross_component_consistency:
    specification_plan_alignment:
      - Verify specifications link to plans and tasks
      - Check task traceability to requirements
      - Validate plan completeness for specifications
      - Assess implementation plan alignment

    task_specification_traceability:
      - Ensure all tasks link to specification requirements
      - Verify requirement coverage in task breakdown
      - Check task completeness for specification coverage
      - Validate task-specification consistency

    test_requirement_coverage:
      - Validate test coverage of specifications
      - Verify user story test implementation
      - Check acceptance criteria test coverage
      - Assess end-to-end testing completeness

  quality_metrics_calculation:
    specification_completeness:
      calculation: Percentage of required sections present
      factors: Structure, content, clarity, completeness

    plan_feasibility:
      assessment: Implementation approach complexity and achievability
      factors: Technical feasibility, resource requirements, timeline realism

    task_quality:
      evaluation: Task structure and dependency validation
      factors: Completeness, clarity, dependency accuracy, risk assessment

    test_coverage:
      analysis: Requirements traceability and test completeness
      factors: User story coverage, acceptance criteria coverage, edge case testing

    sdd_compliance:
      assessment: Overall Specification-Driven Development adherence
      factors: Specification first, traceable, testable, complete

  recommendations_generation:
    critical_issues:
      identification: Must-fix items blocking implementation
      prioritization: Impact assessment and urgency ranking
      action_items: Specific resolution steps and guidance

    quality_improvements:
      opportunities: Enhancements for better development experience
      recommendations: Best practices and optimization suggestions
      implementation: Step-by-step improvement guidance

    missing_elements:
      gaps: Components that need to be added
      completion: Requirements for full coverage
      templates: Standardized components and templates

    optimization_opportunities:
      improvements: Areas for improvement and refinement
      efficiencies: Process and workflow optimizations
      enhancements: Quality and effectiveness improvements
```

## Output Format

**Validation response:**
```yaml
validation_results:
  target: "all"
  feature_id: "001"
  feature_name: "user-authentication"
  overall_quality_score: "91%"

  component_summary:
    specifications:
      score: "93%"
      files_analyzed: 2
      status: "excellent"
      issues: 1

    plans:
      score: "85%"
      files_analyzed: 1
      status: "good"
      issues: 2

    tasks:
      score: "88%"
      files_analyzed: 1
      tasks_analyzed: 25
      status: "good"
      issues: 3

    tests:
      score: "90%"
      files_analyzed: 3
      test_functions: 26
      status: "excellent"
      issues: 2

  sdd_gates_compliance:
    specification_first: "100%"
    traceable: "95%"
    testable: "92%"
    complete: "89%"
    overall_compliance: "94%"

  issues_summary:
    critical: 0
    major: 2
    minor: 6

  recommendations:
    priority_actions:
      - "Complete risk assessment in specifications and tasks"
      - "Add missing test coverage for 2 acceptance criteria"

    quality_improvements:
      - "Enhance plan risk mitigation strategies"
      - "Clarify success criteria for complex tasks"

  readiness_assessment:
    status: "ready_for_implementation"
    confidence: "high"
    blocking_issues: 0
    estimated_completion: "with_minor_improvements"
```

## Error Handling and Recovery

**Comprehensive error scenarios:**
```yaml
error_handling:
  file_structure_problems:
    missing_directories:
      action: Guide user through creating proper structure
      recovery: Provide directory creation commands and templates

    file_permission_errors:
      action: Provide permission fix instructions
      recovery: Offer specific commands for permission restoration

    invalid_file_formats:
      action: Offer template corrections
      recovery: Provide format standardization guidance

    corrupted_files:
      action: Suggest recovery procedures
      recovery: Recommend backup restoration or file recreation

  content_quality_issues:
    missing_required_sections:
      action: Provide section templates
      recovery: Offer complete section structure guidance

    vague_requirements:
      action: Guide through clarification process
      recovery: Provide requirement refinement methodology

    untestable_criteria:
      action: Help refine acceptance criteria
      recovery: Offer testable criteria formulation guidance

    complex_dependencies:
      action: Suggest dependency simplification
      recovery: Provide dependency optimization strategies

  validation_process_errors:
    memory_constraints:
      action: Process files in batches
      recovery: Implement chunked validation approach

    time_limits:
      action: Prioritize critical validations
      recovery: Focus on high-impact validation areas

    access_restrictions:
      action: Provide alternative validation approaches
      recovery: Offer read-only validation methods

    system_errors:
      action: Implement retry mechanisms
      recovery: Provide error recovery and restart procedures
```

## Safety Constraints

- **Path validation**: Only operate within `.specpulse/` directory
- **Protected directories**: Never modify `templates/`, `specpulse/`, AI configs
- **Read-only operations**: Validation does not modify any files
- **Input validation**: Comprehensive sanitization of all inputs
- **Error containment**: Isolate validation errors from project files

## Integration Features

- **Quality Metrics**: Objective scoring and assessment algorithms
- **SDD Gates Compliance**: Complete specification-driven validation
- **Cross-Component Analysis**: End-to-end consistency validation
- **Requirements Traceability**: Complete coverage validation
- **Risk Assessment**: Comprehensive issue identification and mitigation
- **Continuous Improvement**: Actionable recommendations and best practices