---
name: SpecPulse: Status Check
description: Check progress and status without SpecPulse CLI
category: SpecPulse
tags: [specpulse, status, check]
---

# SpecPulse Progress Monitoring

Check comprehensive project progress and status without requiring SpecPulse CLI installation.

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to status reporting and monitoring
- Only read files from specs/, plans/, tasks/, memory/ directories
- Favor straightforward, minimal implementations first

**Steps**
Track these steps as TODOs and complete them one by one.
1. Check .specpulse/memory/context.md for active feature
2. Scan all feature directories in .specpulse/specs/
3. Analyze specification files and their status
4. Review implementation plans and their completeness
5. Examine task breakdowns and progress
6. Calculate overall project metrics
7. Generate comprehensive status report
8. Identify blockers and next steps
9. Provide actionable recommendations

**Reference**
- Use memory/context.md for active feature detection
- Check all directories for comprehensive project overview
- Follow status template for consistent reporting
- Calculate metrics from file analysis

**Usage**
Arguments should be provided as: `[--feature <feature-id>] [--detailed] [--metrics]`

**Status Report Template:**
```markdown
# SpecPulse Project Status Report
**Generated:** [timestamp]
**Active Feature:** [feature-name] ([feature-id])

## 📊 Executive Summary
### Overall Project Health
**Progress Score:** [xx]% (calculating from completed tasks/total tasks)
**Active Features:** [count]
**Completed Features:** [count]
**Blocked Items:** [count]

### Key Metrics
- Total Specifications: [count]
- Total Implementation Plans: [count]
- Total Tasks: [count]
- Completed Tasks: [count] ([xx]%)
- In Progress Tasks: [count]
- Blocked Tasks: [count]

## 🎯 Current Feature: [Feature Name]
### Status Overview
**Feature ID:** [feature-id]
**Progress:** [xx]%
**Phase:** [specification/planning/implementation/testing/completed]
**Last Activity:** [timestamp]

### Specification Status
- ✅ Spec [spec-id]: [title] - [status]
- 📝 In Progress: [count] specifications
- ⏸️ Pending Review: [count] specifications

### Implementation Plan Status
- ✅ Plan [plan-id]: [title] - [status]
- 📝 In Progress: [count] plans
- ⏸️ Pending Review: [count] plans

### Task Breakdown Status
- ✅ [xx]/[total] tasks completed ([xx]%)
- 🔄 [count] tasks in progress
- ⏸️ [count] tasks pending
- ❌ [count] tasks blocked

## 📋 Detailed Task Status

### Recently Completed (Last 7 Days)
- ✅ T[xxx]: [Task Title] - completed [time ago]
- ✅ T[yyy]: [Task Title] - completed [time ago]

### Currently In Progress
- 🔄 T[aaa]: [Task Title] - started [time ago]
- 🔄 T[bbb]: [Task Title] - started [time ago]

### Upcoming Tasks (Dependencies Satisfied)
- ⏭️ T[ccc]: [Task Title] - ready to start
- ⏭️ T[ddd]: [Task Title] - ready to start

### Blockers and Issues
- ❌ T[eee]: [Task Title] - blocked by [dependency]
- ❌ T[fff]: [Task Title] - blocked by [issue]

## 🏗️ All Features Overview

### Active Features
| Feature | Progress | Tasks | Status | Last Activity |
|---------|----------|-------|--------|---------------|
| [feature-1] | [xx]% | [xx]/[yy] | [status] | [time ago] |
| [feature-2] | [xx]% | [xx]/[yy] | [status] | [time ago] |

### Completed Features
| Feature | Completed | Total Tasks | Duration |
|---------|-----------|-------------|----------|
| [feature-3] | [date] | [count] | [duration] |
| [feature-4] | [date] | [count] | [duration] |

## 📈 Progress Analytics

### Velocity Metrics
- **Tasks/Week (Last 4 Weeks):** [average]
- **Completion Rate:** [xx]%
- **Average Task Duration:** [time]
- **Blocker Resolution Time:** [time]

### Trend Analysis
- **Progress Trend:** [improving/stable/declining]
- **Quality Metrics:** [spec completion rate]
- **Efficiency Indicators:** [task completion velocity]

## 🎯 Next Steps and Recommendations

### Immediate Actions
1. **Priority 1:** [actionable recommendation]
2. **Priority 2:** [actionable recommendation]
3. **Priority 3:** [actionable recommendation]

### Process Improvements
- [Recommendation based on metrics]
- [Improvement suggestion]
- [Best practice recommendation]

### Resource Allocation
- Focus on blocked tasks to remove dependencies
- Prioritize high-impact features
- Balance new feature development with task completion

## 🔍 Detailed Metrics (Optional)
Use `--metrics` flag for extended analytics:
- Task completion by category
- Time spent per phase
- Quality and validation metrics
- Historical performance data
```

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Comprehensive project-wide status monitoring
- Real-time progress calculation and analytics
- Actionable recommendations and next steps

**Advanced Features:**
- **Multi-Feature Overview**: Track all features in project
- **Velocity Analytics**: Calculate development velocity and trends
- **Blocker Detection**: Identify and report blockers
- **Predictive Analytics**: Estimate completion dates
- **Quality Metrics**: Track specification and validation quality
<!-- SPECPULSE:END -->