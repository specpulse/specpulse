# SpecPulse AI Integration Guide

This guide explains how AI assistants (Claude Code, Gemini CLI) integrate with SpecPulse to enable specification-driven development workflows.

## 🤖 AI Command Architecture

### CLI-First Design Philosophy

SpecPulse follows a **CLI-first architecture** where AI assistants prioritize CLI commands over direct file operations:

```
User Request → Try CLI Command → Fallback to File Ops → Continue Work
```

**Why CLI First?**
- Automatic metadata management (timestamps, IDs, status)
- Consistent structure validation
- Error handling and recovery
- Context tracking integration

### Command Integration Pattern

All AI commands follow this pattern:

1. **Primary**: Execute corresponding CLI command
2. **Fallback**: Use manual procedures if CLI fails
3. **Documentation**: Reference centralized guides for recovery

```bash
# AI Command Implementation Flow
User: /sp-spec "User authentication system"
    ↓
Step 1: Try CLI
    Bash: specpulse spec create "User authentication system"
    ↓
Step 2: If CLI fails, use fallback
    Manual: Follow AI_FALLBACK_GUIDE.md procedures
    ↓
Step 3: Continue work regardless of CLI status
```

## 📋 Available AI Commands

### Feature Management

#### `/sp-pulse <feature-name>` or `/sp-feature <feature-name>`
Initialize a new feature with intelligent suggestions:

**Features:**
- Smart project type detection (web, mobile, API, etc.)
- 3 specification options with time estimates:
  - **Core Specification** (2-4 hours): Essential functionality
  - **Standard Specification** (8-12 hours): Comprehensive features
  - **Complete Specification** (16-24 hours): Full-featured solution
- Complete directory structure creation
- Git branch integration
- Context management setup

**Example Usage:**
```bash
/sp-pulse user-dashboard
/sp-feature payment-api
```

#### `/sp-continue <feature-name-or-id>`
Switch context to existing feature:

**Features:**
- Feature discovery by name or ID
- Git branch switching
- Context restoration
- Status overview

### Specification Management

#### `/sp-spec [spec-id|description]`
Create or update specifications:

**Features:**
- Create new specification from description
- Update existing specification by ID
- Template-based structure with AI optimization
- Automatic metadata insertion
- Validation integration

**Examples:**
```bash
/sp-spec "OAuth2 authentication with JWT tokens"
/sp-spec spec-001  # Update existing spec
```

#### `/sp-clarify [spec-id]`
Address specification clarifications:

**Features:**
- Mark sections needing clarification
- Add clarification responses
- Update specification status
- Track resolution progress

### Planning and Task Management

#### `/sp-plan [plan-id|description]`
Generate implementation plans:

**Features:**
- Create plans from specifications
- Time-based phase breakdown
- Technology stack recommendations
- Risk assessment and mitigation
- Resource allocation

#### `/sp-task [plan-id]`
Break down plans into actionable tasks:

**Features:**
- Automatic task generation from plans
- Dependency mapping
- Priority assignment
- Acceptance criteria definition

#### `/sp-execute [task-id]`
Execute tasks continuously:

**Features:**
- Non-stop task execution mode
- Progress tracking
- Automatic checkpoint creation
- Context switching between tasks

### Analysis and Validation

#### `/sp-status`
Track progress across features:

**Features:**
- Feature completion overview
- Specification and plan status
- Task progress metrics
- Timeline projections

#### `/sp-validate [type]`
Comprehensive validation:

**Types:**
- `spec`: Specification validation
- `plan`: Plan validation
- `task`: Task validation
- `all`: Complete project validation

#### `/sp-decompose [spec-id]`
Decompose specifications into microservices:

**Features:**
- Service boundary identification
- API contract generation
- Interface definitions
- Database schema design

## 🔧 AI Integration Features

### Context Detection

SpecPulse automatically detects project context:

```python
# Current feature detection methods:
1. Git branch analysis (feature-name from branch)
2. .specpulse/memory/context.md parsing
3. Directory structure scanning
4. Recent file activity analysis
```

### Smart Suggestions

AI commands provide intelligent suggestions based on:

- **Project Type**: Web, mobile, API, desktop, CLI
- **Complexity Assessment**: Simple, moderate, complex
- **Technology Stack**: Detected from existing files
- **Team Size**: Individual, small team, enterprise

### Template Optimization

Templates are AI-optimized with:

- **Instruction Comments**: `<!-- AI: Fill this section -->`
- **Variable Markers**: `{{ feature_name }}` for easy substitution
- **Structured Sections**: Consistent organization for parsing
- **Clarification Markers**: `[NEEDS CLARIFICATION]` for uncertainties

### Progress Tracking

AI integration provides comprehensive tracking:

- **Feature Status**: pending, in-progress, completed, blocked
- **Specification Metrics**: completeness, clarity, acceptance criteria
- **Plan Progress**: phase completion, timeline adherence
- **Task Execution**: completion rates, dependency resolution

## 🛠️ Implementation Details

### Error Handling

AI commands implement robust error handling:

```python
try:
    result = execute_cli_command(command)
    if result.success:
        return result.output
except CLIError as e:
    log_fallback_usage(command, e)
    return manual_fallback_procedure(command)
```

### Fallback Procedures

When CLI fails, AI follows documented fallback procedures:

1. **Directory Creation**: Manual mkdir with proper permissions
2. **Template Usage**: Embedded templates for emergency use
3. **Metadata Generation**: Manual ID assignment and tracking
4. **Progress Continuation**: File-based status tracking

### Cross-Platform Support

AI integration works across platforms:

- **Windows**: UTF-8 encoding, path separator handling
- **macOS**: Native file system operations
- **Linux**: Standard Unix permissions and paths

## 📊 Success Metrics

### AI Command Success Rates

- **CLI Available**: 99% success rate, 3-5x faster execution
- **CLI Fallback**: 95% success rate, 2-3x slower but functional
- **Manual Mode**: 80% feature availability with basic functions

### Performance Metrics

- **Feature Initialization**: <30 seconds with CLI, <2 minutes fallback
- **Specification Creation**: <1 minute with CLI, <3 minutes fallback
- **Plan Generation**: <2 minutes with CLI, <5 minutes fallback

## 🔄 Workflow Examples

### Complete Feature Development

```bash
# 1. Initialize feature
/sp-pulse user-authentication
# → Creates structure, suggests 3 spec options

# 2. Choose specification option
/sp-spec "OAuth2 with JWT and refresh tokens"
# → Creates detailed specification

# 3. Generate implementation plan
/sp-plan
# → Creates phased implementation plan

# 4. Break down into tasks
/sp-task plan-001
# → Creates actionable task list

# 5. Execute continuously
/sp-execute
# → Non-stop task execution
```

### Specification Refinement

```bash
# 1. Create initial specification
/sp-spec "User registration system"
# → Basic specification structure

# 2. Add clarifications
/sp-clarify spec-001
# → Mark sections needing clarification

# 3. Update with details
/sp-spec spec-001 "Add email verification and password reset"
# → Enhanced specification

# 4. Validate completeness
/sp-validate spec
# → Comprehensive validation report
```

### Microservices Decomposition

```bash
# 1. Create monolith specification
/sp-spec "E-commerce platform"
# → Complete system specification

# 2. Decompose into services
/sp-decompose spec-001
# → Service boundaries and contracts

# 3. Generate service specs
# → Individual service specifications
# → API contracts and interfaces
# → Database schemas
```

## 🚀 Best Practices

### For AI Assistants

1. **Always try CLI first** before file operations
2. **Use centralized documentation** for fallback procedures
3. **Log fallback usage** for debugging
4. **Maintain context** across command sequences
5. **Validate results** before continuing

### For Users

1. **Provide clear descriptions** for specifications
2. **Review AI suggestions** before accepting
3. **Use validation commands** to ensure quality
4. **Track progress** with status commands
5. **Leverage git integration** for version control

### For Teams

1. **Standardize specification formats** using templates
2. **Use consistent naming conventions** for features
3. **Implement review processes** for specifications
4. **Track metrics** for process improvement
5. **Document decisions** in clarification sections

## 🔍 Troubleshooting

### Common Issues

**CLI Command Not Found**:
```bash
# Verify installation
python -m specpulse --version
pip install --upgrade specpulse
```

**Permission Errors**:
```bash
# Fix permissions
chmod -R 755 .specpulse/
# Or use fallback procedures
```

**Template Missing**:
```bash
# Reinitialize templates
specpulse init --force
# Or use embedded fallbacks
```

### Getting Help

1. **Check fallback guide**: `.specpulse/docs/AI_FALLBACK_GUIDE.md`
2. **Run diagnostics**: `specpulse doctor`
3. **Check version**: `specpulse --version`
4. **Review logs**: Check command output for error details

## 📚 Additional Resources

- **AI Fallback Guide**: `.specpulse/docs/AI_FALLBACK_GUIDE.md`
- **CLI Documentation**: `specpulse --help`
- **Template Reference**: `.specpulse/templates/`
- **Project Examples**: Community repository

---

*Generated by SpecPulse v2.4.9*
*Created: 2025-11-02*