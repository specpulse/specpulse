---
name: sp-task
description: Create and manage tasks without SpecPulse CLI
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-task Command

Create and manage tasks without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-task [action] [feature-directory]
```

Actions: `breakdown`, `update`, `status`, `execute`, `validate` (defaults to `breakdown`)

## Implementation

When called with `/sp-task {{args}}`, I will:

### 1. Detect Current Feature Context

**I will identify the current working feature:**
- Check `.specpulse/memory/context.md` for active feature
- Look for most recently modified spec/plan/task directory
- Validate feature directory exists and is properly structured
- Extract feature ID and name from directory structure

### 2. Parse Arguments to Determine Action

**I will analyze the arguments:**
- If first argument is `breakdown`, `update`, `status`, `execute`, or `validate` → Use that action
- If no action specified → Default to `breakdown`
- For other arguments → Look for feature name or use current feature

### 3. For Action: breakdown (default)

**I will create comprehensive task breakdowns:**

#### A. Check for Service Decomposition
- Look for `.specpulse/specs/[feature]/decomposition/` directory
- If decomposition exists, identify service directories
- Parse service names for task categorization
- Plan service-specific task generation

#### B. Generate Task Breakdown
- Read implementation plan from `.specpulse/plans/[feature]/` directory
- Analyze plan phases and identify implementation steps
- Create detailed tasks with proper dependencies
- Assign task IDs using universal numbering system

#### C. Create Service-Specific Tasks
If decomposition exists:
- **Auth Service Tasks**: AUTH-T001, AUTH-T002, etc.
- **User Service Tasks**: USER-T001, USER-T002, etc.
- **Integration Tasks**: INT-T001, INT-T002, etc.

#### D. Generate Comprehensive Task Metadata
For each task, I will include:
- **Task ID**: Unique identifier with sequential numbering
- **Status**: Initially set to "todo"
- **Title**: Clear, actionable task description
- **Description**: Detailed "what, why, how, when" explanation
- **Files Touched**: List of files that will be modified
- **Goals**: Specific objectives this task achieves
- **Success Criteria**: Testable completion conditions
- **Dependencies**: Tasks that must be completed first
- **Next Tasks**: Tasks that can start after this one
- **Risk Level**: Assessment of potential issues (low/medium/high)
- **Risk Notes**: Specific concerns and mitigation strategies
- **MOSCOW Analysis**: Must/Should/Know/Won't categorization
- **Priority**: Overall priority ranking with reasoning
- **SDD Gates Compliance**: Specification-driven validation

### 4. For Action: update

**I will update existing task files:**
- Scan `.specpulse/tasks/[feature]/` directory for task files
- Display available task files for selection
- Parse current task structure and status
- Provide interactive update options:
  - Mark tasks as completed/in-progress/blocked
  - Update task descriptions or metadata
  - Add new tasks or remove obsolete ones
- Recalculate progress metrics after updates

### 5. For Action: status

**I will display comprehensive progress:**
- Scan all task files in current feature
- Calculate completion percentages
- Show progress by service (if decomposed)
- Display task status distribution:
  - Completed tasks count and percentage
  - In-progress tasks
  - Blocked tasks with blockers listed
  - Pending tasks available for work
- Show SDD Gates compliance status
- Calculate velocity metrics (tasks/day)
- Identify parallel tasks and sequential chains
- Provide recommendations for next actions

### 6. For Action: execute

**I will execute specific tasks:**
- Allow task selection from available pending tasks
- Validate task readiness and dependencies
- Display task details before execution
- Implement task requirements through code changes
- Test implementation when applicable
- Mark task as completed automatically
- Continue with next available task if requested
- Update progress metrics and context

### 7. For Action: validate

**I will perform comprehensive task validation:**
- Validate task file structure and format
- Check required fields are present and valid
- Verify task dependencies exist and are valid
- Validate SDD Gates compliance
- Check for duplicate task IDs
- Verify success criteria are testable
- Assess risk levels and mitigation strategies
- Report validation results with fixes needed

## Enhanced Task Generation

### Universal ID System

**I ensure conflict-free numbering through systematic analysis:**

#### A. Task ID Generation Algorithm
- **Use Glob tool** to scan `.specpulse/tasks/[feature]/` directory
- **Parse existing task files** to extract current numbering:
  - Global tasks: Extract numbers from `T###.md` patterns
  - Service tasks: Extract from `SERVICE-T###.md` patterns
  - Integration tasks: Extract from `INT-T###.md` patterns
- **Create numbering map**: `{task_type: max_number_used}`
- **Generate next ID**: For each task type, use `max_num + 1`
- **Zero-pad format**: `format(next_num, '03d')` ensures `001`, `002`, `003`

#### B. Service-Specific Task Patterns
- **Authentication Service**: `AUTH-T001.md`, `AUTH-T002.md`, etc.
- **User Management Service**: `USER-T001.md`, `USER-T002.md`, etc.
- **API Gateway Service**: `GATEWAY-T001.md`, `GATEWAY-T002.md`, etc.
- **Database Service**: `DB-T001.md`, `DB-T002.md`, etc.
- **Notification Service**: `NOTIF-T001.md`, `NOTIF-T002.md`, etc.

#### C. Conflict Prevention Mechanisms
- **Atomic file existence check** before creating each task file
- **Validation loop**: If conflict detected, increment and retry
- **Cross-service dependency tracking** to ensure logical numbering
- **Fallback numbering**: If directory empty, start from `T001.md`
- **Gap handling**: Preserve existing numbering gaps, don't renumber

### Service-Specific Task Organization

**For decomposed features:**
- **Authentication Service**: JWT, OAuth, password policies, session management
- **User Management Service**: Profiles, preferences, permissions, roles
- **API Gateway Service**: Rate limiting, authentication, routing, logging
- **Database Service**: Schema management, migrations, backups, optimization
- **Notification Service**: Email, SMS, push notifications, templates
- **Integration Tasks**: Service communication, data synchronization, API contracts

### SDD Gates Compliance

**Every generated task meets:**
- ✅ **Specification Traced**: Links to specific requirements
- ✅ **Task Decomposed**: Complex work broken into manageable pieces
- ✅ **Quality Assurance**: Success criteria are testable
- ✅ **Traceable Implementation**: Clear link between tasks and code

## Progress Tracking and Analytics

### Comprehensive Metrics

**I track detailed progress:**
- Total tasks and completion percentage
- Task status distribution (todo/in-progress/blocked/done)
- Velocity calculations (tasks per day)
- Estimated completion dates based on velocity
- Parallel task availability
- Sequential dependency chains
- SDD Gates compliance percentage

### Risk Assessment

**I identify and track risks:**
- High-risk tasks with mitigation strategies
- Dependency chain vulnerabilities
- Resource allocation issues
- Timeline bottlenecks
- Technical debt accumulation

## Example Outputs

### Task Breakdown Generation
```
User: /sp-task breakdown

🔍 Current feature: 002-auth-microservice
📋 Found decomposition: 3 services (auth, user, api-gateway)
🎯 Generating service-specific tasks...

✅ Created task files:
   📁 auth-service-tasks.md (8 tasks)
      AUTH-T001: Initialize auth service structure
      AUTH-T002: Implement JWT token handling
      AUTH-T003: Create password validation
      AUTH-T004: Design session management
      AUTH-T005: Implement OAuth2 integration
      AUTH-T006: Create token refresh mechanism
      AUTH-T007: Add multi-factor authentication
      AUTH-T008: Design auth API endpoints

   📁 user-service-tasks.md (6 tasks)
      USER-T001: Initialize user service structure
      USER-T002: Design user profile schema
      USER-T003: Implement user preferences
      USER-T004: Create role-based permissions
      USER-T005: Design user API endpoints
      USER-T006: Add user search functionality

   📁 integration-tasks.md (4 tasks)
      INT-T001: Connect auth and user services
      INT-T002: Design service communication protocol
      INT-T003: Implement user authentication flow
      INT-T004: Create cross-service data consistency

📊 Total: 18 tasks across 3 services
⚡ Parallel tasks available: 12
🔗 Sequential chains: 3
✅ SDD Gates compliant: 100%
```

### Task Status Display
```
User: /sp-task status

📊 Feature: 002-auth-microservice
============================================================
Overall Progress: 35% (6/17 tasks completed)

🔧 Service Tasks:
   Auth Service: 4/8 completed (50%)
      ✅ AUTH-T001: Initialize auth service structure
      ✅ AUTH-T002: Implement JWT token handling
      ✅ AUTH-T003: Create password validation
      ✅ AUTH-T004: Design session management
      🔄 AUTH-T005: Implement OAuth2 integration (in progress)
      ⏳ AUTH-T006: Create token refresh mechanism (pending)
      ⏳ AUTH-T007: Add multi-factor authentication (pending)
      ⏳ AUTH-T008: Design auth API endpoints (pending)

   User Service: 1/6 completed (17%)
      ✅ USER-T001: Initialize user service structure
      🔄 USER-T002: Design user profile schema (in progress)
      ⏳ 4 more tasks pending

   Integration: 1/4 completed (25%)
      ✅ INT-T001: Connect auth and user services
      ⏳ 3 more tasks pending

📋 SDD Gates Compliance:
   ✅ 15/17 tasks compliant
   ⚠️  2 tasks need specification traceability

🚀 Parallel Tasks Available: 8
⛓️  Sequential Dependencies: 2 active chains

⚡ Velocity: 2.0 tasks/day
📅 Est. Completion: 2025-01-22

🎯 Recommended Next Steps:
   1. Complete AUTH-T005 (OAuth2 integration) - in progress
   2. Start USER-T003 (user preferences) - can run in parallel
   3. Begin INT-T002 (service communication) - unblocked
```

### Task Execution
```
User: /sp-task execute AUTH-T005

🚀 Executing Task: AUTH-T005
📋 Title: Implement OAuth2 integration
📝 Description: Add OAuth2 authentication support for external providers...

🔍 Validation:
   ✅ Dependencies completed: AUTH-T001, AUTH-T002, AUTH-T003, AUTH-T004
   ✅ Specification traced: ✅ Linked to spec-002.md section 4.3
   ✅ Success criteria testable: ✅ 5 acceptance criteria defined
   ✅ Risk assessment: ✅ Medium risk with mitigation plan

🎯 Implementation Started:
   - Creating OAuth2 provider configurations...
   - Implementing authorization code flow...
   - Adding provider client management...
   - Creating token exchange mechanisms...
   - Adding provider-specific user mapping...

✅ Testing Completed:
   - Google OAuth integration: ✅ Working
   - GitHub OAuth integration: ✅ Working
   - Token exchange: ✅ Working
   - Error handling: ✅ Working
   - Security validation: ✅ Working

📊 Task AUTH-T005 completed successfully!
📈 Progress updated: 30% → 35%
⚡ Velocity: 2.5 tasks/day
```

## Error Handling and Recovery

### Validation Errors
- **No active feature**: Prompt to run `/sp-/sp-pulse` first
- **Missing plan file**: Guide user to create plan with `/sp-/sp-plan`
- **Invalid task format**: Identify and fix structural issues
- **Circular dependencies**: Detect and resolve dependency loops
- **Missing specifications**: Link tasks back to requirements

### Execution Issues
- **Task blockers**: Identify dependencies and provide resolution paths
- **Failed implementations**: Rollback changes and retry with different approach
- **Test failures**: Debug and fix implementation issues
- **Resource conflicts**: Reschedule tasks to avoid conflicts

This `/sp-task` command provides **complete task lifecycle management** without requiring any SpecPulse CLI installation, using only validated file operations and comprehensive project analytics.