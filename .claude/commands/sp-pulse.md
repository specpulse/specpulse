---
name: sp-pulse
description: Initialize a new feature with SpecPulse framework
allowed_tools:
  - Bash
  - Read
  - Write
  - Edit
  - TodoWrite
---

# /sp-pulse Command

Initialize a new feature following SpecPulse methodology with SDD compliance.

## CRITICAL: LLM Workflow Rules

**PRIMARY WORKFLOW: Use CLI when available**
- Always prefer `specpulse` CLI commands over direct file operations
- Use Bash tool ONLY for CLI commands, not for file editing
- Only use Read/Write/Edit tools when CLI doesn't provide functionality

**PROTECTED DIRECTORIES (NEVER EDIT):**
- `templates/` - Template files
- `.specpulse/` - Internal config
- `specpulse/` - Package code
- `.claude/` and `.gemini/` - AI configuration

**ALLOWED DIRECT EDITS (When NO CLI exists):**
- `specs/` - Feature specifications (create/edit spec files)
- `plans/` - Implementation plans (create/edit plan files)
- `tasks/` - Task breakdowns (create/edit task files)
- `memory/` - Project context (update context.md, decisions.md)

## Usage
```
/sp-pulse <feature-name> [feature-id]
```

## Implementation

When called with `/sp-pulse $ARGUMENTS`, I will:

1. **Validate arguments** and extract feature name + optional ID
2. **Try CLI first (if feature init exists)**:
   ```bash
   specpulse feature init feature-name
   ```
   If this succeeds, STOP HERE. CLI handles everything.

3. **If CLI doesn't exist, use File Operations**:

   - **Step 1: Determine Feature ID**
     ```
     Read: specs/ directory (list subdirectories)
     Find highest number (e.g., 001, 002) and increment
     Or use 001 if no features exist
     ```

   - **Step 2: Create Feature Directories Using Bash**
     ```bash
     mkdir -p specs/001-feature-name
     mkdir -p plans/001-feature-name
     mkdir -p tasks/001-feature-name
     ```

   - **Step 3: Update Context File**
     ```
     Read: memory/context.md
     Edit: memory/context.md
     (Add new feature entry with ID, name, timestamp)
     ```

   - **Step 4: Create Git Branch (Optional)**
     ```bash
     git checkout -b 001-feature-name
     ```

4. **Suggest specification creation**:
   - Provide user with 2-3 AI-generated specification suggestions
   - Ask user to choose one or create custom specification
   - Guide user to use `/sp-spec` command after making selection

5. **Validate structure** and report comprehensive status

## SDD Compliance

**Principle 1: Specification First**
- [ ] Feature name is clear and specific
- [ ] Ready for requirements documentation
- [ ] Structure supports specifications

**Principle 2: Incremental Planning**
- [ ] Initial structure supports phased development
- [ ] Templates ready for iterative work
- [ ] Supports any project type

## Example
```
User: /sp-pulse user-authentication-oauth2
```

I will:
- Create feature structure using CLI calls
- Set context: `specpulse context set current.feature "user-authentication-oauth2"`
- Update context: `specpulse context set current.feature_id "001"`
- Create: `specs/001-user-authentication-oauth2/` (empty, ready for spec)
- Create: `plans/001-user-authentication-oauth2/` (empty, ready for plan)
- Create: `tasks/001-user-authentication-oauth2/` (empty, ready for tasks)
- Branch: `001-user-authentication-oauth2`
- Suggest specification options:
  1. "User authentication with OAuth2 providers and JWT tokens"
  2. "Complete authentication system including registration, login, and profile management"
  3. "OAuth2 integration with social login providers"
- Ask: "Which specification would you like to use? (Choose 1-3 or provide your own)"
- Guide: "After choosing, use `/sp-spec [your choice]` to create the specification"
- Status: `STATUS=ready_for_spec, BRANCH_NAME=001-user-authentication-oauth2`

## Error Handling

Enhanced validation includes:
- Feature name sanitization (alphanumeric, hyphens only)
- Directory creation validation
- Template existence verification
- Git repository validation
- Context file management

## Manual Workflow

The `/sp-pulse` command creates the feature structure and then guides you through manual steps:

1. **Phase -1**: **MANUAL** - Use `/sp-spec` to create specification with AI assistance
2. **Phase 0**: **MANUAL** - Use `/sp-plan` to generate implementation plan  
3. **Phase 1**: **MANUAL** - Use `/sp-task` to create task breakdown
4. **Implementation**: Begin development following SDD principles

## Context Detection

The system automatically detects which feature you're working on:
- Checks `memory/context.md` for current feature
- Uses git branch name if available
- Falls back to most recently created feature directory
- You can also specify feature directory explicitly in commands

## Integration Features

- **Automatic context tracking** in `memory/context.md`
- **Enhanced error reporting** with specific failure reasons
- **Git integration** with branch management
- **Template validation** before copying
- **Todo list creation** for progress tracking
- **Cross-platform script execution** with Bash
- **Platform-agnostic operation** for any development environment

## Feature Progress Tracking

The system tracks progress across all features:

### Active Features Overview
```
FEATURE_COUNT=3
ACTIVE_FEATURE=001-user-authentication
COMPLETED_FEATURES=1
IN_PROGRESS_FEATURES=2
```

### Context Management
- `memory/context.md` tracks current active feature
- Progress percentages calculated from task completion
- Feature status: active, completed, paused, blocked
- Automatic context switching when working on different features

### Multi-Feature Workflow
```
/sp-pulse feature-a → /sp-spec → /sp-plan → /sp-task → [work]
/sp-pulse feature-b → /sp-spec → /sp-plan → /sp-task → [work]
/sp-status feature-a → Check progress → /sp-continue feature-a
```

### Feature Switching
When you have multiple features, the system helps you:
- List all existing features with their status
- Switch context between features
- Continue work from where you left off
- Track overall project progress across all features