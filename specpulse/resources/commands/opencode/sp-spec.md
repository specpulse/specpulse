---
agent: build
description: Create or expand specifications using SpecPulse SDD methodology.
---

The user has requested the following change proposal. Use the openspec instructions to create their change proposal.
<UserRequest>
  sp-spec $ARGUMENTS
</UserRequest>

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the specification creation/expansion outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse spec create <spec-title>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/, .opencode/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
1. **Parse arguments** to extract specification details from $ARGUMENTS
2. **Determine current context**:
   - Read: memory/context.md
   - Extract current.feature and current.feature_id if available
3. **Try CLI first**:
   - Run `specpulse spec create "<spec-title>"`
   - If this succeeds, continue with expansion
4. **If CLI doesn't exist, use File Operations**:
   - **Step 1: Create specification file**
     - Create: specs/current-feature_id/spec-001.md (or next available number)
     - Use appropriate template based on project type
5. **Intelligent specification expansion**:
   - Analyze spec title and context to infer requirements
   - Generate comprehensive specification sections:
     1. **Overview & Objectives** (purpose and goals)
     2. **Functional Requirements** (what the system should do)
     3. **Non-Functional Requirements** (performance, security, etc.)
     4. **Technical Requirements** (technologies and constraints)
     5. **Acceptance Criteria** (success conditions)
   - Include implementation considerations and edge cases

6. **Cross-references and validation**:
   - Link related specifications
   - Validate completeness against SDD principles
   - Check for consistency with existing specs

**Usage**
Arguments should be provided as: `"specification title" [expand|create|validate]`

**Examples**

**Basic Specification:**
Input: `"User authentication with OAuth2"`
Output: Create comprehensive authentication specification with all requirements.

**Specification Expansion:**
Input: `"API rate limiting" expand`
Output: Expand existing rate limiting spec with additional requirements and edge cases.

**Specification Validation:**
Input: `"Payment processing" validate`
Output: Validate existing specification against SDD principles and identify gaps.

**Next steps:**
- Guide: "Use `sp-plan` to create implementation plans for this specification"
- Status: `STATUS=spec_complete, SPEC_FILE=specs/001/user-auth-oauth2.md, READY_FOR_PLANNING=true`

**Reference**
- Use `specpulse spec create --help` for additional CLI options
- Check existing specifications in specs/ directory for patterns
- Use `sp-validate` to validate completed specifications
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->