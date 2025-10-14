"""
Memory Provider Service

Extracted from SpecPulse God Object - handles memory/context template loading.

This service is responsible for:
- Constitution template (SDD principles)
- Context template (project state)
- Decisions template (architectural decisions)

Implements IMemoryProvider interface for dependency injection.
"""

from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class MemoryProvider:
    """
    Memory provider service implementing IMemoryProvider.

    Handles loading of memory-related templates.
    """

    def __init__(self, resources_dir: Path):
        """
        Initialize memory provider.

        Args:
            resources_dir: Path to resources directory
        """
        self.resources_dir = resources_dir
        self.memory_dir = resources_dir / "memory"

    def get_constitution_template(self) -> str:
        """Get constitution template (SDD principles)"""
        template_path = self.memory_dir / "constitution.md"

        if template_path.exists():
            try:
                return template_path.read_text(encoding='utf-8')
            except Exception as e:
                logger.error(f"Failed to read constitution template: {e}")

        logger.warning("Constitution template not found, returning empty")
        return ""

    def get_context_template(self) -> str:
        """Get context template (project state)"""
        template_path = self.memory_dir / "context.md"

        if not template_path.exists():
            logger.warning("Context template not found, using embedded fallback")
            return self._get_embedded_context_template()

        try:
            return template_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to read context template: {e}")
            return self._get_embedded_context_template()

    def get_decisions_template(self) -> str:
        """Get architectural decisions template"""
        template_path = self.memory_dir / "decisions.md"

        if not template_path.exists():
            logger.warning("Decisions template not found, using embedded fallback")
            return self._get_embedded_decisions_template()

        try:
            return template_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to read decisions template: {e}")
            return self._get_embedded_decisions_template()

    # Embedded templates

    def _get_embedded_context_template(self) -> str:
        """Embedded context template"""
        return """# Project Context

## Current State
Last Updated: [AI updates this automatically]

### Active Features
1. **[feature-name]** (SPEC-XXX)
   - Status: [Phase]
   - Branch: [branch-name]
   - Blockers: [None|List]

### Recent Decisions
- [Decision with rationale]

### Known Issues
- [Issue description]

## Team Preferences

### Technology Choices
- **Preferred Stack**: [Stack]
- **Testing**: [Framework]
- **CI/CD**: [Platform]

### Coding Patterns
- [Pattern preference]

## Project Glossary

### Domain Terms
- **[Term]**: [Definition]
"""

    def _get_embedded_decisions_template(self) -> str:
        """Embedded decisions template"""
        return """# Architectural Decisions

## Decision Log

### ADR-001: [Title]
**Date**: [DATE]
**Status**: [PROPOSED|ACCEPTED|DEPRECATED]
**Context**: [Why this decision was needed]
**Decision**: [What was decided]
**Consequences**: [What happens as a result]
**Alternatives Considered**: [Other options]

---

### ADR-002: [Title]
[Same structure]
"""


__all__ = ['MemoryProvider']
