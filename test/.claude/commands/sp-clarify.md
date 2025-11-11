---
name: sp-clarify
description: Address clarification markers in specifications
allowed_tools:
  - Read
  - Edit
  - Bash
  - TodoWrite
---

# /sp-clarify Command

Address all `[NEEDS CLARIFICATION]` markers in the current specification by asking user for input and updating the spec.

## CRITICAL: File Edit Restrictions
- **NEVER EDIT**: templates/, commands/, .claude/, .gemini/
- **ONLY EDIT**: specs/, plans/, tasks/, memory/

## Usage
```
/sp-clarify                    # Clarify current spec
/sp-clarify 001                # Clarify specific spec
```

## Implementation

When called with `/sp-clarify $ARGUMENTS`, I will:

1. **Detect target specification**:
   - Read `memory/context.md` for current feature
   - If spec ID provided, use that spec file
   - Otherwise, find most recent spec in current feature

2. **Find all clarification markers**:
   - Read the spec file
   - Search for all `[NEEDS CLARIFICATION: ...]` markers
   - Count total clarifications needed

3. **For each clarification marker**:
   - **Display the question** from the marker
   - **Show context** (the section where it appears)
   - **Ask user for answer**
   - **Wait for user response**
   - **Update spec** by removing marker and adding user's answer
   - **Continue to next** clarification

4. **Update spec file**:
   - Replace each `[NEEDS CLARIFICATION: question]` with actual answer
   - Preserve all other content
   - Maintain formatting and structure

5. **Validate updated spec**:
   ```bash
   specpulse validate spec
   ```

6. **Report results**:
   - Show how many clarifications were resolved
   - Display updated validation status
   - Suggest next steps

## Example

### User runs command
```
User: /sp-clarify
```

### I will do this:
```
1. Read: specs/001-user-auth/spec-001.md

2. Found 4 clarifications needed:

   Clarification 1/4:
   Section: Database Configuration
   Question: Which database? (MongoDB, PostgreSQL, MySQL)

   [Wait for user answer]
   User: PostgreSQL

   Edit: spec-001.md (replace marker with "PostgreSQL")

3. Clarification 2/4:
   Section: Authentication
   Question: Token type? (JWT, Session, OAuth2)

   [Wait for user answer]
   User: JWT with refresh tokens

   Edit: spec-001.md (replace marker with answer)

4. [Continue for all 4 clarifications]

5. Validate: specpulse validate spec

6. Report:
   ✓ Resolved 4 clarifications
   ✓ Specification now complete
   ✓ Ready for /sp-plan
```

## Interactive Flow

**I will:**
1. Find next `[NEEDS CLARIFICATION]` marker
2. Ask user the question
3. **WAIT** for user's answer (don't continue automatically)
4. Update spec with answer
5. Repeat for next marker
6. Only proceed when ALL clarifications are resolved

## Important Notes

- **Interactive**: Must wait for user input for each clarification
- **Sequential**: Handle one clarification at a time
- **Preserve Content**: Only remove markers, keep all other content
- **Validation**: Run validation after all clarifications resolved
- **Context Aware**: Use feature context from memory/context.md

## Output Format

```
🔍 Clarifications Needed: 4

─────────────────────────────────────────
Clarification 1/4
─────────────────────────────────────────
Section: Database Configuration
Context: "...store user data..."

Question: Which database type should be used?
  Options: MongoDB, PostgreSQL, MySQL, or other?

Your answer: [WAITING FOR USER INPUT]

─────────────────────────────────────────
```

## Next Steps After Clarification

Once all clarifications are resolved:
```
✓ All clarifications resolved!
✓ Specification is now complete
✓ Validation: PASSED

Next steps:
  1. Review updated spec: specs/001-feature/spec-001.md
  2. Generate plan: /sp-plan generate
  3. Or validate again: /sp-spec validate
```

## Error Handling

- **No clarifications found**: Report spec is already complete
- **Spec not found**: Guide user to create spec first
- **Invalid answers**: Ask for clarification on the clarification
- **Partial completion**: Save progress, can resume later
