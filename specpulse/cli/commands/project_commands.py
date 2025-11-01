"""
Project Commands

This module handles project-level commands like init, update, and doctor.
"""

from pathlib import Path
from typing import Optional
import sys

from ...core.specpulse import SpecPulse
from ...core.validator import Validator
from ...core.path_manager import PathManager
from ...utils.console import Console
from ...utils.error_handler import SpecPulseError


class ProjectCommands:
    """Project-level command implementations"""

    def __init__(self, console: Console, project_root: Path):
        self.console = console
        self.project_root = project_root
        self.specpulse = SpecPulse()
        # Initialize PathManager for directory structure handling
        self.path_manager = PathManager(project_root, use_legacy_structure=False)

    def init(self, project_name: Optional[str] = None, here: bool = False,
             ai: Optional[str] = None, template_source: str = 'local', **kwargs):
        """
        Initialize a new SpecPulse project

        Args:
            project_name: Name of the project
            here: Initialize in current directory
            ai: AI assistant to configure (claude or gemini)
            template_source: Template source (local or remote)
        """
        # Skip banner for now to avoid Unicode issues
        # self.console.show_banner()
        # self.console.pulse_animation("Initializing SpecPulse Framework", duration=1.0)

        # Delegate to SpecPulse.init()
        result = self.specpulse.init(
            project_name=project_name,
            here=here,
            ai_assistant=ai,
            template_source=template_source,
            console=self.console
        )

        # Handle result with minimal output to avoid Unicode issues
        if result.get("status") == "success":
            print(f"Project initialized successfully!")
            print(f"Project: {result['project_name']}")
            print(f"Path: {result['project_path']}")
            if result.get("ai_assistant"):
                print(f"AI Assistant: {result['ai_assistant']}")
            return result
        else:
            print(f"Initialization failed: {result.get('error', 'Unknown error')}")
            return result

    def update(self, force: bool = False, **kwargs):
        """
        Update SpecPulse to latest version

        Args:
            force: Force update without confirmation
        """
        from ...utils.version_check import check_pypi_version, get_update_message, compare_versions
        from ... import __version__

        self.console.info("Checking for updates...")

        latest = check_pypi_version(timeout=5)
        if not latest:
            self.console.warning("Could not check for updates (network issue)")
            return

        if compare_versions(latest, __version__) > 0:
            message = get_update_message(__version__, latest)
            self.console.info(message)

            if force or self.console.confirm("Update now?"):
                import subprocess
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "specpulse"], check=True)
                    self.console.success(f"Successfully updated to v{latest}")
                except subprocess.CalledProcessError as e:
                    raise SpecPulseError(f"Update failed: {e}")
        else:
            self.console.success(f"Already on latest version (v{__version__})")

    def doctor(self, fix: bool = False, component: str = 'all', **kwargs):
        """
        Run comprehensive health check

        Args:
            fix: Automatically fix issues
            component: Component to check
        """
        validator = Validator(self.project_root)

        self.console.info("Running SpecPulse Doctor...")
        self.console.info("=" * 50)

        # Check project structure
        self.console.info("\n[1/5] Checking project structure...")
        structure_ok = self._check_structure()

        # Check templates
        self.console.info("\n[2/5] Checking templates...")
        templates_ok = self._check_templates()

        # Check memory files
        self.console.info("\n[3/5] Checking memory files...")
        memory_ok = self._check_memory()

        # Check git repository
        self.console.info("\n[4/5] Checking git repository...")
        git_ok = self._check_git()

        # Check AI commands
        self.console.info("\n[5/5] Checking AI commands...")
        ai_ok = self._check_ai_commands()

        # Summary
        self.console.info("\n" + "=" * 50)
        self.console.info("Doctor Summary:")
        checks = {
            "Project Structure": structure_ok,
            "Templates": templates_ok,
            "Memory Files": memory_ok,
            "Git Repository": git_ok,
            "AI Commands": ai_ok
        }

        all_ok = all(checks.values())
        for check, status in checks.items():
            status_icon = "[OK]" if status else "[FAIL]"
            self.console.info(f"  {status_icon} {check}")

        if all_ok:
            self.console.success("\n[SUCCESS] All checks passed! Project is healthy.")
        else:
            self.console.warning("\n[WARNING] Some checks failed. Run with --fix to attempt repairs.")

        return all_ok

    def _check_structure(self) -> bool:
        """Check project directory structure"""
        # Check if we have a .specpulse directory (new structure) or legacy structure
        specpulse_dir = self.project_root / ".specpulse"
        if specpulse_dir.exists():
            # New structure - check .specpulse subdirectories
            required_dirs = ['.specpulse/specs', '.specpulse/plans', '.specpulse/tasks', '.specpulse/memory', '.specpulse/templates']
            all_exist = all((self.project_root / d).exists() for d in required_dirs)

            if all_exist:
                self.console.success("  [OK] All required directories exist (.specpulse structure)")
            else:
                missing = [d for d in required_dirs if not (self.project_root / d).exists()]
                self.console.error(f"  [FAIL] Missing directories: {', '.join(missing)}")

            return all_exist
        else:
            # Legacy structure - check root-level directories
            required_dirs = ['specs', 'plans', 'tasks', 'memory', 'templates']
            all_exist = all((self.project_root / d).exists() for d in required_dirs)

            if all_exist:
                self.console.success("  [OK] All required directories exist (legacy structure)")
            else:
                missing = [d for d in required_dirs if not (self.project_root / d).exists()]
                self.console.error(f"  [FAIL] Missing directories: {', '.join(missing)}")

            return all_exist

    def _check_templates(self) -> bool:
        """Check template files"""
        # Check if we have .specpulse directory (new structure) or legacy structure
        specpulse_dir = self.project_root / ".specpulse"
        if specpulse_dir.exists():
            # New structure - templates are in .specpulse/templates
            templates_dir = self.project_root / ".specpulse" / "templates"
        else:
            # Legacy structure - templates are in root templates directory
            templates_dir = self.project_root / "templates"

        if not templates_dir.exists():
            self.console.error("  [FAIL] Templates directory not found")
            return False

        required_templates = ['spec.md', 'plan.md', 'task.md']
        all_exist = all((templates_dir / t).exists() for t in required_templates)

        if all_exist:
            self.console.success("  [OK] All required templates exist")
        else:
            missing = [t for t in required_templates if not (templates_dir / t).exists()]
            self.console.error(f"  [FAIL] Missing templates: {', '.join(missing)}")

        return all_exist

    def _check_memory(self) -> bool:
        """Check memory files"""
        # Check if we have .specpulse directory (new structure) or legacy structure
        specpulse_dir = self.project_root / ".specpulse"
        if specpulse_dir.exists():
            # New structure - memory is in .specpulse/memory
            memory_dir = self.project_root / ".specpulse" / "memory"
        else:
            # Legacy structure - memory is in root memory directory
            memory_dir = self.project_root / "memory"

        context_file = memory_dir / "context.md"

        if context_file.exists():
            self.console.success("  [OK] Memory context file exists")
            return True
        else:
            self.console.warning("  [WARNING] Memory context file not found (will be created on first use)")
            return True  # Not critical

    def _check_git(self) -> bool:
        """Check git repository"""
        git_dir = self.project_root / ".git"

        if git_dir.exists():
            self.console.success("  [OK] Git repository initialized")
            return True
        else:
            self.console.warning("  [WARNING] Not a git repository (recommended but not required)")
            return True  # Not critical

    def _check_ai_commands(self) -> bool:
        """Check AI command files"""
        ai_dirs = [self.project_root / ".claude", self.project_root / ".gemini"]

        has_ai = any(d.exists() for d in ai_dirs)
        if has_ai:
            self.console.success("  [OK] AI command integration found")
        else:
            self.console.info("  [INFO] No AI command integration (optional)")

        return True  # Not critical
