---
name: sp-pulse
description: Initialize new features and manage project context without SpecPulse CLI
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
  - Glob
---

# /sp-pulse Command

Initialize new features and manage project context without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-pulse [feature-name]           # Initialize new feature
/sp-pulse status                   # Show current feature status
/sp-pulse list                     # List all features
```

## Implementation

When called with `/sp-pulse {{args}}`, I will:

### 1. Parse Arguments to Determine Action

**I will analyze the arguments:**
- If feature name provided → Initialize new feature with that name
- If `status` → Show current feature context
- If `list` → Show all available features
- If no argument → Show current feature status

### 2. For Feature Initialization

**I will create comprehensive feature structure:**

#### A. Generate Universal Feature ID
- Scan existing feature directories in `.specpulse/specs/`
- Find highest used number (001, 002, 003, etc.)
- Generate next sequential ID with zero-padding
- Create feature name from input (kebab-case)

#### B. Create Directory Structure (Atomic Operations)
**I will use atomic file operations to prevent corruption:**

**Atomic Directory Creation:**
- Use **Bash** with `mkdir -p` for atomic directory creation
- Create parent directories first: `.specpulse/`, `.specpulse/specs/`, etc.
- Validate each directory creation before proceeding
- Rollback entire operation if any step fails

**Safe File Operations:**
- Use **Write** tool with full file content (not partial updates)
- Validate file paths are within `.specpulse/` directory only
- Create backup copies before overwriting existing files
- Verify file permissions after creation

**Rollback Mechanism:**
- Track all created files and directories
- If any step fails, use **Bash** to remove partial creations
- Restore original state from backups
- Report specific failure points with recovery instructions

#### C. Initialize Feature Specification
- Create `spec-001.md` with comprehensive template
- Include executive summary placeholder
- Add functional requirements structure
- Include user stories and acceptance criteria template
- Add technical constraints and risk assessment sections

#### D. Update Project Context
- Update `.specpulse/memory/context.md` with new active feature
- Set feature metadata (ID, name, created_at, status)
- Update feature history and navigation
- Initialize decision log for the feature

#### E. Create Initial Memory Structure
- Create feature-specific memory file
- Add project context metadata
- Initialize tracking variables
- Set up decision documentation structure

### 3. For Status Display

**I will show current feature information:**
- Read current feature from `.specpulse/memory/context.md`
- Display feature ID, name, and progress
- Show file counts (specs, plans, tasks)
- Calculate and display completion percentage
- Show last activity timestamp

### 4. For Feature Listing

**I will scan and display all features:**
- Use Glob tool to find all feature directories
- Extract feature IDs and names from directory structure
- Read context information for each feature
- Display progress status and file counts
- Show last activity for each feature

## Universal ID System Implementation

### Feature ID Generation
**I ensure conflict-free numbering:**
- Scan `.specpulse/specs/` for existing directories
- Parse directory names: `XXX-feature-name` pattern
- Extract numeric ID and find highest used number
- Generate next sequential number: `XXX` where XXX = next_number
- Zero-pad to 3 digits: `001`, `002`, `003`, etc.

### File Numbering System
**I maintain consistent numbering across all file types:**
- Specifications: `spec-001.md`, `spec-002.md`, etc.
- Plans: `plan-001.md`, `plan-002.md`, etc.
- Tasks: `tasks-001.md`, `tasks-002.md`, etc.
- Service tasks: `AUTH-T001.md`, `USER-T001.md`, etc.

### Conflict Prevention
**I prevent naming conflicts through:**
- Atomic file existence checks before creation
- Sequential numbering with proper scanning
- Fallback patterns for edge cases
- Validation of directory structure integrity

## CLI-Independent Features

### Project Structure Creation
- **No CLI Dependencies**: 100% independent directory creation
- **Atomic Operations**: Create structure with rollback on failure
- **Template System**: Built-in templates for all file types
- **Validation**: Verify structure integrity after creation

### Context Management
- **Memory System**: File-based context tracking
- **Feature History**: Complete navigation history
- **Decision Logging**: Automatic decision documentation
- **Progress Tracking**: Manual calculation from file structure

### Error Handling and Recovery
- **Directory Creation Failures**: Provide permission guidance
- **File System Errors**: Graceful degradation and recovery
- **Template Missing**: Built-in fallback templates
- **Permission Issues**: Clear resolution instructions

## Output Examples

### Feature Initialization
```
User: /sp-pulse user-authentication

🚀 Initializing New Feature: user-authentication
================================================================

📊 Feature Analysis
   Project Type: User Management System
   Complexity: Standard (authentication flows)
   ID Generation: 001 (next available)
   Directory: 001-user-authentication

📁 Creating Feature Structure
   ✅ Directory: .specpulse/specs/001-user-authentication/
   ✅ Directory: .specpulse/plans/001-user-authentication/
   ✅ Directory: .specpulse/tasks/001-user-authentication/
   ✅ Context: .specpulse/memory/context.md
   ✅ Memory: .specpulse/memory/decisions.md

📄 Creating Initial Files
   ✅ Specification: spec-001.md (Executive summary template)
   ✅ Context: Feature context and metadata
   ✅ Memory: Decision tracking initialized

🔗 Feature Context Updated
   Active Feature: 001-user-authentication
   Status: Initialized
   Created: 2025-01-11 16:30:00 UTC
   Progress: 5% (structure created)

✅ Feature initialization complete!
🎯 Next steps: /sp-spec "detailed requirements" to create specification
```

### Feature Status
```
User: /sp-pulse status

📊 Current Feature Status
================================================================

🎯 Active Feature: 001-user-authentication
📁 Working Directory: .specpulse/specs/001-user-authentication/
🔗 Git Branch: feature/001-user-authentication (if git initialized)

📊 Feature Progress
   Status: In Progress
   Completion: 35% (7/20 tasks completed)
   Created: 2025-01-10 09:00:00 UTC
   Last Activity: 2025-01-11 15:45:00 UTC

📋 Available Files
   ├── Specifications: 2 files (spec-001.md, spec-002.md)
   ├── Plans: 1 file (plan-001.md)
   └── Tasks: 1 file (tasks-001.md)

🚀 Next Steps
   1. Create specification: /sp-spec "additional requirements"
   2. Generate plan: /sp-plan
   3. Break down tasks: /sp-task
   4. Execute tasks: /sp-execute

💡 Feature context ready for development
```

### Feature Listing
```
User: /sp-pulse list

📊 All Features in Project
================================================================

1) 🟢 001-user-authentication (35% complete)
   Status: In Progress
   Files: 2 specs, 1 plan, 1 task file (25 tasks)
   Last Activity: 2 hours ago
   Directory: .specpulse/specs/001-user-authentication/

2) 🟡 002-payment-processing (12% complete)
   Status: Early Development
   Files: 1 spec, 0 plans, 1 task file (12 tasks)
   Last Activity: 1 day ago
   Directory: .specpulse/specs/002-payment-processing/

3) ⏸️ 003-user-profile (0% complete)
   Status: Planned
   Files: 1 spec, 0 plans, 0 task files
   Last Activity: 3 days ago
   Directory: .specpulse/specs/003-user-profile/

📊 Project Summary
   Total Features: 3
   Active Features: 2
   Completed Features: 0
   Overall Progress: 23%

💡 Select feature to switch: /sp-continue [feature-id]
```

## Error Handling and Recovery

### Common Issues and Solutions

#### Feature Creation Failures
- **Permission Denied**: Guide user through directory permissions
- **Directory Exists**: Handle existing feature directories gracefully
- **File System Errors**: Provide recovery instructions
- **Template Missing**: Use built-in fallback structure

#### Context Management Issues
- **Memory File Corrupted**: Rebuild from available feature data
- **Feature Not Found**: Provide list of available features
- **Invalid Feature ID**: Validate and suggest correct IDs
- **Navigation Errors**: Automatic context recovery

#### ID System Conflicts
- **Number Collision**: Intelligent conflict detection and resolution
- **Invalid Format**: Automatic format correction and validation
- **Missing Features**: Handle gaps in feature numbering
- **Duplicate Names**: Suggest alternative feature names

## Advanced Features

### Feature Templates
- **Web Application**: Pre-configured for frontend/backend features
- **API Service**: Optimized for microservice architecture
- **CLI Tool**: Specialized for command-line applications
- **Library/SDK**: Configured for reusable components

### Integration Ready
- **Git Integration**: Automatic branch creation and management
- **Testing Setup**: Test structure initialization
- **CI/CD Ready**: Pipeline configuration templates
- **Documentation**: Auto-generated README and API docs

This `/sp-pulse` command provides **complete feature lifecycle management** without requiring any SpecPulse CLI installation, using only validated file operations and comprehensive project structure creation.