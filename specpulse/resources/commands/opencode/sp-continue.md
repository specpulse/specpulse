---
name: sp-continue
description: Switch to existing feature context without SpecPulse CLI
version: "1.0"
agent: specpulse-assistant
workflow_type: context_switching
---

# SpecPulse Context Switching Workflow

This workflow implements comprehensive CLI-independent feature context switching with memory management and git integration.

## Agent Capabilities Required

- File operations: Read, Write, Edit, Bash, TodoWrite
- Directory traversal protection
- Atomic file operation handling
- Feature discovery and analysis
- Context management and switching
- Git integration and branch management
- Error recovery and validation

## Workflow Steps

### Step 1: Argument Parsing and Action Determination

**Parse input arguments:**
```yaml
inputs:
  feature_identifier: string
  action: enum [switch, list]
```

**Action determination:**
```yaml
action_logic:
  feature_provided:
    condition: feature ID/name provided
    action: Switch to specified feature
    validation: Validate input format (XXX-feature-name or feature-name)

  no_argument:
    condition: No argument provided
    action: List all available features for selection
    behavior: Display feature selection interface
```

### Step 2: Feature Discovery and Listing (No Argument Mode)

**Comprehensive feature analysis:**
```yaml
feature_discovery:
  directory_scanning:
    scan_paths:
      - .specpulse/specs/
      - .specpulse/plans/
      - .specpulse/tasks/

    identification_process:
      - Identify feature directories using naming convention (XXX-feature-name)
      - Extract feature ID and name from directory names
      - Build comprehensive feature inventory with metadata

  feature_analysis:
    progress_calculation:
      - Scan task files for completion status
      - Calculate progress percentage based on task completion
      - Determine active work and incomplete tasks

    file_inventory:
      - Count specification files in each feature
      - Count plan files and assess completeness
      - Count task files and total tasks
      - Determine last activity timestamp from file modifications

    status_classification:
      active:
        criteria: Currently has open tasks or recent activity
        indicator: "🟢 Active Progress"

      completed:
        criteria: All tasks marked as done
        indicator: "✅ Completed"

      in_progress:
        criteria: Has some completed tasks with work remaining
        indicator: "🟡 In Progress"

      paused:
        criteria: No recent activity but not all tasks complete
        indicator: "⏸️ Paused"

      blocked:
        criteria: Has blocked tasks preventing progress
        indicator: "❌ Blocked"

  selection_interface:
    display_format:
      - Feature number for selection (1-N)
      - Feature ID and name
      - Progress percentage and status indicator
      - File counts (specs, plans, tasks)
      - Last activity timestamp
      - Selection instructions (number, ID, name, cancel)
```

### Step 3: Feature Context Switching (Feature Provided Mode)

**Comprehensive context switching:**
```yaml
context_switching:
  feature_detection_validation:
    identifier_parsing:
      - Parse feature identifier (extract ID from XXX-feature-name)
      - Support partial name matching (e.g., "auth" matches "user-authentication")
      - Handle ID pattern matching (e.g., "00" matches features starting with 00)

    validation_process:
      - Validate feature directory exists and is properly structured
      - Check for required .specpulse organization
      - Verify feature has content (specs, plans, or tasks)
      - Confirm directory permissions and accessibility

  context_analysis:
    structure_analysis:
      - Analyze feature directory structure
      - Identify available file types and organization
      - Check for service decomposition if present

    content_assessment:
      - Identify current progress status
      - Check for active work or incomplete tasks
      - Detect any blockers or issues
      - Assess feature readiness for continued work

    status_evaluation:
      - Calculate current completion percentage
      - Determine feature phase and milestone status
      - Identify next logical steps and priorities

  memory_context_update:
    context_file_structure:
      file_path: .specpulse/memory/context.md
      format: YAML frontmatter with markdown content

    update_operations:
      active_feature_update:
        id: "Feature ID (e.g., 002)"
        name: "Feature name (e.g., payment-processing)"
        directory: "Feature directory (e.g., 002-payment-processing)"
        status: "Current status (e.g., in_progress)"
        progress: "Progress percentage (e.g., 23)"
        created_at: "Feature creation timestamp"
        last_activity: "Most recent activity timestamp"

      working_directory_context:
        path: ".specpulse/specs/[feature-directory]/"
        absolute_path: "Full path to feature directory"
        accessibility: "Directory access validation"

      feature_history_tracking:
        previous_feature:
          id: "Previous feature ID"
          name: "Previous feature name"
          switched_from: "Timestamp of context switch"
          duration: "Time spent on previous feature"

        current_feature:
          switched_to: "Timestamp of current context switch"
          session_start: "Current working session start"

  git_integration:
    branch_management:
      detection:
        - Check if feature branch exists (feature/[feature-id]-[feature-name])
        - Validate branch is accessible and up-to-date

      switching_operations:
        - Switch to existing feature branch if available
        - Create feature branch if missing
        - Update working directory to match feature context

      context_synchronization:
        - Update git working directory context
        - Record current commit hash and branch information
        - Synchronize git context with feature context

  validation_verification:
    accessibility_checks:
      - Confirm feature directory is accessible
      - Validate file permissions and structure integrity
      - Verify memory context updated correctly

    consistency_validation:
      - Check git branch matches feature context
      - Validate working directory alignment
      - Ensure context file integrity and format
```

### Step 4: Feature Summary Display

**Comprehensive feature overview:**
```yaml
feature_summary:
  header_information:
    - Feature name and ID
    - Current progress status
    - Feature creation and last update timestamps

  structural_overview:
    available_files:
      specifications:
        - Count and list specification files
        - Show completion status and quality indicators

      plans:
        - Count and list plan files
        - Show implementation strategy status

      tasks:
        - Count and list task files
        - Show total tasks and completion breakdown

    directory_structure:
      - Display organized file structure
      - Show service decomposition if present
      - Indicate working directory context

  progress_analysis:
    current_status:
      - Overall progress percentage
      - Task completion distribution
      - Active work indicators

    phase_assessment:
      - Current implementation phase
      - Phase completion status
      - Next phase readiness

  operational_guidance:
    recommended_next_steps:
      - Continue with specific pending tasks
      - Review specifications or plans as needed
      - Check task status for detailed information
      - Execute next available task

    available_commands:
      - /sp-status for detailed feature information
      - /sp-execute to continue working on tasks
      - /sp-pulse to create new features if needed
      - /sp-validate to check feature quality

  contextual_information:
    git_context:
      - Current branch and commit information
      - Remote tracking status
      - Working directory status

    memory_context:
      - Feature switch history
      - Working session duration
      - Previous feature context
```

### Step 5: Advanced Features and Search

**Enhanced discovery and matching:**
```yaml
advanced_features:
  search_capabilities:
    fuzzy_matching:
      - Partial name matching (e.g., "auth" matches "user-authentication")
      - Phonetic similarity matching
      - Typo tolerance and suggestion

    pattern_matching:
      - ID pattern matching (e.g., "00" matches all features starting with 00)
      - Wildcard support for flexible searching
      - Regular expression matching for complex patterns

  filtering_options:
    status_based_filtering:
      - Show only active features
      - Display completed features only
      - Filter paused or blocked features

    progress_based_filtering:
      - List features by progress percentage ranges
      - Show features needing immediate attention
      - Display nearly completed features

    temporal_filtering:
      - Sort features by last activity
      - Show recently created features
      - Filter by age or inactivity period

  bulk_operations:
    feature_organization:
      - List features by progress percentage
      - Show features with specific file types
      - Display features sorted by priority or status

    comparative_analysis:
      - Side-by-side feature comparison
      - Progress ranking and bottleneck identification
      - Resource allocation assessment
```

## Output Format

**Feature selection response:**
```yaml
feature_selection:
  available_features:
    - index: 1
      id: "001"
      name: "user-authentication"
      progress: "65%"
      status: "active_progress"
      indicator: "🟢"
      files:
        specs: 2
        plans: 1
        tasks: 25
      last_activity: "2 hours ago"
      description: "User registration and authentication system"

    - index: 2
      id: "002"
      name: "payment-processing"
      progress: "23%"
      status: "in_progress"
      indicator: "🟡"
      files:
        specs: 1
        plans: 1
        tasks: 18
      last_activity: "1 day ago"
      description: "Payment gateway integration system"

  selection_instructions:
    methods:
      - "Use number (1-2)"
      - "Use feature ID (001, 002, etc.)"
      - "Use feature name (auth, payment, etc.)"
      - "Type 'cancel' to abort"

  total_features: 2
  active_features: 2
  completed_features: 0
```

**Context switch response:**
```yaml
context_switch:
  status: "success"
  message: "Context switched successfully"

  active_feature:
    id: "002"
    name: "payment-processing"
    directory: "002-payment-processing"
    status: "in_progress"
    progress: 23
    created_at: "2025-01-10T09:00:00Z"
    last_activity: "2025-01-11T14:20:00Z"

  working_context:
    directory: ".specpulse/specs/002-payment-processing/"
    git_branch: "feature/002-payment-processing"
    accessibility: "confirmed"

  available_files:
    specifications:
      - "spec-001.md (Payment API)"

    plans:
      - "plan-001.md (Implementation Strategy)"

    tasks:
      - "payment-tasks.md (18 tasks)"

  next_steps:
    immediate:
      - "Continue with T005: Implement payment gateway integration"
      - "Review specifications: /sp-spec validate"

    follow_up:
      - "Check task status: /sp-status"
      - "Execute next task: /sp-execute"

  feature_summary:
    total_tasks: 18
    completed_tasks: 4
    pending_tasks: 14
    blockers: 0
    estimated_completion: "2025-01-25"
```

## Error Handling and Recovery

**Comprehensive error scenarios:**
```yaml
error_handling:
  feature_not_found:
    invalid_feature_id:
      action: Suggest valid feature IDs from available list
      recovery: Provide feature selection interface

    feature_directory_missing:
      action: Guide through feature discovery process
      recovery: Offer to create missing feature with /sp-pulse

    empty_feature:
      action: Recommend running /sp-pulse to create feature
      recovery: Provide feature creation guidance

  permission_issues:
    directory_access_denied:
      action: Provide permission fix instructions
      recovery: Offer specific chmod commands and guidance

    file_write_errors:
      action: Guide through permission corrections
      recovery: Suggest alternative approaches for context management

    git_operation_failures:
      action: Offer manual git command alternatives
      recovery: Provide non-git context switching options

  context_recovery:
    memory_file_corrupted:
      action: Rebuild from available features
      recovery: Reconstruct context from directory structure

    git_branch_issues:
      action: Work without git integration
      recovery: Provide local context management only

    feature_structure_invalid:
      action: Provide repair instructions
      recovery: Offer structure correction templates
```

## Safety Constraints

- **Path validation**: Only operate within `.specpulse/` directory
- **Protected directories**: Never modify `templates/`, `specpulse/`, AI configs
- **Atomic operations**: Prevent partial context updates
- **Rollback capability**: Restore previous context on failures
- **Input validation**: Comprehensive sanitization of feature identifiers

## Integration Features

- **Memory Management**: Complete context tracking and history
- **Git Integration**: Automatic branch management and synchronization
- **Feature Discovery**: Comprehensive feature analysis and classification
- **Search Capabilities**: Fuzzy matching and advanced filtering
- **Context Preservation**: Feature switch history and session tracking
- **Progress Tracking**: Real-time feature status and progress monitoring