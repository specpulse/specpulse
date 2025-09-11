"""
SpecPulse AI Commands - Claude and Gemini CLI integration
"""

from pathlib import Path


class AICommands:
    """Generate AI-specific command files"""
    
    def __init__(self):
        # Get resource directory path
        self.resources_dir = Path(__file__).parent.parent / "resources"
    
    def get_claude_pulse_command(self) -> str:
        """Get Claude /pulse command from file"""
        command_path = self.resources_dir / "commands" / "claude" / "pulse.md"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded command if file not found
        return """
Initialize a new feature with proper branch and directory structure.

This is the entry point to the SpecPulse development lifecycle.

Given the feature name provided as an argument, do this:

1. Run the script `scripts/pulse-init.sh "{{args}}"` from repo root to create feature branch and directories
2. Parse the output to get:
   - BRANCH_NAME: The created branch name (e.g., 001-feature-name)
   - SPEC_DIR: The specification directory path
   - FEATURE_ID: The feature ID number
3. Create initial structure:
   - specs/{{FEATURE_ID}}-{{feature-name}}/spec.md
   - plans/{{FEATURE_ID}}-{{feature-name}}/plan.md
   - tasks/{{FEATURE_ID}}-{{feature-name}}/tasks.md
4. Update memory/context.md with the new active feature
5. Report completion with branch name and readiness for specification phase

Use the feature name from arguments: {{args}}
"""

    def get_claude_spec_command(self) -> str:
        """Get Claude /spec command from file"""
        command_path = self.resources_dir / "commands" / "claude" / "spec.md"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded command if file not found
        return """
Create a detailed specification from the provided description.

This is the first formal step in the SpecPulse development lifecycle.

Given the feature description provided as an argument, do this:

1. Run `scripts/pulse-spec.sh --current` to get the current feature context
2. Load `templates/spec-template.md` to understand the required structure
3. Generate a comprehensive specification including:
   - Executive Summary
   - Problem Statement
   - Proposed Solution
   - Functional Requirements (numbered FR-001, FR-002, etc.)
   - Non-Functional Requirements (performance, security, scalability)
   - User Stories with acceptance criteria
   - Technical Constraints
   - Dependencies
   - Risks and Mitigations
4. Mark any unclear items with [NEEDS CLARIFICATION]
5. Write the specification to the current feature's spec.md file
6. Update memory/context.md with specification status
7. Report completion and any items needing clarification

Feature description from arguments: {{args}}
"""

    @staticmethod
    def get_claude_plan_command() -> str:
        """Get Claude /plan command"""
        return """
Generate an implementation plan from the current specification.

This is the second step in the SpecPulse development lifecycle.

Given any additional technical context in arguments, do this:

1. Run `scripts/pulse-plan.sh --current` to get current feature and spec path
2. Read and analyze the feature specification to understand all requirements
3. Read memory/constitution.md for architectural principles and constraints
4. Generate implementation plan including:
   - Architecture Overview (with mermaid diagram if applicable)
   - Technology Stack with rationale
   - Implementation Phases (0-4 typically):
     * Phase 0: Setup and Prerequisites
     * Phase 1: Data Layer
     * Phase 2: Business Logic
     * Phase 3: API/Interface Layer
     * Phase 4: Testing and Polish
   - File Structure
   - API Contracts (if applicable)
   - Data Models
   - Testing Strategy
   - Risk Assessment
   - Success Criteria
5. Ensure plan follows constitution principles
6. Write plan to the current feature's plan.md file
7. Generate supporting artifacts if needed:
   - data-model.md for complex entities
   - contracts/ directory for API specifications
   - research.md for technical decisions
8. Update memory/context.md with plan status
9. Report completion with generated artifacts

Additional context from arguments: {{args}}
"""

    @staticmethod
    def get_claude_task_command() -> str:
        """Get Claude /task command"""
        return """
Break down the implementation plan into executable tasks.

This is the third step in the SpecPulse development lifecycle.

Given any task generation preferences in arguments, do this:

1. Run `scripts/pulse-task.sh --current` to get current feature directory
2. Read and analyze available documents:
   - plan.md for phases and technology decisions
   - data-model.md if exists for entity tasks
   - contracts/*.yaml if exists for API tasks
   - spec.md for user stories and acceptance criteria
3. Generate tasks following these patterns:
   - Setup tasks (T001-T00X): Environment, dependencies, configuration
   - Test tasks [P] (T01X): One per contract, one per user story (TDD)
   - Core tasks (T02X-T04X): Models, services, business logic
   - Integration tasks (T05X): API endpoints, database, external services
   - Polish tasks [P] (T06X): Documentation, optimization, deployment
4. Mark parallel tasks with [P] when:
   - Tasks work on different files
   - No shared dependencies
   - Can be executed simultaneously
5. Order tasks by dependencies:
   - Tests before implementation (TDD)
   - Models before services
   - Services before endpoints
   - Core before integration
6. Create numbered task list (T001, T002, etc.) with:
   - Clear description
   - File paths affected
   - Dependencies noted
   - Time estimates
   - [P] marking for parallel execution
7. Write tasks to current feature's tasks.md file
8. Update memory/context.md with task generation complete
9. Report task count, parallel groups, and estimated timeline

Task preferences from arguments: {{args}}
"""

    def get_gemini_pulse_command(self) -> str:
        """Get Gemini pulse command from file"""
        command_path = self.resources_dir / "commands" / "gemini" / "pulse.toml"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded command if file not found
        return """description = "Initialize a new feature with proper branch and directory structure."

prompt = \"\"\"
Initialize a new feature with proper branch and directory structure.

This is the entry point to the SpecPulse development lifecycle.

Given the feature name provided as an argument, do this:

1. Run the script `scripts/pulse-init.sh "{{args}}"` from repo root to create feature branch and directories
2. Parse the output to get:
   - BRANCH_NAME: The created branch name (e.g., 001-feature-name)
   - SPEC_DIR: The specification directory path
   - FEATURE_ID: The feature ID number
3. Create initial structure:
   - specs/{{FEATURE_ID}}-{{feature-name}}/spec.md
   - plans/{{FEATURE_ID}}-{{feature-name}}/plan.md
   - tasks/{{FEATURE_ID}}-{{feature-name}}/tasks.md
4. Update memory/context.md with the new active feature
5. Report completion with branch name and readiness for specification phase

Use the feature name from arguments: {{args}}
\"\"\"
"""

    def get_gemini_spec_command(self) -> str:
        """Get Gemini spec command from file"""
        command_path = self.resources_dir / "commands" / "gemini" / "spec.toml"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded command if file not found
        return """description = "Create a detailed specification from the provided description."

prompt = \"\"\"
Create a detailed specification from the provided description.

This is the first formal step in the SpecPulse development lifecycle.

Given the feature description provided as an argument, do this:

1. Run `scripts/pulse-spec.sh --current` to get the current feature context
2. Load `templates/spec-template.md` to understand the required structure
3. Generate a comprehensive specification including:
   - Executive Summary
   - Problem Statement
   - Proposed Solution
   - Functional Requirements (numbered FR-001, FR-002, etc.)
   - Non-Functional Requirements (performance, security, scalability)
   - User Stories with acceptance criteria
   - Technical Constraints
   - Dependencies
   - Risks and Mitigations
4. Mark any unclear items with [NEEDS CLARIFICATION]
5. Write the specification to the current feature's spec.md file
6. Update memory/context.md with specification status
7. Report completion and any items needing clarification

Feature description from arguments: {{args}}
\"\"\"
"""

    def get_gemini_plan_command(self) -> str:
        """Get Gemini plan command from file"""
        command_path = self.resources_dir / "commands" / "gemini" / "plan.toml"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded command if file not found
        return """description = "Generate an implementation plan from the current specification."

prompt = \"\"\"
Generate an implementation plan from the current specification.

This is the second step in the SpecPulse development lifecycle.

Given any additional technical context in arguments, do this:

1. Run `scripts/pulse-plan.sh --current` to get current feature and spec path
2. Read and analyze the feature specification to understand all requirements
3. Read memory/constitution.md for architectural principles and constraints
4. Generate implementation plan including:
   - Architecture Overview (with mermaid diagram if applicable)
   - Technology Stack with rationale
   - Implementation Phases (0-4 typically):
     * Phase 0: Setup and Prerequisites
     * Phase 1: Data Layer
     * Phase 2: Business Logic
     * Phase 3: API/Interface Layer
     * Phase 4: Testing and Polish
   - File Structure
   - API Contracts (if applicable)
   - Data Models
   - Testing Strategy
   - Risk Assessment
   - Success Criteria
5. Ensure plan follows constitution principles
6. Write plan to the current feature's plan.md file
7. Generate supporting artifacts if needed:
   - data-model.md for complex entities
   - contracts/ directory for API specifications
   - research.md for technical decisions
8. Update memory/context.md with plan status
9. Report completion with generated artifacts

Additional context from arguments: {{args}}
\"\"\"
"""

    def get_gemini_task_command(self) -> str:
        """Get Gemini task command from file"""
        command_path = self.resources_dir / "commands" / "gemini" / "task.toml"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded command if file not found
        return """description = "Break down the implementation plan into executable tasks."

prompt = \"\"\"
Break down the implementation plan into executable tasks.

This is the third step in the SpecPulse development lifecycle.

Given any task generation preferences in arguments, do this:

1. Run `scripts/pulse-task.sh --current` to get current feature directory
2. Read and analyze available documents:
   - plan.md for phases and technology decisions
   - data-model.md if exists for entity tasks
   - contracts/*.yaml if exists for API tasks
   - spec.md for user stories and acceptance criteria
3. Generate tasks following these patterns:
   - Setup tasks (T001-T00X): Environment, dependencies, configuration
   - Test tasks [P] (T01X): One per contract, one per user story (TDD)
   - Core tasks (T02X-T04X): Models, services, business logic
   - Integration tasks (T05X): API endpoints, database, external services
   - Polish tasks [P] (T06X): Documentation, optimization, deployment
4. Mark parallel tasks with [P] when:
   - Tasks work on different files
   - No shared dependencies
   - Can be executed simultaneously
5. Order tasks by dependencies:
   - Tests before implementation (TDD)
   - Models before services
   - Services before endpoints
   - Core before integration
6. Create numbered task list (T001, T002, etc.) with:
   - Clear description
   - File paths affected
   - Dependencies noted
   - Time estimates
   - [P] marking for parallel execution
7. Write tasks to current feature's tasks.md file
8. Update memory/context.md with task generation complete
9. Report task count, parallel groups, and estimated timeline

Task preferences from arguments: {{args}}
\"\"\"
"""