"""
Checkpoint Manager for SpecPulse (v1.9.0)

Automatic versioning and rollback capability for specifications.
"""

from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import shutil
import hashlib
import yaml
import re


@dataclass
class CheckpointInfo:
    """Information about a checkpoint."""

    name: str
    description: str
    created: datetime
    spec_file: str
    tier: str
    progress: float
    file_hash: str
    file_size_bytes: int


class CheckpointManager:
    """
    Manages checkpoint lifecycle for specifications.

    Responsibilities:
    - Create checkpoints before risky operations
    - List all checkpoints for a feature
    - Restore specs to previous checkpoints
    - Cleanup old checkpoints
    """

    def __init__(self, project_root: Path):
        """
        Initialize CheckpointManager.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root)
        self.checkpoints_dir = self.project_root / ".specpulse" / "checkpoints"
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

    def create(
        self, feature_id: str, description: str, spec_file: Optional[Path] = None
    ) -> str:
        """
        Create checkpoint for a feature.

        Args:
            feature_id: Feature identifier (e.g., "003" or "003-feature-name")
            description: Human-readable description of checkpoint
            spec_file: Specific spec file to checkpoint (default: latest)

        Returns:
            Checkpoint name (e.g., "checkpoint-001")

        Raises:
            FileNotFoundError: If spec file doesn't exist
        """
        # Find spec file if not provided
        if spec_file is None:
            spec_file = self._find_latest_spec(feature_id)

        if not spec_file.exists():
            raise FileNotFoundError(f"Spec file not found: {spec_file}")

        # Create feature checkpoint directory
        feature_checkpoint_dir = self.checkpoints_dir / feature_id
        feature_checkpoint_dir.mkdir(parents=True, exist_ok=True)

        # Generate checkpoint name
        checkpoint_name = self._generate_checkpoint_name(feature_checkpoint_dir)

        # Read spec content
        spec_content = spec_file.read_text(encoding="utf-8")

        # Calculate metadata
        file_hash = self._calculate_hash(spec_content)
        file_size = len(spec_content.encode("utf-8"))
        tier, progress = self._extract_metadata(spec_content)

        # Create checkpoint file (copy of spec)
        checkpoint_file = feature_checkpoint_dir / f"{checkpoint_name}.spec.md"
        checkpoint_file.write_text(spec_content, encoding="utf-8")

        # Create metadata file
        metadata = {
            "created": datetime.now().isoformat(),
            "description": description,
            "spec_file": spec_file.name,
            "tier": tier,
            "progress": progress,
            "file_hash": file_hash,
            "file_size_bytes": file_size,
        }

        metadata_file = feature_checkpoint_dir / f"{checkpoint_name}.meta.yaml"
        with open(metadata_file, "w", encoding="utf-8") as f:
            yaml.dump(metadata, f, default_flow_style=False)

        return checkpoint_name

    def list(self, feature_id: str) -> List[CheckpointInfo]:
        """
        List all checkpoints for a feature.

        Args:
            feature_id: Feature identifier

        Returns:
            List of CheckpointInfo objects, sorted by creation time (newest first)
        """
        feature_checkpoint_dir = self.checkpoints_dir / feature_id

        if not feature_checkpoint_dir.exists():
            return []

        checkpoints = []
        metadata_files = sorted(feature_checkpoint_dir.glob("*.meta.yaml"))

        for meta_file in metadata_files:
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    metadata = yaml.safe_load(f)

                checkpoint_name = meta_file.stem.replace(".meta", "")

                checkpoints.append(
                    CheckpointInfo(
                        name=checkpoint_name,
                        description=metadata.get("description", ""),
                        created=datetime.fromisoformat(metadata.get("created", "")),
                        spec_file=metadata.get("spec_file", ""),
                        tier=metadata.get("tier", "unknown"),
                        progress=metadata.get("progress", 0.0),
                        file_hash=metadata.get("file_hash", ""),
                        file_size_bytes=metadata.get("file_size_bytes", 0),
                    )
                )
            except Exception:
                # Skip corrupt metadata files
                continue

        # Sort by creation time, newest first
        checkpoints.sort(key=lambda c: c.created, reverse=True)

        return checkpoints

    def restore(
        self, feature_id: str, checkpoint_name: str, force: bool = False
    ) -> bool:
        """
        Restore spec to previous checkpoint.

        Args:
            feature_id: Feature identifier
            checkpoint_name: Checkpoint to restore (e.g., "checkpoint-001")
            force: Skip confirmation prompt

        Returns:
            True if successful, False otherwise

        Raises:
            FileNotFoundError: If checkpoint doesn't exist
        """
        feature_checkpoint_dir = self.checkpoints_dir / feature_id
        checkpoint_file = feature_checkpoint_dir / f"{checkpoint_name}.spec.md"
        metadata_file = feature_checkpoint_dir / f"{checkpoint_name}.meta.yaml"

        if not checkpoint_file.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_name}")

        # Load metadata
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)

        # Find target spec file
        spec_file = self._find_latest_spec(feature_id)

        # Verify checkpoint integrity
        checkpoint_content = checkpoint_file.read_text(encoding="utf-8")
        expected_hash = metadata.get("file_hash", "")
        actual_hash = self._calculate_hash(checkpoint_content)

        if expected_hash != actual_hash:
            raise ValueError(
                f"Checkpoint integrity check failed. File may be corrupted."
            )

        # Create safety backup of current state
        current_content = spec_file.read_text(encoding="utf-8")
        safety_backup = self._create_safety_backup(spec_file)

        try:
            # Show diff preview
            if not force:
                self._show_restore_diff(current_content, checkpoint_content, metadata)
                response = input("\nContinue with restoration? [y/N]: ")
                if response.lower() != "y":
                    # Cleanup safety backup
                    safety_backup.unlink()
                    return False

            # Restore checkpoint
            spec_file.write_text(checkpoint_content, encoding="utf-8")

            # Verify restoration
            restored_content = spec_file.read_text(encoding="utf-8")
            restored_hash = self._calculate_hash(restored_content)

            if restored_hash != expected_hash:
                # Rollback failed restoration
                spec_file.write_text(current_content, encoding="utf-8")
                raise ValueError("Restoration verification failed. Changes rolled back.")

            # Cleanup safety backup after successful restore
            safety_backup.unlink()

            return True

        except Exception as e:
            # Restore from safety backup
            if safety_backup.exists():
                spec_file.write_text(current_content, encoding="utf-8")
                safety_backup.unlink()
            raise

    def cleanup(self, feature_id: str, older_than_days: int = 30) -> int:
        """
        Delete old checkpoints.

        Args:
            feature_id: Feature identifier
            older_than_days: Delete checkpoints older than this many days

        Returns:
            Number of checkpoints deleted
        """
        feature_checkpoint_dir = self.checkpoints_dir / feature_id

        if not feature_checkpoint_dir.exists():
            return 0

        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        deleted_count = 0

        checkpoints = self.list(feature_id)

        for checkpoint in checkpoints:
            if checkpoint.created < cutoff_date:
                # Delete checkpoint files
                checkpoint_file = (
                    feature_checkpoint_dir / f"{checkpoint.name}.spec.md"
                )
                metadata_file = (
                    feature_checkpoint_dir / f"{checkpoint.name}.meta.yaml"
                )

                if checkpoint_file.exists():
                    checkpoint_file.unlink()
                if metadata_file.exists():
                    metadata_file.unlink()

                deleted_count += 1

        return deleted_count

    # Private helper methods

    def _find_latest_spec(self, feature_id: str) -> Path:
        """Find the latest spec file for a feature."""
        specs_dir = self.project_root / "specs"

        # Find feature directory
        feature_dirs = list(specs_dir.glob(f"*{feature_id}*"))

        if not feature_dirs:
            raise FileNotFoundError(f"Feature directory not found for: {feature_id}")

        feature_dir = feature_dirs[0]

        # Find latest spec file
        spec_files = sorted(feature_dir.glob("spec-*.md"))

        if not spec_files:
            raise FileNotFoundError(f"No spec files found in {feature_dir}")

        return spec_files[-1]

    def _generate_checkpoint_name(self, checkpoint_dir: Path) -> str:
        """Generate sequential checkpoint name."""
        existing = list(checkpoint_dir.glob("checkpoint-*.spec.md"))
        if not existing:
            return "checkpoint-001"

        # Extract numbers
        numbers = []
        for f in existing:
            match = re.search(r"checkpoint-(\d+)", f.stem)
            if match:
                numbers.append(int(match.group(1)))

        next_num = max(numbers) + 1 if numbers else 1
        return f"checkpoint-{next_num:03d}"

    def _calculate_hash(self, content: str) -> str:
        """Calculate SHA-256 hash of content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _extract_metadata(self, content: str) -> tuple[str, float]:
        """
        Extract tier and progress from spec content.

        Returns:
            Tuple of (tier, progress)
        """
        # Parse YAML frontmatter
        lines = content.split("\n")
        in_frontmatter = False
        tier = "unknown"
        progress = 0.0

        for line in lines:
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break
            if in_frontmatter:
                if line.startswith("tier:"):
                    try:
                        parts = line.split(":", 1)
                        if len(parts) == 2:
                            tier = parts[1].strip()
                    except (ValueError, IndexError):
                        pass
                elif line.startswith("progress:"):
                    try:
                        parts = line.split(":", 1)
                        if len(parts) == 2:
                            progress = float(parts[1].strip())
                    except (ValueError, IndexError):
                        progress = 0.0

        return tier, progress

    def _create_safety_backup(self, spec_file: Path) -> Path:
        """Create temporary safety backup."""
        import tempfile

        temp_dir = Path(tempfile.gettempdir())
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f"{spec_file.stem}.safety-{timestamp}{spec_file.suffix}"
        backup_path = temp_dir / backup_name

        shutil.copy2(spec_file, backup_path)

        return backup_path

    def _show_restore_diff(
        self, current_content: str, checkpoint_content: str, metadata: dict
    ) -> None:
        """Show diff preview before restoration."""
        print(f"\nRestoring to: {metadata.get('description', 'Unknown')}")
        print(f"Created: {metadata.get('created', 'Unknown')}")
        print(f"\nChanges:")

        current_tier, current_progress = self._extract_metadata(current_content)
        checkpoint_tier = metadata.get("tier", "unknown")
        checkpoint_progress = metadata.get("progress", 0.0)

        print(f"  Tier: {current_tier} → {checkpoint_tier}")
        print(f"  Progress: {current_progress:.0%} → {checkpoint_progress:.0%}")

        # Count sections
        current_sections = len(re.findall(r"^## ", current_content, re.MULTILINE))
        checkpoint_sections = len(
            re.findall(r"^## ", checkpoint_content, re.MULTILINE)
        )
        print(f"  Sections: {current_sections} → {checkpoint_sections}")
