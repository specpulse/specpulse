---
name: sp-validate
description: Validate current specifications, plans, or tasks
allowed_tools:
  - Read
  - Bash
  - TodoWrite
---

# /sp-validate Command

Validate project components for completeness and SDD compliance.

## Usage
```
/sp-validate                  # Validate current spec
/sp-validate spec             # Validate specifications
/sp-validate plan             # Validate plans
/sp-validate task             # Validate tasks
/sp-validate all              # Validate everything
```

## Implementation

When called with `/sp-validate $ARGUMENTS`, I will:

1. **Parse validation target**:
   - If `spec`: Validate specifications
   - If `plan`: Validate plans
   - If `task`: Validate tasks
   - If `all`: Validate everything
   - If no argument: Default to current spec

2. **For spec validation**:
   - Read current spec file
   - Check required sections present:
     * Executive Summary
     * Problem Statement
     * Functional Requirements
     * User Stories
     * Acceptance Criteria
     * Technical Constraints
   - Count `[NEEDS CLARIFICATION]` markers
   - Verify Given-When-Then format in acceptance criteria
   - Run CLI validation:
     ```bash
     specpulse validate spec --verbose
     ```

3. **For plan validation**:
   - Read plan file
   - Check phases defined
   - Verify task breakdown exists
   - Check dependencies mapped
   - Run CLI validation:
     ```bash
     specpulse validate plan
     ```

4. **For task validation**:
   - Read task files
   - Check status fields present
   - Verify dependencies listed
   - Check acceptance criteria
   - Run CLI validation:
     ```bash
     specpulse validate task
     ```

5. **Report results**:
   - Show validation status (✓ or ✗)
   - List missing sections
   - Count clarifications needed
   - Suggest fixes
   - Recommend next steps

## Examples

### Validate current spec
```
User: /sp-validate

Output:
✓ Specification Validation Results

  File: specs/001-user-auth/spec-001.md
  Status: Complete ✓

  Sections: 12/12 complete
  Clarifications: 0 needed
  Acceptance Criteria: 8 defined

  ✓ Ready for /sp-plan
```

### Validate with issues
```
User: /sp-validate spec

Output:
✗ Specification Validation Results

  File: specs/001-user-auth/spec-001.md
  Status: Incomplete

  Missing Sections:
    - Non-functional requirements
    - Risk assessment

  Clarifications: 3 needed
    1. Database type
    2. Authentication method
    3. Deployment target

  → Next: /sp-clarify to resolve questions
```

### Validate all
```
User: /sp-validate all

Output:
📊 Complete Project Validation

  Specifications: 2 files
    ✓ spec-001.md - Complete
    ✗ spec-002.md - Missing sections

  Plans: 1 file
    ✓ plan-001.md - Complete

  Tasks: 5 files
    ✓ All tasks valid

  Overall: 90% complete

  → Next: Fix spec-002.md issues
```

## Output Format

Use clear, structured output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VALIDATION RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 File: specs/001-feature/spec-001.md

✓ Complete Sections (10/12):
  • Executive Summary
  • Problem Statement
  • Functional Requirements
  • User Stories
  ... (show all complete)

✗ Missing Sections (2/12):
  • Risk Assessment
  • Deployment Strategy

⚠️ Clarifications Needed (3):
  1. Database type selection
  2. Authentication mechanism
  3. Performance requirements

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Resolve clarifications: /sp-clarify
2. Or proceed with warnings: /sp-plan generate
3. Or fix manually and re-validate
```

## Integration with Workflow

After validation:
- ✓ **Complete**: Proceed to `/sp-plan`
- ⚠️ **Clarifications needed**: Use `/sp-clarify`
- ✗ **Missing sections**: Update spec manually or use `/sp-spec update`

## CLI Integration

Uses SpecPulse CLI for validation:
```bash
specpulse validate spec --verbose
specpulse validate plan
specpulse validate task
specpulse validate all --fix
```

Output is parsed and presented in user-friendly format.
