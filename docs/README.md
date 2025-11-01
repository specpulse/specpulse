# SpecPulse Documentation

Welcome to the SpecPulse documentation! This directory contains comprehensive guides for using SpecPulse v2.4.1.

---

## 📚 Documentation Index

### Getting Started

- **[Installation Guide](INSTALLATION.md)** - System requirements, installation, and initial setup
- **[Quick Start](../README.md#quick-start)** - Get up and running in 5 minutes

### Core Concepts

- **[AI Integration Guide](AI_INTEGRATION.md)** - How SpecPulse works with Claude Code and Gemini CLI
- **[Migration Guide](MIGRATION.md)** - Upgrading from previous versions
- **[Migration Guide v2.2.0](MIGRATION_v2.2.0.md)** - Specific migration for v2.2.0

### Troubleshooting

- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and solutions

---

## 🎯 Quick Navigation

### For New Users

1. Start with [Installation Guide](INSTALLATION.md)
2. Follow [Quick Start](../README.md#quick-start)
3. Learn about [AI Integration](AI_INTEGRATION.md)

### For Existing Users

1. Check [Migration Guide](MIGRATION.md) for upgrade path
2. Review [Troubleshooting Guide](TROUBLESHOOTING.md) if needed

### For Developers

1. See [../README.md](../README.md#contributing) for contribution guidelines
2. Check [../CHANGELOG.md](../CHANGELOG.md) for version history

---

## 📖 Documentation Overview

### Installation Guide
**File**: `INSTALLATION.md`

Covers:
- System requirements
- Installation methods
- Virtual environment setup
- Platform-specific instructions
- Verification steps

### AI Integration Guide
**File**: `AI_INTEGRATION.md`

Covers:
- How SpecPulse integrates with AI assistants
- Claude Code setup and usage
- Gemini CLI setup and usage
- Custom slash commands
- Privacy and security
- Workflow examples

### Migration Guide
**File**: `MIGRATION.md`

Covers:
- v2.1.2 → v2.4.1 migration (CLI-First Architecture)
- v2.0.0 → v2.1.2 migration (script elimination)
- Breaking changes
- Command mapping
- Rollback procedures
- Testing migration

### Troubleshooting Guide
**File**: `TROUBLESHOOTING.md`

Covers:
- Common errors and solutions
- Platform-specific issues
- CLI command problems
- AI integration issues
- Performance optimization
- Debug mode

---

## 🚀 What's New in v2.4.1

### Major Changes

✅ **CLI-First Architecture (v2.1.2+)**
- AI assistants must try CLI commands before file operations
- Deprecated AI commands (`specpulse ai *`)
- Enhanced performance and reliability

✅ **Enhanced Validation System (v2.2.0)**
- Auto-fix capabilities
- Parallel processing for large projects
- Comprehensive security improvements

✅ **Performance Improvements**
- Thread-safe feature IDs
- 3-5x faster validation
- TTL template caching
- Better memory management

✅ **Architecture Improvements**
- Service-oriented design
- Dependency injection
- Clean code principles
- Better testability

### Historical Changes (v2.1.0)

✅ **Scripts Eliminated**
- No more bash/PowerShell scripts
- Pure Python CLI
- Cross-platform by default

✅ **New CLI Commands**
- `specpulse feature init/continue`
- `specpulse spec create/update/validate`
- `specpulse plan create/update`
- `specpulse task create/breakdown/update`
- `specpulse execute start/done`

### Migration Summary

```bash
# Upgrade to latest
pip install --upgrade specpulse

# For v2.0.0 → v2.1.0: Remove old scripts (optional)
rm -rf scripts/

# For v2.1.2 → v2.4.1: No changes needed
# CLI-first workflow is automatic

# Done! Everything works (much faster and more reliable)
```

See [Migration Guide](MIGRATION.md) for details.

---

## 💡 Key Concepts

### Specification-Driven Development (SDD)

SpecPulse enforces a specification-first approach:

1. **Specification** → What needs to be built
2. **Plan** → How to build it
3. **Tasks** → Step-by-step implementation
4. **Execution** → Tracked progress

### AI-Enhanced Workflow

```
User → Claude Code/Gemini → SpecPulse CLI → LLM-Friendly Files
                ↓
           AI expands files with full details (CLI-first approach)
                ↓
        Complete specs, plans, tasks
```

**CLI-First Pattern (v2.1.2+)**:
```
User Request: /sp-spec OAuth2 login
    ↓
Step 1: Try CLI first
    Bash: specpulse spec create "OAuth2 login"
    ↓
Step 2: If CLI doesn't exist, use File Operations
    Claude reads template, writes file, expands content
```

### Privacy-First Design

- ✅ No external API calls
- ✅ All processing local
- ✅ Your code stays on your machine
- ✅ Works offline

---

## 🔧 Common Workflows

### Complete Feature Development

```bash
# 1. Initialize project
specpulse init my-project --ai claude

# 2. Start feature
specpulse feature init oauth-login

# 3. Create specification
specpulse spec create "OAuth2 login with JWT"

# 4. AI expands spec in Claude Code
# /sp-spec validate

# 5. Generate plan
specpulse plan create "implementation roadmap"

# 6. AI generates plan
# /sp-plan validate

# 7. Break down tasks
specpulse task breakdown 001

# 8. Execute tasks
specpulse execute start 001
# [implement task]
specpulse execute done 001
```

### Quick Prototyping

```bash
# Use minimal tier for quick specs
specpulse init prototype --ai claude
specpulse feature init mvp-feature
specpulse spec create "basic user login"
# AI creates minimal spec (2-3 min)
```

### Enterprise Development

```bash
# Use complete tier for full specs
specpulse init enterprise-app --ai claude
specpulse feature init payment-system
specpulse spec create "payment processing with Stripe"
# AI creates complete spec (30-45 min)
```

---

## 📞 Getting Help

### Documentation

- Read guides in this folder
- Check [README.md](../README.md)
- Review [CHANGELOG.md](../CHANGELOG.md)

### Command Line Help

```bash
specpulse --help                # General help
specpulse feature --help        # Feature commands
specpulse spec --help           # Spec commands
specpulse doctor                # System diagnostics
```

### Community Support

- [GitHub Issues](https://github.com/specpulse/specpulse/issues)
- [GitHub Discussions](https://github.com/specpulse/specpulse/discussions)

---

## 🎓 Learning Path

### Beginner

1. **Week 1**: Installation and basic commands
   - Install SpecPulse
   - Create first project
   - Initialize first feature
   - Create first spec

2. **Week 2**: AI integration
   - Setup Claude Code or Gemini
   - Use slash commands
   - Let AI expand specifications

3. **Week 3**: Full workflow
   - Complete feature cycle
   - Use plans and tasks
   - Track execution

### Intermediate

1. **Month 2**: Advanced features
   - Custom templates
   - Memory management
   - Checkpoint system
   - Validation customization

2. **Month 3**: Team workflows
   - Multi-developer projects
   - Git integration
   - CI/CD integration
   - Best practices

### Advanced

1. **Month 4+**: Mastery
   - Template customization
   - Workflow automation
   - Plugin development
   - Contributing to SpecPulse

---

## 📝 Documentation Standards

All SpecPulse documentation follows these standards:

- ✅ **Clear Examples**: Every concept includes code examples
- ✅ **Step-by-Step**: Guides are sequential and complete
- ✅ **Platform-Agnostic**: Works on Windows, macOS, Linux
- ✅ **Version-Specific**: Clearly marked for v2.4.1
- ✅ **Tested**: All examples are tested and verified

---

## 🔄 Documentation Updates

**Last Updated**: 2025-11-01
**Version**: v2.4.1
**Status**: Current and Complete

### Recent Changes

- ✅ Updated for v2.4.1 (CLI-First Architecture)
- ✅ Enhanced AI integration documentation
- ✅ New validation system coverage
- ✅ Performance improvements documentation
- ✅ Updated migration guides for all versions

---

## 📋 Quick Reference

### Essential Commands

```bash
# Project
specpulse init <name>                # Initialize project
specpulse doctor                     # Health check

# Features
specpulse feature init <name>        # New feature
specpulse feature continue <name>    # Switch feature

# Specifications
specpulse spec create <desc>         # Create spec
specpulse spec validate              # Validate spec

# Plans & Tasks
specpulse plan create <desc>         # Create plan
specpulse task breakdown <id>        # Generate tasks

# Execution
specpulse execute start <id>         # Start task
specpulse execute done <id>          # Complete task
```

### Essential Slash Commands

```bash
# In Claude Code or Gemini CLI:
/sp-pulse <feature-name>             # Initialize feature
/sp-spec create <description>        # Create spec
/sp-plan generate                    # Generate plan
/sp-task breakdown                   # Break into tasks
/sp-execute                          # Execute tasks
```

---

**Ready to dive deeper?** Pick a guide and start reading! 📖
