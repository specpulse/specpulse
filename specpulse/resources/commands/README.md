# SpecPulse Custom Commands System (v2.1.3)

## 📁 Directory Structure (v2.1.3)

```
commands/
├── README.md                     # This file - system documentation
├── claude/                       # Claude Code commands (.md format)
│   ├── sp-pulse.md             # Feature initialization (v2.1.3 CLI)
│   ├── sp-spec.md              # Specification management (v2.1.3 CLI)
│   ├── sp-plan.md              # Implementation planning (v2.1.3 CLI)
│   ├── sp-task.md              # Task management (v2.1.3 CLI)
│   ├── sp-execute.md           # Continuous execution
│   ├── sp-status.md            # Progress tracking
│   ├── sp-continue.md          # Resume work
│   ├── sp-decompose.md         # Feature decomposition
│   ├── sp-validate.md          # Validation
│   ├── sp-clarify.md           # Clarifications
│   └── utility/                # Utility commands
└── gemini/                       # Gemini CLI commands (.toml format)
    ├── sp-pulse.toml           # Same as Claude (TOML format)
    ├── sp-spec.toml            # Same as Claude (TOML format)
    ├── sp-plan.toml            # Same as Claude (TOML format)
    ├── sp-task.toml            # Same as Claude (TOML format)
    ├── sp-execute.toml         # Same as Claude (TOML format)
    ├── sp-status.toml          # Same as Claude (TOML format)
    ├── sp-continue.toml        # Same as Claude (TOML format)
    ├── sp-decompose.toml       # Same as Claude (TOML format)
    ├── sp-validate.toml        # Same as Claude (TOML format)
    ├── sp-clarify.toml         # Same as Claude (TOML format)
    └── utility/                # Utility commands

Note: Claude uses Markdown (.md), Gemini uses TOML (.toml)
Both formats contain the SAME instructions and workflows!
```

## 🚀 Command Categories

### 🔄 Workflow Commands
**Purpose**: Manage the complete development workflow
- **Init**: Start new features and projects
- **Spec**: Create and manage specifications
- **Plan**: Generate implementation plans
- **Task**: Break down work into manageable tasks
- **Execute**: Run tasks continuously
- **Status**: Track progress and state
- **Continue**: Resume work on existing features

### 🔍 Analysis Commands
**Purpose**: Analyze and improve existing work
- **Decompose**: Break large features into components
- **Analyze**: Code quality and structure analysis
- **Validate**: Quality checks and compliance

### 🛠️ Utility Commands
**Purpose**: Support operations and maintenance
- **Backup**: Create project backups
- **Restore**: Restore from backups
- **Clean**: Clean up old or unused files

## 📋 Command Reference

### Workflow Commands
| Command | Purpose | CLI Integration |
|---------|---------|-----------------|
| `/sp-init` | Initialize feature | `specpulse create_feature_structure()` |
| `/sp-spec` | Create specification | `specpulse validate spec` |
| `/sp-plan` | Create plan | `specpulse validate plan` |
| `/sp-task` | Create tasks | `specpulse validate task` |
| `/sp-execute` | Execute tasks | `specpulse doctor` |
| `/sp-status` | Check progress | `specpulse spec progress` |
| `/sp-continue` | Resume work | `specpulse context get` |

### Analysis Commands
| Command | Purpose | CLI Integration (v2.1.3) |
|---------|---------|--------------------------|
| `/sp-decompose` | Decompose features | `specpulse decompose <spec-id>` |
| `/sp-validate` | Quality checks | `specpulse sp-spec validate` |
| `/sp-clarify` | Address clarifications | `specpulse sp-spec clarify <id>` |

## 🔧 Integration Guidelines (v2.1.3+)

### Custom Commands CLI Integration
```bash
# v2.1.3: New sp-* command structure
# Claude/Gemini slash commands now call:

/sp-pulse user-auth
  → specpulse sp-pulse init user-auth
  → Creates structure
  → LLM continues with /sp-spec

/sp-spec OAuth2 authentication
  → specpulse sp-spec create "OAuth2 authentication"
  → Creates template
  → LLM reads and expands with requirements

/sp-plan
  → specpulse sp-plan create "Implementation plan"
  → Creates template
  → LLM reads and expands with architecture

/sp-task
  → specpulse sp-task breakdown 001
  → Creates template
  → LLM reads plan and creates task breakdown
```

### Memory Integration
```bash
# Context is now auto-managed by sp-pulse commands
# No manual context setting needed!

# Context auto-updated by:
specpulse sp-pulse init <name>      # Sets active feature
specpulse sp-pulse continue <name>  # Switches feature

# LLM can read context:
cat memory/context.md
```

## 📝 Development Guidelines

### Adding New Commands
1. Choose appropriate category (workflow/analysis/utility)
2. Create command file in correct directory
3. Update CLI integration if needed
4. Test with both Claude and Gemini
5. Update documentation

### Command Structure Template
```markdown
---
name: command-name
description: Brief description
allowed_tools:
  - Bash
  - Read
  - Write
  - Edit
  - TodoWrite
---

# Command Documentation

## Usage
```
/command [args]
```

## Implementation
1. Step-by-step description
2. CLI integration points
3. Memory updates
4. Validation checks
```

## 🔄 Maintenance

- Regularly review command organization
- Update CLI integration as needed
- Keep documentation current
- Test with all AI assistants
- Archive unused commands