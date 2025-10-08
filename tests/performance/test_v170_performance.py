"""
Performance benchmarks for v1.7.0 features

Tests performance targets:
- Memory query: < 100ms
- Context injection: < 50ms
- Note creation: < 10ms
"""

import pytest
import time
from pathlib import Path
import tempfile
import shutil
from specpulse.core.memory_manager import MemoryManager
from specpulse.core.context_injector import ContextInjector
from specpulse.core.notes_manager import NotesManager


@pytest.fixture
def bench_project():
    """Create temporary project for benchmarking"""
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir)

    # Create structure
    (project_path / "memory").mkdir()
    (project_path / ".specpulse").mkdir()

    yield project_path

    shutil.rmtree(temp_dir)


class TestV170Performance:
    """Performance benchmarks for v1.7.0"""

    def test_memory_query_performance(self, bench_project):
        """Target: < 100ms for 1000 entries"""

        memory_manager = MemoryManager(bench_project)

        # Add 1000 decisions
        for i in range(1000):
            memory_manager.add_decision(
                title=f"Decision {i}",
                rationale=f"Rationale for decision {i}",
                related_features=[f"{(i % 100):03d}"]
            )

        # Benchmark query
        start = time.perf_counter()
        results = memory_manager.query_by_tag("decision")
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Verify
        assert len(results) == 1000
        assert elapsed_ms < 100, f"Query took {elapsed_ms:.2f}ms (target: <100ms)"

        # Benchmark filtered query
        start = time.perf_counter()
        filtered = memory_manager.query_by_tag("decision", feature="001")
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 100, f"Filtered query took {elapsed_ms:.2f}ms (target: <100ms)"

    def test_context_injection_performance(self, bench_project):
        """Target: < 50ms for context building"""

        memory_manager = MemoryManager(bench_project)

        # Add some entries
        for i in range(10):
            memory_manager.add_decision(f"Decision {i}", f"Rationale {i}", [f"{i:03d}"])
            memory_manager.add_pattern(f"Pattern {i}", f"Example {i}", [f"{i:03d}"])

        # Benchmark context injection
        injector = ContextInjector(bench_project, memory_manager)

        start = time.perf_counter()
        context = injector.build_context("001")
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Verify
        assert len(context) < 550
        assert elapsed_ms < 50, f"Context injection took {elapsed_ms:.2f}ms (target: <50ms)"

    def test_note_creation_performance(self, bench_project):
        """Target: < 10ms for note creation"""

        notes_manager = NotesManager(bench_project)

        # Benchmark note creation
        start = time.perf_counter()
        note_id = notes_manager.add_note("Test note content", feature_id="001")
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Verify
        assert note_id is not None
        assert elapsed_ms < 10, f"Note creation took {elapsed_ms:.2f}ms (target: <10ms)"

    def test_query_recent_performance(self, bench_project):
        """Test performance of recent queries"""

        memory_manager = MemoryManager(bench_project)

        # Add 500 decisions
        for i in range(500):
            memory_manager.add_decision(
                title=f"Decision {i}",
                rationale=f"Rationale {i}"
            )

        # Benchmark recent query
        start = time.perf_counter()
        recent = memory_manager.query_by_tag("decision", recent=3)
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Verify
        assert len(recent) == 3
        assert elapsed_ms < 100, f"Recent query took {elapsed_ms:.2f}ms (target: <100ms)"

    def test_migration_performance(self, bench_project):
        """Test migration completes in reasonable time (<5 seconds)"""

        # Create large context file
        context_file = bench_project / "memory" / "context.md"
        large_content = "# Project Context\n\n"

        for i in range(100):
            large_content += f"""
## Decision {i}
We decided to use technology {i} because of reason {i}.
This has implications for the project architecture.
"""

        context_file.write_text(large_content, encoding='utf-8')

        # Benchmark migration
        memory_manager = MemoryManager(bench_project)

        start = time.perf_counter()
        report = memory_manager.migrate_to_tagged_format()
        elapsed = time.perf_counter() - start

        # Verify
        assert report["status"] == "success"
        assert elapsed < 5.0, f"Migration took {elapsed:.2f}s (target: <5s)"

"""
Performance Summary:

Run benchmarks with:
    pytest tests/benchmarks/test_v170_performance.py -v

Expected results:
    - Memory query (1000 entries): < 100ms
    - Context injection: < 50ms
    - Note creation: < 10ms
    - Migration (100 sections): < 5 seconds
"""
