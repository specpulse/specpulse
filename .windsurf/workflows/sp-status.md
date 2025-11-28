---
description: Track progress across all features and specific feature details with comprehensive reporting
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the progress tracking outcome
- Only read files - NEVER modify any files during status reporting

**Critical Rules**
- **PRIMARY**: Use `specpulse status [feature-name]` when available
- **FALLBACK**: File Operations only if CLI fails
- **READ-ONLY OPERATION**: This command only reads files, never modifies them
- **PROTECTED DIRECTORIES**: All directories are read-only during status reporting

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments** to determine scope:
   - If feature name provided: Show detailed status for that feature
   - Otherwise: Show overview of all features

2. **Try CLI First**:
   ```bash
   specpulse status [feature-name]
   specpulse progress [feature-id]
   ```
   If CLI succeeds, STOP HERE.

3. **Read feature context** from `memory/context.md`

4. **For /sp-status (all features overview):**
   - **Scan all feature directories** (specs/*, plans/*, tasks/*)
   - **Count features by status**: active, completed, in_progress, paused
   - **Calculate overall project progress**
   - **Show summary statistics**:
     ```
     TOTAL_FEATURES=5
     ACTIVE_FEATURES=2
     COMPLETED_FEATURES=1
     IN_PROGRESS_FEATURES=1
     PAUSED_FEATURES=1
     OVERALL_PROGRESS=42%
     ```
   - **List all features** with their status and progress percentage
   - **Highlight current active feature** from context

5. **For /sp-status [feature-name] (detailed feature status):**
   - **Detect feature directory** (using context detection logic)
   - **Read all task files** in the feature's tasks directory
   - **Calculate completion percentage** based on task status
   - **Show detailed breakdown**:
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
   - **Show phase-by-phase progress**
   - **List any blockers or issues**
   - **Provide recommendations for next steps**

6. **Progress calculation logic**:
   - **Scan task files** for completion status:
     * `[x]` for completed
     * `[ ]` for pending
     * `[-]` for in progress
     * `[!]` for blocked
   - **Calculate percentages**: completed / total * 100
   - **Track trends over time** if historical data available

7. **Generate comprehensive status report** with visual indicators

**Usage**
```
/sp-status [feature-name]
```

**Feature Status Indicators**

- **Active**: Currently being worked on (in context.md)
- **Completed**: All tasks marked as complete
- **In Progress**: Has task files with some completed tasks
- **Paused**: No recent activity, not all tasks complete
- **Blocked**: Has blocked tasks preventing progress

**Task Status Format**
```markdown
- [ ] T001: [S] Set up project structure      # Pending
- [>] T002: [M] Create database schema       # In Progress
- [x] T003: [L] Implement authentication      # Completed
- [!] T004: [S] Fix authentication bug        # Blocked
```

**Examples**

**All features overview:**
```
/sp-status
```
Output:
```
## Feature Status Overview

**Total Features**: 5
**Overall Progress**: 42%

### Active Features
- [PROG] 001-user-authentication (65%)
- [PROG] 002-payment-processing (23%)

### Completed Features
- [OK] 000-project-setup (100%)

### Paused Features
- [PAUSED] 003-user-profile (45%)

### Detailed Breakdown
**001-user-authentication** (ACTIVE)
- Progress: 65% (16/25 tasks completed)
- Status: In development
- Next step: Continue with T017
- Blockers: T004 (Authentication bug) needs review

**002-payment-processing** (ACTIVE)
- Progress: 23% (5/22 tasks completed)
- Status: Early development
- Next step: Implement payment gateway integration
```

**Specific feature status:**
```
/sp-status 001-user-authentication
```
Output:
```
## Feature Status: 001-user-authentication

**Status**: Active
**Progress**: 65% (16/25 tasks completed)

### File Structure
- Specs: 2 files (spec-001.md, spec-002.md)
- Plans: 1 file (plan-001.md)
- Tasks: 1 file (task-001.md)

### Task Breakdown
- Completed: 16 tasks (64%)
- In Progress: 5 tasks (20%)
- Pending: 3 tasks (12%)
- Blocked: 1 task (4%)

### Phase Progress
- Phase 0 (Critical Path): 100% (3/3)
- Phase 1 (Foundation): 80% (8/10)
- Phase 2 (Core Features): 50% (4/8)
- Phase 3 (Polish): 0% (0/3)
- Phase 4 (Testing): 0% (0/1)

### Current Blockers
- **T004**: Authentication bug requires security review
- **T015**: Database schema waiting for DBA approval

### Recommendations
1. Resolve T004 blocker first (security review)
2. Continue with Phase 1 foundation tasks
3. Plan database schema review for next sprint

### Last Updated
2025-01-09 14:30:00
```

**Multi-Feature Progress Summary**

**Project Overview Statistics:**
```
PROJECT_STATS:
TOTAL_FEATURES=5
ACTIVE_FEATURES=2
COMPLETED_FEATURES=1
PAUSED_FEATURES=1
BLOCKED_FEATURES=1

TASK_STATS:
TOTAL_TASKS=127
COMPLETED_TASKS=68
IN_PROGRESS_TASKS=23
PENDING_TASKS=31
BLOCKED_TASKS=5

OVERALL_PROGRESS=54%
ESTIMATED_COMPLETION=2025-02-15
```

**CLI Integration**

**Try CLI First:**
```bash
specpulse status
specpulse progress <feature-id>
specpulse spec-progress <feature-id>
```

**Fallback to Manual Status if CLI Fails:**
1. Read feature directories manually
2. Parse task completion status
3. Calculate progress percentages
4. Generate status report

**Advanced Progress Tracking**

**Trend Analysis:**
- Progress velocity (tasks/day)
- Completion time estimates
- Blocker resolution tracking
- Feature dependency analysis

**Health Metrics:**
- Task completion rate
- Blocker frequency
- Feature churn rate
- Quality indicator trends

**Export Options**

**Status Reports:**
- JSON format for automation
- Markdown for documentation
- CSV for data analysis

**Integrations:**
- Project management tools
- CI/CD pipeline status
- Stakeholder reporting

**Task Status Transitions**
```
[ ] Pending → [>] In Progress → [x] Completed
                ↓                    ↓
           [!] Blocked → [x] Completed
```

**Reference**
- Use `specpulse status --help` if you need additional CLI options
- Check `memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- Use `/sp-continue` to resume work on a feature
- This command is READ-ONLY - it never modifies files
<!-- SPECPULSE:END -->