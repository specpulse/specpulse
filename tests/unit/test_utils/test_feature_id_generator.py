"""
Tests for Thread-Safe Feature ID Generator

Tests cover:
- Sequential ID generation
- Concurrent ID generation (no duplicates)
- Lock acquisition and release
- Counter persistence
- Initialization from existing features
- Error handling and timeouts
"""

import pytest
import tempfile
from pathlib import Path
import threading
import time

from specpulse.core.feature_id_generator import (
    FeatureIDGenerator,
    get_next_feature_id
)


class TestSequentialGeneration:
    """Test sequential feature ID generation"""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".specpulse").mkdir()
            (project_root / "specs").mkdir()
            yield project_root

    def test_first_id_is_001(self, temp_project):
        """Test that first feature ID is 001"""
        gen = FeatureIDGenerator(temp_project)
        first_id = gen.get_next_id()
        assert first_id == "001"

    def test_sequential_ids(self, temp_project):
        """Test that IDs increment sequentially"""
        gen = FeatureIDGenerator(temp_project)

        ids = [gen.get_next_id() for _ in range(10)]

        expected = [f"{i:03d}" for i in range(1, 11)]
        assert ids == expected

    def test_counter_persistence(self, temp_project):
        """Test that counter persists across instances"""
        # First generator
        gen1 = FeatureIDGenerator(temp_project)
        id1 = gen1.get_next_id()  # "001"
        id2 = gen1.get_next_id()  # "002"

        # Second generator (simulates new process)
        gen2 = FeatureIDGenerator(temp_project)
        id3 = gen2.get_next_id()  # Should be "003", not "001"

        assert id1 == "001"
        assert id2 == "002"
        assert id3 == "003"

    def test_counter_file_created(self, temp_project):
        """Test that counter file is created"""
        gen = FeatureIDGenerator(temp_project)
        gen.get_next_id()

        counter_file = temp_project / ".specpulse" / "feature_counter.txt"
        assert counter_file.exists()

        content = counter_file.read_text()
        assert content == "1"

    def test_get_current_id(self, temp_project):
        """Test getting current ID without incrementing"""
        gen = FeatureIDGenerator(temp_project)

        # Generate some IDs
        gen.get_next_id()  # 001
        gen.get_next_id()  # 002

        # Current should be 2
        current = gen.get_current_id()
        assert current == 2

        # Next should be 003
        next_id = gen.get_next_id()
        assert next_id == "003"


class TestConcurrentGeneration:
    """Test concurrent feature ID generation (critical for race condition prevention)"""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".specpulse").mkdir()
            (project_root / "specs").mkdir()
            yield project_root

    def test_concurrent_generation_no_duplicates(self, temp_project):
        """
        CRITICAL: Test that concurrent ID generation produces no duplicates

        This simulates the race condition scenario where multiple threads/processes
        create features simultaneously.
        """
        generated_ids = []
        errors = []

        def generate_id(thread_num):
            """Thread worker function"""
            try:
                gen = FeatureIDGenerator(temp_project)
                feature_id = gen.get_next_id()
                generated_ids.append(feature_id)
            except Exception as e:
                errors.append((thread_num, str(e)))

        # Create 10 threads that generate IDs simultaneously
        threads = []
        for i in range(10):
            thread = threading.Thread(target=generate_id, args=(i,))
            threads.append(thread)

        # Start all threads at once
        for thread in threads:
            thread.start()

        # Wait for all to complete
        for thread in threads:
            thread.join(timeout=10.0)

        # Verify results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(generated_ids) == 10, f"Expected 10 IDs, got {len(generated_ids)}"

        # CRITICAL: No duplicates
        assert len(set(generated_ids)) == 10, (
            f"Duplicate IDs detected! Generated: {sorted(generated_ids)}"
        )

        # Verify sequential
        expected = [f"{i:03d}" for i in range(1, 11)]
        assert sorted(generated_ids) == expected

    def test_high_concurrency(self, temp_project):
        """Test with higher concurrency (50 threads)"""
        generated_ids = []

        def generate_id():
            gen = FeatureIDGenerator(temp_project)
            feature_id = gen.get_next_id()
            generated_ids.append(feature_id)

        threads = [threading.Thread(target=generate_id) for _ in range(50)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(timeout=15.0)

        # Verify no duplicates
        assert len(generated_ids) == 50
        assert len(set(generated_ids)) == 50, "Duplicate IDs in high concurrency test!"

    def test_lock_timeout(self, temp_project):
        """Test that lock timeout works"""
        gen = FeatureIDGenerator(temp_project)

        # Reduce timeout for testing
        gen.LOCK_TIMEOUT = 0.5

        # Acquire lock and hold it
        lock_file = gen.lock_file
        if not lock_file.exists():
            lock_file.touch()

        import platform
        if platform.system() == 'Windows':
            import msvcrt
            with lock_file.open('w') as f:
                msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)

                # Try to get ID (should timeout)
                with pytest.raises(TimeoutError, match="Could not acquire"):
                    gen.get_next_id()

                # Release lock
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            with lock_file.open('w') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)

                # Try to get ID in another thread (should timeout)
                def try_get_id():
                    with pytest.raises(TimeoutError):
                        gen.get_next_id()

                thread = threading.Thread(target=try_get_id)
                thread.start()
                thread.join(timeout=2.0)

                # Release lock
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class TestInitializationFromExisting:
    """Test initialization from existing feature directories"""

    @pytest.fixture
    def temp_project_with_features(self):
        """Create project with existing features"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".specpulse").mkdir()
            specs_dir = project_root / "specs"
            specs_dir.mkdir()

            # Create existing feature directories
            (specs_dir / "001-auth").mkdir()
            (specs_dir / "002-payment").mkdir()
            (specs_dir / "005-dashboard").mkdir()  # Gap in sequence

            yield project_root

    def test_initialize_from_existing_features(self, temp_project_with_features):
        """Test that counter initializes from existing features"""
        gen = FeatureIDGenerator(temp_project_with_features)

        # Initialize should find highest ID (005)
        max_id = gen.initialize_from_existing()
        assert max_id == 5

        # Next ID should be 006
        next_id = gen.get_next_id()
        assert next_id == "006"

    def test_no_existing_features(self, temp_project_with_features):
        """Test initialization with no features"""
        # Remove all features
        specs_dir = temp_project_with_features / "specs"
        for item in specs_dir.iterdir():
            if item.is_dir():
                item.rmdir()

        gen = FeatureIDGenerator(temp_project_with_features)
        max_id = gen.initialize_from_existing()

        assert max_id == 0

        # First ID should be 001
        first_id = gen.get_next_id()
        assert first_id == "001"


class TestErrorHandling:
    """Test error handling and edge cases"""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".specpulse").mkdir()
            yield project_root

    def test_corrupted_counter_file(self, temp_project):
        """Test recovery from corrupted counter file"""
        gen = FeatureIDGenerator(temp_project)

        # Write invalid content to counter file
        gen.counter_file.write_text("invalid_number")

        # Should reinitialize (no features = 0)
        next_id = gen.get_next_id()
        assert next_id == "001"

    def test_missing_config_directory(self):
        """Test that missing .specpulse directory is created"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            # Don't create .specpulse directory

            gen = FeatureIDGenerator(project_root)
            next_id = gen.get_next_id()

            # Should create directory and work
            assert (project_root / ".specpulse").exists()
            assert next_id == "001"

    def test_permission_error_handling(self, temp_project):
        """Test handling of permission errors"""
        gen = FeatureIDGenerator(temp_project)

        # Make counter file read-only (simulate permission error)
        counter_file = gen.counter_file
        counter_file.touch()

        # On Unix, we can actually test this
        # On Windows, might not be possible
        import platform
        if platform.system() != 'Windows':
            import os
            counter_file.chmod(0o444)  # Read-only

            with pytest.raises(IOError):
                gen.get_next_id()

            # Restore permissions
            counter_file.chmod(0o644)


class TestPerformance:
    """Performance tests for ID generation"""

    def test_generation_performance(self):
        """Test that ID generation is fast"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".specpulse").mkdir()

            gen = FeatureIDGenerator(project_root)

            # Generate 100 IDs and measure time
            start = time.time()
            ids = [gen.get_next_id() for _ in range(100)]
            duration = time.time() - start

            # Should complete in under 1 second
            assert duration < 1.0, f"ID generation too slow: {duration:.2f}s"

            # Verify all IDs are unique
            assert len(set(ids)) == 100


class TestConvenienceFunction:
    """Test convenience function"""

    def test_get_next_feature_id_function(self):
        """Test convenience wrapper function"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".specpulse").mkdir()

            id1 = get_next_feature_id(project_root)
            id2 = get_next_feature_id(project_root)

            assert id1 == "001"
            assert id2 == "002"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
