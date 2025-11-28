# SpecPulse v2.7.1 Migration Guide

## 📋 Table of Contents

- [Overview](#overview)
- [v2.7.0 → v2.7.1 Migration](#v270--v271-migration)
- [v2.6.x → v2.7.1 Migration](#v26x--v271-migration)
- [v2.5.x → v2.7.1 Migration](#v25x--v271-migration)
- [v2.4.x → v2.7.1 Migration](#v24x--v271-migration)
- [v2.2.x → v2.7.1 Migration](#v22x--v271-migration)
- [v2.1.x → v2.7.1 Migration](#v21x--v271-migration)
- [v2.0.x → v2.7.1 Migration](#v20x--v271-migration)
- [Breaking Changes](#breaking-changes)
- [Rollback Procedures](#rollback-procedures)
- [Testing Migration](#testing-migration)

---

## 🎯 Overview

This guide helps you migrate to SpecPulse v2.7.1 from any previous version. SpecPulse v2.7.1 focuses on fixing the OpenCode command directory issue and maintaining backward compatibility while introducing selective AI tool initialization.

### What's New in v2.7.1

- **Fixed**: OpenCode custom commands directory structure
- **Enhanced**: Selective AI tool initialization
- **Maintained**: Full backward compatibility
- **Improved**: Domain and website integration

---

## 🔄 v2.7.0 → v2.7.1 Migration

### Changes

- **OpenCode Directory Fix**: Commands now go to `.opencode/command/` instead of `.opencode/commands/`
- **No Breaking Changes**: Existing projects continue to work
- **Enhanced Validation**: Better directory structure enforcement

### Migration Steps

```bash
# 1. Upgrade SpecPulse
pip install --upgrade specpulse==2.7.1

# 2. Fix existing OpenCode directory (if exists)
if [ -d ".opencode/commands" ] && [ ! -d ".opencode/command" ]; then
    mv .opencode/commands .opencode/command
    echo "Fixed OpenCode directory structure"
fi

# 3. Verify installation
specpulse --version  # Should show v2.7.1
specpulse doctor     # Should pass all checks
```

### Verification

```bash
# Check directory structure
ls -la .opencode/
# Should show: command/ (not commands/)

# Test OpenCode commands
ls .opencode/command/
# Should show all OpenCode command files
```

---

## 🔄 v2.6.x → v2.7.1 Migration

### Major Changes

- **Selective AI Tool Initialization**: Choose which AI platforms to initialize
- **Enhanced Multi-Platform Support**: 8 AI platforms with consistent commands
- **OpenCode Directory Fix**: Correct directory structure
- **Domain Integration**: New specpulse.xyz domain

### Migration Steps

```bash
# 1. Backup current project
cp -r .specpulse .specpulse.backup

# 2. Upgrade SpecPulse
pip install --upgrade specpulse==2.7.1

# 3. Fix OpenCode directory (if needed)
if [ -d ".opencode/commands" ] && [ ! -d ".opencode/command" ]; then
    mv .opencode/commands .opencode/command
fi

# 4. (Optional) Re-initialize with selective AI tools
specpulse init . --ai interactive
```

### New Features Available

```bash
# Initialize new projects with selective AI tools
specpulse init new-project --ai claude,gemini
specpulse init new-project --ai all
specpulse init new-project --ai interactive

# Check available AI platforms
specpulse --help | grep -i ai
```

---

## 🔄 v2.5.x → v2.7.1 Migration

### Breaking Changes

- **CLI-First Architecture**: AI commands deprecated, use CLI commands
- **Template System**: Enhanced template management
- **Directory Structure**: Enforced .specpulse/ structure

### Migration Steps

```bash
# 1. Backup everything
cp -r .specpulse .specpulse.backup
cp -r .claude .claude.backup  # If exists
cp -r .gemini .gemini.backup  # If exists

# 2. Upgrade SpecPulse
pip install --upgrade specpulse==2.7.1

# 3. Fix OpenCode directory
if [ -d ".opencode/commands" ] && [ ! -d ".opencode/command" ]; then
    mv .opencode/commands .opencode/command
fi

# 4. Update project structure
specpulse doctor --fix

# 5. Re-initialize AI integration
specpulse init . --ai claude  # Or your preferred AI
```

### Command Changes

**Old Commands (Deprecated)**:
```bash
specpulse ai init          # Don't use
specpulse ai context        # Don't use
specpulse ai status         # Don't use
```

**New Commands (Use These)**:
```bash
specpulse feature init      # Use this
specpulse spec create       # Use this
specpulse plan create       # Use this
specpulse task breakdown    # Use this
```

---

## 🔄 v2.4.x → v2.7.1 Migration

### Major Changes

- **Validation System**: Enhanced validation with auto-fix
- **Performance**: 3-5x faster operations
- **Security**: Comprehensive security improvements
- **Multi-Platform AI**: Support for 8 AI platforms

### Migration Steps

```bash
# 1. Full backup
tar -czf specpulse-backup-$(date +%Y%m%d).tar.gz .specpulse .claude .gemini 2>/dev/null || true

# 2. Upgrade SpecPulse
pip install --upgrade specpulse==2.7.1

# 3. Fix directory structure
if [ -d ".opencode/commands" ] && [ ! -d ".opencode/command" ]; then
    mv .opencode/commands .opencode/command
fi

# 4. Validate and fix project
specpulse validate all --fix

# 5. Re-initialize if needed
specpulse init . --ai all
```

### Performance Verification

```bash
# Test new performance
time specpulse spec create "Test performance"
# Should be significantly faster than v2.4.x
```

---

## 🔄 v2.2.x → v2.7.1 Migration

### Major Changes

- **Template System**: Complete overhaul
- **Service Architecture**: Dependency injection
- **CLI Commands**: New command structure
- **Memory System**: Enhanced memory management

### Migration Steps

```bash
# 1. Critical backup
tar -czf v2.2-backup.tar.gz .specpulse .claude .gemini 2>/dev/null || true

# 2. Upgrade in stages
pip install --upgrade specpulse==2.7.1

# 3. Fix OpenCode directory
if [ -d ".opencode/commands" ] && [ ! -d ".opencode/command" ]; then
    mv .opencode/commands .opencode/command
fi

# 4. Migrate templates
specpulse init . --force --ai claude

# 5. Validate everything
specpulse doctor
specpulse validate all
```

### Template Migration

Old templates are automatically migrated, but you can customize:

```bash
# Check new templates
ls .specpulse/templates/
ls .claude/commands/
ls .gemini/commands/
```

---

## 🔄 v2.1.x → v2.7.1 Migration

### Breaking Changes

- **Scripts Eliminated**: No more bash/PowerShell scripts
- **Pure Python CLI**: All functionality in Python CLI
- **New Commands**: Complete command set replacement

### Migration Steps

```bash
# 1. Remove old scripts (if exist)
rm -rf scripts/ 2>/dev/null || true

# 2. Backup configuration
cp -r .specpulse .specpulse.v2.1.backup

# 3. Upgrade SpecPulse
pip install --upgrade specpulse==2.7.1

# 4. Fix OpenCode directory
if [ -d ".opencode/commands" ] && [ ! -d ".opencode/command" ]; then
    mv .opencode/commands .opencode/command
fi

# 5. Re-initialize project
specpulse init . --ai interactive
```

### Script to CLI Mapping

| Old Script | New CLI Command |
|------------|-----------------|
| `scripts/feature.sh` | `specpulse feature init` |
| `scripts/spec.sh` | `specpulse spec create` |
| `scripts/plan.sh` | `specpulse plan create` |
| `scripts/task.sh` | `specpulse task breakdown` |

---

## 🔄 v2.0.x → v2.7.1 Migration

### Major Overhaul

This is a major version upgrade requiring careful migration:

### Migration Steps

```bash
# 1. Complete backup
tar -czf v2.0-complete-backup.tar.gz .specpulse scripts/ .claude .gemini 2>/dev/null || true

# 2. Clean upgrade
pip uninstall specpulse
pip install specpulse==2.7.1

# 3. Remove old artifacts
rm -rf scripts/ .claude/ .gemini/ .specpulse/ 2>/dev/null || true

# 4. Fresh initialization
specpulse init new-project --ai all

# 5. Migrate custom content manually
# Copy your old specs/plans/tasks to new structure
```

### Manual Content Migration

```bash
# Copy old content to new structure
# Old: specs/SPEC-001.md
# New: .specpulse/specs/001-feature-name/spec-001.md

# Example migration
mkdir -p .specpulse/specs/001-migrated-feature
cp old-specs/SPEC-001.md .specpulse/specs/001-migrated-feature/spec-001.md
```

---

## ⚠️ Breaking Changes

### v2.7.1 Breaking Changes

✅ **None** - v2.7.1 is fully backward compatible

### Historical Breaking Changes

**v2.7.0**:
- Selective AI tool initialization (opt-in)
- Domain changes (specpulse.xyz)

**v2.6.9**:
- Multi-platform AI support
- New directory structures for AI platforms

**v2.5.x**:
- CLI-first architecture
- Deprecated AI commands

**v2.4.x**:
- Enhanced validation system
- Performance improvements

**v2.2.x**:
- Template system overhaul
- Service architecture

**v2.1.x**:
- Script elimination
- Pure Python CLI

**v2.0.x**:
- Complete architecture overhaul

---

## 🔄 Rollback Procedures

### Rollback to Previous Version

```bash
# 1. Uninstall current version
pip uninstall specpulse

# 2. Install previous version
pip install specpulse==2.7.0

# 3. Restore from backup (if needed)
rm -rf .specpulse
tar -xzf specpulse-backup.tar.gz
```

### Rollback Project Changes

```bash
# Restore .specpulse from backup
rm -rf .specpulse
cp -r .specpulse.backup .specpulse

# Fix OpenCode directory for rollback
if [ -d ".opencode/command" ] && [ ! -d ".opencode/commands" ]; then
    mv .opencode/command .opencode/commands
fi
```

---

## 🧪 Testing Migration

### Pre-Migration Testing

```bash
# 1. Current system health
specpulse doctor
specpulse validate all

# 2. Backup critical data
tar -czf pre-migration-backup.tar.gz .specpulse .claude .gemini .opencode 2>/dev/null || true

# 3. Document current state
specpulse status > current-status.txt
```

### Post-Migration Testing

```bash
# 1. Verify installation
specpulse --version  # Should show v2.7.1
specpulse doctor     # Should pass all checks

# 2. Test core functionality
specpulse feature init test-migration
specpulse spec create "Migration test specification"
specpulse plan create "Migration test plan"
specpulse task breakdown 001

# 3. Test AI integration
# Check your AI platform commands work:
# Claude: /sp-status
# Gemini: /sp-status
# etc.

# 4. Verify directory structure
ls -la .specpulse/
ls -la .claude/commands/ 2>/dev/null || echo "Claude not initialized"
ls -la .gemini/commands/ 2>/dev/null || echo "Gemini not initialized"
ls -la .opencode/command/ 2>/dev/null || echo "OpenCode not initialized"

# 5. Validate project
specpulse validate all
```

### Migration Success Checklist

- [ ] `specpulse --version` shows v2.7.1
- [ ] `specpulse doctor` passes all checks
- [ ] Core CLI commands work (`feature`, `spec`, `plan`, `task`)
- [ ] AI platform commands work (your chosen platforms)
- [ ] Directory structure is correct
- [ ] OpenCode uses `.opencode/command/` (not `.opencode/commands/`)
- [ ] All existing content is accessible
- [ ] No data loss occurred

---

## 🆘 Troubleshooting Migration

### Common Issues

#### OpenCode Directory Issue

**Problem**: Commands in wrong directory
```bash
# Wrong
.opencode/commands/

# Correct
.opencode/command/
```

**Solution**:
```bash
if [ -d ".opencode/commands" ] && [ ! -d ".opencode/command" ]; then
    mv .opencode/commands .opencode/command
fi
```

#### CLI Commands Not Found

**Problem**: `specpulse: command not found`

**Solution**:
```bash
# Reinstall with proper PATH
pip install --upgrade --force-reinstall specpulse==2.7.1
python -m specpulse --version  # Test direct module call
```

#### AI Commands Not Working

**Problem**: Slash commands not recognized

**Solution**:
```bash
# Re-initialize AI integration
specpulse init . --ai your-platform

# Check command files exist
ls .claude/commands/
ls .gemini/commands/
ls .opencode/command/
```

#### Validation Failures

**Problem**: `specpulse validate all` shows errors

**Solution**:
```bash
# Auto-fix validation issues
specpulse validate all --fix

# Manual fix for specific issues
specpulse doctor --verbose
```

---

## 📞 Getting Help

### Migration Support

- **Documentation**: [Installation Guide](INSTALLATION.md)
- **Troubleshooting**: [Troubleshooting Guide](TROUBLESHOOTING.md)
- **AI Integration**: [AI Integration Guide](AI_INTEGRATION.md)
- **Community**: [GitHub Discussions](https://github.com/specpulse/specpulse/discussions)
- **Issues**: [GitHub Issues](https://github.com/specpulse/specpulse/issues)

### Quick Help Commands

```bash
# General help
specpulse --help

# Specific command help
specpulse feature --help
specpulse spec --help
specpulse plan --help
specpulse task --help

# System diagnostics
specpulse doctor
specpulse validate all
```

---

**🎉 Congratulations! You've successfully migrated to SpecPulse v2.7.1!**

Enjoy the enhanced OpenCode directory structure, selective AI tool initialization, and continued backward compatibility.