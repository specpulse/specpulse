---
name: pulse
description: Initialize a new feature with SpecPulse framework
allowed_tools:
  - Bash
  - Read
  - Write
  - Edit
---

# /pulse Command

Initialize a new feature following SpecPulse methodology.

## Usage
```
/pulse <feature-name>
```

## Implementation

When called with `/pulse $ARGUMENTS`, I will:

1. **Extract feature name** from `$ARGUMENTS`
2. **Run initialization script**: `bash scripts/pulse-init.sh "$ARGUMENTS"`
3. **Create feature structure**:
   - Generate feature ID (001, 002, etc.)
   - Create directories: `specs/XXX-feature/`, `plans/XXX-feature/`, `tasks/XXX-feature/`
   - Copy templates to feature directories
   - Update `memory/context.md` with current feature
   - Create git branch if in git repository

4. **Report results** to user with created structure

## Example
```
User: /pulse user-authentication
```

I will:
- Run: `bash scripts/pulse-init.sh "user-authentication"`
- Create: `specs/001-user-authentication/spec.md`
- Create: `plans/001-user-authentication/plan.md`  
- Create: `tasks/001-user-authentication/tasks.md`
- Switch to branch: `001-user-authentication` (if git)
- Report success and next steps

## Next Steps
After initialization:
- Use `/spec` to create the specification
- Use `/plan` to generate implementation plan
- Use `/task` to break down into tasks