# LLM-Safe Operations Guide

## 🚨 CRITICAL: NEVER Use These Operations Directly

**LLM MUST NOT use direct file operations! Always use the safe systems!**

### ❌ FORBIDDEN OPERATIONS (NEVER DO THESE)

```bash
# NEVER create directories manually
mkdir -p specs/001-feature
mkdir -p .specpulse/plans/my-feature

# NEVER create files manually
touch specs/001-feature/spec.md
echo "content" > plans/001-feature/plan.md

# NEVER use CLI commands for file operations
specpulse feature init my-feature
specpulse spec create "description"

# NEVER edit template files
vi templates/spec.md
edit .specpulse/templates/plan.md

# NEVER use arbitrary file names
echo "content" > specs/my-spec.md
echo "content" > tasks/T1.md
```

### ✅ APPROVED OPERATIONS (ALWAYS USE THESE)

## 1. Feature Creation

**Command:** `/sp-pulse-safe <feature-name>`

```python
# ✅ CORRECT: Use safe system
from specpulse.utils.llm_safe_file_operations import get_llm_safe_operations

file_ops = get_llm_safe_operations(Path.cwd())
feature_id, dirs = file_ops.create_feature_directories("user authentication")

# This creates:
# - specs/001-user-authentication/
# - plans/001-user-authentication/
# - tasks/001-user-authentication/
# - Atomic feature ID generation
# - Sanitized naming
# - No race conditions
```

## 2. Specification Creation

**Command:** `/sp-spec-safe "<description>"`

```python
# ✅ CORRECT: Use template system
from specpulse.utils.llm_safe_template_system import get_template_system

template_system = get_template_system(Path.cwd())
success, result, metadata = template_system.create_specification_safe(
    "user-auth",
    "OAuth2 authentication with JWT tokens"
)

# This creates:
# - specs/001-user-authentication/spec-001.md
# - Validated template rendering
# - Proper variable substitution
# - Atomic file write
```

## 3. Plan Creation

**Command:** `/sp-plan-safe "<description>"`

```python
# ✅ CORRECT: Use safe plan creation
template_system = get_template_system(Path.cwd())
success, result, metadata = template_system.create_plan_safe(
    "001-user-authentication",
    "Implementation plan for OAuth2 authentication"
)

# This creates:
# - plans/001-user-authentication/plan-001.md
# - Validated naming
# - Template-based content
```

## 4. Task Creation

**Command:** `/sp-task-safe "<description>"`

```python
# ✅ CORRECT: Use safe task creation
template_system = get_template_system(Path.cwd())
success, result, metadata = template_system.create_task_safe(
    "001-user-authentication",
    "Setup authentication middleware",
    {"COMPLEXITY": "medium", "ESTIMATED_HOURS": "4"}
)

# This creates:
# - tasks/001-user-authentication/T001.md
# - Proper task numbering
# - Template content
```

## 5. Context Management

```python
# ✅ CORRECT: Update context safely
context_file = Path.cwd() / ".specpulse" / "memory" / "context.md"
file_ops.atomic_write_file(context_file, context_content)

# NEVER: echo "content" > .specpulse/memory/context.md
```

## 6. File Reading

```python
# ✅ CORRECT: Validate before reading
if file_ops.validate_file_operation(file_path, "read"):
    content = file_path.read_text()

# NEVER: Read arbitrary files without validation
content = Path("any_file.txt").read_text()
```

## Strict Validation Rules

### Feature Directory Names
- ✅ **Valid:** `001-user-authentication`, `042-payment-processing`
- ❌ **Invalid:** `user-auth`, `auth`, `my-feature`, `001`

### Spec File Names
- ✅ **Valid:** `spec-001.md`, `spec-002.md`, `spec-010.md`
- ❌ **Invalid:** `spec.md`, `spec-1.md`, `Specification.md`

### Plan File Names
- ✅ **Valid:** `plan-001.md`, `plan-002.md`, `plan-010.md`
- ❌ **Invalid:** `plan.md`, `plan-1.md`, `implementation.md`

### Task File Names
- ✅ **Valid:** `T001.md`, `T002.md`, `T010.md`
- ✅ **Valid (Service):** `AUTH-T001.md`, `USER-T002.md`
- ❌ **Invalid:** `task.md`, `task-1.md`, `my-task.md`

## Validation Checklist

Before ANY file operation, system validates:

### Path Validation
- [ ] Path is within `.specpulse/` directory
- [ ] No directory traversal (`..`)
- [ ] No forbidden characters (`<>:"|?*`)
- [ ] No forbidden names (`CON`, `PRN`, `AUX`, etc.)
- [ ] Path length < 255 characters
- [ ] Not in protected directories (`templates/`, `commands/`)

### Content Validation
- [ ] Template variables are valid
- [ ] Required variables provided
- [ ] Content length reasonable (<10KB per variable)
- [ ] No dangerous content injection

### Operation Validation
- [ ] Write operations allowed in this location
- [ ] File doesn't already exist (or overwrite intended)
- [ ] Sufficient permissions
- [ ] Atomic operation possible

## Error Prevention

### Common Mistakes to Avoid

1. **Manual Directory Creation**
   ```bash
   # ❌ WRONG
   mkdir -p specs/my-feature

   # ✅ RIGHT
   /sp-pulse-safe "my feature"
   ```

2. **Manual File Creation**
   ```bash
   # ❌ WRONG
   echo "# Spec" > specs/001-feature/spec.md

   # ✅ RIGHT
   /sp-spec-safe "Feature specification"
   ```

3. **CLI Command Usage**
   ```bash
   # ❌ WRONG
   specpulse feature init my-feature

   # ✅ RIGHT
   /sp-pulse-safe "my feature"
   ```

4. **Template Modification**
   ```bash
   # ❌ WRONG
   vi .specpulse/templates/spec.md

   # ✅ RIGHT
   # Never modify templates - use safe system
   ```

## Debugging Safe Operations

### Check Project Structure
```python
from specpulse.utils.llm_safe_file_operations import get_llm_safe_operations

file_ops = get_llm_safe_operations(Path.cwd())
results = file_ops.validate_project_structure()

if not results["valid"]:
    print("Project structure issues:")
    for error in results["errors"]:
        print(f"  ❌ {error}")
```

### List Available Templates
```python
from specpulse.utils.llm_safe_template_system import get_template_system

template_system = get_template_system(Path.cwd())
templates = template_system.list_templates()

for name, metadata in templates.items():
    print(f"📄 {name}: {metadata.get('description', 'No description')}")
```

### Validate Template Variables
```python
template_content = template_content
variables = {"FEATURE_ID": "001", "FEATURE_NAME": "test"}

success, missing_vars = template_system.validate_template_variables(template_content, variables)

if not success:
    print(f"Missing variables: {missing_vars}")
```

## Performance Monitoring

### Operation Logging
All operations are logged to:
- `.specpulse/logs/operations.log` - File operations
- `.specpulse/logs/template_operations.log` - Template operations
- `.specpulse/logs/validation.log` - Validation results

### Performance Metrics
- Operation success rate
- Average execution time
- Error frequency
- Most common failures

## Emergency Procedures

### If Safe Operations Fail

1. **Check Project Structure**
   ```bash
   /sp-pulse-safe "test-feature"  # Test if system works
   ```

2. **Validate Project**
   ```python
   file_ops.validate_project_structure()
   ```

3. **Check Permissions**
   ```bash
   ls -la .specpulse/
   chmod 755 .specpulse/
   ```

4. **Reset Feature Counter**
   ```bash
   rm .specpulse/feature_counter.txt
   # System will recreate on next operation
   ```

## Migration from Unsafe to Safe Operations

### Step 1: Identify Existing Unsafe Files
```bash
find .specpulse -name "*.md" | grep -v -E "(spec-[0-9]{3}\.md|plan-[0-9]{3}\.md|T[0-9]{3}\.md)"
```

### Step 2: Rename to Safe Format
```python
# Example: Rename spec.md to spec-001.md
# Use safe system to create new file with proper name
```

### Step 3: Update References
```python
# Update context files to use new naming
# Update any hardcoded references
```

### Step 4: Validate
```python
file_ops.validate_project_structure()
```

Remember: **NEVER use direct file operations! Always use the safe systems!**