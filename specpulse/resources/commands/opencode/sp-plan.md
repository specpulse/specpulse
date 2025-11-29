---
name: sp-plan
description: Generate and manage implementation plans without SpecPulse CLI
version: "1.0"
agent: specpulse-assistant
workflow_type: plan_management
---

# SpecPulse Plan Management Workflow

This workflow implements complete CLI-independent implementation plan creation and management with intelligent planning algorithms.

## Agent Capabilities Required

- File operations: Read, Write, Edit, Bash, Glob, TodoWrite
- Directory traversal protection
- Atomic file operation handling
- Specification analysis and dependency mapping
- Optimization algorithms and risk assessment
- Error recovery and rollback mechanisms

## Workflow Steps

### Step 1: Argument Parsing and Action Determination

**Parse input arguments:**
```yaml
inputs:
  action: enum [generate, validate, optimize]
  feature_directory: string
```

**Action logic:**
- Parse the command arguments:
  - If first argument is generate, validate, or optimize → Use that action
  - If no action specified → Default to generate
  - For other arguments → Look for feature name or use current feature

### Step 2: Current Feature Context Detection

**Feature context algorithm:**
1. Check `.specpulse/memory/context.md` for active feature
2. Look for most recently modified spec/plan/task directory
3. Validate feature directory exists and is properly structured
4. Extract feature ID and name from directory structure
5. Set working context for subsequent operations

### Step 3: Plan Generation (Action: generate)

**Specification Analysis:**
```yaml
analysis_process:
  specification_reading:
    - Read specification files from .specpulse/specs/[feature]/
    - Parse functional requirements and user stories
    - Extract technical constraints and dependencies
    - Identify complexity and risk factors

  decomposition_support:
    - Check for .specpulse/specs/[feature]/decomposition/ directory
    - Identify service directories if decomposition exists
    - Plan service-specific implementation strategies
    - Generate service-dependent task breakdowns
```

**Plan Structure Design:**
```yaml
plan_components:
  implementation_strategy:
    description: High-level approach and methodology
    elements: [Architecture, Technology stack, Development methodology]

  phase_breakdown:
    structure: Structured implementation phases (Phase 0-4)
    phases:
      - Phase 0: Setup and Foundation
      - Phase 1: Core Implementation
      - Phase 2: Feature Integration
      - Phase 3: Testing and Validation
      - Phase 4: Deployment and Documentation

  task_dependencies:
    mapping: Dependency mapping and critical path identification
    analysis: Critical path, bottlenecks, parallel opportunities

  resource_requirements:
    tools: Development tools and libraries
    external: External dependencies and services
    human: Skill requirements and team composition

  timeline_estimates:
    methodology: Realistic timeframes for each phase
    factors: Complexity, dependencies, team size

  risk_mitigation:
    identification: Implementation risks and mitigation strategies
    categories: [Technical, Resource, Timeline, External dependencies]
```

**Service-Specific Planning (if decomposed):**
```yaml
service_planning:
  for_each_service:
    service_implementation_plan: Service-specific approach
    service_dependencies: Inter-service communication patterns
    integration_strategy: How services will work together
    data_flow: Information flow between services
    api_contracts: Service interface definitions

  integration_planning:
    orchestration_strategy: Service deployment and management
    communication_protocols: REST, GraphQL, message queues
    data_consistency: Transaction management and data sync
    monitoring: Service health and performance monitoring
```

**Universal ID System Implementation:**
```yaml
plan_id_generation:
  scan_directory: ".specpulse/plans/[feature]/"
  file_pattern: "plan-(\\d+)\\.md"
  algorithm: |
    1. Use Glob tool to scan directory
    2. Parse existing plan files using regex plan-(\d+)\.md pattern
    3. Extract all numbers and convert to integers for comparison
    4. Find maximum value: max_num = max(extracted_numbers) or 0 if empty
    5. Generate next sequential: next_num = max_num + 1
    6. Zero-pad: f"plan-{next_num:03d}.md" → plan-001.md, plan-002.md

service_specific_planning:
  service_plan_patterns:
    - auth-service-plan.md
    - user-service-plan.md
    - integration-plan.md
    - api-gateway-plan.md

  cross_service_coordination:
    - Maintain global coordination to prevent conflicts
    - Ensure service dependencies are properly mapped
    - Validate integration points and contracts
```

### Step 4: Plan Validation (Action: validate)

**File Structure Validation:**
```yaml
structure_validation:
  file_existence:
    - Verify plan files exist in .specpulse/plans/[feature]/
    - Check file naming follows plan-[###].md pattern
    - Validate plan file format and readability
    - Ensure proper markdown structure

  directory_validation:
    - Confirm proper directory hierarchy
    - Validate directory permissions
    - Check for required subdirectories
```

**Content Completeness Validation:**
```yaml
content_validation:
  required_sections:
    implementation_strategy:
      requirement: Clear and comprehensive approach
      validation: Strategy is well-defined and achievable

    phase_breakdown:
      requirement: Properly structured implementation phases
      validation: All phases have clear objectives and deliverables

    task_dependencies:
      requirement: Logical dependency mapping
      validation: Dependencies are realistic and properly sequenced

    resource_requirements:
      requirement: Complete tool and library lists
      validation: Resources are available and appropriate

    timeline_estimates:
      requirement: Realistic and justified timeframes
      validation: Estimates account for complexity and dependencies

    risk_mitigation:
      requirement: Comprehensive risk identification and mitigation
      validation: Risks are identified with actionable mitigation strategies
```

**Technical Feasibility Validation:**
```yaml
feasibility_analysis:
  complexity_assessment:
    - Assess implementation approach complexity
    - Validate technical approach is sound
    - Check for potential technical bottlenecks

  dependency_validation:
    - Validate dependency relationships are logical
    - Check for circular dependencies
    - Verify external dependencies are available

  timeline_validation:
    - Check timeline estimates are achievable
    - Validate resource allocation is realistic
    - Identify potential timeline risks
```

### Step 5: Plan Optimization (Action: optimize)

**Plan Analysis:**
```yaml
analysis_process:
  current_state_assessment:
    - Read and analyze existing plan files
    - Identify complexity issues and optimization opportunities
    - Assess current phase breakdown effectiveness
    - Evaluate dependency management efficiency

  optimization_identification:
    - Phase consolidation opportunities
    - Dependency optimization possibilities
    - Timeline improvement potential
    - Resource optimization options
```

**Optimization Strategies:**
```yaml
optimization_techniques:
  phase_consolidation:
    description: Merge related phases where possible
    benefits: Reduced overhead, improved flow
    risks: Increased complexity per phase

  dependency_optimization:
    description: Reorganize dependencies for parallel execution
    benefits: Reduced timeline, better resource utilization
    risks: Coordination complexity

  timeline_optimization:
    description: Adjust estimates based on complexity analysis
    benefits: More realistic planning
    risks: External dependencies

  resource_optimization:
    description: Suggest better tool or library choices
    benefits: Improved efficiency, reduced costs
    risks: Learning curve, compatibility issues
```

**Risk Assessment Updates:**
```yaml
risk_update_process:
  strategy_refresh:
    - Update risk mitigation strategies
    - Identify new optimization-related risks
    - Provide contingency planning recommendations

  risk_monitoring:
    - Continuous risk assessment process
    - Early warning indicators
    - Risk response procedures
```

### Step 6: SDD Gates Compliance

**Compliance validation:**
```yaml
sdd_gates:
  specification_first:
    requirement: Plan directly derived from specifications
    validation: Every plan element can be traced to specification requirements

  task_decomposition:
    requirement: Plan includes detailed task breakdown
    validation: Implementation phases are broken down into specific, actionable tasks

  quality_assurance:
    requirement: Testing and validation strategies included
    validation: Quality gates and testing procedures are defined for each phase

  traceable_implementation:
    requirement: Clear link from requirements to implementation
    validation: Bidirectional traceability between requirements and plan elements
```

## Output Format

**Success response:**
```yaml
plan:
  id: "001"
  feature_id: "002"
  file_path: ".specpulse/plans/002-payment-processing/plan-001.md"
  status: "created"
  created_at: "2025-01-11T16:30:00Z"

analysis:
  project_type: "API Service with payment gateway integration"
  complexity: "Standard (single service with external dependencies)"
  implementation_strategy: "Monolithic with future microservices migration"
  estimated_timeline: "3 weeks"

structure:
  phases: 5
  dependencies_mapped: 12
  resources_identified: 8
  risks_assessed: 6

validation_results:
  content_completeness: 100%
  technical_feasibility: 95%
  sdd_gates_compliance: true
  optimization_score: 88%

next_steps:
  - "Create task breakdown: /sp-task"
  - "Begin implementation: /sp-execute"
  - "Monitor progress: /sp-status"
```

## Error Handling and Recovery

**Comprehensive error scenarios:**
```yaml
error_handling:
  context_errors:
    no_active_feature:
      action: Prompt to run /sp-pulse first
      recovery: Guide through feature initialization

    missing_specifications:
      action: Guide user to create specifications first
      recovery: Provide specification creation assistance

  analysis_errors:
    vague_requirements:
      action: Ask clarifying questions
      recovery: Facilitate requirement refinement process

    conflicting_requirements:
      action: Identify and request resolution
      recovery: Provide requirement reconciliation guidance

  generation_errors:
    template_missing:
      action: Create comprehensive plan structure manually
      recovery: Use built-in plan template system

    decomposition_complexity:
      action: Break down into manageable sections
      recovery: Provide step-by-step planning assistance

  validation_errors:
    invalid_structure:
      action: Provide template corrections
      recovery: Guide through structure repair process

    unrealistic_timeline:
      action: Offer timeline adjustment recommendations
      recovery: Provide realistic planning methodology
```

## Safety Constraints

- **Path validation**: Only operate within `.specpulse/` directory
- **Protected directories**: Never modify `templates/`, `specpulse/`, AI configs
- **Atomic operations**: Prevent partial updates and corruption
- **Rollback capability**: Restore original state on failures
- **Input validation**: Comprehensive sanitization of all inputs

## Integration Features

- **Specification Integration**: Direct analysis and mapping from specifications
- **Decomposition Support**: Service-specific planning for microservices
- **Cross-Plan Dependencies**: Track dependencies between multiple features
- **Progress Integration**: Link plan phases to task completion
- **Template System**: Consistent plan structure and quality standards
- **Optimization Engine**: Continuous plan improvement algorithms