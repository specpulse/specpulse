---
agent: build
description: Validate specifications and plans using SpecPulse SDD methodology.
---

The user has requested the following change proposal. Use the openspec instructions to create their change proposal.
<UserRequest>
  sp-validate $ARGUMENTS
</UserRequest>

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the validation outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse validate [component]` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/, .opencode/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
1. **Parse arguments** to extract validation target and options from $ARGUMENTS
2. **Determine current context**:
   - Read: memory/context.md
   - Extract current.feature and current.feature_id if available
3. **Try CLI first**:
   - Run `specpulse validate [target]`
   - If this succeeds, display validation results
4. **If CLI doesn't exist, use File Operations**:
   - **Step 1: Identify validation target**
     - If no target specified, validate current component
     - Read appropriate files based on target (spec/plan/task)
5. **Comprehensive validation**:
   - Validate against SDD principles and best practices
   - Generate validation report sections:
     1. **Validation Overview** (summary and scope)
     2. **Structure Analysis** (format, completeness, organization)
     3. **Content Quality** (clarity, consistency, detail level)
     4. **Cross-Reference Validation** (dependencies, conflicts)
     5. **Compliance Check** (SDD principles, project standards)
   - Include specific issues found and recommendations

6. **Validation reporting**:
   - Categorize issues by severity (critical, major, minor)
   - Provide actionable recommendations
   - Suggest improvements and best practices
   - Generate validation summary

**Usage**
Arguments should be provided as: `[target] [options]`

**Examples**

**Validate Current Component:**
Input: (no arguments)
Output: Validate current active component (spec/plan/task).

**Validate Specific Component:**
Input: `spec-001`
Output: Validate specific specification file.

**Validate with Options:**
Input: `plans strict:true`
Output: Strict validation of all plan files.

**Next steps:**
- Recommend: "Address critical issues before proceeding"
- Action: "Use appropriate sp-* command to fix identified issues"
- Status: `STATUS=validation_complete, ISSUES_FOUND=3, CRITICAL_ISSUES=1, READY_TO_PROCEED=false`

**Reference**
- Use `specpulse validate --help` for additional CLI options
- Check validation rules in specpulse/resources/validation_rules.yaml
- Use appropriate sp-* commands to address validation issues
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->