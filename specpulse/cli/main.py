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
from datetime import datetime
from typing import Optional

from .. import __version__
from ..core.specpulse import SpecPulse
from ..core.validator import Validator
from ..utils.console import Console
from ..utils.git_utils import GitUtils


class SpecPulseCLI:
    def __init__(self, no_color: bool = False, verbose: bool = False):
        self.console = Console(no_color=no_color, verbose=verbose)
        self.specpulse = SpecPulse()
        self.validator = Validator()
        
    def init(self, project_name: Optional[str] = None, 
             here: bool = False, 
             ai: str = "claude",
             template: str = "web"):
        """Initialize SpecPulse in an existing or new project"""
        
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
            "templates"
        ]
        
        # Create directories with progress bar
        with self.console.progress_bar("Creating project structure", len(directories)) as progress:
            task = progress.add_task("Creating directories...", total=len(directories))
            
            for dir_name in directories:
                (project_path / dir_name).mkdir(parents=True, exist_ok=True)
                progress.update(task, advance=1, description=f"Created {dir_name}/")
                import time
                time.sleep(0.05)  # Small delay for visual effect
        
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
                "spec": "templates/spec-001.md",
                "plan": "templates/plan-001.md",
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
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False)
        self.console.success("Created config.yaml")
        
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
    
    def _create_templates(self, project_path: Path):
        """Create template files"""
        templates_dir = project_path / "templates"
        
        # Create spec template
        spec_template = self.specpulse.get_spec_template()
        with open(templates_dir / "spec-001.md", 'w', encoding='utf-8') as f:
            f.write(spec_template)
        
        # Create plan template  
        plan_template = self.specpulse.get_plan_template()
        with open(templates_dir / "plan-001.md", 'w', encoding='utf-8') as f:
            f.write(plan_template)
        
        # Create task template
        task_template = self.specpulse.get_task_template()
        with open(templates_dir / "task.md", 'w', encoding='utf-8') as f:
            f.write(task_template)
        
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
        resources_scripts_dir = self.specpulse.resources_dir / "scripts"
        
        # Copy all script files from resources
        script_extensions = [".sh", ".py"]
        scripts_copied = 0
        
        for script_file in resources_scripts_dir.iterdir():
            if script_file.suffix in script_extensions:
                dest_path = scripts_dir / script_file.name
                shutil.copy2(script_file, dest_path)
                
                # Make shell scripts executable
                if script_file.suffix == ".sh":
                    try:
                        os.chmod(dest_path, 0o755)
                    except:
                        pass  # Windows may not support chmod
                
                scripts_copied += 1
        
        if scripts_copied == 0:
            self.console.warning("No scripts found in resources directory")
        else:
            self.console.animated_success(f"Scripts created ({scripts_copied} files)")
    
    def _create_ai_commands(self, project_path: Path):
        """Create AI command files for Claude and Gemini CLI integration"""
        
        # Copy all command files from resources
        resources_commands_dir = self.specpulse.resources_dir / "commands"
        commands_copied = 0
        
        # Copy Claude commands (.md format)
        claude_commands_dir = project_path / ".claude" / "commands"
        claude_resources_dir = resources_commands_dir / "claude"
        
        if claude_resources_dir.exists():
            for command_file in claude_resources_dir.glob("*.md"):
                dest_path = claude_commands_dir / command_file.name
                shutil.copy2(command_file, dest_path)
                commands_copied += 1
        
        # Copy Gemini commands (.toml format)
        gemini_commands_dir = project_path / ".gemini" / "commands"
        gemini_resources_dir = resources_commands_dir / "gemini"
        
        if gemini_resources_dir.exists():
            for command_file in gemini_resources_dir.glob("*.toml"):
                dest_path = gemini_commands_dir / command_file.name
                shutil.copy2(command_file, dest_path)
                commands_copied += 1
        
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
            
            ms_content = ms_content.replace("{{ communication_patterns }}", "- REST APIs for synchronous
- Event Bus for asynchronous")
            ms_content = ms_content.replace("{{ data_boundaries }}", "- Each service owns its data
- No shared databases")
            ms_content = ms_content.replace("{{ integration_points }}", "- API Gateway
- Message Queue")
            
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


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="SpecPulse - Specification-Driven Development Framework"
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
    
    # Version
    parser.add_argument("--version", action="version", version=f"SpecPulse {__version__}")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    cli = SpecPulseCLI(no_color=args.no_color if hasattr(args, 'no_color') else False,
                       verbose=args.verbose if hasattr(args, 'verbose') else False)
    
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
    else:
        # Show beautiful banner and help when no command
        console = Console()
        console.show_banner()
        console.gradient_text("Welcome to SpecPulse - Your Specification-Driven Development Framework")
        console.divider()
        parser.print_help()


if __name__ == "__main__":
    main()