# SpecPulse Examples

This directory contains example projects demonstrating how to use SpecPulse for different types of applications.

## Example Projects

### 1. E-Commerce Platform
A complete e-commerce platform specification showing:
- User authentication and authorization
- Product catalog management
- Shopping cart functionality
- Payment processing
- Order management

[View Example →](./ecommerce-platform/)

### 2. Todo App
A simple todo application demonstrating:
- Basic CRUD operations
- User interface design
- State management
- Local storage integration

[View Example →](./todo-app/)

### 3. API Service
A RESTful API service showcasing:
- Endpoint design
- Authentication strategies
- Rate limiting
- Documentation generation

[View Example →](./api-service/)

## Getting Started

Each example follows the SpecPulse workflow:

1. **Initialize**: Each project starts with `specpulse init`
2. **Specify**: Requirements defined in `specs/`
3. **Plan**: Implementation strategy in `plans/`
4. **Tasks**: Broken down work items in `tasks/`

## How to Use

1. Navigate to any example directory
2. Review the specification in `specs/001-feature/spec.md`
3. Check the implementation plan in `plans/001-feature/plan.md`
4. See task breakdown in `tasks/001-feature/tasks.md`

## Creating Your Own Project

Start with SpecPulse:

```bash
# Install SpecPulse
pip install specpulse

# Initialize your project
specpulse init my-project --ai claude

# Start with Claude or Gemini
/pulse my-feature
/spec create detailed requirements
/plan generate
/task breakdown
```

## Common Patterns

### Authentication Flow
```markdown
# specs/001-auth/spec.md
## Requirements
- Must have secure password storage
- Should support OAuth2
- Could have 2FA
```

### API Design
```markdown
# plans/001-api/plan.md
## Endpoints
- POST /api/auth/login
- GET /api/users/:id
- PUT /api/users/:id
```

### Task Management
```markdown
# tasks/001-feature/tasks.md
- [x] T001: [S] Setup project structure
- [ ] T002: [M] Implement authentication
- [ ] T003: [L] Add test coverage
```

## Contributing

To add a new example:
1. Create a new directory under `examples/`
2. Initialize with `specpulse init`
3. Add complete specifications, plans, and tasks
4. Update this README with the new example

## Resources

- [SpecPulse Documentation](https://github.com/specpulse/specpulse)
- [PyPI Package](https://pypi.org/project/specpulse/)
- [Constitution Principles](../memory/constitution.md)