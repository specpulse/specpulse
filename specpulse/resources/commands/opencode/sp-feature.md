---
agent: build
description: Initialize new features with comprehensive setup using SpecPulse SDD methodology.
---

The user has requested the following change proposal. Use the openspec instructions to create their change proposal.
<UserRequest>
  sp-feature $ARGUMENTS
</UserRequest>

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the feature initialization outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse feature init <feature-name>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/, .opencode/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
1. **Parse arguments** to extract feature name and options from $ARGUMENTS
2. **Try CLI first**:
   - Run `specpulse feature init <feature-name>`
   - If this succeeds, STOP HERE. CLI handles everything.
3. **If CLI doesn't exist, use File Operations**:
   - **Step 1: Determine Feature ID**
     - Read specs/ directory (list subdirectories)
     - Find highest number (e.g., 001, 002) and increment
     - Or use 001 if no features exist
   - **Step 2: Create Feature Structure**
     ```bash
     mkdir -p specs/001-feature-name
     mkdir -p plans/001-feature-name
     mkdir -p tasks/001-feature-name
     ```
   - **Step 3: Update Context and Git**
     - Update memory/context.md with new feature
     - Create git branch: `git checkout -b 001-feature-name`
4. **Comprehensive feature setup**:
   - Generate initial feature documentation
   - Create feature specification template
   - Set up initial planning structure
   - Configure task tracking framework

**Usage**
Arguments should be provided as: `<feature-name> [options]`

**Examples**

**Basic Feature:**
Input: `user-authentication`
Output: Create complete feature structure with ID 001.

**Feature with Options:**
Input: `payment-system template:ecommerce`
Output: Create feature with e-commerce-specific templates.

**Next steps:**
- Guide: "Use `sp-spec` to create detailed specifications"
- Status: `STATUS=feature_ready, FEATURE_ID=001, BRANCH=001-user-authentication`

**Reference**
- This is an alias for `sp-pulse` with enhanced feature management
- Use `specpulse feature init --help` for additional CLI options
- Continue with `sp-spec` for specification creation
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->