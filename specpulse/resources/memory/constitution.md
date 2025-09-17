# Project Constitution
*Universal principles that enable Specification-Driven Development (SDD) for any software project*

## The Nine Universal SDD Principles

### 1. SPECIFICATION FIRST
**Rule:** Every feature starts with a clear specification.

**Requirements:**
- Define what you're building before how
- Include user stories and acceptance criteria
- Use [NEEDS CLARIFICATION] markers for unknowns
- Document functional and non-functional requirements

**Validation:** Can someone else understand what to build from this spec?

**Example:**
```markdown
# ✅ GOOD: Clear specification
## User Authentication
- Users can register with email and password
- [NEEDS CLARIFICATION]: OAuth2 provider list
- Password reset via email required

# ❌ BAD: Vague specification
"Make a login system that works"
```

### 2. INCREMENTAL PLANNING
**Rule:** Break specifications into manageable, phased plans.

**Requirements:**
- Create phase-based implementation plans
- Define clear milestones and checkpoints
- Prioritize features by business value
- Each phase should deliver working software

**Validation:** Is each phase independently valuable and deployable?

**Example:**
```markdown
# ✅ GOOD: Phased delivery
Phase 1: Core authentication (Week 1)
Phase 2: User profiles (Week 2)
Phase 3: Role management (Week 3)

# ❌ BAD: Everything at once
"Complete user management system in one sprint"
```

### 3. TASK DECOMPOSITION
**Rule:** Break plans into concrete, executable tasks.

**Requirements:**
- Create specific, actionable tasks with clear outcomes
- Estimate effort in hours or days
- Define "Definition of Done" for each task
- Include acceptance criteria

**Validation:** Could a developer pick this up and start immediately?

**Example:**
```markdown
# ✅ GOOD: Actionable task
T001: Implement user registration endpoint
- Effort: 4 hours
- Done: POST /api/users accepts and validates data
- Test: Registration creates user in database

# ❌ BAD: Vague task
"Do user stuff"
```

### 4. TRACEABLE IMPLEMENTATION
**Rule:** Every piece of code should trace back to a specification.

**Requirements:**
- Reference spec requirements in code comments
- Link commits to tasks and specs
- Update specs when requirements change
- Maintain bidirectional traceability

**Validation:** Can you trace this code to a specific requirement?

**Example:**
```markdown
# ✅ GOOD: Traceable implementation
- Commit message: "Implement user auth (SPEC-001, T003)"
- Code comment: "// Implements REQ-SEC-03: Password validation"
- PR description: Links to spec-001.md#security
- Task reference: T003 from task-001.md

# ❌ BAD: No traceability
- Commit: "Fixed stuff"
- No spec references in code
- No task linkage
```

### 5. CONTINUOUS VALIDATION
**Rule:** Validate implementation against specifications continuously.

**Requirements:**
- Check implementation matches spec after each task
- Run acceptance tests regularly
- Update specs if reality differs from plan
- Maintain spec-code synchronization

**Validation:** Does the current implementation match the specification?

**Example:**
```markdown
# ✅ GOOD: Regular validation
- After each task: Check against spec
- Daily: Run acceptance tests
- Weekly: Full spec review

# ❌ BAD: No validation
"We'll check at the end of the project"
```

### 6. QUALITY ASSURANCE
**Rule:** Ensure quality through appropriate testing and review.

**Requirements:**
- Test based on acceptance criteria
- Choose appropriate test types for your project
- Automate testing where valuable
- Conduct code reviews for critical features

**Validation:** Are all acceptance criteria verifiable and tested?

**Example:**
```markdown
# ✅ GOOD: Appropriate testing
- Unit tests for business logic
- Integration tests for APIs
- E2E tests for critical user flows

# ❌ BAD: No testing strategy
"We'll test manually"
```

### 7. ARCHITECTURE DOCUMENTATION
**Rule:** Document key architectural decisions and patterns.

**Requirements:**
- Record technology choices and rationale
- Document integration points and APIs
- Track technical debt and trade-offs
- Maintain architecture decision records (ADRs)

**Validation:** Will someone understand these decisions in 6 months?

**Example:**
```markdown
# ✅ GOOD: Documented decisions
ADR-001: Choose PostgreSQL over MongoDB
- Date: 2025-01-15
- Rationale: Need ACID transactions
- Trade-offs: Less flexible schema

# ❌ BAD: No documentation
"We just picked what we knew"
```

### 8. ITERATIVE REFINEMENT
**Rule:** Specifications and implementations evolve based on learnings.

**Requirements:**
- Update specs based on user feedback
- Refine based on implementation discoveries
- Version specifications for traceability
- Document lessons learned

**Validation:** Do specs reflect current reality and learnings?

**Example:**
```markdown
# ✅ GOOD: Learning from implementation
Spec v1: "Users login with email"
Spec v2: "Added: Support for username login (user feedback)"
Spec v3: "Added: MFA option (security review)"

# ❌ BAD: Never updating specs
"Original spec from 6 months ago"
```

### 9. STAKEHOLDER ALIGNMENT
**Rule:** Keep all stakeholders aligned through specifications.

**Requirements:**
- Share specs with team and clients
- Get approval before major phases
- Communicate changes clearly
- Maintain shared understanding

**Validation:** Does everyone understand what's being built and why?

**Example:**
```markdown
# ✅ GOOD: Clear communication
- Weekly spec reviews with team
- Client approval before each phase
- Documented change requests

# ❌ BAD: Working in isolation
"We'll show them when it's done"
```

## SDD Methodology Enforcement

### Phase Gates
Every implementation plan MUST pass through SDD compliance gates:

#### Phase -1: Pre-Implementation Gates
- [ ] Specification First: Requirements clear and documented?
- [ ] Incremental Planning: Work broken into valuable phases?
- [ ] Task Decomposition: Tasks concrete and actionable?
- [ ] Traceable Implementation: Code-to-spec mapping planned?
- [ ] Continuous Validation: Validation checkpoints defined?
- [ ] Quality Assurance: Test strategy appropriate?
- [ ] Architecture Documentation: Decision tracking planned?
- [ ] Iterative Refinement: Feedback loops established?
- [ ] Stakeholder Alignment: Communication plan in place?

### Decision Tracking
All significant architectural decisions and trade-offs MUST be documented:
```yaml
architectural_decisions:
  - decision: "Microservices for payment processing"
    rationale: "PCI compliance requires isolation"
    trade_offs: "Increased operational complexity"
    approved_by: "Team Lead"
    date: "2025-09-11"
    review_date: "2025-Q2"
```

### Amendment Process
While principles guide development, their application can evolve:

1. Proposed amendments require:
   - Explicit documentation of rationale
   - Impact assessment on existing code
   - Backwards compatibility analysis
   - Team consensus

2. Amendments are versioned and dated
3. Original principles remain visible with strikethrough
4. New principles are added with effective date

## Principles in Practice

### When Starting a New Feature
1. Write specification first (Principle 1)
2. Create phased plan (Principle 2)
3. Break into tasks (Principle 3)
4. Ensure traceability (Principle 4)
5. Set up validation (Principle 5)
6. Define quality strategy (Principle 6)
7. Document architecture (Principle 7)

### When Reviewing Code
- Does it trace to a specification? (Principle 4)
- Is testing appropriate? (Principle 6)
- Are decisions documented? (Principle 7)
- Has it been validated? (Principle 5)
- Are stakeholders aligned? (Principle 9)

### When Making Architectural Decisions
1. Document the decision and rationale
2. Get stakeholder approval for significant changes
3. Track in architecture decision records
4. Plan for future improvements

## Technical Standards

### Code Style Guidelines
- Follow language-specific best practices
- Use consistent formatting (Prettier, Black, etc.)
- Write self-documenting code
- Add meaningful comments where needed

### Testing Requirements
- Choose coverage appropriate for project risk
- Test based on acceptance criteria
- Critical features need comprehensive testing
- Use testing approach suitable for project type

### Project-Specific Standards
- Define standards appropriate for your project type
- Web apps: Response times, Core Web Vitals
- Mobile apps: Battery usage, offline capability
- Games: FPS targets, load times
- APIs: Throughput, latency percentiles

## Development Workflow

### SpecPulse Development Process
1. `specpulse init` - Initialize feature with proper structure
2. `/sp-spec` - Create specification following template guidelines
3. `/sp-plan` - Generate implementation plan with Phase Gates
4. `/sp-task` - Break down into executable tasks
5. Execute with Quality Assurance
6. `/sp-validate` - Validate against SDD principles and specification
7. Update specifications based on learnings

### Version Control
- Feature branches from specifications
- Semantic commit messages
- Specifications versioned with code
- Pull requests reference specifications

### Continuous Integration
- Specification validation on every commit
- SDD compliance checks in CI
- Appropriate test coverage for project type
- Architecture decision tracking

## Specification Quality Standards

### Completeness Requirements
- [ ] All user stories have acceptance criteria
- [ ] Non-functional requirements documented
- [ ] Edge cases identified
- [ ] Error scenarios defined
- [ ] Success metrics specified

### Clarity Requirements
- [ ] No ambiguous language
- [ ] [NEEDS CLARIFICATION] markers for unknowns
- [ ] Testable acceptance criteria
- [ ] Measurable success metrics
- [ ] Clear scope boundaries

### Traceability Requirements
- [ ] Requirements numbered for reference
- [ ] User stories linked to requirements
- [ ] Tests trace to acceptance criteria
- [ ] Implementation maps to specifications
- [ ] Changes documented in specification

## Living Constitution
This constitution is a living document that learns from experience while maintaining core principles. Each project iteration strengthens these principles through practical application and refinement.

*Last Updated: 2025-09-11*
*Version: 2.0 - Full SDD Methodology Implementation*