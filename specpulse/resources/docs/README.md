# SpecPulse Documentation

This directory contains comprehensive documentation for SpecPulse AI integration and fallback procedures.

## 📚 Documentation Structure

### Core Documentation

- **[AI_INTEGRATION.md](./AI_INTEGRATION.md)** - Complete guide for AI assistant integration
- **[AI_FALLBACK_GUIDE.md](./AI_FALLBACK_GUIDE.md)** - Emergency procedures when CLI fails

### Quick Reference

#### For AI Assistants
- **Primary Workflow**: CLI commands first, file operations fallback
- **Error Recovery**: Use fallback guide when CLI fails
- **Context Management**: Maintain feature context across commands

#### For Users
- **Getting Started**: Use `/sp-pulse` or `/sp-feature` to initialize
- **Daily Workflow**: `/sp-spec` → `/sp-plan` → `/sp-task` → `/sp-execute`
- **Progress Tracking**: `/sp-status` and `/sp-validate`

## 🚨 Emergency Procedures

If SpecPulse CLI commands fail, AI assistants should:

1. **Detect CLI failure** (exit codes, error patterns, timeouts)
2. **Apply fallback procedures** from [AI_FALLBACK_GUIDE.md](./AI_FALLBACK_GUIDE.md)
3. **Continue work** using manual file operations
4. **Log fallback usage** for debugging

### Critical Fallback Patterns

```bash
# Directory structure creation
mkdir -p .specpulse/specs/001-feature-name
mkdir -p .specpulse/plans/001-feature-name
mkdir -p .specpulse/tasks/001-feature-name

# Template-based file creation
# Use embedded templates from fallback guide

# Metadata management
# Manual ID assignment: 001-, 002-, 003-
# Timestamp format: 2025-11-02T12:00:00
```

## 🤖 AI Command Reference

### Feature Management
- `/sp-pulse <name>` - Initialize feature with smart suggestions
- `/sp-feature <name>` - Alias for sp-pulse
- `/sp-continue <name>` - Switch to existing feature

### Specification Work
- `/sp-spec [id|description]` - Create/update specifications
- `/sp-clarify [id]` - Address specification clarifications

### Planning and Execution
- `/sp-plan [id|description]` - Generate implementation plans
- `/sp-task [plan-id]` - Break down into tasks
- `/sp-execute [task-id]` - Execute tasks continuously

### Analysis and Validation
- `/sp-status` - Track project progress
- `/sp-validate [type]` - Comprehensive validation
- `/sp-decompose [spec-id]` - Decompose into microservices

## 📊 Success Metrics

### Reliability Rates
- **CLI Available**: 99% success rate
- **CLI Fallback**: 95% success rate
- **Manual Mode**: 80% feature availability

### Performance
- **Feature Init**: <30 seconds (CLI), <2 minutes (fallback)
- **Spec Creation**: <1 minute (CLI), <3 minutes (fallback)
- **Plan Generation**: <2 minutes (CLI), <5 minutes (fallback)

## 🛠️ Platform Support

### Supported AI Platforms
- **Claude Code** (claude.ai/code) - Full integration
- **Gemini CLI** - Full integration

### Operating Systems
- **Windows** - UTF-8 support, path handling
- **macOS** - Native file operations
- **Linux** - Unix permissions and paths

## 🔄 Workflow Examples

### New Feature Development
```bash
/sp-pulse user-authentication
# → Choose spec option (Core/Standard/Complete)
/sp-spec "OAuth2 with JWT tokens"
/sp-plan
/sp-task plan-001
/sp-execute
```

### Specification Refinement
```bash
/sp-spec "User registration system"
/sp-clarify spec-001
/sp-spec spec-001 "Add email verification"
/sp-validate spec
```

### Microservices Decomposition
```bash
/sp-spec "E-commerce platform"
/sp-decompose spec-001
# → Generates service specs and contracts
```

## 📋 File Structure

```
.specpulse/
├── docs/                    # This documentation
│   ├── README.md           # This file
│   ├── AI_INTEGRATION.md   # AI integration guide
│   └── AI_FALLBACK_GUIDE.md # Emergency procedures
├── memory/                  # Context and tracking
│   └── context.md          # Active feature context
├── specs/                   # Specifications
│   └── 001-feature-name/
│       ├── spec-001.md     # Main specification
│       └── spec-002.md     # Additional specs
├── plans/                   # Implementation plans
│   └── 001-feature-name/
│       └── plan-001.md     # Implementation plan
├── tasks/                   # Task breakdowns
│   └── 001-feature-name/
│       ├── task-001.md     # Individual tasks
│       └── _breakdown_*.md # Breakdown markers
└── templates/               # Project templates
    ├── spec.md             # Specification template
    ├── plan.md             # Plan template
    └── task.md             # Task template
```

## 🔧 Configuration

### AI Command Setup
AI commands are automatically configured during project initialization:
- Claude Code: `.claude/commands/` directory
- Gemini CLI: `.gemini/commands/` directory

### Template Customization
Templates can be customized per project:
- Edit files in `.specpulse/templates/`
- Maintain AI instruction comments
- Preserve variable markers for substitution

### Context Management
Project context is tracked in:
- `.specpulse/memory/context.md` - Active feature information
- Git branch names - Feature identification
- File metadata - Status and timestamps

## 🚨 Troubleshooting

### Common Issues

**CLI Commands Fail**:
1. Check installation: `python -m specpulse --version`
2. Use fallback procedures from [AI_FALLBACK_GUIDE.md](./AI_FALLBACK_GUIDE.md)
3. Verify permissions: `chmod -R 755 .specpulse/`

**Template Missing**:
1. Reinitialize: `specpulse init --force`
2. Use embedded templates from fallback guide
3. Check file permissions

**Context Lost**:
1. Check git branch: `git branch`
2. Review context file: `.specpulse/memory/context.md`
3. Use `/sp-continue` to restore context

### Getting Help

1. **Emergency Procedures**: [AI_FALLBACK_GUIDE.md](./AI_FALLBACK_GUIDE.md)
2. **Integration Details**: [AI_INTEGRATION.md](./AI_INTEGRATION.md)
3. **CLI Help**: `specpulse --help`
4. **Diagnostics**: `specpulse doctor`

## 📈 Best Practices

### For Development Teams
1. **Standardize Specifications**: Use consistent templates
2. **Regular Validation**: Check specs and plans frequently
3. **Context Switching**: Use `/sp-continue` for feature changes
4. **Progress Tracking**: Monitor with `/sp-status`

### For AI Assistants
1. **CLI First**: Always try CLI commands before file operations
2. **Fallback Logging**: Document when fallbacks are used
3. **Context Maintenance**: Keep feature context active
4. **Validation**: Verify results before continuing

### For Project Management
1. **Feature Planning**: Use smart suggestions from `/sp-pulse`
2. **Timeline Estimation**: Leverage time-based suggestions
3. **Risk Assessment**: Review plan risk sections
4. **Quality Gates**: Use `/sp-validate` at milestones

---

*Generated by SpecPulse v2.4.9*
*Created: 2025-11-02*
*Last Updated: 2025-11-02*