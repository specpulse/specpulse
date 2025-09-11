---
name: spec
description: Create or manage feature specifications
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
---

# /spec Command

Create, update, or validate feature specifications using SpecPulse methodology.

## Usage
```
/spec [action] [description]
```

Actions: `create`, `update`, `validate` (defaults to `create`)

## Implementation

When called with `/spec $ARGUMENTS`, I will:

1. **Parse arguments** to determine action:
   - If starts with `create`: Generate new specification
   - If starts with `update`: Modify existing specification
   - If starts with `validate`: Check specification completeness
   - If no action specified: Default to `create` with full arguments as description

2. **For `/spec create [description]` or `/spec [description]`:**
   - Read template from `templates/spec.md`
   - Parse the description to identify:
     - Functional requirements (Must/Should/Could have)
     - User stories and acceptance criteria
     - Technical requirements
   - Mark any uncertainties with `[NEEDS CLARIFICATION: detail]`
   - Find current feature directory (latest in specs/)
   - Write specification to `specs/XXX-feature/spec.md`

3. **For `/spec update`:**
   - Read existing specification
   - Ask user for clarifications or changes
   - Update content while preserving structure
   - Remove resolved `[NEEDS CLARIFICATION]` markers

4. **For `/spec validate`:**
   - Check all required sections are filled
   - Count `[NEEDS CLARIFICATION]` markers
   - Verify acceptance criteria are testable
   - Report validation results

## Examples

### Creating a new specification
```
User: /spec user authentication with OAuth2 and email/password
```
I will create a comprehensive specification with all requirements.

### Updating existing specification
```
User: /spec update
```
I will read the current spec and guide through updates.

### Validating specification
```
User: /spec validate
```
I will check completeness and report any issues.

## Template Structure
The specification follows this structure:
- Project Overview
- Functional Requirements (Must/Should/Could have)
- User Stories with Acceptance Criteria  
- Technical Specifications
- Clarifications Needed
- Validation Checklist