---
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the specification creation outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use file operations (CLI-independent mode)
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments to determine action**:
   - If first argument is create, update, validate, or clarify → Use that action
   - If no action specified → Default to create
   - For create → All remaining text becomes the description
   - For other actions → Look for feature name or use current feature

2. **Detect current feature context**:
   - Check .specpulse/memory/context.md for active feature
   - Look for most recently modified spec/plan/task directory
   - Validate feature directory exists and is properly structured
   - Extract feature ID and name from directory structure

3. **For action: create (default)**:
   - **Step 1: Generate Next Spec Number (Universal ID System)**
     - Use Glob tool to scan .specpulse/specs/[feature]/ directory
     - Parse all existing spec-###.md files to extract numbers
     - Convert to integers and find the maximum value
     - Generate next sequential number: next_num = max_num + 1
     - Zero-pad to 3 digits: format(max_num + 1, '03d') → 001, 002, 003
     - Validate no conflicts exist before using the number
   - **Step 2: Read Template**
     - Load .specpulse/templates/spec.md template file
     - If template missing, create comprehensive specification structure
   - **Step 3: Expand Specification with AI**
     - Generate Executive Summary, Functional Requirements, User Stories
     - Include Technical Constraints, Risk Assessment, Success Metrics
   - **Step 4: Write Specification File**
     - Create .specpulse/specs/[feature]/spec-[###].md with generated content
     - Use atomic file operations to prevent corruption

4. **For action: update**:
   - List all specification files in current feature
   - Allow user to select which spec to update
   - Parse existing content and identify sections needing updates
   - Generate updated content based on new requirements
   - Preserve existing structure while enhancing content

5. **For action: validate**:
   - Check specification file exists and is readable
   - Validate required sections are present (Executive Summary, Functional Requirements, etc.)
   - Count any [NEEDS CLARIFICATION] markers
   - Verify Given-When-Then format in user stories
   - Calculate completeness percentage
   - Identify missing or incomplete sections

6. **For action: clarify**:
   - Scan specification for [NEEDS CLARIFICATION:...] patterns
   - Extract each question with surrounding context
   - Ask user for resolution on each clarification
   - Replace markers with ✅ **CLARIFIED**: [answer] format
   - Update specification with resolved clarifications

7. **Validate structure and report comprehensive status**

**Usage**
```
/sp-spec [action] [description|feature-name]
```

**Examples**

**Basic Usage:**
```
/sp-spec create user authentication system with JWT tokens
```

Output: Create comprehensive specification with AI-generated content, structure, and validation.

**Validate Specification:**
```
/sp-spec validate
```

Output: Perform comprehensive validation, check required sections, count clarifications, calculate completeness.

**Update Specification:**
```
/sp-spec update add MFA support
```

Output: Update existing specification with new requirements while preserving structure.

**Advanced Features:**
- **AI-Powered Content Analysis**: Project type detection, complexity assessment
- **SDD Gates Compliance**: Specification First, Traceable, Testable, Complete
- **Universal ID System**: Conflict-free file numbering with validation
- **Context Management**: File-based project memory and decision tracking

**Error Handling**
- No active feature: Prompt to run /sp-pulse first
- Permission denied: Guide user to check file permissions
- Invalid feature name: Suggest valid feature names
- Template missing: Create specification structure manually

**Reference**
- Check memory/context.md for current feature context
- Run validation on created specification
- After specification creation, continue with /sp-plan for implementation planning

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Uses LLM-safe file operations with atomic writes
- AI-enhanced content generation and analysis
- Comprehensive error recovery and validation
<!-- SPECPULSE:END -->