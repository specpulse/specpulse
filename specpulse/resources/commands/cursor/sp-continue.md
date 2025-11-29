---
name: /sp-continue
id: sp-continue
category: SpecPulse
description: Switch to existing feature context without SpecPulse CLI
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the context switching outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use file operations (CLI-independent mode)
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments to determine action**:
   - If feature ID/name provided: Switch to that feature
   - If no argument: List all available features for selection
   - Validate input format (XXX-feature-name or just feature-name)

2. **For listing available features**:
   - **Step 1: Feature Discovery**
     - Scan .specpulse/specs/, .specpulse/plans/, .specpulse/tasks/ directories
     - Identify all feature directories using naming convention (XXX-feature-name)
     - Build comprehensive feature inventory
   - **Step 2: Feature Analysis**
     - Calculate progress percentage (if tasks exist)
     - Count files (specs, plans, tasks) for each feature
     - Determine last activity timestamp from file modifications
     - Classify status (Active, Completed, In Progress, Paused, Blocked)
   - **Step 3: Display Feature Selection Interface**
     - Show each feature with ID, name, progress, status, file counts, last activity
     - Provide selection instructions (number, ID, name, cancel)

3. **For feature context switching**:
   - **Step 1: Feature Detection and Validation**
     - Parse feature identifier (extract ID from XXX-feature-name)
     - Validate feature directory exists and is properly structured
     - Check for required .specpulse organization
     - Verify feature has content (specs, plans, or tasks)
   - **Step 2: Context Analysis**
     - Analyze feature structure and content
     - Identify current progress status
     - Check for active work or incomplete tasks
     - Detect any blockers or issues
   - **Step 3: Update Memory Context**
     - Update .specpulse/memory/context.md with new active feature
     - Set current working directory context
     - Record feature switch history
     - Update feature status and metadata
   - **Step 4: Git Integration**
     - Check if feature branch exists
     - Switch to feature branch if available
     - Create feature branch if missing
     - Update git working directory context

4. **Context switch validation**:
   - Confirm feature directory is accessible
   - Validate memory context updated correctly
   - Check file permissions and structure
   - Verify git branch (if applicable)

5. **Display feature summary**:
   - Show feature name and ID
   - Display current progress status
   - List available files (specs, plans, tasks)
   - Show last activity information
   - Provide recommended next steps
   - Highlight any active work or blockers

6. **Validate structure and report comprehensive status**

**Usage**
```
/sp-continue [feature-id|feature-name]
```

**Examples**

**List Available Features:**
```
/sp-continue
```

Output: Show all available features with progress, status, file counts, and selection interface.

**Switch to Specific Feature:**
```
/sp-continue 002-payment-processing
```

Output: Switch context to payment processing feature, update memory context, and show feature summary.

**Quick Feature Switch:**
```
/sp-continue auth
```

Output: Find and switch to user-authentication feature using fuzzy matching.

**Feature Selection Interface:**
- Display features with progress indicators and status
- Show file counts and last activity timestamps
- Provide multiple selection methods (number, ID, name)
- Include cancel option and help instructions

**Context Memory Management:**
- Update .specpulse/memory/context.md with new active feature
- Maintain feature switch history for tracking
- Set working directory context for commands
- Record git branch information if available

**Advanced Features:**
- **Feature Search**: Partial name matching and ID pattern matching
- **Status Filtering**: Show only active, completed, or paused features
- **Bulk Operations**: List features by progress, file types, activity
- **Context Presets**: Save frequently used feature combinations

**Error Handling**
- Feature not found: Suggest valid feature IDs from available list
- Directory access denied: Provide permission fix instructions
- Memory file corrupted: Rebuild from available features
- Git operation failures: Offer manual git command alternatives

**Context Structure:**
```yaml
active_feature:
  id: "002"
  name: "payment-processing"
  directory: "002-payment-processing"
  status: "in_progress"
  progress: 23
git_context:
  branch: "feature/002-payment-processing"
  working_directory: ".specpulse/specs/002-payment-processing"
```

**Reference**
- Check memory/context.md for current feature context
- Use /sp-status to see detailed feature information
- Run /sp-execute to continue working on tasks
- Use /sp-pulse to create new features if needed

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Uses LLM-safe file operations for context management
- Comprehensive feature discovery and analysis
- Git integration with automatic branch management
- Feature switch history and context preservation
<!-- SPECPULSE:END -->