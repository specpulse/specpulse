---
name: task
description: Generate and manage task breakdowns using AI-optimized templates
allowed_tools:
  - Read
  - Write  
  - Edit
  - Bash
  - TodoWrite
---

# /task Command

Generate task breakdowns from implementation plans using SpecPulse methodology with AI-optimized templates and enhanced validation.

## Usage
```
/task [action] [feature-directory]
```

Actions: `breakdown`, `update`, `status`, `execute` (defaults to `breakdown`)

## Implementation

When called with `/task $ARGUMENTS`, I will:

1. **Parse arguments** to determine action:
   - If `update`: Update task status and dependencies
   - If `status`: Show comprehensive progress with metrics
   - If `execute`: Execute task with script integration
   - Otherwise: Generate task breakdown

2. **For `/task breakdown` or `/task`:**
   
   a. **Enhanced validation** using cross-platform script:
      ```bash
      # Cross-platform detection
      if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
          powershell scripts/pulse-task.ps1 "$FEATURE_DIR"
      else
          bash scripts/pulse-task.sh "$FEATURE_DIR" || python scripts/pulse-task.py "$FEATURE_DIR"
      fi
      ```
   
   b. **Read implementation plan** from `plans/XXX-feature/plan.md`
   
   c. **Generate AI-optimized tasks** using template variables:
      ```markdown
      # Task List: {{ feature_name }}
      ## Metadata
      - **Total Tasks**: {{ task_count }}
      - **Estimated Duration**: {{ total_duration }}
      ```

   d. **Generate structured task categories**:
      - **Constitutional Gates Compliance**: Pre-implementation validation
      - **Critical Path (Phase 0)**: Tasks that impact timeline
      - **Parallel Groups**: Tasks that can execute simultaneously
      - **Sequential Tasks**: Tasks with dependencies
      - **Execution Schedule**: Time-based task organization
      - **Progress Tracking**: YAML configuration for monitoring

   e. **For each task**, generate comprehensive metadata:
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

   f. **Generate execution commands** with script integration:
      ```bash
      # Execute parallel tasks
      parallel_tasks="T001 T002 T003"
      for task in $parallel_tasks; do
          ./scripts/execute-task.sh "$task" &
      done
      wait
      ```

   g. **Write comprehensive task breakdown** to `tasks/XXX-feature/tasks.md`

3. **For `/task update`:**
   - **Enhanced analysis** using cross-platform script:
     ```bash
     # Cross-platform detection
     if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
         powershell scripts/pulse-task.ps1 "$FEATURE_DIR"
     else
         bash scripts/pulse-task.sh "$FEATURE_DIR" || python scripts/pulse-task.py "$FEATURE_DIR"
     fi
     ```
   - **Parse current tasks** with comprehensive status:
     - Total tasks, completed, pending, blocked
     - Parallel tasks identification
     - Constitutional gates status
     - Completion percentage calculation
   - **Interactive task updates**:
     - Mark tasks as completed/in-progress/blocked
     - Update dependencies and blockers
     - Add newly discovered tasks with proper metadata
     - Adjust estimates based on actual progress
   - **Generate updated progress tracking** YAML

4. **For `/task status`:**
   - **Enhanced reporting** from script output:
     ```bash
     TOTAL_TASKS=25
     COMPLETED_TASKS=10
     COMPLETION_PERCENTAGE=40%
     CONSTITUTIONAL_GATES_PENDING=2
     ```
   - **Display comprehensive progress**:
     - Overall completion percentage
     - Phase-by-phase progress
     - Blocker identification and resolution
     - Velocity metrics and estimates
     - Constitutional gates compliance status

5. **For `/task execute`:**
   - **Validate task readiness** using constitutional gates
   - **Execute task** with enhanced error handling:
     ```bash
     ./scripts/execute-task.sh "$TASK_ID"
     ```
   - **Track execution results** and update status
   - **Update progress tracking** automatically

## Enhanced Task Format
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

### Generate task breakdown
```
User: /task breakdown
```
I will:
- Run: Cross-platform detection and execution
  ```bash
  # Cross-platform detection
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
      powershell scripts/pulse-task.ps1 "$FEATURE_DIR"
  else
      bash scripts/pulse-task.sh "$FEATURE_DIR" || python scripts/pulse-task.py "$FEATURE_DIR"
  fi
  ```
- Create: AI-optimized task structure with template variables
- Output: `TOTAL_TASKS=25, PARALLEL_TASKS=8, STATUS=generated`

### Update task status
```
User: /task update mark T001-T005 as completed
```
I will update task status and recalculate progress metrics.

### Show comprehensive status
```
User: /task status
```
I will display detailed progress with constitutional gates compliance.

### Execute specific task
```
User: /task execute T001
```
I will:
- Validate: Constitutional gates compliance and task readiness
- Execute: Cross-platform task execution
  ```bash
  # Cross-platform task execution
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
      powershell scripts/pulse-task.ps1 "$FEATURE_DIR" "execute:$TASK_ID"
  else
      bash scripts/pulse-task.sh "$FEATURE_DIR" "execute:$TASK_ID" || python scripts/pulse-task.py "$FEATURE_DIR" "execute:$TASK_ID"
  fi
  ```
- Track: Results and update progress automatically

## Enhanced Features

- **Cross-platform script execution** with automatic detection (PowerShell/Bash/Python)
- **AI-optimized templates** with Jinja2-style variables
- **Enhanced script integration** for validation and execution
- **Constitutional gates compliance** tracking
- **Parallel task identification** and execution
- **Comprehensive progress tracking** with YAML configuration
- **Automatic percentage calculation** and velocity metrics
- **Task dependency management** with conflict detection
- **Execution command generation** with script integration
- **Platform-agnostic operation** for Windows, Linux, and macOS

## Error Handling

- Plan existence validation before task generation
- Constitutional gates compliance checking
- Template structure validation
- Dependency conflict detection
- Task execution error handling with rollback
- Progress tracking validation and correction