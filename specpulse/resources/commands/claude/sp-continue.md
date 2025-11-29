---
name: sp-continue
description: Switch to existing feature context without SpecPulse CLI
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-continue Command

Switch to existing feature context without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-continue [feature-id|feature-name]    # Switch to specific feature
/sp-continue                             # Show available features
```

## Implementation

When called with `/sp-continue {{args}}`, I will:

### 1. Parse Arguments to Determine Action

**I will analyze the arguments:**
- If feature ID/name provided: Switch to that feature
- If no argument: List all available features for selection
- Validate input format (XXX-feature-name or just feature-name)

### 2. For Listing Available Features

**I will scan and display all features:**
- Scan `.specpulse/specs/`, `.specpulse/plans/`, `.specpulse/tasks/` directories
- Identify all feature directories using naming convention (XXX-feature-name)
- Display each feature with:
  - Feature ID and name
  - Progress percentage (if tasks exist)
  - File counts (specs, plans, tasks)
  - Last activity timestamp
  - Current status indicator

### 3. For Feature Context Switching

**I will perform comprehensive context switch:**

#### A. Feature Detection and Validation
- Parse feature identifier (extract ID from XXX-feature-name)
- Validate feature directory exists and is properly structured
- Check for required `.specpulse` organization
- Verify feature has content (specs, plans, or tasks)

#### B. Context Analysis
- Analyze feature structure and content
- Identify current progress status
- Check for active work or incomplete tasks
- Detect any blockers or issues

#### C. Update Memory Context
- Update `.specpulse/memory/context.md` with new active feature
- Set current working directory context
- Record feature switch history
- Update feature status and metadata

#### D. Git Integration
- Check if feature branch exists
- Switch to feature branch if available
- Create feature branch if missing
- Update git working directory context

### 4. Context Switch Validation

**I will verify successful context switch:**
- Confirm feature directory is accessible
- Validate memory context updated correctly
- Check file permissions and structure
- Verify git branch (if applicable)

### 5. Display Feature Summary

**After successful switch, I will show:**
- Feature name and ID
- Current progress status
- Available files (specs, plans, tasks)
- Last activity information
- Recommended next steps
- Any active work or blockers

## Feature Selection Interface

### When No Argument Provided
```
🔄 Feature Selection - Switch Context
================================================================

Available Features:

1) 🟢 001-user-authentication (65% complete)
   Status: Active Progress
   Files: 2 specs, 1 plan, 25 tasks
   Last Activity: 2 hours ago

2) 🟡 002-payment-processing (23% complete)
   Status: In Progress
   Files: 1 spec, 1 plan, 18 tasks
   Last Activity: 1 day ago

3) ⏸️  003-user-profile (45% complete)
   Status: Paused
   Files: 1 spec, 0 plans, 12 tasks
   Last Activity: 3 days ago

4) ✅ 000-project-setup (100% complete)
   Status: Completed
   Files: 1 spec, 1 plan, 8 tasks
   Last Activity: 1 week ago

💡 Select feature to switch to:
- Use number (1-4)
- Use feature ID (001, 002, etc.)
- Use feature name (user-auth, payment, etc.)
- Type 'cancel' to abort
```

### Successful Context Switch
```
✅ Context Switched Successfully!

🎯 Active Feature: 002-payment-processing
📁 Working Directory: .specpulse/specs/002-payment-processing/
🔗 Git Branch: feature/002-payment-processing

📊 Feature Status:
   Progress: 23% (4/18 tasks completed)
   Status: In Progress
   Created: 2025-01-10
   Last Updated: 2025-01-11

📋 Available Files:
   ├── Specifications: spec-001.md (Payment API)
   ├── Plans: plan-001.md (Implementation Strategy)
   └── Tasks: payment-tasks.md (18 tasks)

🚀 Next Steps:
   1. Continue with T005: Implement payment gateway integration
   2. Review specifications: /sp-spec validate
   3. Check task status: /sp-status
   4. Execute next task: /sp-execute

💡 Memory context updated. Ready to continue work on payment processing!
```

## Context Memory Structure

The feature context is stored in `.specpulse/memory/context.md`:

```yaml
---
context_version: "1.0"
last_updated: "2025-01-11T15:30:00Z"
active_feature:
  id: "002"
  name: "payment-processing"
  directory: "002-payment-processing"
  status: "in_progress"
  progress: 23
  created_at: "2025-01-10T09:00:00Z"
  last_activity: "2025-01-11T14:20:00Z"
git_context:
  branch: "feature/002-payment-processing"
  remote: "origin"
  commit_hash: "abc123def"
working_directory: "/project/root/.specpulse/specs/002-payment-processing"
feature_history:
  - feature_id: "001"
    name: "user-authentication"
    switched_from: "2025-01-11T15:30:00Z"
    duration: "2 days 4 hours"
  - feature_id: "002"
    name: "payment-processing"
    switched_to: "2025-01-11T15:30:00Z"
---
```

## Error Handling and Recovery

### Feature Not Found
- **Invalid feature ID**: Suggest valid feature IDs from available list
- **Feature directory missing**: Guide through feature discovery process
- **Empty feature**: Recommend running `/sp-pulse` to create feature

### Permission Issues
- **Directory access denied**: Provide permission fix instructions
- **File write errors**: Guide through permission corrections
- **Git operation failures**: Offer manual git command alternatives

### Context Recovery
- **Memory file corrupted**: Rebuild from available features
- **Git branch issues**: Work without git integration
- **Feature structure invalid**: Provide repair instructions

## Advanced Features

### Feature Search and Fuzzy Matching
- Partial name matching (e.g., "auth" matches "user-authentication")
- ID pattern matching (e.g., "00" matches all features starting with 00)
- Status-based filtering (show only active, completed, or paused features)

### Bulk Operations
- List features by progress percentage
- Show features with specific file types
- Display features sorted by last activity
- Filter features by completion status

### Context Presets
- Save frequently used feature combinations
- Quick switch between related features
- Bookmark important feature contexts

This `/sp-continue` command provides **seamless feature context switching** without requiring any SpecPulse CLI installation, using only validated file operations and comprehensive context management.