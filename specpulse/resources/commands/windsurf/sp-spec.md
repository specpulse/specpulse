---
description: Create or manage feature specifications using AI-optimized templates and SDD methodology
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the specification management outcome
- Only edit files in specs/ directory - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse spec create/update/validate` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/
- **EDITABLE ONLY**: specs/

**CLI Failure Detection:**
- Exit code != 0
- Error messages: "command not found", "No such file", "Permission denied"
- Timeout > 30 seconds
- Missing dependencies

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Detect current feature context**:
   - Read `.specpulse/memory/context.md` for current feature metadata
   - Use git branch name if available (e.g., `001-user-authentication`)
   - Fall back to most recently created feature directory
   - If no context found, ask user to specify feature or run `/sp-pulse` first

2. **Parse arguments** to determine action:
   - If starts with `create`: Generate new specification
   - If starts with `update`: Modify existing specification
   - If starts with `validate`: Check specification completeness
   - If starts with `clarify`: Address [NEEDS CLARIFICATION] markers
   - If no action specified: Default to `create` with full arguments as description

3. **For /sp-spec create [description] or /sp-spec [description]:**
   - **CRITICAL NUMBERING LOGIC**:
     - Check if `.specpulse/specs/XXX-feature/spec-001.md` exists
     - If spec-001.md does NOT exist: Create spec-001.md with full content from template
     - If spec-001.md EXISTS: Create spec-002.md (or next number) with new content
     - NEVER leave spec-001.md as placeholder if it's the first spec

   - **Step 1: Try CLI First**
     ```bash
     specpulse spec create "<description>"
     ```
     If CLI succeeds, STOP HERE.

   - **Step 2: Fallback to File Operations (if CLI fails)**
     - **Read Template**: `.specpulse/templates/spec.md`
     - **Create Spec File**: `.specpulse/specs/XXX-feature/spec-YYY.md`
     - **Content should include**:
       * Metadata section with feature ID, date, version
       * User's description
       * Full template content for LLM expansion
       * [NEEDS CLARIFICATION] markers for uncertainties

   - **Step 3: EXPAND Specification**
     - Parse the description to identify:
       * Functional requirements (Must/Should/Could/Won't have)
       * User stories with testable acceptance criteria
       * Technical specifications and constraints
       * Success metrics and out-of-scope items
     - Fill in ALL template sections with complete details
     - Mark any uncertainties with `[NEEDS CLARIFICATION: specific question]`

   - **Step 4: Write Expanded Content Back**
     - Edit: `.specpulse/specs/XXX-feature/spec-YYY.md`
     - Replace template placeholders with full specification

   - **Step 5: Validate (Optional)**
     ```bash
     specpulse spec validate [spec-id]
     ```

4. **For /sp-spec update:**
   - **Show existing spec files**: List all spec-XXX.md files in current feature directory
   - **Ask user to select**: Which spec file to update
   - Read selected specification file
   - Parse update requests and identify sections to modify
   - Update content while preserving AI-friendly template structure
   - Remove resolved `[NEEDS CLARIFICATION]` markers
   - Run validation to ensure completeness

5. **For /sp-spec validate:**
   - **Read Spec File**: `.specpulse/specs/XXX-feature/spec-YYY.md`
   - **Manual Validation Checks**:
     * Count `[NEEDS CLARIFICATION]` markers
     * Verify all template sections are filled
     * Check acceptance criteria follow Given-When-Then format
     * Verify SDD compliance indicators present
   - **Run SpecPulse Validation (Optional)**:
     ```bash
     specpulse spec validate [spec-id]
     ```
   - **Report Results**:
     * Show validation status (complete/incomplete)
     * List missing sections
     * Highlight clarifications needed
     * Suggest next steps

6. **For /sp-spec clarify:**
   - **Show existing spec files**: List all spec-XXX.md files in current feature directory
   - **Ask user to select**: Which spec file to clarify
   - Find all `[NEEDS CLARIFICATION]` markers
   - Address each uncertainty with user input
   - Update specification with resolved information
   - Remove clarification markers
   - Re-run validation

**Usage**
```
/sp-spec [action] [description|feature-name]
```

Actions: `create`, `update`, `validate`, `clarify` (defaults to `create`)

**Examples**

**Creating a new specification:**
```
/sp-spec create user authentication system with OAuth2 and JWT tokens
```
Output: Creates comprehensive specification using AI-optimized templates with:
- Jinja2-style variables for AI processing
- SDD compliance sections
- Testable acceptance criteria
- Automated validation

**Updating existing specification:**
```
/sp-spec update add password complexity requirements
```
Output: Reads current spec, updates password requirements, and validates changes.

**Validating specification:**
```
/sp-spec validate
```
Output: Enhanced validation with detailed reporting:
```
SPEC_FILE=.specpulse/specs/001-user-authentication/spec.md
CLARIFICATIONS_NEEDED=3
MISSING_SECTIONS=0
STATUS=validation_complete
```

**Addressing clarifications:**
```
/sp-spec clarify
```
Output: Systematically addresses all [NEEDS CLARIFICATION] markers.

**SDD Compliance Tracking**

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

**Task Format**
```markdown
- [ ] Detect current feature context
- [ ] Parse command arguments
- [ ] Try CLI command first
- [ ] Create/update spec file if CLI fails
- [ ] Expand specification with AI optimization
- [ ] Validate completeness
- [ ] Report results
```

**Error Handling**

- Template existence validation
- Feature directory auto-discovery
- Required sections validation
- Acceptance criteria format checking
- Clarification marker tracking
- CLI failure detection and fallback

**Reference**
- Use `specpulse spec --help` if you need additional CLI options
- Check `.specpulse/memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- After specification creation, continue with `/sp-plan` for implementation planning
- Use `CLI_FALLBACK_GUIDE.md` for manual procedures when CLI fails
<!-- SPECPULSE:END -->