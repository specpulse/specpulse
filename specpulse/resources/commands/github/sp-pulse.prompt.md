---
description: Initialize new features and manage project context without SpecPulse CLI
---

$ARGUMENTS
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the feature initialization outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use file operations (CLI-independent mode)
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments from $ARGUMENTS**:
   - If feature name provided → Initialize new feature with that name
   - If "status" → Show current feature context
   - If "list" → Show all available features
   - If no argument → Show current feature status

2. **For feature initialization**:
   - **Step 1: Determine Feature ID**
     - Read specs/ directory (list subdirectories)
     - Find highest number (e.g., 001, 002) and increment
     - Or use 001 if no features exist
   - **Step 2: Create Feature Structure Using Atomic Operations**
     ```bash
     mkdir -p specs/001-feature-name
     mkdir -p plans/001-feature-name
     mkdir -p tasks/001-feature-name
     mkdir -p memory/
     ```
   - **Step 3: Create Initial Specification**
     - Create spec-001.md with comprehensive template
     - Include executive summary, requirements, user stories
   - **Step 4: Update Context File**
     - Read: memory/context.md
     - Edit: memory/context.md (Add new feature entry with ID, name, timestamp)
   - **Step 5: Create Git Branch (Optional)**
     ```bash
     git checkout -b feature/001-feature-name
     ```

3. **For feature status display**:
   - Read current feature from memory/context.md
   - Display feature ID, name, and progress
   - Show file counts (specs, plans, tasks)
   - Calculate and display completion percentage
   - Show last activity timestamp

4. **For feature listing**:
   - Use Glob tool to find all feature directories
   - Extract feature IDs and names from directory structure
   - Read context information for each feature
   - Display progress status and file counts
   - Show last activity for each feature

5. **Validate structure and report comprehensive status**

**Usage**
Arguments should be provided as: `[feature-name] [action]`

**Examples**

**Basic Usage:**
```
/sp-pulse user-authentication-oauth2
```

Output: Create feature structure with atomic operations, set context, and provide next steps.

**Status Check:**
```
/sp-pulse status
```

Output: Display current feature information with progress metrics.

**Feature Listing:**
```
/sp-pulse list
```

Output: Show all available features with progress and activity status.

**Advanced Features:**
- **Atomic Operations**: Create structure with rollback on failure
- **Context Management**: File-based context tracking
- **Feature Templates**: Web Application, API Service, CLI Tool, Library/SDK
- **Integration Ready**: Git Integration, Testing Setup, CI/CD Ready
- **Documentation**: Auto-generated README and API docs

**Error Handling**
- Feature name sanitization (alphanumeric, hyphens only)
- Directory creation validation
- Template existence verification
- Git repository validation
- Context file management

**Reference**
- Check memory/context.md for current feature context
- Run validation on created structure
- After feature creation, continue with /sp-spec for specification creation

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Uses LLM-safe file operations
- Atomic operations prevent corruption
- Comprehensive error recovery
<!-- SPECPULSE:END -->