# SpecPulse Usage Guide

## What is SpecPulse?

SpecPulse is a universal Specification-Driven Development (SDD) framework that works with ANY software project - web apps, mobile apps, games, desktop software, APIs, ML projects, and more. It ensures every feature starts with clear specifications, validated plans, and tracked tasks, regardless of your technology stack.

## Getting Started

### Installation

```bash
pip install specpulse
```

### Initialize Your Project

```bash
# Create new project
specpulse init my-project

# Or initialize in current directory
specpulse init --here
```

## Core Workflow

SpecPulse follows a strict progression:

```
Specification → Plan → Task → Execute
```

### Step 1: Create a Feature Specification

In your AI assistant (Claude/Gemini), use:

```bash
/sp-pulse authentication
/sp-spec
```

This creates:
- `specs/001-authentication/spec-001.md`

### Step 2: Generate Implementation Plan

```bash
/sp-plan
```

This creates:
- `plans/001-authentication/plan-001.md`

### Step 3: Break Down into Tasks

```bash
/sp-task
```

This creates:
- `tasks/001-authentication/task-001.md`

### Step 4: Execute Tasks

```bash
/sp-execute all
```

This executes all tasks continuously without stopping.

## How to Break Your Project into Features (Pulses)

### Understanding Feature Boundaries

A feature in SpecPulse is called a "pulse". Each pulse should be:
- **Independent**: Can be developed and tested separately
- **Complete**: Provides a full piece of functionality
- **Sized Right**: Not too large (max 10 tasks) or too small (min 3 tasks)

### Example: E-Commerce Platform

Here's how to break down an e-commerce platform into pulses:

```
001-user-authentication
- User registration
- Login/logout
- Password reset
- Session management

002-product-catalog
- Product CRUD operations
- Category management
- Search and filtering
- Product images

003-shopping-cart
- Add/remove items
- Update quantities
- Cart persistence
- Price calculation

004-payment-processing
- Payment gateway integration
- Order creation
- Transaction handling
- Receipt generation

005-order-management
- Order history
- Status tracking
- Cancellations
- Refunds
```

### Example: Social Media Application

```
001-user-profiles
- Profile creation
- Profile editing
- Avatar upload
- Privacy settings

002-content-posting
- Create posts
- Edit/delete posts
- Media attachments
- Drafts

003-social-interactions
- Like/unlike
- Comments
- Shares
- Mentions

004-friend-system
- Send requests
- Accept/decline
- Block users
- Friend lists

005-notifications
- Real-time alerts
- Email notifications
- Notification preferences
- Mark as read
```

### Example: Project Management Tool

```
001-workspace-management
- Create workspaces
- Invite members
- Role management
- Settings

002-project-creation
- Project templates
- Project details
- Team assignment
- Milestones

003-task-management
- Create tasks
- Assign tasks
- Due dates
- Status updates

004-collaboration
- Comments
- File attachments
- Activity feed
- @mentions

005-reporting
- Progress charts
- Time tracking
- Export reports
- Analytics
```

## Feature Decomposition Guidelines

### When to Create a New Pulse

Create a new pulse when:
- The functionality serves a distinct user need
- It can be tested independently
- It has its own data models
- It could potentially be a microservice

### When to Keep in Same Pulse

Keep in the same pulse when:
- Features are tightly coupled
- They share the same data models
- One cannot work without the other
- They form a logical unit

### Sizing Guidelines

| Pulse Size | Tasks | Development Time | When to Use |
|------------|-------|------------------|-------------|
| Small | 3-5 | 1-2 days | Simple CRUD, basic features |
| Medium | 6-10 | 3-5 days | Standard features with some complexity |
| Large | 11-15 | 1-2 weeks | Complex features (consider decomposing) |
| Too Large | >15 | >2 weeks | Must decompose into multiple pulses |

## Naming Conventions

### Pulse Naming

Format: `XXX-feature-name`

```
001-user-authentication
002-payment-gateway
003-admin-dashboard
```

### Why Sequential Numbers?
- Provides natural ordering
- Shows development sequence
- Helps track progress
- Enables easy reference

## Universal SDD Principles

Every project using SpecPulse follows these 9 principles:

1. **Specification First**: Start with clear requirements and acceptance criteria
2. **Incremental Planning**: Break work into valuable, deployable phases
3. **Task Decomposition**: Create concrete tasks with clear outcomes
4. **Traceable Implementation**: Link all code to specifications
5. **Continuous Validation**: Verify spec-implementation alignment
6. **Quality Assurance**: Apply appropriate testing for your project type
7. **Architecture Documentation**: Record and justify technical decisions
8. **Iterative Refinement**: Evolve based on feedback and learnings
9. **Stakeholder Alignment**: Maintain shared understanding

These principles work for ANY project:
- ✅ Web applications (React, Vue, Angular)
- ✅ Mobile apps (iOS, Android, Flutter, React Native)
- ✅ Desktop software (Electron, Qt, WPF)
- ✅ Games (Unity, Unreal, Godot)
- ✅ APIs (REST, GraphQL, gRPC)
- ✅ ML/AI projects
- ✅ Embedded systems
- ✅ Blockchain applications

## Advanced Features

### Microservice Decomposition

For complex features, use decomposition:

```bash
/sp-decompose 001
```

This creates:
- Service boundaries
- API contracts
- Integration plans
- Service-specific tasks (AUTH-T001, USER-T001)

### Continuous Execution

Execute all tasks without interruption:

```bash
/sp-execute all
```

Benefits:
- No context switching
- 10x faster completion
- Maintains flow state
- Automatic progression

## Best Practices

### DO's
- ✅ Start with clear feature boundaries
- ✅ Keep pulses independent
- ✅ Validate after each pulse
- ✅ Use continuous execution
- ✅ Document decisions in `memory/decisions.md`

### DON'Ts
- ❌ Create pulses larger than 15 tasks
- ❌ Mix unrelated functionality
- ❌ Skip specifications
- ❌ Implement without plans
- ❌ Violate SDD principles

## Command Reference

### CLI Commands
```bash
sp init [project]        # Initialize project
sp validate             # Validate structure
sp doctor              # Run diagnostics
sp sync                # Sync state
sp decompose [id]      # Decompose feature
```

### AI Commands (Claude/Gemini)
```bash
/sp-pulse [name]       # Start new feature
/sp-spec              # Create specification
/sp-plan              # Generate plan
/sp-task              # Create tasks
/sp-execute           # Execute next task
/sp-execute all       # Execute all tasks
/sp-decompose [id]    # Decompose to microservices
```

## Project Structure

```
my-project/
├── specs/              # Feature specifications
│   └── 001-feature/
│       └── spec-001.md
├── plans/              # Implementation plans
│   └── 001-feature/
│       └── plan-001.md
├── tasks/              # Task breakdowns
│   └── 001-feature/
│       └── task-001.md
├── memory/             # Project memory
│   ├── constitution.md
│   ├── context.md
│   └── decisions.md
├── templates/          # Custom templates
└── scripts/            # Automation scripts
```

## Troubleshooting

### Common Issues

**Issue**: Feature too large to manage
**Solution**: Decompose using `/sp-decompose`

**Issue**: Tasks taking too long
**Solution**: Break down into smaller tasks

**Issue**: Dependencies between pulses
**Solution**: Complete dependent pulse first

**Issue**: Specification incomplete
**Solution**: Look for [NEEDS CLARIFICATION] markers

## Success Metrics

Track your progress with:
- Number of completed pulses
- Average tasks per pulse
- Time per pulse
- Test coverage per pulse
- SDD compliance score

## Conclusion

SpecPulse transforms chaotic development into a structured, predictable process. By breaking your project into well-defined pulses and following the specification-driven approach, you'll deliver higher quality software faster and with fewer errors.

Remember: **Specification → Plan → Task → Execute**. Always in that order.