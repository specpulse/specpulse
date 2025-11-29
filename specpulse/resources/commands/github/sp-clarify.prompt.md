$ARGUMENTS

# GitHub Copilot SpecPulse Clarification Resolver

Resolve `[NEEDS CLARIFICATION]` markers in specifications without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-clarify [spec-id]    # Clarify current spec or specific spec
```

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the clarification outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use file operations (CLI-independent mode)
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Implementation Steps**

1. **Detect Target Specification**
   - Use Read tool to detect current feature context from .specpulse/memory/context.md
   - If arguments provided (e.g., 001), look for spec-001.md in current feature
   - If no arguments, find the most recent specification in current feature
   - Search across all feature directories if needed
   - Use Glob tool to safely find specification files

2. **Validate Specification File**
   - Use Read tool to examine the specification content
   - Manually check for required sections: Requirements, User Stories, Acceptance Criteria, Technical Specification
   - Report any structural issues that need addressing

3. **Find Clarification Markers**
   - Use Grep tool to search for [NEEDS CLARIFICATION:...] patterns
   - Count total clarifications needed
   - If none found, report specification is complete
   - Display summary of clarifications to resolve

4. **Interactive Clarification Resolution**
   - For each clarification:
     - Extract the question from the marker
     - Use Read tool to get surrounding context (±200 characters)
     - Display context with highlighted question
     - WAIT for user input (interactive prompt)
     - If user provides answer:
       - Use Edit tool to replace marker with ✅ **CLARIFIED**: [answer]
       - Report successful resolution
     - If no answer provided, skip and continue

5. **Update Specification File**
   - Use Edit tool to update the specification with resolved clarifications
   - Ensure all changes are properly formatted
   - Validate file was updated successfully
   - Report completion status

6. **Validate Updated Specification**
   - Use Grep tool to confirm no clarification markers remain
   - Perform manual SDD compliance checks: Requirements documented, User stories defined, Acceptance criteria valid, Technical specification present, Success metrics defined
   - Calculate SDD compliance percentage
   - Report overall specification quality

7. **Generate Next Steps**
   - Display updated specification file path
   - Recommend next commands: /sp-plan, /sp-task, /sp-status
   - Provide contextual suggestions based on content (authentication → sp-decompose, api → sp-test, database → migration planning)

8. **Validate structure and report comprehensive clarification results**

**Interactive Flow**
1. Find all [NEEDS CLARIFICATION] markers
2. Ask user each question with context
3. WAIT for user's input (interactive)
4. Update spec with formatted answer
5. Repeat for all clarifications
6. Validate updated specification manually
7. Report results and next steps

**Examples**

**Basic Clarification:**
```
/sp-clarify
```

Output: Find and resolve all [NEEDS CLARIFICATION] markers in current specification interactively.

**Specific Spec Clarification:**
```
/sp-clarify 001
```

Output: Target spec-001.md in current feature and resolve clarification markers.

**Clarification Process:**
- **Context-Aware Questions**: Analyze surrounding content for better context
- **Validation Enhancement**: SDD compliance scoring and completeness calculation
- **Integration Suggestions**: Recommend related commands based on content

**Error Handling**
- No spec found: Guide user to create specification with /sp-spec
- No clarifications: Report specification is already complete
- File permission errors: Provide troubleshooting steps
- Empty answers: Allow user to skip or retry
- Partial completion: Save progress, can resume with same command

**Success Indicators**
- Complete Clarification: All markers resolved
- Valid Specification: Meets SDD standards
- Next Steps Ready: Clear implementation path
- User Engagement: Interactive and guided process
- Quality Assurance: Comprehensive validation

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Interactive clarification resolution with context awareness
- SDD compliance validation and quality scoring
- Context-aware suggestions and next steps
- Manual validation logic with enhanced analysis
<!-- SPECPULSE:END -->

## Implementation Notes

When called with the specified arguments, execute the clarification resolution workflow. Use only file operations within the allowed directories, perform interactive clarification resolution with context awareness, and provide comprehensive validation and next steps.