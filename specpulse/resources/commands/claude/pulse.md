---
name: pulse
description: Initialize a new feature with SpecPulse framework
allowed_tools:
  - Bash
  - Read
  - Write
  - Edit
  - TodoWrite
---

# /pulse Command

Initialize a new feature following SpecPulse methodology with constitutional compliance.

## Usage
```
/pulse <feature-name> [feature-id]
```

## Implementation

When called with `/pulse $ARGUMENTS`, I will:

1. **Validate arguments** and extract feature name + optional ID
2. **Run initialization script** with cross-platform detection:
   - **Windows**: `powershell scripts/pulse-init.ps1 "$FEATURE_NAME" "$OPTIONAL_ID"`
   - **Linux/macOS**: `bash scripts/pulse-init.sh "$FEATURE_NAME" "$OPTIONAL_ID"`
   - **Python Fallback**: `python scripts/pulse-init.py "$FEATURE_NAME" "$OPTIONAL_ID"`
3. **Create complete feature structure**:
   - Generate feature ID (001, 002, etc.) or use provided ID
   - Create sanitized branch name: `ID-feature-name`
   - Create directories: `specs/ID-feature-name/`, `plans/ID-feature-name/`, `tasks/ID-feature-name/`
   - Copy AI-optimized templates to feature directories
   - Update `memory/context.md` with current feature metadata
   - Create and switch to git branch if in git repository

4. **Validate structure** and report comprehensive status
5. **Create todo list** for tracking feature development progress

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
User: /pulse user-authentication-oauth2
```

I will:
- Run: `bash scripts/pulse-init.sh "user-authentication-oauth2"`
- Create: `specs/001-user-authentication-oauth2/spec.md`
- Create: `plans/001-user-authentication-oauth2/plan.md`  
- Create: `tasks/001-user-authentication-oauth2/tasks.md`
- Branch: `001-user-authentication-oauth2`
- Status: `STATUS=initialized, BRANCH_NAME=001-user-authentication-oauth2`

## Error Handling

Enhanced validation includes:
- Feature name sanitization (alphanumeric, hyphens only)
- Directory creation validation
- Template existence verification
- Git repository validation
- Context file management

## Next Steps (Constitutional Order)

1. **Phase -1**: Use `/spec` to create specification with constitutional gates
2. **Phase 0**: Use `/plan` to generate implementation plan with complexity tracking
3. **Phase 1**: Use `/task` to break down into executable tasks
4. **Implementation**: Begin development following constitutional principles

## Integration Features

- **Automatic context tracking** in `memory/context.md`
- **Enhanced error reporting** with specific failure reasons
- **Git integration** with branch management
- **Template validation** before copying
- **Todo list creation** for progress tracking
- **Cross-platform script execution** with automatic detection
- **Multiple language support**: Bash, PowerShell, Python
- **Platform-agnostic operation** for any development environment