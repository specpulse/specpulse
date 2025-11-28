---
description: Address clarification markers in specifications through interactive user input and resolution
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the clarification resolution outcome
- Only edit specs/ directory - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse spec clarify <spec-id>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/
- **EDITABLE ONLY**: specs/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Detect target specification**:
   - Read `memory/context.md` for current feature
   - If spec ID provided, use that spec file
   - Otherwise, find most recent spec in current feature

2. **Try CLI First**:
   ```bash
   specpulse spec clarify <spec-id>
   ```
   If CLI succeeds, STOP HERE.

3. **Find all clarification markers**:
   - Read the spec file
   - Search for all `[NEEDS CLARIFICATION: ...]` markers
   - Count total clarifications needed
   - List all clarification questions with context

4. **For each clarification marker**:
   - **Display the question** from the marker
   - **Show context** (the section where it appears)
   - **Ask user for answer**
   - **Wait for user response**
   - **Update spec** by removing marker and adding user's answer
   - **Continue to next** clarification

5. **Update spec file**:
   - Replace each `[NEEDS CLARIFICATION: question]` with actual answer
   - Preserve all other content
   - Maintain formatting and structure

6. **Validate updated spec**:
   ```bash
   specpulse validate spec
   ```

7. **Report results**:
   - Show how many clarifications were resolved
   - Display updated validation status
   - Suggest next steps

**Usage**
```
/sp-clarify                    # Clarify current spec
/sp-clarify 001                # Clarify specific spec
```

**Clarification Workflow**

**Marker Format:**
```markdown
[NEEDS CLARIFICATION: Which database should be used? (PostgreSQL, MongoDB, MySQL)]
```

**Resolution Process:**
1. **Extract Question**: Parse the clarification question
2. **Show Context**: Display where the question appears in the spec
3. **Gather Input**: Ask user for specific answer
4. **Apply Resolution**: Replace marker with user's answer
5. **Validate**: Check if spec is now complete

**Examples**

**Interactive clarification session:**
```
/sp-clarify
```
Output:
```
## Clarification Session: 001-user-authentication

Found 4 clarifications that need resolution:

### Clarification 1/4
**Section**: Database Configuration
**Question**: Which database should be used? (PostgreSQL, MongoDB, MySQL)

**Context**:
> The system should store user data in [NEEDS CLARIFICATION: Which database should be used? (PostgreSQL, MongoDB, MySQL)] with proper indexing.

**Your Answer**: PostgreSQL

✓ Resolved: "PostgreSQL"

### Clarification 2/4
**Section**: Authentication Strategy
**Question**: Token type? (JWT with refresh tokens, Session-based, OAuth2)

**Context**:
> Authentication will use [NEEDS CLARIFICATION: Token type? (JWT with refresh tokens, Session-based, OAuth2)] for secure session management.

**Your Answer**: JWT with refresh tokens

✓ Resolved: "JWT with refresh tokens"

### Clarification 3/4
**Section**: Password Requirements
**Question**: Minimum password complexity? (8 chars with special chars, 12 chars, Passphrase)

**Context**:
> Password security will enforce [NEEDS CLARIFICATION: Minimum password complexity? (8 chars with special chars, 12 chars, Passphrase)].

**Your Answer**: 12 chars minimum with special characters

✓ Resolved: "12 chars minimum with special characters"

### Clarification 4/4
**Section**: User Roles
**Question**: Initial user roles? (Admin/User only, Admin/User/Moderator, Custom roles)

**Context**:
> The system will support [NEEDS CLARIFICATION: Initial user roles? (Admin/User only, Admin/User/Moderator, Custom roles)].

**Your Answer**: Admin/User/Moderator

✓ Resolved: "Admin/User/Moderator"

## Clarification Complete

✅ **All 4 clarifications resolved**
✅ **Specification updated**
✅ **Validation passed**

**Next Steps**:
1. Review updated specification
2. Run `/sp-plan` to create implementation plan
3. Continue with `/sp-task` for task breakdown
```

**Specific spec clarification:**
```
/sp-clarify 002
```
Output: Clarifies spec 002 with the same interactive process.

**Batch Clarification Mode**

**When multiple clarifications exist:**
```
/sp-clarify --batch
```
Output:
```
## Batch Clarification Mode

Found 7 clarifications. I'll ask them all at once:

**Please provide answers for all 7 questions:**

1. **Database**: PostgreSQL, MongoDB, MySQL?
2. **Auth Method**: JWT, Session, OAuth2?
3. **Password Policy**: 8 chars, 12 chars, Passphrase?
4. **User Roles**: Admin/User, Admin/User/Moderator, Custom?
5. **Email Service**: SendGrid, AWS SES, Custom SMTP?
6. **File Storage**: Local, AWS S3, CloudFront?
7. **Logging**: Winston, Pino, Custom?

**Your Answers** (one per line):
1. PostgreSQL
2. JWT with refresh tokens
3. 12 chars with special characters
4. Admin/User/Moderator
5. AWS SES
6. AWS S3
7. Winston

✅ **All clarifications applied**
```

**Smart Clarification Features**

**Context-Aware Suggestions:**
Based on specification content, provide intelligent suggestions:

```
### Clarification: Database Selection
**Question**: Which database for user data?
**Suggested**: PostgreSQL (based on user authentication requirements)
**Options**:
- PostgreSQL (Recommended for ACID compliance)
- MongoDB (Recommended for flexible schema)
- MySQL (Recommended for legacy compatibility)

**Your Answer**: [PostgreSQL]
```

**Template-Based Clarifications:**
Common question templates with predefined options:

```markdown
[NEEDS CLARIFICATION: Database choice? (PostgreSQL, MongoDB, MySQL)]
[NEEDS CLARIFICATION: Authentication method? (JWT, Session, OAuth2)]
[NEEDS CLARIFICATION: Frontend framework? (React, Vue, Angular)]
[NEEDS CLARIFICATION: Deployment platform? (AWS, GCP, Azure)]
```

**Clarification Categories**

**Technical Decisions:**
- Database choice
- Authentication method
- API framework
- Deployment platform

**Business Requirements:**
- User roles and permissions
- Performance requirements
- Compliance standards
- Integration needs

**UX/UI Decisions:**
- Frontend framework
- Design system
- Accessibility requirements
- Mobile support

**CLI Integration**

**Try CLI First:**
```bash
specpulse spec clarify <spec-id>
specpulse sp-spec clarify <spec-id>
```

**Fallback to Manual Clarification if CLI Fails:**
1. Read specification file manually
2. Parse [NEEDS CLARIFICATION] markers
3. Ask questions interactively
4. Update specification with answers
5. Validate completion

**Advanced Features**

**Clarification History:**
- Track all resolved clarifications
- Store decision rationale
- Maintain change history

**Smart Completion:**
- Auto-suggest answers based on context
- Detect similar specifications for reference
- Provide best practice recommendations

**Validation Integration:**
- Automatic validation after clarification
- Check for completeness
- Identify remaining ambiguities

**Error Handling**

**Invalid Responses:**
- Ask for clarification if answer is unclear
- Provide options for multiple choice questions
- Suggest default values for technical decisions

**Specification Updates:**
- Preserve formatting when applying answers
- Maintain section structure
- Update related sections automatically

**Best Practices**

**Effective Clarification Questions:**
- Be specific and concrete
- Provide clear options
- Include business context
- Suggest best practices

**Answer Management:**
- Store decisions for future reference
- Document rationale
- Update dependent sections
- Validate consistency

**Integration Scenarios**

**Team Collaboration:**
```
/sp-clarify --team
```
Output: Gathers input from multiple team members for decisions.

**Stakeholder Review:**
```
/sp-clarify --stakeholder
```
Output: Highlights business decisions that need stakeholder approval.

**Technical Architecture:**
```
/sp-clarify --architect
```
Output: Focuses on technical architecture decisions.

**Reference**
- Use `specpulse spec clarify --help` if you need additional CLI options
- Check `memory/context.md` for current specification context
- Run `specpulse doctor` if you encounter system issues
- After clarification, use `/sp-validate` to confirm completeness
- Then proceed with `/sp-plan` for implementation planning
<!-- SPECPULSE:END -->