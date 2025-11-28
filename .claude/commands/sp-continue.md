---
name: sp-continue
description: Switch context and continue work on a specific feature
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-continue Command

Switch context to a specific feature and continue work from where you left off.

## Usage
```
/sp-continue <feature-name|feature-id>
```

## Implementation

When called with `/sp-continue $ARGUMENTS`, I will:

1. **Parse arguments** to extract feature name or ID
2. **Find feature directory** using context detection:
   - Search for matching feature directory (specs/*, plans/*, tasks/*)
   - Support partial matching (e.g., "auth" matches "001-user-authentication")
   - Support ID matching (e.g., "001" matches "001-user-authentication")

3. **Validate feature exists**:
   - Check if feature directory has any files
   - Verify feature structure is intact
   - Report if feature not found

4. **Update context** in `memory/context.md`:
   ```yaml
   # Feature Context
   
   ## Current Feature
   - **ID**: 001
   - **Name**: user-authentication
   - **Branch**: 001-user-authentication
   - **Status**: active
   - **Created**: 2025-01-09
   - **Last Updated**: 2025-01-09
   - **Switched To**: 2025-01-09 (via /continue)
   ```

5. **Switch git branch** if in git repository:
   - Checkout feature branch if it exists
   - Report if branch doesn't exist
   - Handle branch switching errors gracefully

6. **Display feature status**:
   - Show current progress percentage
   - List next available actions
   - Highlight any blockers or issues
   - Show recent activity

7. **Suggest next steps** based on feature state:
   - If no spec files: `/spec <description>`
   - If spec but no plan: `/plan`
   - If plan but no tasks: `/task`
   - If tasks exist: Show task completion status and suggest next task

## Feature Detection Logic

The command supports multiple ways to identify features:

### By Name
```
/sp-continue user-authentication
/sp-continue "user authentication"
/sp-continue auth
```

### By ID
```
/sp-continue 001
/sp-continue 002
```

### By Partial Match
```
/sp-continue user  # Matches any feature with "user" in name
/sp-continue pay   # Matches "payment-processing"
```

## Context Switching

When switching features, the system:

1. **Saves previous context**:
   - Stores previous feature state
   - Notes switch reason and timestamp
   - Preserves all progress tracking data

2. **Loads new context**:
   - Updates `memory/context.md` with new feature
   - Loads feature metadata
   - Calculates current progress

3. **Environment setup**:
   - Switches git branch if available
   - Updates working directory context
   - Prepares for continued development

## Examples

### Basic feature switch
```
User: /sp-continue user-authentication
```

I will:
- Find feature: `001-user-authentication`
- Update context: Switch from current feature to `001-user-authentication`
- Switch git branch: `git checkout 001-user-authentication`
- Display status:
  ```
  ## Switched to Feature: 001-user-authentication
  
  **Progress**: 65% complete
  **Status**: Active
  **Last Worked**: 2025-01-09
  
  ### Next Steps
  - 16 tasks completed, 9 remaining
  - 1 blocker: T015 (Database schema approval)
  - Suggested action: /sp-status user-authentication for details
  ```

### Continue with ID
```
User: /sp-continue 002
```

I will:
- Find feature: `002-payment-processing`
- Switch context and display feature status

### Feature not found
```
User: /sp-continue non-existent-feature
```

I will:
- Search for matching features
- Show available features:
  ```
  Feature "non-existent-feature" not found.
  
  Available features:
  - 001-user-authentication (65%)
  - 002-payment-processing (23%)
  - 003-user-profile (45%)
  
  Use /sp-status to see all features.
  ```

## Integration Features

- **Intelligent feature matching** with partial name and ID support
- **Context preservation** when switching between features
- **Git integration** with automatic branch switching
- **Progress tracking** across feature switches
- **Smart suggestions** for next actions based on feature state
- **Error recovery** with helpful fallback options
- **Cross-platform compatibility** for any development environment

## Error Handling

- Feature not found with suggestions
- Git branch switching errors
- Context file permission issues
- Directory structure validation
- Progress calculation errors
- Working directory validation

## Multi-Feature Workflow

The `/continue` command enables efficient multi-feature development:

```
# Start new feature
/sp-pulse new-feature
/sp-spec "feature description"
/sp-plan
/sp-task

# Switch to existing feature
/sp-continue user-authentication

# Check status and continue work
/sp-status user-authentication
# ... complete some tasks ...

# Switch back to new feature
/sp-continue new-feature
```

This enables developers to context-switch between multiple active features while maintaining progress tracking and development context.