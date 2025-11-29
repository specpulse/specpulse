---
name: sp-status
description: Track project progress without SpecPulse CLI
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-status Command

Track project progress without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-status [feature-name]    # Show overview or specific feature status
```

## Implementation

When called with `/sp-status {{args}}`, I will:

### 1. Parse Arguments to Determine Scope

**I will analyze the arguments:**
- If feature name provided: Show detailed status for that feature
- If no argument: Show overview of all features
- Parse options like `--verbose`, `--validate`, `--trends`

### 2. Detect Current Feature Context

**I will identify the current working feature:**
- Check `.specpulse/memory/context.md` for active feature
- Look for most recently modified spec/plan/task directory
- Validate feature directory exists and is properly structured
- Extract feature ID and name from directory structure

### 3. For Overall Project Status (no arguments)

**I will scan and analyze all features:**

#### A. Feature Discovery
- Scan `.specpulse/specs/`, `.specpulse/plans/`, `.specpulse/tasks/` directories
- Identify all feature directories using naming convention (XXX-feature-name)
- Build comprehensive feature inventory

#### B. Feature Status Assessment
For each feature, I will determine:
- **Active**: Currently has open tasks or recent activity
- **Completed**: All tasks marked as done
- **In Progress**: Has some completed tasks with work remaining
- **Paused**: No recent activity but not all tasks complete
- **Blocked**: Has blocked tasks preventing progress

#### C. Project-Level Metrics
Calculate overall statistics:
```
TOTAL_FEATURES=5
ACTIVE_FEATURES=2
COMPLETED_FEATURES=1
IN_PROGRESS_FEATURES=1
PAUSED_FEATURES=1
OVERALL_PROGRESS=42%
```

#### D. Display Feature Overview
Show concise summary for each feature:
- Feature name and ID
- Progress percentage
- Status indicator
- File counts (specs, plans, tasks)
- Last activity timestamp
- Highlight current active feature

### 4. For Specific Feature Status

**I will provide detailed feature analysis:**

#### A. Feature Detection and Validation
- Locate feature directory structure
- Validate proper `.specpulse` organization
- Check for required subdirectories (specs/, plans/, tasks/)

#### B. File Inventory and Analysis
Count and analyze files:
- **Specification files**: Number and completeness status
- **Plan files**: Implementation plan presence and quality
- **Task files**: Task breakdown structure and progress

#### C. Progress Calculation
Calculate detailed progress metrics:
- **Overall percentage**: Based on task completion status
- **Task distribution**: Completed/in-progress/blocked/pending counts
- **Phase breakdown**: Progress by implementation phases
- **Velocity metrics**: Tasks completed per time period

#### D. Task Status Analysis
Parse task files to determine:
- Individual task status: `[x]` completed, `[ ]` pending, `[-]` in progress, `[!]` blocked
- Dependency relationships and chain status
- Parallel task availability
- Blocker identification and resolution paths

### 5. Advanced Analysis Features

#### A. Universal ID System Integration
- Track ID usage across specs, plans, and tasks
- Detect potential ID conflicts before they occur
- Show ID allocation statistics
- Validate ID numbering consistency

#### B. SDD Gates Compliance
- Verify specifications meet SDD standards
- Check task traceability to requirements
- Validate quality assurance presence
- Assess implementation completeness

#### C. Trend Analysis (if historical data available)
- Progress velocity over time
- Completion rate trends
- Blocker frequency and resolution time
- Feature development patterns

#### D. Validation and Health Check
- File structure integrity
- Required section completeness
- Dependency cycle detection
- Permission and access verification

### 6. Context Management and Updates

**I will maintain project context:**
- Update `.specpulse/memory/context.md` with latest status
- Track status check history for trend analysis
- Link related features and dependencies
- Maintain searchable status history

## Status Display Formats

### Overall Project Overview
```
🏗️  SpecPulse Project Status Overview
================================================================

📊 Project Summary
   Total Features: 5
   Overall Progress: 42% (21/50 total tasks)
   Active Features: 2
   Completed Features: 1

🚀 Active Features
   [PROG] 001-user-authentication (65%)
      Specs: 2 files ✅ Plans: 1 file ✅ Tasks: 25 tasks (16 completed)
      Last Activity: 2 hours ago

   [PROG] 002-payment-processing (23%)
      Specs: 1 file ✅ Plans: 1 file ✅ Tasks: 18 tasks (4 completed)
      Last Activity: 1 day ago

✅ Completed Features
   [OK] 000-project-setup (100%)
      All components completed and validated

⏸️  In Progress Features
   [WAIT] 003-user-profile (45%)
      Specs: 1 file ⚠️ Plans: 0 files ❌ Tasks: 12 tasks (5 completed)
      Missing: Implementation plan needed

⏸️  Paused Features
   [PAUSED] 004-notifications (78%)
      No recent activity (3 days)

📈 Project Metrics
   Average Velocity: 2.3 tasks/day
   Est. Project Completion: 2025-02-15
   Blockers: 1 (Database schema approval)

🎯 Current Context
   Active Feature: 001-user-authentication
   Working Directory: project-root/
```

### Detailed Feature Status
```
📋 Feature Status: 001-user-authentication
================================================================

**Overall Progress**: 65% (16/25 tasks completed)
**Status**: Active
**Created**: 2025-01-09
**Last Updated**: 2025-01-11 (2 hours ago)

📁 File Structure
├── Specifications: spec-001.md, spec-002.md (2 files)
│   ✅ spec-001.md - User Registration (Complete)
│   ✅ spec-002.md - Authentication Flow (Complete)
├── Plans: plan-001.md (1 file)
│   ✅ plan-001.md - Implementation Strategy (Complete)
└── Tasks: auth-service-tasks.md (1 file, 25 total tasks)

📊 Task Progress Breakdown
├── ✅ Completed: 16 tasks (64%)
├── 🔄 In Progress: 5 tasks (20%)
├── ⏸️  Pending: 3 tasks (12%)
└── ❌ Blocked: 1 task (4%)

🏗️  Phase Progress
├── Phase 0 (Critical Path): 80% complete ✅
├── Phase 1 (Foundation): 70% complete ✅
├── Phase 2 (Core Features): 50% complete 🔄
├── Phase 3 (Polish): 20% complete ⏸️
└── Phase 4 (Testing): 0% complete ❌

⚠️  Blockers and Issues
├── T015: Database schema approval pending
└── Impact: Blocks Phase 3 tasks (3 tasks affected)

🚀 Available for Work
├── Parallel Tasks: 8 available
├── Sequential Chains: 2 active chains
└── Next Recommended: T018 (Password Reset Implementation)

📈 Velocity Metrics
├── Tasks Completed: 16
├── Average Velocity: 2.5 tasks/day
├── Current Sprint: 6 tasks in 3 days
└── Est. Feature Completion: 2025-01-18

🎯 Next Steps Priority
1. Resolve T015 blocker (Database schema)
2. Complete Phase 2 core features (3 tasks)
3. Start Phase 3 polish tasks in parallel
4. Begin Phase 4 testing preparation

🔗 Dependencies
├── Depends On: 000-project-setup (completed)
├── Blocks: 003-user-profile (waiting on auth)
└── Related: 002-payment-processing (integration planned)
```

### SDD Gates Compliance Report
```
🛡️  SDD Gates Compliance Status
================================================================

📋 Feature: 001-user-authentication

✅ Specification First: 100%
   ├── 2/2 specifications complete
   ├── All requirements documented
   ├── Acceptance criteria defined
   └── No clarification markers remaining

✅ Task Decomposition: 95%
   ├── 25 tasks created from plan
   ├── Dependencies mapped and validated
   ├── Success criteria testable
   └── ⚠️ 1 task missing risk assessment

✅ Quality Assurance: 80%
   ├── Test requirements defined
   ├── Validation criteria established
   ├── Code review process planned
   └── ⚠️  Performance testing not defined

✅ Traceable Implementation: 90%
   ├── Tasks linked to specifications
   ├── Requirements traceability matrix
   ├── Implementation coverage tracked
   └── ⚠️  2 specifications tasks not mapped

📊 Overall SDD Compliance: 91%
🎯 Required: 95% for production deployment
```

## Error Handling and Recovery

### Common Issues and Solutions

#### Context Detection Failures
- **No memory file**: Create initial context structure
- **Invalid feature directory**: Suggest valid feature names
- **Multiple active features**: Prompt to select primary feature
- **Corrupted task files**: Guide through file recovery process

#### Validation Errors
- **Missing directories**: Create proper `.specpulse` structure
- **Invalid file formats**: Provide template corrections
- **Dependency cycles**: Identify and resolve circular references
- **Permission issues**: Guide user through permission fixes

#### Calculation Errors
- **Invalid task statuses**: Correct status marker format
- **Missing progress data**: Recalculate from file timestamps
- **Division by zero**: Handle edge cases in percentage calculations
- **Corrupted ID system**: Rebuild ID mapping from files

This `/sp-status` command provides **comprehensive project tracking** without requiring any SpecPulse CLI installation, using only validated file operations and detailed progress analytics.