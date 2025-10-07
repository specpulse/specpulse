# Changelog

All notable changes to SpecPulse will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.1] - 2025-10-07

### 🔧 Patch Release - Missing Commands Added

**Added:**
- ✅ `sp-clarify` command for both Claude and Gemini
- ✅ `sp-validate` command for both Claude and Gemini

**Details:**
- `sp-clarify`: Interactive command to resolve `[NEEDS CLARIFICATION]` markers
- `sp-validate`: Comprehensive validation for specs, plans, tasks

**Command Parity:**
- Claude: 11 commands
- Gemini: 11 commands
- Full feature parity achieved ✅

**No Breaking Changes** - Direct upgrade from v2.1.0

---

## [2.1.0] - 2025-10-07

### 🚀 MAJOR ARCHITECTURE CHANGE - CLI-First Design

This release eliminates bash/PowerShell scripts and moves all functionality to SpecPulse CLI, creating a cleaner, more maintainable architecture.

### ✨ New Features

**CLI Commands** (Complete)
- `specpulse feature init <name>` - Initialize new feature with directory structure
- `specpulse feature continue <name>` - Switch to existing feature
- `specpulse spec create <description>` - Create new specification
- `specpulse spec update <id> <description>` - Update existing spec
- `specpulse spec validate` - Validate specifications
- `specpulse plan create <description>` - Create implementation plan
- `specpulse plan update <id> <description>` - Update existing plan
- `specpulse task create <description>` - Create new task
- `specpulse task breakdown <plan-id>` - Generate tasks from plan
- `specpulse task update <id> <description>` - Update existing task
- `specpulse execute start <task-id>` - Mark task as started
- `specpulse execute done <task-id>` - Mark task as completed

### 🔧 Breaking Changes

**Script Removal**
- ⚠️ All bash/PowerShell scripts removed from `specpulse/resources/scripts/`
- ⚠️ Projects no longer have `scripts/` folder after init
- ✅ All functionality now via `specpulse` CLI commands
- ✅ Slash commands updated to use CLI instead of scripts

**Benefits**
- ✅ Smaller project footprint (~50KB less per project)
- ✅ No scripts/ folder needed
- ✅ Cross-platform by default (pure Python)
- ✅ Easier to maintain and test
- ✅ Faster execution (no shell overhead)

### 📦 New Modules

- `specpulse/cli/feature_commands.py` - Feature lifecycle management
- `specpulse/cli/spec_commands.py` - Specification management
- `specpulse/cli/plan_task_commands.py` - Plan, Task, Execute commands

### 🗑️ Removed

- `specpulse/resources/scripts/` folder (14 files, ~2000 lines)
- Script creation in `specpulse init`
- Script dependencies from slash commands

### 🛠️ Improvements

**Slash Commands Updated**
- `/sp-pulse` now uses `specpulse feature init`
- `/sp-spec` now uses `specpulse spec create/update/validate`
- `/sp-plan` now uses `specpulse plan create/update`
- `/sp-task` now uses `specpulse task create/breakdown/update`
- `/sp-execute` now uses `specpulse execute start/done`

**AI Assistant Integration**
- Claude Code and Gemini CLI call SpecPulse CLI directly
- No shell script intermediate layer
- Cleaner, more reliable command execution
- Better error handling and reporting

### 🔄 Migration Guide

**From 2.0.0 to 2.1.0**

1. **Automatic Upgrade**: Most features work without changes
2. **Remove Old Scripts**: Safe to delete `scripts/` folder in existing projects
   ```bash
   rm -rf scripts/
   ```
3. **New Commands Available**: Try the new CLI commands
   ```bash
   specpulse feature init my-feature
   specpulse spec create "new feature description"
   ```
4. **Slash Commands Work**: All slash commands automatically use new CLI

**No Data Loss**: All existing specs, plans, tasks remain compatible

### 📊 Statistics

- **Lines Removed**: ~2000 (scripts + utils)
- **Lines Added**: ~500 (CLI commands)
- **Net Change**: -1500 lines ✅
- **New Commands**: 12 new CLI commands
- **Files Deleted**: 14 script files
- **New Modules**: 3 command modules

---

## [2.0.0] - 2025-10-07

### 🚀 MAJOR RELEASE - Enhanced AI Integration & Advanced Workflow

This release represents a revolutionary evolution of SpecPulse with enhanced AI integration, smart context detection, and advanced workflow orchestration capabilities while maintaining our privacy-first design principles.

### ✨ New Features

**Enhanced AI Integration** (Complete)
- **Smart Context Detection**: Auto-detects current feature from git branch and memory files
- **AI-Powered Suggestions**: Intelligent next-step recommendations based on project state
- **Multi-LLM Support**: Switch between Claude, Gemini, or both simultaneously
- **AI Workflow Checkpoints**: Track and restore AI workflow states
- **Interactive AI Assistance**: Get contextual help and template recommendations
- **Real-time Progress Tracking**: Monitor workflow progress with AI insights
- **Privacy-First Design**: No external API calls - works completely offline

**New AI Commands** (Complete)
- `specpulse ai context` - Show AI-detected project context
- `specpulse ai suggest` - Get AI-powered suggestions
- `specpulse ai suggest --query <topic>` - Get help with specific topics
- `specpulse ai switch <llm>` - Switch active LLM (claude/gemini/both)
- `specpulse ai checkpoint <description>` - Create AI workflow checkpoint
- `specpulse ai summary` - Show complete AI workflow summary

**Advanced Template System** (Enhanced)
- **3-Tier Architecture**:
  - Minimal (2-3 min, quick prototypes)
  - Standard (10-15 min, most features)
  - Complete (30-45 min, production features)
- **Smart Template Selection**: AI recommends optimal template based on complexity
- **Enhanced LLM Guidance**: Comprehensive guidance comments throughout templates
- **Template Inheritance**: Standard and Complete templates extend Minimal

**Improved Context Management** (Enhanced)
- **Git Integration**: Auto-detect features from branch names
- **Memory System**: Enhanced memory management with smart features
- **Cross-Reference**: Automatic linking between specs, plans, and tasks
- **Progress Tracking**: Real-time workflow progress monitoring

### 🔧 Breaking Changes

**CLI Interface Updates**
- **New AI Commands**: Added `ai` subcommand with multiple actions
- **Enhanced Context**: Better context detection and management
- **Unicode Fixes**: Removed emoji characters for Windows compatibility

**Template Structure Changes**
- **New Template Files**:
  - `spec-tier1-minimal.md` - Enhanced minimal template
  - `spec-tier2-standard.md` - Enhanced standard template
  - `spec-tier3-complete.md` - Enhanced complete template
- **Legacy Support**: Old template names maintained with deprecation warnings
- **Enhanced Metadata**: Improved YAML frontmatter with progress tracking

### 📦 New Modules

- `specpulse/core/ai_integration.py` (400+ lines) - Enhanced AI integration system
- Enhanced `specpulse/cli/main.py` - New AI command handlers (150+ lines)
- Updated template system with 3-tier architecture

### 🛠️ Improvements

**Performance & Reliability**
- ✅ Fixed Unicode encoding issues on Windows
- ✅ Enhanced error handling for AI commands
- ✅ Improved context detection accuracy
- ✅ Better memory management and caching

**Developer Experience**
- ✅ Smarter command suggestions
- ✅ Enhanced workflow visibility
- ✅ Better error messages and recovery suggestions
- ✅ Interactive help system

**Quality Assurance**
- ✅ All AI integration features thoroughly tested
- ✅ Enhanced test coverage for new features
- ✅ Cross-platform compatibility verified
- ✅ Privacy-first design validated

### 🔄 Migration Guide

**From 1.9.x to 2.0.0**

1. **Automatic Upgrade**: Most features work without changes
2. **New AI Commands**: Try `specpulse ai context` to see enhanced features
3. **Template Updates**: New tiered templates provide better guidance
4. **No Data Migration**: All existing files remain compatible

**Recommended Actions**
- Run `specpulse ai summary` to see your current workflow state
- Try `specpulse ai suggest` to get intelligent recommendations
- Explore new tiered templates for better spec quality

### 🐛 Bug Fixes

- Fixed Unicode encoding issues on Windows systems
- Enhanced error handling for AI command failures
- Improved context detection reliability
- Fixed template loading issues in certain environments
- Resolved memory management edge cases

### 📊 Statistics

- **New Lines of Code**: 550+ lines of new functionality
- **New Commands**: 5 new AI commands with 15+ sub-options
- **New Templates**: 3 enhanced tiered templates with comprehensive guidance
- **Test Coverage**: Maintained >90% coverage for all features
- **Platform Support**: Windows, Linux, macOS fully verified

---

## [1.9.1] - 2025-10-06

### 🔧 Bug Fix Release

**Fixed:**
- ✅ Tier templates now correctly copied during `specpulse init`
- ✅ All 6 tier template files (spec-tier1/2/3.md) now included in new projects

**No Breaking Changes** - Direct upgrade from 1.9.0

---

## [1.9.0] - 2025-10-06

### 🚀 MAJOR RELEASE - Better Workflow Support (Incremental Spec Building)

This release implements v1.9.0 from ROADMAP, enabling incremental spec building with checkpoints and progress tracking. Users can now start with minimal specs (2-3 minutes) and expand when ready, with automatic safety checkpoints.

### ✨ New Features

**Checkpoint System** (Complete)
- **Automatic Checkpoints**: Created before tier expansion and section addition
- **Manual Checkpoints**: `specpulse checkpoint create <feature-id> "description"`
- **List & Restore**: `specpulse checkpoint list/restore <feature-id> <checkpoint-name>`
- **Auto-Cleanup**: Delete checkpoints older than 30 days
- **SHA-256 Verification**: Integrity checks on creation and restoration
- **Atomic Operations**: All-or-nothing with automatic rollback

**Incremental Building** (Complete)
- **Progress Tracking**: `specpulse spec progress <feature-id>` shows completion percentage
- **Section Addition**: `specpulse spec add-section <feature-id> <section-name>`
- **Visual Indicators**: ✓ (complete), ⚠️ (partial), ⭕ (not started)
- **Smart Recommendations**: Suggests next section to work on

**Tiered Templates** (Complete - enhanced from v1.6.0)
- **spec-tier1.md**: Minimal tier (3 sections, 2-3 min)
- **spec-tier2.md**: Standard tier (7-8 sections, 10-15 min)
- **spec-tier3.md**: Complete tier (15+ sections, 30-45 min)
- **Enhanced LLM Guidance**: All templates include extensive `<!-- LLM GUIDANCE -->` comments

### 📦 New Modules

- `specpulse/core/checkpoints.py` (300 lines)
- Enhanced `specpulse/core/progress_calculator.py` (200 lines)
- Updated template system with tier inheritance

### 🛠️ Improvements

- **Safety**: Atomic operations with automatic rollback
- **Performance**: Optimized checkpoint operations
- **User Experience**: Visual progress indicators and smart suggestions
- **Integration**: Seamless integration with existing workflow

---

## [1.8.0] - 2025-10-06

### 🔧 MAJOR RELEASE - Better Validation Feedback

This release completely redesigns validation feedback to provide actionable, LLM-friendly error messages and auto-fix capabilities.

### ✨ New Features

**Actionable Validation for LLMs** (Complete)
- **Enhanced Error Messages**: Errors include meaning, examples, suggestions, and help commands
- **Auto-Fix**: `--fix` flag automatically adds missing sections with backups
- **Partial Validation**: `--partial` for work-in-progress specs (shows completion %)
- **Rich Formatting**: Beautiful color-coded error panels with icons (✓ ⚠️ ⭕)
- **Custom Rules**: Project-type-specific validation (web-app, api, mobile-app)
- **LLM-Optimized**: Examples show exactly what to add, suggestions are actionable
- **Smart Suggestions**: Next section recommendations based on completion state

### 🔧 Breaking Changes

- **Validation Output Format**: Completely redesigned for better LLM interaction
- **New Command Options**: Added `--fix`, `--partial`, `--progress`, `--show-examples`
- **Enhanced Error Codes**: More specific error categories and messages

### 📦 New Modules

- `specpulse/core/validation_helpers.py` (400 lines)
- Enhanced `specpulse/core/validator.py` (600+ lines)
- Updated `specpulse/utils/error_handler.py` (300+ lines)

### 🛠️ Improvements

- **Error Recovery**: Automatic fixes with backup and rollback
- **User Guidance**: Step-by-step instructions for fixing issues
- **Performance**: Faster validation with better caching
- **Integration**: Better integration with AI assistants

---

## [1.7.0] - 2025-10-06

### 🔧 MAJOR RELEASE - Better Context for LLMs

This release introduces intelligent context management that eliminates repetitive questions from LLMs and provides structured memory for project knowledge.

### ✨ New Features

**Intelligent Context Management** (Complete)
- **Structured Memory**: Tag-based organization (decisions, patterns, constraints, current state)
- **Auto Context Injection**: AI scripts automatically receive project context
- **Quick Notes**: Capture insights during development, merge to specs later
- **Zero Friction**: LLMs stop asking repetitive questions about tech stack
- **Queryable Memory**: Find past decisions and patterns instantly
- **Performance**: Sub-100ms queries, <500 char context injection

### 🔧 Breaking Changes

- **Memory Format**: New structured memory system with tags
- **Context Injection**: Enhanced AI command templates with context
- **Command Structure**: Updated AI scripts to use new memory system

### 📦 New Modules

- `specpulse/core/memory_manager.py` (500+ lines)
- Enhanced AI command templates with context injection
- Updated memory templates with structured format

### 🛠️ Improvements

- **Context Awareness**: AI understands project state better
- **Knowledge Persistence**: Important decisions are preserved
- **Search Capability**: Instant access to past decisions
- **Performance**: Faster AI interactions with better context

---

## [1.6.0] - 2025-10-06

### 🔧 MAJOR RELEASE - Tiered Templates

This release introduces progressive specification building with three template tiers, allowing teams to start minimal and expand as needed.

### ✨ New Features

**Progressive Specification Building** (Complete)
- **Three Template Tiers**: Minimal (3 sections), Standard (7-8 sections), Complete (15+ sections)
- **Content Preservation**: Your work is never lost during tier expansion
- **LLM Guidance**: AI-optimized comments in every template
- **Flexible Workflow**: Start minimal, expand when ready
- **Automatic Backups**: Timestamped backups before each expansion
- **Preview Changes**: `--show-diff` to see what will be added

### 🔧 Breaking Changes

- **Template System**: New tiered template architecture
- **Command Structure**: New `expand` command for tier management
- **Template Names**: Updated naming convention for clarity

### 📦 New Modules

- `specpulse/core/tier_manager.py` (300+ lines)
- Enhanced template system with tier inheritance
- New tiered templates with progressive complexity

### 🛠️ Improvements

- **Flexibility**: Start simple, expand complexity as needed
- **Safety**: Automatic backups protect your work
- **Guidance**: Better AI assistance with tiered templates
- **Performance**: Optimized for different workflow stages

---

## Previous Releases

### [1.5.0] - 2025-10-06

**Quality & Documentation Enhancement**
- Comprehensive help system with 6 detailed topics
- Complete documentation suite
- 377+ tests with cross-platform CI/CD
- Template validation, memory management, advanced error handling
- Enhanced Windows, macOS, and Linux compatibility

### [1.4.0] - 2025-10-05

**Version Management & Templates**
- Single source of truth in `_version.py`
- Enhanced template system with validation
- Improved template inheritance
- Better template management commands

### [1.3.0] - 2025-10-04

**Memory Management**
- Structured memory system for decisions and patterns
- Quick note capture during development
- Searchable project knowledge base
- Memory integration with AI commands

### [1.2.0] - 2025-10-03

**Enhanced Validation**
- Comprehensive validation system
- Project-specific validation rules
- Auto-fix capabilities
- Detailed validation reporting

### [1.1.0] - 2025-10-02

**CLI Enhancement**
- Rich console output with colors and formatting
- Progress bars and animations
- Enhanced error handling
- Better user experience

### [1.0.0] - 2025-10-01

**Initial Release**
- Core specification-driven development framework
- Template system
- Basic CLI commands
- Cross-platform support