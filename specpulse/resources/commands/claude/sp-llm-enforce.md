# SpecPulse LLM Enforcement Commands for Claude

## 🔒 STRICT COMPLIANCE REQUIRED
This is NOT a normal command. This enforces strict LLM compliance with no interpretation allowed.

## MANDATORY RULES (NO EXCEPTIONS)

### 1. SESSION MANAGEMENT
- ALWAYS start with compliance enforcement
- ALWAYS track all operations
- NEVER operate outside enforced session
- ALWAYS end session with validation

### 2. DIRECTORY ENFORCEMENT
- ALL files MUST stay within `.specpulse/`
- NEVER create files outside enforced structure
- ALWAYS validate file paths before operations
- NEVER bypass directory restrictions

### 3. STATUS TRACKING
- ALWAYS update task status before operations
- ALWAYS update task status after operations
- NEVER skip status updates
- ALWAYS provide justification for changes

### 4. FILE TRACKING
- ALWAYS track every file created
- ALWAYS track every file modified
- NEVER perform untracked file operations
- ALWAYS use proper tracking methods

### 5. MEMORY UPDATES
- ALWAYS update memory files after operations
- NEVER skip memory updates
- ALWAYS include operation context
- NEVER create conflicting memory entries

## USAGE EXAMPLES

### ✅ CORRECT: Create Specification
```python
from specpulse.core.llm_cli_interface import LLMCLIInterface
from specpulse.core.llm_compliance_enforcer import enforce_llm_compliance
from specpulse.core.llm_task_status_manager import LLMOperationType

# Initialize interface
cli = LLMCLIInterface(Path.cwd())

# Create specification (automatically enforced)
result = cli.create_specification(
    feature_id="001",  # EXACT: 3 digits
    feature_name="user-auth",  # EXACT: kebab-case
    template_type="tech"
)

# Check result
if result.success:
    print("Specification created successfully")
    print(f"Files affected: {result.files_affected}")
else:
    print(f"Error: {result.stderr}")
    raise Exception("Specification creation failed")
```

### ✅ CORRECT: Execute Task with Status Updates
```python
from specpulse.core.llm_cli_interface import LLMCLIInterface
from specpulse.core.llm_task_status_manager import TaskStatus

cli = LLMCLIInterface(Path.cwd()))

# Execute task with automatic compliance
result = cli.execute_task("001-user-auth-task-001")

# Task status is automatically updated
# Memory files are automatically updated
# File operations are automatically tracked

if not result.success:
    # Automatic error handling and status update
    raise Exception(f"Task execution failed: {result.stderr}")
```

### ❌ WRONG: Manual File Operations
```python
# NEVER DO THIS - Violates compliance rules
with open(".specpulse/specs/001-test.md", "w") as f:
    f.write("# Manual spec")  # ❌ UNTRACKED OPERATION
```

### ❌ WRONG: Skipping Status Updates
```python
# NEVER DO THIS - Violates compliance rules
cli.execute_task("001-user-auth-task-001")  # ❌ No status tracking
# Status not updated - COMPLIANCE VIOLATION
```

## ENFORCED OPERATIONS

### Specification Creation
```python
# ENFORCED: Validated parameters, tracked files, status updates
cli.create_specification(
    feature_id="001",  # Must be 3 digits
    feature_name="user-auth",  # Must be kebab-case
    template_type="tech",  # Valid template
    description="Optional description"  # Optional
)
```

### Plan Creation
```python
# ENFORCED: Links to specification, tracked files
cli.create_plan(
    feature_id="001",
    feature_name="user-auth",
    spec_number=1  # Optional
)
```

### Task Execution
```python
# ENFORCED: Status tracking, progress monitoring
cli.execute_task(
    task_id="001-user-auth-task-001",  # Exact format
    task_file="path/to/task.md"  # Optional
)
```

### Status Monitoring
```python
# ENFORCED: Always know current state
status = cli.get_status(detailed=True)
compliance = cli.get_compliance_status()
```

## COMPLIANCE VIOLATIONS (STRICTLY FORBIDDEN)

1. **No Session Management**: Operating without compliance enforcement
2. **Directory Violations**: Creating files outside `.specpulse/`
3. **Status Skipping**: Not updating task status properly
4. **File Violations**: Untracked file operations
5. **Memory Neglect**: Not updating memory files
6. **Parameter Violation**: Invalid parameter formats
7. **Timeout Violation**: Operations exceeding time limits

## ERROR HANDLING

### ✅ CORRECT: Proper Error Handling
```python
try:
    result = cli.create_specification("001", "user-auth", "tech")
    if result.success:
        # Continue with workflow
        pass
    else:
        # Handle failure properly
        print(f"Creation failed: {result.stderr}")
        # Status automatically updated to FAILED
except Exception as e:
    # Compliance automatically handles errors
    print(f"Error: {e}")
    # Session automatically ends with error status
```

### ❌ WRONG: Ignoring Errors
```python
result = cli.create_specification("001", "user-auth", "tech")
if not result.success:
    pass  # ❌ Ignoring failure violates compliance
```

## AUTOMATIC ENFORCEMENTS

The system automatically enforces:

1. **Session Validation**: All operations must be in valid sessions
2. **Path Validation**: All file paths validated against `.specpulse/`
3. **Status Validation**: All status transitions validated
4. **File Tracking**: All file operations automatically tracked
5. **Memory Updates**: Memory files automatically updated
6. **Error Handling**: Errors automatically handled and logged
7. **Compliance Scoring**: All operations scored for compliance
8. **Timeout Protection**: Operations automatically timeout

## REQUIRED WORKFLOW

1. **Initialize**: `cli = LLMCLIInterface(Path.cwd())`
2. **Execute**: Use enforced methods (create_specification, execute_task, etc.)
3. **Validate**: Check result.success
4. **Handle**: Proper error handling if needed
5. **Continue**: Only continue if success=True

## 🔒 ZERO TOLERANCE POLICY

- No interpretation of rules allowed
- No exceptions to compliance requirements
- No bypassing of enforcement mechanisms
- No ignoring of status updates
- No untracked file operations
- No manual memory management

## TESTING

Always test compliance:
```python
# Quick compliance test
from specpulse.core.llm_cli_tester import quick_cli_test

test_result = quick_cli_test()
if test_result['success_rate'] < 0.9:
    raise Exception("CLI compliance below 90%")
```

## EMERGENCY PROCEDURES

If compliance fails:
1. STOP all operations immediately
2. Run `cli.run_doctor(fix_issues=True)`
3. Check compliance status
4. Fix violations before continuing

---

**Remember**: This system enforces strict compliance with no room for interpretation.
Follow the rules exactly or operations will fail automatically.

**SpecPulse LLM Enforcement System v2.6.7**