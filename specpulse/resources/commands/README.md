# SpecPulse Custom Commands System

## 📁 Directory Structure

```
commands/
├── README.md                     # This file - system documentation
├── claude/                       # Claude Code commands
│   ├── workflow/               # Workflow management commands
│   │   ├── sp-init.md        # Initialize new feature
│   │   ├── sp-spec.md         # Specification creation
│   │   ├── sp-plan.md        # Implementation planning
│   │   ├── sp-task.md        # Task breakdown
│   │   ├── sp-execute.md     # Task execution
│   │   ├── sp-status.md      # Progress tracking
│   │   ├── sp-continue.md    # Resume work
│   │   └── sp-summary.md     # Generate summaries
│   ├── analysis/               # Analysis and decomposition commands
│   │   ├── sp-decompose.md   # Feature decomposition
│   │   ├── sp-analyze.md     # Code analysis
│   │   └── sp-validate.md    # Validation and quality
│   └── utility/                # Utility commands
│       ├── sp-backup.md      # Backup operations
│       ├── sp-restore.md    # Restore operations
│       └── sp-clean.md       # Cleanup operations
└── gemini/                       # Gemini CLI commands
    ├── workflow/
    │   ├── sp-init.toml
    │   ├── sp-spec.toml
    │   ├── sp-plan.toml
    │   ├── sp-task.toml
    │   ├── sp-execute.toml
    │   ├── sp-status.toml
    │   ├── sp-continue.toml
    │   └── sp-summary.toml
    ├── analysis/
    │   ├── sp-decompose.toml
    │   ├── sp-analyze.toml
    │   └── sp-validate.toml
    └── utility/
        ├── sp-backup.toml
        ├── sp-restore.toml
        └── sp-clean.toml
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
| Command | Purpose | CLI Integration |
|---------|---------|-----------------|
| `/sp-decompose` | Decompose features | `specpulse validate decomposition` |
| `/sp-analyze` | Analyze code | `specpulse doctor --analyze` |
| `/sp-validate` | Quality checks | `specpulse validate --fix` |

## 🔧 Integration Guidelines

### Custom Commands CLI Integration
```bash
# Example: sp-spec command structure
# Instead of: bash scripts/sp-pulse-spec.sh
# Use: specpulse --no-color validate spec --verbose
```

### Memory Integration
```bash
# Set current feature context
specpulse context set current.feature "user-auth"
specpulse context set current.feature_id "001"

# Get context for AI
specpulse context get current.feature
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