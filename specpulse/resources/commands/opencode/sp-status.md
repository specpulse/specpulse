---
name: sp-status
description: Track project progress without SpecPulse CLI
version: "1.0"
agent: specpulse-assistant
workflow_type: progress_tracking
---

# SpecPulse Progress Tracking Workflow

This workflow implements complete CLI-independent project status tracking with comprehensive analytics and trend analysis.

## Agent Capabilities Required

- File operations: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
- Directory traversal protection
- Atomic file operation handling
- Progress calculation algorithms
- Dependency analysis and validation
- Trend analysis and metrics calculation
- Error recovery and data validation

## Workflow Steps

### Step 1: Argument Parsing and Scope Determination

**Parse input arguments:**
```yaml
inputs:
  feature_name: string
  options:
    verbose: boolean
    validate: boolean
    trends: boolean
```

**Analysis modes:**
```yaml
scope_modes:
  project_overview:
    trigger: No feature name provided
    action: Show overview of all features with project-level metrics

  feature_detailed:
    trigger: Feature name provided
    action: Show detailed status for specific feature with comprehensive analysis

  advanced_analysis:
    trigger: Options like --validate, --trends, --verbose
    action: Enhanced analysis with SDD compliance, trends, and health checks
```

### Step 2: Current Feature Context Detection

**Feature context algorithm:**
1. Check `.specpulse/memory/context.md` for active feature
2. Look for most recently modified spec/plan/task directory
3. Validate feature directory exists and is properly structured
4. Extract feature ID and name from directory structure
5. Set working context for subsequent operations

### Step 3: Project Overview Mode (No Feature Specified)

**Comprehensive project analysis:**
```yaml
project_analysis:
  feature_discovery:
    scan_directories:
      - .specpulse/specs/
      - .specpulse/plans/
      - .specpulse/tasks/

    identification_process:
      - Identify all feature directories using naming convention (XXX-feature-name)
      - Build comprehensive feature inventory with metadata
      - Validate feature directory structure and integrity

  status_assessment:
    feature_classification:
      active:
        criteria: Currently has open tasks or recent activity
        indicator: "[PROG]"

      completed:
        criteria: All tasks marked as done
        indicator: "[OK]"

      in_progress:
        criteria: Has some completed tasks with work remaining
        indicator: "[PROG]"

      paused:
        criteria: No recent activity but not all tasks complete
        indicator: "[PAUSED]"

      blocked:
        criteria: Has blocked tasks preventing progress
        indicator: "[BLOCKED]"

  project_metrics:
    calculation:
      total_features: Count of all discovered features
      active_features: Count of features with active development
      completed_features: Count of fully completed features
      overall_progress: Weighted average of all feature progress

    statistical_analysis:
      average_velocity: Tasks completed per day across all features
      completion_rate: Features completed per time period
      blocker_frequency: Rate of blocking issues occurrence
      feature_development_patterns: Analysis of development workflows

  overview_display:
    feature_summary_format:
      - Feature name and ID
      - Progress percentage
      - Status indicator
      - File counts (specs, plans, tasks)
      - Last activity timestamp
      - Current active feature highlighting
```

### Step 4: Detailed Feature Status Mode

**Comprehensive feature analysis:**
```yaml
feature_analysis:
  detection_and_validation:
    location_process:
      - Locate feature directory structure
      - Validate proper .specpulse organization
      - Check for required subdirectories (specs/, plans/, tasks/)

    integrity_checks:
      - File structure validation
      - Required section completeness
      - Format consistency verification

  file_inventory_analysis:
    specification_files:
      counting: Number of specification files
      completeness: Analysis of spec completeness status
      quality: Assessment of spec detail and requirements

    plan_files:
      presence: Implementation plan existence
      quality: Plan detail and strategy assessment
      completeness: Phase breakdown and dependency mapping

    task_files:
      structure: Task breakdown structure analysis
      progress: Task completion status calculation
      quality: Task detail and dependency validation

  progress_calculation:
    detailed_metrics:
      overall_percentage: Based on task completion status
      task_distribution: Completed/in-progress/blocked/pending counts
      phase_breakdown: Progress by implementation phases
      velocity_metrics: Tasks completed per time period

    advanced_analytics:
      dependency_chains: Analysis of task dependencies and critical path
      parallel_availability: Count of tasks that can be executed in parallel
      bottleneck_identification: Tasks blocking progress of multiple dependent tasks

  task_status_analysis:
    parsing_process:
      - Parse task files to determine individual task status
      - Extract task metadata: title, description, dependencies, success criteria
      - Identify status markers: [x] completed, [ ] pending, [>] in progress, [!] blocked

    relationship_analysis:
      - Dependency relationship mapping and validation
      - Chain status analysis for sequential tasks
      - Parallel task availability identification
      - Blocker identification and resolution path analysis
```

### Step 5: Advanced Analysis Features

**Comprehensive analysis capabilities:**
```yaml
advanced_features:
  universal_id_system:
    tracking:
      - Track ID usage across specs, plans, and tasks
      - Monitor ID allocation patterns and conflicts
      - Validate ID numbering consistency and gaps

    conflict_detection:
      - Detect potential ID conflicts before they occur
      - Show ID allocation statistics and availability
      - Validate ID system integrity and consistency

  sdd_gates_compliance:
    specification_first:
      verification:
        - Verify specifications meet SDD standards
        - Check requirement completeness and clarity
        - Validate acceptance criteria and testability

    task_decomposition:
      analysis:
        - Check task traceability to requirements
        - Validate task completeness and atomicity
        - Assess dependency mapping and logic

    quality_assurance:
      evaluation:
        - Validate quality assurance presence and completeness
        - Check testing requirements and validation criteria
        - Assess code review processes and standards

    traceable_implementation:
      assessment:
        - Verify tasks linked to specifications
        - Validate requirements traceability matrix
        - Assess implementation coverage and completeness

  trend_analysis:
    progress_tracking:
      - Progress velocity over time analysis
      - Completion rate trends and patterns
      - Blocker frequency and resolution time tracking
      - Feature development patterns and workflows

    predictive_analytics:
      - Estimated completion time based on velocity
      - Risk assessment based on historical patterns
      - Resource allocation recommendations
      - Timeline optimization suggestions

  validation_health_check:
    structural_integrity:
      - File structure integrity validation
      - Required section completeness verification
      - Dependency cycle detection and resolution
      - Permission and access verification

    data_quality:
      - Content validation and format checking
      - Consistency verification across files
      - Error detection and correction recommendations
```

### Step 6: Context Management and Updates

**Comprehensive context handling:**
```yaml
context_management:
  maintenance:
    - Update .specpulse/memory/context.md with latest status
    - Track status check history for trend analysis
    - Link related features and dependencies
    - Maintain searchable status history

  synchronization:
    - Keep task status and context aligned
    - Update progress metrics automatically
    - Maintain consistency across all status reports
    - Ensure data integrity and accuracy
```

### Step 7: Status Reporting and Display

**Comprehensive status reporting:**
```yaml
status_reporting:
  project_overview_format:
    summary_section:
      - Total features count
      - Overall progress percentage
      - Active features count
      - Completed features count

    feature_listings:
      - Active features with progress indicators
      - Completed features with completion confirmation
      - In-progress features with blocking status
      - Paused features with activity gaps
      - Blocked features with issue identification

    metrics_section:
      - Average velocity calculations
      - Estimated project completion dates
      - Current blockers and issues
      - Trend analysis results

  detailed_feature_format:
    header_information:
      - Feature ID and name
      - Overall progress percentage
      - Status classification
      - Creation and last update timestamps

    file_structure_analysis:
      - Specification files count and status
      - Plan files presence and quality
      - Task files structure and progress

    progress_breakdown:
      - Task status distribution (completed/in-progress/blocked/pending)
      - Phase progress percentages
      - Velocity metrics and completion estimates
      - Available parallel tasks and sequential chains

    advanced_analytics:
      - SDD Gates compliance assessment
      - Dependency analysis and critical path
      - Blocker identification and resolution strategies
      - Risk assessment and mitigation recommendations
```

## Output Format

**Project overview response:**
```yaml
project_status:
  total_features: 5
  overall_progress: "42%"
  active_features: 2
  completed_features: 1

  features_by_status:
    active:
      - id: "001"
        name: "user-authentication"
        progress: "65%"
        last_activity: "2 hours ago"
        file_counts:
          specs: 2
          plans: 1
          tasks: 25

      - id: "002"
        name: "payment-processing"
        progress: "23%"
        last_activity: "1 day ago"
        file_counts:
          specs: 1
          plans: 1
          tasks: 18

    completed:
      - id: "000"
        name: "project-setup"
        progress: "100%"
        completion_date: "2025-01-05"

    paused:
      - id: "004"
        name: "notifications"
        progress: "78%"
        last_activity: "3 days ago"

  project_metrics:
    average_velocity: "2.3 tasks/day"
    estimated_completion: "2025-02-15"
    current_blockers: 1
    sdd_compliance: "91%"

  current_context:
    active_feature: "001-user-authentication"
    working_directory: "project-root/"
```

## Error Handling and Recovery

**Comprehensive error scenarios:**
```yaml
error_handling:
  context_detection_failures:
    no_memory_file:
      action: Create initial context structure
      recovery: Build context from available feature data

    invalid_feature_directory:
      action: Suggest valid feature names
      recovery: Provide feature selection from available options

    multiple_active_features:
      action: Prompt to select primary feature
      recovery: Allow user to choose working feature

    corrupted_task_files:
      action: Guide through file recovery process
      recovery: Restore from backups or recreate structure

  validation_errors:
    missing_directories:
      action: Create proper .specpulse structure
      recovery: Initialize missing directories with templates

    invalid_file_formats:
      action: Provide template corrections
      recovery: Guide through file format standardization

    dependency_cycles:
      action: Identify and resolve circular references
      recovery: Provide dependency resolution strategies

    permission_issues:
      action: Guide user through permission fixes
      recovery: Provide specific commands for permission restoration

  calculation_errors:
    invalid_task_statuses:
      action: Correct status marker format
      recovery: Standardize status markers across all files

    missing_progress_data:
      action: Recalculate from file timestamps
      recovery: Use metadata for progress estimation

    division_by_zero:
      action: Handle edge cases in percentage calculations
      recovery: Provide fallback calculations and indicators

    corrupted_id_system:
      action: Rebuild ID mapping from files
      recovery: Reconstruct universal ID system from existing files
```

## Safety Constraints

- **Path validation**: Only operate within `.specpulse/` directory
- **Protected directories**: Never modify `templates/`, `specpulse/`, AI configs
- **Atomic operations**: Prevent partial updates and corruption
- **Rollback capability**: Restore original state on failures
- **Input validation**: Comprehensive sanitization of all inputs

## Integration Features

- **Universal ID System**: Complete ID tracking and conflict prevention
- **SDD Gates Compliance**: Full specification-driven validation
- **Trend Analysis**: Comprehensive progress analytics and prediction
- **Health Monitoring**: Continuous system integrity validation
- **Context Management**: Automatic context updates and history tracking
- **Dependency Analysis**: Complete dependency mapping and critical path analysis