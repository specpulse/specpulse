---
description: Create or manage feature specifications using AI-optimized templates and SDD methodology.
---

$ARGUMENTS
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the specification management outcome
- Only edit files in specs/ directory - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse spec create/update/validate` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/
- **EDITABLE ONLY**: specs/

**CLI Failure Detection:**
- Exit code != 0
- Error messages: "command not found", "No such file", "Permission denied"
- Timeout > 30 seconds
- Missing dependencies

**Steps**
Track these steps as TODOs and complete them one by one.
1. **Parse arguments** from $ARGUMENTS to determine action:
   - If starts with `create`: Generate new specification
   - If starts with `update`: Modify existing specification
   - If starts with `validate`: Check specification completeness
   - If starts with `clarify`: Address [NEEDS CLARIFICATION] markers
   - If no action specified: Default to `create` with full arguments as description
2. **Detect current feature context**:
   - Read `.specpulse/memory/context.md` for current feature metadata
   - Use git branch name if available (e.g., `001-user-authentication`)
   - Fall back to most recently created feature directory
   - If no context found, ask user to specify feature or run `/sp-pulse` first
3. **For spec creation**:
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
4. **For spec update**:
   - **Show existing spec files**: List all spec-XXX.md files in current feature directory
   - **Ask user to select**: Which spec file to update
   - Read selected specification file
   - Parse update requests and identify sections to modify
   - Update content while preserving AI-friendly template structure
   - Remove resolved `[NEEDS CLARIFICATION]` markers
   - Run validation to ensure completeness
5. **For spec validation**:
   - **Read Spec File**: `.specpulse/specs/XXX-feature/spec-YYY.md`
   - **Manual Validation Checks**:
     * Count `[NEEDS CLARIFICATION]` markers
     * Verify all template sections are filled
     * Check acceptance criteria follow Given-When-Then format
     * Verify SDD compliance indicators present
   - **Report Results**:
     * Show validation status (complete/incomplete)
     * List missing sections
     * Highlight clarifications needed
     * Suggest next steps

**Usage**
Arguments should be provided as: `[action] [description|feature-name]`

Actions: `create`, `update`, `validate`, `clarify` (defaults to `create`)

**Examples**

**Creating a new specification:**
Input: `create user authentication system with OAuth2 and JWT tokens`
Output: Creates comprehensive specification using AI-optimized templates.

**Validating specification:**
Input: `validate`
Output: Enhanced validation with detailed reporting.

**Reference**
- Use `specpulse spec --help` if you need additional CLI options
- Check `.specpulse/memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- After specification creation, continue with `/sp-plan` for implementation planning
<!-- SPECPULSE:END -->