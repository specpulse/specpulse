---
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the plan creation outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use file operations (CLI-independent mode)
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments to determine action**:
   - If first argument is generate, validate, or optimize → Use that action
   - If no action specified → Default to generate
   - For other arguments → Look for feature name or use current feature

2. **Detect current feature context**:
   - Check .specpulse/memory/context.md for active feature
   - Look for most recently modified spec/plan/task directory
   - Validate feature directory exists and is properly structured
   - Extract feature ID and name from directory structure

3. **For action: generate (default)**:
   - **Step 1: Specification Analysis**
     - Read specification files from .specpulse/specs/[feature]/
     - Analyze functional requirements and user stories
     - Extract technical constraints and dependencies
     - Identify complexity and risk factors
   - **Step 2: Decomposition Support Check**
     - Look for .specpulse/specs/[feature]/decomposition/ directory
     - If decomposition exists, identify service directories
     - Plan service-specific implementation strategies
     - Generate service-dependent task breakdowns
   - **Step 3: Plan Structure Design**
     - Create Implementation Strategy, Phase Breakdown, Task Dependencies
     - Include Resource Requirements, Timeline Estimates, Risk Mitigation
   - **Step 4: Service-Specific Planning (if decomposed)**
     - Generate Service Implementation Plan, Service Dependencies
     - Create Integration Strategy, Data Flow, API Contracts
   - **Step 5: Generate Next Plan Number (Universal ID System)**
     - Use Glob tool to scan .specpulse/plans/[feature]/ directory
     - Parse existing plan files using regex plan-(\d+)\.md pattern
     - Extract all numbers and convert to integers for comparison
     - Find maximum value: max_num = max(extracted_numbers) or 0 if empty
     - Generate next sequential: next_num = max_num + 1
     - Zero-pad format: f"plan-{next_num:03d}.md" → plan-001.md, plan-002.md
   - **Step 6: Write Plan File**
     - Create .specpulse/plans/[feature]/plan-[###].md with generated content
     - Use atomic file operations to prevent corruption

4. **For action: validate**:
   - **File Structure Validation**
     - Verify plan files exist in .specpulse/plans/[feature]/
     - Check file naming follows plan-[###].md pattern
     - Validate plan file format and readability
     - Ensure proper markdown structure
   - **Content Completeness Validation**
     - Check Implementation Strategy, Phase Breakdown, Task Dependencies
     - Validate Resource Requirements, Timeline Estimates, Risk Mitigation
   - **Technical Feasibility Validation**
     - Assess implementation approach complexity
     - Validate dependency relationships are logical
     - Check timeline estimates are achievable
     - Verify resource requirements are realistic

5. **For action: optimize**:
   - **Plan Analysis**
     - Read and analyze existing plan files
     - Identify complexity issues and optimization opportunities
     - Assess current phase breakdown effectiveness
     - Evaluate dependency management efficiency
   - **Optimization Strategies**
     - Apply Phase Consolidation, Dependency Optimization
     - Implement Timeline Optimization, Resource Optimization
   - **Risk Assessment Updates**
     - Update risk mitigation strategies
     - Identify new optimization-related risks
     - Provide contingency planning recommendations

6. **Validate structure and report comprehensive status**

**Usage**
```
/sp-plan [action] [feature-directory]
```

**Examples**

**Basic Usage:**
```
/sp-plan generate
```

Output: Create comprehensive implementation plan with specification analysis, phase breakdown, and service-specific planning.

**Validate Plan:**
```
/sp-plan validate
```

Output: Perform comprehensive validation, check file structure, content completeness, and technical feasibility.

**Optimize Plan:**
```
/sp-plan optimize
```

Output: Improve existing plans with optimization strategies, risk assessment updates, and timeline adjustments.

**Advanced Features:**
- **Decomposed Services Support**: Service-specific planning for microservices architecture
- **SDD Gates Compliance**: Specification First, Task Decomposition, Quality Assurance, Traceable Implementation
- **Universal ID System**: Conflict-free plan numbering with validation
- **Cross-Plan Dependency Management**: Track dependencies between multiple features

**Error Handling**
- No active feature: Prompt to run /sp-pulse first
- Invalid feature directory: Suggest valid feature names
- Missing specifications: Guide user to create specifications first
- Template missing: Create comprehensive plan structure manually

**Reference**
- Check memory/context.md for current feature context
- Run validation on created plan
- After plan creation, continue with /sp-task for task breakdown

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Uses LLM-safe file operations with atomic writes
- Intelligent planning algorithms and optimization
- Comprehensive error recovery and validation
<!-- SPECPULSE:END -->