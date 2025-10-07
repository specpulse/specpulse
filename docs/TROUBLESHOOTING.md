# SpecPulse v2.0.0 Troubleshooting Guide

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

### Quick Diagnosis

```bash
# System health check
specpulse doctor

# Show current status
specpulse ai summary

# Validate core functionality
specpulse validate all

# Check AI integration
specpulse ai context
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
   pip install specpulse==2.0.0
   ```

3. **Check Python Environment:**
   ```bash
   python --version
   # Should be 3.11+ for v2.0.0
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
pip install specpulse==2.0.0
# ERROR: SpecPulse 2.0.0 requires Python 3.11+
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
   python3.12 -m pip install specpulse==2.0.0
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
pip install specpulse==2.0.0
```

### Network Issues

**Issue:**
```bash
pip install specpulse==2.0.0
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

### AI Commands Not Found

**Issue:**
```bash
specpulse ai context
# Error: Unknown command 'ai'
```

**Solutions:**

1. **Verify Version:**
   ```bash
   specpulse --version
   # Should be 2.0.0
   ```

2. **Check Project Recognition:**
   ```bash
   cd your-project
   ls -la .specpulse/
   # Should see ai_state.json
   ```

3. **Force Context Refresh:**
   ```bash
   specpulse ai context --refresh
   ```

### Context Detection Problems

**Issue:**
```bash
specpulse ai context
# Shows "No current feature detected"
```

**Solutions:**

1. **Check Git Status:**
   ```bash
   git status
   git branch --show-current
   ```

2. **Initialize Git if Needed:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **Check Project Structure:**
   ```bash
   ls specs/ plans/ tasks/ memory/
   ```

4. **Manual Context Update:**
   ```bash
   specpulse context set current_feature "my-feature"
   ```

### AI Suggestions Not Working

**Issue:**
```bash
specpulse ai suggest
# Shows generic or irrelevant suggestions
```

**Solutions:**

1. **Check Context:**
   ```bash
   specpulse ai context
   specpulse memory summary
   ```

2. **Provide Specific Query:**
   ```bash
   specpulse ai suggest --query "my specific authentication problem"
   ```

3. **Update Project Context:**
   ```bash
   specpulse context set tech_stack.framework React
   specpulse context set current_feature "user-authentication"
   ```

### Multi-LLM Issues

**Issue:**
```bash
specpulse ai switch claude
# Error: Failed to switch to claude
```

**Solutions:**

1. **Check Available LLMs:**
   ```bash
   specpulse ai summary
   # Shows current active LLM
   ```

2. **Reset AI State:**
   ```bash
   rm .specpulse/ai_state.json
   specpulse ai context
   ```

3. **Check LLM Configuration:**
   ```bash
   cat .specpulse/config.yaml
   # Verify ai section exists and is correct
   ```

### AI State Corruption

**Issue:**
```bash
specpulse ai summary
# Error: Failed to load AI state
```

**Solutions:**

1. **Reset AI State:**
   ```bash
   rm .specpulse/ai_state.json
   specpulse ai context
   ```

2. **Check Permissions:**
   ```bash
   ls -la .specpulse/
   chmod 755 .specpulse/
   ```

3. **Verify Cache Directory:**
   ```bash
   mkdir -p .specpulse/ai_cache
   chmod 755 .specpulse/ai_cache/
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

### Slow Context Detection

**Issue:**
```bash
specpulse ai context
# Takes >10 seconds to complete
```

**Solutions:**

1. **Clean Old Data:**
   ```bash
   specpulse memory cleanup --days 30
   specpulse ai checkpoint cleanup --older-than-days 30
   ```

2. **Optimize Cache:**
   ```bash
   export SPECPULSE_AI_CACHE_DIR="/tmp/specpulse-cache"
   rm -rf /tmp/specpulse-cache
   mkdir -p /tmp/specpulse-cache
   ```

3. **Reduce Scope:**
   ```bash
   specpulse ai context --refresh
   specpulse ai suggest --query "next immediate steps"
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
   specpulse memory cleanup --days 7
   ```

2. **Adjust Retention Policy:**
   ```yaml
   # Edit .specpulse/config.yaml
   ai:
     cache_retention_days: 7
   ```

3. **Monitor Usage:**
   ```bash
   specpulse memory summary
   specpulse ai summary
   ```

### AI Response Slow

**Issue:**
```bash
specpulse ai suggest
# AI suggestions take a long time to generate
```

**Solutions:**

1. **Use Targeted Queries:**
   ```bash
   specpulse ai suggest --query "immediate next steps"
   ```

2. **Switch Faster LLM:**
   ```bash
   specpulse ai switch gemini
   # Gemini is faster for routine tasks
   ```

3. **Use Both for Complex Work:**
   ```bash
   specpulse ai switch both
   # Leverage both Claude and Gemini insights
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
- ✅ **Already Fixed**: v2.0.0 includes Unicode fixes
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
# Show available help topics
specpulse help --list

# Get help on specific topics
specpulse help ai_integration
specpulse help troubleshooting
specpulse help templates

# Get contextual help
specpulse ai suggest --query "help"
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

# Context-specific help
specpulse ai suggest --query "installation issues"
specpulse ai suggest --query "AI integration problems"
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
   pip install specpulse==2.0.0
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

**🎉 With proper preparation and troubleshooting, your migration to SpecPulse v2.0.0 should be smooth and successful!**