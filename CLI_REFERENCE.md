# SpecPulse CLI Reference Guide

## Quick Reference

This guide provides a comprehensive reference for all SpecPulse CLI commands and their usage.

## Core Commands

### Project Management

#### `specpulse init [name]`
Initialize a new SpecPulse project.

**Syntax:**
```bash
specpulse init [project_name] [options]
```

**Options:**
- `--here` - Initialize in current directory instead of creating new one
- `--ai claude|gemini` - Set primary AI assistant (default: claude)
- `--template web|api|cli|mobile|microservice` - Project template type (default: web)

**Examples:**
```bash
# Create new project
specpulse init my-web-app

# Initialize in current directory
specpulse init --here

# Create microservice project with Gemini
specpulse init user-service --template microservice --ai gemini
```

#### `specpulse validate [component]`
Validate project components and check for issues.

**Syntax:**
```bash
specpulse validate [component] [options]
```

**Arguments:**
- `component` - Component to validate: all, spec, plan, constitution (default: all)

**Options:**
- `--fix` - Attempt to auto-fix discovered issues
- `--verbose` - Show detailed validation output

**Examples:**
```bash
# Validate entire project
specpulse validate

# Validate specifications only
specpulse validate spec

# Validate and fix issues
specpulse validate --fix

# Show detailed output
specpulse validate --verbose
```

#### `specpulse doctor`
Perform system health check and diagnostics.

**Syntax:**
```bash
specpulse doctor
```

**Checks performed:**
- Python version compatibility
- Git installation and configuration
- Project structure completeness
- Required directories and files
- System permissions

#### `specpulse sync`
Synchronize project state and update memory system.

**Syntax:**
```bash
specpulse sync
```

**Actions performed:**
- Create missing directories
- Update context file with timestamp
- Count specifications, plans, and tasks
- Check Git status if in Git repository
- Update project state in memory system

### Specification Management

#### `specpulse decompose [spec_id]`
Decompose large specifications into smaller components.

**Syntax:**
```bash
specpulse decompose [spec_id] [options]
```

**Arguments:**
- `spec_id` - Specification ID to decompose (e.g., 001 or 001-feature)

**Options:**
- `--microservices` - Generate microservice boundaries
- `--apis` - Generate API contracts
- `--interfaces` - Generate interface specifications

**Examples:**
```bash
# Decompose specification 001
specpulse decompose 001

# Full decomposition with all outputs
specpulse decompose user-auth --microservices --apis --interfaces
```

**Generated outputs:**
- Microservice boundaries and responsibilities
- OpenAPI 3.0 specification files
- TypeScript interface definitions
- Integration maps and data flow diagrams

## Template Management

### Template Commands

#### `specpulse template list [--category]`
List available templates with metadata.

**Syntax:**
```bash
specpulse template list [options]
```

**Options:**
- `--category spec|plan|task|decomposition` - Filter by template category

**Output:**
- Template name and version
- Category and author
- Last modified date
- Template status

#### `specpulse template validate [name]`
Validate template syntax and structure.

**Syntax:**
```bash
specpulse template validate [template_name] [options]
```

**Arguments:**
- `template_name` - Specific template to validate (validates all if omitted)

**Options:**
- `--fix` - Attempt to auto-fix template issues

**Validation checks:**
- Jinja2 syntax validation
- Required variables presence
- Template structure compliance
- SDD principle alignment

#### `specpulse template preview <name>`
Preview template with sample data.

**Syntax:**
```bash
specpulse template preview <template_name>
```

**Arguments:**
- `template_name` - Name of template to preview

**Features:**
- Renders template with sample data
- Shows variable substitutions
- Highlights template structure
- Displays in formatted output

#### `specpulse template backup`
Backup all templates with versioning.

**Syntax:**
```bash
specpulse template backup
```

**Actions:**
- Creates timestamped backup directory
- Copies all template files
- Preserves template metadata
- Generates backup manifest

#### `specpulse template restore <path>`
Restore templates from backup.

**Syntax:**
```bash
specpulse template restore <backup_path>
```

**Arguments:**
- `backup_path` - Path to backup directory

**Actions:**
- Validates backup integrity
- Restores template files
- Recovers template metadata
- Updates template registry

## Memory Management

### Memory Commands

#### `specpulse memory search <query>`
Search memory system for entries matching query.

**Syntax:**
```bash
specpulse memory search <query> [options]
```

**Arguments:**
- `query` - Search query string

**Options:**
- `--category <category>` - Filter by memory category
- `--days <N>` - Limit to last N days

**Search filters:**
- Feature names and descriptions
- Decision records
- Context entries
- Action items

**Output:**
- Entry type and ID
- Date/timestamp
- Summary of content
- Relevance ranking

#### `specpulse memory summary`
Show memory system summary and statistics.

**Syntax:**
```bash
specpulse memory summary
```

**Statistics displayed:**
- Total decision records
- Active/completed features
- Context entry count
- Memory usage in MB
- Recent activity timeline

#### `specpulse memory cleanup [--days <N>]`
Clean up old memory entries to manage storage.

**Syntax:**
```bash
specpulse memory cleanup [options]
```

**Options:**
- `--days <N>` - Remove entries older than N days (default: 90)

**Cleanup actions:**
- Removes old context entries
- Archives old decision records
- Updates memory index
- Reports cleanup statistics

#### `specpulse memory export [--format <format>] [--output <file>]`
Export memory data for backup or analysis.

**Syntax:**
```bash
specpulse memory export [options]
```

**Options:**
- `--format json|yaml` - Export format (default: json)
- `--output <file>` - Save to specific file (displays preview if omitted)

**Export includes:**
- Decision records
- Context entries
- Feature status
- Memory metadata

## Help System

### Help Commands

#### `specpulse help [topic]`
Show comprehensive help and documentation.

**Syntax:**
```bash
specpulse help [topic] [options]
```

**Arguments:**
- `topic` - Specific help topic (shows overview if omitted)

**Options:**
- `--list` - List all available help topics

**Available topics:**
- `overview` - SpecPulse concepts and principles
- `commands` - Complete command reference
- `workflow` - Development workflow guide
- `templates` - Template system documentation
- `troubleshooting` - Common issues and solutions
- `examples` - Real-world usage examples

## Global Options

These options can be used with any SpecPulse command:

### `--version`
Show SpecPulse version information.

**Syntax:**
```bash
specpulse --version
```

### `--no-color`
Disable colored output for compatibility.

**Syntax:**
```bash
specpulse --no-color <command>
```

### `--verbose` / `-v`
Enable verbose output for debugging.

**Syntax:**
```bash
specpulse --verbose <command>
```

## Command Examples by Use Case

### New Project Setup
```bash
# Initialize project
specpulse init my-project --template web

# Navigate and start AI assistant
cd my-project
claude .

# Create first feature
/sp-pulse user-authentication
```

### Project Validation
```bash
# Quick health check
specpulse doctor

# Validate entire project
specpulse validate --verbose

# Fix issues automatically
specpulse validate --fix
```

### Template Management
```bash
# List all templates
specpulse template list

# Validate templates
specpulse template validate

# Preview template
specpulse template preview spec.md

# Backup before changes
specpulse template backup
```

### Memory Management
```bash
# Search for decisions
specpulse memory search "authentication"

# Show memory status
specpulse memory summary

# Export memory data
specpulse memory export --format json --output backup.json

# Clean old entries
specpulse memory cleanup --days 30
```

### Advanced Workflows
```bash
# Decompose large feature
specpulse decompose 001 --microservices --apis --interfaces

# Validate specific component
specpulse validate spec --verbose

# Get help with workflow
specpulse help workflow
```

## Error Handling

### Common Exit Codes
- `0` - Success
- `1` - General error
- `130` - User interruption (Ctrl+C)

### Error Recovery
- Use `specpulse doctor` for system diagnostics
- Check `specpulse help troubleshooting` for common issues
- Use `--verbose` flag for detailed error information
- Validate project structure with `specpulse validate`

### Getting Help
- `specpulse help` - General help and overview
- `specpulse help --list` - List all help topics
- `specpulse help <topic>` - Specific topic help
- `specpulse <command> --help` - Command-specific help

## Tips and Best Practices

### Productivity
- Use tab completion for commands and options
- Create shell aliases for frequently used commands
- Use project templates for consistent setup
- Regular validation prevents issues accumulation

### Workflow
- Always run `specpulse doctor` when encountering issues
- Use `--verbose` flag for debugging complex problems
- Backup templates before making customizations
- Regular memory cleanup maintains performance

### Collaboration
- Use memory system for team decisions and context
- Maintain consistent template standards
- Regular validation ensures project health
- Share help documentation with team members

## Advanced Usage

### Scripting
All SpecPulse commands can be used in shell scripts:

```bash
#!/bin/bash
# Setup new project with validation
specpulse init "$1" --template web
cd "$1"
specpulse doctor
specpulse validate
echo "Project $1 ready for development"
```

### Integration
SpecPulse integrates with:
- Git workflows (automatic commits)
- CI/CD pipelines (validation steps)
- IDE tools (file watchers)
- AI assistants (custom commands)

### Customization
- Modify templates for project-specific needs
- Extend memory system with custom categories
- Create custom shell scripts for workflows
- Integrate with existing development tools

This reference guide covers all SpecPulse CLI functionality. For additional help, use the built-in help system or consult the project documentation.