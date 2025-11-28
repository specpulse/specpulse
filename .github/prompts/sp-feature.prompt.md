---
description: Initialize a new feature with SpecPulse framework (alias for sp-pulse) using SDD methodology.
---

$ARGUMENTS
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the feature initialization outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse feature init <feature-name>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Note: This command is an alias for `/sp-pulse` but provides a more intuitive name for feature initialization**

**Steps**
Track these steps as TODOs and complete them one by one.
1. **Parse arguments** to extract feature name + optional ID from $ARGUMENTS
2. **Try CLI first**:
   ```bash
   specpulse feature init <feature-name>
   ```
   If this succeeds, STOP HERE. CLI handles everything.
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
Arguments should be provided as: `<feature-name> [feature-id]`

**Examples**

**Web application feature:**
Input: `user-dashboard`
Output: Feature initialization with directory structure and specification suggestions.

**API service feature:**
Input: `payment-api`
Output: API service initialization with enterprise-grade suggestions.

**With custom feature ID:**
Input: `authentication 005`
Output: Feature initialization with custom ID.

**Integration Workflow**

After feature initialization, continue with:
```bash
# Create specification
/sp-spec standard

# Generate implementation plan
/sp-plan

# Break down into tasks
/sp-task

# Execute tasks
/sp-execute
```

**Project Type Detection**

**Examples of detected types:**
- **Web App**: `user-dashboard`, `admin-panel`, `checkout-flow`
- **API Service**: `payment-api`, `notification-service`, `auth-endpoint`
- **Mobile Component**: `push-notifications`, `offline-sync`, `user-profile`
- **Database System**: `user-migration`, `data-analytics`, `reporting-engine`
- **Integration**: `oauth-integration`, `stripe-payment`, `email-service`

**Complexity Assessment**

**Simple**: Single responsibility, few dependencies
- Estimated time: 2-4 hours (Core), 8-12 hours (Standard)

**Moderate**: Multiple components, some integrations
- Estimated time: 4-6 hours (Core), 12-16 hours (Standard)

**Complex**: Multiple services, advanced requirements
- Estimated time: 6-8 hours (Core), 16-24 hours (Standard)

**Reference**
- Use `specpulse feature init --help` if you need additional CLI options
- Check `memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- This command is an alias for `/sp-pulse` with identical functionality
- After feature creation, continue with `/sp-spec` for specification development
<!-- SPECPULSE:END -->