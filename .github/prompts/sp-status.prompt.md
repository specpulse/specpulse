---
description: Track progress across all features and specific feature details with comprehensive reporting.
---

$ARGUMENTS
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the progress tracking outcome
- READ-ONLY OPERATION: This command only reads files, never modifies any files

**Critical Rules**
- **PRIMARY**: Use `specpulse status [feature-name]` when available
- **FALLBACK**: File Operations only if CLI fails
- **READ-ONLY VALIDATION**: This command only validates, never modifies files
- **PROTECTED DIRECTORIES**: All directories are read-only during status reporting

**Steps**
Track these steps as TODOs and complete them one by one.
1. **Parse arguments** from $ARGUMENTS to determine scope:
   - If feature name provided: Show detailed status for that feature
   - Otherwise: Show overview of all features
2. **Try CLI First**:
   ```bash
   specpulse status [feature-name]
   specpulse progress [feature-id]
   ```
   If CLI succeeds, STOP HERE.
3. **Read feature context** from `memory/context.md`
4. **For all features overview**:
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
5. **For specific feature status**:
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

**Usage**
Arguments should be provided as: `[feature-name]`

If no feature name provided, shows overview of all features.

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
Input: No arguments
Output: Comprehensive project overview with feature breakdown.

**Specific feature status:**
Input: `001-user-authentication`
Output: Detailed feature progress with task breakdown and recommendations.

**Reference**
- Use `specpulse status --help` if you need additional CLI options
- Check `memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- Use `/sp-continue` to resume work on a feature
- This command is READ-ONLY - it never modifies files
<!-- SPECPULSE:END -->