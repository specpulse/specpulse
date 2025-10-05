"""
Performance Tests for SpecPulse
"""

import pytest
import time
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from unittest.mock import patch

from specpulse.core.template_manager import TemplateManager
from specpulse.core.memory_manager import MemoryManager
from specpulse.core.validator import Validator
from specpulse.cli.main import SpecPulseCLI


class TestPerformance:
    """Performance benchmarking tests"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_initialization_performance(self):
        """Test SpecPulse CLI initialization performance"""
        start_time = time.time()

        cli = SpecPulseCLI(no_color=True, verbose=False)

        end_time = time.time()
        initialization_time = end_time - start_time

        # Should initialize within 2 seconds
        assert initialization_time < 2.0, f"Initialization took {initialization_time:.2f}s, should be < 2.0s"

        print(f"CLI Initialization: {initialization_time:.3f}s")

    def test_project_initialization_performance(self):
        """Test project initialization performance"""
        cli = SpecPulseCLI(no_color=True, verbose=False)

        start_time = time.time()
        success = cli.init("perf-test", here=True)
        end_time = time.time()

        init_time = end_time - start_time
        assert success, "Project initialization should succeed"
        assert init_time < 5.0, f"Project initialization took {init_time:.2f}s, should be < 5.0s"

        print(f"Project Initialization: {init_time:.3f}s")

    def test_template_validation_performance(self):
        """Test template validation performance with many templates"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("perf-templates", here=True)

        template_manager = TemplateManager(self.project_path)

        # Create multiple templates
        templates_dir = self.project_path / "templates"
        num_templates = 50

        for i in range(num_templates):
            template_path = templates_dir / f"test_template_{i}.md"
            template_content = f"""
# Test Template {i}

## Variables
- feature_name: {{{{ feature_name }}}}
- spec_id: {{{{ spec_id }}}}
- date: {{{{ date }}}}

## Content
This is test template {i} for {{{{ feature_name }}}.

## Sections
{chr(10).join(f"## Section {j}\\nContent for section {j}\\n" for j in range(5))}
"""
            template_path.write_text(template_content)

        # Measure validation performance
        start_time = time.time()
        results = template_manager.validate_all_templates()
        end_time = time.time()

        validation_time = end_time - start_time
        assert len(results) == num_templates + 3  # 3 default templates + our test templates
        assert validation_time < 2.0, f"Validating {num_templates} templates took {validation_time:.2f}s, should be < 2.0s"

        print(f"Template Validation ({num_templates} templates): {validation_time:.3f}s")

    def test_memory_operations_performance(self):
        """Test memory system performance with many entries"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("perf-memory", here=True)

        memory_manager = MemoryManager(self.project_path)
        num_entries = 100

        # Measure bulk context updates
        start_time = time.time()
        for i in range(num_entries):
            memory_manager.update_context(
                feature_name=f"Feature {i}",
                feature_id=f"{i:03d}",
                action=f"action_{i % 10}",
                details={"iteration": i, "batch": "performance_test"},
                impact="medium",
                category="spec"
            )
        end_time = time.time()

        update_time = end_time - start_time
        assert update_time < 3.0, f"Updating {num_entries} context entries took {update_time:.2f}s, should be < 3.0s"

        print(f"Memory Updates ({num_entries} entries): {update_time:.3f}s")

        # Measure search performance
        start_time = time.time()
        search_results = memory_manager.search_memory("Feature")
        end_time = time.time()

        search_time = end_time - start_time
        assert len(search_results) == num_entries
        assert search_time < 1.0, f"Search took {search_time:.3f}s, should be < 1.0s"

        print(f"Memory Search ({len(search_results)} results): {search_time:.3f}s")

    def test_validation_system_performance(self):
        """Test validation system performance"""
        # Initialize project with many files
        cli = SpecPulseCLI(no_color=True)
        cli.init("perf-validation", here=True)

        validator = Validator(self.project_path)

        # Create many specification files
        num_specs = 20
        for i in range(num_specs):
            feature_id = f"{i+1:03d}-feature-{i+1}"
            spec_dir = self.project_path / "specs" / feature_id
            spec_dir.mkdir(parents=True)

            spec_file = spec_dir / f"spec-{i+1:03d}.md"
            spec_content = f"""
# Specification: Feature {i+1}

## Functional Requirements
FR-00{i}: Requirement {i+1}
- Acceptance: Test acceptance {i+1}
- Priority: MUST

## User Stories
### Story {i+1}: User Story {i+1}
**As a** user
**I want** feature {i+1}
**So that** benefit {i+1}

**Acceptance Criteria:**
- [ ] Criterion {i+1}.1
- [ ] Criterion {i+1}.2
- [ ] Criterion {i+1}.3

## Acceptance Criteria
- [ ] All requirements implemented
- [ ] User stories completed
"""
            spec_file.write_text(spec_content)

        # Create corresponding plan and task files
        for i in range(num_specs):
            feature_id = f"{i+1:03d}-feature-{i+1}"

            # Plan file
            plan_dir = self.project_path / "plans" / feature_id
            plan_dir.mkdir(parents=True)

            plan_file = plan_dir / f"plan-{i+1:03d}.md"
            plan_file.write_text(f"""
# Implementation Plan: Feature {i+1}

## Architecture Overview
Implementation plan for feature {i+1}

## Phase 1: Core Implementation
### Objectives
- Implement core functionality for feature {i+1}

### Tasks
- [ ] Task {i+1}.1
- [ ] Task {i+1}.2
- [ ] Task {i+1}.3

## Success Criteria
- Feature {i+1} works correctly
- All requirements met
""")

            # Task file
            task_dir = self.project_path / "tasks" / feature_id
            task_dir.mkdir(parents=True)

            task_file = task_dir / f"task-{i+1:03d}.md"
            task_file.write_text(f"""
# Task Breakdown: Feature {i+1}

### T{i+1:03d}: Task {i+1}
**Status**: [ ]
**Effort**: 4 hours

### T{i+2:03d}: Task {i+1}
**Status**: [ ]
**Effort**: 6 hours

## Progress Tracking
- Total Tasks: 2
- Completed: 0
- In Progress: 0
""")

        # Measure validation performance
        start_time = time.time()
        validation_results = validator.validate_all(self.project_path, verbose=False)
        end_time = time.time()

        validation_time = end_time - start_time
        assert len(validation_results) > 0
        assert validation_time < 5.0, f"Validating {num_specs*3} files took {validation_time:.2f}s, should be < 5.0s"

        print(f"System Validation ({num_specs*3} files): {validation_time:.3f}s")

    def test_large_project_simulation_performance(self):
        """Test performance with simulated large project"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("perf-large", here=True)

        template_manager = TemplateManager(self.project_path)
        memory_manager = MemoryManager(self.project_path)

        # Simulate large project with many features
        num_features = 100
        start_time = time.time()

        for i in range(num_features):
            feature_id = f"{i+1:03d}-feature-{i+1}"

            # Create directories and files
            spec_dir = self.project_path / "specs" / feature_id
            spec_dir.mkdir(parents=True)
            (spec_dir / f"spec-{i+1:03d}.md").write_text(f"# Spec {i+1}")

            plan_dir = self.project_path / "plans" / feature_id
            plan_dir.mkdir(parents=True)
            (plan_dir / f"plan-{i+1:03d}.md").write_text(f"# Plan {i+1}")

            task_dir = self.project_path / "tasks" / feature_id
            task_dir.mkdir(parents=True)
            (task_dir / f"task-{i+1:03d}.md").write_text(f"# Tasks {i+1}")

            # Update memory every 10 features
            if i % 10 == 0:
                memory_manager.update_context(
                    feature_name=f"Feature {i+1}",
                    feature_id=f"{i+1:03d}",
                    action="feature_created",
                    details={"batch": f"batch_{i//10}"}
                )

        creation_time = time.time()
        creation_duration = creation_time - start_time

        # Test performance of operations on large project
        validator = Validator(self.project_path)

        # Test search performance
        start_time = time.time()
        search_results = memory_manager.search_memory("Feature")
        search_time = time.time() - start_time

        # Test template listing performance
        start_time = time.time()
        templates = template_manager.list_templates()
        template_time = time.time() - start_time

        # Test memory summary performance
        start_time = time.time()
        summary = memory_manager.get_memory_summary()
        summary_time = time.time() - start_time

        print(f"Large Project Creation ({num_features} features): {creation_duration:.3f}s")
        print(f"Memory Search ({len(search_results)} results): {search_time:.3f}s")
        print(f"Template Listing ({len(templates)} templates): {template_time:.3f}s")
        print(f"Memory Summary Generation: {summary_time:.3f}s")

        # Performance assertions
        assert creation_duration < 10.0, f"Large project creation took {creation_duration:.2f}s, should be < 10.0s"
        assert search_time < 1.0, f"Large project search took {search_time:.3f}s, should be < 1.0s"
        assert template_time < 0.5, f"Template listing took {template_time:.3f}s, should be < 0.5s"
        assert summary_time < 0.5, f"Memory summary took {summary_time:.3f}s, should be < 0.5s"

    def test_memory_cleanup_performance(self):
        """Test memory cleanup performance with many entries"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("perf-cleanup", here=True)

        memory_manager = MemoryManager(self.project_path)

        # Add many old entries
        num_entries = 1000
        old_timestamp = (datetime.now() - timedelta(days=100)).isoformat()

        for i in range(num_entries):
            old_entry = {
                "timestamp": old_timestamp,
                "action": f"old_action_{i}",
                "details": {"old": True, "index": i},
                "impact": "low",
                "category": "cleanup_test"
            }
            memory_manager.memory_index["context_entries"].append(old_entry)

        # Add some recent entries
        for i in range(100):
            memory_manager.update_context(
                action=f"recent_action_{i}",
                details={"recent": True, "index": i},
                impact="medium",
                category="cleanup_test"
            )

        # Measure cleanup performance
        start_time = time.time()
        removed_count = memory_manager.cleanup_old_entries(days=90)
        end_time = time.time()

        cleanup_time = end_time - start_time
        assert removed_count == num_entries, f"Should remove {num_entries} old entries, removed {removed_count}"
        assert cleanup_time < 2.0, f"Cleanup took {cleanup_time:.2f}s, should be < 2.0s"

        print(f"Memory Cleanup ({removed_count} entries): {cleanup_time:.3f}s")

    def test_concurrent_operations_performance(self):
        """Test performance with concurrent operations"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("perf-concurrent", here=True)

        template_manager = TemplateManager(self.project_path)
        memory_manager = MemoryManager(self.project_path)

        # Test concurrent memory updates
        import threading
        import queue

        num_threads = 10
        operations_per_thread = 50
        results_queue = queue.Queue()

        def memory_worker(worker_id):
            """Worker function for concurrent memory operations"""
            try:
                start_time = time.time()
                for i in range(operations_per_thread):
                    memory_manager.update_context(
                        action=f"worker_{worker_id}_action_{i}",
                        details={"worker": worker_id, "operation": i},
                        impact="low",
                        category="concurrent_test"
                    )
                end_time = time.time()
                results_queue.put(("success", worker_id, end_time - start_time))
            except Exception as e:
                results_queue.put(("error", worker_id, str(e)))

        # Start concurrent operations
        start_time = time.time()
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=memory_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        end_time = time.time()
        total_time = end_time - start_time

        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        successful_results = [r for r in results if r[0] == "success"]
        assert len(successful_results) == num_threads, f"All threads should succeed, got {len(successful_results)}/{num_threads}"

        print(f"Concurrent Operations ({num_threads} threads, {num_threads * operations_per_thread} ops): {total_time:.3f}s")

        # Performance assertion - should complete in reasonable time
        assert total_time < 10.0, f"Concurrent operations took {total_time:.2f}s, should be < 10.0s"

    def test_memory_export_performance(self):
        """Test memory export performance with large dataset"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("perf-export", here=True)

        memory_manager = MemoryManager(self.project_path)

        # Add substantial amount of data
        num_entries = 500
        for i in range(num_entries):
            memory_manager.update_context(
                feature_name=f"Export Feature {i}",
                feature_id=f"{i:03d}",
                action=f"export_action_{i}",
                details={
                    "description": f"Description for feature {i}",
                    "tags": [f"tag_{j}" for j in range(5)],
                    "metadata": {"key": f"value_{i}"} for key in range(3)
                },
                impact="medium",
                category="export_test"
            )

        # Add decisions
        from specpulse.core.memory_manager import DecisionRecord
        for i in range(50):
            decision = DecisionRecord(
                id=f"{i:03d}",
                title=f"Decision {i}",
                status="accepted",
                date="2024-01-01",
                author="Test Author",
                rationale=f"Rationale for decision {i}",
                alternatives_considered=[f"Alternative {i}-{j}" for j in range(3)],
                consequences=[f"Consequence {i}-{j}" for j in range(2)],
                related_decisions=[],
                tags=[f"tag_{i}_{j}" for j in range(3)]
            )
            memory_manager.add_decision_record(decision)

        # Test JSON export performance
        start_time = time.time()
        json_export = memory_manager.export_memory("json")
        json_time = time.time() - start_time

        # Test YAML export performance
        start_time = time.time()
        yaml_export = memory_manager.export_memory("yaml")
        yaml_time = time.time() - start_time

        print(f"JSON Export ({len(json_export)} chars): {json_time:.3f}s")
        print(f"YAML Export ({len(yaml_export)} chars): {yaml_time:.3f}s")

        # Performance assertions
        assert json_time < 1.0, f"JSON export took {json_time:.3f}s, should be < 1.0s"
        assert yaml_time < 1.5, f"YAML export took {yaml_time:.3f}s, should be < 1.5s"
        assert len(json_export) > 10000, "JSON export should contain substantial data"
        assert len(yaml_export) > 5000, "YAML export should contain substantial data"


if __name__ == "__main__":
    # Run performance tests individually for measurement
    test_perf = TestPerformance()

    print("=== SpecPulse Performance Tests ===")
    print()

    test_perf.setup_method()
    test_perf.test_initialization_performance()
    test_perf.teardown_method()

    test_perf.setup_method()
    test_perf.test_project_initialization_performance()
    test_perf.teardown_method()

    test_perf.setup_method()
    test_perf.test_template_validation_performance()
    test_perf.teardown_method()

    test_perf.setup_method()
    test_perf.test_memory_operations_performance()
    test_perf.teardown_method()

    test_perf.setup_method()
    test_perf.test_validation_system_performance()
    test_perf.teardown_method()

    test_perf.setup_method()
    test_perf.test_large_project_simulation_performance()
    test_perf.teardown_method()

    print("\n=== Performance Tests Complete ===")