"""
Memory ID Manager

This module integrates the universal ID system with memory management
to ensure consistent ID generation for decisions, patterns, and constraints.
"""

from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime
from .universal_id_generator import get_universal_id_generator, IDType

class MemoryIDManager:
    """
    Memory ID Manager for generating consistent IDs in memory files.

    Handles:
    - Decision IDs (DEC-001, DEC-002...)
    - Pattern IDs (PATTERN-001, PATTERN-002...)
    - Constraint IDs (CONST-001, CONST-002...)
    - Checkpoint IDs (CHK-001, CHK-002...)
    """

    def __init__(self, project_root: Path):
        """
        Initialize memory ID manager.

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root.resolve()
        self.id_generator = get_universal_id_generator(project_root)
        self.memory_dir = self.project_root / ".specpulse" / "memory"

    def generate_decision_id(self) -> str:
        """
        Generate next decision ID.

        Returns:
            Decision ID (e.g., "DEC-001")
        """
        return self.id_generator.get_next_id(IDType.DECISION)

    def generate_pattern_id(self) -> str:
        """
        Generate next pattern ID.

        Returns:
            Pattern ID (e.g., "PATTERN-001")
        """
        return self.id_generator.get_next_id(IDType.PATTERN)

    def generate_constraint_id(self) -> str:
        """
        Generate next constraint ID.

        Returns:
            Constraint ID (e.g., "CONST-001")
        """
        return self.id_generator.get_next_id(IDType.CONSTRAINT)

    def generate_checkpoint_id(self) -> str:
        """
        Generate next checkpoint ID.

        Returns:
            Checkpoint ID (e.g., "CHK-001")
        """
        return self.id_generator.get_next_id(IDType.CHECKPOINT)

    def format_decision_entry(self, title: str, description: str,
                            related_features: Optional[List[str]] = None) -> str:
        """
        Format decision entry with generated ID.

        Args:
            title: Decision title
            description: Decision description
            related_features: List of related feature IDs

        Returns:
            Formatted decision entry
        """
        decision_id = self.generate_decision_id()
        current_date = datetime.now().strftime("%Y-%m-%d")

        entry = f"""### {decision_id}: {title}
**Date**: {current_date}
**Description**: {description}
**Related**: {', '.join(related_features) if related_features else 'None'}

---

"""

        return entry

    def format_pattern_entry(self, title: str, description: str,
                           usage_examples: Optional[List[str]] = None) -> str:
        """
        Format pattern entry with generated ID.

        Args:
            title: Pattern title
            description: Pattern description
            usage_examples: List of usage examples

        Returns:
            Formatted pattern entry
        """
        pattern_id = self.generate_pattern_id()
        current_date = datetime.now().strftime("%Y-%m-%d")

        entry = f"""### {pattern_id}: {title}
**Created**: {current_date}
**Description**: {description}
**Examples**:
{chr(10).join(f"- {example}" for example in usage_examples) if usage_examples else "- None"}

---

"""

        return entry

    def format_constraint_entry(self, title: str, description: str,
                              violation_impact: str) -> str:
        """
        Format constraint entry with generated ID.

        Args:
            title: Constraint title
            description: Constraint description
            violation_impact: Impact of violating this constraint

        Returns:
            Formatted constraint entry
        """
        constraint_id = self.generate_constraint_id()
        current_date = datetime.now().strftime("%Y-%m-%d")

        entry = f"""### {constraint_id}: {title}
**Created**: {current_date}
**Description**: {description}
**Violation Impact**: {violation_impact}

---

"""

        return entry

    def add_decision_to_memory(self, title: str, description: str,
                             related_features: Optional[List[str]] = None) -> str:
        """
        Add decision to memory file with auto-generated ID.

        Args:
            title: Decision title
            description: Decision description
            related_features: List of related feature IDs

        Returns:
            Generated decision ID
        """
        decisions_file = self.memory_dir / "decisions.md"
        entry = self.format_decision_entry(title, description, related_features)

        # Read existing content
        if decisions_file.exists():
            content = decisions_file.read_text(encoding='utf-8')
        else:
            content = """# Project Decisions

This file contains all architectural and technical decisions made during development.

---

"""

        # Add new entry
        content += entry
        decisions_file.write_text(content, encoding='utf-8')

        # Return the generated ID
        lines = entry.strip().split('\n')
        return lines[0].split(': ')[0]  # Extract ID from first line

    def add_pattern_to_memory(self, title: str, description: str,
                            usage_examples: Optional[List[str]] = None) -> str:
        """
        Add pattern to memory file with auto-generated ID.

        Args:
            title: Pattern title
            description: Pattern description
            usage_examples: List of usage examples

        Returns:
            Generated pattern ID
        """
        patterns_file = self.memory_dir / "patterns.md"
        entry = self.format_pattern_entry(title, description, usage_examples)

        # Read existing content
        if patterns_file.exists():
            content = patterns_file.read_text(encoding='utf-8')
        else:
            content = """# Development Patterns

This file contains reusable development patterns and best practices.

---

"""

        # Add new entry
        content += entry
        patterns_file.write_text(content, encoding='utf-8')

        # Return the generated ID
        lines = entry.strip().split('\n')
        return lines[0].split(': ')[0]  # Extract ID from first line

    def add_constraint_to_memory(self, title: str, description: str,
                                violation_impact: str) -> str:
        """
        Add constraint to memory file with auto-generated ID.

        Args:
            title: Constraint title
            description: Constraint description
            violation_impact: Impact of violating this constraint

        Returns:
            Generated constraint ID
        """
        constraints_file = self.memory_dir / "constraints.md"
        entry = self.format_constraint_entry(title, description, violation_impact)

        # Read existing content
        if constraints_file.exists():
            content = constraints_file.read_text(encoding='utf-8')
        else:
            content = """# Project Constraints

This file contains all project constraints and their implications.

---

"""

        # Add new entry
        content += entry
        constraints_file.write_text(content, encoding='utf-8')

        # Return the generated ID
        lines = entry.strip().split('\n')
        return lines[0].split(': ')[0]  # Extract ID from first line

    def get_id_statistics(self) -> Dict:
        """
        Get current ID statistics for memory entities.

        Returns:
            Dictionary with current counts
        """
        stats = self.id_generator.get_statistics()

        return {
            "current_decision_id": self.id_generator.get_current_id(IDType.DECISION),
            "current_pattern_id": self.id_generator.get_current_id(IDType.PATTERN),
            "current_constraint_id": self.id_generator.get_current_id(IDType.CONSTRAINT),
            "current_checkpoint_id": self.id_generator.get_current_id(IDType.CHECKPOINT),
            "total_ids_used": stats["total_ids_used"],
            "last_updated": stats["last_updated"]
        }


# Convenience functions
def add_project_decision(project_root: Path, title: str, description: str,
                        related_features: Optional[List[str]] = None) -> str:
    """Add decision to project memory with auto-generated ID."""
    manager = MemoryIDManager(project_root)
    return manager.add_decision_to_memory(title, description, related_features)

def add_project_pattern(project_root: Path, title: str, description: str,
                      usage_examples: Optional[List[str]] = None) -> str:
    """Add pattern to project memory with auto-generated ID."""
    manager = MemoryIDManager(project_root)
    return manager.add_pattern_to_memory(title, description, usage_examples)

def add_project_constraint(project_root: Path, title: str, description: str,
                         violation_impact: str) -> str:
    """Add constraint to project memory with auto-generated ID."""
    manager = MemoryIDManager(project_root)
    return manager.add_constraint_to_memory(title, description, violation_impact)