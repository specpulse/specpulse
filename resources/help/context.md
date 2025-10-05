# Context Management (v1.7.0)

## Overview

Project context stores tech stack, team preferences, and project metadata. Context is automatically injected into AI scripts to reduce repetitive questions.

## Project Context Structure

```yaml
project:
  name: MyApp
  type: web-app
  description: E-commerce platform
  version: 1.0.0

tech_stack:
  frontend: React, TypeScript, Tailwind CSS
  backend: Node.js, Express
  database: PostgreSQL
  cache: Redis
  message_queue: RabbitMQ

team_size: 1

preferences:
  - Functional components over class components
  - Prefer composition over inheritance
  - Always include loading states
```

## Commands

### Set Context Variable

```bash
# Set tech stack
specpulse context set tech_stack.frontend "React, TypeScript"
specpulse context set tech_stack.backend "Node.js, Express"
specpulse context set tech_stack.database "PostgreSQL"

# Set project info
specpulse context set project.name "MyApp"
specpulse context set project.type "web-app"

# Set team size
specpulse context set team_size 3
```

### Get Context Variable

```bash
# Get all context
specpulse context get

# Get specific value
specpulse context get tech_stack.frontend
# Output: React, TypeScript

# Get entire tech stack
specpulse context get tech_stack
```

### Auto-Detect Tech Stack

```bash
# Scan package files and detect tech stack
specpulse context auto-detect
```

Detects from:
- `package.json` → React, Vue, Angular, Express, Next.js
- `pyproject.toml` → FastAPI, Django, Flask
- `go.mod` → Go
- `Gemfile` → Ruby, Rails
- `composer.json` → PHP, Laravel

### Inject Context

```bash
# General context
specpulse context inject

# Feature-specific context
specpulse context inject --feature 001
```

Outputs HTML comment block ready for copy-paste into templates.

## Context Injection

### What Gets Injected

Context blocks include:
- Project name and type
- Tech stack (frontend | backend | database)
- Recent decisions (last 3)
- Active patterns (last 3)

### Format

```html
<!-- SPECPULSE CONTEXT -->
Project: MyApp (web-app)
Tech Stack: React, TypeScript | Node.js, Express | PostgreSQL
Recent Decisions:
  - DEC-001: Use Stripe for payments (2024-10-06)
  - DEC-002: PostgreSQL for database (2024-10-05)
Patterns:
  - PATTERN-001: API Error Format
  - PATTERN-002: Loading States
<!-- END SPECPULSE CONTEXT -->
```

### Size Limit

Context is limited to 500 characters (plus HTML tags) to avoid overwhelming AI prompts.

## Automatic Injection

Context is automatically injected by `/sp-*` scripts:
- `/sp-pulse` → General context
- `/sp-spec` → Feature-specific context with patterns
- `/sp-plan` → Context with architectural decisions
- `/sp-task` → Context with patterns and constraints
- `/sp-decompose` → Context with architectural patterns

## Workflow

```bash
# Initial setup
specpulse context set project.name "MyApp"
specpulse context set tech_stack.frontend "React"
specpulse context set tech_stack.backend "Node.js"

# Or use auto-detect
specpulse context auto-detect

# Add architectural decision
specpulse memory add-decision "Use REST over GraphQL" \
  --rationale "Simpler, better caching"

# Create new feature (context auto-injected!)
/sp-pulse user-authentication
# AI sees context automatically, doesn't ask about tech stack!
```

## Storage

- **File**: `.specpulse/project_context.yaml`
- **Format**: YAML (human-editable)
- **Git**: Track in version control for team sharing
