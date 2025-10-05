---
name: sp-execute
description: Execute tasks continuously without stopping - complete all pending work
allowed_tools:
  - Bash
  - Read
  - Write
  - Edit
  - MultiEdit
  - TodoWrite
  - Grep
  - WebSearch
---

# /sp-execute Command

Execute tasks continuously from the task list without stopping between tasks. Perfect for completing multiple tasks in sequence.

## Usage
```
/sp-execute                    # Execute next pending task and continue
/sp-execute next               # Same as above
/sp-execute all                # Execute ALL pending tasks non-stop
/sp-execute T001               # Execute specific task
/sp-execute AUTH-T001          # Execute specific service task
```

## CRITICAL: Continuous Execution Mode

**This command enables NON-STOP task execution. I will:**
1. Execute the current/next task
2. Mark it as completed
3. Immediately move to the next task
4. Continue until ALL tasks are done or blocked

**NO STOPPING** between tasks unless:
- All tasks are completed
- Remaining tasks are blocked
- An error occurs that requires user intervention
- User explicitly stops me

## Implementation

When called with `/sp-execute $ARGUMENTS`, I will:

1. **Run the execution script**:
   ```bash
   scripts/sp-pulse-execute.sh $ARGUMENTS
   ```

2. **Analyze task status** from script output:
   - Identify next task to execute
   - Check if decomposed (service-specific tasks)
   - Calculate overall progress

3. **Execute task implementation**:
   - Read task description from task file
   - Implement the solution
   - Test if applicable
   - Mark task as completed in task file

4. **Continue immediately**:
   - NO PAUSE for confirmation
   - NO STOPPING to explain what was done
   - Move directly to next task

5. **Repeat until done**:
   - Continue executing tasks in sequence
   - Only stop when all tasks are completed or blocked

## Task Execution Flow

### Single Task Mode (`/sp-execute` or `/sp-execute next`)
```
1. Find next pending task (T001 or AUTH-T001)
2. Mark as in-progress: [ ] → [>]
3. Implement the task
4. Mark as completed: [>] → [x]
5. Automatically continue to next task
6. Repeat until all done
```

### Batch Mode (`/sp-execute all`)
```
1. Get list of ALL pending tasks
2. Execute each task in sequence
3. No stopping between tasks
4. Continue until completion or blockage
```

## Task Status Markers

- `[ ]` - Pending task (ready to execute)
- `[>]` - In progress (currently working on)
- `[x]` - Completed (done)
- `[!]` - Blocked (waiting for dependency)

## Example Execution

### Continuous execution
```
User: /sp-execute
```

I will:
1. Check current tasks: "Found 15 pending tasks"
2. Start with T001: "Implementing user model..."
3. Complete T001: ✓ User model created
4. Move to T002: "Creating authentication service..."
5. Complete T002: ✓ Authentication service implemented
6. Continue with T003, T004, T005... WITHOUT STOPPING
7. Only report: "All 15 tasks completed successfully!"

### Batch execution
```
User: /sp-execute all
```

I will:
- Process ALL pending tasks in one go
- No interruptions or pauses
- Complete the entire task list
- Report final status only

### Specific task
```
User: /sp-execute AUTH-T003
```

I will:
- Execute only AUTH-T003
- Then continue with AUTH-T004, AUTH-T005...
- Keep going until all AUTH tasks are done

## Workflow Integration

### Starting fresh
```
/sp-pulse new-feature
/sp-spec "Create user authentication with OAuth2"
/sp-plan
/sp-task
/sp-execute all    # Complete everything!
```

### Resuming work
```
/sp-continue 001-user-auth
/sp-execute        # Continue from where we left off
```

## Non-Stop Execution Rules

1. **NO EXPLANATIONS** between tasks - just execute
2. **NO WAITING** for confirmation - keep going
3. **NO SUMMARIES** after each task - save for the end
4. **ONLY STOP** when:
   - All tasks completed
   - Hit a blocker
   - Critical error occurs
   - User explicitly says "stop"

## Error Handling

If an error occurs during task execution:
1. Mark task as blocked: `[!]`
2. Note the error in task file
3. Skip to next available task
4. Continue execution
5. Report all blockers at the end

## Progress Tracking

During execution, I maintain:
- Task completion counter
- Progress percentage
- List of completed tasks
- List of any blockers encountered

Final report shows:
```
## Execution Complete

**Progress**: 100% (25/25 tasks)
**Duration**: Continuous execution
**Status**: All tasks completed

### Summary
✓ 25 tasks completed
✗ 0 tasks blocked
→ 0 tasks remaining

Ready for validation: /sp-validate
```

## Benefits

- **Maximum efficiency** - No time wasted between tasks
- **Flow state** - Continuous productive work
- **Rapid delivery** - Complete features faster
- **Reduced context switching** - Stay focused on implementation
- **Automated workflow** - Let AI handle the execution