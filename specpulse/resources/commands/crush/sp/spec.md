---
name: SpecPulse: Create Specification
description: Create or expand specifications using SpecPulse SDD methodology
category: SpecPulse
tags: [specpulse, specification, sdd, documentation]
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the specification creation/expansion outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse spec create <spec-title>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/, .opencode/, .crush/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments** to extract specification details
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

**Reference**
- Use `specpulse spec create --help` for additional CLI options
- Check existing specifications in specs/ directory for patterns
- Use `validate` to validate completed specifications
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->