# Migration Guide: v2.1.2 → v2.1.3

## 🎯 Overview

SpecPulse v2.1.3 introduces a **major CLI refactoring** with new `sp-*` commands that provide better organization, more features, and improved workflow.

## ⚠️ Breaking Changes

### 1. Removed `sp` Alias

**Before (v2.1.2):**
```bash
sp init my-project
sp validate --fix
```

**After (v2.1.3):**
```bash
specpulse init my-project
specpulse validate --fix
```

**Action Required:** Update any scripts or aliases that use `sp` command.

### 2. New Command Structure

Old commands still work but are **deprecated**:

| Old Command (deprecated) | New Command (v2.1.3) |
|-------------------------|----------------------|
| `specpulse feature init <name>` | `specpulse sp-pulse init <name>` |
| `specpulse feature continue <name>` | `specpulse sp-pulse continue <name>` |
| `specpulse spec create <desc>` | `specpulse sp-spec create <desc>` |
| `specpulse spec validate` | `specpulse sp-spec validate` |
| `specpulse plan create <desc>` | `specpulse sp-plan create <desc>` |
| `specpulse task breakdown <id>` | `specpulse sp-task breakdown <id>` |

**Note:** Old commands will be removed in v3.0.0.

## ✨ New Features in v2.1.3

### 27 New CLI Commands

#### sp-pulse (Feature Management) - 5 commands
```bash
specpulse sp-pulse init <name>           # Initialize feature
specpulse sp-pulse continue <name>       # Switch to existing feature
specpulse sp-pulse list                  # List all features
specpulse sp-pulse status                # Show current feature status
specpulse sp-pulse delete <name>         # Delete feature
```

#### sp-spec (Specification) - 7 commands
```bash
specpulse sp-spec create "<desc>"        # Create specification
specpulse sp-spec update <id> "<changes>" # Update specification
specpulse sp-spec validate [id]          # Validate spec(s)
specpulse sp-spec clarify <id>           # Show clarification markers
specpulse sp-spec list                   # List all specs
specpulse sp-spec show <id>              # Display spec content
specpulse sp-spec progress <id>          # Show completion %
```

#### sp-plan (Implementation Plans) - 7 commands
```bash
specpulse sp-plan create "<desc>"        # Create plan
specpulse sp-plan update <id> "<changes>" # Update plan
specpulse sp-plan validate [id]          # Validate plan(s)
specpulse sp-plan list                   # List all plans
specpulse sp-plan show <id>              # Display plan
specpulse sp-plan progress <id>          # Show progress
specpulse sp-plan phases <id>            # Show phases
```

#### sp-task (Task Management) - 8 commands
```bash
specpulse sp-task breakdown <plan-id>    # Generate tasks from plan
specpulse sp-task create "<desc>"        # Create manual task
specpulse sp-task update <id> "<changes>" # Update task
specpulse sp-task start <id>             # Mark as started
specpulse sp-task done <id>              # Mark as completed
specpulse sp-task list                   # List all tasks
specpulse sp-task show <id>              # Display task
specpulse sp-task progress               # Overall progress
```

## 🔄 Migration Steps

### Step 1: Upgrade Package

```bash
pip install --upgrade specpulse
# or
pip install specpulse==2.1.3
```

### Step 2: Update Scripts/Aliases

If you have custom scripts or shell aliases using `sp`:

**Before:**
```bash
# .bashrc or .zshrc
alias sp='specpulse'
```

**After:**
```bash
# Remove or update
# Option 1: Remove alias (recommended)
# Option 2: Keep but don't use 'sp' as command name
```

### Step 3: Update Workflow

**Old Workflow (v2.1.2):**
```bash
specpulse feature init user-auth
# Then LLM creates spec via file operations
```

**New Workflow (v2.1.3):**
```bash
specpulse sp-pulse init user-auth
specpulse sp-spec create "OAuth2 authentication"
# Then LLM expands the spec
specpulse sp-spec validate 001
```

### Step 4: Test New Commands

```bash
# Verify installation
specpulse --version
# Should show: SpecPulse 2.1.3

# Test new commands
specpulse sp-pulse --help
specpulse sp-spec --help
specpulse sp-plan --help
specpulse sp-task --help
```

## 💡 Key Improvements

### 1. Context-Aware Operations

**Before:**
```bash
specpulse spec create "description" --feature 001-user-auth
```

**After:**
```bash
specpulse sp-spec create "description"
# Auto-detects feature from memory/context.md or git branch
```

### 2. Better Progress Tracking

**New:**
```bash
specpulse sp-spec progress 001
# Shows:
#   ✓ Requirements
#   ✓ User Stories
#   ✗ Acceptance Criteria
#   Completion: 66%
```

### 3. Enhanced Metadata

All files now have automatic metadata:
```markdown
<!-- SPECPULSE_METADATA
FEATURE_DIR: 001-user-auth
FEATURE_ID: 001
SPEC_ID: 001
CREATED: 2025-10-08T19:00:00
STATUS: draft
-->
```

### 4. Feature Switching

**New:**
```bash
# Switch between features easily
specpulse sp-pulse continue 001-user-auth
specpulse sp-pulse continue 002-payment
```

## 🚨 Important Notes

### SpecPulse Role (Unchanged)

**SpecPulse is STILL just a framework:**
- ✅ Creates structure (folders, templates, metadata)
- ✅ Validates structure (sections present?)
- ✅ Calculates progress (% complete)
- ❌ Does NOT generate content
- ❌ Does NOT write requirements
- ❌ Does NOT make decisions

**LLM still does all content generation:**
- Writing specifications
- Creating implementation plans
- Breaking down tasks
- Making technical decisions

### Slash Commands Updated

All slash commands (`.claude/commands/*.md`) are updated to use new CLI:

```markdown
# In Claude Code:
/sp-pulse user-authentication
# Runs: specpulse sp-pulse init user-authentication

/sp-spec OAuth2 with JWT
# Runs: specpulse sp-spec create "OAuth2 with JWT"
# Then AI expands the spec
```

## 📚 Updated Documentation

- `CLAUDE.md` - Updated workflow rules
- `CHANGELOG.md` - v2.1.3 entry added
- Slash commands - CLI-first workflow
- This migration guide

## 🆘 Troubleshooting

### Issue: `sp: command not found`

**Cause:** `sp` alias removed in v2.1.3

**Solution:** Use full `specpulse` command

### Issue: Old commands not working

**Cause:** Deprecated commands may have issues

**Solution:** Use new `sp-*` commands:
```bash
# Instead of:
specpulse feature init name

# Use:
specpulse sp-pulse init name
```

### Issue: Commands show "Not a SpecPulse project"

**Solution:**
```bash
# Make sure you're in a SpecPulse project
ls .specpulse/config.yaml

# Or initialize
specpulse init --here
```

## 📞 Support

- **GitHub Issues**: https://github.com/specpulse/specpulse/issues
- **Documentation**: `docs/`
- **Help Command**: `specpulse --help`

## 🎯 Benefits of Upgrading

1. **27 new commands** - More control and flexibility
2. **Context-aware** - Less typing, auto-detection
3. **Better progress tracking** - Know exactly where you are
4. **Enhanced metadata** - Automatic tracking
5. **Modular code** - Easier to maintain and extend
6. **Future-proof** - Ready for v3.0 features

**Upgrade is smooth and backward-compatible (except `sp` alias)!**
