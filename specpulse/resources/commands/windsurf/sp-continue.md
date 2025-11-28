---
description: Switch context and continue work on a specific feature with intelligent state management
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the context switching outcome
- Only edit memory/context.md file - NEVER modify other files

**Critical Rules**
- **PRIMARY**: Use `specpulse context set/get` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/
- **EDITABLE ONLY**: memory/context.md

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments** to extract feature name or ID
2. **Try CLI First**:
   ```bash
   specpulse context set current.feature <feature-name>
   specpulse continue <feature-name>
   ```
   If CLI succeeds, STOP HERE.

3. **Find feature directory** using context detection:
   - Search for matching feature directory (specs/*, plans/*, tasks/*)
   - Support partial matching (e.g., "auth" matches "001-user-authentication")
   - Support ID matching (e.g., "001" matches "001-user-authentication")

4. **Validate feature exists**:
   - Check if feature directory has any files
   - Verify feature structure is intact
   - Report if feature not found

5. **Update context** in `memory/context.md`:
   ```yaml
   # Feature Context

   ## Current Feature
   - **ID**: 001
   - **Name**: user-authentication
   - **Branch**: 001-user-authentication
   - **Status**: active
   - **Created**: 2025-01-09
   - **Last Updated**: 2025-01-09
   - **Switched To**: 2025-01-09 (via /sp-continue)
   ```

6. **Switch git branch** if in git repository:
   ```bash
   git checkout <feature-branch>
   ```
   - Checkout feature branch if it exists
   - Report if branch doesn't exist
   - Handle branch switching errors gracefully

7. **Display feature status**:
   - Show current progress percentage
   - List next available actions
   - Highlight any blockers or issues
   - Show recent activity

8. **Suggest next steps** based on feature state:
   - If no spec files: `/sp-spec <description>`
   - If spec but no plan: `/sp-plan`
   - If plan but no tasks: `/sp-task`
   - If tasks exist: Show task completion status and suggest next task

**Usage**
```
/sp-continue <feature-name|feature-id>
```

**Feature Detection Logic**

**By Name:**
```
/sp-continue user-authentication
/sp-continue "user authentication"
/sp-continue auth
```

**By ID:**
```
/sp-continue 001
/sp-continue 002
```

**By Partial Match:**
```
/sp-continue user  # Matches any feature with "user" in name
/sp-continue pay   # Matches "payment-processing"
```

**Context Switching Process**

**When switching features, the system:**

1. **Saves previous context**:
   - Stores previous feature state
   - Notes switch reason and timestamp
   - Preserves all progress tracking data

2. **Loads new context**:
   - Updates `memory/context.md` with new feature
   - Sets working directory context
   - Initializes feature-specific variables

3. **Validates environment**:
   - Checks git repository state
   - Validates feature structure
   - Ensures all necessary files exist

**Examples**

**Continue work on user authentication:**
```
/sp-continue user-authentication
```
Output:
```
## Switching to Feature: 001-user-authentication

### Feature Status
- **Progress**: 65% (16/25 tasks completed)
- **Current Branch**: 001-user-authentication ✓
- **Status**: Active development

### Context Updated
- **Previous Feature**: 002-payment-processing
- **New Feature**: 001-user-authentication
- **Switch Time**: 2025-01-09 14:30:00

### Next Steps
1. Continue with T017: Implement JWT token refresh logic
2. Review T004 blocker: Authentication bug needs security review
3. Plan Phase 2 core features integration

### Recent Activity
- Last work session: 2025-01-08 16:45:00
- Tasks completed in last session: 3
- Current blocker: T004 (Authentication bug)

Use /sp-status for detailed progress or /sp-execute to continue development.
```

**Continue by ID:**
```
/sp-continue 001
```
Output: Same as above, finds feature by ID.

**Continue with partial match:**
```
/sp-continue auth
```
Output: Matches "001-user-authentication" and switches context.

**Continue to new feature:**
```
/sp-continue payment-system
```
Output:
```
## Switching to Feature: 003-payment-system

### Feature Status
- **Progress**: 0% (New feature)
- **Current Branch**: 003-payment-system (created)
- **Status**: Initial setup

### Next Steps
1. Create specification: /sp-spec "payment system integration with Stripe"
2. Generate implementation plan: /sp-plan
3. Break down into tasks: /sp-task

### Structure Created
- specs/003-payment-system/
- plans/003-payment-system/
- tasks/003-payment-system/

Ready to start development!
```

**Multi-Feature Workflow**

**Feature Switching Example:**
```bash
/sp-continue user-auth    # Switch to auth feature
# ... work on auth tasks ...
/sp-continue payment      # Switch to payment feature
# ... work on payment tasks ...
/sp-continue 001          # Switch back to auth by ID
```

**Context Preservation:**
- All feature progress is preserved
- Task status maintained
- Context switching is seamless
- No data loss during switches

**Advanced Features**

**Auto-Detection Enhancement:**
- Fuzzy matching for feature names
- Intelligent ID resolution
- Directory structure validation
- Git branch synchronization

**Context Validation:**
- Feature structure integrity check
- Missing file detection
- Progress consistency validation
- Branch synchronization status

**Intelligent Suggestions:**
Based on feature state analysis:
- **New features**: Suggest starting with `/sp-spec`
- **Spec only**: Suggest `/sp-plan` for implementation planning
- **Plan ready**: Suggest `/sp-task` for task breakdown
- **Tasks available**: Show next pending tasks
- **Blocked features**: Highlight blockers and resolutions

**CLI Integration**

**Try CLI First:**
```bash
specpulse context set current.feature <feature-name>
specpulse continue <feature-name>
specpulse sp-pulse continue <feature-name>
```

**Fallback to Manual Context if CLI Fails:**
1. Update memory/context.md manually
2. Parse feature directories
3. Switch git branches manually
4. Generate status report

**Error Handling**

**Common Issues:**
- Feature not found: List available features
- Branch doesn't exist: Offer to create branch
- Context file corrupted: Rebuild from directory structure
- Git not available: Skip branch switching

**Recovery Options:**
- Create missing feature structure
- Restore context from backup
- Initialize new features automatically
- Provide manual workarounds

**Context File Format**
```yaml
# SpecPulse Context
## Current Feature
- **ID**: 001
- **Name**: user-authentication
- **Branch**: 001-user-authentication
- **Status**: active
- **Created**: 2025-01-09
- **Last Updated**: 2025-01-09
- **Switched To**: 2025-01-09 14:30:00 (via /sp-continue)

## Previous Features
- **002**: payment-processing (switched from at 14:30:00)
```

**Reference**
- Use `specpulse context --help` if you need additional CLI options
- Check `memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- Use `/sp-status` to check feature progress after switching
- Use `/sp-execute` to continue development tasks
<!-- SPECPULSE:END -->