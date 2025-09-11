# /pulse

Initialize a new feature with SpecPulse framework.

## Usage
```
/pulse init <feature-name>
```

## What This Does
1. Runs `scripts/pulse-init.sh <feature-name>` to:
   - Create feature ID (001, 002, etc.)
   - Create branch name (001-feature-name)
   - Create directories: specs/, plans/, tasks/
   - Copy templates to feature directories
   - Update memory/context.md
   - Create git branch if in git repo

2. Reports the created structure back to user

## Example
```
/pulse init user-authentication
```

Creates:
- Branch: 001-user-authentication
- specs/001-user-authentication/spec.md
- plans/001-user-authentication/plan.md
- tasks/001-user-authentication/tasks.md

## Next Steps
After initialization, use:
- `/spec create` to write the specification
- `/plan generate` to create implementation plan
- `/task breakdown` to generate tasks