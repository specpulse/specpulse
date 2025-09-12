---
name: sp-task
description: Generate and manage task breakdowns using AI-optimized templates
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-task Command

Generate task breakdowns from implementation plans using SpecPulse methodology with AI-optimized templates and enhanced validation.

## CRITICAL: File Edit Restrictions
- **NEVER EDIT**: templates/, scripts/, commands/, .claude/, .gemini/
- **ONLY EDIT**: specs/, plans/, tasks/, memory/
- Templates are COPIED to tasks/ folder, then edited there

## Usage
```
/sp-task [action] [feature-directory]
```

Actions: `breakdown`, `update`, `status`, `execute` (defaults to `breakdown`)

## Implementation

When called with `/sp-task $ARGUMENTS`, I will:

1. **Detect current feature context**:
   - Read `memory/context.md` for current feature metadata
   - Use git branch name if available (e.g., `001-user-authentication`)
   - Fall back to most recently created feature directory
   - If no context found, ask user to specify feature or run `/sp-pulse` first

2. **Parse arguments** to determine action:
   - If `update`: Update task status and dependencies
   - If `status`: Show comprehensive progress with metrics
   - If `execute`: Execute task with script integration
   - Otherwise: Generate task breakdown

3. **For `/sp-task breakdown` or `/sp-task`:**
   
   a. **Check for decomposition**: Look for `specs/XXX-feature/decomposition/` directory
   b. **If decomposed**:
      - Read service definitions from decomposition
      - Show service-specific plan files (auth-service-plan.md, user-service-plan.md, etc.)
      - Generate tasks per service with service prefix (AUTH-T001, USER-T001)
      - Create integration tasks (INT-T001) for cross-service work
      - Structure: `tasks/XXX-feature/auth-service-tasks.md`, `integration-tasks.md`
   c. **If not decomposed**:
      - Show existing plan files and ask user to select
      - Generate single task file with standard IDs (T001, T002)
   c. **Validation** using script:
      ```bash
      bash scripts/sp-pulse-task.sh "$FEATURE_DIR"
      ```
   
   d. **Read implementation plan** from selected plan file
   
   e. **Generate AI-optimized tasks** by COPYING template from templates/task.md to tasks/XXX-feature/:
      - **IMPORTANT**: Can EDIT files in tasks/ folder, but NEVER modify templates/, scripts/, or commands/ folders
      ```markdown
      # Task List: {{ feature_name }}
      ## Metadata
      - **Total Tasks**: {{ task_count }}
      - **Estimated Duration**: {{ total_duration }}
      - **Plan Reference**: plan-{{ plan_version }}.md
      - **Task Version**: {{ task_version }}
      ```

   f. **Generate structured task categories based on architecture**:
      - **For decomposed services**:
        * Service-specific tasks with bounded context
        * Inter-service integration tasks
        * Service deployment order tasks
        * Contract testing tasks between services
      - **For monolithic architecture**:
        * Layer-based tasks (data, business, API)
        * Module-specific tasks
      - **Common categories**:
        * Constitutional Gates Compliance
        * Critical Path identification
        * Parallel vs Sequential grouping
        * Progress Tracking configuration

   g. **For each task**, generate comprehensive metadata:
      - **ID**: T[XXX] format (T001, T002)
      - **Type**: setup, development, testing, documentation
      - **Priority**: HIGH, MEDIUM, LOW
      - **Estimate**: Hours or complexity points
      - **Dependencies**: Task ID dependencies
      - **Description**: Clear what needs to be done
      - **Acceptance**: How to verify completion
      - **Files**: Files to be created/modified
      - **Assignable**: Role/skill required
      - **Parallel**: Whether can run in parallel [P]

   h. **Generate AI execution guidelines** with workflow integration:
      ```markdown
      ## AI Execution Strategy
      ### Parallel Tasks (can be worked on simultaneously):
      - T001, T002, T003: Independent tasks, no dependencies
      ### Sequential Tasks (must be completed in order):
      - T004 → T005 → T006: Dependency chain
      ```

   i. **Version management**: Check existing task files and create next version (task-001.md, task-002.md, etc.)
   j. **Write comprehensive task breakdown** to `tasks/XXX-feature/task-XXX.md`

4. **For `/sp-task update`:**
   a. **Show existing task files**: List all task-XXX.md files in current feature directory
   b. **Ask user to select**: Which task file to update
   c. **Analysis** using script:
     ```bash
     bash scripts/sp-pulse-task.sh "$FEATURE_DIR"
     ```
   d. **Parse current tasks** from selected file with comprehensive status:
     - Total tasks, completed, pending, blocked
     - Parallel tasks identification
     - Constitutional gates status
     - Completion percentage calculation
   e. **Interactive task updates**:
     - Mark tasks as completed/in-progress/blocked
     - Update dependencies and blockers
     - Add newly discovered tasks with proper metadata
     - Adjust estimates based on actual progress
   f. **Generate updated progress tracking** YAML

5. **For `/sp-task status`:**
   a. **Show existing task files**: List all task-XXX.md files in current feature directory
   b. **Ask user to select**: Which task file to show status for
   c. **Enhanced reporting** from script output:
     ```bash
     TOTAL_TASKS=25
     COMPLETED_TASKS=10
     COMPLETION_PERCENTAGE=40%
     CONSTITUTIONAL_GATES_PENDING=2
     ```
   d. **Display comprehensive progress**:
     - Overall completion percentage
     - Phase-by-phase progress
     - Blocker identification and resolution
     - Velocity metrics and estimates
     - Constitutional gates compliance status

6. **For `/sp-task execute`:**
   a. **Show existing task files**: List all task-XXX.md files in current feature directory
   b. **Ask user to select**: Which task file to execute from
   c. **Ask user to specify**: Which specific task ID to execute
   d. **Validate task readiness** using constitutional gates
   e. **Execute task** using AI assistant capabilities:
     ```markdown
     ## Task Execution: {{ TASK_ID }}
     **AI Assistant**: Claude/Gemini
     **Method**: Direct implementation within AI session
     **Status**: [ ] Pending → [-] In Progress → [x] Completed
     ```
   f. **Track execution results** and update status
   g. **Update progress tracking** automatically

## Enhanced Task Format

### For Decomposed Services
```markdown
### Auth Service Tasks
#### AUTH-T001: Initialize auth service structure
- **Service**: Authentication
- **Type**: setup
- **Priority**: HIGH
- **Dependencies**: None

### User Service Tasks  
#### USER-T001: Initialize user service structure
- **Service**: User Management
- **Type**: setup
- **Priority**: HIGH
- **Dependencies**: None

### Integration Tasks
#### INT-T001: Set up service communication
- **Services**: Auth ↔ User
- **Type**: integration
- **Priority**: HIGH
- **Dependencies**: AUTH-T001, USER-T001
```

### For Monolithic Architecture
```markdown
### Parallel Group A
#### T001: Initialize project structure
- **Type**: setup
- **Priority**: HIGH
- **Estimate**: 2 hours
- **Dependencies**: None
- **Description**: Set up project directory structure and configuration
- **Acceptance**: All directories exist and config files are valid
- **Files**: package.json, README.md, .gitignore
- **Assignable**: developer
- **Parallel**: [P]

## Progress Tracking
```yaml
status:
  total: 25
  completed: 10
  in_progress: 3
  blocked: 0
  
metrics:
  velocity: 2-3 tasks/day
  estimated_completion: 2025-09-15
  completion_percentage: 40%
```

## Constitutional Gates Integration

Each task breakdown includes constitutional compliance validation:
- **Simplicity Gate**: Tasks avoid unnecessary complexity
- **Test-First Gate**: Test tasks before implementation tasks
- **Integration-First Gate**: Real service integration preferred
- **Research Gate**: Technology research tasks included

## Examples

### Generate tasks for decomposed spec
```
User: /sp-task breakdown
```
Detecting decomposition in `specs/001-authentication/decomposition/`...
I will create:
- `tasks/001-authentication/auth-service-tasks.md`
- `tasks/001-authentication/user-service-tasks.md`
- `tasks/001-authentication/integration-tasks.md`

### Generate tasks for monolithic spec
```
User: /sp-task breakdown
```
No decomposition found. Creating single task file:
- `tasks/001-authentication/task-001.md`

### Execute service-specific task
```
User: /sp-task execute AUTH-T001
```
I will:
- Run: Cross-platform detection and execution
  ```bash
  bash scripts/sp-pulse-task.sh "$FEATURE_DIR"
  ```
- Create: AI-optimized task structure with template variables
- Output: `TOTAL_TASKS=25, PARALLEL_TASKS=8, STATUS=generated`

### Update task status
```
User: /sp-task update mark T001-T005 as completed
```
I will update task status and recalculate progress metrics.

### Show comprehensive status
```
User: /sp-task status
```
I will display detailed progress with constitutional gates compliance.

### Execute specific task
```
User: /sp-task execute T001
```
I will:
- Validate: Constitutional gates compliance and task readiness
- Execute: Cross-platform task execution
  ```bash
  bash scripts/sp-pulse-task.sh "$FEATURE_DIR" "execute:$TASK_ID"
  ```
- Track: Results and update progress automatically

## Enhanced Features

- **Script execution** with Bash
- **AI-optimized templates** with Jinja2-style variables
- **Script integration** for validation and execution
- **Constitutional gates compliance** tracking
- **Parallel task identification** and execution
- **Comprehensive progress tracking** with YAML configuration
- **Automatic percentage calculation** and velocity metrics
- **Task dependency management** with conflict detection
- **Execution command generation** with script integration
- **Cross-platform operation** with Bash

## Error Handling

- Plan existence validation before task generation
- Constitutional gates compliance checking
- Template structure validation
- Dependency conflict detection
- Task execution error handling with rollback
- Progress tracking validation and correction