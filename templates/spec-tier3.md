# Specification: {{feature_name}}

---
tier: complete
progress: 0.0
sections_completed: []
sections_partial: []
last_updated: {{date}}
---

## What

<!-- LLM GUIDANCE: Same as Tier 1 & 2 - ONE sentence -->

[One sentence: What does this feature do?]

---

## Why

<!-- LLM GUIDANCE: Same as Tier 1 & 2 - ONE sentence -->

[One sentence: Why is this feature needed?]

---

## Done When

<!-- LLM GUIDANCE: Same as Tier 1 & 2 - 3 testable acceptance criteria -->

- [ ] [First acceptance criterion]
- [ ] [Second acceptance criterion]
- [ ] [Third acceptance criterion]

---

## User Stories

<!-- LLM GUIDANCE: Same as Tier 2 - 3-5 user stories -->

### Story 1: [Title]

**As a** [type of user]
**I want** [action/capability]
**So that** [benefit/value]

**Acceptance Criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

---

## Functional Requirements

<!-- LLM GUIDANCE: Same as Tier 2 - 5-8 requirements with FR-XXX numbering -->

**FR-001**: [Requirement statement]
- **Acceptance**: [How to verify]
- **Priority**: MUST | SHOULD | COULD

---

## Technical Approach

<!-- LLM GUIDANCE: Same as Tier 2 - HIGH-LEVEL architecture, 2-4 paragraphs -->

[Technical approach description]

---

## API Design

<!-- LLM GUIDANCE: Same as Tier 2 - Main endpoints/interfaces -->

### Main Endpoints

**[METHOD] /api/path**
- **Description**: [What this does]
- **Request**: [Request format]
- **Response**: [Response format]
- **Auth**: Required | Not required

---

## Dependencies

<!-- LLM GUIDANCE: Same as Tier 2 - Internal, External, Infrastructure -->

### Internal Dependencies
- **[Feature/Service]**: [Why needed]

### External Dependencies
- **[API/Service]**: [Why needed]

### Infrastructure
- **[Database/Queue]**: [Why needed]

---

## Risks and Mitigations

<!-- LLM GUIDANCE: Same as Tier 2 - 2-4 major risks -->

**[Risk Name]**: [Description]
- **Impact**: High | Medium | Low
- **Likelihood**: High | Medium | Low
- **Mitigation**: [Plan]

---

## Security Considerations

<!-- LLM GUIDANCE:
Production-grade security analysis.

Cover these areas:
1. **Authentication**: How users prove identity
2. **Authorization**: Who can access what
3. **Data Protection**: Encryption, PII handling
4. **Input Validation**: Prevent injection attacks
5. **Threat Model**: What attacks are possible

Examples (GOOD):
**Authentication**: JWT tokens with 15-minute expiry, httpOnly refresh tokens
**Authorization**: Role-based access control (RBAC) - admin, user, guest roles
**Data Protection**: Passwords hashed with bcrypt (work factor 10), PII encrypted at rest with AES-256
**Input Validation**: All inputs sanitized, parameterized queries prevent SQL injection
**Threat Model**: Main risks are credential stuffing (mitigated by rate limiting) and session hijacking (mitigated by short token expiry)

Examples (BAD):
**Security**: We'll follow security best practices
(Too vague - WHICH practices?)

Think: What could an attacker do? How do we prevent it?
Length: 1-2 paragraphs covering the 5 areas
Be specific: Name actual technologies and techniques
-->

### Authentication & Authorization
[How users authenticate and what they can access]

### Data Protection
[How sensitive data is protected - encryption, hashing, PII handling]

### Input Validation & Threat Model
[How we prevent attacks - injection, XSS, CSRF, etc.]

---

## Performance Requirements

<!-- LLM GUIDANCE:
Define measurable performance targets.

Categories:
1. **Response Time**: How fast should API calls be?
2. **Throughput**: How many requests per second?
3. **Resource Usage**: Memory, CPU, disk limits
4. **Data Limits**: Max file size, record count, etc.

Format:
- **[Metric]**: [Target] under [conditions]

Examples (GOOD):
- **API Response Time**: < 200ms (p95) for read operations, < 500ms (p95) for writes
- **Throughput**: Support 1000 concurrent users, 10,000 requests/minute
- **Database Queries**: < 100ms (p95), max 3 queries per request
- **Memory**: < 512MB per instance under normal load
- **File Upload**: Max 10MB per file, 50MB per request

Examples (BAD):
- **Performance**: Should be fast
- **Scalability**: Should scale well
(Not measurable)

Think: What performance do users expect? What's acceptable?
Include: p50, p95, p99 targets (not just averages)
Be realistic: Based on technology choices and constraints
-->

### Response Time
- **[Operation]**: [Target latency] under [load conditions]

### Throughput
- **[Metric]**: [Target requests/sec] with [concurrent users]

### Resource Usage
- **[Resource]**: [Max usage] under [conditions]

---

## Monitoring & Alerts

<!-- LLM GUIDANCE:
Define what to monitor and when to alert.

Categories:
1. **Key Metrics**: What to track (dashboards)
2. **Health Checks**: How to know system is working
3. **Alert Rules**: When to page someone
4. **SLOs**: Service Level Objectives (uptime, latency)

Format:
**[Metric]**: [What to track]
- **Dashboard**: [Where to view]
- **Alert**: [When to fire] → [Who to notify]

Examples (GOOD):
**Login Success Rate**: Track % successful vs failed logins
- **Dashboard**: Auth dashboard, updated every 5 minutes
- **Alert**: < 95% success rate for 5 minutes → Page on-call engineer
- **SLO**: 99% success rate over 30 days

**API Response Time**: Track p50, p95, p99 latency
- **Dashboard**: Performance dashboard, real-time
- **Alert**: p95 > 1 second for 5 minutes → Slack #engineering
- **SLO**: p95 < 500ms for 99% of requests

**Error Rate**: Track 5xx errors per minute
- **Dashboard**: Error dashboard with breakdown by endpoint
- **Alert**: > 10 errors/minute → Page on-call, > 1% error rate → Slack
- **SLO**: < 0.1% error rate over 30 days

Examples (BAD):
**Monitor everything**: Track all the metrics
(Too vague)

**Alert on any error**: Send alert for every 500 error
(Alert fatigue - will be ignored)

Think: What indicates the system is healthy vs broken?
Focus: 3-5 KEY metrics (not everything)
Alerts: Only actionable issues worth waking someone up
-->

### Key Metrics
**[Metric Name]**: [What to measure]
- **Dashboard**: [Where to view it]
- **Alert Rule**: [When to alert] → [Who/where]
- **SLO**: [Service level objective]

---

## Rollback Strategy

<!-- LLM GUIDANCE:
Define how to safely rollback if deployment fails.

Include:
1. **Deployment Method**: Blue/green, canary, rolling, etc.
2. **Rollback Trigger**: What indicates deployment failure
3. **Rollback Process**: Steps to revert
4. **Data Migrations**: How to handle schema changes
5. **Rollback Time**: How long does rollback take

Examples (GOOD):
**Deployment**: Blue/green deployment with 10-minute soak period
**Triggers**: Error rate > 1%, p95 latency > 2x baseline, manual rollback command
**Process**:
1. Stop routing traffic to new version (30 seconds)
2. Route all traffic back to old version
3. Keep new version running for 1 hour for debugging
4. Total rollback time: < 2 minutes

**Data Migrations**: Use backward-compatible schema changes only
- Add new columns as nullable
- Keep old columns until next release
- Run data migration in background, not during deploy

**Zero-Downtime**: Keep both versions running, seamless cutover

Examples (BAD):
**Rollback**: Git revert and redeploy
(Too slow - what about downtime? data?)

Think: How quickly can we undo a bad deploy?
Critical: Database migrations - can they be reversed?
Goal: < 5 minutes to rollback, zero data loss
-->

### Deployment Method
[Blue/green, canary, rolling, etc.]

### Rollback Triggers
[What indicates we should rollback]

### Rollback Process
[Step-by-step revert process]

### Data Migration Strategy
[How to handle schema changes safely]

---

## Operational Runbook

<!-- LLM GUIDANCE:
Document how to operate and troubleshoot this feature.

Include:
1. **Common Issues**: Problems and solutions
2. **Debug Steps**: How to investigate issues
3. **Support Escalation**: When to escalate, to whom
4. **Maintenance Tasks**: Regular upkeep needed

Examples (GOOD):
**Users can't log in**:
1. Check auth service status: `kubectl get pods -n auth`
2. Check database connectivity: `psql -h db.example.com -U auth_user`
3. Review recent logins: `SELECT * FROM audit_log WHERE created_at > NOW() - INTERVAL '1 hour'`
4. Check for rate limiting: Redis key `rate_limit:login:{user_id}`
5. Escalate to: #auth-team if issue persists > 15 minutes

**High API latency**:
1. Check database slow query log: `SELECT * FROM pg_stat_statements ORDER BY mean_time DESC`
2. Check Redis connection pool: `INFO stats` in Redis CLI
3. Check for long-running transactions: `SELECT * FROM pg_stat_activity WHERE state = 'active'`
4. Escalate to: On-call engineer if p95 > 2 seconds

Examples (BAD):
**If something breaks**: Check the logs
(Too vague - WHICH logs? What to look for?)

Think: What will break at 2am? How does on-call fix it?
Format: Symptom → Diagnostic steps → Solution
Include: Actual commands to run, not just "check logs"
-->

### Common Issues

**[Issue]: [Symptom]**
- **Diagnosis**: [How to identify root cause]
- **Resolution**: [How to fix]
- **Prevention**: [How to avoid in future]

### Debug Commands

```bash
# Check service health
[command to check if service is running]

# View recent errors
[command to see error logs]

# Check dependencies
[commands to verify DB, Redis, etc. are accessible]
```

### Escalation

- **Tier 1** (Self-service): Common issues, documented solutions
- **Tier 2** (Team Slack): Issues requiring code knowledge
- **Tier 3** (On-call Page): Production outages, data loss risk

---

## Compliance Requirements

<!-- LLM GUIDANCE:
Document regulatory and compliance needs.

Common frameworks:
- **GDPR**: EU data protection (right to delete, data portability, consent)
- **CCPA**: California privacy law (similar to GDPR)
- **HIPAA**: Healthcare data protection (encryption, audit logs, access controls)
- **SOC 2**: Security controls audit (Type I = design, Type II = operation)
- **PCI-DSS**: Payment card data security (if handling credit cards)

Format:
**[Framework]**: [Requirements]
- **Impact**: [What this means for our feature]
- **Implementation**: [How we comply]

Examples (GOOD):
**GDPR**: EU users have right to delete their data
- **Impact**: Must provide "Delete Account" functionality
- **Implementation**: DELETE /api/users/:id endpoint, cascade deletes across all tables, confirmation email sent

**SOC 2 Type II**: Must log all access to sensitive data
- **Impact**: Audit logs for all authentication attempts
- **Implementation**: Write to audit_log table on every login/logout, retain for 1 year

Examples (BAD):
**Compliance**: We'll be compliant with all regulations
(Too vague - WHICH regulations?)

**GDPR**: Users can delete their data
(Missing HOW we implement this)

Think: What regulations apply to this feature?
Only include: Frameworks that actually apply (not hypothetical)
Be specific: Cite actual requirements and our solution
-->

### Applicable Frameworks

**[Framework Name]**: [Brief description]
- **Requirements**: [What regulations say]
- **Implementation**: [How we comply]
- **Evidence**: [How to prove compliance]

---

## Cost Analysis

<!-- LLM GUIDANCE:
Estimate infrastructure and operational costs.

Break down by:
1. **Compute**: Servers, containers, lambda functions
2. **Storage**: Database, file storage, backups
3. **Network**: Data transfer, CDN, load balancers
4. **Third-party**: APIs, SaaS services
5. **Support**: On-call, monitoring, logging

Format:
**[Resource]**: [Cost] per [unit] = [monthly estimate]

Examples (GOOD):
**Compute**: 2 t3.medium instances @ $0.0416/hour = $60/month
**Database**: RDS PostgreSQL db.t3.small @ $0.034/hour = $25/month
**Storage**: 100GB database storage @ $0.115/GB = $12/month
**SendGrid**: 40,000 emails/month @ $0.0005/email = $20/month
**CloudWatch**: 10GB logs @ $0.50/GB + 5M API calls @ $0.01/10K = $6/month

**Total**: ~$123/month at 1000 active users
**Cost per user**: $0.12/month

**Scaling**: At 10,000 users, need 4x instances = ~$400/month ($0.04/user)

Examples (BAD):
**Infrastructure**: Will cost money
(Not helpful)

**AWS**: $500/month
(No breakdown - can't optimize)

Think: What resources does this feature need?
Include: Fixed costs (minimum infrastructure) + variable costs (per user/request)
Estimate: At different scales (1K, 10K, 100K users)
-->

### Infrastructure Costs

**[Resource]**: [Cost calculation] = [Monthly total]

### Third-Party Services

**[Service]**: [Cost calculation] = [Monthly total]

### Total Cost Estimate

- **At 1,000 users**: $X/month ($Y per user)
- **At 10,000 users**: $X/month ($Y per user)
- **At 100,000 users**: $X/month ($Y per user)

---

## Migration Strategy

<!-- LLM GUIDANCE:
How to migrate from current state to new feature (if applicable).

Only include if:
- Replacing an existing feature
- Migrating data from old system
- Changing data models
- Backwards compatibility needed

Include:
1. **Current State**: What exists today
2. **Migration Steps**: How to transition
3. **Backwards Compatibility**: Do old systems keep working?
4. **Rollout Plan**: Gradual or all-at-once
5. **Data Migration**: How to move/transform data

Examples (GOOD):
**Current State**: Using session cookies for authentication
**Migration Plan**:
1. Add JWT support alongside sessions (both work)
2. Update frontend to use JWT for new logins
3. Keep sessions working for existing users
4. After 30 days, deprecate session support
5. After 60 days, remove session code

**Data Migration**:
- No data migration needed (JWT is stateless)
- Existing sessions expire naturally (24 hour TTL)
- Users seamlessly transition on next login

**Backwards Compatibility**: 60-day overlap period

Examples (BAD):
**Migration**: Switch to new system
(No plan - how? when? what breaks?)

Think: How do we get from HERE to THERE without breaking production?
Critical: Zero downtime, no data loss, rollback plan
Timeline: Specific dates and milestones
-->

### Current State
[What exists today that we're changing/replacing]

### Migration Steps
1. [Step 1 with timeline]
2. [Step 2 with timeline]
3. [Step 3 with timeline]

### Backwards Compatibility
[What old systems/clients keep working during migration]

### Data Migration
[How to move/transform data, estimated time, validation]

---

## Next Steps

<!--
This is a COMPLETE tier specification (Tier 3 of 3).
You have production-ready detail for critical features.

Next actions:
1. Generate implementation plan:
   Command: /sp-plan

2. Generate task breakdown:
   Command: /sp-task

3. Check progress:
   Command: specpulse spec progress {{feature_id}}
-->

**Current Tier**: Complete (15+ sections)
**Time to Complete**: 30-45 minutes
**Ready for Planning**: ✓ Yes
**Production-Ready**: ✓ Yes

💡 **Tip**: Complete tier is for production-critical features requiring security audits, compliance, and detailed operational runbooks. Most features don't need this level of detail!
