---
name: /sp-pulse
id: sp-pulse
category: SpecPulse
description: Initialize a new feature with SpecPulse framework using SDD methodology.
---
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the feature initialization outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse feature init <feature-name>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.
1. **Validate arguments** and extract feature name + optional ID
2. **Try CLI first**:
   - Run `!{bash specpulse feature init <feature-name>}`
   - If this succeeds, STOP HERE. CLI handles everything.
3. **If CLI doesn't exist, use File Operations**:
   - **Step 1: Determine Feature ID**
     - Read specs/ directory (list subdirectories)
     - Find highest number (e.g., 001, 002) and increment
     - Or use 001 if no features exist
   - **Step 2: Create Feature Directories Using Bash**
     ```bash
     mkdir -p specs/001-feature-name
     mkdir -p plans/001-feature-name
     mkdir -p tasks/001-feature-name
     ```
   - **Step 3: Update Context File**
     - Read: memory/context.md
     - Edit: memory/context.md (Add new feature entry with ID, name, timestamp)
   - **Step 4: Create Git Branch (Optional)**
     ```bash
     git checkout -b 001-feature-name
     ```
4. **Intelligent specification suggestions**:
   - Analyze feature name to infer project type and complexity
   - Generate 3 context-aware specification suggestions:
     1. **Core specification** (essential functionality only)
     2. **Standard specification** (comprehensive with detailed requirements)
     3. **Complete specification** (full-featured with all aspects)
   - Show estimated development time for each option
   - Guide user to `/sp-spec [chosen-option]` after selection
5. **Validate structure** and report comprehensive status

**Usage**
```
/sp-pulse <feature-name> [feature-id]
```

**Examples**

**Basic Usage:**
```
/sp-pulse user-authentication-oauth2
```
Output: Create feature structure using CLI calls, set context, and provide specification suggestions.

**Project type detection**: Web app, API, mobile app, database system, etc.
**Complexity assessment**: Simple, moderate, or complex based on feature name

**Next steps:**
- Ask: "Which specification approach would you like? (core/standard/complete or custom description)"
- Guide: "After choosing, use `/sp-spec [your-option]` to create the specification"
- Status: `STATUS=ready_for_spec, BRANCH_NAME=001-user-authentication-oauth2, PROJECT_TYPE=detected`

**Reference**
- Use `specpulse feature init --help` if you need additional CLI options
- Check `memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- After feature creation, continue with `/sp-spec` for specification creation
<!-- SPECPULSE:END -->