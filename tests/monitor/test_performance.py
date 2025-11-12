"""
Performance Tests for Task Monitor

Performance benchmarking and regression testing for the task monitoring system.
"""

import pytest
import time
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import psutil
import os

from specpulse.monitor import (
    TaskState, TaskInfo, ProgressData, MonitoringConfig,
    StateStorage, TaskStateManager, ProgressCalculator
)


class TestPerformance:
    """Performance tests for task monitoring system."""

    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary project directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            (project_path / ".specpulse" / "memory").mkdir(parents=True)
            (project_path / ".specpulse" / "tasks" / "001-perf-test").mkdir(parents=True)
            yield project_path

    def test_storage_performance_large_dataset(self, temp_project_dir):
        """Test storage performance with large task datasets."""

        # Create large dataset
        task_count = 5000
        tasks = []
        for i in range(task_count):
            task = TaskInfo(
                id=f"T{i:04d}",
                title=f"Performance test task {i}",
                state=TaskState.COMPLETED if i % 4 == 0 else TaskState.PENDING,
                last_updated=datetime.now() - timedelta(minutes=i),
                execution_time=float(i % 100) / 10,
                description=f"Description for task {i} with additional content to simulate real-world data size. " * 5,
                estimated_hours=1.0 + (i % 10) * 0.5
            )
            tasks.append(task)

        storage = StateStorage(temp_project_dir)

        # Test save performance
        start_time = time.time()
        storage.save_tasks(tasks, "001-perf-test")
        save_time = time.time() - start_time

        print(f"Save performance: {task_count} tasks in {save_time:.3f}s ({task_count/save_time:.0f} tasks/sec)")

        # Performance assertions
        assert save_time < 2.0, f"Save too slow: {save_time:.3f}s for {task_count} tasks"
        assert task_count / save_time > 1000, f"Save rate too low: {task_count/save_time:.0f} tasks/sec"

        # Test load performance
        start_time = time.time()
        loaded_tasks = storage.load_tasks("001-perf-test")
        load_time = time.time() - start_time

        print(f"Load performance: {len(loaded_tasks)} tasks in {load_time:.3f}s ({len(loaded_tasks)/load_time:.0f} tasks/sec)")

        assert load_time < 1.0, f"Load too slow: {load_time:.3f}s for {len(loaded_tasks)} tasks"
        assert len(loaded_tasks) / load_time > 2000, f"Load rate too low: {len(loaded_tasks)/load_time:.0f} tasks/sec"
        assert len(loaded_tasks) == task_count

    def test_calculation_performance_scalability(self, temp_project_dir):
        """Test calculation performance scales linearly with task count."""

        calculator = ProgressCalculator()
        results = {}

        for task_count in [100, 500, 1000, 2000, 5000]:
            # Create test dataset
            tasks = []
            for i in range(task_count):
                task = TaskInfo(
                    id=f"T{i:04d}",
                    title=f"Test task {i}",
                    state=TaskState.COMPLETED if i % 3 == 0 else TaskState.PENDING,
                    last_updated=datetime.now(),
                    execution_time=1.0 if i % 3 == 0 else None,
                    estimated_hours=2.0
                )
                tasks.append(task)

            # Measure calculation time
            start_time = time.time()
            progress = calculator.calculate_progress(tasks, f"001-scale-test-{task_count}")
            calc_time = time.time() - start_time

            results[task_count] = {
                'time': calc_time,
                'rate': task_count / calc_time,
                'progress': progress.percentage
            }

            print(f"Calculation performance: {task_count} tasks in {calc_time:.4f}s ({task_count/calc_time:.0f} tasks/sec)")

            # Performance should be reasonable
            assert calc_time < 0.1, f"Calculation too slow for {task_count} tasks: {calc_time:.4f}s"
            assert task_count / calc_time > 10000, f"Calculation rate too low: {task_count/calc_time:.0f} tasks/sec"

        # Check scalability (should be roughly linear)
        if len(results) >= 2:
            task_counts = sorted(results.keys())
            rates = [results[tc]['rate'] for tc in task_counts]

            # Rate should not degrade significantly with larger datasets
            rate_variation = max(rates) / min(rates)
            assert rate_variation < 5.0, f"Performance degrades too much with scale: {rate_variation:.1f}x variation"

    def test_concurrent_access_performance(self, temp_project_dir):
        """Test performance under concurrent access."""

        storage = StateStorage(temp_project_dir)
        thread_count = 10
        operations_per_thread = 100

        def worker_thread(thread_id):
            """Worker thread for concurrent operations."""
            results = []
            for i in range(operations_per_thread):
                task = TaskInfo(
                    id=f"T{thread_id:02d}-{i:03d}",
                    title=f"Thread {thread_id} Task {i}",
                    state=TaskState.COMPLETED if i % 2 == 0 else TaskState.PENDING,
                    last_updated=datetime.now()
                )

                feature_id = f"001-concurrent-{thread_id}"

                # Measure operation time
                start_time = time.time()
                storage.save_tasks([task], feature_id)
                operation_time = time.time() - start_time

                results.append(operation_time)

            return {
                'thread_id': thread_id,
                'avg_time': sum(results) / len(results),
                'max_time': max(results),
                'min_time': min(results),
                'operations': len(results)
            }

        # Run concurrent operations
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [executor.submit(worker_thread, i) for i in range(thread_count)]
            thread_results = [future.result() for future in futures]
        total_time = time.time() - start_time

        # Analyze results
        total_operations = sum(r['operations'] for r in thread_results)
        avg_operation_time = sum(r['avg_time'] for r in thread_results) / len(thread_results)
        max_operation_time = max(r['max_time'] for r in thread_results)
        overall_rate = total_operations / total_time

        print(f"Concurrent performance: {total_operations} operations in {total_time:.3f}s")
        print(f"Overall rate: {overall_rate:.0f} ops/sec, Avg operation time: {avg_operation_time:.4f}s")

        # Performance assertions
        assert total_time < 10.0, f"Concurrent operations too slow: {total_time:.3f}s"
        assert overall_rate > 100, f"Overall rate too low: {overall_rate:.0f} ops/sec"
        assert avg_operation_time < 0.1, f"Average operation time too high: {avg_operation_time:.4f}s"
        assert max_operation_time < 0.5, f"Maximum operation time too high: {max_operation_time:.4f}s"

    def test_memory_usage_under_load(self, temp_project_dir):
        """Test memory usage stays within limits under heavy load."""

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        # Create and process many tasks
        batch_size = 1000
        total_batches = 10
        memory_measurements = []

        for batch in range(total_batches):
            # Create tasks
            tasks = []
            for i in range(batch_size):
                task = TaskInfo(
                    id=f"T{batch * batch_size + i:04d}",
                    title=f"Memory test task {i}",
                    state=TaskState.COMPLETED if i % 3 == 0 else TaskState.PENDING,
                    last_updated=datetime.now(),
                    description="Large description to test memory usage. " * 10,  # ~500 bytes
                    estimated_hours=2.0
                )
                tasks.append(task)

            # Save and load tasks
            feature_id = f"001-memory-batch-{batch}"
            storage.save_tasks(tasks, feature_id)
            loaded_tasks = storage.load_tasks(feature_id)

            # Calculate progress
            progress = ProgressCalculator().calculate_progress(loaded_tasks, feature_id)

            # Measure memory usage
            current_memory = process.memory_info().rss
            memory_mb = (current_memory - initial_memory) / (1024 * 1024)
            memory_measurements.append(memory_mb)

            if batch % 3 == 0:
                print(f"Batch {batch}: Memory usage: {memory_mb:.1f}MB")

            # Memory should not grow uncontrollably
            assert memory_mb < 100, f"Memory usage too high at batch {batch}: {memory_mb:.1f}MB"

        # Analyze memory growth
        max_memory = max(memory_measurements)
        final_memory = memory_measurements[-1]

        print(f"Memory usage - Peak: {max_memory:.1f}MB, Final: {final_memory:.1f}MB")

        # Memory should be reasonable
        assert max_memory < 50, f"Peak memory usage too high: {max_memory:.1f}MB"
        assert final_memory < 30, f"Final memory usage too high: {final_memory:.1f}MB"

    def test_cache_performance(self, temp_project_dir):
        """Test caching performance benefits."""

        storage = StateStorage(temp_project_dir)
        state_manager = TaskStateManager(storage, MonitoringConfig())

        # Create tasks
        task_count = 1000
        tasks = []
        for i in range(task_count):
            task = TaskInfo(
                id=f"T{i:04d}",
                title=f"Cached task {i}",
                state=TaskState.COMPLETED if i % 2 == 0 else TaskState.PENDING,
                last_updated=datetime.now()
            )
            tasks.append(task)

        feature_id = "001-cache-test"
        storage.save_tasks(tasks, feature_id)

        # Test without cache (first load)
        start_time = time.time()
        tasks_1 = state_manager.get_tasks(feature_id)
        first_load_time = time.time() - start_time

        # Test with cache (subsequent loads)
        cache_times = []
        for i in range(10):
            start_time = time.time()
            tasks_2 = state_manager.get_tasks(feature_id)
            cache_time = time.time() - start_time
            cache_times.append(cache_time)

        avg_cache_time = sum(cache_times) / len(cache_times)

        print(f"First load: {first_load_time:.4f}s, Average cached load: {avg_cache_time:.4f}s")
        print(f"Cache speedup: {first_load_time/avg_cache_time:.1f}x")

        # Results should be consistent
        assert len(tasks_1) == len(tasks_2) == task_count

        # Cache should provide performance benefit
        if first_load_time > 0.01:  # Only check if first load was measurable
            assert avg_cache_time < first_load_time, "Cache should improve performance"
            assert first_load_time / avg_cache_time > 2.0, "Cache should provide at least 2x speedup"

    def test_backup_performance(self, temp_project_dir):
        """Test backup creation performance."""

        storage = StateStorage(temp_project_dir)

        # Configure with backup enabled
        config = MonitoringConfig(backup_enabled=True, max_backups=5)
        storage.config = config

        # Create tasks
        task_count = 1000
        tasks = []
        for i in range(task_count):
            task = TaskInfo(
                id=f"T{i:04d}",
                title=f"Backup test task {i}",
                state=TaskState.COMPLETED,
                last_updated=datetime.now()
            )
            tasks.append(task)

        feature_id = "001-backup-test"

        # Test backup performance
        backup_times = []
        for i in range(5):  # Create 5 backups
            start_time = time.time()
            storage.save_tasks(tasks, feature_id)  # This should trigger backup
            backup_time = time.time() - start_time
            backup_times.append(backup_time)

        avg_backup_time = sum(backup_times) / len(backup_times)

        print(f"Backup performance: {task_count} tasks, average backup time: {avg_backup_time:.3f}s")

        # Backup should be reasonably fast
        assert avg_backup_time < 0.5, f"Backup too slow: {avg_backup_time:.3f}s"

        # Verify backups were created
        backup_dir = temp_project_dir / ".specpulse" / "memory" / "backups"
        backup_files = list(backup_dir.glob("task-states_*.json"))
        assert len(backup_files) > 0, "Backup files should be created"

        # Verify backup limit is respected
        assert len(backup_files) <= config.max_backups, f"Too many backup files: {len(backup_files)}"

    def test_cli_performance(self, temp_project_dir):
        """Test CLI command performance."""

        from specpulse.monitor.display import StatusDisplay

        # Create test data
        tasks = []
        for i in range(1000):
            task = TaskInfo(
                id=f"T{i:04d}",
                title=f"CLI performance test task {i}",
                state=TaskState.COMPLETED if i % 3 == 0 else TaskState.PENDING,
                last_updated=datetime.now(),
                description="Test description for CLI performance testing. " * 3
            )
            tasks.append(task)

        progress = ProgressData.from_tasks(tasks, "001-cli-test")

        # Test Rich display performance
        display = StatusDisplay(no_color=False)
        start_time = time.time()
        rich_output = display.show_status(progress, tasks, verbose_mode=True)
        rich_time = time.time() - start_time

        # Test plain text display performance
        display_plain = StatusDisplay(no_color=True)
        start_time = time.time()
        plain_output = display_plain.show_status(progress, tasks, verbose_mode=True)
        plain_time = time.time() - start_time

        print(f"CLI Performance - Rich display: {rich_time:.3f}s, Plain display: {plain_time:.3f}s")

        # Both displays should be reasonably fast
        assert rich_time < 1.0, f"Rich display too slow: {rich_time:.3f}s"
        assert plain_time < 0.5, f"Plain display too slow: {plain_time:.3f}s"

        # Output should be generated
        assert len(rich_output) > 1000, "Rich output should be substantial"
        assert len(plain_output) > 1000, "Plain output should be substantial"

        # Plain text should generally be faster
        if rich_time > 0.1 and plain_time > 0.1:
            assert plain_time < rich_time, "Plain text display should be faster than Rich"

    @pytest.mark.parametrize("task_count", [100, 500, 1000, 2000])
    def test_scalability_benchmark(self, temp_project_dir, task_count):
        """Benchmark performance at different scales."""

        # Create test dataset
        tasks = []
        for i in range(task_count):
            task = TaskInfo(
                id=f"T{i:04d}",
                title=f"Benchmark task {i}",
                state=TaskState.COMPLETED if i % 4 == 0 else TaskState.PENDING,
                last_updated=datetime.now(),
                execution_time=float(i % 50) / 10,
                description="Benchmark task description with realistic content. " * 5,
                estimated_hours=1.0 + (i % 8) * 0.5
            )
            tasks.append(task)

        storage = StateStorage(temp_project_dir)
        calculator = ProgressCalculator()

        # Benchmark operations
        operations = {
            'save': lambda: storage.save_tasks(tasks, "001-benchmark"),
            'load': lambda: storage.load_tasks("001-benchmark"),
            'calculate_progress': lambda: calculator.calculate_progress(tasks, "001-benchmark"),
            'calculate_performance': lambda: calculator.calculate_performance_metrics(tasks, []),
        }

        results = {}
        for op_name, op_func in operations.items():
            # Warm up
            op_func()

            # Measure performance
            times = []
            for _ in range(5):  # Run 5 times for average
                start_time = time.time()
                op_func()
                times.append(time.time() - start_time)

            avg_time = sum(times) / len(times)
            rate = task_count / avg_time

            results[op_name] = {
                'avg_time': avg_time,
                'rate': rate,
                'task_count': task_count
            }

            print(f"Benchmark {op_name}: {task_count} tasks in {avg_time:.3f}s ({rate:.0f} tasks/sec)")

        # Performance assertions based on scale
        if task_count <= 500:
            assert results['save']['rate'] > 1000, f"Save rate too low: {results['save']['rate']:.0f} tasks/sec"
            assert results['load']['rate'] > 2000, f"Load rate too low: {results['load']['rate']:.0f} tasks/sec"
        else:
            assert results['save']['rate'] > 500, f"Save rate too low: {results['save']['rate']:.0f} tasks/sec"
            assert results['load']['rate'] > 1000, f"Load rate too low: {results['load']['rate']:.0f} tasks/sec"

        # Calculations should always be fast
        assert results['calculate_progress']['rate'] > 10000, f"Progress calculation too slow: {results['calculate_progress']['rate']:.0f} tasks/sec"

        return results