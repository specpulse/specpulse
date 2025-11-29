---
name: sp-task
description: Create and manage tasks without SpecPulse CLI
version: "1.0"
agent: specpulse-assistant
workflow_type: task_management
---

# SpecPulse Task Management Workflow

This workflow implements complete CLI-independent task lifecycle management with service-specific organization and comprehensive analytics.

## Agent Capabilities Required

- File operations: Read, Write, Edit, Bash, Glob, TodoWrite
- Directory traversal protection
- Atomic file operation handling
- Service decomposition analysis
- Dependency mapping and validation
- Progress analytics and calculation
- Error recovery and rollback mechanisms

## Workflow Steps

### Step 1: Current Feature Context Detection

**Feature context algorithm:**
1. Check `.specpulse/memory/context.md` for active feature
2. Look for most recently modified spec/plan/task directory
3. Validate feature directory exists and is properly structured
4. Extract feature ID and name from directory structure
5. Set working context for subsequent operations

### Step 2: Argument Parsing and Action Determination

**Parse input arguments:**
```yaml
inputs:
  action: enum [breakdown, update, status, execute, validate]
  feature_directory: string
  task_id: string
```

**Action logic:**
- Parse the command arguments:
  - If first argument is breakdown, update, status, execute, or validate → Use that action
  - If no action specified → Default to breakdown
  - For other arguments → Look for feature name or use current feature

### Step 3: Task Breakdown Generation (Action: breakdown)

**Service Decomposition Analysis:**
```yaml
decomposition_check:
  scan_directory: ".specpulse/specs/[feature]/decomposition/"
  service_identification:
    - Parse service directories for task categorization
    - Identify service boundaries and responsibilities
    - Map service dependencies and communication patterns

  service_planning:
    auth_service: "JWT, OAuth, password policies, session management"
    user_service: "Profiles, preferences, permissions, roles"
    api_gateway: "Rate limiting, authentication, routing, logging"
    database_service: "Schema management, migrations, backups"
    notification_service: "Email, SMS, push notifications, templates"
```

**Task Generation Process:**
```yaml
task_breakdown:
  plan_analysis:
    - Read implementation plan from .specpulse/plans/[feature]/ directory
    - Analyze plan phases and identify implementation steps
    - Create detailed tasks with proper dependencies

  task_metadata_generation:
    required_fields:
      - task_id: "Unique identifier with sequential numbering"
      - status: "Initially set to 'todo'"
      - title: "Clear, actionable task description"
      - description: "Detailed what, why, how, when explanation"
      - files_touched: "List of files that will be modified"
      - goals: "Specific objectives this task achieves"
      - success_criteria: "Testable completion conditions"
      - dependencies: "Tasks that must be completed first"
      - next_tasks: "Tasks that can start after this one"
      - risk_level: "Assessment of potential issues (low/medium/high)"
      - risk_notes: "Specific concerns and mitigation strategies"
      - moscow_analysis: "Must/Should/Know/Won't categorization"
      - priority: "Overall priority ranking with reasoning"
      - sdd_gates_compliance: "Specification-driven validation"
```

**Universal ID System Implementation:**
```yaml
task_id_generation:
  scan_directory: ".specpulse/tasks/[feature]/"
  file_patterns:
    global_tasks: "T(\\d+)\\.md"
    service_tasks: "([A-Z]+)-T(\\d+)\\.md"
    integration_tasks: "INT-T(\\d+)\\.md"

  algorithm: |
    1. Use Glob tool to scan directory
    2. Parse existing task files to extract current numbering
    3. Create numbering map: {task_type: max_number_used}
    4. Generate next ID: For each task type, use max_num + 1
    5. Zero-pad: format(next_num, '03d') ensures 001, 002, 003

  service_specific_patterns:
    authentication_service: "AUTH-T001.md", "AUTH-T002.md"
    user_management_service: "USER-T001.md", "USER-T002.md"
    api_gateway_service: "GATEWAY-T001.md", "GATEWAY-T002.md"
    database_service: "DB-T001.md", "DB-T002.md"
    notification_service: "NOTIF-T001.md", "NOTIF-T002.md"

  conflict_prevention:
    - Atomic file existence check before creating each task file
    - Validation loop: If conflict detected, increment and retry
    - Cross-service dependency tracking to ensure logical numbering
    - Fallback numbering: If directory empty, start from T001.md
    - Gap handling: Preserve existing numbering gaps, don't renumber
```

### Step 4: Task Management (Action: update)

**Task Update Workflow:**
```yaml
update_process:
  task_discovery:
    - Scan .specpulse/tasks/[feature]/ directory for task files
    - Display available task files for selection
    - Parse current task structure and status

  update_operations:
    status_updates:
      - Mark tasks as completed/in-progress/blocked
      - Update completion timestamps
      - Recalculate dependent task availability

    content_modifications:
      - Update task descriptions or metadata
      - Add new tasks or remove obsolete ones
      - Modify dependencies and relationships

  progress_recalculation:
    - Recalculate completion percentages
    - Update velocity metrics
    - Adjust estimated completion dates
```

### Step 5: Progress Tracking (Action: status)

**Comprehensive Analytics:**
```yaml
progress_analysis:
  completion_metrics:
    - Total tasks and completion percentage
    - Task status distribution (todo/in-progress/blocked/done)
    - Service-specific progress breakdown
    - SDD Gates compliance percentage

  velocity_calculation:
    - Tasks per day calculation
    - Completion rate trends
    - Estimated completion dates based on velocity
    - Productivity patterns and insights

  dependency_analysis:
    - Parallel task availability count
    - Sequential dependency chain mapping
    - Critical path identification
    - Bottleneck detection

  recommendations:
    - Next available tasks for execution
    - Dependency resolution paths
    - Resource allocation suggestions
    - Risk mitigation priorities
```

### Step 6: Task Execution (Action: execute)

**Execution Workflow:**
```yaml
execution_process:
  task_selection:
    - Allow task selection from available pending tasks
    - Validate task readiness and dependencies
    - Display task details before execution

  implementation:
    - Implement task requirements through code changes
    - Create or modify specified files
    - Follow task description and success criteria

  validation:
    - Test implementation when applicable
    - Verify success criteria are met
    - Validate no unintended side effects

  completion:
    - Mark task as completed automatically
    - Update dependent tasks' availability
    - Continue with next available task if requested
    - Update progress metrics and context
```

### Step 7: Task Validation (Action: validate)

**Comprehensive Validation:**
```yaml
validation_checks:
  structural_validation:
    - Validate task file structure and format
    - Check required fields are present and valid
    - Verify proper markdown formatting

  logical_validation:
    - Verify task dependencies exist and are valid
    - Check for circular dependencies
    - Validate dependency chains are logical

  quality_validation:
    - Validate SDD Gates compliance
    - Check for duplicate task IDs
    - Verify success criteria are testable
    - Assess risk levels and mitigation strategies

  reporting:
    - Report validation results with specific fixes needed
    - Provide remediation guidance for identified issues
    - Track validation history and improvements
```

### Step 8: SDD Gates Compliance

**Compliance validation:**
```yaml
sdd_gates:
  specification_traced:
    requirement: Links to specific requirements
    validation: Each task references specification sections

  task_decomposed:
    requirement: Complex work broken into manageable pieces
    validation: Tasks are atomic and actionable

  quality_assurance:
    requirement: Success criteria are testable
    validation: Success criteria can be objectively verified

  traceable_implementation:
    requirement: Clear link between tasks and code
    validation: File changes can be traced back to specific tasks
```

## Output Format

**Task breakdown response:**
```yaml
task_breakdown:
  feature_id: "002"
  feature_name: "auth-microservice"
  decomposition_found: true
  services_identified: 3

  tasks_created:
    auth_service:
      file: "auth-service-tasks.md"
      task_count: 8
      tasks:
        - id: "AUTH-T001"
          title: "Initialize auth service structure"
          status: "todo"
          dependencies: []
          priority: "high"
        - id: "AUTH-T002"
          title: "Implement JWT token handling"
          status: "todo"
          dependencies: ["AUTH-T001"]
          priority: "high"

    user_service:
      file: "user-service-tasks.md"
      task_count: 6
      tasks:
        - id: "USER-T001"
          title: "Initialize user service structure"
          status: "todo"
          dependencies: []
          priority: "high"

    integration:
      file: "integration-tasks.md"
      task_count: 4
      tasks:
        - id: "INT-T001"
          title: "Connect auth and user services"
          status: "todo"
          dependencies: ["AUTH-T001", "USER-T001"]
          priority: "medium"

  summary:
    total_tasks: 18
    parallel_tasks_available: 12
    sequential_chains: 3
    sdd_gates_compliant: true
    estimated_completion_days: 9
```

## Error Handling and Recovery

**Comprehensive error scenarios:**
```yaml
error_handling:
  context_errors:
    no_active_feature:
      action: Prompt to run /sp-pulse first
      recovery: Guide through feature initialization

    missing_plan_file:
      action: Guide user to create plan with /sp-plan
      recovery: Provide plan creation assistance

  task_generation_errors:
    invalid_plan_structure:
      action: Identify and fix structural issues
      recovery: Guide through plan repair process

    circular_dependencies:
      action: Detect and resolve dependency loops
      recovery: Provide dependency resolution strategies

  execution_errors:
    task_blockers:
      action: Identify dependencies and provide resolution paths
      recovery: Clear blocked tasks and suggest alternatives

    failed_implementations:
      action: Rollback changes and retry with different approach
      recovery: Provide alternative implementation strategies
```

## Safety Constraints

- **Path validation**: Only operate within `.specpulse/` directory
- **Protected directories**: Never modify `templates/`, `specpulse/`, AI configs
- **Atomic operations**: Prevent partial updates and corruption
- **Rollback capability**: Restore original state on failures
- **Input validation**: Comprehensive sanitization of all inputs

## Integration Features

- **Service Decomposition**: Automatic service boundary detection and task organization
- **Dependency Management**: Complex dependency mapping and validation
- **Progress Analytics**: Comprehensive metrics and velocity tracking
- **SDD Gates Compliance**: Full specification-driven task management
- **Universal ID System**: Conflict-free task numbering across all services
- **Execution Engine**: Automated task implementation with validation