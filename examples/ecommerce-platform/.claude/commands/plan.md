---
name: plan
description: Generate or validate implementation plans
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
---

# /plan Command

Generate implementation plans from specifications following SpecPulse methodology.

## Usage
```
/plan [action]
```

Actions: `generate`, `validate` (defaults to `generate`)

## Implementation

When called with `/plan $ARGUMENTS`, I will:

1. **Parse arguments** to determine action:
   - If `$ARGUMENTS` is `validate`: Check plan against constitution
   - Otherwise: Generate new plan

2. **For `/plan generate` or `/plan`:**
   a. **Read current specification** from `specs/XXX-feature/spec.md`
   
   b. **Run Phase Gates checks**:
   - Constitutional compliance
   - Simplicity check (≤3 modules)
   - Test-first strategy defined
   - Framework selection complete
   - Research completed

   c. **Generate plan sections**:
   - Technology stack
   - Architecture overview
   - Implementation phases
   - API contracts
   - Data models
   - Testing strategy

   d. **Track complexity**:
   - If >3 modules, document justification
   - Create simplification roadmap

   e. **Write plan** to `plans/XXX-feature/plan.md`

3. **For `/plan validate`:**
   - Read existing plan from `plans/XXX-feature/plan.md`
   - Verify Phase Gates compliance
   - Check complexity tracking
   - Ensure test-first approach
   - Validate framework choices
   - Report validation results

## Phase Gates (Phase -1)
Must pass before implementation:
- ✅ Using ≤3 projects/modules
- ✅ Tests defined before code
- ✅ Using framework features directly
- ✅ No premature abstractions
- ✅ Research completed

## Example
```
/plan generate
```