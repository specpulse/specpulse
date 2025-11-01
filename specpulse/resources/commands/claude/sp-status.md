---
name: sp-status
description: Track progress across all features and specific feature details
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-status Command

Track progress across all features or get detailed status of a specific feature.

## Usage
```
/sp-status [feature-name]
```

## Implementation

When called with `/sp-status $ARGUMENTS`, I will:

1. **Parse arguments** to determine scope:
   - If feature name provided: Show detailed status for that feature
   - Otherwise: Show overview of all features

2. **Read feature context** from `memory/context.md`

3. **For `/sp-status` (all features overview):**
   - Scan all feature directories (specs/*, plans/*, tasks/*)
   - Count features by status: active, completed, in_progress, paused
   - Calculate overall project progress
   - Show summary statistics:
     ```
     TOTAL_FEATURES=5
     ACTIVE_FEATURES=2
     COMPLETED_FEATURES=1
     IN_PROGRESS_FEATURES=1
     PAUSED_FEATURES=1
     OVERALL_PROGRESS=42%
     ```
   - List all features with their status and progress percentage
   - Highlight current active feature from context

4. **For `/sp-status [feature-name]` (detailed feature status):**
   - Detect feature directory (using context detection logic)
   - Read all task files in the feature's tasks directory
   - Calculate completion percentage based on task status
   - Show detailed breakdown:
     ```
     FEATURE: 001-user-authentication
     STATUS: active
     PROGRESS: 65%
     SPECS: 2 files
     PLANS: 1 file  
     TASKS: 1 file (25 total tasks)
     COMPLETED_TASKS: 16
     IN_PROGRESS_TASKS: 5
     BLOCKED_TASKS: 1
     LAST_UPDATED: 2025-01-09
     ```
   - Show phase-by-phase progress
   - List any blockers or issues
   - Provide recommendations for next steps

5. **Progress calculation logic:**
   - Scan task files for completion status: `[x]` for completed, `[ ]` for pending, `[-]` for in progress, `[!]` for blocked
   - Calculate percentages: completed / total * 100
   - Track trends over time if historical data available

## Feature Status Indicators

- **Active**: Currently being worked on (in context.md)
- **Completed**: All tasks marked as complete
- **In Progress**: Has task files with some completed tasks
- **Paused**: No recent activity, not all tasks complete
- **Blocked**: Has blocked tasks preventing progress

## Examples

### All features overview
```
User: /sp-status
```

I will display:
```
## Feature Status Overview

**Total Features**: 5
**Overall Progress**: 42%

### Active Features
- [PROG] 001-user-authentication (65%)
- [PROG] 002-payment-processing (23%)

### Completed Features  
- [OK] 000-project-setup (100%)

### In Progress Features
- [WAIT] 003-user-profile (45%)

### Paused Features
- [PAUSED] 004-notifications (78%)

### Current Context
**Active Feature**: 001-user-authentication
**Last Updated**: 2025-01-09
```

### Specific feature status
```
User: /sp-status user-authentication
```

I will display:
```
## Feature Status: 001-user-authentication

**Overall Progress**: 65%
**Status**: Active
**Created**: 2025-01-09
**Last Updated**: 2025-01-09

### Files
- **Specifications**: spec-001.md, spec-002.md (2 files)
- **Plans**: plan-001.md (1 file)
- **Tasks**: task-001.md (1 file, 25 total tasks)

### Task Progress
- **Completed**: 16 tasks (64%)
- **In Progress**: 5 tasks (20%)
- **Blocked**: 1 task (4%)
- **Pending**: 3 tasks (12%)

### Phase Progress
- **Phase 0 (Critical Path)**: 80% complete
- **Phase 1 (Foundation)**: 70% complete
- **Phase 2 (Core Features)**: 50% complete
- **Phase 3 (Polish)**: 20% complete
- **Phase 4 (Testing)**: 0% complete

### Blockers
- T015: Database schema approval pending

### Recommendations
1. Resolve database schema blocker (T015)
2. Continue with Phase 2 core features
3. Consider starting Phase 4 testing in parallel
```

## Integration Features

- **Multi-feature tracking** across entire project
- **Progress percentage calculation** from task completion
- **Status categorization** with visual indicators
- **Blocker identification** and resolution tracking
- **Context-aware operation** using memory/context.md
- **Cross-platform compatibility** with proper path handling
- **Historical trend tracking** for progress over time

## Error Handling

- Feature directory validation
- Task file parsing with error recovery
- Progress calculation validation
- Context file fallback handling
- Permission and access error handling