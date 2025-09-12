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

Initialize a new feature following SpecPulse methodology with constitutional compliance.

## CRITICAL SECURITY NOTE
**NEVER edit files in these protected directories:**
- `templates/` - Template files (spec.md, plan.md, task.md)
- `scripts/` - Shell scripts (sp-pulse-*.sh)
- `commands/` - AI command definitions
- `.claude/` and `.gemini/` - AI configuration files

**ONLY create and edit files in:**
- `specs/` - Feature specifications
- `plans/` - Implementation plans
- `tasks/` - Task breakdowns
- `memory/` - Project context (context.md, decisions.md)

## Usage
```
/sp-pulse <feature-name> [feature-id]
```

## Implementation

When called with `/sp-pulse $ARGUMENTS`, I will:

1. **Validate arguments** and extract feature name + optional ID
2. **Run initialization script**:
   - `bash scripts/sp-pulse-init.sh "$FEATURE_NAME" "$OPTIONAL_ID"`
3. **Create complete feature structure**:
   - Generate feature ID (001, 002, etc.) or use provided ID
   - Create sanitized branch name: `ID-feature-name`
   - Create directories: `specs/ID-feature-name/`, `plans/ID-feature-name/`, `tasks/ID-feature-name/`
   - Copy AI-optimized templates to feature directories
   - Update `memory/context.md` with current feature metadata
   - Create and switch to git branch if in git repository

4. **Suggest specification creation**:
   - Provide user with 2-3 AI-generated specification suggestions
   - Ask user to choose one or create custom specification
   - Guide user to use `/sp-spec` command after making selection

5. **Validate structure** and report comprehensive status

## Constitutional Compliance

**Article I: Simplicity**
- [ ] Feature name is clear and specific
- [ ] No unnecessary abstractions in initial structure
- [ ] Single responsibility per feature

**Article II: Anti-Abstraction**  
- [ ] Direct template usage (no wrapper layers)
- [ ] Minimal initial structure
- [ ] Framework-ready files

## Example
```
User: /sp-pulse user-authentication-oauth2
```

I will:
- Run: `bash scripts/sp-pulse-init.sh "user-authentication-oauth2"`
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
4. **Implementation**: Begin development following constitutional principles

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