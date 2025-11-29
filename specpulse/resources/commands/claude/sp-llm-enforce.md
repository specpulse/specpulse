---
name: sp-llm-enforce
description: Enforce strict LLM compliance rules for SpecPulse operations
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-llm-enforce Command

Enforce strict LLM compliance rules for SpecPulse operations without CLI dependencies. Works completely independently through validated operations.

## Usage
```
/sp-llm-enforce [action] [context]    # Start enforcement session or check status
```

Actions: `start`, `status`, `validate`, `end` (defaults to `start`)

## Implementation

When called with `/sp-llm-enforce {{args}}`, I will:

### 1. Parse Arguments to Determine Enforcement Action

**I will analyze the arguments:**
- If action provided: Use specific enforcement action
- If no argument: Start new enforcement session
- Parse context information for targeted enforcement

### 2. For Action: start (default)

**I will initiate strict compliance enforcement:**

#### A. Session Initialization
- Create enforcement session with unique ID
- Initialize operation tracking
- Establish compliance boundaries
- Set directory access restrictions

#### B. Directory Enforcement Setup
- Restrict all operations to `.specpulse/` directory only
- Validate all file paths before operations
- Create safe operation whitelist
- Establish protected directory rules

#### C. Status Tracking Initialization
- Create session status tracking file
- Initialize operation counters
- Set up compliance validation rules
- Establish audit trail requirements

#### D. Memory Context Validation
- Validate current memory structure
- Check context file integrity
- Initialize compliance session memory
- Set operation context boundaries

### 3. For Action: status

**I will display current enforcement status:**

#### A. Session Information
- Show active enforcement session details
- Display operation counts and types
- Show compliance violations detected
- List tracked file operations

#### B. Compliance Metrics
- Directory restriction compliance: 100%
- File operation validation: Tracked/Validated
- Status update completeness: All operations logged
- Memory update accuracy: Context maintained

#### C. Risk Assessment
- Identify potential compliance risks
- Show blocked operation attempts
- Display violation patterns
- Recommend corrective actions

### 4. For Action: validate

**I will perform comprehensive compliance validation:**

#### A. Directory Structure Validation
- Verify all operations stay within `.specpulse/`
- Check for unauthorized directory access
- Validate file path safety
- Ensure no protected directories modified

#### B. Operation Tracking Validation
- Verify all file operations are tracked
- Check status update completeness
- Validate audit trail integrity
- Ensure proper operation logging

#### C. Memory Consistency Validation
- Validate memory file updates
- Check context file integrity
- Verify session state consistency
- Ensure no conflicting entries

#### D. Session Compliance Validation
- Verify all session rules followed
- Check enforcement protocol compliance
- Validate operation boundaries
- Ensure proper session termination

### 5. For Action: end

**I will terminate enforcement session:**

#### A. Session Finalization
- Generate comprehensive compliance report
- Validate all operations were compliant
- Create session audit summary
- Update final memory state

#### B. Report Generation
- Operation summary with counts
- Compliance violations (if any)
- Risk assessment results
- Recommendations for future operations

#### C. Memory Context Updates
- Finalize session memory updates
- Update context with session results
- Store compliance metrics
- Prepare for next session

## Enforcement Rules

### Strict Directory Enforcement
**I will ensure:**
- ✅ All file operations confined to `.specpulse/`
- ✅ No operations on protected directories
- ✅ Validated file paths before any operations
- ✅ Safe operation whitelist compliance

### Comprehensive Operation Tracking
**I will maintain:**
- ✅ Complete audit trail of all operations
- ✅ File creation and modification tracking
- ✅ Operation status updates before and after
- ✅ Justification for all changes made

### Memory Context Management
**I will update:**
- ✅ Memory files after every operation
- ✅ Operation context information
- ✅ Session state and compliance metrics
- ✅ Consistent context without conflicts

### Session Protocol Compliance
**I will follow:**
- ✅ Proper session initiation and termination
- ✅ Enforcement protocol throughout session
- ✅ Status reporting and validation
- ✅ Audit trail maintenance

## Output Examples

### Session Start
```
User: /sp-llm-enforce start

🔒 Enforcement Session Started
================================================================

Session ID: ENF-2025-01-11-001
Started At: 2025-01-11 15:30:00 UTC
Context: Full compliance enforcement mode

📋 Enforcement Rules Active:
   ✅ Directory restrictions: .specpulse/ only
   ✅ Operation tracking: Complete audit trail
   ✅ Status updates: Before/after every operation
   ✅ Memory management: Real-time context updates
   ✅ File validation: Path safety verification

🎯 Session Capabilities:
   - File operations within enforced boundaries
   - Operation tracking and validation
   - Compliance monitoring and reporting
   - Risk assessment and prevention

⚡ Enforcement Active - All operations will be monitored for compliance
💡 Use /sp-llm-enforce status to check compliance metrics
```

### Status Check
```
User: /sp-llm-enforce status

🔒 Enforcement Session Status
================================================================

Session ID: ENF-2025-01-11-001
Duration: 45 minutes 12 seconds
Status: Active and Compliant

📊 Operations Tracked:
   Files Created: 3
   Files Modified: 7
   Files Read: 15
   Directories Created: 2
   Status Updates: 20

✅ Compliance Metrics:
   Directory Restrictions: 100% compliant
   Operation Tracking: 100% complete
   Status Updates: 100% current
   Memory Updates: 100% accurate

🛡️  Risk Assessment:
   Low Risk: All operations within boundaries
   No violations detected
   Session integrity maintained
   Compliance score: 100%

📋 Last Operations:
   - Modified: .specpulse/tasks/001-auth/task-001.md (15:28:45)
   - Created: .specpulse/memory/session-enf-001.md (15:25:30)
   - Updated: .specpulse/memory/context.md (15:24:12)

⚡ Enforcement continues - All operations being monitored
```

### Validation Report
```
User: /sp-llm-enforce validate

🔍 Compliance Validation Results
================================================================

Session ID: ENF-2025-01-11-001
Validation Type: Full compliance check
Validated At: 2025-01-11 16:15:00 UTC

✅ Directory Compliance: 100%
   All operations within .specpulse/ boundaries
   No protected directory access attempts
   File path validation successful

✅ Operation Tracking: 100%
   All 25 operations properly tracked
   Complete audit trail maintained
   Status updates current for all operations

✅ Memory Management: 100%
   Memory files updated after operations
   Context consistency maintained
   No conflicting entries detected

✅ Session Protocol: 100%
   Proper session initiation and management
   Enforcement rules followed throughout
   Audit trail integrity verified

📊 Overall Compliance Score: 100%
⚠️ Issues Found: 0
🎯 Risk Level: Low

✅ Session is fully compliant with all enforcement rules
```

### Session End
```
User: /sp-llm-enforce end

🔒 Enforcement Session Ended
================================================================

Session ID: ENF-2025-01-11-001
Duration: 2 hours 35 minutes
Ended At: 2025-01-11 17:05:00 UTC

📊 Final Session Metrics:
   Total Operations: 42
   Files Created: 8
   Files Modified: 18
   Files Read: 28
   Status Updates: 42

✅ Final Compliance Results:
   Directory Restrictions: 100% compliant
   Operation Tracking: 100% complete
   Status Updates: 100% current
   Memory Management: 100% accurate

🎯 Session Summary:
   - Zero compliance violations
   - Complete operation tracking
   - Proper memory context management
   - Full protocol compliance

📋 Session Audit Report Created:
   File: .specpulse/memory/enforcement-report-enf-001.md
   Contains: Complete operation log, compliance metrics, risk assessment

✅ Enforcement session completed successfully
💡 New session can be started with /sp-llm-enforce start
```

## Error Handling and Recovery

### Compliance Violations
- **Directory breach detection**: Immediate operation blocking
- **Unauthorized operations**: Automatic session termination
- **Tracking failures**: Operation rollback and error reporting
- **Memory inconsistency**: Context repair and validation

### Session Recovery
- **Session interruption**: Resume with status validation
- **Operation failures**: Retry with compliance validation
- **Memory corruption**: Context restoration from backup
- **Enforcement override**: Emergency compliance protocols

This `/sp-llm-enforce` command provides **strict compliance enforcement** without requiring any SpecPulse CLI installation, using only validated file operations and comprehensive audit tracking.