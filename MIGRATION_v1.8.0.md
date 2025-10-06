# Migration Guide: v1.7.0 → v1.8.0

## Overview

SpecPulse v1.8.0 introduces **Better Validation Feedback** with three major components:
1. **Actionable Validation Messages** - Enhanced errors with examples and suggestions
2. **Partial Validation** - Progressive validation for incomplete specs
3. **Custom Validation Rules** - Project-specific validation

**Good News**: All changes are **100% backward compatible**. Existing validation continues to work unchanged.

---

## What's New in v1.8.0

### Component 3.1: Actionable Validation Messages

**Before** (v1.7.0):
```
❌ Validation failed
Missing sections: Acceptance Criteria
```

**After** (v1.8.0):
```
╭───────────── Validation Error ─────────────╮
│ ❌ Missing: Acceptance Criteria             │
│                                             │
│ What this means:                            │
│   Acceptance criteria define when the       │
│   feature is "done"                         │
│                                             │
│ Example:                                    │
│   ✓ User can login with email/password     │
│   ✓ Invalid credentials show error         │
│                                             │
│ Suggestion for LLM:                         │
│   Add section '## Acceptance Criteria'      │
│   with 3-5 testable conditions              │
│                                             │
│ Quick fix:                                  │
│   specpulse validate 001 --fix              │
╰─────────────────────────────────────────────╯
```

**New Features**:
- Enhanced error messages with meaning, examples, suggestions
- Auto-fix command: `specpulse validate --fix`
- 20+ validation examples in YAML
- Rich-formatted output with color coding

### Component 3.2: Partial Validation

**New Command**: `specpulse validate --partial`

**Example Output**:
```
Progress: 40% complete

✓ Executive Summary (complete)
✓ Problem Statement (complete)
⚠️ Requirements (2 items - consider adding 1-2 more)
⭕ User Stories (not started)
⭕ Acceptance Criteria (not started)

Next suggested section: Requirements
```

**New Features**:
- Progressive validation for work-in-progress specs
- Completion percentage tracking
- Section status indicators (✓ complete, ⚠️ partial, ⭕ missing)
- Smart next section suggestions
- No errors for incomplete specs

### Component 3.3: Custom Validation Rules

**New File**: `.specpulse/validation_rules.yaml`

**Example**:
```yaml
rules:
  - name: security_requirement
    enabled: true
    message: "Web apps should include security requirements"
    applies_to: [web-app, api]
    severity: warning
```

**New Commands**:
```bash
specpulse validation rules list
specpulse validation rules enable security_requirement
specpulse validation rules disable accessibility_check
specpulse validation rules add my_custom_rule --template
```

**New Features**:
- Project-type-aware validation (web-app, api, mobile-app, etc.)
- 12 default rules for common project types
- Enable/disable rules per project
- Create custom rules
- Automatic project type detection

---

## Migration Steps

### Step 1: Update SpecPulse

```bash
pip install --upgrade specpulse
# or
pip install specpulse==1.8.0
```

### Step 2: (Optional) Enable Custom Rules

If you want project-specific validation rules:

```bash
# Copy default rules to your project
cp specpulse/resources/validation_rules.yaml .specpulse/validation_rules.yaml

# Enable desired rules
specpulse validation rules enable security_requirement
specpulse validation rules enable accessibility_check
```

### Step 3: (Optional) Set Project Type

For better custom rule matching:

```bash
# Edit .specpulse/project_context.yaml (if exists from v1.7.0)
project:
  type: web-app  # or: api, mobile-app, desktop, cli, library
```

Or let SpecPulse auto-detect from your project files (package.json, pyproject.toml, etc.).

### Step 4: Try New Features

```bash
# Enhanced validation errors
specpulse validate

# Auto-fix missing sections
specpulse validate --fix

# Partial validation for WIP specs
specpulse validate --partial

# Show completion percentage only
specpulse validate --progress

# View all validation examples
specpulse validate --show-examples
```

---

## Breaking Changes

**None!** All v1.7.0 validation behavior is preserved. New features are opt-in via flags.

---

## New CLI Flags

### `specpulse validate` Command

| Flag | Description | Example |
|------|-------------|---------|
| `--fix` | Auto-fix validation issues | `specpulse validate --fix` |
| `--partial` | Progressive validation (no errors for incomplete specs) | `specpulse validate --partial` |
| `--progress` | Show only completion % | `specpulse validate --progress` |
| `--show-examples` | Display all validation examples | `specpulse validate --show-examples` |

### New `validation rules` Subcommands

```bash
specpulse validation rules list                    # List all rules
specpulse validation rules enable <rule-name>      # Enable a rule
specpulse validation rules disable <rule-name>     # Disable a rule
specpulse validation rules add <name> --template   # Add custom rule
```

---

## API Changes (for Python API users)

### New Classes

```python
from specpulse.core.validator import ValidationExample, ValidationProgress
from specpulse.core.custom_validation import ValidationRule, RuleEngine, ProjectType
from specpulse.utils.project_detector import ProjectDetector
from specpulse.utils.rule_manager import RuleManager
```

### New Methods

```python
validator = Validator()

# Load validation examples
examples = validator.load_validation_examples()  # Returns Dict[str, ValidationExample]

# Get specific example
example = validator.get_validation_example("missing_acceptance_criteria")

# Check section with enhanced errors
error = validator._check_section_exists(content, "User Stories")  # Returns Optional[ValidationExample]

# Format enhanced error
formatted = validator.format_enhanced_error(example)
plain = validator.format_enhanced_error_plain(example)

# Auto-fix
success, changes, backup = validator.auto_fix_validation_issues(spec_path, backup=True)

# Partial validation
progress = validator.validate_partial(spec_path)  # Returns ValidationProgress
print(f"Completion: {progress.completion_pct}%")
print(f"Next: {progress.next_suggestion}")
```

---

## Configuration Files

### validation_examples.yaml

Location: `specpulse/resources/validation_examples.yaml`

Contains 20+ pre-defined validation examples with:
- Error message
- Meaning explanation
- Concrete example
- Actionable suggestion
- Help command
- Auto-fix capability flag

**You don't need to modify this file** - it's used automatically.

### validation_rules.yaml

Location: `specpulse/resources/validation_rules.yaml` (default)
User override: `.specpulse/validation_rules.yaml` (project-specific)

Contains 12 default rules:
- **Web-app**: security_requirement, accessibility_check, performance_requirement
- **API**: api_documentation, rate_limiting, authentication_requirement
- **Mobile**: platform_support, offline_mode, app_store_requirements
- **General**: error_handling_strategy, testing_strategy, deployment_strategy

**To customize**: Copy to `.specpulse/validation_rules.yaml` and enable desired rules.

---

## Troubleshooting

### Auto-fix not working?

Check that:
1. You're using `--fix` flag: `specpulse validate --fix`
2. File is writable (not read-only)
3. Backup directory `.specpulse/backups/` can be created

### Custom rules not triggering?

Check that:
1. Rules are enabled: `specpulse validation rules list`
2. Project type is detected: See `.specpulse/project_context.yaml`
3. Rule's `applies_to` matches your project type

### Enhanced errors not showing?

Enhanced errors are always shown in v1.8.0. If you see plain errors:
1. Check you're using v1.8.0: `specpulse --version`
2. Validation examples YAML is present: `ls specpulse/resources/validation_examples.yaml`

---

## Performance Impact

**Minimal!** Validation performance impact:
- Enhanced errors: <5% overhead (caching used)
- Partial validation: Same speed as full validation
- Custom rules: <10% overhead (only if rules enabled)

**Overall**: Validation still completes in <2 seconds for typical specs.

---

## Rollback to v1.7.0

If you need to rollback:

```bash
pip install specpulse==1.7.0
```

All v1.7.0 features continue to work in v1.8.0, so rollback should be seamless.

---

## Getting Help

### Validation Examples
```bash
specpulse validate --show-examples  # See all examples
```

### Custom Rules
```bash
specpulse validation rules list           # See all rules
specpulse validation rules add --template # Generate rule template
```

### Documentation
- See `docs/validation_examples.md` for validation guidance
- See `docs/custom_rules.md` for custom rule creation

---

## Checklist for Migration

- [ ] Update to v1.8.0: `pip install --upgrade specpulse`
- [ ] Try enhanced validation: `specpulse validate`
- [ ] (Optional) Enable custom rules: Copy validation_rules.yaml
- [ ] (Optional) Set project type in project_context.yaml
- [ ] Try partial validation on WIP spec: `specpulse validate --partial`
- [ ] Try auto-fix: `specpulse validate --fix`
- [ ] Run tests to ensure everything works

---

## What's Next (v1.9.0)

Future features being considered:
- Incremental spec building (section-by-section workflow)
- Spec checkpoints (versioning)
- Feature dependencies tracking
- See ROADMAP.md for details

---

**Upgrade today and enjoy better validation feedback!** 🚀

For issues or questions: https://github.com/specpulse/specpulse/issues
