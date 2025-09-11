<!-- SpecPulse Task List Template v2.0 -->
<!-- AI Instructions: Generate from implementation plan -->

# Task List: [FEATURE_NAME]

## Metadata
- **Plan Reference**: [PLAN_ID]
- **Total Tasks**: [COUNT]
- **Estimated Duration**: [TOTAL_HOURS]
- **Parallel Groups**: [COUNT]

## Task Organization

### Parallel Group A
*These tasks can be executed simultaneously*

#### T001: [Task Name]
- **Type**: [setup|development|testing|documentation]
- **Priority**: [HIGH|MEDIUM|LOW]
- **Estimate**: [hours]
- **Dependencies**: None
- **Description**: [What needs to be done]
- **Acceptance**: [How to verify completion]
- **Files**: [List of files to be created/modified]
- **Assignable**: [role/skill required]

#### T002: [Task Name]
[Same structure as above]

### Sequential Tasks
*These tasks must be completed in order*

#### T003: [Task Name]
- **Dependencies**: T001
[Rest of structure]

### Critical Path
*Tasks that directly impact timeline*

1. T001 → T003 → T007
2. Estimated critical path duration: [hours]

## Task Details

### Setup Tasks (T001-T009)
- [ ] T001: Initialize project structure
- [ ] T002: Install dependencies
- [ ] T003: Configure development environment
- [ ] T004: Setup database
- [ ] T005: Configure CI/CD

### Test Tasks [P] (T010-T019)
- [ ] T010: Write unit tests for [component]
- [ ] T011: Write integration tests for [feature]
- [ ] T012: Write E2E tests for user flow
- [ ] T013: Performance test setup

### Development Tasks (T020-T049)
- [ ] T020: Implement [component]
- [ ] T021: Create [feature]
- [ ] T022: Integrate [service]

### Integration Tasks (T050-T059)
- [ ] T050: Connect to database
- [ ] T051: Integrate external APIs
- [ ] T052: Setup middleware

### Polish Tasks [P] (T060-T069)
- [ ] T060: Documentation
- [ ] T061: Performance optimization
- [ ] T062: Security hardening
- [ ] T063: Deployment preparation

## Execution Schedule

### Day 1-2
- Morning: T001, T002, T003 (parallel)
- Afternoon: T004, T005

### Day 3-4
- Morning: T010-T013 (parallel, TDD)
- Afternoon: T020, T021

### Day 5-6
- Full days: T022-T049 (development sprint)

### Day 7
- Morning: T050-T052 (integration)
- Afternoon: T060-T063 (polish, parallel)

## Progress Tracking
```yaml
status:
  total: [count]
  completed: 0
  in_progress: 0
  blocked: 0
  
metrics:
  velocity: [tasks/day]
  estimated_completion: [date]
  blockers: []
  
parallel_groups:
  - name: "Setup"
    tasks: [T001, T002, T003]
    can_start: immediately
  - name: "Tests"
    tasks: [T010, T011, T012, T013]
    can_start: after_setup
  - name: "Polish"
    tasks: [T060, T061, T062, T063]
    can_start: after_development
```

## Task Execution Commands

### For parallel tasks:
```bash
# Execute multiple [P] tasks simultaneously
parallel_tasks="T001 T002 T003"
for task in $parallel_tasks; do
    echo "Starting $task in parallel..."
    # Execute task
done
```

### For sequential tasks:
```bash
# Execute tasks in order
sequential_tasks="T004 T005 T020"
for task in $sequential_tasks; do
    echo "Executing $task..."
    # Execute task
    # Wait for completion before next
done
```

## Notes
- Tasks marked with [P] can be executed in parallel
- Update progress tracking after each task completion
- If blocked, document reason and mitigation
- Adjust estimates based on actual velocity