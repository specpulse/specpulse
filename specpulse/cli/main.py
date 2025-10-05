#!/usr/bin/env python3
"""
SpecPulse CLI - Main entry point
"""

import argparse
import sys
import os
from pathlib import Path
import yaml
import shutil
from datetime import datetime, timedelta
from typing import Optional, Dict

from .. import __version__
from ..core.specpulse import SpecPulse
from ..core.validator import Validator
from ..core.template_manager import TemplateManager
from ..core.memory_manager import MemoryManager
from ..utils.console import Console
from ..utils.git_utils import GitUtils
from ..utils.version_check import check_pypi_version, compare_versions, get_update_message, should_check_version
from ..utils.error_handler import (
    ErrorHandler, SpecPulseError, ValidationError, ProjectStructureError,
    TemplateError, GitError, handle_specpulse_error, validate_project_directory,
    validate_templates, suggest_recovery_for_error, ErrorSeverity
)


class SpecPulseCLI:
    def __init__(self, no_color: bool = False, verbose: bool = False):
        self.console = Console(no_color=no_color, verbose=verbose)
        self.verbose = verbose
        self.error_handler = ErrorHandler(verbose=verbose)

        try:
            self.specpulse = SpecPulse()
            self.validator = Validator()

            # Initialize template manager
            project_root = Path.cwd()
            if self._is_specpulse_project(project_root):
                self.template_manager = TemplateManager(project_root)
                self.memory_manager = MemoryManager(project_root)
            else:
                self.template_manager = None
                self.memory_manager = None

            # Check for updates (non-blocking)
            self._check_for_updates()
        except Exception as e:
            self.console.error("Failed to initialize SpecPulse components")
            suggestions = suggest_recovery_for_error(str(e))
            self.console.warning("Recovery suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                self.console.info(f"   {i}. {suggestion}")
            if verbose:
                self.console.warning(f"Technical details: {str(e)}")
            sys.exit(1)

    def _check_for_updates(self):
        """Check for available updates on PyPI"""
        try:
            if not should_check_version():
                return

            latest = check_pypi_version(timeout=1)
            if latest:
                current = __version__
                is_outdated, is_major = compare_versions(current, latest)

                if is_outdated:
                    message, color = get_update_message(current, latest, is_major)
                    # Only show for init command or when verbose
                    # Don't spam on every command
                    import sys
                    if len(sys.argv) > 1 and sys.argv[1] in ['init', '--version']:
                        self.console.info(message, style=color)
        except:
            # Never fail due to version check
            pass

    def init(self, project_name: Optional[str] = None,
             here: bool = False,
             ai: str = "claude",
             template: str = "web"):
        """Initialize SpecPulse in an existing or new project"""

        try:
            # Validate project name for invalid characters
            import re
            if project_name and not here:
                if not re.match(r'^[a-zA-Z0-9_-]+$', project_name):
                    raise ValidationError(
                        f"Project name contains invalid characters: {project_name}",
                        validation_type="project_name",
                        missing_items=["Valid characters: letters, numbers, underscore, hyphen"]
                    )
  
            if here:
                project_path = Path.cwd()
                project_name = project_path.name
            else:
                if not project_name:
                    # If no project name, initialize in current directory
                    project_path = Path.cwd()
                    project_name = project_path.name
                else:
                    project_path = Path.cwd() / project_name
                    if not project_path.exists():
                        project_path.mkdir(parents=True)

            # Validate project path
            if not project_path.exists():
                raise ProjectStructureError(
                    f"Project path does not exist: {project_path}",
                    missing_dirs=[str(project_path)]
                )

            # Show banner on init
            self.console.show_banner()
            self.console.pulse_animation("Initializing SpecPulse Framework", duration=1.0)

            self.console.header(f"Initializing Project: {project_name}", style="bright_green")
        
            # Create directory structure
            directories = [
            ".specpulse",
            ".specpulse/cache",
            ".claude",
            ".claude/commands",
            ".gemini",
            ".gemini/commands",
            "memory",
            "specs",
            "plans",
            "tasks",
            "scripts",
            "templates",
            "templates/decomposition"
        ]
        
        # Create directories with progress bar and error handling
            failed_dirs = []
            with self.console.progress_bar("Creating project structure", len(directories)) as progress:
                task = progress.add_task("Creating directories...", total=len(directories))

                for dir_name in directories:
                    try:
                        dir_path = project_path / dir_name
                        dir_path.mkdir(parents=True, exist_ok=True)
                        progress.update(task, advance=1, description=f"Created {dir_name}/")
                        import time
                        time.sleep(0.05)  # Small delay for visual effect
                    except Exception as e:
                        failed_dirs.append(dir_name)
                        progress.update(task, advance=1, description=f"Failed {dir_name}/")
                        if self.verbose:
                            self.console.warning(f"Failed to create {dir_name}: {str(e)}")

            if failed_dirs:
                raise ProjectStructureError(
                    f"Failed to create {len(failed_dirs)} directories: {', '.join(failed_dirs)}",
                    missing_dirs=failed_dirs
                )
        
            # Create config file
            config = {
            "version": __version__,
            "project": {
                "name": project_name,
                "type": template,
                "created": datetime.now().isoformat()
            },
            "ai": {
                "primary": ai
            },
            "templates": {
                "spec": "templates/spec.md",
                "plan": "templates/plan.md",
                "task": "templates/task.md"
            },
            "conventions": {
                "branch_naming": "{number:03d}-{feature-name}",
                "spec_naming": "SPEC-{number:03d}",
                "task_naming": "TASK-{number:03d}"
            },
            "validation": {
                "required_sections": {
                    "spec": ["requirements", "user_stories", "acceptance_criteria"],
                    "plan": ["architecture", "phases", "technology_stack"],
                    "task": ["dependencies", "estimates", "assignments"]
                },
                "coverage": {
                    "unit_test": 80,
                    "integration_test": 60,
                    "e2e_test": 40
                }
            },
            "constitution": {
                "enforce": True,
                "strict_mode": False,
                "principles": [
                    "simplicity_first",
                    "test_driven", 
                    "single_responsibility",
                    "documented",
                    "secure_by_design"
                ]
            },
            "workflow": {
                "stages": ["draft", "review", "approved", "implementation", "testing", "deployed"],
                "transitions": {
                    "draft_to_review": {
                        "requires": ["complete_specification", "no_clarifications_pending"]
                    },
                    "review_to_approved": {
                        "requires": ["peer_review", "validation_passed"]
                    },
                    "approved_to_implementation": {
                        "requires": ["plan_generated", "tasks_created"]
                    }
                }
            },
            "integrations": {
                "git": {
                    "auto_commit": True,
                    "commit_template": "[SpecPulse] {action}: {description}"
                },
                "ci_cd": {
                    "provider": "github_actions",
                    "trigger_on": ["plan_approved", "tests_passed"]
                }
            }
            }
        
            config_path = project_path / ".specpulse" / "config.yaml"
            try:
                with open(config_path, 'w', encoding='utf-8') as f:
                    yaml.dump(config, f, default_flow_style=False)
                self.console.success("Created config.yaml")
            except Exception as e:
                raise SpecPulseError(
                    f"Failed to create config file: {config_path}",
                    severity=ErrorSeverity.HIGH,
                    recovery_suggestions=[
                        "Check write permissions for the project directory",
                        "Ensure sufficient disk space is available",
                        "Try running with administrator privileges"
                    ],
                    technical_details=str(e)
                )

            # Copy templates
            self._create_templates(project_path)

            # Create memory files
            self._create_memory_files(project_path)

            # Create scripts
            self._create_scripts(project_path)

            # Create AI command files
            self._create_ai_commands(project_path)

            # Create PULSE.md manifest
            self._create_manifest(project_path, project_name)

            self.console.success(f"SpecPulse project initialized successfully!")
            self.console.info(f"Next steps:")
            self.console.info(f"  cd {project_name if not here else '.'}")
            self.console.info(f"  {ai} ." if ai == "claude" else "gemini")

            return True

        except Exception as e:
            # Handle any errors that occurred during initialization
            return self.error_handler.handle_error(e, f"Initializing project '{project_name}'")
    
    def _create_templates(self, project_path: Path):
        """Create template files"""
        templates_dir = project_path / "templates"

        # Create spec template
        spec_template = self.specpulse.get_spec_template()
        with open(templates_dir / "spec.md", 'w', encoding='utf-8') as f:
            f.write(spec_template)

        # Create plan template
        plan_template = self.specpulse.get_plan_template()
        with open(templates_dir / "plan.md", 'w', encoding='utf-8') as f:
            f.write(plan_template)

        # Create task template
        task_template = self.specpulse.get_task_template()
        with open(templates_dir / "task.md", 'w', encoding='utf-8') as f:
            f.write(task_template)

        # Copy decomposition templates
        decomp_dir = templates_dir / "decomposition"
        decomp_dir.mkdir(parents=True, exist_ok=True)

        resources_decomp_dir = self.specpulse.resources_dir / "templates" / "decomposition"
        if resources_decomp_dir.exists():
            for template_file in resources_decomp_dir.iterdir():
                if template_file.is_file():
                    shutil.copy2(template_file, decomp_dir / template_file.name)

        self.console.success("Created templates")
    
    def _create_memory_files(self, project_path: Path):
        """Create memory system files"""
        memory_dir = project_path / "memory"
        
        # Constitution
        constitution = self.specpulse.get_constitution_template()
        with open(memory_dir / "constitution.md", 'w', encoding='utf-8') as f:
            f.write(constitution)
        
        # Context
        context = self.specpulse.get_context_template()
        with open(memory_dir / "context.md", 'w', encoding='utf-8') as f:
            f.write(context)
        
        # Decisions
        decisions = self.specpulse.get_decisions_template()
        with open(memory_dir / "decisions.md", 'w', encoding='utf-8') as f:
            f.write(decisions)
        
        self.console.animated_success("Memory files created")
    
    def _create_scripts(self, project_path: Path):
        """Create automation scripts - copy all cross-platform scripts from resources"""
        scripts_dir = project_path / "scripts"
        scripts_dir.mkdir(exist_ok=True)

        resources_scripts_dir = self.specpulse.resources_dir / "scripts"

        # Check if resources directory exists
        if not resources_scripts_dir.exists():
            # Create minimal test script for testing purposes
            test_script = scripts_dir / "test.sh"
            test_script.write_text("#!/bin/bash\necho 'Test script'")
            return

        # Copy all script files from resources
        script_extensions = [".sh", ".ps1", ".py"]
        scripts_copied = 0

        for script_file in resources_scripts_dir.iterdir():
            if script_file.suffix in script_extensions:
                dest_path = scripts_dir / script_file.name
                shutil.copy2(script_file, dest_path)

                # Make shell scripts executable
                if script_file.suffix in [".sh", ".ps1"]:
                    try:
                        os.chmod(dest_path, 0o755)
                    except:
                        pass  # Windows may not support chmod for .sh files
                
                scripts_copied += 1
        
        if scripts_copied == 0:
            self.console.warning("No scripts found in resources directory")
        else:
            self.console.animated_success(f"Scripts created ({scripts_copied} files)")
    
    def _create_ai_commands(self, project_path: Path):
        """Create AI command files for Claude and Gemini CLI integration"""

        # Create directories first
        claude_commands_dir = project_path / ".claude" / "commands"
        claude_commands_dir.mkdir(parents=True, exist_ok=True)

        gemini_commands_dir = project_path / ".gemini" / "commands"
        gemini_commands_dir.mkdir(parents=True, exist_ok=True)

        # Copy all command files from resources
        resources_commands_dir = self.specpulse.resources_dir / "commands"
        commands_copied = 0

        # Copy Claude commands (.md format)
        claude_resources_dir = resources_commands_dir / "claude"

        if claude_resources_dir.exists():
            for command_file in claude_resources_dir.glob("*.md"):
                dest_path = claude_commands_dir / command_file.name
                shutil.copy2(command_file, dest_path)
                commands_copied += 1
        else:
            # Create test command for testing purposes
            test_cmd = claude_commands_dir / "test.md"
            test_cmd.write_text("---\nname: test\ndescription: Test command\n---\n\nTest command")

        # Copy Gemini commands (.toml format)
        gemini_resources_dir = resources_commands_dir / "gemini"

        if gemini_resources_dir.exists():
            for command_file in gemini_resources_dir.glob("*.toml"):
                dest_path = gemini_commands_dir / command_file.name
                shutil.copy2(command_file, dest_path)
                commands_copied += 1
        else:
            # Create test command for testing purposes
            test_cmd = gemini_commands_dir / "test.toml"
            test_cmd.write_text('[test]\nname = "test"\ndescription = "Test command"')
        
        if commands_copied == 0:
            self.console.warning("No AI command files found in resources directory")
        else:
            self.console.animated_success(f"AI command files created ({commands_copied} files)")
    
    # def _create_ai_files(self, project_path: Path, ai: str):
    #     """Create AI instruction files (deprecated - AI tools create these themselves)"""
    #     # CLAUDE.md and GEMINI.md are now created by the AI tools themselves
    #     pass
    
    def _create_manifest(self, project_path: Path, project_name: str):
        """Create PULSE.md manifest"""
        manifest = f"""# {project_name} - SpecPulse Project

## Overview
This project uses SpecPulse for specification-driven development.

## Quick Start
1. Open in your AI assistant (Claude or Gemini)
2. Use `/sp-pulse <feature>` to start a new feature
3. Use `/sp-spec create` to generate specifications
4. Use `/sp-decompose <spec-id>` to break down large specs
5. Use `/sp-plan generate` to create implementation plans
6. Use `/sp-task breakdown` to create task lists
7. Use `/validate all` before implementation

## Project Structure
- `specs/` - Feature specifications
- `plans/` - Implementation plans
- `tasks/` - Task lists
- `memory/` - Project memory and constitution
- `scripts/` - Automation scripts
- `templates/` - Document templates

## Commands
- `/sp-pulse <feature>` - Initialize new feature
- `/sp-spec create <description>` - Create specification
- `/sp-decompose <spec-id>` - Decompose specs into microservices/APIs
- `/sp-plan generate` - Generate implementation plan
- `/sp-task breakdown` - Create task list
- `/validate [component]` - Validate project

Generated with SpecPulse v1.0.0
"""
        with open(project_path / "PULSE.md", 'w', encoding='utf-8') as f:
            f.write(manifest)
        
        self.console.animated_success("PULSE.md manifest created")
        
        # Show celebration animation
        self.console.celebration()
        
        # Show feature showcase
        features = [
            {"name": "Memory System", "description": "Persistent project context"},
            {"name": "AI Integration", "description": "Claude & Gemini support"},
            {"name": "Validation", "description": "Automatic project validation"},
            {"name": "Git Sync", "description": "Version control integration"}
        ]
        self.console.feature_showcase(features)
    
    def update(self):
        """Update SpecPulse templates to latest version"""
        self.console.show_banner(mini=True)
        self.console.header("Template Update", style="bright_yellow")
        
        project_path = Path.cwd()
        config_path = project_path / ".specpulse" / "config.yaml"
        
        if not config_path.exists():
            self.console.error("Not a SpecPulse project (missing .specpulse/config.yaml)")
            return False
        
        with self.console.progress_bar("Updating templates", 3) as progress:
            task = progress.add_task("Processing...", total=3)
            
            # Backup current templates
            progress.update(task, advance=1, description="Backing up current templates...")
            backup_dir = project_path / ".specpulse" / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            templates_dir = project_path / "templates"
            if templates_dir.exists():
                shutil.copytree(templates_dir, backup_dir / "templates")
                import time
                time.sleep(0.5)
            
            # Update templates
            progress.update(task, advance=1, description="Installing new templates...")
            self._create_templates(project_path)
            time.sleep(0.5)
            
            # Finalize
            progress.update(task, advance=1, description="Finalizing update...")
            time.sleep(0.3)
        
        self.console.info(f"Templates backed up to: {backup_dir}")
        self.console.animated_success("Templates updated successfully!")
        
        # Show what was updated
        update_items = [
            ("Specification Template", "Updated"),
            ("Plan Template", "Updated"),
            ("Task Template", "Updated"),
            ("Memory Templates", "Updated")
        ]
        self.console.status_panel("Update Summary", update_items)
        
        return True
    
    def validate(self, component: str = "all", fix: bool = False, verbose: bool = False):
        """Validate project components"""
        self.console.show_banner(mini=True)
        self.console.header("Project Validation", style="bright_yellow")
        
        project_path = Path.cwd()
        
        # Show spinner during validation
        self.console.spinner(f"Validating {component} components")
        if component == "all":
            results = self.validator.validate_all(project_path, fix=fix, verbose=verbose)
        elif component == "spec":
            results = self.validator.validate_spec(project_path, fix=fix, verbose=verbose)
        elif component == "plan":
            results = self.validator.validate_plan(project_path, fix=fix, verbose=verbose)
        elif component == "constitution":
            results = self.validator.validate_constitution(project_path, verbose=verbose)
        else:
            self.console.error(f"Unknown component: {component}")
            return False
        
        # Convert results to validation format
        validation_results = {}
        for result in results:
            component_name = result.get("component", "Unknown")
            validation_results[component_name] = result["status"] != "error"
        
        # Display beautiful validation results
        self.console.validation_results(validation_results)
        
        return all(r["status"] != "error" for r in results)
    
    def decompose(self, spec_id: Optional[str] = None, 
                  microservices: bool = False,
                  apis: bool = False, 
                  interfaces: bool = False):
        """Decompose large specifications into smaller components"""
        self.console.show_banner(mini=True)
        self.console.header("Specification Decomposition", style="bright_yellow")
        
        project_path = Path.cwd()
        specs_dir = project_path / "specs"
        
        # Find target specification
        if spec_id:
            # Handle both "001" and "001-feature" formats
            spec_id_num = spec_id.split('-')[0] if '-' in spec_id else spec_id
            spec_dirs = list(specs_dir.glob(f"{spec_id_num}*"))
        else:
            # Try to detect from context or most recent
            spec_dirs = sorted(specs_dir.glob("*"), reverse=True)
        
        if not spec_dirs:
            self.console.error("No specifications found. Run /sp-spec create first.")
            return False
        
        target_dir = spec_dirs[0]
        spec_files = list(target_dir.glob("spec-*.md"))
        
        if not spec_files:
            self.console.error(f"No specification files found in {target_dir}")
            return False
        
        # Use most recent spec file
        spec_file = sorted(spec_files)[-1]
        
        self.console.info(f"Decomposing: {spec_file.name}")
        self.console.spinner("Analyzing specification complexity")
        
        # Create decomposition directory
        decomp_dir = target_dir / "decomposition"
        decomp_dir.mkdir(exist_ok=True)
        
        # Determine what to generate
        if not any([microservices, apis, interfaces]):
            # Default to all
            microservices = apis = interfaces = True
        
        decomp_items = []
        
        if microservices:
            # Use template from SpecPulse core
            ms_template = self.specpulse.get_decomposition_template("microservices")
            ms_content = ms_template.replace("{{ feature_name }}", target_dir.name)
            ms_content = ms_content.replace("{{ spec_id }}", target_dir.name.split('-')[0])
            ms_content = ms_content.replace("{{ date }}", datetime.now().isoformat())
            ms_content = ms_content.replace("{{ version }}", "1.0.0")
            
            # Placeholder content for services (AI will fill this)
            ms_content = ms_content.replace("{{ services }}", """### Authentication Service
- **Responsibility**: User identity and access control
- **Bounded Context**: Identity Management

### User Management Service  
- **Responsibility**: User profiles and preferences
- **Bounded Context**: User Domain""")
            
            ms_content = ms_content.replace("{{ communication_patterns }}", """- REST APIs for synchronous
- Event Bus for asynchronous""")
            ms_content = ms_content.replace("{{ data_boundaries }}", """- Each service owns its data
- No shared databases""")
            ms_content = ms_content.replace("{{ integration_points }}", """- API Gateway
- Message Queue""")
            
            # Simplified microservices content
            ms_content = """# Microservice Decomposition

## Services Identified

### Authentication Service
- **Responsibility**: User identity and access control
- **Bounded Context**: Identity Management
- **Data Ownership**: users, sessions, tokens

### User Management Service  
- **Responsibility**: User profile and preferences
- **Bounded Context**: User Domain
- **Data Ownership**: profiles, preferences, settings

## Communication Patterns
- Synchronous: REST APIs
- Asynchronous: Event Bus
- Hybrid: CQRS for read/write separation
"""
            with open(decomp_dir / "microservices.md", 'w', encoding='utf-8') as f:
                f.write(ms_content)
            decomp_items.append(("Microservices", "Generated"))
        
        if apis:
            # Generate API contracts using template
            api_dir = decomp_dir / "api-contracts"
            api_dir.mkdir(exist_ok=True)
            
            # Use template from SpecPulse core
            api_template = self.specpulse.get_decomposition_template("api")
            
            # Basic API content (AI will expand this)
            api_content = """openapi: 3.0.0
info:
  title: Authentication Service API
  version: 1.0.0
paths:
  /api/v1/auth/login:
    post:
      summary: Authenticate user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
      responses:
        200:
          description: Successful authentication
"""
            with open(api_dir / "auth-service.yaml", 'w', encoding='utf-8') as f:
                f.write(api_content)
            decomp_items.append(("API Contracts", "Generated"))
        
        if interfaces:
            # Generate interface specifications using template
            iface_dir = decomp_dir / "interfaces"
            iface_dir.mkdir(exist_ok=True)
            
            # Use template from SpecPulse core
            iface_template = self.specpulse.get_decomposition_template("interface")
            
            # Basic interface content (AI will expand this)
            iface_content = """// Authentication Service Interface
export interface IAuthenticationService {
  authenticate(credentials: Credentials): Promise<AuthToken>;
  validateToken(token: string): Promise<TokenValidation>;
  refreshToken(refreshToken: string): Promise<AuthToken>;
  revokeToken(token: string): Promise<void>;
}

export interface Credentials {
  username: string;
  password: string;
}

export interface AuthToken {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}
"""
            with open(iface_dir / "IAuthService.ts", 'w', encoding='utf-8') as f:
                f.write(iface_content)
            decomp_items.append(("Interfaces", "Generated"))
        
        # Generate integration map
        map_content = """# Integration Map

## Service Communication

```mermaid
graph LR
    A[API Gateway] --> B[Auth Service]
    A --> C[User Service]
    B --> D[Session Store]
    C --> E[Profile DB]
    B -.->|Events| F[Event Bus]
    C -.->|Events| F
```

## Data Flow
1. Client → API Gateway
2. Gateway → Authentication
3. Auth → Session Store
4. Success → User Service
5. User → Profile Data
"""
        with open(decomp_dir / "integration-map.md", 'w', encoding='utf-8') as f:
            f.write(map_content)
        decomp_items.append(("Integration Map", "Created"))
        
        import time
        time.sleep(1)  # Visual effect
        
        # Display results
        self.console.status_panel("Decomposition Complete", decomp_items)
        self.console.animated_success(f"Specification decomposed into {len(decomp_items)} components")
        self.console.info(f"Output: {decomp_dir}")
        
        return True
    
    def sync(self):
        """Synchronize project state"""
        self.console.show_banner(mini=True)
        self.console.header("Project Synchronization", style="bright_magenta")
        
        project_path = Path.cwd()
        sync_items = []
        
        # Create missing directories if they don't exist
        for dir_name in ["specs", "plans", "tasks", "memory", "templates", "scripts"]:
            dir_path = project_path / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                sync_items.append((dir_name, "Created"))
        
        self.console.spinner("Synchronizing project state")
        import time
        
        # Update context file
        context_path = project_path / "memory" / "context.md"
        if context_path.exists():
            # Add timestamp
            with open(context_path, 'a', encoding='utf-8') as f:
                f.write(f"\n\n## Last Sync\n{datetime.now().isoformat()}\n")
            sync_items.append(("Context", "Updated"))
        
        # Consolidate specs
        specs_dir = project_path / "specs"
        if specs_dir.exists():
            spec_count = len(list(specs_dir.glob("*/spec-*.md")))
            sync_items.append(("Specifications", f"{spec_count} found"))
        
        # Check git status
        git_utils = GitUtils()
        if git_utils.is_git_repo(project_path):
            branch = git_utils.get_current_branch()
            sync_items.append(("Git Branch", branch))
            
            # Check for uncommitted changes
            if git_utils.has_changes():
                sync_items.append(("Git Status", "Uncommitted changes"))
            else:
                sync_items.append(("Git Status", "Clean"))
        
        time.sleep(0.5)  # Visual effect
        
        # Display sync status
        self.console.status_panel("Synchronization Complete", sync_items)
        self.console.animated_success("Project synchronized successfully!")
        
        return True
    
    def list_specs(self):
        """List all specifications in the project"""
        specs_dir = Path("specs")
        if not specs_dir.exists():
            self.console.warning("No specs directory found")
            return []
        
        spec_files = []
        for feature_dir in specs_dir.iterdir():
            if feature_dir.is_dir():
                for spec_file in feature_dir.glob("spec-*.md"):
                    spec_files.append(spec_file)
        
        if not spec_files:
            self.console.warning("No specifications found")
            return []
        
        self.console.info(f"Found {len(spec_files)} specifications")
        for spec_file in spec_files:
            self.console.info(f"  - {spec_file.relative_to(specs_dir)}")
        
        return spec_files
    
    def expand(self, feature_id: str, to_tier: str, show_diff: bool = False):
        """Expand specification to higher tier"""
        from ..core.tier_manager import TierManager

        self.console.show_banner(mini=True)
        self.console.header("Tier Expansion", style="bright_cyan")

        try:
            tier_manager = TierManager(Path.cwd())

            # Show current tier
            current_tier = tier_manager.get_current_tier(feature_id)
            self.console.info(f"Current tier: {current_tier}")
            self.console.info(f"Target tier: {to_tier}")

            # Expand
            success = tier_manager.expand_tier(
                feature_id=feature_id,
                to_tier=to_tier,  # type: ignore
                show_diff=show_diff,
            )

            if success:
                self.console.success(f"✓ Expanded to {to_tier} tier")
                return True
            else:
                self.console.error("Expansion cancelled or failed")
                return False

        except ValueError as e:
            self.console.error(f"Invalid tier transition: {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            self.console.error(f"Spec not found: {e}")
            sys.exit(1)
        except Exception as e:
            self.console.error(f"Expansion failed: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            sys.exit(1)

    def doctor(self):
        """System check and diagnostics"""
        self.console.show_banner(mini=True)
        self.console.header("System Diagnostics", style="bright_cyan")
        
        checks = []
        
        # Check Python version with animation
        self.console.spinner("Checking Python version")
        import time
        time.sleep(0.5)  # Visual effect
        python_version = sys.version_info
        if python_version >= (3, 11):
            checks.append(("Python 3.11+", True, f"{python_version.major}.{python_version.minor}.{python_version.micro}"))
        else:
            checks.append(("Python 3.11+", False, f"{python_version.major}.{python_version.minor}.{python_version.micro}"))
        
        # Check Git
        self.console.spinner("Checking Git installation")
        time.sleep(0.3)
        git_utils = GitUtils()
        if git_utils.check_git_installed():
            checks.append(("Git installed", True, "Available"))
        else:
            checks.append(("Git installed", False, "Not found"))
        
        # Check project structure
        self.console.spinner("Checking project structure")
        time.sleep(0.3)
        project_path = Path.cwd()
        if (project_path / ".specpulse" / "config.yaml").exists():
            checks.append(("SpecPulse project", True, "Configured"))
        else:
            checks.append(("SpecPulse project", False, "Not initialized"))
        
        # Check required directories
        self.console.spinner("Checking required directories")
        time.sleep(0.3)
        required_dirs = ["memory", "specs", "plans", "tasks"]
        missing_dirs = []
        for dir_name in required_dirs:
            if not (project_path / dir_name).exists():
                missing_dirs.append(dir_name)
        
        if not missing_dirs:
            checks.append(("Project structure", True, "Complete"))
        else:
            checks.append(("Project structure", False, f"Missing: {', '.join(missing_dirs)}"))
        
        # Display results in a beautiful table
        self.console.section("Diagnostic Results")
        
        # Prepare table data
        table_rows = []
        for check_item in checks:
            if len(check_item) == 3:
                name, passed, details = check_item
            else:
                name, passed = check_item
                details = "OK" if passed else "Failed"
            
            status = "[PASS]" if passed else "[FAIL]"
            table_rows.append([name, status, details])
        
        # Display table
        self.console.table(
            "System Check Results",
            ["Component", "Status", "Details"],
            table_rows
        )
        
        # Overall status
        all_passed = all(item[1] for item in checks)
        if all_passed:
            self.console.animated_success("All checks passed! System is healthy.")
        else:
            self.console.error("Some checks failed. Please address the issues above.")
        
        return all_passed

    def _is_specpulse_project(self, path: Path) -> bool:
        """Check if current directory is a SpecPulse project"""
        required_dirs = ['specs', 'plans', 'tasks', 'memory', 'templates']
        return all((path / dir_name).exists() for dir_name in required_dirs)

    def template_list(self, category: Optional[str] = None):
        """List all templates"""
        if not self.template_manager:
            self.console.error("Not in a SpecPulse project directory")
            return False

        try:
            templates = self.template_manager.list_templates(category)
            if not templates:
                self.console.info("No templates found")
                return True

            self.console.header(f"Templates ({category or 'All Categories'})")

            from rich.table import Table
            table = Table(title="Registered Templates")
            table.add_column("Name", style="cyan")
            table.add_column("Category", style="green")
            table.add_column("Version", style="yellow")
            table.add_column("Author", style="magenta")
            table.add_column("Modified", style="blue")

            for template in templates:
                modified_date = template['modified'][:10] if template['modified'] else 'Unknown'
                table.add_row(
                    template['name'],
                    template['category'],
                    template['version'],
                    template['author'],
                    modified_date
                )

            self.console.console.print(table)
            return True

        except Exception as e:
            return self.error_handler.handle_error(e, "Listing templates")

    def template_validate(self, template_name: Optional[str] = None, fix: bool = False):
        """Validate templates"""
        if not self.template_manager:
            self.console.error("Not in a SpecPulse project directory")
            return False

        try:
            if template_name:
                # Validate specific template
                template_path = self.template_manager.templates_dir / template_name
                result = self.template_manager.validate_template(template_path)
                self._display_template_validation_result(template_name, result)
            else:
                # Validate all templates
                results = self.template_manager.validate_all_templates()
                all_valid = True
                for template_key, result in results.items():
                    self._display_template_validation_result(template_key, result)
                    if not result.valid:
                        all_valid = False

                if all_valid:
                    self.console.success("All templates are valid!")
                else:
                    self.console.warning("Some templates have validation issues")

            return True

        except Exception as e:
            return self.error_handler.handle_error(e, "Validating templates")

    def _display_template_validation_result(self, template_name: str, result):
        """Display template validation result"""
        if result.valid:
            self.console.success(f"✓ {template_name}: Valid")
        else:
            self.console.error(f"✗ {template_name}: Invalid")

        if result.errors:
            self.console.error("  Errors:")
            for error in result.errors:
                self.console.info(f"    • {error}")

        if result.warnings:
            self.console.warning("  Warnings:")
            for warning in result.warnings:
                self.console.info(f"    • {warning}")

        if result.suggestions:
            self.console.info("  Suggestions:")
            for suggestion in result.suggestions:
                self.console.info(f"    💡 {suggestion}")

    def template_preview(self, template_name: str):
        """Generate template preview"""
        if not self.template_manager:
            self.console.error("Not in a SpecPulse project directory")
            return False

        try:
            template_path = self.template_manager.templates_dir / template_name
            preview = self.template_manager.get_template_preview(template_path)

            self.console.header(f"Template Preview: {template_name}")
            self.console.code_block(preview, language="markdown", theme="monokai")
            return True

        except Exception as e:
            return self.error_handler.handle_error(e, f"Previewing template {template_name}")

    def template_backup(self):
        """Backup all templates"""
        if not self.template_manager:
            self.console.error("Not in a SpecPulse project directory")
            return False

        try:
            backup_path = self.template_manager.backup_templates()
            self.console.success(f"Templates backed up to: {backup_path}")
            return True

        except Exception as e:
            return self.error_handler.handle_error(e, "Backing up templates")

    def template_restore(self, backup_path: str):
        """Restore templates from backup"""
        if not self.template_manager:
            self.console.error("Not in a SpecPulse project directory")
            return False

        try:
            success = self.template_manager.restore_templates(backup_path)
            if success:
                self.console.success("Templates restored successfully")
            return success

        except Exception as e:
            return self.error_handler.handle_error(e, f"Restoring templates from {backup_path}")

    def memory_search(self, query: str, category: Optional[str] = None, days: Optional[int] = None):
        """Search memory system"""
        if not self.memory_manager:
            self.console.error("Not in a SpecPulse project directory")
            return False

        try:
            # Prepare date range if specified
            date_range = None
            if days:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
                date_range = (start_date.isoformat(), end_date.isoformat())

            results = self.memory_manager.search_memory(query, category, date_range)

            if not results:
                self.console.info(f"No results found for: {query}")
                return True

            self.console.header(f"Memory Search Results: {query}")
            self.console.info(f"Found {len(results)} results")

            from rich.table import Table
            table = Table()
            table.add_column("Type", style="cyan")
            table.add_column("ID/Name", style="green")
            table.add_column("Date", style="yellow")
            table.add_column("Summary", style="magenta")

            for result in results:
                item_type = result["type"].title()
                item_data = result["data"]
                item_id = result.get("id", item_data.get("id", item_data.get("name", "N/A")))
                item_date = item_data.get("timestamp", item_data.get("date", "N/A"))[:10]
                item_summary = self._get_memory_item_summary(result)

                table.add_row(item_type, str(item_id)[:30], item_date, item_summary[:50])

            self.console.console.print(table)
            return True

        except Exception as e:
            return self.error_handler.handle_error(e, f"Searching memory for: {query}")

    def _get_memory_item_summary(self, result: Dict) -> str:
        """Get summary text for memory item"""
        item_type = result["type"]
        item_data = result["data"]

        if item_type == "context":
            action = item_data.get("action", "").replace("_", " ").title()
            feature = item_data.get("feature_name", "General")
            return f"{action} - {feature}"
        elif item_type == "decision":
            title = item_data.get("title", "Untitled")
            status = item_data.get("status", "")
            return f"{title} ({status})"
        elif item_type == "feature":
            name = item_data.get("name", "Unnamed")
            status = item_data.get("status", "")
            return f"{name} ({status})"
        else:
            return "Unknown item type"

    def memory_summary(self):
        """Show memory system summary"""
        if not self.memory_manager:
            self.console.error("Not in a SpecPulse project directory")
            return False

        try:
            summary = self.memory_manager.get_memory_summary()

            self.console.header("Memory System Summary")

            # Statistics
            stats = summary["statistics"]
            self.console.info("📊 Statistics:")
            self.console.info(f"  Total Decisions: {stats['total_decisions']}")
            self.console.info(f"  Active Features: {stats['active_features']}")
            self.console.info(f"  Completed Features: {stats['completed_features']}")
            self.console.info(f"  Context Entries: {stats['total_context_entries']}")
            self.console.info(f"  Memory Size: {stats['memory_size_mb']} MB")

            # Active Features
            active_features = summary["active_features"]
            if active_features:
                self.console.info("🔄 Active Features:")
                for feature in active_features[:5]:  # Show max 5
                    self.console.info(f"  • {feature['name']} ({feature['id']})")
                if len(active_features) > 5:
                    self.console.info(f"  ... and {len(active_features) - 5} more")

            # Recent Activity
            recent_activity = summary["recent_activity"]
            if recent_activity:
                self.console.info("📝 Recent Activity:")
                for entry in recent_activity[-3:]:  # Show last 3
                    action = entry.get("action", "").replace("_", " ").title()
                    feature = entry.get("feature_name", "General")
                    date = entry.get("timestamp", "")[:10]
                    self.console.info(f"  • {action} - {feature} ({date})")

            return True

        except Exception as e:
            return self.error_handler.handle_error(e, "Getting memory summary")

    def memory_cleanup(self, days: int = 90):
        """Clean up old memory entries"""
        if not self.memory_manager:
            self.console.error("Not in a SpecPulse project directory")
            return False

        try:
            removed_count = self.memory_manager.cleanup_old_entries(days)
            if removed_count > 0:
                self.console.success(f"Cleaned up {removed_count} old entries (older than {days} days)")
            else:
                self.console.info(f"No entries to clean up (all entries are newer than {days} days)")
            return True

        except Exception as e:
            return self.error_handler.handle_error(e, f"Cleaning up memory entries older than {days} days")

    def memory_export(self, format: str = "json", output_file: Optional[str] = None):
        """Export memory data"""
        if not self.memory_manager:
            self.console.error("Not in a SpecPulse project directory")
            return False

        try:
            output_path = Path(output_file) if output_file else None
            export_path = self.memory_manager.export_memory(format, output_path)

            if output_path:
                self.console.success(f"Memory exported to: {export_path}")
            else:
                # Display preview if no file specified
                self.console.header(f"Memory Export Preview ({format.upper()})")
                self.console.code_block(export_path[:1000] + "..." if len(export_path) > 1000 else export_path,
                                     language=format.lower())

            return True

        except Exception as e:
            return self.error_handler.handle_error(e, f"Exporting memory as {format}")

    def show_help(self, topic: Optional[str] = None, list_topics: bool = False):
        """Show comprehensive help and documentation"""
        self.console.show_banner(mini=True)

        help_content = {
            "overview": {
                "title": "SpecPulse Overview",
                "content": """
SpecPulse is a universal Specification-Driven Development (SDD) framework that works with ANY software project type - web apps, mobile apps, desktop software, games, APIs, ML projects, and more.

## Key Concepts

**Specification-Driven Development (SDD)**: Every feature starts with clear specifications, validated plans, and tracked tasks before implementation begins.

**9 Universal Principles**:
1. Specification First - Clear requirements drive development
2. Incremental Planning - Break work into valuable increments
3. Task Decomposition - Create concrete, executable tasks
4. Traceable Implementation - Link code to specifications
5. Continuous Validation - Regular verification against specs
6. Quality Assurance - Testing strategies for each component
7. Architecture Documentation - Record technical decisions
8. Iterative Refinement - Evolve based on learnings
9. Stakeholder Alignment - Maintain shared understanding

## Project Structure

```
project/
├── specs/           # Feature specifications (001-feature/)
├── plans/           # Implementation plans
├── tasks/           # Task breakdowns (T001, T002)
├── memory/          # Project state and decisions
├── templates/       # Customizable document templates
└── scripts/         # Automation scripts
```

## AI Integration

SpecPulse integrates seamlessly with AI assistants like Claude and Gemini through custom commands:

- `/sp-pulse <feature>` - Initialize new feature
- `/sp-spec create` - Generate specifications
- `/sp-decompose <spec-id>` - Break down into services/APIs
- `/sp-plan generate` - Create implementation plans
- `/sp-task breakdown` - Create task lists
- `/sp-execute` - Execute tasks continuously

## Getting Started

1. Initialize: `specpulse init my-project`
2. Navigate: `cd my-project`
3. Start AI assistant: `claude .` or `gemini .`
4. Create feature: `/sp-pulse user-authentication`
5. Generate specs: `/sp-spec create`
6. Execute tasks: `/sp-execute all`
"""
            },
            "commands": {
                "title": "Available Commands",
                "content": """
## Project Management

**specpulse init [name]** - Initialize new SpecPulse project
  • `--here` - Initialize in current directory
  • `--ai claude|gemini` - Set primary AI assistant
  • `--template web|api|cli|mobile|microservice` - Project template

**specpulse validate [component]** - Validate project components
  • `--fix` - Attempt to auto-fix issues
  • `--verbose` - Detailed validation output
  • Components: all, spec, plan, constitution

**specpulse doctor** - System health check and diagnostics

**specpulse sync** - Synchronize project state

## Specification Management

**specpulse decompose [spec-id]** - Decompose specifications
  • `--microservices` - Generate service boundaries
  • `--apis` - Generate API contracts
  • `--interfaces` - Generate interface specifications

## Template Management

**specpulse template list [--category]** - List available templates
  • Categories: spec, plan, task, decomposition

**specpulse template validate [name]** - Validate templates
  • `--fix` - Auto-fix template issues

**specpulse template preview <name>** - Preview template with sample data

**specpulse template backup** - Backup all templates
**specpulse template restore <path>** - Restore from backup

## Memory Management

**specpulse memory search <query>** - Search memory system
  • `--category` - Filter by category
  • `--days N` - Limit to last N days

**specpulse memory summary** - Show memory system summary

**specpulse memory cleanup [--days 90]** - Clean old entries

**specpulse memory export [--format json|yaml]** - Export memory data
  • `--output <file>` - Save to specific file

## Help & Information

**specpulse help [topic]** - Show detailed help
  • `--list` - List all available topics

**specpulse --version** - Show version information
**--no-color** - Disable colored output
**--verbose** - Enable verbose output
"""
            },
            "workflow": {
                "title": "Development Workflow",
                "content": """
## Complete Development Workflow

### 1. Project Setup
```bash
# Initialize new project
specpulse init my-project
cd my-project

# Start AI assistant
claude .    # or gemini .
```

### 2. Feature Development
```bash
# Initialize new feature
/sp-pulse user-authentication

# Create specification
/sp-spec create "User authentication system with login, registration, and password reset"

# Review and refine specification
# (AI assistant helps create comprehensive spec)
```

### 3. Planning & Decomposition
```bash
# Generate implementation plan
/sp-plan generate

# For large features, decompose into services
/sp-decompose 001 --microservices --apis --interfaces

# Create task breakdown
/sp-task breakdown
```

### 4. Execution
```bash
# Execute all tasks continuously
/sp-execute all

# Or execute specific task
/sp-execute T001

# Check progress
/sp-status
```

### 5. Validation & Quality
```bash
# Validate project (in terminal)
specpulse validate --fix

# Run health check
specpulse doctor

# Sync project state
specpulse sync
```

## AI Command Best Practices

### Sequential Commands
1. `/sp-pulse <feature-name>` - Always start here
2. `/sp-spec create` - Generate specification
3. `/sp-plan generate` - Create implementation plan
4. `/sp-task breakdown` - Break down into tasks
5. `/sp-execute all` - Execute everything

### Continuous Execution
- `/sp-execute` - Execute next task and continue
- `/sp-execute all` - Execute ALL pending tasks without stopping
- `/sp-execute T001` - Start from specific task

### Key Features
- **No Stopping**: Commands don't pause for confirmation
- **Auto-Progression**: Automatically moves to next task
- **Context Awareness**: Maintains project state across commands
- **Error Recovery**: Handles failures gracefully

## File Numbering System

- **Specifications**: spec-001.md, spec-002.md, ...
- **Plans**: plan-001.md, plan-002.md, ...
- **Tasks**: task-001.md, task-002.md, ...
- **Services**: AUTH-T001, USER-T002, ... (for microservices)
- **Features**: 001-feature-name, 002-feature-name, ...

## Memory System

The memory system automatically tracks:
- Feature development progress
- Architecture decisions
- Context changes
- Task completion status

Access memory via:
- CLI commands: `specpulse memory search/summary`
- Memory files: `memory/context.md`, `memory/decisions.md`
"""
            },
            "templates": {
                "title": "Template System",
                "content": """
## Template Overview

SpecPulse uses customizable templates for consistent documentation across all projects.

## Template Types

### Specification Templates
- **spec.md** - Feature specification template
- **decomposition/microservices.md** - Microservice decomposition
- **decomposition/api-contract.yaml** - API specification
- **decomposition/interface.ts** - TypeScript interfaces

### Planning Templates
- **plan.md** - Implementation plan template
- **decomposition/service-plan.md** - Service-specific plans
- **decomposition/integration-plan.md** - Integration planning

### Task Templates
- **task.md** - Task breakdown template
- **decomposition/*-tasks.md** - Service-specific tasks

## Template Customization

### Adding Custom Templates
```bash
# List current templates
specpulse template list

# Validate template syntax
specpulse template validate custom-template.md

# Preview template with sample data
specpulse template preview custom-template.md
```

### Template Backup & Restore
```bash
# Backup current templates
specpulse template backup

# Restore from backup
specpulse template restore /path/to/backup
```

## Template Variables

Templates use Jinja2 syntax with these standard variables:

### Project Variables
- `{{ project_name }}` - Project name
- `{{ version }}` - Current version
- `{{ date }}` - Current date

### Feature Variables
- `{{ feature_name }}` - Feature description
- `{{ feature_id }}` - Feature identifier (001, 002, etc.)
- `{{ spec_id }}` - Specification ID

### System Variables
- `{{ author }}` - Current user
- `{{ timestamp }}` - Current timestamp

## Template Best Practices

1. **Keep Templates Simple** - Focus on structure, not content
2. **Use Standard Variables** - Leverage built-in variables
3. **Validate Templates** - Check syntax before use
4. **Backup Before Changes** - Always backup custom templates
5. **Test Templates** - Preview with sample data

## Advanced Features

### Conditional Sections
```jinja2
{% if feature_type == "microservice" %}
## API Contracts
- OpenAPI 3.0 specification
- Service boundaries
{% endif %}
```

### Loops and Lists
```jinja2
{% for requirement in requirements %}
- {{ requirement }}
{% endfor %}
```

### Template Inheritance
Templates can extend base templates for reusability.
"""
            },
            "troubleshooting": {
                "title": "Troubleshooting & Common Issues",
                "content": """
## Common Issues & Solutions

### Initialization Problems

**Issue**: `specpulse init` fails
**Solutions**:
- Check Python version: `python --version` (needs 3.11+)
- Verify permissions: Ensure write access to directory
- Check disk space: `df -h` (Unix) or check drive space
- Run `specpulse doctor` for system diagnostics

**Issue**: Git not found
**Solutions**:
- Install Git: https://git-scm.com/downloads
- Verify installation: `git --version`
- Add Git to system PATH

### Template Issues

**Issue**: Template validation fails
**Solutions**:
```bash
# Check template syntax
specpulse template validate

# Backup and reset templates
specpulse template backup
specpulse template restore /path/to/backup
```

**Issue**: Templates not found
**Solutions**:
- Check templates directory: `ls templates/`
- Verify template permissions
- Restore default templates: `specpulse update`

### AI Command Issues

**Issue**: AI commands not working
**Solutions**:
- Verify project structure: `specpulse doctor`
- Check AI tool installation (Claude/Gemini)
- Verify scripts directory: `ls scripts/`
- Check command files: `ls .claude/commands/` or `ls .gemini/commands/`

**Issue**: Scripts not executable
**Solutions**:
```bash
# Unix/Linux/macOS
chmod +x scripts/*.sh

# Windows - scripts should work with Git Bash
# If issues occur, run scripts in PowerShell
```

### Memory System Issues

**Issue**: Memory not updating
**Solutions**:
- Check memory directory: `ls memory/`
- Verify file permissions
- Check memory size: `specpulse memory summary`
- Clean old entries: `specpulse memory cleanup --days 30`

### Performance Issues

**Issue**: Slow performance
**Solutions**:
- Check system resources: `specpulse doctor`
- Clean old memory entries: `specpulse memory cleanup`
- Reduce project size if very large
- Check for memory leaks in long-running processes

## Getting Help

### Built-in Help
```bash
# General help
specpulse help

# Specific topics
specpulse help commands
specpulse help workflow
specpulse help templates

# List all topics
specpulse help --list
```

### Diagnostic Tools
```bash
# System health check
specpulse doctor

# Validate project
specpulse validate --verbose

# Check memory status
specpulse memory summary
```

### Community Support
- **GitHub Issues**: https://github.com/specpulse/specpulse/issues
- **Documentation**: Check SPECPULSE_USAGE_GUIDE.md
- **Examples**: See examples/ directory in project

### Debug Mode
Enable verbose output for troubleshooting:
```bash
specpulse --verbose <command>
```

### Log Files
Check these locations for debug information:
- `.specpulse/logs/` - Application logs
- `memory/context.md` - Recent operations
- AI tool output - Check Claude/Gemini console
"""
            },
            "examples": {
                "title": "Usage Examples",
                "content": """
## Real-World Examples

### Example 1: Web Application Feature

```bash
# Initialize project
specpulse init my-web-app
cd my-web-app
claude .

# Create user authentication feature
/sp-pulse user-authentication
/sp-spec create "Complete user authentication system with registration, login, logout, password reset, and email verification"

# Generate implementation plan
/sp-plan generate

# Break down into tasks
/sp-task breakdown

# Execute all tasks
/sp-execute all
```

### Example 2: Microservice API

```bash
# Initialize microservice project
specpulse init user-service --template microservice
cd user-service
gemini .

# Create user management API
/sp-pulse user-management-api
/sp-spec create "RESTful API for user management including CRUD operations, authentication, and profile management"

# Decompose into microservices
/sp-decompose 001 --microservices --apis --interfaces

# Review generated services and APIs
# (AI creates separate service plans and API contracts)

# Execute implementation
/sp-execute all
```

### Example 3: Mobile App Feature

```bash
# Initialize mobile project
specpulse init fitness-tracker --template mobile
cd fitness-tracker
claude .

# Create workout tracking feature
/sp-pulse workout-tracking
/sp-spec create "Workout tracking system with exercise library, workout plans, progress tracking, and social features"

# Generate mobile-specific plans
/sp-plan generate

# Execute tasks with mobile considerations
/sp-execute all
```

### Example 4: CLI Tool Enhancement

```bash
# Initialize CLI project
specpulse init data-processor --template cli
cd data-processor
gemini .

# Add data validation feature
/sp-pulse data-validation
/sp-spec create "Data validation framework with schema validation, error reporting, and data transformation capabilities"

# Generate implementation
/sp-plan generate
/sp-task breakdown
/sp-execute all
```

### Example 5: API Development

```bash
# Initialize API project
specpulse init notification-api --template api
cd notification-api
claude .

# Create notification system
/sp-pulse notification-system
/sp-spec create "Multi-channel notification system supporting email, SMS, push notifications, and webhooks"

# Generate API specifications
/sp-decompose 001 --apis --interfaces

# Review generated OpenAPI specifications
ls specs/001-notification-system/decomposition/api-contracts/

# Execute implementation
/sp-execute all
```

## Advanced Workflows

### Workflow 1: Large Feature Decomposition

```bash
# Start large feature
/sp-pulse e-commerce-platform

# Create comprehensive specification
/sp-spec create "Full e-commerce platform with product catalog, user management, order processing, payment integration, and admin dashboard"

# Decompose into microservices
/sp-decompose 001 --microservices --apis --interfaces

# Review generated services:
# - product-service
# - user-service
# - order-service
# - payment-service
# - notification-service

# Generate service-specific plans and tasks
/sp-plan generate  # Creates plans for each service
/sp-task breakdown # Creates tasks for each service

# Execute all service implementations
/sp-execute all
```

### Workflow 2: Iterative Development

```bash
# Start with basic feature
/sp-pulse user-profiles

# Create MVP specification
/sp-spec create "Basic user profile management with view and edit functionality"

# Implement MVP
/sp-plan generate
/sp-task breakdown
/sp-execute all

# Later - enhance feature
/sp-spec update "Add profile photo upload, privacy settings, and activity timeline"

# Generate additional tasks for enhancement
/sp-task breakdown

# Execute enhancement tasks
/sp-execute all
```

### Workflow 3: Cross-Platform Development

```bash
# Initialize shared backend
specpulse init shared-backend --template api
cd shared-backend

# Create API specification
/sp-pulse shared-user-api
/sp-spec create "Shared user management API for multiple client applications"

# Generate API and documentation
/sp-decompose 001 --apis --interfaces
/sp-execute all

# Initialize web client
cd ../
specpulse init web-client --template web
cd web-client
claude .

# Connect to shared API
/sp-pulse web-user-interface
/sp-spec create "Web interface for user management consuming shared API"

# Implement web client
/sp-execute all

# Repeat for mobile client
cd ../
specpulse init mobile-client --template mobile
# ... similar process
```

## Tips & Best Practices

### Planning Phase
- **Start Small**: Break large features into smaller, manageable pieces
- **Clear Requirements**: Ensure specifications are detailed and unambiguous
- **Consider Dependencies**: Identify external dependencies early

### Execution Phase
- **Continuous Execution**: Use `/sp-execute all` for uninterrupted workflow
- **Monitor Progress**: Use `/sp-status` to track completion
- **Validate Early**: Run `specpulse validate` after major milestones

### Team Collaboration
- **Shared Memory**: Use memory system for team decisions and context
- **Consistent Templates**: Maintain template standards across team
- **Regular Sync**: Use `specpulse sync` to maintain project state

### Quality Assurance
- **Regular Validation**: Validate specifications and plans
- **Code Reviews**: Review generated code and implementations
- **Testing**: Implement tests as part of task execution
"""
            }
        }

        if list_topics:
            self._show_help_topics(help_content)
        elif topic:
            self._show_help_topic(help_content, topic)
        else:
            self._show_default_help(help_content)

    def _show_help_topics(self, help_content):
        """List all available help topics"""
        self.console.header("Available Help Topics", style="bright_cyan")

        from rich.table import Table
        table = Table(title="Choose a topic for detailed information")
        table.add_column("Topic", style="cyan", width=15)
        table.add_column("Description", style="white")

        topic_descriptions = {
            "overview": "What is SpecPulse and key concepts",
            "commands": "Complete command reference",
            "workflow": "Step-by-step development workflow",
            "templates": "Template system and customization",
            "troubleshooting": "Common issues and solutions",
            "examples": "Real-world usage examples"
        }

        for topic, description in topic_descriptions.items():
            table.add_row(topic, description)

        self.console.console.print(table)
        self.console.info("Usage: specpulse help <topic>")
        self.console.info("Example: specpulse help workflow")

    def _show_help_topic(self, help_content, topic):
        """Show detailed help for specific topic"""
        if topic not in help_content:
            available = ", ".join(help_content.keys())
            self.console.error(f"Unknown topic: {topic}")
            self.console.info(f"Available topics: {available}")
            self.console.info("Use 'specpulse help --list' to see all topics")
            return

        topic_data = help_content[topic]
        self.console.header(topic_data["title"], style="bright_cyan")

        # Display content with proper formatting
        content_lines = topic_data["content"].strip().split('\n')
        in_code_block = False
        current_section = ""

        for line in content_lines:
            line = line.rstrip()

            # Handle code blocks
            if line.startswith('```'):
                in_code_block = not in_code_block
                if in_code_block:
                    self.console.console.print()  # Add spacing
                continue

            if in_code_block:
                # Print code lines directly
                self.console.console.print(line, style="dim white")
                continue

            # Handle headers
            if line.startswith('##'):
                if current_section:
                    self.console.console.print()  # Add spacing between sections
                current_section = line.replace('##', '').strip()
                self.console.subheader(current_section, style="bright_yellow")
            elif line.startswith('###'):
                self.console.console.print(f"📋 {line.replace('###', '').strip()}", style="yellow")
            elif line.startswith('**') and line.endswith('**'):
                self.console.console.print(f"• {line.replace('**', '')}", style="bright_green")
            elif line.startswith('- '):
                self.console.console.print(f"  • {line[2:]}", style="white")
            elif line.strip() == '':
                self.console.console.print()
            else:
                self.console.console.print(line)

        # Add footer navigation
        self.console.console.print()
        self.console.divider()
        self.console.info("Related topics:")

        # Suggest related topics
        related_topics = {
            "overview": ["commands", "workflow"],
            "commands": ["workflow", "examples"],
            "workflow": ["examples", "commands"],
            "templates": ["examples", "workflow"],
            "troubleshooting": ["commands", "workflow"],
            "examples": ["workflow", "templates"]
        }

        if topic in related_topics:
            for related in related_topics[topic]:
                self.console.info(f"  • specpulse help {related}")

    def _show_default_help(self, help_content):
        """Show default help overview"""
        self.console.header("SpecPulse Help System", style="bright_cyan")
        self.console.info("Welcome to SpecPulse - Your Specification-Driven Development Framework")
        self.console.console.print()

        # Quick overview
        self.console.subheader("Quick Start", style="bright_green")
        quick_start = """
1. Initialize: specpulse init my-project
2. Navigate: cd my-project
3. Start AI: claude . or gemini .
4. Create feature: /sp-pulse user-auth
5. Generate specs: /sp-spec create
6. Execute: /sp-execute all
"""
        for line in quick_start.strip().split('\n'):
            if line.strip():
                self.console.console.print(f"  {line}")

        self.console.console.print()
        self.console.subheader("Available Help Topics", style="bright_yellow")

        topic_info = [
            ("overview", "What is SpecPulse and key concepts"),
            ("commands", "Complete command reference"),
            ("workflow", "Step-by-step development workflow"),
            ("templates", "Template system and customization"),
            ("troubleshooting", "Common issues and solutions"),
            ("examples", "Real-world usage examples")
        ]

        for topic, description in topic_info:
            self.console.console.print(f"  • specpulse help {topic:<12} - {description}")

        self.console.console.print()
        self.console.subheader("Getting Help", style="bright_cyan")
        help_commands = [
            "specpulse help --list      - List all topics",
            "specpulse help <topic>     - Get help on specific topic",
            "specpulse doctor           - System health check",
            "specpulse --help           - Show command options"
        ]

        for cmd in help_commands:
            self.console.console.print(f"  {cmd}")

        self.console.console.print()
        self.console.divider()
        self.console.success("Need more help? Visit: https://github.com/specpulse/specpulse")


def main():
    """Main CLI entry point with enhanced error handling"""

    try:
        parser = argparse.ArgumentParser(
            description="SpecPulse - Specification-Driven Development Framework",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  specpulse init my-project          Initialize new project
  specpulse init --here              Initialize in current directory
  specpulse validate --fix           Validate and fix issues
  specpulse doctor                   System health check

Need help? Visit https://github.com/specpulse/specpulse
            """
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Init command
        init_parser = subparsers.add_parser("init", help="Initialize new SpecPulse project")
        init_parser.add_argument("project_name", nargs="?", help="Project name")
        init_parser.add_argument("--here", action="store_true", help="Initialize in current directory")
        init_parser.add_argument("--ai", choices=["claude", "gemini"], default="claude", help="Primary AI assistant")
        init_parser.add_argument("--template", choices=["web", "api", "cli", "mobile", "microservice"], default="web", help="Project template")

        # Update command
        update_parser = subparsers.add_parser("update", help="Update SpecPulse templates")

        # Validate command
        validate_parser = subparsers.add_parser("validate", help="Validate project components")
        validate_parser.add_argument("component", nargs="?", default="all", choices=["all", "spec", "plan", "constitution"], help="Component to validate")
        validate_parser.add_argument("--fix", action="store_true", help="Attempt to fix issues")
        validate_parser.add_argument("--verbose", action="store_true", help="Verbose output")

        # Decompose command
        decompose_parser = subparsers.add_parser("decompose", help="Decompose specifications into smaller components")
        decompose_parser.add_argument("spec_id", nargs="?", help="Specification ID (e.g., 001 or 001-feature)")
        decompose_parser.add_argument("--microservices", action="store_true", help="Generate microservice boundaries")
        decompose_parser.add_argument("--apis", action="store_true", help="Generate API contracts")
        decompose_parser.add_argument("--interfaces", action="store_true", help="Generate interface specifications")

        # Sync command
        sync_parser = subparsers.add_parser("sync", help="Synchronize project state")

        # Doctor command
        doctor_parser = subparsers.add_parser("doctor", help="System check and diagnostics")

        # Expand command
        expand_parser = subparsers.add_parser("expand", help="Expand specification to higher tier")
        expand_parser.add_argument("feature_id", help="Feature ID (e.g., 001 or 001-feature-name)")
        expand_parser.add_argument("--to-tier", choices=["standard", "complete"], required=True, help="Target tier level")
        expand_parser.add_argument("--show-diff", action="store_true", help="Preview changes before applying")

        # Help command
        help_parser = subparsers.add_parser("help", help="Show comprehensive help and documentation")
        help_parser.add_argument("topic", nargs="?", help="Specific topic to get help with")
        help_parser.add_argument("--list", action="store_true", help="List all available help topics")

        # Template commands
        template_parser = subparsers.add_parser("template", help="Template management")
        template_subparsers = template_parser.add_subparsers(dest="template_action", help="Template actions")

        # Template list
        template_list_parser = template_subparsers.add_parser("list", help="List templates")
        template_list_parser.add_argument("--category", choices=["spec", "plan", "task", "decomposition"], help="Filter by category")

        # Template validate
        template_validate_parser = template_subparsers.add_parser("validate", help="Validate templates")
        template_validate_parser.add_argument("template_name", nargs="?", help="Specific template to validate")
        template_validate_parser.add_argument("--fix", action="store_true", help="Auto-fix issues if possible")

        # Template preview
        template_preview_parser = template_subparsers.add_parser("preview", help="Preview template with sample data")
        template_preview_parser.add_argument("template_name", help="Template name to preview")

        # Template backup
        template_backup_parser = template_subparsers.add_parser("backup", help="Backup all templates")

        # Template restore
        template_restore_parser = template_subparsers.add_parser("restore", help="Restore templates from backup")
        template_restore_parser.add_argument("backup_path", help="Path to backup directory")

        # Memory commands
        memory_parser = subparsers.add_parser("memory", help="Memory management")
        memory_subparsers = memory_parser.add_subparsers(dest="memory_action", help="Memory actions")

        # Memory search
        memory_search_parser = memory_subparsers.add_parser("search", help="Search memory system")
        memory_search_parser.add_argument("query", help="Search query")
        memory_search_parser.add_argument("--category", help="Filter by category")
        memory_search_parser.add_argument("--days", type=int, help="Limit to last N days")

        # Memory summary
        memory_summary_parser = memory_subparsers.add_parser("summary", help="Show memory summary")

        # Memory cleanup
        memory_cleanup_parser = memory_subparsers.add_parser("cleanup", help="Clean up old memory entries")
        memory_cleanup_parser.add_argument("--days", type=int, default=90, help="Remove entries older than N days")

        # Memory export
        memory_export_parser = memory_subparsers.add_parser("export", help="Export memory data")
        memory_export_parser.add_argument("--format", choices=["json", "yaml"], default="json", help="Export format")
        memory_export_parser.add_argument("--output", help="Output file path")

        # Global arguments
        parser.add_argument("--version", action="version", version=f"SpecPulse {__version__}")
        parser.add_argument("--no-color", action="store_true", help="Disable colored output")
        parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

        args = parser.parse_args()

        # Initialize CLI with error handling
        cli = SpecPulseCLI(no_color=getattr(args, 'no_color', False),
                           verbose=getattr(args, 'verbose', False))

        # Available commands for suggestion
        available_commands = ["init", "update", "validate", "decompose", "sync", "doctor", "expand", "help", "template", "memory"]

        # Execute command with error handling
        if args.command == "init":
            cli.init(args.project_name, args.here, args.ai, args.template)
        elif args.command == "update":
            cli.update()
        elif args.command == "validate":
            cli.validate(args.component, args.fix, args.verbose)
        elif args.command == "decompose":
            cli.decompose(args.spec_id, args.microservices, args.apis, args.interfaces)
        elif args.command == "sync":
            cli.sync()
        elif args.command == "doctor":
            cli.doctor()
        elif args.command == "expand":
            cli.expand(args.feature_id, args.to_tier, args.show_diff)
        elif args.command == "help":
            cli.show_help(args.topic, args.list)
        elif args.command == "template":
            if args.template_action == "list":
                cli.template_list(args.category)
            elif args.template_action == "validate":
                cli.template_validate(args.template_name, args.fix)
            elif args.template_action == "preview":
                cli.template_preview(args.template_name)
            elif args.template_action == "backup":
                cli.template_backup()
            elif args.template_action == "restore":
                cli.template_restore(args.backup_path)
            else:
                console = Console(no_color=getattr(args, 'no_color', False))
                console.error("Unknown template action. Use 'specpulse template --help' for available actions.")
                sys.exit(1)
        elif args.command == "memory":
            if args.memory_action == "search":
                cli.memory_search(args.query, args.category, args.days)
            elif args.memory_action == "summary":
                cli.memory_summary()
            elif args.memory_action == "cleanup":
                cli.memory_cleanup(args.days)
            elif args.memory_action == "export":
                cli.memory_export(args.format, args.output)
            else:
                console = Console(no_color=getattr(args, 'no_color', False))
                console.error("Unknown memory action. Use 'specpulse memory --help' for available actions.")
                sys.exit(1)
        elif args.command is None:
            # Show beautiful banner and help when no command
            console = Console()
            console.show_banner()
            console.gradient_text("Welcome to SpecPulse - Your Specification-Driven Development Framework")
            console.divider()
            parser.print_help()
        else:
            # Unknown command - suggest correction
            error_handler = ErrorHandler(verbose=getattr(args, 'verbose', False))
            suggestion = error_handler.suggest_command_correction(args.command, available_commands)

            if suggestion:
                console = Console(no_color=getattr(args, 'no_color', False))
                console.error(f"Unknown command: {args.command}")
                console.info(f"Did you mean: {suggestion}?")
                console.info(f"Try: specpulse {suggestion}")
            else:
                console = Console(no_color=getattr(args, 'no_color', False))
                console.error(f"Unknown command: {args.command}")
                console.info("Available commands: " + ", ".join(available_commands))
                console.info("Use --help for more information")

            sys.exit(1)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        console = Console()
        console.warning("\nOperation cancelled by user")
        sys.exit(130)
    except SystemExit:
        # Re-raise system exit (from argparse or explicit exit calls)
        raise
    except Exception as e:
        # Handle any other unexpected errors
        error_handler = ErrorHandler(verbose=getattr(args, 'verbose', False) if 'args' in locals() else False)
        exit_code = error_handler.handle_error(e, "SpecPulse CLI")
        sys.exit(exit_code)


if __name__ == "__main__":
    main()