"""
Path Manager for SpecPulse v2.6.7

Centralized path management for all SpecPulse directories.
This class provides a single source of truth for all path resolutions,
ENFORCING the consolidated .specpulse/ directory structure.

Mandatory Structure (v2.2.0+):
- .specpulse/specs/
- .specpulse/plans/
- .specpulse/tasks/
- .specpulse/memory/
- .specpulse/templates/
- .specpulse/cache/
- .specpulse/checkpoints/
- .specpulse/docs/
- .claude/ (root - AI commands only)
- .gemini/ (root - AI commands only)
- .windsurf/ (root - AI commands only)
- .cursor/ (root - AI commands only)
- .github/ (root - AI commands only)
- .opencode/ (root - AI commands only)
- .crush/ (root - AI commands only)
- .qwen/ (root - AI commands only)

CRITICAL: All SpecPulse operations MUST stay within .specpulse directory.
No SpecPulse-generated files should be created in the root project directory.
Custom commands MUST stay in their respective AI directories.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import warnings


class PathManager:
    """
    Centralized path management for SpecPulse projects.

    This class ENFORCES the .specpulse/ consolidated structure.
    Legacy structure is NOT supported - all operations MUST use .specpulse/ directory.
    """

    def __init__(self, project_root: Path):
        """
        Initialize path manager with enforced .specpulse/ structure.

        Args:
            project_root: Root directory of the project

        Raises:
            ValueError: If project_root is invalid
        """
        self.project_root = Path(project_root)
        if not self.project_root.exists():
            raise ValueError(f"Project root does not exist: {self.project_root}")

        # ENFORCED: Always use .specpulse/ structure
        self.use_legacy_structure = False

        # Core .specpulse directory (MANDATORY)
        self.specpulse_dir = self.project_root / ".specpulse"

        # ENFORCE: Create .specpulse directory immediately
        self.specpulse_dir.mkdir(exist_ok=True)

        # AI integration directories (always at root for custom commands)
        self.claude_dir = self.project_root / ".claude"
        self.gemini_dir = self.project_root / ".gemini"
        self.windsurf_dir = self.project_root / ".windsurf"
        self.cursor_dir = self.project_root / ".cursor"
        self.github_dir = self.project_root / ".github"
        self.opencode_dir = self.project_root / ".opencode"
        self.crush_dir = self.project_root / ".crush"
        self.qwen_dir = self.project_root / ".qwen"

        # System directories (within .specpulse)
        self.cache_dir = self.specpulse_dir / "cache"
        self.checkpoints_dir = self.specpulse_dir / "checkpoints"

        # ENFORCED: Initialize ONLY new structure paths
        self._init_enforced_paths()

    def _init_enforced_paths(self):
        """Initialize ENFORCED .specpulse/ structure paths."""
        self.specs_dir = self.specpulse_dir / "specs"
        self.plans_dir = self.specpulse_dir / "plans"
        self.tasks_dir = self.specpulse_dir / "tasks"
        self.memory_dir = self.specpulse_dir / "memory"
        self.templates_dir = self.specpulse_dir / "templates"
        self.notes_dir = self.memory_dir / "notes"
        self.docs_dir = self.specpulse_dir / "docs"
        self.template_backups_dir = self.specpulse_dir / "template_backups"

    def get_all_directories(self) -> Dict[str, Path]:
        """
        Get all managed directories as a dictionary.

        Returns:
            Dictionary mapping directory names to Path objects
        """
        return {
            # Core SpecPulse directories (within .specpulse)
            'specs': self.specs_dir,
            'plans': self.plans_dir,
            'tasks': self.tasks_dir,
            'memory': self.memory_dir,
            'templates': self.templates_dir,
            'notes': self.notes_dir,
            'cache': self.cache_dir,
            'checkpoints': self.checkpoints_dir,
            'docs': self.docs_dir,
            'template_backups': self.template_backups_dir,

            # AI command directories (at root for custom commands)
            'claude': self.claude_dir,
            'gemini': self.gemini_dir,
            'windsurf': self.windsurf_dir,
            'cursor': self.cursor_dir,
            'github': self.github_dir,
            'opencode': self.opencode_dir,
            'crush': self.crush_dir,
            'qwen': self.qwen_dir,

            # Main directories
            'specpulse': self.specpulse_dir,
        }

    def ensure_directories(self, directories: Optional[list] = None) -> bool:
        """
        Ensure specified directories exist, creating them if needed.

        Args:
            directories: List of directory names to create. If None, creates all.

        Returns:
            True if all directories were created successfully, False otherwise
        """
        if directories is None:
            directories = ['specs', 'plans', 'tasks', 'memory', 'templates',
                          'cache', 'checkpoints', 'notes']

        failed_dirs = []
        for dir_name in directories:
            dir_path = getattr(self, f"{dir_name}_dir", None)
            if dir_path is None:
                failed_dirs.append(dir_name)
                continue

            try:
                dir_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                failed_dirs.append(dir_name)

        if failed_dirs:
            warnings.warn(f"Failed to create directories: {', '.join(failed_dirs)}")
            return False
        return True

    def get_feature_dir(self, feature_id: str, feature_name: str, dir_type: str) -> Path:
        """
        Get feature-specific directory path.

        Args:
            feature_id: Feature ID (e.g., "001")
            feature_name: Feature name (e.g., "user-auth")
            dir_type: Type of directory ('specs', 'plans', 'tasks')

        Returns:
            Path to feature directory
        """
        if dir_type not in ['specs', 'plans', 'tasks']:
            raise ValueError(f"Invalid directory type: {dir_type}")

        base_dir = getattr(self, f"{dir_type}_dir")
        return base_dir / f"{feature_id}-{feature_name}"

    def get_spec_file(self, feature_id: str, feature_name: str, spec_number: int) -> Path:
        """
        Get specification file path.

        Args:
            feature_id: Feature ID
            feature_name: Feature name
            spec_number: Specification number

        Returns:
            Path to specification file
        """
        feature_dir = self.get_feature_dir(feature_id, feature_name, 'specs')
        return feature_dir / f"spec-{spec_number:03d}.md"

    def get_plan_file(self, feature_id: str, feature_name: str, plan_number: int) -> Path:
        """
        Get plan file path.

        Args:
            feature_id: Feature ID
            feature_name: Feature name
            plan_number: Plan number

        Returns:
            Path to plan file
        """
        feature_dir = self.get_feature_dir(feature_id, feature_name, 'plans')
        return feature_dir / f"plan-{plan_number}.md"

    def get_task_file(self, feature_id: str, feature_name: str, task_number: int) -> Path:
        """
        Get task file path.

        Args:
            feature_id: Feature ID
            feature_name: Feature name
            task_number: Task number

        Returns:
            Path to task file
        """
        feature_dir = self.get_feature_dir(feature_id, feature_name, 'tasks')
        return feature_dir / f"task-{task_number}.md"

    def get_memory_file(self, filename: str) -> Path:
        """
        Get memory file path.

        Args:
            filename: Memory filename (e.g., "context.md")

        Returns:
            Path to memory file
        """
        return self.memory_dir / filename

    def get_template_file(self, filename: str) -> Path:
        """
        Get template file path.

        Args:
            filename: Template filename (e.g., "spec.md")

        Returns:
            Path to template file
        """
        return self.templates_dir / filename

    def get_decomposition_dir(self, feature_id: str, feature_name: str) -> Path:
        """
        Get decomposition directory path.

        Args:
            feature_id: Feature ID
            feature_name: Feature name

        Returns:
            Path to decomposition directory
        """
        feature_dir = self.get_feature_dir(feature_id, feature_name, 'specs')
        return feature_dir / "decomposition"

    def detect_structure(self) -> str:
        """
        ENFORCED: Always returns 'new' since only .specpulse/ structure is supported.
        Legacy structure is NOT supported.

        Returns:
            Always returns 'new'
        """
        # ENFORCED: Always new structure
        return "new"

    def migrate_to_new_structure(self, backup: bool = True) -> bool:
        """
        NOT APPLICABLE: Migration not needed since only .specpulse/ structure is supported.
        This method is kept for API compatibility but always returns True.

        Args:
            backup: Unused - kept for API compatibility

        Returns:
            Always returns True - no migration needed
        """
        # ENFORCED: No migration needed - we only support .specpulse/ structure
        return True

    def validate_specpulse_path(self, file_path: Path) -> bool:
        """
        Validate that a path is within .specpulse directory for security.

        Args:
            file_path: Path to validate

        Returns:
            True if path is valid (within .specpulse), False otherwise
        """
        try:
            # Convert to absolute paths
            abs_file_path = file_path.resolve()
            abs_specpulse_dir = self.specpulse_dir.resolve()

            # Check if the file path is within .specpulse directory
            return abs_file_path.is_relative_to(abs_specpulse_dir)
        except (OSError, ValueError):
            return False

    def enforce_specpulse_rules(self) -> Dict[str, Any]:
        """
        ENFORCED: Validate that all operations respect .specpulse directory structure.
        Legacy structure is NOT supported.

        Returns:
            Dictionary with validation results and warnings
        """
        results = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'structure_type': 'enforced',
            'enforced_directories': []
        }

        # ENFORCED: Always use .specpulse/ structure
        if self.use_legacy_structure:
            results['valid'] = False
            results['errors'].append(
                "Legacy structure is NOT supported. Only .specpulse/ structure is enforced."
            )

        # Validate that all SpecPulse data directories are within .specpulse
        for dir_name, dir_path in self.get_all_directories().items():
            # AI command directories can be at root - they are for custom commands only
            if dir_name in ['claude', 'gemini', 'windsurf', 'cursor', 'github', 'opencode', 'crush', 'qwen']:
                continue

            # Validate that directory is within .specpulse
            if not self.validate_specpulse_path(dir_path):
                results['valid'] = False
                results['errors'].append(
                    f"Directory '{dir_name}' is outside .specpulse: {dir_path}"
                )
            else:
                results['enforced_directories'].append(dir_name)

        # ENFORCED: Ensure .specpulse directory exists
        if not self.specpulse_dir.exists():
            results['valid'] = False
            results['errors'].append(
                f".specpulse directory does not exist: {self.specpulse_dir}"
            )

        # Validate AI command directories isolation
        ai_violations = self.validate_ai_command_isolation()
        if ai_violations:
            results['valid'] = False
            results['errors'].extend(ai_violations)

        return results

    def validate_ai_command_isolation(self) -> list:
        """
        Validate that AI command directories only contain their respective commands.

        Returns:
            List of violations found
        """
        violations = []

        # Define expected subdirectories for each AI platform
        ai_platforms = {
            'claude': ['commands'],
            'gemini': ['commands'],
            'windsurf': ['workflows'],  # ENFORCED: Windsurf uses workflows, not commands
            'cursor': ['commands'],
            'github': ['prompts'],
            'opencode': ['command'],  # ENFORCED: OpenCode uses command (singular) only
            'crush': ['commands'],
            'qwen': ['commands']
        }

        for platform, expected_subdirs in ai_platforms.items():
            ai_dir = getattr(self, f"{platform}_dir")
            if ai_dir.exists():
                # Check that only expected subdirectories exist
                for item in ai_dir.iterdir():
                    if item.is_dir() and item.name not in expected_subdirs:
                        violations.append(
                            f"Unexpected subdirectory in .{platform}/: {item.name}"
                        )
                    elif item.is_file() and not item.name.startswith('.'):
                        # Only allow hidden files (like .gitkeep)
                        violations.append(
                            f"Unexpected file in .{platform}/ root: {item.name}"
                        )

        return violations

    def lock_custom_commands_to_directories(self, selected_tools: Optional[list] = None) -> bool:
        """
        ENFORCED: Ensure custom commands stay within their respective AI directories.

        Args:
            selected_tools: List of selected AI tools. If None, creates all directories.

        Returns:
            True if all custom commands are properly isolated
        """
        try:
            # Create AI command directories if they don't exist
            ai_platforms = ['claude', 'gemini', 'windsurf', 'cursor', 'github', 'opencode', 'crush', 'qwen']

            # If selected tools are specified, only process those
            if selected_tools:
                ai_platforms = [tool for tool in ai_platforms if tool in selected_tools]

            for platform in ai_platforms:
                ai_dir = getattr(self, f"{platform}_dir")
                if platform == 'github':
                    commands_dir = ai_dir / 'prompts'
                    # Create directory if it doesn't exist
                    commands_dir.mkdir(parents=True, exist_ok=True)
                    # Add .gitkeep to maintain directory structure
                    gitkeep_file = commands_dir / '.gitkeep'
                    if not gitkeep_file.exists():
                        gitkeep_file.write_text('# Maintains directory structure for SpecPulse\n')
                elif platform == 'windsurf':
                    # ENFORCED: Windsurf uses workflows only - don't create commands
                    commands_dir = ai_dir / 'workflows'
                    commands_dir.mkdir(parents=True, exist_ok=True)
                    # Add .gitkeep to maintain directory structure
                    gitkeep_file = commands_dir / '.gitkeep'
                    if not gitkeep_file.exists():
                        gitkeep_file.write_text('# Maintains directory structure for SpecPulse\n')
                elif platform == 'opencode':
                    # ENFORCED: OpenCode uses command (singular) directory for custom commands
                    commands_dir = ai_dir / 'command'
                    commands_dir.mkdir(parents=True, exist_ok=True)
                    # Add .gitkeep to maintain directory structure
                    gitkeep_file = commands_dir / '.gitkeep'
                    if not gitkeep_file.exists():
                        gitkeep_file.write_text('# Maintains directory structure for SpecPulse\n')
                else:
                    # For claude, gemini, cursor, crush, qwen
                    commands_dir = ai_dir / 'commands'
                    commands_dir.mkdir(parents=True, exist_ok=True)
                    # Add .gitkeep to maintain directory structure
                    gitkeep_file = commands_dir / '.gitkeep'
                    if not gitkeep_file.exists():
                        gitkeep_file.write_text('# Maintains directory structure for SpecPulse\n')

            # Validate isolation
            violations = self.validate_ai_command_isolation()
            return len(violations) == 0

        except Exception as e:
            import warnings
            warnings.warn(f"Failed to lock custom commands to directories: {e}")
            return False

    def get_safe_output_path(self, file_type: str, feature_id: str = None,
                           feature_name: str = None, filename: str = None) -> Path:
        """
        Get a safe output path that always stays within .specpulse directory.
        ENFORCED: Only .specpulse/ structure is supported.

        Args:
            file_type: Type of file ('spec', 'plan', 'task', 'memory', 'cache')
            feature_id: Feature ID (for spec/plan/task files)
            feature_name: Feature name (for spec/plan/task files)
            filename: Filename (optional, will be generated if not provided)

        Returns:
            Safe Path within .specpulse directory

        Raises:
            ValueError: If file_type is invalid
        """
        # ENFORCED: Always use .specpulse/ structure
        if file_type == 'spec' and feature_id and feature_name:
            if filename:
                return self.get_feature_dir(feature_id, feature_name, 'specs') / filename
            else:
                spec_num = 1  # Default, should be calculated
                return self.get_spec_file(feature_id, feature_name, spec_num)

        elif file_type == 'plan' and feature_id and feature_name:
            if filename:
                return self.get_feature_dir(feature_id, feature_name, 'plans') / filename
            else:
                plan_num = 1  # Default, should be calculated
                return self.get_plan_file(feature_id, feature_name, plan_num)

        elif file_type == 'task' and feature_id and feature_name:
            if filename:
                return self.get_feature_dir(feature_id, feature_name, 'tasks') / filename
            else:
                task_num = 1  # Default, should be calculated
                return self.get_task_file(feature_id, feature_name, task_num)

        elif file_type == 'memory':
            return self.memory_dir / (filename or "context.md")

        elif file_type == 'cache':
            return self.cache_dir / (filename or "default.cache")

        elif file_type == 'docs':
            return self.docs_dir / (filename or "readme.md")

        elif file_type == 'template_backup':
            return self.template_backups_dir / (filename or "backup.md")

        else:
            # Default to .specpulse root for unknown types
            return self.specpulse_dir / (filename or "output.md")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert path manager configuration to dictionary.

        Returns:
            Dictionary representation of path configuration
        """
        return {
            'project_root': str(self.project_root),
            'use_legacy_structure': self.use_legacy_structure,
            'structure_detected': self.detect_structure(),
            'directories': {name: str(path) for name, path in self.get_all_directories().items()}
        }