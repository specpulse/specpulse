---
name: sp-execute
description: Execute tasks without SpecPulse CLI
allowed_tools:
  - Bash
  - Read
  - Write
  - Edit
  - TodoWrite
  - Grep
---

# /sp-execute Command

Execute tasks without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-execute [task-id|all|next]    # Execute specific task, all tasks, or next pending task
```

## Implementation

When called with `/sp-execute {{args}}`, I will:

### 1. Parse Arguments and Determine Execution Mode

**I will:**
- Parse the command arguments:
  - `all` → Execute ALL pending tasks non-stop
  - `next` or no argument → Execute next pending task and continue
  - `T001` or `AUTH-T001` → Execute specific task
- Set execution mode accordingly
- Determine if continuous execution is needed

### 2. Detect Current Feature Context

**I will:**
- Use **Read** tool to examine `.specpulse/memory/context.md`
- Look for `**Directory**:` field to identify current feature
- If no context found, use **Glob** tool to find first feature with task files
- Validate feature directory follows naming convention (XXX-feature-name)
- Set `tasks_dir` to `.specpulse/tasks/[current-feature]`

### 3. Load and Analyze Task Files

**I will:**
- Use **Glob** tool to find all `*.md` files in tasks directory
- Use **Read** tool to examine each task file
- Parse task status markers:
  - `[ ]` = Pending task
  - `[>]` = In progress task
  - `[x]` = Completed task
  - `[!]` = Blocked task
- Build task inventory with status and dependencies
- Validate task file structure and content

### 4. Determine Task Execution Order

**For continuous mode (`all` or `next`):**
- Find first pending task (`[ ]`)
- Check if dependencies are completed
- If dependencies not met, skip to next available task
- For specific task mode, validate the requested task exists

**For service tasks:**
- Handle `AUTH-T001`, `USER-T001` patterns
- Respect service-specific dependencies
- Consider integration tasks after service tasks complete

### 5. Execute Task Implementation

**For each selected task:**

**I will:**
- Use **Edit** tool to change task status from `[ ]` to `[>]` (in progress)
- Parse task requirements from the file content
- Extract specific implementation steps from task description
- Execute **atomic file operations** based on task type:

#### A. For Backend/API Tasks:
- **Database Operations**: Create schema files, migrations, models
- **API Endpoints**: Implement controller methods with proper HTTP status codes
- **Authentication**: Add JWT middleware, session management, password validation
- **Validation**: Implement input validation and error handling

#### B. For Frontend Tasks:
- **Component Creation**: Build React/Vue components with proper state management
- **Styling**: Add CSS/SCSS with responsive design and accessibility
- **User Interactions**: Implement event handlers, form validation, user feedback
- **Routing**: Set up navigation, route guards, page transitions

#### C. For Integration Tasks:
- **Service Communication**: Implement API calls between microservices
- **Data Synchronization**: Create event handlers and data consistency logic
- **Testing**: Add unit tests, integration tests, end-to-end tests
- **Documentation**: Update API docs, README files, code comments

#### D. For Infrastructure Tasks:
- **Configuration**: Create config files, environment variables, deployment scripts
- **CI/CD**: Set up pipelines, automated testing, deployment workflows
- **Monitoring**: Add logging, metrics collection, health checks
- **Security**: Implement authentication, authorization, input sanitization

#### E. Implementation Verification:
- **Syntax Validation**: Use **Bash** to run linters, type checkers, syntax validators
- **Unit Testing**: Create and run unit tests for implemented code
- **Integration Testing**: Test component interactions and API endpoints
- **Manual Verification**: Test functionality through actual usage scenarios

### 6. Mark Task Completion

**I will:**
- Use **Edit** tool to change task status from `[>]` to `[x]` (completed)
- Add completion timestamp if not present
- Verify all requirements from task description are met
- Update any dependent tasks that can now be executed

### 7. Continue Execution (If in continuous mode)

**I will:**
- Immediately move to next pending task
- Repeat steps 4-6 without stopping for confirmation
- Continue until all tasks are completed or blocked
- Only stop when:
  - All tasks are completed
  - No more tasks can be executed due to blockers
  - An error occurs that requires user intervention
  - User explicitly stops execution

### 8. Final Status Report

**I will:**
- Use **Read** tool to verify final state of all task files
- Count completed vs remaining tasks
- Calculate completion percentage
- List any blockers that prevented completion
- Provide summary of work accomplished
- Suggest next steps (testing, validation, etc.)

## Task Execution Examples

### Execute next pending task:
```bash
/sp-/sp-execute
```

**I will:**
- Find current feature from context
- Locate next `[ ]` task
- Change to `[>]` (in progress)
- Implement the task requirements
- Change to `[x]` (completed)
- Continue to next task

### Execute all tasks:
```bash
/sp-/sp-execute all
```

**I will:**
- Find ALL pending tasks
- Execute each in sequence without stopping
- Update status as completed
- Report final progress

### Execute specific task:
```bash
/sp-/sp-execute T001
```

**I will:**
- Find task in T001.md file
- Execute all pending tasks in that file
- Update progress accordingly

## CLI-Independent Features

- **No CLI Dependencies**: 100% independent of SpecPulse CLI installation
- **Manual Task Parsing**: Direct file content analysis without CLI
- **Atomic Task Updates**: Safe file operations prevent corruption
- **Progress Tracking**: Manual calculation from task files
- **Error Recovery**: Comprehensive error handling
- **Continuous Execution**: Non-stop task completion

## Task Status Markers

- `[ ]` - Pending task (ready to execute)
- `[>]` - In progress (currently working on)
- `[x]` - Completed (done)
- `[!]` - Blocked (waiting for dependency)

## CLI-Independent Examples

### Execute next pending task
```bash
User: /sp-/sp-execute
```

I will:
- Detect current feature from memory context
- Find next pending task using file scanning
- Mark as in-progress and execute
- Complete and move to next task automatically

### Execute all pending tasks
```bash
User: /sp-/sp-execute all
```

I will:
- Find ALL pending tasks across all task files
- Execute each task in sequence without stopping
- Complete entire task list non-stop
- Report final progress and status

### Execute specific task
```bash
User: /sp-/sp-execute T001
```

I will:
- Find task file T001.md
- Execute all pending tasks in that file
- Continue with subsequent tasks if needed

## CLI-Independent Safety Features

### Atomic File Operations
- **Task Status Updates**: Use **Edit** tool with complete file content replacement
- **Before Update Validation**: Verify file exists and is writable
- **After Update Verification**: Confirm changes were applied correctly
- **Rollback on Failure**: Restore original content if update fails

### Safe Directory Access
- **Path Validation**: Ensure all paths are within `.specpulse/` directory
- **Directory Traversal Protection**: Reject paths with `../` or absolute paths
- **Permission Checks**: Verify read/write access before operations
- **Error Recovery**: Provide clear guidance for permission issues

### Error Handling and Recovery

#### Task Execution Failures
- **Implementation Errors**: Document failure, mark task as blocked, continue
- **Test Failures**: Fix implementation errors, retry testing, mark as completed
- **File System Errors**: Provide specific error messages and resolution steps
- **Network Issues**: Retry operations, provide offline alternatives

#### Data Corruption Prevention
- **Backup Creation**: Create `.backup` files before major changes
- **Validation Checks**: Verify file integrity after operations
- **Recovery Procedures**: Provide steps to restore from backups
- **Consistency Maintenance**: Ensure task files remain valid markdown

#### Memory Context Management
- **Automatic Feature Detection**: Fallback methods if context file missing
- **Context Recovery**: Rebuild context from available feature data
- **State Synchronization**: Keep task status and context aligned
- **Progress Tracking**: Manual calculation with error tolerance

**Key Benefits vs Regular Commands**
| Regular /sp-execute | CLI-Independent /sp-/sp-execute |
|-------------------|---------------------------------|
| Requires CLI installation | Works completely independently |
| Uses CLI task commands | Manual file parsing and updates |
| CLI progress tracking | Manual progress calculation |
| Limited error handling | Comprehensive error recovery |
| CLI dependency issues | Self-contained operation |

**Status**: `CLI-Independent task execution complete, no SpecPulse CLI required` ✅