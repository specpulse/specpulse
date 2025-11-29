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
└── windsurf/                     # Windsurf commands (.md format with custom structure)
    ├── sp-pulse.md             # Feature initialization (Windsurf format)
    ├── sp-spec.md              # Specification management (Windsurf format)
    ├── sp-plan.md              # Implementation planning (Windsurf format)
    ├── sp-task.md              # Task management (Windsurf format)
    ├── sp-execute.md           # Continuous execution (Windsurf format)
    ├── sp-status.md            # Progress tracking (Windsurf format)
    ├── sp-continue.md          # Resume work (Windsurf format)
    ├── sp-decompose.md         # Feature decomposition (Windsurf format)
    ├── sp-validate.md          # Validation (Windsurf format)
    ├── sp-clarify.md           # Clarifications (Windsurf format)
    ├── sp-feature.md           # Feature initialization alias (Windsurf format)
    └── utility/                # Utility commands
└── cursor/                      # Cursor commands (.md format with custom front matter)
    ├── sp-pulse.md             # Feature initialization (Cursor format)
    ├── sp-spec.md              # Specification management (Cursor format)
    ├── sp-plan.md              # Implementation planning (Cursor format)
    ├── sp-task.md              # Task management (Cursor format)
    ├── sp-execute.md           # Continuous execution (Cursor format)
    ├── sp-status.md            # Progress tracking (Cursor format)
    ├── sp-validate.md          # Validation (Cursor format)
    ├── sp-feature.md           # Feature initialization alias (Cursor format)
    └── utility/                # Utility commands
└── github/                      # GitHub Copilot commands (.prompt.md format)
    ├── sp-pulse.prompt.md       # Feature initialization (GitHub Copilot format)
    ├── sp-spec.prompt.md        # Specification management (GitHub Copilot format)
    ├── sp-plan.prompt.md        # Implementation planning (GitHub Copilot format)
    ├── sp-task.prompt.md        # Task management (GitHub Copilot format)
    ├── sp-execute.prompt.md     # Continuous execution (GitHub Copilot format)
    ├── sp-status.prompt.md      # Progress tracking (GitHub Copilot format)
    ├── sp-validate.prompt.md    # Validation (GitHub Copilot format)
    ├── sp-feature.prompt.md     # Feature initialization alias (GitHub Copilot format)
    └── utility/                 # Utility commands
└── crush/                       # Crush AI commands (.md format with category)
    ├── pulse.md                 # Feature initialization (Crush format)
    ├── spec.md                  # Specification management (Crush format)
    ├── plan.md                  # Implementation planning (Crush format)
    ├── task.md                  # Task management (Crush format)
    ├── execute.md               # Continuous execution (Crush format)
    ├── status.md                # Progress tracking (Crush format)
    ├── validate.md              # Validation (Crush format)
    ├── continue.md              # Resume work (Crush format)
    ├── decompose.md             # Feature decomposition (Crush format)
    ├── clarify.md               # Clarifications (Crush format)
    └── utility/                 # Utility commands

Note:
- Claude uses Markdown (.md) with YAML front matter
- Gemini uses TOML (.toml) configuration format
- Windsurf uses Markdown (.md) with custom front matter and SPECPULSE:START/END blocks
- Cursor uses Markdown (.md) with custom front matter (name, id, category) and SPECPULSE:START/END blocks
- GitHub Copilot uses Markdown (.prompt.md) with $ARGUMENTS placeholder and SPECPULSE:START/END blocks
- Crush uses Markdown (.md) with category front matter and SPECPULSE:START/END blocks (no sp- prefix in filenames)
- OpenCode uses Workflow format with agent and workflow_type fields
All formats contain the SAME instructions and workflows!
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
2. Create command file in correct directory format:
   - **Claude**: `.md` with YAML front matter
   - **Gemini**: `.toml` configuration
   - **Windsurf**: `.md` with custom front matter and SPECPULSE:START/END blocks
   - **Cursor**: `.md` with custom front matter (name, id, category) and SPECPULSE:START/END blocks
   - **GitHub Copilot**: `.prompt.md` with $ARGUMENTS placeholder and SPECPULSE:START/END blocks
3. Update CLI integration if needed
4. Test with all supported AI tools (Claude, Gemini, Windsurf, Cursor, GitHub Copilot)
5. Update documentation
6. Update AIInstructionProvider if adding new methods

### Command Structure Templates

#### Claude Format (.md)
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

#### Gemini Format (.toml)
```toml
description = "Brief description"
prompt = """
## Command: /command [args]

1. Step-by-step description
2. CLI integration points
3. Memory updates
4. Validation checks
"""
```

#### Windsurf Format (.md)
```markdown
---
description: Brief description
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the command outcome
- Only edit specific directories as needed

**Steps**
1. Step-by-step description
2. CLI integration points
3. Memory updates
4. Validation checks

**Usage**
```
/command [args]
```
<!-- SPECPULSE:END -->
```

#### Cursor Format (.md)
```markdown
---
name: /command-name
id: command-name
category: SpecPulse
description: Brief description
---
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the command outcome
- Only edit specific directories as needed

**Steps**
Track these steps as TODOs and complete them one by one.
1. Step-by-step description
2. CLI integration points
3. Memory updates
4. Validation checks

**Usage**
```
/command [args]
```

**Reference**
- Additional help and reference information
<!-- SPECPULSE:END -->
```

#### GitHub Copilot Format (.prompt.md)
```markdown
---
description: Brief description
---

$ARGUMENTS
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the command outcome
- Only edit specific directories as needed

**Steps**
Track these steps as TODOs and complete them one by one.
1. Parse arguments from $ARGUMENTS
2. Step-by-step description
3. CLI integration points
4. Memory updates
5. Validation checks

**Usage**
Arguments should be provided as: `[args]`

**Reference**
- Additional help and reference information
<!-- SPECPULSE:END -->
```

## 🔄 Maintenance

- Regularly review command organization
- Update CLI integration as needed
- Keep documentation current
- Test with all AI assistants
- Archive unused commands