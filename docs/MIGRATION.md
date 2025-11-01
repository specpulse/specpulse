# SpecPulse Migration Guide

## v2.1.2 → v2.4.1 (Current)

### 📋 Overview

SpecPulse v2.4.1 introduces the CLI-First Architecture, a fundamental shift in how AI assistants interact with SpecPulse. This is a **backward compatible** upgrade that improves performance and maintains all existing functionality.

### 🔧 Key Changes in v2.4.1

**Major Architectural Change:**
- ✅ **CLI-First Architecture**: AI assistants must try CLI commands before file operations
- ✅ **Deprecated AI Commands**: `specpulse ai *` commands removed in favor of direct CLI usage
- ✅ **Enhanced Validation**: Improved validation system with auto-fix capabilities
- ✅ **Better Error Handling**: More informative error messages and recovery suggestions
- ✅ **Performance Improvements**: Faster command execution and reduced overhead

**What Stayed the Same:**
- ✅ All existing specs, plans, tasks remain compatible
- ✅ Templates unchanged
- ✅ Memory system unchanged
- ✅ AI assistant integration (Claude/Gemini) unchanged
- ✅ Slash commands work the same way

---

### 🚀 Migration Steps to v2.4.1

#### Step 1: Upgrade SpecPulse

```bash
# Upgrade to latest version
pip install --upgrade specpulse

# Verify version
specpulse --version
# Should show: 2.4.1
```

#### Step 2: Update Workflow (Optional)

For **existing projects**, the workflow remains the same but AI assistants should now follow the CLI-first approach:

**Old Workflow (AI commands):**
```bash
# Deprecated - no longer needed
specpulse ai context
specpulse ai suggest
```

**New Workflow (Direct CLI):**
```bash
# Use CLI commands directly
specpulse feature init my-feature
specpulse spec create "My feature description"
specpulse plan create "Implementation plan"
specpulse task breakdown <plan-id>
```

#### Step 3: Test New Features

```bash
# Test enhanced validation
specpulse validate all --fix

# Test improved error handling
specpulse doctor

# Test new CLI capabilities
specpulse feature --help
```

**That's it!** No data migration needed - all existing files remain compatible.

---

### 📊 CLI-First Architecture

**The New Workflow Pattern:**

```
User Request: /sp-spec OAuth2 login with JWT
    ↓
Step 1: Try CLI first
    Bash: specpulse spec create "OAuth2 login with JWT"
    ↓
Step 2: If CLI doesn't exist, use File Operations:
    Claude reads: .specpulse/templates/spec.md
    Claude writes: .specpulse/specs/001-feature/spec-001.md
    Claude edits: .specpulse/specs/001-feature/spec-001.md (expand)
    ↓
Complete specification ready
```

**Why CLI First?**
- **Metadata Handling**: CLI manages timestamps, IDs, status automatically
- **Structure Validation**: CLI validates before creating files
- **Context Updates**: CLI updates context.md consistently
- **Error Handling**: CLI provides recovery and validation
- **File Operations**: Fallback for flexibility when CLI doesn't cover operation

---

## v2.0.0 → v2.1.2

### 📋 Overview

SpecPulse v2.1.0 eliminated bash/PowerShell scripts and moved all functionality to pure Python CLI. This was a **backward compatible** upgrade with optional cleanup.

### 🔧 Key Changes in v2.1.0

**What Changed:**
- ✅ Scripts removed (`specpulse/resources/scripts/` deleted)
- ✅ All functionality moved to CLI commands
- ✅ No `scripts/` folder in new projects
- ✅ Slash commands updated to use CLI
- ✅ ~50KB smaller projects
- ✅ ~3x faster execution

**What Stayed the Same:**
- ✅ All existing specs, plans, tasks remain compatible
- ✅ Templates unchanged
- ✅ Memory system unchanged
- ✅ AI integration unchanged
- ✅ Slash commands work the same (just faster)

---

### 🚀 Migration Steps

#### Step 1: Upgrade SpecPulse

```bash
# Upgrade to latest version
pip install --upgrade specpulse

# Verify version
specpulse --version
# Should show: 2.1.0
```

#### Step 2: Clean Up Old Scripts (Optional)

For **existing v2.0.0 projects**, the `scripts/` folder is now unnecessary:

```bash
# Navigate to your project
cd my-project

# Remove old scripts (safe to delete)
rm -rf scripts/

# Verify slash commands still work
# (they now use CLI instead of scripts)
```

#### Step 3: Test Workflow

```bash
# Test feature creation
specpulse feature init test-migration

# Test spec creation
specpulse spec create "test spec for migration"

# Verify file was created
ls specs/001-test-migration/spec-001.md
```

**That's it!** No data migration needed.

---

### 📊 Command Mapping

Old scripts → New CLI commands:

| Old (v2.0.0) | New (v2.1.0) | Notes |
|--------------|--------------|-------|
| `bash scripts/sp-pulse-init.sh` | `specpulse feature init` | Native CLI |
| `bash scripts/sp-pulse-spec.sh` | `specpulse spec create` | Native CLI |
| `bash scripts/sp-pulse-plan.sh` | `specpulse plan create` | Native CLI |
| `bash scripts/sp-pulse-task.sh` | `specpulse task breakdown` | Native CLI |
| `bash scripts/sp-pulse-execute.sh` | `specpulse execute start/done` | Native CLI |

**Slash commands automatically updated** - no changes needed!

---

### 🆕 New CLI Commands in v2.1.0

```bash
# Feature management
specpulse feature init <name>        # Initialize feature
specpulse feature continue <name>    # Switch to feature

# Spec management
specpulse spec create <description>  # Create spec
specpulse spec update <id> <desc>    # Update spec
specpulse spec validate              # Validate spec

# Plan management
specpulse plan create <description>  # Create plan
specpulse plan update <id> <desc>    # Update plan

# Task management
specpulse task create <description>  # Create task
specpulse task breakdown <plan-id>   # Generate tasks
specpulse task update <id> <desc>    # Update task

# Execution tracking
specpulse execute start <task-id>    # Start task
specpulse execute done <task-id>     # Complete task
```

---

### 🔄 Project Structure Changes

**Before (v2.0.0):**
```
my-project/
├── scripts/                # ❌ No longer needed
│   ├── sp-pulse-init.sh
│   ├── sp-pulse-spec.sh
│   └── ...
├── specs/
├── plans/
└── tasks/
```

**After (v2.1.0):**
```
my-project/
├── specs/                 # Same
├── plans/                 # Same
└── tasks/                 # Same
# No scripts/ folder! ✅
```

---

### ⚠️ Breaking Changes

**Only one breaking change:**
- Scripts removed from `specpulse/resources/scripts/`
- Projects no longer get `scripts/` folder on init

**Everything else remains compatible:**
- ✅ Existing specs, plans, tasks work unchanged
- ✅ Templates remain the same
- ✅ Memory files unchanged
- ✅ AI integration unchanged
- ✅ Slash commands work (use CLI internally)

---

### 🐛 Troubleshooting

#### Issue: "Command not found: specpulse"

**Solution:**
```bash
# Reinstall SpecPulse
pip install --upgrade --force-reinstall specpulse

# Check installation
which specpulse  # Unix/Mac
where specpulse  # Windows
```

#### Issue: "Scripts folder still exists"

**Solution:**
```bash
# Safe to delete in existing projects
rm -rf scripts/

# New projects won't create it
specpulse init test-project --ai claude
ls test-project/  # No scripts/ folder
```

#### Issue: "Slash commands not working"

**Solution:**
Slash commands should work automatically. If not:

1. Check SpecPulse version: `specpulse --version`
2. Re-initialize project: `specpulse init --here`
3. Verify command files exist: `ls .claude/commands/`

---

### 📝 Testing Migration

```bash
# 1. Create test project
mkdir test-v2.1.0
cd test-v2.1.0
specpulse init --here --ai claude

# 2. Verify no scripts folder
ls scripts/  # Should fail or be empty

# 3. Test feature workflow
specpulse feature init test-feature

# 4. Test spec creation
specpulse spec create "test specification"

# 5. Verify file created
cat specs/001-test-feature/spec-001.md

# 6. Success! ✅
```

---

### 🔄 Rollback Plan (If Needed)

If you need to rollback to v2.0.0:

```bash
# 1. Uninstall v2.1.0
pip uninstall specpulse

# 2. Install v2.0.0
pip install specpulse==2.0.0

# 3. Your data is safe
# All specs, plans, tasks remain intact
```

**Note**: Rolling back means scripts will be expected but not present. You'd need to copy scripts from a fresh v2.0.0 init.

---

## v1.x → v2.0.0

See [CHANGELOG.md](../CHANGELOG.md) for v2.0.0 migration details.

**Summary:**
- AI integration added
- 3-tier template system
- Enhanced validation
- Memory management
- All v1.x features remain functional

---

## 📞 Migration Support

**Having issues?**

1. **Check documentation**: [docs/](.)
2. **Run diagnostics**: `specpulse doctor`
3. **View changelog**: [CHANGELOG.md](../CHANGELOG.md)
4. **Get help**: `specpulse --help`
5. **Report issues**: [GitHub Issues](https://github.com/specpulse/specpulse/issues)

---

## ✅ Post-Migration Checklist

After upgrading to v2.4.1:

- [ ] `specpulse --version` shows 2.4.1
- [ ] `specpulse feature init` works
- [ ] `specpulse spec create` works
- [ ] `specpulse plan create` works
- [ ] `specpulse task breakdown` works
- [ ] `specpulse validate all --fix` works
- [ ] `specpulse doctor` shows no errors
- [ ] Slash commands work in Claude Code/Gemini
- [ ] Existing specs/plans/tasks still accessible
- [ ] CLI-first workflow understood by team

---

**🎉 Migration Complete!**

Enjoy faster, cleaner, CLI-first SpecPulse v2.4.1!

```bash
specpulse feature init my-new-feature
```
