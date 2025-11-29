---
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the status tracking outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use file operations (CLI-independent mode)
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments to determine scope**:
   - If feature name provided: Show detailed status for that feature
   - If no argument: Show overview of all features
   - Parse options like --verbose, --validate, --trends

2. **Detect current feature context**:
   - Check .specpulse/memory/context.md for active feature
   - Look for most recently modified spec/plan/task directory
   - Validate feature directory exists and is properly structured
   - Extract feature ID and name from directory structure

3. **For overall project status (no arguments)**:
   - **Step 1: Feature Discovery**
     - Scan .specpulse/specs/, .specpulse/plans/, .specpulse/tasks/ directories
     - Identify all feature directories using naming convention (XXX-feature-name)
     - Build comprehensive feature inventory
   - **Step 2: Feature Status Assessment**
     - For each feature, determine: Active, Completed, In Progress, Paused, Blocked
     - Calculate project-level metrics (total features, active features, overall progress)
   - **Step 3: Display Feature Overview**
     - Show concise summary for each feature with progress percentage, status indicator
     - Include file counts (specs, plans, tasks) and last activity timestamp
     - Highlight current active feature

4. **For specific feature status**:
   - **Step 1: Feature Detection and Validation**
     - Locate feature directory structure
     - Validate proper .specpulse organization
     - Check for required subdirectories (specs/, plans/, tasks/)
   - **Step 2: File Inventory and Analysis**
     - Count and analyze files: specification files, plan files, task files
     - Determine completeness status and quality metrics
   - **Step 3: Progress Calculation**
     - Calculate detailed progress metrics: overall percentage, task distribution
     - Analyze phase breakdown and velocity metrics
   - **Step 4: Task Status Analysis**
     - Parse task files to determine individual task status
     - Analyze dependency relationships and chain status
     - Identify parallel task availability and blockers

5. **Advanced analysis features**:
   - **Universal ID System Integration**: Track ID usage, detect conflicts, validate consistency
   - **SDD Gates Compliance**: Verify specifications meet standards, check traceability
   - **Trend Analysis**: Progress velocity over time, completion rate trends
   - **Validation and Health Check**: File structure integrity, dependency cycles

6. **Context management and updates**:
   - Update .specpulse/memory/context.md with latest status
   - Track status check history for trend analysis
   - Link related features and dependencies
   - Maintain searchable status history

7. **Validate structure and report comprehensive status**

**Usage**
```
/sp-status [feature-name]
```

**Examples**

**Project Overview:**
```
/sp-status
```

Output: Show overview of all features with progress percentages, status indicators, and project-level metrics.

**Feature Status:**
```
/sp-status 001-user-authentication
```

Output: Detailed feature analysis with task breakdown, phase progress, blockers, and velocity metrics.

**Advanced Analysis:**
```
/sp-status --validate --trends
```

Output: Comprehensive analysis with SDD compliance, trend analysis, and health check validation.

**Status Display Features:**
- **Project Summary**: Total features, overall progress, active features
- **Feature Breakdown**: Individual feature status with progress indicators
- **Task Analysis**: Completed/in-progress/blocked/pending task distribution
- **Phase Progress**: Implementation phase completion percentages
- **Velocity Metrics**: Tasks completed per time period, completion estimates
- **Blocker Identification**: Current blockers and resolution paths
- **Dependencies**: Feature relationships and blocking chains

**Advanced Features:**
- **Universal ID System**: Track ID usage, detect conflicts, validate consistency
- **SDD Gates Compliance**: Specification standards, task traceability validation
- **Trend Analysis**: Progress velocity trends, completion rate patterns
- **Health Check**: File structure integrity, dependency validation
- **Context Management**: Automatic context updates and history tracking

**Error Handling**
- No memory file: Create initial context structure
- Invalid feature directory: Suggest valid feature names
- Multiple active features: Prompt to select primary feature
- Corrupted task files: Guide through file recovery process

**Status Indicators**
- `[OK]` - Completed feature
- `[PROG]` - Active development
- `[WAIT]` - In progress (waiting for dependencies)
- `[PAUSED]` - No recent activity
- `[BLOCKED]` - Blocked by issues

**Reference**
- Check memory/context.md for current feature context
- Run validation to ensure file structure integrity
- Use --verbose option for detailed analysis
- Track trends with repeated status checks

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Uses LLM-safe file operations for status calculation
- Comprehensive progress analytics and trend analysis
- Real-time dependency tracking and blocker identification
<!-- SPECPULSE:END -->