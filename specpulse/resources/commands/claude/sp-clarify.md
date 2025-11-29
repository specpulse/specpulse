---
name: sp-clarify
description: Resolve clarification markers in specifications without SpecPulse CLI
allowed_tools:
  - Read
  - Edit
  - Bash
  - TodoWrite
---

# /sp-clarify Command

Resolve `[NEEDS CLARIFICATION]` markers in specifications without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-clarify [spec-id]    # Clarify current spec or specific spec
```

## CLI-Independent Implementation

When called with `/sp-clarify $ARGUMENTS`, I will:

## Implementation Steps

When called with `/sp-clarify $ARGUMENTS`, I will:

### 1. Detect Target Specification

**I will:**
- Use the **Read** tool to detect current feature context from `.specpulse/memory/context.md`
- If arguments provided (e.g., `001`), look for `spec-001.md` in current feature
- If no arguments, find the most recent specification in current feature
- Search across all feature directories if needed
- Use **Glob** tool to safely find specification files

### 2. Validate Specification File

**I will:**
- Use **Read** tool to examine the specification content
- Manually check for required sections:
  - `# Requirements` section present?
  - `# User Stories` section present?
  - `# Acceptance Criteria` section present?
  - `## Technical Specification` section present?
- Report any structural issues that need addressing

### 3. Find Clarification Markers

**I will:**
- Use **Grep** tool to search for `[NEEDS CLARIFICATION:...]` patterns
- Count total clarifications needed
- If none found, report specification is complete
- Display summary of clarifications to resolve

### 4. Interactive Clarification Resolution

**For each clarification:**
- Extract the question from the marker
- Use **Read** tool to get surrounding context (±200 characters)
- Display context with highlighted question
- **WAIT** for user input (interactive prompt)
- If user provides answer:
  - Use **Edit** tool to replace marker with `✅ **CLARIFIED**: [answer]`
  - Report successful resolution
- If no answer provided, skip and continue

### 5. Update Specification File

**I will:**
- Use **Edit** tool to update the specification with resolved clarifications
- Ensure all changes are properly formatted
- Validate file was updated successfully
- Report completion status

### 6. Validate Updated Specification

**I will:**
- Use **Grep** tool to confirm no clarification markers remain
- Perform manual SDD compliance checks:
  - Requirements documented? ✅/❌
  - User stories defined? ✅/❌
  - Acceptance criteria valid? ✅/❌
  - Technical specification present? ✅/❌
  - Success metrics defined? ✅/❌
- Calculate SDD compliance percentage
- Report overall specification quality

### 7. Generate Next Steps

**I will:**
- Display updated specification file path
- Recommend next commands based on content:
  - `/sp-/sp-plan` - Generate implementation plan
  - `/sp-/sp-task` - Create task breakdown
  - `/sp-/sp-status` - Check project status
- Provide contextual suggestions:
  - If "authentication" found → suggest `/sp-decompose`
  - If "api" found → suggest `/sp-/sp-test`
  - If "database" found → suggest migration planning

## Interactive Flow

**I will:**
1. **Find** all `[NEEDS CLARIFICATION]` markers
2. **Ask** user each question with context
3. **WAIT** for user's input (interactive)
4. **Update** spec with formatted answer
5. **Repeat** for all clarifications
6. **Validate** updated specification manually
7. **Report** results and next steps

## Example Session

### User runs command
```
User: /sp-clarify 001
```

### I will do this:
```
🔍 Found 4 clarifications to resolve:

============================================================
📍 Clarification 1/4
============================================================
📋 Context:
   ...store user data securely🎯 QUESTION:Which database? (MongoDB, PostgreSQL, MySQL)🎯...

❓ Question: Which database? (MongoDB, PostgreSQL, MySQL)
💡 Please provide your answer:
Your answer: PostgreSQL

✅ Clarification resolved!

============================================================
📍 Clarification 2/4
============================================================
📋 Context:
   ...authenticate users🎯 QUESTION:Authentication method?🎯...

❓ Question: Authentication method?
💡 Please provide your answer:
Your answer: JWT with refresh tokens

✅ Clarification resolved!
[Continue for all 4 clarifications]

🎯 All clarifications resolved!
📄 Updated specification: .specpulse/specs/001-user-auth/spec-001.md

🔍 Validating updated specification...
✅ All clarification markers resolved!
✅ Requirements documentation
✅ User stories section
✅ Acceptance criteria
✅ Technical specification
✅ Success metrics

📊 SDD Compliance: 100% (5/5)
🎉 Specification meets SDD standards!
🚀 Ready for implementation planning!

📋 Next Steps:
1. Review specification: .specpulse/specs/001-user-auth/spec-001.md
2. Generate implementation plan: /sp-/sp-plan
3. Create task breakdown: /sp-/sp-task
4. Check project status: /sp-/sp-status
```

## Error Handling

- **No spec found**: Guide user to create specification with `/sp-/sp-spec`
- **No clarifications**: Report specification is already complete
- **File permission errors**: Provide troubleshooting steps
- **Empty answers**: Allow user to skip or retry
- **Partial completion**: Save progress, can resume with same command

## Advanced Features

### Context-Aware Questions
- Analyze surrounding content for better context
- Provide specific suggestions based on feature type
- Reference related sections in the specification

### Validation Enhancement
- SDD compliance scoring
- Completeness percentage calculation
- Missing section identification
- Quality assessment indicators

### Integration Suggestions
- Suggest related commands based on content
- Provide microservice decomposition hints
- Recommend testing strategies

## Key Benefits vs CLI Version

| Feature | CLI Version | LLM-Safe Version |
|---------|-------------|-----------------|
| Dependency | Requires specpulse CLI | Complete independence |
| Validation | `specpulse validate spec` | Manual validation logic |
| Context | Built-in CLI context | LLM-detected context |
| Portability | Platform-specific | Universal compatibility |
| Intelligence | Basic validation | Enhanced analysis |

## Success Indicators

✅ **Complete Clarification**: All markers resolved
✅ **Valid Specification**: Meets SDD standards
✅ **Next Steps Ready**: Clear implementation path
✅ **User Engagement**: Interactive and guided process
✅ **Quality Assurance**: Comprehensive validation