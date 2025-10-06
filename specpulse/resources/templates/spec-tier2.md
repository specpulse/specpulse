# Specification: {{feature_name}}

---
tier: standard
progress: 0.0
sections_completed: []
sections_partial: []
last_updated: {{date}}
---

## What

<!-- LLM GUIDANCE: Same as Tier 1 - keep it to ONE sentence -->

[One sentence: What does this feature do?]

---

## Why

<!-- LLM GUIDANCE: Same as Tier 1 - keep it to ONE sentence -->

[One sentence: Why is this feature needed?]

---

## Done When

<!-- LLM GUIDANCE: Same as Tier 1 - list 3 testable acceptance criteria -->

- [ ] [First acceptance criterion]
- [ ] [Second acceptance criterion]
- [ ] [Third acceptance criterion]

---

## User Stories

<!-- LLM GUIDANCE:
Write 3-5 user stories in standard format.

Format:
**As a** [type of user]
**I want** [action/capability]
**So that** [benefit/value]

Each story should have 2-4 acceptance criteria.

Examples (GOOD):
**As a** registered user
**I want** to reset my password via email
**So that** I can regain access if I forget my credentials

**Acceptance Criteria:**
- [ ] Password reset link sent within 1 minute
- [ ] Link expires after 24 hours
- [ ] New password meets security requirements
- [ ] User receives confirmation after successful reset

Examples (BAD):
**As a** user
**I want** authentication
**So that** security
(Too vague - no specific action or benefit)

Think: WHO needs this? WHAT do they want to do? WHY does it matter?
Count: 3-5 stories recommended
Focus: Cover main user workflows, not every edge case
-->

### Story 1: [Title describing the user action]

**As a** [type of user]
**I want** [action/capability]
**So that** [benefit/value]

**Acceptance Criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

### Story 2: [Title]

**As a** [type of user]
**I want** [action/capability]
**So that** [benefit/value]

**Acceptance Criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

### Story 3: [Title]

**As a** [type of user]
**I want** [action/capability]
**So that** [benefit/value]

**Acceptance Criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

---

## Functional Requirements

<!-- LLM GUIDANCE:
List 5-8 specific, testable requirements using FR-XXX numbering.

Format:
**FR-XXX**: [Requirement statement]
- **Acceptance**: [How to verify]
- **Priority**: MUST | SHOULD | COULD

Priority guide:
- MUST: Critical for MVP, feature broken without it
- SHOULD: Important but feature works without it
- COULD: Nice to have, low priority

Examples (GOOD):
**FR-001**: Users can log in with email and password
- **Acceptance**: Successful login redirects to dashboard, invalid credentials show error
- **Priority**: MUST

**FR-002**: System locks account after 5 failed login attempts
- **Acceptance**: 6th attempt blocked, unlock email sent after 15 minutes
- **Priority**: SHOULD

Examples (BAD):
**FR-001**: Implement authentication
- **Acceptance**: Authentication works
- **Priority**: MUST
(Too vague - what KIND of auth? How verify?)

Think: WHAT must the system do? (not HOW)
Count: 5-8 requirements (fewer is better than bloat)
Focus: Concrete capabilities, not implementation details
-->

**FR-001**: [Requirement statement - what system must do]
- **Acceptance**: [How to verify this works]
- **Priority**: MUST | SHOULD | COULD

**FR-002**: [Requirement statement]
- **Acceptance**: [How to verify this works]
- **Priority**: MUST | SHOULD | COULD

**FR-003**: [Requirement statement]
- **Acceptance**: [How to verify this works]
- **Priority**: MUST | SHOULD | COULD

**FR-004**: [Requirement statement]
- **Acceptance**: [How to verify this works]
- **Priority**: MUST | SHOULD | COULD

**FR-005**: [Requirement statement]
- **Acceptance**: [How to verify this works]
- **Priority**: MUST | SHOULD | COULD

---

## Technical Approach

<!-- LLM GUIDANCE:
Describe the HIGH-LEVEL architecture and technology choices.

Include:
- Architecture style (monolithic, microservices, serverless, etc.)
- Key technologies (languages, frameworks, databases)
- Integration points (APIs, services, third-party)
- Data flow (high-level - don't design database schema here)

Length: 2-4 paragraphs

Examples (GOOD):
"We'll implement a REST API using Node.js and Express, with JWT tokens for stateless authentication. User credentials will be hashed with bcrypt and stored in PostgreSQL. The API will integrate with SendGrid for password reset emails."

"This will be a React SPA with TypeScript, calling backend APIs. State management via Redux Toolkit. Real-time updates using WebSocket connection to backend server."

Examples (BAD):
"We'll use the best technologies available and follow industry standards."
(Too vague)

"Authentication will use OAuth2 with PKCE flow, JWT access tokens with 15-minute expiry, refresh tokens in httpOnly cookies with 7-day sliding expiration, Redis for session storage with LRU eviction..."
(Too detailed - save for implementation planning)

Think: What's the overall approach? What big decisions need to be made?
Keep it high-level: Details come later in planning
-->

[2-4 paragraphs describing the technical approach:
- Architecture style
- Key technologies
- Integration points
- Data flow
]

---

## API Design

<!-- LLM GUIDANCE:
List the main API endpoints or interfaces this feature exposes.

Format (REST API):
- **POST /api/resource** - Create new resource
- **GET /api/resource/:id** - Get single resource
- **PUT /api/resource/:id** - Update resource
- **DELETE /api/resource/:id** - Delete resource

Format (GraphQL):
- **mutation createResource** - Create new resource
- **query getResource(id)** - Fetch single resource

Format (Function/Method):
- **authenticateUser(email, password)** → User | Error
- **sendPasswordReset(email)** → Success | Error

Include:
- HTTP method and path (for REST)
- Brief description
- Key request parameters
- Expected response

Examples (GOOD):
**POST /api/auth/login**
- Request: `{ email, password }`
- Response: `{ token, user: { id, email, name } }`
- Errors: 401 Unauthorized, 400 Bad Request

**GET /api/users/:id**
- Request: No body (requires auth token in header)
- Response: `{ user: { id, email, name, createdAt } }`
- Errors: 401 Unauthorized, 404 Not Found

Examples (BAD):
**POST /api/auth**
- Does authentication stuff
(Too vague - login? logout? register?)

Think: What endpoints will other systems or the frontend call?
Count: 3-7 main endpoints (don't list every CRUD operation)
Focus: Public interface, not internal implementation
-->

### Main Endpoints

**[METHOD] /api/path**
- **Description**: [What this endpoint does]
- **Request**: `{ field1, field2 }`
- **Response**: `{ data }` or `{ error }`
- **Auth**: Required | Not required
- **Errors**: 400, 401, 404, 500

**[METHOD] /api/path/:id**
- **Description**: [What this endpoint does]
- **Request**: [Request format]
- **Response**: [Response format]
- **Auth**: Required | Not required
- **Errors**: [Common error codes]

---

## Dependencies

<!-- LLM GUIDANCE:
List what this feature depends on to work.

Categories:
1. Internal dependencies (other features, services, modules)
2. External dependencies (third-party APIs, services, libraries)
3. Infrastructure dependencies (databases, message queues, storage)

Format:
**[Dependency Name]**: [Why needed]

Examples (GOOD):
**User Service**: Required to fetch user profiles and permissions
**SendGrid API**: Required to send password reset emails
**PostgreSQL**: Required to store user credentials and sessions
**Redis**: Required for rate limiting (optional - can fall back to in-memory)

Examples (BAD):
**Node.js**: Runtime environment
**Express**: Web framework
(These are technology choices, not dependencies)

**The internet**: Required to work
(Too obvious)

Think: What MUST exist for this to work? What external systems do we call?
Count: 2-6 dependencies typical
Mark optional dependencies clearly
-->

### Internal Dependencies
- **[Feature/Service]**: [Why needed]

### External Dependencies
- **[API/Service]**: [Why needed]
- **[Library/Tool]**: [Why needed]

### Infrastructure
- **[Database/Queue/Storage]**: [Why needed]

---

## Risks and Mitigations

<!-- LLM GUIDANCE:
Identify 2-4 major risks and how to mitigate them.

Format:
**[Risk]**: [Description]
- **Impact**: High | Medium | Low
- **Likelihood**: High | Medium | Low
- **Mitigation**: [How to reduce risk]

Examples (GOOD):
**Third-party API downtime**: SendGrid outage prevents password reset emails
- **Impact**: High (users locked out)
- **Likelihood**: Low (99.9% uptime SLA)
- **Mitigation**: Queue failed emails for retry, provide support contact option

**Performance degradation**: Bcrypt hashing slows login under high load
- **Impact**: Medium (slow but functional)
- **Likelihood**: Medium (during peak hours)
- **Mitigation**: Use work factor 10 (not 12), consider Redis caching for repeat logins

Examples (BAD):
**Bugs in code**: Code might have bugs
- **Impact**: Unknown
- **Likelihood**: Unknown
- **Mitigation**: Test everything
(Too vague - every project has bugs)

Think: What could go wrong? What's the plan if it does?
Count: 2-4 real risks (not hypothetical disasters)
Focus: Risks specific to THIS feature
-->

**[Risk Name]**: [Description of what could go wrong]
- **Impact**: High | Medium | Low
- **Likelihood**: High | Medium | Low
- **Mitigation**: [Specific plan to reduce or handle risk]

---

## Next Steps

<!--
This is a STANDARD tier specification (Tier 2 of 3).
You have enough detail to start planning implementation.

Next actions:
1. Generate implementation plan:
   Command: /sp-plan

2. Expand to COMPLETE tier if this is production-critical:
   Command: specpulse expand {{feature_id}} --to-tier complete
   (Adds: Security, Performance, Monitoring, Compliance, Cost Analysis)

3. Add individual sections if needed:
   Command: specpulse spec add-section {{feature_id}} <section-name>

Check your progress:
   Command: specpulse spec progress {{feature_id}}
-->

**Current Tier**: Standard (7-8 sections)
**Time to Complete**: 10-15 minutes
**Ready for Planning**: ✓ Yes

💡 **Tip**: Most features work well at Standard tier. Only expand to Complete if you need production-grade detail (security audits, compliance, etc.)
