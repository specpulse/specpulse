"""
Backup Manager for safe file modifications.

Provides backup creation and rollback functionality for auto-fix operations.
"""
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
import shutil


class BackupManager:
    """
    Manages backup creation and restoration for file modifications.

    This utility ensures safe auto-fix operations by creating backups
    before any modifications and providing rollback capabilities.
    """

    def __init__(self, backup_dir: Optional[Path] = None):
        """
        Initialize BackupManager.

        Args:
            backup_dir: Directory to store backups (defaults to .specpulse/backups/)
        """
        self.backup_dir = backup_dir

    def create_backup(self, file_path: Path) -> Path:
        """
        Create a timestamped backup of a file.

        Args:
            file_path: Path to file to backup

        Returns:
            Path to the backup file

        Raises:
            FileNotFoundError: If source file doesn't exist
            IOError: If backup creation fails
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Cannot backup non-existent file: {file_path}")

        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}.bak-{timestamp}{file_path.suffix}"

        # Determine backup directory
        if self.backup_dir:
            backup_dir = self.backup_dir
        else:
            # Use .specpulse/backups/ relative to file location
            backup_dir = file_path.parent.parent.parent / ".specpulse" / "backups"

        # Create backup directory if it doesn't exist
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Create backup path
        backup_path = backup_dir / backup_name

        try:
            # Copy file to backup location
            shutil.copy2(file_path, backup_path)
            return backup_path

        except Exception as e:
            raise IOError(f"Failed to create backup: {e}")

    def restore_from_backup(self, backup_path: Path, original_path: Path) -> bool:
        """
        Restore a file from backup.

        Args:
            backup_path: Path to backup file
            original_path: Path where file should be restored

        Returns:
            True if restore successful, False otherwise

        Raises:
            FileNotFoundError: If backup file doesn't exist
        """
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        try:
            # Copy backup to original location
            shutil.copy2(backup_path, original_path)
            return True

        except Exception as e:
            print(f"Warning: Failed to restore from backup: {e}")
            return False

    def create_backup_inline(self, file_path: Path) -> Path:
        """
        Create a backup in the same directory as the original file.

        This creates a .bak file next to the original for quick rollback.

        Args:
            file_path: Path to file to backup

        Returns:
            Path to the backup file
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Cannot backup non-existent file: {file_path}")

        # Generate backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = file_path.with_suffix(f".bak-{timestamp}{file_path.suffix}")

        try:
            shutil.copy2(file_path, backup_path)
            return backup_path

        except Exception as e:
            raise IOError(f"Failed to create inline backup: {e}")

    def list_backups(self, file_path: Path) -> list[Path]:
        """
        List all backups for a given file.

        Args:
            file_path: Original file path

        Returns:
            List of backup file paths, sorted by timestamp (newest first)
        """
        if self.backup_dir:
            backup_dir = self.backup_dir
        else:
            backup_dir = file_path.parent.parent.parent / ".specpulse" / "backups"

        if not backup_dir.exists():
            return []

        # Find all backups matching the file stem
        pattern = f"{file_path.stem}.bak-*{file_path.suffix}"
        backups = list(backup_dir.glob(pattern))

        # Sort by modification time (newest first)
        backups.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        return backups

    def cleanup_old_backups(self, file_path: Path, keep_count: int = 5) -> int:
        """
        Remove old backups, keeping only the most recent ones.

        Args:
            file_path: Original file path
            keep_count: Number of backups to keep (default: 5)

        Returns:
            Number of backups deleted
        """
        backups = self.list_backups(file_path)

        if len(backups) <= keep_count:
            return 0

        # Delete old backups
        deleted_count = 0
        for backup in backups[keep_count:]:
            try:
                backup.unlink()
                deleted_count += 1
            except Exception as e:
                print(f"Warning: Failed to delete old backup {backup}: {e}")

        return deleted_count


def create_backup(file_path: Path) -> Path:
    """
    Convenience function to create a backup.

    Args:
        file_path: Path to file to backup

    Returns:
        Path to backup file
    """
    manager = BackupManager()
    return manager.create_backup(file_path)


def restore_backup(backup_path: Path, original_path: Path) -> bool:
    """
    Convenience function to restore from backup.

    Args:
        backup_path: Path to backup file
        original_path: Path to restore to

    Returns:
        True if successful, False otherwise
    """
    manager = BackupManager()
    return manager.restore_from_backup(backup_path, original_path)
