# AI CLI Fallback Implementation Examples

This document shows how AI commands should implement CLI fallback logic.

## Example: /sp-spec Implementation

```python
# AI should implement this pattern:

def handle_sp_spec(args):
    """Handle /sp-spec command with CLI fallback"""

    # Step 1: Parse arguments
    description = extract_description(args)

    # Step 2: Try CLI first
    try:
        result = bash(f'specpulse spec create "{description}"')
        if result.exit_code == 0:
            # CLI succeeded - expand the created spec
            return expand_spec_from_cli_result(result)
    except Exception as e:
        log_warning(f"[FALLBACK] CLI command failed: specpulse spec create '{description}'")
        log_error(f"CLI Error: {e}")

    # Step 3: Apply fallback
    log_info("[FALLBACK] Using manual spec creation procedure")

    try:
        # Create directory structure
        feature_dir = create_feature_directory()

        # Create spec file with embedded template
        spec_file = create_spec_file(feature_dir, description)

        # Expand with AI content
        expand_spec_content(spec_file, description)

        return success_result(f"Spec created via fallback: {spec_file}")

    except Exception as fallback_error:
        log_error(f"[FALLBACK] Manual spec creation failed: {fallback_error}")
        return error_result("Both CLI and fallback procedures failed")

def create_feature_directory():
    """Create feature directory structure (fallback)"""

    # Detect current feature or create new one
    feature_id = detect_or_create_feature_id()
    feature_name = generate_feature_name()

    # Create directories
    dirs = [
        f".specpulse/specs/{feature_id}-{feature_name}",
        f".specpulse/plans/{feature_id}-{feature_name}",
        f".specpulse/tasks/{feature_id}-{feature_name}"
    ]

    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        log_debug(f"Created directory: {dir_path}")

    # Update context
    update_memory_context(feature_id, feature_name)

    return f"{feature_id}-{feature_name}"

def create_spec_file(feature_dir, description):
    """Create spec file with embedded template (fallback)"""

    # Get next spec number
    spec_num = get_next_spec_number(feature_dir)

    # Create spec file content
    content = f"""# Specification: {description}

<!-- FEATURE_DIR: {feature_dir} -->
<!-- FEATURE_ID: {feature_id} -->
<!-- SPEC_NUMBER: {spec_num:03d} -->
<!-- STATUS: pending -->
<!-- CREATED: {get_current_timestamp()} -->

## Description
{description}

## Requirements

### Functional Requirements
- [ ] Requirement 1
- [ ] Requirement 2

### Non-Functional Requirements
- [ ] Performance requirement
- [ ] Security requirement

## Acceptance Criteria

### User Stories
- **As a** [user role], **I want** [functionality], **so that** [benefit]
  - **Given** [context]
  - **When** [action]
  - **Then** [expected outcome]

## Technical Specifications

### Architecture
[Technical details]

### Dependencies
[External dependencies]

## Out of Scope
[What's not included]

## Success Metrics
[How to measure success]

## [NEEDS CLARIFICATION: Any uncertainties?]
"""

    spec_file = os.path.join(feature_dir, f"spec-{spec_num:03d}.md")

    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(content)

    log_info(f"[FALLBACK] Created spec file: {spec_file}")
    return spec_file
```

## CLI Error Detection Patterns

```python
def detect_cli_failure(bash_result):
    """Detect if CLI command failed"""

    # Check exit code
    if bash_result.exit_code != 0:
        return True, f"CLI exit code: {bash_result.exit_code}"

    # Check for common error patterns in output
    error_patterns = [
        "command not found",
        "No such file or directory",
        "Permission denied",
        "is not recognized",
        "ModuleNotFoundError",
        "ImportError"
    ]

    output_lower = bash_result.stdout.lower() + bash_result.stderr.lower()

    for pattern in error_patterns:
        if pattern.lower() in output_lower:
            return True, f"CLI error pattern: {pattern}"

    # Check for timeout
    if bash_result.duration > 30:  # 30 seconds
        return True, "CLI timeout"

    return False, ""
```

## Fallback Logging

```python
def log_fallback_usage(command, error_msg):
    """Log fallback usage for debugging"""

    timestamp = get_current_timestamp()
    log_entry = f"[{timestamp}] [FALLBACK] CLI command failed: {command}"
    log_entry += f"\n[{timestamp}] [FALLBACK] Error: {error_msg}"
    log_entry += f"\n[{timestamp}] [FALLBACK] Using manual procedure"

    # Write to fallback log
    with open(".specpulse/fallback.log", "a", encoding="utf-8") as f:
        f.write(log_entry + "\n\n")

    # Also output to console
    print(log_entry)
```

## Success Criteria for Fallback

```python
def validate_fallback_success(operation, result):
    """Validate that fallback operation succeeded"""

    if operation == "spec_create":
        return os.path.exists(result) and result.endswith(".md")

    elif operation == "plan_create":
        return os.path.exists(result) and "plan-" in result

    elif operation == "task_breakdown":
        return os.path.exists(result.replace(".md", "_breakdown.md"))

    return False
```

## Example Complete Workflow

```python
def complete_sp_spec_workflow(description):
    """Complete /sp-spec workflow with CLI fallback"""

    # Log operation start
    log_info(f"Starting /sp-spec for: {description}")

    # Step 1: Try CLI
    cli_success, cli_result = try_cli_command(f'specpulse spec create "{description}"')

    if cli_success:
        log_info("CLI succeeded - expanding spec")
        return expand_spec_file(cli_result.file_path, description)

    # Step 2: CLI failed - apply fallback
    log_warning("CLI failed - applying fallback procedure")

    # Step 2a: Create directory structure
    try:
        feature_dir = create_feature_directory()
        log_info(f"Created feature directory: {feature_dir}")
    except Exception as e:
        log_error(f"Failed to create directories: {e}")
        return error_result("Directory creation failed")

    # Step 2b: Create spec file
    try:
        spec_file = create_spec_file(feature_dir, description)
        log_info(f"Created spec file: {spec_file}")
    except Exception as e:
        log_error(f"Failed to create spec file: {e}")
        return error_result("Spec file creation failed")

    # Step 2c: Expand with AI content
    try:
        expand_spec_content(spec_file, description)
        log_info(f"Expanded spec content: {spec_file}")
    except Exception as e:
        log_error(f"Failed to expand spec content: {e}")
        # Don't fail completely - basic spec exists

    # Step 3: Return success
    success_msg = f"Spec created successfully via fallback: {spec_file}"
    log_info(success_msg)

    return success_result(success_msg, {
        "file_path": spec_file,
        "feature_dir": feature_dir,
        "method": "fallback"
    })
```

## Key Principles

1. **Always try CLI first** - CLI is the preferred method
2. **Immediate fallback** - Don't wait, apply fallback immediately on CLI failure
3. **Comprehensive logging** - Log all fallback usage for debugging
4. **Graceful degradation** - Even partial success is better than complete failure
5. **Consistent behavior** - All AI commands should follow the same fallback pattern
6. **User notification** - Always inform user when fallback is being used

## Testing Fallback Logic

```python
def test_cli_fallback():
    """Test CLI fallback logic"""

    # Test with valid CLI command
    result = handle_sp_spec("Test specification")
    assert result.success == True

    # Test with CLI failure (simulate by using non-existent command)
    # This should trigger fallback
    result = handle_sp_spec("Test specification")
    assert result.success == True  # Fallback should succeed
    assert result.method == "fallback"

    print("✅ CLI fallback logic working correctly")
```

Remember: **AI should never completely fail** when CLI is unavailable - fallback procedures ensure work can always continue!