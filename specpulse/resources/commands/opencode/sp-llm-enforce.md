---
name: sp-llm-enforce
description: Enforce strict LLM compliance rules for SpecPulse operations without SpecPulse CLI
version: "1.0"
agent: specpulse-assistant
workflow_type: compliance_enforcement
---

# SpecPulse LLM Compliance Enforcement Workflow

This workflow implements complete CLI-independent LLM compliance enforcement with real-time monitoring and violation prevention.

## Agent Capabilities Required

- File operations: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
- Directory traversal protection and validation
- Compliance monitoring and enforcement
- Real-time violation detection and correction
- Session management and configuration
- Error recovery and rollback mechanisms

## Workflow Steps

### Step 1: Argument Parsing and Enforcement Action Determination

**Parse input arguments:**
```yaml
inputs:
  action: enum [start, status, validate, end]
  enforcement_context: string
  rule_severity: enum [low, medium, high, critical]
```

**Action determination logic:**
```yaml
action_logic:
  action_provided:
    condition: action parameter provided
    action: Use specified enforcement action
    validation: Validate action parameter against allowed values

  default_action:
    condition: No action provided
    action: Default to "start" enforcement session
    behavior: Begin compliance monitoring with default settings
```

### Step 2: Compliance Rule Initialization

**Compliance framework setup:**
```yaml
compliance_framework:
  protected_directories:
    never_modify:
      - templates/
      - .specpulse/
      - specpulse/
      - .claude/
      - gemini/
      - .windsurf/
      - .cursor/
      - .github/
      - .opencode/
    editable_only:
      - specs/
      - plans/
      - tasks/
      - memory/

  rule_categories:
    directory_traversal:
      description: Prevent access outside allowed directories
      patterns: ["../", "C:\\", "/etc/", "/usr/"]
      severity: critical
      action: block

    file_modification:
      description: Validate file modification operations
      protected_patterns: ["*.exe", "*.dll", "*.so", "*.dylib"]
      severity: high
      action: validate

    content_validation:
      description: Check file content for malicious patterns
      scan_types: [markdown_syntax, encoding_validation, content_patterns]
      severity: medium
      action: scan_and_correct
```

### Step 3: CLI-First Compliance Validation

**CLI priority enforcement:**
```yaml
cli_first_approach:
  step_1: {
    action: "Check for SpecPulse CLI availability",
    method: "bash",
    command: "specpulse --version"
    fallback: "Continue with file-based enforcement"
  }

  step_2: {
    action: "Attempt CLI operations first",
    validation: "Verify CLI command success before file operations",
    fallback: "Use file operations if CLI fails"
  }

  step_3: {
    action: "Enforce atomic operations",
    requirement: "All operations must be atomic with rollback capability",
    implementation: "File operations with validation and recovery"
  }
```

### Step 4: Real-Time Compliance Monitoring

**Active monitoring system:**
```yaml
monitoring_system:
  file_operation_monitoring:
    track_operations: [create, modify, delete, move, copy]
    validation_points:
      - Pre-operation: Path validation and permission check
      - During operation: Content validation and rule enforcement
      - Post-operation: Integrity verification and audit logging

  violation_detection:
   实时监控:
      - Directory access attempts outside allowed paths
      - File modification in protected directories
      - Suspicious content patterns
      - Unauthorized operation attempts

  enforcement_actions:
    violation_types:
      directory_traversal:
        action: "Block operation with error message"
        logging: "Log violation details to audit trail"
        notification: "Alert user about security violation"

      protected_directory_access:
        action: "Redirect to safe operation"
        guidance: "Provide correction instructions"
        validation: "Verify compliance with rules"

      content_violations:
        action: "Clean or sanitize content"
        quarantine: "Isolate problematic content"
        reporting: "Generate violation report"
```

### Step 5: Session Management and Configuration

**Enforcement session management:**
```yaml
session_management:
  session_lifecycle:
    start_session:
      action: "Initialize compliance enforcement"
      configuration: "Load rule settings and monitoring options"
      state_management: "Create session state tracking"
      logging: "Start audit trail logging"

    active_monitoring:
      action: "Real-time compliance monitoring"
      rule_enforcement: "Apply configured compliance rules"
      violation_handling: "Detect, correct, and report violations"
      status_reporting: "Periodic compliance status updates"

    end_session:
      action: "Terminate enforcement session"
      final_report: "Generate compliance summary and statistics"
      cleanup: "Clean up session state and temporary data"
      archiving: "Archive session logs and audit trail"
```

### Step 6: Status Reporting and Analytics

**Compliance status reporting:**
```yaml
status_reporting:
  compliance_scoring:
    calculation_method: "Weighted scoring based on violation types and severity"
    score_ranges:
      excellent: [90, 100]
      good: [75, 89]
      acceptable: [60, 74]
      poor: [0, 59]

  reporting_components:
    violation_summary:
      - Total violations by category
      - Severity distribution
      - Resolution success rate
      - Repeat violation analysis

    compliance_metrics:
      - Compliance score over time
      - Rule effectiveness analysis
      - Trend identification and prediction
      - Performance impact assessment

    risk_assessment:
      - Security risk evaluation
      - Compliance risk levels
      - Mitigation recommendations
      - Priority-based action planning
```

### Step 7: Error Prevention and Recovery

**Comprehensive error handling:**
```yaml
error_handling:
  prevention_strategies:
    input_validation:
      - Validate all inputs before processing
      - Sanitize file paths and content
      - Check permissions before operations
      - Validate operation parameters

    atomic_operations:
      - Implement rollback mechanisms
      - Create operation snapshots
      - Validate integrity before commit
      - Maintain operation logs

  recovery_procedures:
    operation_failure:
      - Rollback to pre-operation state
      - Log failure details and context
      - Provide specific error guidance
      - Offer alternative approaches

    permission_denied:
      - Provide permission fix instructions
      - Suggest alternative safe operations
      - Document resolution steps
      - Implement validation checks

    corruption_prevention:
      - Create backup files before changes
      - Validate file integrity after operations
      - Implement corruption detection
      - Maintain recovery procedures
```

### Step 8: Advanced Features and Capabilities

**Enhanced compliance features:**
```yaml
advanced_features:
  real_time_monitoring:
    violation_detection: "Immediate detection and response"
    automated_correction: "Auto-fix common compliance issues"
    adaptive_rules: "Dynamic rule adjustment based on patterns"
    predictive_analysis: "Anticipate potential violations"

  audit_trail_generation:
    comprehensive_logging: "Complete operation audit trail"
    compliance_reports: "Regular compliance status reports"
    violation_tracking: "Detailed violation history and analysis"
    trend_analysis: "Compliance trend identification and prediction"

  session_customization:
    rule_configuration: "Customizable rule sets and severity levels"
    monitoring_sensitivity: "Adjustable monitoring thresholds"
    reporting_frequency: "Configurable status update intervals"
    integration_options: "External monitoring and alerting integration"
```

**CLI-Independent Benefits:**
- Complete compliance enforcement without CLI dependencies
- Real-time monitoring with automated violation prevention
- Comprehensive reporting and analytics
- Atomic operations with guaranteed integrity and rollback

**Advanced Compliance Features:**
- Real-time violation detection with automated corrections
- Adaptive rule systems that learn from patterns
- Session-based management with persistent configuration
- Comprehensive audit trail generation and analysis

**Error Handling and Recovery:**
- Input validation and sanitization for all operations
- Comprehensive error recovery with rollback mechanisms
- Permission issue resolution with detailed guidance
- Complete data corruption prevention and recovery

**Safety and Security Features:**
- Directory traversal protection with multi-layer validation
- File operation security with comprehensive validation
- Atomic operation rollback with integrity verification
- Complete error handling with detailed recovery procedures

## Output Format

**Compliance Session Report:**
```yaml
session_summary:
  session_id: "compliance-session-001"
  enforcement_action: "start"
  duration: "45 minutes"
  rule_severity: "medium"

compliance_metrics:
  overall_score: 87
  violations_detected: 3
  violations_resolved: 3
  repeat_violations: 0

violation_summary:
  category_counts:
    directory_traversal: 0
    protected_directory_access: 1
    content_violations: 2

  severity_distribution:
    critical: 0
    high: 1
    medium: 2
    low: 0

recommendations:
  - "Continue current compliance level"
  - "Monitor for pattern changes"
  - "Review rule effectiveness"
```

## Implementation Notes

When called with `/sp-llm-enforce {{args}}`, the workflow should:
1. Parse and validate arguments
2. Initialize compliance framework
3. Start real-time monitoring
4. Enforce compliance rules
5. Generate status reports and analytics
6. Manage session lifecycle and configuration