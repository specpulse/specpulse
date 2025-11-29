---
name: sp-pulse
description: Initialize new features and manage project context without SpecPulse CLI
version: "1.0"
agent: specpulse-assistant
workflow_type: feature_initialization
---

# SpecPulse Feature Initialization Workflow

This workflow implements complete CLI-independent feature initialization with atomic operations and Universal ID System.

## Agent Capabilities Required

- File operations: Read, Write, Edit, Bash, Glob
- Directory traversal protection
- Atomic file operation handling
- Error recovery and rollback mechanisms

## Workflow Steps

### Step 1: Argument Parsing and Action Determination

**Parse input arguments:**
```yaml
inputs:
  feature_name: string
  action: enum [create, status, list]
```

**Action logic:**
- Parse the command arguments:
  - If feature_name provided → Initialize new feature
  - If action=status → Show current feature context
  - If action=list → Show all available features
  - If no input → Show current feature status

### Step 2: Universal Feature ID Generation

**Algorithm:**
1. Use Glob tool to scan `.specpulse/specs/` directory
2. Parse directory names with regex `(\d+)-(.+)` pattern
3. Extract numeric IDs and convert to integers
4. Find maximum: `max_id = max(extracted_ids)` or 0 if empty
5. Generate next sequential: `next_id = max_id + 1`
6. Zero-pad: `feature_id = format(next_id, '03d')`
7. Create feature name from input (kebab-case)

**Conflict prevention:**
- Atomic file existence checks
- Validation loop with increment/retry
- Gap handling (preserve existing gaps)

### Step 3: Atomic Directory Structure Creation

**Create directories with rollback:**
```yaml
directory_structure:
  - .specpulse/specs/[feature_id]-[feature_name]/
  - .specpulse/plans/[feature_id]-[feature_name]/
  - .specpulse/tasks/[feature_id]-[feature_name]/
  - .specpulse/memory/
```

**Atomic operations:**
- Use `bash mkdir -p` for atomic creation
- Validate each step before proceeding
- Track all operations for rollback
- Rollback mechanism on failure

### Step 4: Safe File Operations

**Specification initialization:**
- Create `spec-001.md` with comprehensive template
- Include executive summary, functional requirements
- Include user stories and acceptance criteria template
- Add technical constraints and risk assessment sections

**Context management:**
- Update `.specpulse/memory/context.md` with feature metadata
- Set ID, name, created_at, status
- Initialize decision log for the feature
- Create feature-specific memory tracking

### Step 5: Universal ID System Integration

**File numbering:**
- Specifications: `spec-001.md`, `spec-002.md`, etc.
- Plans: `plan-001.md`, `plan-002.md`, etc.
- Tasks: `tasks-001.md`, `tasks-002.md`, etc.
- Service tasks: `SERVICE-T001.md`, `SERVICE-T002.md`, etc.

**Conflict resolution:**
- Systematic numbering analysis
- Atomic file existence validation
- Intelligent conflict detection and resolution

### Step 6: Error Handling and Recovery

**Comprehensive error recovery:**
```yaml
error_scenarios:
  feature_creation_failure:
    action: Guide through directory permissions
  directory_exists:
    action: Handle existing feature directories gracefully
  file_system_errors:
    action: Provide recovery instructions
  template_missing:
    action: Use built-in fallback structure
  context_corrupted:
    action: Rebuild from available feature data
  permission_denied:
    action: Clear resolution instructions
```

**Data protection:**
- Backup creation before major changes
- Validation checks after operations
- Recovery procedures from backups
- Consistency maintenance

## Output Format

**Success response:**
```yaml
feature:
  id: "001"
  name: "user-authentication"
  directory: "001-user-authentication"
  status: "initialized"
  created_at: "2025-01-11T16:30:00Z"
  progress: 5%

structure:
  directories_created: 4
  files_created: 2
  context_updated: true
  git_branch: "feature/001-user-authentication"

next_steps:
  - "Create specification: /sp-spec 'detailed requirements'"
  - "Generate plan: /sp-plan"
  - "Break down tasks: /sp-task"
  - "Execute tasks: /sp-execute"
```

## Safety Constraints

- **Path validation**: Only operate within `.specpulse/` directory
- **Protected directories**: Never modify `templates/`, `specpulse/`, AI configs
- **Permission checks**: Validate read/write access before operations
- **Atomic operations**: Prevent partial updates and corruption
- **Rollback capability**: Restore original state on failures

## Integration Features

- **Git integration**: Automatic branch creation and management
- **Template system**: Built-in templates for all file types
- **Context management**: File-based context tracking
- **Progress monitoring**: Manual calculation from file structure
- **Cross-platform compatibility**: Identical functionality across platforms