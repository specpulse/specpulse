"""
Tests for CheckpointManager (v1.9.0)
"""

import pytest
from pathlib import Path
from datetime import datetime, timedelta
import tempfile
import shutil

from specpulse.core.checkpoints import CheckpointManager, CheckpointInfo


@pytest.fixture
def temp_project(tmp_path):
    """Create temporary project structure."""
    # Create project structure
    specs_dir = tmp_path / "specs" / "003-test-feature"
    specs_dir.mkdir(parents=True)

    # Create sample spec file
    spec_content = """---
tier: minimal
progress: 1.0
sections_completed:
  - what
  - why
  - done_when
last_updated: 2025-10-06
---

## What
Test feature for authentication

## Why
Security requirement

## Done When
- [ ] Users can login
- [ ] Users can logout
- [ ] Sessions expire after 24h
"""
    spec_file = specs_dir / "spec-001.md"
    spec_file.write_text(spec_content, encoding="utf-8")

    return tmp_path


@pytest.fixture
def checkpoint_mgr(temp_project):
    """Create CheckpointManager instance."""
    return CheckpointManager(temp_project)


class TestCheckpointCreation:
    """Tests for checkpoint creation."""

    def test_create_checkpoint(self, checkpoint_mgr, temp_project):
        """Test basic checkpoint creation."""
        checkpoint_name = checkpoint_mgr.create("003-test-feature", "Initial checkpoint")

        assert checkpoint_name == "checkpoint-001"

        # Verify files created
        checkpoint_dir = temp_project / ".specpulse" / "checkpoints" / "003-test-feature"
        assert (checkpoint_dir / "checkpoint-001.spec.md").exists()
        assert (checkpoint_dir / "checkpoint-001.meta.yaml").exists()

    def test_checkpoint_metadata(self, checkpoint_mgr, temp_project):
        """Test that metadata is correctly stored."""
        checkpoint_name = checkpoint_mgr.create("003-test-feature", "Test checkpoint")

        # Read metadata
        checkpoint_dir = temp_project / ".specpulse" / "checkpoints" / "003-test-feature"
        import yaml

        with open(checkpoint_dir / f"{checkpoint_name}.meta.yaml") as f:
            metadata = yaml.safe_load(f)

        assert metadata["description"] == "Test checkpoint"
        assert metadata["tier"] == "minimal"
        assert metadata["progress"] == 1.0
        assert "file_hash" in metadata
        assert "created" in metadata

    def test_sequential_checkpoint_naming(self, checkpoint_mgr):
        """Test that checkpoints are numbered sequentially."""
        cp1 = checkpoint_mgr.create("003-test-feature", "First")
        cp2 = checkpoint_mgr.create("003-test-feature", "Second")
        cp3 = checkpoint_mgr.create("003-test-feature", "Third")

        assert cp1 == "checkpoint-001"
        assert cp2 == "checkpoint-002"
        assert cp3 == "checkpoint-003"

    def test_checkpoint_content_preservation(self, checkpoint_mgr, temp_project):
        """Test that checkpoint preserves exact spec content."""
        # Get original content
        spec_file = temp_project / "specs" / "003-test-feature" / "spec-001.md"
        original_content = spec_file.read_text(encoding="utf-8")

        # Create checkpoint
        checkpoint_name = checkpoint_mgr.create("003-test-feature", "Preserve test")

        # Read checkpoint file
        checkpoint_dir = temp_project / ".specpulse" / "checkpoints" / "003-test-feature"
        checkpoint_file = checkpoint_dir / f"{checkpoint_name}.spec.md"
        checkpoint_content = checkpoint_file.read_text(encoding="utf-8")

        assert checkpoint_content == original_content


class TestCheckpointListing:
    """Tests for checkpoint listing."""

    def test_list_empty(self, checkpoint_mgr):
        """Test listing when no checkpoints exist."""
        checkpoints = checkpoint_mgr.list("003-test-feature")
        assert checkpoints == []

    def test_list_checkpoints(self, checkpoint_mgr):
        """Test listing multiple checkpoints."""
        checkpoint_mgr.create("003-test-feature", "First")
        checkpoint_mgr.create("003-test-feature", "Second")
        checkpoint_mgr.create("003-test-feature", "Third")

        checkpoints = checkpoint_mgr.list("003-test-feature")

        assert len(checkpoints) == 3
        assert all(isinstance(cp, CheckpointInfo) for cp in checkpoints)

    def test_list_sorted_by_date(self, checkpoint_mgr):
        """Test that checkpoints are sorted newest first."""
        import time

        checkpoint_mgr.create("003-test-feature", "Old")
        time.sleep(0.1)
        checkpoint_mgr.create("003-test-feature", "New")

        checkpoints = checkpoint_mgr.list("003-test-feature")

        # Newest should be first
        assert checkpoints[0].description == "New"
        assert checkpoints[1].description == "Old"


class TestCheckpointRestoration:
    """Tests for checkpoint restoration."""

    def test_restore_checkpoint(self, checkpoint_mgr, temp_project):
        """Test basic checkpoint restoration."""
        spec_file = temp_project / "specs" / "003-test-feature" / "spec-001.md"

        # Create checkpoint
        original_content = spec_file.read_text(encoding="utf-8")
        checkpoint_name = checkpoint_mgr.create("003-test-feature", "Before changes")

        # Modify spec
        spec_file.write_text(original_content + "\n\n## New Section\nAdded content", encoding="utf-8")

        # Restore
        success = checkpoint_mgr.restore("003-test-feature", checkpoint_name, force=True)

        assert success
        # Content should match original
        restored_content = spec_file.read_text(encoding="utf-8")
        assert restored_content == original_content

    def test_restore_nonexistent_checkpoint(self, checkpoint_mgr):
        """Test restoring nonexistent checkpoint raises error."""
        with pytest.raises(FileNotFoundError):
            checkpoint_mgr.restore("003-test-feature", "checkpoint-999", force=True)

    def test_restore_creates_safety_backup(self, checkpoint_mgr, temp_project):
        """Test that safety backup is created during restore."""
        spec_file = temp_project / "specs" / "003-test-feature" / "spec-001.md"

        # Create checkpoint
        checkpoint_name = checkpoint_mgr.create("003-test-feature", "Before")

        # Modify spec
        original = spec_file.read_text(encoding="utf-8")
        spec_file.write_text(original + "\n\nModified", encoding="utf-8")

        # Restore (should create safety backup in temp)
        checkpoint_mgr.restore("003-test-feature", checkpoint_name, force=True)

        # Verify restoration worked
        assert spec_file.read_text(encoding="utf-8") == original


class TestCheckpointCleanup:
    """Tests for checkpoint cleanup."""

    def test_cleanup_old_checkpoints(self, checkpoint_mgr, temp_project):
        """Test deletion of old checkpoints."""
        # Create checkpoints
        cp1 = checkpoint_mgr.create("003-test-feature", "Old checkpoint")

        # Manually set old date in metadata
        checkpoint_dir = temp_project / ".specpulse" / "checkpoints" / "003-test-feature"
        meta_file = checkpoint_dir / f"{cp1}.meta.yaml"

        import yaml

        with open(meta_file) as f:
            metadata = yaml.safe_load(f)

        # Set created date to 60 days ago
        old_date = datetime.now() - timedelta(days=60)
        metadata["created"] = old_date.isoformat()

        with open(meta_file, "w") as f:
            yaml.dump(metadata, f)

        # Cleanup checkpoints older than 30 days
        deleted = checkpoint_mgr.cleanup("003-test-feature", older_than_days=30)

        assert deleted == 1
        assert not (checkpoint_dir / f"{cp1}.spec.md").exists()
        assert not (checkpoint_dir / f"{cp1}.meta.yaml").exists()

    def test_cleanup_no_old_checkpoints(self, checkpoint_mgr):
        """Test cleanup when no old checkpoints."""
        checkpoint_mgr.create("003-test-feature", "Recent")

        deleted = checkpoint_mgr.cleanup("003-test-feature", older_than_days=30)

        assert deleted == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
