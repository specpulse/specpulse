---
name: sp-execute
description: Execute tasks without SpecPulse CLI
version: "1.0"
agent: specpulse-assistant
workflow_type: task_execution
---

# SpecPulse Task Execution Workflow

This workflow implements complete CLI-independent task execution with atomic operations and comprehensive error recovery.

## Agent Capabilities Required

- File operations: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
- Directory traversal protection
- Atomic file operation handling
- Task parsing and dependency validation
- Implementation verification and testing
- Error recovery and rollback mechanisms

## Workflow Steps

### Step 1: Argument Parsing and Execution Mode Determination

**Parse input arguments:**
```yaml
inputs:
  execution_target: enum [task-id, all, next]
  task_identifier: string
```

**Execution modes:**
```yaml
execution_modes:
  all:
    description: Execute ALL pending tasks non-stop
    behavior: Find all pending tasks, execute in sequence without stopping

  next:
    description: Execute next pending task and continue
    behavior: Find first available task, execute, then continue to next

  specific_task:
    description: Execute specific task by ID
    behavior: Find task file T001.md or AUTH-T001.md, execute pending tasks in that file
```

### Step 2: Current Feature Context Detection

**Feature context algorithm:**
1. Use Read tool to examine `.specpulse/memory/context.md`
2. Look for `**Directory**:` field to identify current feature
3. If no context found, use Glob tool to find first feature with task files
4. Validate feature directory follows naming convention (XXX-feature-name)
5. Set `tasks_dir` to `.specpulse/tasks/[current-feature]`

### Step 3: Task File Loading and Analysis

**Task discovery process:**
```yaml
task_loading:
  file_discovery:
    - Use Glob tool to find all *.md files in tasks directory
    - Validate file naming patterns (T###.md, SERVICE-T###.md)
    - Filter out non-task files and directories

  content_analysis:
    - Use Read tool to examine each task file
    - Parse task status markers:
      - `[ ]` = Pending task (ready to execute)
      - `[>]` = In progress task (currently working on)
      - `[x]` = Completed task (done)
      - `[!]` = Blocked task (waiting for dependency)
    - Extract task metadata: title, description, dependencies, success criteria
    - Build task inventory with status and dependencies

  validation:
    - Validate task file structure and content
    - Check required fields are present
    - Verify task IDs follow proper naming conventions
    - Validate dependency references exist
```

### Step 4: Execution Order Determination

**Task selection algorithm:**
```yaml
execution_ordering:
  continuous_mode:
    - Find first pending task (`[ ]`)
    - Check if dependencies are completed
    - If dependencies not met, skip to next available task
    - Maintain execution queue with prioritized tasks

  service_task_handling:
    - Handle AUTH-T001, USER-T001 patterns
    - Respect service-specific dependencies
    - Consider integration tasks after service tasks complete
    - Validate cross-service dependencies

  specific_task_mode:
    - Validate the requested task exists
    - Check task is in pending state
    - Verify dependencies are completed
    - Prepare for single task execution
```

### Step 5: Task Implementation Execution

**Atomic execution process:**
```yaml
task_execution:
  pre_execution:
    status_update:
      - Use Edit tool to change task status from `[ ]` to `[>]` (in progress)
      - Add execution timestamp
      - Record implementation start time

  requirement_analysis:
    - Parse task requirements from the file content
    - Extract specific implementation steps from task description
    - Identify files to be created or modified
    - Determine success criteria and validation steps

  implementation_execution:
    backend_tasks:
      database_operations:
        - Create schema files, migrations, models
        - Validate database connections and permissions

      api_endpoints:
        - Implement controller methods with proper HTTP status codes
        - Add input validation and error handling
        - Document API endpoints and request/response formats

      authentication:
        - Add JWT middleware, session management
        - Implement password validation and security measures

      validation:
        - Implement input validation and sanitization
        - Add comprehensive error handling and logging

    frontend_tasks:
      component_creation:
        - Build React/Vue components with proper state management
        - Implement responsive design and accessibility features
        - Add proper error boundaries and loading states

      styling:
        - Add CSS/SCSS with responsive design and accessibility
        - Implement design system consistency
        - Optimize for performance and browser compatibility

      user_interactions:
        - Implement event handlers, form validation, user feedback
        - Add accessibility features (ARIA labels, keyboard navigation)
        - Create smooth user experience with proper feedback

    integration_tasks:
      service_communication:
        - Implement API calls between microservices
        - Add error handling and retry mechanisms
        - Implement proper service discovery and load balancing

      data_synchronization:
        - Create event handlers and data consistency logic
        - Implement proper transaction handling
        - Add data validation and conflict resolution

    infrastructure_tasks:
      configuration:
        - Create config files, environment variables, deployment scripts
        - Implement proper secret management and security measures

      cicd:
        - Set up pipelines, automated testing, deployment workflows
        - Add monitoring and alerting capabilities

      monitoring:
        - Add logging, metrics collection, health checks
        - Implement proper error tracking and performance monitoring

  post_implementation:
    verification:
      syntax_validation:
        - Use Bash to run linters, type checkers, syntax validators
        - Validate code quality and consistency

      unit_testing:
        - Create and run unit tests for implemented code
        - Ensure test coverage meets quality standards

      integration_testing:
        - Test component interactions and API endpoints
        - Validate end-to-end functionality

      manual_verification:
        - Test functionality through actual usage scenarios
        - Validate user experience and accessibility
```

### Step 6: Task Completion Management

**Completion workflow:**
```yaml
task_completion:
  status_finalization:
    - Use Edit tool to change task status from `[>]` to `[x]` (completed)
    - Add completion timestamp and implementation notes
    - Record any issues or blockers encountered

  validation:
    - Verify all requirements from task description are met
    - Confirm success criteria are satisfied
    - Validate no unintended side effects were introduced

  dependency_updates:
    - Update any dependent tasks that can now be executed
    - Recalculate task availability and execution order
    - Update progress metrics and completion percentages
```

### Step 7: Continuous Execution Management

**Continuous execution logic:**
```yaml
continuous_mode:
  execution_loop:
    - Immediately move to next pending task
    - Repeat steps 4-6 without stopping for confirmation
    - Continue until all tasks are completed or blocked
    - Maintain execution state and progress tracking

  stopping_conditions:
    - All tasks are completed
    - No more tasks can be executed due to blockers
    - An error occurs that requires user intervention
    - User explicitly stops execution
    - Maximum execution time reached

  progress_reporting:
    - Provide real-time progress updates
    - Report completed tasks and remaining work
    - Identify blockers and resolution paths
    - Calculate estimated completion time
```

### Step 8: Final Status Reporting

**Comprehensive reporting:**
```yaml
final_reporting:
  status_verification:
    - Use Read tool to verify final state of all task files
    - Count completed vs remaining tasks
    - Calculate completion percentage and velocity metrics

  blocker_analysis:
    - List any blockers that prevented completion
    - Provide resolution strategies for remaining tasks
    - Identify dependency issues and external factors

  accomplishment_summary:
    - Provide summary of work accomplished
    - Detail implementations completed and features added
    - Document any issues encountered and resolutions

  next_steps:
    - Suggest next steps (testing, validation, deployment)
    - Recommend additional tasks or improvements
    - Provide guidance for project continuation
```

## Output Format

**Execution response:**
```yaml
execution_result:
  mode: "continuous" | "single" | "all"
  feature_id: "002"
  feature_name: "user-authentication"
  tasks_executed: 5
  tasks_completed: 4
  tasks_blocked: 1

  execution_details:
    duration: "45 minutes"
    success_rate: "80%"
    issues_encountered: 1
    blockers_identified: 1

  completed_tasks:
    - id: "AUTH-T001"
      title: "Initialize auth service structure"
      status: "completed"
      duration: "8 minutes"

    - id: "AUTH-T002"
      title: "Implement JWT token handling"
      status: "completed"
      duration: "12 minutes"

  blocked_tasks:
    - id: "AUTH-T003"
      title: "Create password validation"
      status: "blocked"
      blocker: "Waiting for database schema"

  summary:
    total_progress: "75%"
    remaining_tasks: 2
    estimated_completion: "30 minutes"

  next_steps:
    - "Resolve database schema blocker"
    - "Continue with AUTH-T003 execution"
    - "Run integration tests for completed components"
```

## Error Handling and Recovery

**Comprehensive error scenarios:**
```yaml
error_handling:
  execution_errors:
    implementation_failures:
      action: Document failure, mark task as blocked, continue with next task
      recovery: Provide specific error messages and resolution steps

    test_failures:
      action: Fix implementation errors, retry testing, mark as completed
      recovery: Debug implementation issues, provide alternative approaches

  system_errors:
    file_system_errors:
      action: Provide specific error messages and resolution steps
      recovery: Check file permissions, disk space, directory access

    network_issues:
      action: Retry operations, provide offline alternatives
      recovery: Implement offline mode, cache external dependencies

  data_protection:
    backup_procedures:
      - Create .backup files before major changes
      - Maintain version history of task files
      - Enable rollback to previous states

    corruption_prevention:
      - Use atomic file operations
      - Validate file integrity after operations
      - Implement consistency checks
```

## Safety Constraints

- **Path validation**: Only operate within `.specpulse/` directory
- **Protected directories**: Never modify `templates/`, `specpulse/`, AI configs
- **Atomic operations**: Prevent partial updates and corruption
- **Rollback capability**: Restore original state on failures
- **Input validation**: Comprehensive sanitization of all inputs

## Integration Features

- **Atomic Task Updates**: Safe status changes prevent data corruption
- **Continuous Execution**: Non-stop task completion with progress tracking
- **Service-Specific Handling**: Proper dependency management for microservices
- **Implementation Verification**: Comprehensive testing and validation
- **Progress Analytics**: Real-time status updates and completion metrics
- **Error Recovery**: Comprehensive rollback and recovery mechanisms