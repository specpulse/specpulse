# SpecPulse v2.7.1 Troubleshooting Guide

## 📋 Table of Contents

- [Common Issues](#common-issues)
- [Installation Issues](#installation-issues)
- [AI Integration Issues](#ai-integration-issues)
- [Template Issues](#template-issues)
- [Memory Issues](#memory-issues)
- [Performance Issues](#performance-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Getting Help](#getting-help)

---

## 🚨 Common Issues

### OpenCode Command Directory Issue (v2.7.1)

**Problem**: OpenCode custom commands are in the wrong directory

**Symptoms**:
- Commands in `.opencode/commands/` (plural)
- Should be in `.opencode/command/` (singular)

**Diagnosis**:
```bash
# Check directory structure
ls -la .opencode/

# Wrong:
# .opencode/commands/

# Correct:
# .opencode/command/
```

**Solution**:
```bash
# Fix directory structure
if [ -d ".opencode/commands" ] && [ ! -d ".opencode/command" ]; then
    mv .opencode/commands .opencode/command
    echo "Fixed OpenCode directory structure"
fi

# Re-initialize OpenCode commands
specpulse init . --ai opencode
```

### Multi-Platform AI Integration Issues

**Problem**: AI commands not working across platforms

**Symptoms**:
- Slash commands not recognized
- Missing command files
- Platform-specific errors

**Diagnosis**:
```bash
# Check which AI platforms are initialized
ls -la .claude/ .gemini/ .gpt/ .windsurf/ .cursor/ .github/ .opencode/ .crush/ .qwen/

# Check command files exist
ls .claude/commands/ 2>/dev/null || echo "Claude not initialized"
ls .gemini/commands/ 2>/dev/null || echo "Gemini not initialized"
ls .opencode/command/ 2>/dev/null || echo "OpenCode not initialized"
```

**Solution**:
```bash
# Re-initialize with specific platforms
specpulse init . --ai claude,gemini

# Or initialize all platforms
specpulse init . --ai all

# Or interactive selection
specpulse init . --ai interactive
```

### Quick Diagnosis

```bash
# System health check
specpulse doctor

# Show current status
specpulse feature list

# Validate core functionality
specpulse validate all

# Check CLI commands
specpulse feature --help
specpulse spec --help
```

---

## 🔧 Installation Issues

### SpecPulse Not Found

**Issue:**
```bash
specpulse --version
# Command not found: 'specpulse'
# Python error: No module named 'specpulse'
```

**Solutions:**

1. **Verify Installation:**
   ```bash
   pip list | grep specpulse
   ```

2. **Reinstall SpecPulse:**
   ```bash
   pip uninstall specpulse
   pip install specpulse==2.4.1
   ```

3. **Check Python Environment:**
   ```bash
   python --version
   # Should be 3.11+ for v2.7.1
   ```

4. **Virtual Environment:**
   ```bash
   # Activate virtual environment
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

### Version Conflicts

**Issue:**
```bash
pip install specpulse==2.4.1
# ERROR: SpecPulse 2.4.1 requires Python 3.11+
```

**Solutions:**

1. **Upgrade Python:**
   ```bash
   # Using pyenv
   pyenv install 3.12.0
   pyenv global 3.12.0

   # Using conda
   conda install python=3.12
   conda activate myenv
   ```

2. **Use System Python 3.12+ (if available):**
   ```bash
   python3.12 -m pip install specpulse==2.4.1
   ```

### Permission Issues

**Windows Error:**
```cmd
'pip' is not recognized
# Access denied
```

**Solutions:**

1. **Run as Administrator:**
   ```cmd
   # Right-click Command Prompt → Run as administrator
   ```

2. **Install for User Only:**
   ```bash
   pip install --user specpulse==2.0.0
   ```

3. **Add to PATH:**
   ```bash
   echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
   source ~/.bashrc
   ```

**Linux/macOS Error:**
```bash
Permission denied: /usr/local/lib/python3.11/site-packages/
```

**Solutions:**
```bash
# Install for user only
pip install --user specpulse==2.0.0

# Use virtual environment
python -m venv specpulse-env
source specpulse-env/bin/activate
pip install specpulse==2.4.1
```

### Network Issues

**Issue:**
```bash
pip install specpulse==2.4.1
# ERROR: Could not find a version that satisfies the requirement
```

**Solutions:**

1. **Use PyPI Mirror:**
   ```bash
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ specpulse==2.0.0
   ```

2. **Use Alternative Index:**
   ```bash
   pip install --index-url https://pypi.org/simple/ specpulse==2.0.0
   ```

3. **Download and Install Locally:**
   ```bash
   wget https://files.pythonhosted.org/packages/source/s/specpulse/SpecPulse-2.0.0.tar.gz
   tar -xzf SpecPulse-2.0.0.tar.gz
   cd SpecPulse-2.0.0
   python setup.py install
   ```

---

## 🤖 AI Integration Issues

### Deprecated AI Commands

**Issue:**
```bash
specpulse ai context
# Error: Unknown command 'ai'
```

**Explanation**: AI commands have been deprecated in v2.7.1 in favor of CLI-first architecture.

**Solutions:**

1. **Use Direct CLI Commands:**
   ```bash
   # Instead of: specpulse ai context
   specpulse feature list
   specpulse feature status 001-feature

   # Instead of: specpulse ai suggest
   specpulse feature init my-feature
   specpulse spec create "My feature description"
   ```

2. **Use AI Assistant Slash Commands:**
   ```bash
   # In Claude Code or Gemini CLI:
   /sp-pulse my-feature
   /sp-spec create "My feature description"
   /sp-plan generate
   /sp-task breakdown
   ```

3. **Verify Version:**
   ```bash
   specpulse --version
   # Should be 2.4.1
   ```

### Context Detection Problems

**Issue:**
```bash
specpulse feature continue my-feature
# Error: Feature not found
```

**Solutions:**

1. **Check Git Branch:**
   ```bash
   git status
   git branch --show-current
   # Should be on a feature branch like 001-my-feature
   ```

2. **List Available Features:**
   ```bash
   specpulse feature list
   # Shows all available features
   ```

3. **Initialize Git if Needed:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git checkout -b 001-my-feature
   ```

4. **Check Project Structure:**
   ```bash
   ls .specpulse/specs/
   ls .specpulse/plans/
   ls .specpulse/tasks/
   ```

5. **Manual Feature Creation:**
   ```bash
   specpulse feature init my-feature
   ```

### AI Assistant Commands Not Working

**Issue:**
```bash
# In Claude Code or Gemini CLI:
/sp-spec create "My feature"
# Error: Command not found or file not found
```

**Solutions:**

1. **Initialize Project with AI Support:**
   ```bash
   specpulse init my-project --ai claude
   # or
   specpulse init my-project --ai gemini
   ```

2. **Check Command Files Exist:**
   ```bash
   ls .claude/commands/
   ls .gemini/commands/
   # Should see sp-*.md or sp-*.toml files
   ```

3. **Reinitialize AI Commands:**
   ```bash
   specpulse init --here --ai claude
   ```

4. **Check Project Structure:**
   ```bash
   ls .specpulse/templates/
   # Templates must exist for slash commands to work
   ```

### AI Assistant Integration Issues

**Issue:**
```bash
# Claude Code or Gemini CLI not recognizing SpecPulse context
```

**Solutions:**

1. **Check AI Assistant Setup:**
   ```bash
   # Verify you're in a SpecPulse project
   ls .specpulse/
   ls .claude/  # For Claude
   ls .gemini/  # For Gemini
   ```

2. **Reinitialize AI Integration:**
   ```bash
   specpulse init --here --ai claude
   # or
   specpulse init --here --ai gemini
   ```

3. **Check Template Access:**
   ```bash
   ls .specpulse/templates/
   # AI assistants need access to templates
   ```

4. **Verify Memory System:**
   ```bash
   ls .specpulse/memory/
   # Context files should exist
   ```

### Project State Corruption

**Issue:**
```bash
specpulse doctor
# Error: Failed to load project state
```

**Solutions:**

1. **Check Project Structure:**
   ```bash
   ls -la .specpulse/
   # Should have: specs/, plans/, tasks/, memory/, templates/
   ```

2. **Reset Memory System:**
   ```bash
   rm .specpulse/memory/context.md
   specpulse feature init test-feature
   specpulse feature delete test-feature --force
   ```

3. **Check Permissions:**
   ```bash
   ls -la .specpulse/
   chmod 755 .specpulse/
   ```

4. **Verify Template Directory:**
   ```bash
   mkdir -p .specpulse/templates/
   chmod 755 .specpulse/templates/
   ```

---

## 📋 Template Issues

### Template Loading Errors

**Issue:**
```bash
specpulse template list
# Error: Not in a SpecPulse project directory
```

**Solutions:**

1. **Verify Project Structure:**
   ```bash
   ls -la | grep -E "(specs|plans|tasks|memory|templates)"
   ```

2. **Reinitialize Templates:**
   ```bash
   rm -rf templates/
   specpulse update
   ```

3. **Check Template Registry:**
   ```bash
   cat .specpulse/template_registry.json
   ```

### Template Validation Failures

**Issue:**
```bash
specpulse template validate
# Error: Template validation failed
```

**Solutions:**

1. **Validate Specific Template:**
   ```bash
   specpulse template validate spec-tier2-standard
   ```

2. **Fix Validation Errors:**
   ```bash
   specpulse template validate --fix
   ```

3. **Restore from Backup:**
   ```bash
   specpulse template restore backup_20251007_120000
   ```

### Template Inheritance Issues

**Issue:**
```bash
specpulse expand 001-feature --to-tier complete
# Error: Template inheritance failed
```

**Solutions:**

1. **Check Template Registry:**
   ```bash
   cat .specpulse/template_registry.json
   # Verify extends field is correct
   ```

2. **Validate Template Chain:**
   ```bash
   specpulse template validate spec-tier1-minimal
   specpulse template validate spec-tier2-standard
   specpulse template validate spec-tier3-complete
   ```

3. **Check Template Files:**
   ```bash
   ls templates/
   # Ensure all template files exist
   ```

---

## 💾 Memory Issues

### Memory Search Not Working

**Issue:**
```bash
specpulse memory search "authentication"
# No results found
```

**Solutions:**

1. **Check Memory Files:**
   ```bash
   ls memory/
   # Check if memory files exist
   ```

2. **Add Memory Content:**
   ```bash
   specpulse memory add-decision "Database Choice" --rationale "PostgreSQL chosen"
   specpulse memory add-pattern "Repository Pattern" --example "class UserRepository:"
   ```

3. **Use Structured Tags:**
   ```bash
   specpulse memory query --tag decision
   specpulse memory query --tag pattern
   ```

### Memory Organization Issues

**Issue:**
```bash
specpulse memory summary
# Memory system appears disorganized
```

**Solutions:**

1. **Migrate Memory Format:**
   ```bash
   specpulse memory migrate
   ```

2. **Clean Up Old Entries:**
   ```bash
   specpulse memory cleanup --days 30
   ```

3. **Reorganize Memory:**
   ```bash
   # Edit memory files manually using proper structure
   # Follow the tagged memory system format
   ```

### Memory Performance Issues

**Issue:**
```bash
specpulse memory summary
# Memory system is slow
```

**Solutions:**

1. **Reduce History:**
   ```bash
   specpulse memory cleanup --days 7
   ```

2. **Optimize Cache:**
   ```bash
   export SPECPULSE_AI_CACHE_DIR="/tmp/specpulse-cache"
   rm -rf /tmp/specpulse-cache
   mkdir -p /tmp/specpulse-cache
   ```

3. **Monitor Usage:**
   ```bash
   specpulse memory summary
   specpulse ai summary
   ```

---

## ⚡ Performance Issues

### Slow Command Execution

**Issue:**
```bash
specpulse feature list
# Takes >10 seconds to complete
```

**Solutions:**

1. **Clean Old Data:**
   ```bash
   find .specpulse/ -name "*.md" -mtime +30 -delete
   ```

2. **Optimize File System:**
   ```bash
   # Check for large files
   du -sh .specpulse/
   find .specpulse/ -size +10M -delete
   ```

3. **Use Verbose Mode for Debugging:**
   ```bash
   export SPECPULSE_VERBOSE=1
   specpulse feature list
   ```

4. **Check Git Performance:**
   ```bash
   git gc --prune=now
   git status
   ```

### High Memory Usage

**Issue:**
```bash
# Memory usage growing over time
# Performance degrades
```

**Solutions:**

1. **Regular Cleanup:**
   ```bash
   find .specpulse/ -name "*.md" -mtime +7 -delete
   ```

2. **Check Directory Sizes:**
   ```bash
   du -sh .specpulse/*
   # Identify large directories
   ```

3. **Monitor Usage:**
   ```bash
   specpulse doctor
   du -sh .specpulse/
   ```

### CLI Commands Slow

**Issue:**
```bash
specpulse validate all
# Validation takes a long time to complete
```

**Solutions:**

1. **Use Specific Validation:**
   ```bash
   specpulse validate spec
   specpulse validate plan
   # Instead of validating everything at once
   ```

2. **Enable Auto-Fix:**
   ```bash
   specpulse validate all --fix
   # Auto-fix can speed up the process
   ```

3. **Check for Large Files:**
   ```bash
   find .specpulse/ -size +1M -ls
   # Large files can slow down validation
   ```

---

## 🖥 Platform-Specific Issues

### Windows Issues

#### Unicode Encoding Problems

**Issue:**
```cmd
specpulse ai context
# Error: Character encoding issues in console output
```

**Solutions:**
- ✅ **Already Fixed**: v2.7.1 includes Unicode fixes
- Use PowerShell instead of Command Prompt
- Set console encoding: `chcp 65001`

#### Path Length Limitations

**Issue:**
```cmd
# File path too long errors during installation
```

**Solutions:**
- Use shorter project names
- Install to user directory: `pip install --user`
- Use virtual environments

#### Permission Issues

**Issue:**
```cmd
Access denied errors during installation
```

**Solutions:**
- Run as Administrator
- Install for user only: `pip install --user`
- Set appropriate directory permissions

### Linux Issues

#### Package Manager Conflicts

**Issue:**
```bash
# Conflicts between system Python and user-installed Python
```

**Solutions:**
- Use virtual environments: `python -m venv`
- Use conda environments: `conda create -n myenv python=3.12`
- Install for user only: `pip install --user`

#### Development Dependencies

**Issue:**
```bash
# Missing development dependencies like git, curl, etc.
```

**Solutions:**
- Install development tools:
  ```bash
  sudo apt install git curl build-essential
  sudo dnf install python3-pip python3-dev
  ```

- Use conda with development environment:
  ```bash
  conda install -c conda-forge python=3.12
  conda activate myenv
  ```

### macOS Issues

#### Xcode Command Line Tools

**Issue:**
```bash
# Xcode command line tools not found
```

**Solutions:**
- Install Xcode Command Line Tools:
  ```bash
  xcode-select --install
  ```

- Install via Homebrew:
  ```bash
  brew install git
  brew install python@3
  ```

#### Python Installation

**Issue:**
```bash
# Multiple Python versions installed
# Ambiguous which to use
```

**Solutions:**
- Use Homebrew Python: `brew install python@3.12`
- Use pyenv for version management
- Use virtual environments consistently

---

## 🔍 Getting Help

### Self-Help System

```bash
# Get general help
specpulse --help

# Get help on specific commands
specpulse feature --help
specpulse spec --help
specpulse plan --help
specpulse task --help
specpulse validate --help

# System diagnostics
specpulse doctor
```

### Community Support

#### Online Resources

- **GitHub Issues**: [github.com/specpulse/specpulse/issues](https://github.com/specpulse/specpulse/issues)
- **GitHub Discussions**: [github.com/specpulse/specpulse/discussions](https://github.com/specpulse/specpulse/discussions)
- **GitHub Wiki**: [github.com/specpulse/specpulse/wiki](https://github.com/specpulse/specpulse/wiki)

#### Getting Help

```bash
# Comprehensive support
specpulse doctor
# Shows system status and recommendations

# Command-specific help
specpulse feature --help
specpulse spec --help
specpulse validate --help
```

### Bug Reporting

When reporting issues, include:

1. **System Information:**
   ```bash
   python --version
   pip show specpulse
   git --version
   uname -a
   ```

2. **Error Messages:**
   Full error output and stack traces

3. **Reproduction Steps:**
   Clear steps to reproduce the issue

4. **Expected vs Actual:**
   What you expected vs. what actually happened

5. **Environment Details:**
   Operating system, Python version, SpecPulse version

### Documentation Resources

- [Installation Guide](INSTALLATION.md)
- [AI Integration Guide](AI_INTEGRATION.md)
- [Migration Guide](MIGRATION.md)
- [API Reference](docs/API_REFERENCE.md)

---

## 🎯 Recovery Checklist

### Emergency Recovery

1. **Quick Diagnosis:**
   ```bash
   specpulse doctor
   specpulse ai summary
   ```

2. **Reset AI State:**
   ```bash
   rm .specpulse/ai_state.json
   specpulse ai context
   ```

3. **Configuration Reset:**
   ```bash
   rm .specpulse/config.yaml.backup
   cp .specpulse/config.yaml.backup .specpulse/config.yaml
   ```

4. **Package Reinstall:**
   ```bash
   pip uninstall specpulse
   pip install specpulse==2.4.1
   ```

### Partial Rollback

1. **Disable AI Features:**
   ```yaml
   # Edit .specpulse/config.yaml
   ai:
     enabled: false
   suggestions:
       enabled: false
     multi_llm:
       enabled: false
   ```

2. **Reset AI State:**
   ```bash
   rm .specpulse/ai_state.json
   ```

3. **Keep Core Functionality:**
   ```bash
   specpulse validate all
   specpulse template list
   specpulse memory summary
   ```

### Complete Rollback

1. **Downgrade Package:**
   ```bash
   pip install specpulse==1.9.1
   ```

2. **Restore Configuration:**
   ```bash
   rm .specpulse/ai_state.json
   # Restore v1.x config format
   ```

3. **Continue with v1.x Workflow:**
   ```bash
   specpulse validate all
   specpulse template list
   # Continue using v1.x features
   ```

---

**🎉 With proper preparation and troubleshooting, your migration to SpecPulse v2.7.1 should be smooth and successful!**