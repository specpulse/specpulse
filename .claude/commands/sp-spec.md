---
name: sp-spec
description: Create or manage feature specifications using AI-optimized templates
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-spec Command

Create, update, or validate feature specifications using SpecPulse methodology with AI-optimized templates.

## CRITICAL: LLM Workflow Rules

**PRIMARY WORKFLOW: Use CLI when available**
- Prefer `specpulse spec create/update/validate` when those commands exist
- Use Bash tool ONLY for CLI commands, not for file editing
- Only use Read/Write/Edit tools for specs/ files when CLI doesn't cover the operation

**PROTECTED DIRECTORIES (NEVER EDIT):**
- `templates/` - Template files
- `.specpulse/` - Internal config
- `specpulse/` - Package code
- `.claude/` and `.gemini/` - AI configuration

**WORKFLOW:**
1. Try `specpulse spec create "description"` first
2. If CLI doesn't exist or doesn't cover your need, use File Operations
3. Templates are READ from templates/, then specs are CREATED/EDITED in specs/

## Usage
```
/sp-spec [action] [description|feature-name]
```

Actions: `create`, `update`, `validate`, `clarify` (defaults to `create`)

## Implementation

When called with `/sp-spec $ARGUMENTS`, I will:

1. **Detect current feature context**:
   - Read `memory/context.md` for current feature metadata
   - Use git branch name if available (e.g., `001-user-authentication`)
   - Fall back to most recently created feature directory
   - If no context found, ask user to specify feature or run `/sp-pulse` first

2. **Parse arguments** to determine action:
   - If starts with `create`: Generate new specification
   - If starts with `update`: Modify existing specification
   - If starts with `validate`: Check specification completeness
   - If starts with `clarify`: Address [NEEDS CLARIFICATION] markers
   - If no action specified: Default to `create` with full arguments as description

3. **For `/sp-spec create [description]` or `/sp-spec [description]`:**
   - **CRITICAL NUMBERING LOGIC**:
     - Check if `specs/XXX-feature/spec-001.md` exists
     - If spec-001.md does NOT exist: Create spec-001.md with full content from template
     - If spec-001.md EXISTS: Create spec-002.md (or next number) with new content
     - NEVER leave spec-001.md as placeholder if it's the first spec

   - **Step 1: Read Template**
     ```
     Read: templates/spec.md
     ```

   - **Step 2: Create Spec File Using Write Tool**
     ```
     Write: specs/XXX-feature/spec-YYY.md

     Content should include:
     - Metadata section with feature ID, date, version
     - User's description
     - Full template content for LLM expansion
     - [NEEDS CLARIFICATION] markers for uncertainties
     ```

   - **Step 3: Read Created File**
     ```
     Read: specs/XXX-feature/spec-YYY.md
     ```

   - **Step 4: EXPAND Specification**
     - Parse the description to identify:
       * Functional requirements (Must/Should/Could/Won't have)
       * User stories with testable acceptance criteria
       * Technical specifications and constraints
       * Success metrics and out-of-scope items
     - Fill in ALL template sections with complete details
     - Mark any uncertainties with `[NEEDS CLARIFICATION: specific question]`

   - **Step 5: Write Expanded Content Back**
     ```
     Edit: specs/XXX-feature/spec-YYY.md
     (Replace template placeholders with full specification)
     ```

   - **Step 6: Validate (Optional)**
     ```
     Bash: specpulse validate spec
     ```
     Note: Validation is optional - only if user requests it

4. **For `/sp-spec update`:**
   - **Show existing spec files**: List all spec-XXX.md files in current feature directory
   - **Ask user to select**: Which spec file to update
   - Read selected specification file
   - Parse update requests and identify sections to modify
   - Update content while preserving AI-friendly template structure
   - Remove resolved `[NEEDS CLARIFICATION]` markers
   - Run validation to ensure completeness

5. **For `/sp-spec validate`:**
   - **Step 1: Read Spec File**
     ```
     Read: specs/XXX-feature/spec-YYY.md
     ```

   - **Step 2: Manual Validation Checks**
     - Count `[NEEDS CLARIFICATION]` markers
     - Verify all template sections are filled
     - Check acceptance criteria follow Given-When-Then format
     - Verify SDD compliance indicators present

   - **Step 3: Run SpecPulse Validation (Optional)**
     ```
     Bash: specpulse validate spec
     ```
     Note: This is optional, manual checks are primary

   - **Step 4: Report Results**
     - Show validation status (complete/incomplete)
     - List missing sections
     - Highlight clarifications needed
     - Suggest next steps

6. **For `/sp-spec clarify`:**
   - **Show existing spec files**: List all spec-XXX.md files in current feature directory
   - **Ask user to select**: Which spec file to clarify
   - Find all `[NEEDS CLARIFICATION]` markers
   - Address each uncertainty with user input
   - Update specification with resolved information
   - Remove clarification markers
   - Re-run validation

## Examples

### Creating a new specification
```
User: /sp-spec create user authentication system with OAuth2 and JWT tokens
```
I will create a comprehensive specification using AI-optimized templates with:
- Jinja2-style variables for AI processing
- SDD compliance sections
- Testable acceptance criteria
- Automated validation

### Updating existing specification
```
User: /sp-spec update add password complexity requirements
```
I will read the current spec, update password requirements, and validate changes.

### Validating specification
```
User: /sp-spec validate
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
User: /sp-spec clarify
```
I will systematically address all [NEEDS CLARIFICATION] markers.

## Enhanced Template Structure

The AI-optimized specification template includes:
- **Metadata**: Template variables for AI processing
- **SDD Gates**: Pre-implementation validation
- **Functional Requirements**: Structured Must/Should/Could/Won't
- **User Stories**: Given-When-Then acceptance criteria
- **Validation Checklist**: Automated completeness checks
- **Integration Points**: AI command workflow guidance

## SDD Compliance

**Principle 1: Specification First**
- [ ] Requirements clearly documented
- [ ] Acceptance criteria defined
- [ ] User stories included

**Principle 6: Quality Assurance**
- [ ] Test scenarios defined
- [ ] Acceptance criteria testable
- [ ] Quality metrics specified

**Principle 7: Architecture Documentation**
- [ ] Technology choices documented
- [ ] Integration points identified
- [ ] Security considerations addressed

## Enhanced Error Handling

- Template existence validation
- Feature directory auto-discovery
- Required sections validation
- Acceptance criteria format checking
- Clarification marker tracking

## Integration Features

- **Script execution** with Bash support
- **Template variable processing** for AI optimization
- **Automated validation** with detailed reporting
- **Context-aware operation** using memory/context.md
- **Progress tracking** with todo list integration
- **Cross-platform operation** with Bash