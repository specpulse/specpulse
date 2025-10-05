"""
Context Injector Module (v1.7.0)

Handles automatic context injection into AI scripts and templates.
Injects project context, decisions, and patterns as HTML comments.
"""

from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from .memory_manager import MemoryManager, MemoryEntry


class ContextInjector:
    """Handles context injection for AI scripts and templates.

    Generates compact HTML comment blocks with project context,
    recent decisions, and patterns for LLM consumption.
    """

    MAX_CONTEXT_SIZE = 500  # Maximum characters for injected context

    def __init__(self, project_root: Optional[Path] = None, memory_manager: Optional[MemoryManager] = None):
        """Initialize ContextInjector.

        Args:
            project_root: Project root directory
            memory_manager: MemoryManager instance (optional)
        """
        self.project_root = project_root or Path.cwd()
        self.memory_manager = memory_manager or MemoryManager(self.project_root)

    def build_context(self, feature_id: Optional[str] = None) -> str:
        """Build HTML comment context block for injection.

        Args:
            feature_id: Optional feature ID for feature-specific context

        Returns:
            HTML comment string with context (<500 chars)
        """
        # Load project context
        project_context = self._load_project_context()

        # Get recent decisions (last 3)
        decisions = self.memory_manager.query_by_tag("decision", recent=3)

        # Get active patterns
        patterns = self.memory_manager.query_by_tag("pattern", recent=3)

        # Build context string
        context_parts = []

        # Project info
        project_name = project_context.get("project", {}).get("name", "Unknown")
        project_type = project_context.get("project", {}).get("type", "project")
        context_parts.append(f"Project: {project_name} ({project_type})")

        # Tech stack
        tech_stack = self._format_tech_stack(project_context)
        if tech_stack:
            context_parts.append(f"Tech Stack: {tech_stack}")

        # Recent decisions
        if decisions:
            decision_str = self._format_decisions(decisions)
            context_parts.append(f"Recent Decisions:\n{decision_str}")

        # Patterns
        if patterns:
            pattern_str = self._format_patterns(patterns)
            context_parts.append(f"Patterns:\n{pattern_str}")

        # Combine and wrap in HTML comment
        context_body = "\n".join(context_parts)

        # Truncate if too long
        if len(context_body) > self.MAX_CONTEXT_SIZE - 50:  # Reserve space for HTML tags
            context_body = context_body[:self.MAX_CONTEXT_SIZE - 53] + "..."

        context_html = f"""<!-- SPECPULSE CONTEXT -->
{context_body}
<!-- END SPECPULSE CONTEXT -->"""

        return context_html

    def inject(self, template: str, feature_id: Optional[str] = None) -> str:
        """Inject context into a template string.

        Args:
            template: Template string to inject context into
            feature_id: Optional feature ID for feature-specific context

        Returns:
            Template with context injected at the beginning
        """
        context = self.build_context(feature_id)
        return f"{context}\n\n{template}"

    def _load_project_context(self) -> Dict[str, Any]:
        """Load project context from YAML file.

        Returns:
            Project context dictionary
        """
        context_file = self.project_root / ".specpulse" / "project_context.yaml"

        if not context_file.exists():
            return {
                "project": {
                    "name": "SpecPulse Project",
                    "type": "software"
                },
                "tech_stack": {}
            }

        try:
            import yaml
            with open(context_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {"project": {}, "tech_stack": {}}

    def _format_tech_stack(self, project_context: Dict[str, Any]) -> str:
        """Format tech stack for compact display.

        Args:
            project_context: Project context dictionary

        Returns:
            Formatted tech stack string
        """
        tech_stack = project_context.get("tech_stack", {})

        if not tech_stack:
            return ""

        parts = []
        if "frontend" in tech_stack:
            parts.append(tech_stack["frontend"])
        if "backend" in tech_stack:
            parts.append(tech_stack["backend"])
        if "database" in tech_stack:
            parts.append(tech_stack["database"])

        return " | ".join(parts) if parts else ""

    def _format_decisions(self, decisions: list[MemoryEntry]) -> str:
        """Format decisions for compact display.

        Args:
            decisions: List of decision MemoryEntry objects

        Returns:
            Formatted decisions string
        """
        lines = []
        for decision in decisions:
            # Format: "  - DEC-001: Title (date)"
            lines.append(f"  - {decision.id}: {decision.title} ({decision.date})")

        return "\n".join(lines)

    def _format_patterns(self, patterns: list[MemoryEntry]) -> str:
        """Format patterns for compact display.

        Args:
            patterns: List of pattern MemoryEntry objects

        Returns:
            Formatted patterns string
        """
        lines = []
        for pattern in patterns:
            # Truncate title if too long
            title = pattern.title
            if len(title) > 40:
                title = title[:37] + "..."

            lines.append(f"  - {pattern.id}: {title}")

        return "\n".join(lines)
