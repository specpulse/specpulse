# SpecPulse CLI Fallback Guide for AI Commands

This guide provides fallback procedures when SpecPulse CLI commands fail, ensuring AI can continue operations.

## 🚨 CLI Failure Detection

AI should detect CLI failures through:
1. **Exit codes**: Non-zero exit codes indicate failure
2. **Error patterns**: "command not found", "No such file", "Permission denied"
3. **Timeout**: Commands taking too long (>30 seconds)
4. **Missing dependencies**: Required tools not available

## 🛠️ Standard Fallback Procedures

### 1. Directory Structure Creation

**CLI Command**: `specpulse feature init <name>`
**Fallback**: Manual directory creation
```bash
# Detect current project root
PROJECT_ROOT=$(pwd)

# Create feature directory structure
FEATURE_DIR="$PROJECT_ROOT/.specpulse/specs/001-feature-name"
mkdir -p "$FEATURE_DIR"
mkdir -p "$PROJECT_ROOT/.specpulse/plans/001-feature-name"
mkdir -p "$PROJECT_ROOT/.specpulse/tasks/001-feature-name"

# Update context.md
echo "### Active Feature: Feature Name" >> "$PROJECT_ROOT/.specpulse/memory/context.md"
echo "- Feature ID: 001" >> "$PROJECT_ROOT/.specpulse/memory/context.md"
```

### 2. Specification Creation

**CLI Command**: `specpulse spec create "description"`
**Fallback**: Manual spec file creation
```bash
# Find next spec number
SPEC_NUM=$(ls "$FEATURE_DIR" | grep "spec-" | wc -l | awk '{printf "%03d", $1+1}')

# Create spec file with embedded template
cat > "$FEATURE_DIR/spec-$SPEC_NUM.md" << 'EOF'
# Specification: [DESCRIPTION]

<!-- FEATURE_DIR: 001-feature-name -->
<!-- FEATURE_ID: 001 -->
<!-- SPEC_NUMBER: SPEC_NUM -->
<!-- STATUS: pending -->
<!-- CREATED: CURRENT_TIMESTAMP -->

## Description
[DESCRIPTION]

## Requirements

### Functional Requirements
- [ ] Requirement 1
- [ ] Requirement 2

### Non-Functional Requirements
- [ ] Performance requirement
- [ ] Security requirement

## Acceptance Criteria

### User Stories
- **As a** [user role], **I want** [functionality], **so that** [benefit]
  - **Given** [context]
  - **When** [action]
  - **Then** [expected outcome]

## Technical Specifications

### Architecture
[Technical details]

### Dependencies
[External dependencies]

## Out of Scope
[What's not included]

## Success Metrics
[How to measure success]

## [NEEDS CLARIFICATION: Any uncertainties?]
EOF
```

### 3. Plan Creation

**CLI Command**: `specpulse plan create "description"`
**Fallback**: Manual plan file creation
```bash
# Find next plan number
PLAN_NUM=$(ls "$PROJECT_ROOT/.specpulse/plans/001-feature-name" | grep "plan-" | wc -l | awk '{printf "%03d", $1+1}')

# Create plan file with embedded template
cat > "$PROJECT_ROOT/.specpulse/plans/001-feature-name/plan-$PLAN_NUM.md" << 'EOF'
# Implementation Plan: [DESCRIPTION]

<!-- FEATURE_DIR: 001-feature-name -->
<!-- FEATURE_ID: 001 -->
<!-- PLAN_NUMBER: PLAN_NUM -->
<!-- STATUS: pending -->
<!-- CREATED: CURRENT_TIMESTAMP -->

## Description
[DESCRIPTION]

## Implementation Phases

### Phase 1: Foundation
- [ ] Task 1.1
- [ ] Task 1.2

### Phase 2: Core Features
- [ ] Task 2.1
- [ ] Task 2.2

### Phase 3: Polish & Testing
- [ ] Task 3.1
- [ ] Task 3.2

## Technology Stack
- [Frontend]: [Technologies]
- [Backend]: [Technologies]
- [Database]: [Database]
- [Infrastructure]: [Infrastructure]

## Timeline
- Phase 1: [X] weeks
- Phase 2: [Y] weeks
- Phase 3: [Z] weeks

## Dependencies
- External: [Dependencies]
- Internal: [Dependencies]

## Risks & Mitigations
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

## Success Criteria
- [ ] [Success criteria 1]
- [ ] [Success criteria 2]
EOF
```

### 4. Task Breakdown

**CLI Command**: `specpulse task breakdown <plan-id>`
**Fallback**: Manual task file creation
```bash
# Create task breakdown marker
cat > "$PROJECT_ROOT/.specpulse/tasks/001-feature-name/_breakdown_from_plan-$PLAN_NUM.md" << 'EOF'
# Task Breakdown Request

**Plan ID**: $PLAN_NUM
**Description**: [Plan description]
**Created**: CURRENT_TIMESTAMP

## Tasks Generated from Plan

### Task Categories
- [ ] Backend Development
- [ ] Frontend Development
- [ ] Database Setup
- [ ] Testing

### Next Steps
1. Create individual task files
2. Assign task numbers
3. Define acceptance criteria
4. Set up dependencies
EOF

# Create initial task files
TASK_NUM=1

# Example task file
cat > "$PROJECT_ROOT/.specpulse/tasks/001-feature-name/task-$TASK_NUM.md" << 'EOF'
# Task T$TASK_NUM: [Task Title]

<!-- TASK_NUMBER: TASK_NUM -->
<!-- STATUS: pending -->
<!-- CREATED: CURRENT_TIMESTAMP -->

## Description
[Task description]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Implementation Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Dependencies
- [Depends on other tasks]

## Testing
- [Unit tests]
- [Integration tests]

## Notes
[Any additional notes]
EOF
```

### 5. Task Execution

**CLI Command**: `specpulse execute status`
**Fallback**: Manual task tracking
```bash
# Read task files and show status
echo "## Current Task Status"

for task_file in "$PROJECT_ROOT/.specpulse/tasks/001-feature-name"/task-*.md; do
    if [ -f "$task_file" ]; then
        task_name=$(basename "$task_file" .md)
        status=$(grep "<!-- STATUS:" "$task_file" | sed 's/.*STATUS: \([a-z_]*\).*/\1/')

        case $status in
            "completed")
                echo "✓ $task_name: Completed"
                ;;
            "in_progress")
                echo "> $task_name: In Progress"
                ;;
            *)
                echo "○ $task_name: Pending"
                ;;
        esac
    fi
done
```

## 🔄 Standard Error Recovery

### Permission Errors
```bash
# Try fixing permissions
chmod -R 755 "$PROJECT_ROOT/.specpulse"

# If still fails, work in temp directory
TEMP_DIR=$(mktemp -d)
echo "Working in temporary directory: $TEMP_DIR"
```

### Path Issues
```bash
# Convert to absolute paths
PROJECT_ROOT=$(pwd -P)

# Handle Windows paths
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    PROJECT_ROOT=$(cygpath -w "$PROJECT_ROOT")
fi
```

### Template Missing
```bash
# Use embedded templates as shown above
# Log the missing template
echo "Warning: Template not found, using embedded fallback" >&2
```

## 📋 Validation Without CLI

### Manual Spec Validation
```bash
validate_spec() {
    local spec_file="$1"

    echo "## Validating: $spec_file"

    # Check for required sections
    required_sections=("Description" "Requirements" "Acceptance Criteria" "Technical Specifications")

    for section in "${required_sections[@]}"; do
        if grep -q "^## $section" "$spec_file"; then
            echo "✓ Found: $section"
        else
            echo "✗ Missing: $section"
        fi
    done

    # Check for clarification markers
    clarification_count=$(grep -c "\[NEEDS CLARIFICATION:" "$spec_file")
    if [ "$clarification_count" -gt 0 ]; then
        echo "⚠ $clarification_count clarifications needed"
    else
        echo "✓ No clarifications needed"
    fi
}
```

## 🤖 AI Integration Best Practices

### Always Try CLI First
1. **Execute CLI command with timeout**
2. **Check exit code and output**
3. **If failed, apply fallback immediately**
4. **Log the fallback usage**

### Error Handling Pattern
```python
# AI should use this pattern:
try:
    result = run_cli_command("specpulse spec create", description)
    if result.success:
        return result
except CLIError:
    log_warning("CLI failed, using manual fallback")
    return manual_spec_creation(description)
```

### Fallback Logging
Always log when fallbacks are used:
```bash
echo "[FALLBACK] CLI command failed: $cmd" >&2
echo "[FALLBACK] Using manual procedure" >&2
```

## 📞 Getting Help

If fallbacks fail repeatedly:

1. **Check SpecPulse Installation**
   ```bash
   python -m specpulse --version
   pip list | grep specpulse
   ```

2. **Check Environment**
   ```bash
   python --version
   which specpulse
   echo $PATH
   ```

3. **Manual Recovery**
   - Create directory structure manually
   - Use embedded templates
   - Track progress in simple text files
   - Focus on core functionality over tooling

## ✅ Success Criteria

Fallback is successful when:
- [ ] Files are created in correct locations
- [ ] Content follows expected format
- [ ] Metadata is properly set
- [ ] Progress can be tracked
- [ ] User can continue work without CLI

## 🚨 When to Escalate

Escalate to manual intervention when:
- Multiple fallbacks fail in sequence
- Critical system dependencies are missing
- File permissions cannot be resolved
- User reports persistent issues

Remember: **AI should always enable work to continue, even when tooling fails!**