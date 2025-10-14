#!/usr/bin/env python3
"""
Migration Script: Initialize Feature Counter

This script initializes the thread-safe feature counter for existing SpecPulse projects.
It scans existing feature directories and sets the counter accordingly.

Usage:
    python scripts/migrate_feature_counter.py
    python scripts/migrate_feature_counter.py /path/to/project

This is a one-time migration for projects created before v2.1.4.
New projects automatically use the thread-safe counter.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from specpulse.core.feature_id_generator import FeatureIDGenerator
from specpulse.utils.console import Console


def migrate_project(project_root: Path, dry_run: bool = False) -> bool:
    """
    Migrate existing project to use thread-safe feature ID generator.

    Args:
        project_root: Project root directory
        dry_run: If True, only report what would be done

    Returns:
        True if successful, False otherwise
    """
    console = Console()

    console.header("Feature Counter Migration", style="bright_cyan")
    console.info(f"Project: {project_root}")

    # Check if this is a SpecPulse project
    if not (project_root / ".specpulse").exists():
        console.error("Not a SpecPulse project (missing .specpulse directory)")
        return False

    # Check if already migrated
    counter_file = project_root / ".specpulse" / "feature_counter.txt"
    if counter_file.exists():
        console.warning("Counter file already exists. Project may already be migrated.")
        current_value = counter_file.read_text().strip()
        console.info(f"Current counter value: {current_value}")

        # Ask for confirmation
        response = input("Reinitialize counter from existing features? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            console.info("Migration cancelled")
            return False

    # Initialize generator
    generator = FeatureIDGenerator(project_root)

    # Scan existing features
    console.info("\nScanning existing features...")
    max_id = generator.initialize_from_existing()

    # Report findings
    specs_dir = project_root / "specs"
    if specs_dir.exists():
        features = [
            d.name for d in specs_dir.iterdir()
            if d.is_dir() and d.name[0].isdigit()
        ]

        console.success(f"Found {len(features)} existing features:")
        for feature in sorted(features):
            console.info(f"  - {feature}")

    console.info(f"\nHighest feature ID: {max_id:03d}")
    console.info(f"Next feature ID will be: {max_id + 1:03d}")

    if dry_run:
        console.warning("\nDRY RUN - No changes made")
        return True

    # Write counter
    console.info("\nWriting counter file...")
    counter_file.write_text(str(max_id))

    console.success(f"\n✓ Migration complete!")
    console.success(f"Counter initialized: {counter_file}")
    console.success(f"Current value: {max_id}")
    console.success(f"Next feature ID: {max_id + 1:03d}")

    console.info("\nℹ All future feature creations will use thread-safe ID generation.")

    return True


def main():
    """Main entry point"""
    console = Console()

    # Get project root from argument or use current directory
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1])
    else:
        project_root = Path.cwd()

    # Check for --dry-run flag
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv

    if dry_run:
        console.info("Running in DRY RUN mode (no changes will be made)\n")

    # Validate project root exists
    if not project_root.exists():
        console.error(f"Project directory does not exist: {project_root}")
        return 1

    # Run migration
    success = migrate_project(project_root, dry_run=dry_run)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
