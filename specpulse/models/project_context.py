"""
Project Context Model (v1.7.0)

Manages project-wide context variables like tech stack, preferences, and team size.
"""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml


@dataclass
class TechStack:
    """Technical stack configuration."""
    frontend: Optional[str] = None
    backend: Optional[str] = None
    database: Optional[str] = None
    message_queue: Optional[str] = None
    cache: Optional[str] = None
    other: Dict[str, str] = field(default_factory=dict)


@dataclass
class ProjectInfo:
    """Project information."""
    name: str = "Unknown Project"
    type: str = "software"
    description: Optional[str] = None
    version: Optional[str] = None


@dataclass
class ProjectContext:
    """Project context with tech stack, preferences, and metadata.

    Attributes:
        project: Project information
        tech_stack: Technology stack details
        team_size: Team size (default: 1 for solo developer)
        preferences: Development preferences
    """
    project: ProjectInfo = field(default_factory=ProjectInfo)
    tech_stack: TechStack = field(default_factory=TechStack)
    team_size: int = 1
    preferences: List[str] = field(default_factory=list)

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "ProjectContext":
        """Load project context from YAML file.

        Args:
            path: Path to project_context.yaml (defaults to .specpulse/project_context.yaml)

        Returns:
            ProjectContext instance
        """
        if path is None:
            path = Path(".specpulse/project_context.yaml")

        path = Path(path)

        if not path.exists():
            # Return default context
            return cls()

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not data:
                return cls()

            # Parse project info
            project_data = data.get("project", {})
            project = ProjectInfo(
                name=project_data.get("name", "Unknown Project"),
                type=project_data.get("type", "software"),
                description=project_data.get("description"),
                version=project_data.get("version")
            )

            # Parse tech stack
            tech_data = data.get("tech_stack", {})
            tech_stack = TechStack(
                frontend=tech_data.get("frontend"),
                backend=tech_data.get("backend"),
                database=tech_data.get("database"),
                message_queue=tech_data.get("message_queue"),
                cache=tech_data.get("cache"),
                other=tech_data.get("other", {})
            )

            # Parse other fields
            team_size = data.get("team_size", 1)
            preferences = data.get("preferences", [])

            return cls(
                project=project,
                tech_stack=tech_stack,
                team_size=team_size,
                preferences=preferences
            )

        except (yaml.YAMLError, IOError) as e:
            # Return default context on error
            print(f"Warning: Could not load project context: {e}")
            return cls()

    def save(self, path: Optional[Path] = None) -> None:
        """Save project context to YAML file.

        Args:
            path: Path to save to (defaults to .specpulse/project_context.yaml)
        """
        if path is None:
            path = Path(".specpulse/project_context.yaml")

        path = Path(path)

        # Create directory if needed
        path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict
        data = {
            "project": {
                "name": self.project.name,
                "type": self.project.type,
                "description": self.project.description,
                "version": self.project.version
            },
            "tech_stack": {
                "frontend": self.tech_stack.frontend,
                "backend": self.tech_stack.backend,
                "database": self.tech_stack.database,
                "message_queue": self.tech_stack.message_queue,
                "cache": self.tech_stack.cache,
                "other": self.tech_stack.other
            },
            "team_size": self.team_size,
            "preferences": self.preferences
        }

        # Remove None values
        data = self._remove_none_values(data)

        # Write to file
        try:
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        except IOError as e:
            raise IOError(f"Failed to save project context: {e}")

    def set_value(self, key: str, value: Any) -> None:
        """Set a value using dot notation (e.g., "tech_stack.frontend").

        Args:
            key: Key in dot notation
            value: Value to set
        """
        parts = key.split('.')

        if len(parts) == 1:
            # Top-level key
            if parts[0] == "team_size":
                self.team_size = int(value)
            elif parts[0] == "preferences":
                if isinstance(value, list):
                    self.preferences = value
                else:
                    self.preferences.append(value)
            else:
                raise ValueError(f"Unknown top-level key: {parts[0]}")

        elif len(parts) == 2:
            # Nested key
            if parts[0] == "project":
                if parts[1] == "name":
                    self.project.name = value
                elif parts[1] == "type":
                    self.project.type = value
                elif parts[1] == "description":
                    self.project.description = value
                elif parts[1] == "version":
                    self.project.version = value
                else:
                    raise ValueError(f"Unknown project key: {parts[1]}")

            elif parts[0] == "tech_stack":
                if parts[1] == "frontend":
                    self.tech_stack.frontend = value
                elif parts[1] == "backend":
                    self.tech_stack.backend = value
                elif parts[1] == "database":
                    self.tech_stack.database = value
                elif parts[1] == "message_queue":
                    self.tech_stack.message_queue = value
                elif parts[1] == "cache":
                    self.tech_stack.cache = value
                else:
                    # Store in 'other' dict
                    self.tech_stack.other[parts[1]] = value
            else:
                raise ValueError(f"Unknown section: {parts[0]}")

        else:
            raise ValueError(f"Invalid key format: {key}. Use dot notation like 'tech_stack.frontend'")

    def get_value(self, key: str) -> Any:
        """Get a value using dot notation.

        Args:
            key: Key in dot notation

        Returns:
            Value or None if not found
        """
        parts = key.split('.')

        if len(parts) == 1:
            # Top-level key
            if parts[0] == "team_size":
                return self.team_size
            elif parts[0] == "preferences":
                return self.preferences
            elif parts[0] == "project":
                return asdict(self.project)
            elif parts[0] == "tech_stack":
                return asdict(self.tech_stack)
            else:
                return None

        elif len(parts) == 2:
            # Nested key
            if parts[0] == "project":
                return getattr(self.project, parts[1], None)
            elif parts[0] == "tech_stack":
                value = getattr(self.tech_stack, parts[1], None)
                if value is None and parts[1] in self.tech_stack.other:
                    return self.tech_stack.other[parts[1]]
                return value
            else:
                return None

        else:
            return None

    def _remove_none_values(self, data: Dict) -> Dict:
        """Remove None values from nested dict.

        Args:
            data: Dictionary to clean

        Returns:
            Cleaned dictionary
        """
        if not isinstance(data, dict):
            return data

        return {
            k: self._remove_none_values(v) if isinstance(v, dict) else v
            for k, v in data.items()
            if v is not None and v != {} and v != []
        }

    def validate(self) -> List[str]:
        """Validate project context.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Validate project name
        if not self.project.name or self.project.name == "Unknown Project":
            errors.append("Project name is not set")

        # Validate team size
        if self.team_size < 1:
            errors.append("Team size must be at least 1")

        # Validate tech stack (at least one component should be set)
        if not any([
            self.tech_stack.frontend,
            self.tech_stack.backend,
            self.tech_stack.database,
            self.tech_stack.other
        ]):
            errors.append("Tech stack is empty (recommended to set at least one component)")

        return errors
