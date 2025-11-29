---
name: SpecPulse: Continue
description: Switch to existing feature context without SpecPulse CLI
category: SpecPulse
tags: [specpulse, continue, context]
---

# SpecPulse Context Switching

Switch to existing feature context and resume work without requiring SpecPulse CLI installation.

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to context switching and memory updates
- Only edit files in memory/ directory
- Favor straightforward, minimal implementations first

**Steps**
Track these steps as TODOs and complete them one by one.
1. Parse arguments to determine action (switch or list)
2. Scan .specpulse/specs/, .specpulse/plans/, .specpulse/tasks/ for features
3. If no argument: Display feature selection interface
4. If feature provided: Validate feature exists and is accessible
5. Load and analyze feature structure and content
6. Identify current progress status and active work
7. Update .specpulse/memory/context.md with new active feature
8. Switch to feature branch if available in git
9. Validate successful context switch
10. Display comprehensive feature summary

**Reference**
- Use memory/context.md for context management
- Check all feature directories for discovery
- Follow git integration for branch switching
- Validate feature structure and accessibility

**Usage**
Arguments should be provided as: `[feature-id|feature-name]` or leave empty to list features

**Feature Selection Interface (No Arguments):**
```markdown
# Available Features for Context Switch

## 🟢 Active Features
1. **001-user-authentication** (65% complete)
   - Status: In Progress
   - Files: 2 specs, 1 plan, 25 tasks
   - Last Activity: 2 hours ago

2. **002-payment-processing** (23% complete)
   - Status: In Progress
   - Files: 1 spec, 1 plan, 18 tasks
   - Last Activity: 1 day ago

## ✅ Completed Features
3. **003-user-profiles** (100% complete)
   - Status: Completed
   - Files: 1 spec, 1 plan, 12 tasks
   - Last Activity: 3 days ago

## Selection Options
- Use number (1-3)
- Use feature ID (001, 002, 003)
- Use feature name (auth, payment, profiles)
- Type 'cancel' to abort
```

**Context Switch Template:**
```markdown
# Context Switched Successfully
**Active Feature:** [Feature Name] ([feature-id])
**Switched At:** [timestamp]

## Feature Overview
### Status and Progress
**Overall Progress:** [xx]%
**Current Phase:** [specification/planning/implementation/testing]
**Last Activity:** [time ago]

### Available Files
**Specifications:**
- spec-[id].md - [title] ([status])

**Implementation Plans:**
- plan-[id].md - [title] ([status])

**Task Breakdowns:**
- tasks-[id].md - [count] tasks total

### Current Working Context
**Directory:** .specpulse/specs/[feature-directory]/
**Git Branch:** feature/[feature-id]-[feature-name]
**Memory Context:** Updated and active

## 🎯 Next Steps
### Immediate Actions
1. **Continue Current Work:** [specific recommendation]
2. **Review Progress:** Use /status-check for detailed status
3. **Execute Tasks:** Use /task-execute [task-id|all]

### Recommended Commands
- `/status-check` - View detailed progress and metrics
- `/task-execute` - Continue with task execution
- `/validate-quality` - Check work quality
- `/plan-generate` - Update implementation plans if needed

### Feature Summary
**Total Tasks:** [count]
**Completed Tasks:** [count] ([xx]%)
**In Progress:** [count]
**Blocked:** [count]
**Estimated Completion:** [date]

## 🔄 Context History
**Previous Feature:** [feature-name] (switched from [time ago])
**Session Start:** [timestamp]
**Total Switches Today:** [count]

## ✅ Context Ready
Feature context is now active and ready for continued development.
All SpecPulse commands will now operate within this feature context.
```

**Memory Context Structure:**
```yaml
---
context_version: "1.0"
last_updated: "[timestamp]"
active_feature:
  id: "[feature-id]"
  name: "[feature-name]"
  directory: "[feature-directory]"
  status: "[in_progress/completed/paused]"
  progress: [xx]
  created_at: "[creation-timestamp]"
  last_activity: "[activity-timestamp]"
git_context:
  branch: "feature/[feature-id]-[feature-name]"
  remote: "origin"
  commit_hash: "[commit-hash]"
working_directory: ".specpulse/specs/[feature-directory]/"
feature_history:
  - feature_id: "[previous-id]"
    name: "[previous-name]"
    switched_from: "[timestamp]"
    duration: "[time spent]"
  - feature_id: "[current-id]"
    name: "[current-name]"
    switched_to: "[timestamp]"
---
```

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Comprehensive feature discovery and analysis
- Git integration for branch management
- Memory-based context tracking and history
- Intelligent feature status detection

**Advanced Features:**
- **Feature Discovery**: Automatic scanning and analysis of all features
- **Progress Detection**: Calculate completion status from task files
- **Git Integration**: Automatic branch switching and synchronization
- **Memory Management**: Complete context tracking and switch history
- **Status Classification**: Active, completed, paused, or blocked features
<!-- SPECPULSE:END -->