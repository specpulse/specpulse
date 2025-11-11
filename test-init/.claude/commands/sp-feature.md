---
name: sp-feature
description: Initialize a new feature (alias for sp-pulse)
allowed_tools:
  - Bash
  - Read
  - Write
  - Edit
  - TodoWrite
---

# /sp-feature Command

**Alias for `/sp-pulse`** - Initialize a new feature with SpecPulse framework.

## Usage
```
/sp-feature <feature-name> [feature-id]
```

## Implementation

This command is identical to `/sp-pulse` but provides a more intuitive name for feature initialization. It follows the exact same workflow as `/sp-pulse`:

1. **CLI First Approach**: Try `specpulse feature init <name>` command
2. **Fallback to File Operations**: If CLI fails, create directories manually
3. **Smart Specification Suggestions**: Generate 3 context-aware specification options
4. **Project Structure Setup**: Create complete feature directory structure
5. **Context Management**: Update project context and git integration

## Specification Suggestions

The command analyzes the feature name and provides intelligent suggestions:

- **Core Specification** (2-4 hours): Essential functionality
- **Standard Specification** (8-12 hours): Comprehensive features
- **Complete Specification** (16-24 hours): Full-featured solution

Each suggestion includes:
- Project type detection (web app, API, mobile, etc.)
- Complexity assessment
- Estimated development time
- Tailored requirements based on feature name analysis

## Examples

```bash
# Web application feature
/sp-feature user-dashboard

# API service
/sp-feature payment-api

# Mobile app component
/sp-feature notification-system

# With custom feature ID
/sp-feature authentication 005
```

## Integration

After feature initialization, continue with:
```bash
/sp-spec core              # Create specification using core approach
/sp-plan                    # Generate implementation plan
/sp-task                    # Create task breakdown
```

## Documentation

For complete fallback procedures when CLI fails, see:
`.specpulse/docs/AI_FALLBACK_GUIDE.md`

---

*Alias for /sp-pulse command*
*SpecPulse v2.4.9*