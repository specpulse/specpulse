# AI-SpecPulse CLI Integration Guide

This guide explains how AI assistants (Claude/Gemini) use the SpecPulse CLI tool and what happens when CLI commands fail.

## 🤖 AI-CLI Collaboration

### AI Role
- **Content Generation**: Specifications, plans, task details
- **Strategic Planning**: Architecture decisions, dependencies
- **Implementation**: Code writing, testing
- **Validation**: Quality control, verification

### CLI Role
- **Structure Management**: Directory creation, file organization
- **Metadata**: ID assignment, version tracking, status management
- **Validation**: Syntax checking, structural integrity
- **Cross-platform**: Windows/macOS/Linux compatibility

### Collaboration Pattern
```
1. AI: "Create user authentication spec" → CLI: specpulse spec create
2. CLI: Creates directory and files → AI: Fills and details content
3. AI: "Create plan for this spec" → CLI: specpulse plan create
4. CLI: Creates plan structure → AI: Develops plan details
5. AI: "Break down tasks" → CLI: specpulse task breakdown
6. CLI: Creates task files → AI: Enriches task content
7. AI: "Execute tasks" → CLI: specpulse execute status
8. CLI: Shows status → AI: Implements and completes tasks
```

## 🛡️ CLI Failure Scenarios

### Common CLI Errors
1. **Command Not Found**: Command doesn't exist
2. **Permission Denied**: File permissions missing
3. **Path Issues**: Path not found
4. **Dependencies**: Missing dependencies
5. **Unicode/Encoding**: Character encoding issues
6. **Timeout**: Command timeout

### AI Response
**ABSOLUTELY**: AI never stops, always uses alternative path

## 🔄 Fallback Mechanisms

### Level 1: CLI Retry
```bash
# AI first attempt
specpulse spec create "User authentication"
```

### Level 2: Manual Structure
```bash
# If CLI fails
mkdir -p .specpulse/specs/001-user-authentication
touch .specpulse/specs/001-user-authentication/spec-001.md
# Manual content addition...
```

### Level 3: Embedded Template
```markdown
# If CLI fails
<!-- AI: Use embedded template to create spec -->
# Specification: User authentication

<!-- FEATURE_DIR: 001-user-authentication -->
<!-- FEATURE_ID: 001 -->
<!-- SPEC_NUMBER: 001 -->
<!-- STATUS: pending -->
<!-- CREATED: 2025-11-02T12:00:00 -->

## Description
User authentication system

## Requirements
[To be filled by AI...]
```

## 📋 AI Commands and CLI Usage

### /sp-spec Command
```bash
# AI command
/sp-spec "User authentication with JWT"

# CLI attempt
Bash: specpulse spec create "User authentication with JWT"

# Success → AI expands spec
# Failure → AI creates manual spec
```

### /sp-plan Command
```bash
# AI command
/sp-plan "Secure authentication flow"

# CLI attempt
Bash: specpulse plan create "Secure authentication flow"

# Success → AI details plan
# Failure → AI creates manual plan
```

### /sp-task Command
```bash
# AI command
/sp-task 001

# CLI attempt
Bash: specpulse task breakdown 001

# Success → AI details tasks
# Failure → AI creates manual tasks
```

### /sp-execute Command
```bash
# AI command
/sp-execute

# CLI attempt
Bash: specpulse execute status

# Success → AI sees status and executes tasks
# Failure → AI tracks tasks manually
```

## 🚨 What Happens When CLI is Not Available?

### Full Manual Mode
AI continues to work even without SpecPulse CLI:

```python
# AI's manual procedure
def create_spec_without_cli(description):
    # 1. Create directory structure
    feature_dir = create_feature_directory()

    # 2. Create spec file
    spec_file = f"{feature_dir}/spec-001.md"

    # 3. Generate content
    content = f"""# Specification: {description}

    ## Description
    {description}

    ## Requirements
    [To be filled by AI...]
    """

    # 4. Save file
    with open(spec_file, 'w') as f:
        f.write(content)

    return spec_file
```

### Limited Mode
Some features may be limited when CLI is not available:
- ✅ Spec, plan, task creation (manual)
- ✅ Content generation (AI)
- ✅ File management (Read/Write/Edit)
- ❌ Automatic ID assignment (manual)
- ❌ Automatic validation (manual)
- ❌ Cross-platform optimization (manual)

## 📊 Success Rates

### When CLI Works
- ✅ Speed: 3-5x faster
- ✅ Consistency: 99%+ success rate
- ✅ Features: All features available
- ✅ Quality: Automatic validation and error checking

### When CLI Fails
- ⚠️ Speed: 2-3x slower
- ✅ Consistency: 95%+ success rate (with fallback)
- ✅ Features: 80-90% features available
- ⚠️ Quality: Manual validation required

## 🔧 Installation and Setup

### For AI Assistants
AI commands come with SpecPulse:
- **Claude Code**: `.claude/commands/sp-*.md` files
- **Gemini CLI**: `.gemini/commands/sp-*.toml` files

### Manual Installation
```bash
# Check if AI commands are installed
ls .claude/commands/
ls .gemini/commands/

# If missing, reinstall SpecPulse
pip install --upgrade specpulse
```

## 🧪 Test Scenarios

### Test 1: CLI Available
```bash
# Normal situation
/spec-spec "Test specification"
# Expected: CLI succeeds, AI expands spec
```

### Test 2: CLI Missing
```bash
# When CLI is removed
mv /usr/local/bin/specpulse /usr/local/bin/specpulse.backup
/spec-spec "Test specification"
# Expected: CLI fails, AI uses fallback
```

### Test 3: CLI Broken
```bash
# When CLI is broken
echo "#!/bin/bash\necho 'CLI command failed'\nexit 1" > /usr/local/bin/specpulse
chmod +x /usr/local/bin/specpulse
/sp-spec "Test specification"
# Expected: CLI fails, AI uses fallback
```

## 📞 Troubleshooting

### If AI Commands Don't Work
1. **Check SpecPulse installation**:
   ```bash
   specpulse --version
   ```

2. **Check AI command files**:
   ```bash
   ls .claude/commands/sp-spec.md
   ls .gemini/commands/sp-spec.toml
   ```

3. **Check Python path**:
   ```bash
   python -c "import specpulse; print('OK')"
   ```

4. **Check fallback log**:
   ```bash
   cat .specpulse/fallback.log
   ```

### Manual Recovery
If CLI is completely unavailable:

1. **Create directory structure manually**:
   ```bash
   mkdir -p .specpulse/{specs,plans,tasks,memory,templates}
   ```

2. **Copy templates**:
   ```bash
   # Use embedded templates
   ```

3. **Manual ID assignment**:
   ```bash
   # Use IDs in 001-, 002- format
   ```

4. **Continue using AI commands**:
   ```bash
   # AI commands will continue to work with fallback
   ```

## ✅ Success Criteria

AI-SpecPulse integration is considered successful when:

- [ ] AI uses CLI preferentially when available
- [ ] AI uses automatic fallback when CLI fails
- [ ] All AI commands continue to work with fallback
- [ ] User is notified when fallback is used
- [ ] Fallback logs are maintained and used for debugging
- [ ] Basic functions work even in manual mode

**Remember**: AI should never completely fail! There's always an alternative path. 🚀