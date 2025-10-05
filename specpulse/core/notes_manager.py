"""
Notes Manager Module (v1.7.0)

Handles lightweight note-taking during development with merge-to-spec capability.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import re


@dataclass
class Note:
    """Represents a development note.

    Attributes:
        id: Note ID (timestamp-based)
        content: Note content
        feature: Feature ID this note belongs to
        timestamp: Creation timestamp
        merged: Whether note has been merged to spec
    """
    id: str
    content: str
    feature: str
    timestamp: datetime
    merged: bool = False


class NotesManager:
    """Manages development notes with merge-to-spec functionality."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize NotesManager.

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root or Path.cwd()
        self.notes_dir = self.project_root / "memory" / "notes"
        self.notes_dir.mkdir(parents=True, exist_ok=True)

    def add_note(self, content: str, feature_id: Optional[str] = None) -> str:
        """Add a note to the notes system.

        Args:
            content: Note content
            feature_id: Feature ID (auto-detected if None)

        Returns:
            Note ID
        """
        # Auto-detect feature if not provided
        if feature_id is None:
            feature_id = self._detect_current_feature()

        if not feature_id:
            raise ValueError("Could not detect current feature. Please provide feature_id.")

        # Generate note ID from timestamp
        now = datetime.now()
        note_id = now.strftime("%Y%m%d%H%M%S")

        # Create note entry
        note_entry = f"""### Note {note_id}
Timestamp: {now.strftime("%Y-%m-%d %H:%M:%S")}
Status: Active

{content}

---

"""

        # Append to feature notes file
        notes_file = self.notes_dir / f"{feature_id}.md"

        if not notes_file.exists():
            notes_file.write_text(f"# Notes for Feature {feature_id}\n\n", encoding='utf-8')

        # Append note
        existing_content = notes_file.read_text(encoding='utf-8')
        notes_file.write_text(existing_content + note_entry, encoding='utf-8')

        return note_id

    def list_notes(self, feature_id: Optional[str] = None) -> List[Note]:
        """List notes for a feature.

        Args:
            feature_id: Feature ID (auto-detected if None)

        Returns:
            List of Note objects
        """
        # Auto-detect feature if not provided
        if feature_id is None:
            feature_id = self._detect_current_feature()

        if not feature_id:
            return []

        notes_file = self.notes_dir / f"{feature_id}.md"

        if not notes_file.exists():
            return []

        # Parse notes from file
        content = notes_file.read_text(encoding='utf-8')
        notes = []

        # Pattern to match note entries
        note_pattern = re.compile(
            r'### Note (\d+)\s*\nTimestamp: (.+?)\s*\nStatus: (.+?)\s*\n\n(.+?)(?=\n---|\Z)',
            re.DOTALL
        )

        for match in note_pattern.finditer(content):
            note_id = match.group(1)
            timestamp_str = match.group(2)
            status = match.group(3)
            note_content = match.group(4).strip()

            # Parse timestamp
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                timestamp = datetime.now()

            # Check if merged
            merged = status.lower() == "merged"

            note = Note(
                id=note_id,
                content=note_content,
                feature=feature_id,
                timestamp=timestamp,
                merged=merged
            )
            notes.append(note)

        # Sort by timestamp (newest first)
        notes.sort(key=lambda n: n.timestamp, reverse=True)

        return notes

    def merge_to_spec(self, feature_id: str, note_id: str, section: Optional[str] = None) -> str:
        """Merge note content into specification file.

        Args:
            feature_id: Feature ID
            note_id: Note ID to merge
            section: Target section in spec (auto-detected if None)

        Returns:
            Path to updated spec file
        """
        # Find the note
        notes = self.list_notes(feature_id)
        note = next((n for n in notes if n.id == note_id), None)

        if not note:
            raise ValueError(f"Note {note_id} not found in feature {feature_id}")

        if note.merged:
            raise ValueError(f"Note {note_id} has already been merged")

        # Find latest spec file
        spec_dir = self.project_root / "specs" / f"{feature_id}-*"
        spec_dirs = list(self.project_root.glob(f"specs/*{feature_id}*"))

        if not spec_dirs:
            raise ValueError(f"No spec directory found for feature {feature_id}")

        spec_dir = spec_dirs[0]

        # Find latest spec file
        spec_files = sorted(spec_dir.glob("spec-*.md"), reverse=True)

        if not spec_files:
            raise ValueError(f"No spec files found in {spec_dir}")

        spec_file = spec_files[0]

        # Determine target section
        if section is None:
            section = self._detect_section(note.content)

        # Read spec content
        spec_content = spec_file.read_text(encoding='utf-8')

        # Find section to insert into
        section_pattern = rf'(## {re.escape(section)})'

        if not re.search(section_pattern, spec_content):
            # Section doesn't exist, add it at the end
            merge_content = f"""

## {section}

<!-- Merged from note {note_id} -->
{note.content}
"""
            spec_content += merge_content
        else:
            # Insert after section header
            parts = re.split(rf'(## {re.escape(section)})', spec_content)

            if len(parts) >= 3:
                # Find next section
                next_section_match = re.search(r'\n## ', parts[2])

                merge_content = f"""

<!-- Merged from note {note_id} -->
{note.content}
"""

                if next_section_match:
                    section_content = parts[2][:next_section_match.start()]
                    rest = parts[2][next_section_match.start():]
                    spec_content = parts[0] + parts[1] + section_content + merge_content + rest
                else:
                    spec_content = parts[0] + parts[1] + parts[2] + merge_content

        # Write updated spec
        spec_file.write_text(spec_content, encoding='utf-8')

        # Mark note as merged
        self._mark_note_merged(feature_id, note_id)

        return str(spec_file)

    def _detect_current_feature(self) -> Optional[str]:
        """Detect current feature from context.md.

        Returns:
            Feature ID or None
        """
        context_file = self.project_root / "memory" / "context.md"

        if not context_file.exists():
            return None

        content = context_file.read_text(encoding='utf-8')

        # Look for Active Feature
        match = re.search(r'Active Feature[:\s]+(\d{3})', content, re.IGNORECASE)

        if match:
            return match.group(1)

        return None

    def _detect_section(self, content: str) -> str:
        """Detect appropriate spec section for note content.

        Args:
            content: Note content

        Returns:
            Section name
        """
        content_lower = content.lower()

        # Keyword-based detection
        if any(kw in content_lower for kw in ["security", "auth", "permission"]):
            return "Security Considerations"
        elif any(kw in content_lower for kw in ["performance", "speed", "optimize"]):
            return "Performance Requirements"
        elif any(kw in content_lower for kw in ["constraint", "limitation", "requirement"]):
            return "Technical Constraints"
        elif any(kw in content_lower for kw in ["risk", "issue", "concern"]):
            return "Risks and Mitigations"
        else:
            return "Additional Notes"

    def _mark_note_merged(self, feature_id: str, note_id: str) -> None:
        """Mark a note as merged in the notes file.

        Args:
            feature_id: Feature ID
            note_id: Note ID
        """
        notes_file = self.notes_dir / f"{feature_id}.md"

        if not notes_file.exists():
            return

        content = notes_file.read_text(encoding='utf-8')

        # Replace "Status: Active" with "Status: Merged" for this note
        pattern = rf'(### Note {note_id}\s*\nTimestamp: .+?\s*\n)Status: Active'
        replacement = r'\1Status: Merged'

        updated_content = re.sub(pattern, replacement, content)

        notes_file.write_text(updated_content, encoding='utf-8')
