---
name: spec
description: Create or manage feature specifications using AI-optimized templates
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /spec Command

Create, update, or validate feature specifications using SpecPulse methodology with AI-optimized templates.

## Usage
```
/spec [action] [description|feature-name]
```

Actions: `create`, `update`, `validate`, `clarify` (defaults to `create`)

## Implementation

When called with `/spec $ARGUMENTS`, I will:

1. **Parse arguments** to determine action:
   - If starts with `create`: Generate new specification
   - If starts with `update`: Modify existing specification
   - If starts with `validate`: Check specification completeness
   - If starts with `clarify`: Address [NEEDS CLARIFICATION] markers
   - If no action specified: Default to `create` with full arguments as description

2. **For `/spec create [description]` or `/spec [description]`:**
   - Read AI-optimized template from `templates/spec.md`
   - Parse the description to identify:
     - Functional requirements (Must/Should/Could/Won't have)
     - User stories with testable acceptance criteria
     - Technical specifications and constraints
     - Success metrics and out-of-scope items
   - Generate specification using Jinja2-style template variables:
     ```markdown
     # Specification: {{ feature_name }}
     ## Metadata
     - **ID**: SPEC-{{ feature_id }}
     - **Created**: {{ date }}
     ```
   - Mark any uncertainties with `[NEEDS CLARIFICATION: specific question]`
   - Find current feature directory from context or create new
   - Write specification to `specs/ID-feature-name/spec.md`
   - Run enhanced validation with cross-platform detection:
     - **Windows**: `powershell scripts/pulse-spec.ps1 "$FEATURE_DIR"`
     - **Linux/macOS**: `bash scripts/pulse-spec.sh "$FEATURE_DIR"`
     - **Python Fallback**: `python scripts/pulse-spec.py "$FEATURE_DIR"`

3. **For `/spec update`:**
   - Read existing specification from current context
   - Parse update requests and identify sections to modify
   - Update content while preserving AI-friendly template structure
   - Remove resolved `[NEEDS CLARIFICATION]` markers
   - Run validation to ensure completeness

4. **For `/spec validate`:**
   - Read current specification
   - Check all required sections using enhanced validation:
     ```bash
     # Cross-platform detection
     if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
         powershell scripts/pulse-spec.ps1 "$FEATURE_DIR"
     else
         bash scripts/pulse-spec.sh "$FEATURE_DIR" || python scripts/pulse-spec.py "$FEATURE_DIR"
     fi
     ```
   - Count `[NEEDS CLARIFICATION]` markers
   - Verify acceptance criteria follow Given-When-Then format
   - Check constitutional compliance indicators
   - Report detailed validation results

5. **For `/spec clarify`:**
   - Find all `[NEEDS CLARIFICATION]` markers
   - Address each uncertainty with user input
   - Update specification with resolved information
   - Remove clarification markers
   - Re-run validation

## Examples

### Creating a new specification
```
User: /spec create user authentication system with OAuth2 and JWT tokens
```
I will create a comprehensive specification using AI-optimized templates with:
- Jinja2-style variables for AI processing
- Constitutional compliance sections
- Testable acceptance criteria
- Automated validation

### Updating existing specification
```
User: /spec update add password complexity requirements
```
I will read the current spec, update password requirements, and validate changes.

### Validating specification
```
User: /spec validate
```
I will run enhanced validation with detailed reporting:
```
SPEC_FILE=specs/001-user-authentication/spec.md
CLARIFICATIONS_NEEDED=3
MISSING_SECTIONS=0
STATUS=validation_complete
```

### Addressing clarifications
```
User: /spec clarify
```
I will systematically address all [NEEDS CLARIFICATION] markers.

## Enhanced Template Structure

The AI-optimized specification template includes:
- **Metadata**: Template variables for AI processing
- **Constitutional Gates**: Pre-implementation validation
- **Functional Requirements**: Structured Must/Should/Could/Won't
- **User Stories**: Given-When-Then acceptance criteria
- **Validation Checklist**: Automated completeness checks
- **Integration Points**: AI command workflow guidance

## Constitutional Compliance

**Article III: Test-First**
- [ ] Acceptance criteria written before implementation
- [ ] Test scenarios clearly defined
- [ ] Integration points identified

**Article VI: Research**
- [ ] Technology choices documented
- [ ] Security considerations addressed
- [ ] Performance requirements specified

## Enhanced Error Handling

- Template existence validation
- Feature directory auto-discovery
- Required sections validation
- Acceptance criteria format checking
- Clarification marker tracking

## Integration Features

- **Cross-platform script execution** with automatic detection
- **Enhanced script integration** with Bash, PowerShell, and Python support
- **Template variable processing** for AI optimization
- **Automated validation** with detailed reporting
- **Context-aware operation** using memory/context.md
- **Progress tracking** with todo list integration
- **Platform-agnostic operation** for Windows, Linux, and macOS