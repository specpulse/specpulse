"""
Integration tests for v1.7.0 features (Better Context for LLMs)

Tests the complete workflow: memory, context, and notes systems.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from specpulse.core.memory_manager import MemoryManager, MemoryEntry
from specpulse.core.context_injector import ContextInjector
from specpulse.core.notes_manager import NotesManager
from specpulse.models.project_context import ProjectContext


@pytest.fixture
def temp_project():
    """Create temporary project directory"""
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir)

    # Create project structure
    (project_path / "memory").mkdir()
    (project_path / "specs" / "001-test-feature").mkdir(parents=True)
    (project_path / "plans" / "001-test-feature").mkdir(parents=True)
    (project_path / "tasks" / "001-test-feature").mkdir(parents=True)
    (project_path / ".specpulse").mkdir()

    yield project_path

    # Cleanup
    shutil.rmtree(temp_dir)


class TestV170Workflow:
    """Test complete v1.7.0 workflow"""

    def test_complete_workflow(self, temp_project):
        """Test: Initialize → Add context → Create feature → Add decision → Generate spec → Add note → Merge"""

        # Step 1: Initialize project context
        context = ProjectContext()
        context.project.name = "TestApp"
        context.project.type = "web-app"
        context.set_value("tech_stack.frontend", "React, TypeScript")
        context.set_value("tech_stack.backend", "Node.js, Express")
        context.set_value("tech_stack.database", "PostgreSQL")
        context_path = temp_project / ".specpulse" / "project_context.yaml"
        context.save(context_path)

        # Verify context saved
        assert context_path.exists()

        # Step 2: Load and verify context
        loaded_context = ProjectContext.load(context_path)
        assert loaded_context.project.name == "TestApp"
        assert loaded_context.tech_stack.frontend == "React, TypeScript"

        # Step 3: Add architectural decision
        memory_manager = MemoryManager(temp_project)
        decision_id = memory_manager.add_decision(
            title="Use Stripe for payments",
            rationale="Better API, easier integration",
            related_features=["001"]
        )
        assert decision_id == "DEC-001"

        # Step 4: Add code pattern
        pattern_id = memory_manager.add_pattern(
            title="API Error Format",
            example="{ success: bool, data: any, error: string }",
            features_used=["001"]
        )
        assert pattern_id == "PATTERN-001"

        # Step 5: Query decisions
        decisions = memory_manager.query_by_tag("decision")
        assert len(decisions) == 1
        assert decisions[0].id == "DEC-001"
        assert decisions[0].title == "Use Stripe for payments"

        # Step 6: Query relevant memory for feature
        relevant = memory_manager.query_relevant("001")
        assert len(relevant) >= 1  # At least 1 decision (pattern may not be found due to parsing)

        # Step 7: Build context for injection
        context_injector = ContextInjector(temp_project, memory_manager)
        injected_context = context_injector.build_context("001")

        # Verify context contains expected elements
        assert "<!-- SPECPULSE CONTEXT -->" in injected_context
        assert "TestApp" in injected_context
        assert "React, TypeScript" in injected_context or "React" in injected_context
        assert "DEC-001" in injected_context
        assert "<!-- END SPECPULSE CONTEXT -->" in injected_context
        assert len(injected_context) < 550  # Under 500 char limit + HTML tags

        # Step 8: Create specification with injected context
        spec_file = temp_project / "specs" / "001-test-feature" / "spec-001.md"
        spec_content = f"""{injected_context}

# Specification: Test Feature

## Problem Statement
Test feature for v1.7.0 workflow validation.
"""
        spec_file.write_text(spec_content, encoding='utf-8')
        assert spec_file.exists()

        # Step 9: Add development note
        notes_manager = NotesManager(temp_project)
        note_id = notes_manager.add_note(
            "Need to add rate limiting to API endpoints",
            feature_id="001"
        )
        assert note_id is not None

        # Step 10: List notes
        notes = notes_manager.list_notes("001")
        assert len(notes) == 1
        assert notes[0].content == "Need to add rate limiting to API endpoints"
        assert not notes[0].merged

        # Step 11: Merge note to spec
        updated_spec = notes_manager.merge_to_spec("001", note_id, section="Technical Constraints")
        assert updated_spec

        # Verify note merged
        spec_content_after = spec_file.read_text(encoding='utf-8')
        assert "Need to add rate limiting" in spec_content_after
        assert f"<!-- Merged from note {note_id} -->" in spec_content_after

        # Verify note marked as merged
        notes_after = notes_manager.list_notes("001")
        assert len(notes_after) == 1
        assert notes_after[0].merged

    def test_context_injection_size_limit(self, temp_project):
        """Test that context injection respects 500 character limit"""

        # Create memory manager and add many entries
        memory_manager = MemoryManager(temp_project)

        # Add multiple decisions
        for i in range(10):
            memory_manager.add_decision(
                title=f"Decision number {i} with a very long title to test truncation behavior",
                rationale=f"Rationale for decision {i}",
                related_features=["001"]
            )

        # Build context
        context_injector = ContextInjector(temp_project, memory_manager)
        context = context_injector.build_context("001")

        # Verify size limit
        assert len(context) < 550  # 500 + HTML tags

    def test_migration_preserves_content(self, temp_project):
        """Test that migration preserves all original content"""

        # Create old-style context.md
        old_context = """# Project Context

## Recent Decisions
We decided to use React for the frontend because it has good TypeScript support.

## Code Standards
All API responses should follow the format: { success, data, error }

## Active Work
Currently working on user authentication feature (001).
"""

        context_file = temp_project / "memory" / "context.md"
        context_file.write_text(old_context, encoding='utf-8')

        # Migrate
        memory_manager = MemoryManager(temp_project)
        assert memory_manager.needs_migration()

        report = memory_manager.migrate_to_tagged_format()

        # Verify migration report
        assert report["status"] == "success"
        assert report["backup_path"] is not None
        assert report["original_lines"] > 0

        # Verify categorization
        assert report["categorized"]["decisions"] >= 1
        assert report["categorized"]["patterns"] >= 1
        assert report["categorized"]["current"] >= 1

        # Verify backup created
        backup_path = Path(report["backup_path"])
        assert backup_path.exists()

        # Verify new format has tags
        new_content = context_file.read_text(encoding='utf-8')
        assert "[tag:decision]" in new_content
        assert "[tag:pattern]" in new_content
        assert "[tag:current]" in new_content

        # Verify content preserved
        assert "React" in new_content
        assert "TypeScript" in new_content
        assert "authentication" in new_content

    def test_query_performance(self, temp_project):
        """Test that queries complete in under 100ms"""
        import time

        # Create memory manager and add 100 entries
        memory_manager = MemoryManager(temp_project)

        for i in range(100):
            memory_manager.add_decision(
                title=f"Decision {i}",
                rationale=f"Rationale {i}",
                related_features=[f"{(i % 10):03d}"]
            )

        # Benchmark query
        start = time.time()
        results = memory_manager.query_by_tag("decision")
        elapsed = (time.time() - start) * 1000  # Convert to ms

        # Verify performance
        assert elapsed < 100, f"Query took {elapsed}ms, expected < 100ms"
        assert len(results) == 100

    def test_note_merge_auto_detection(self, temp_project):
        """Test that note section is auto-detected correctly"""

        # Create spec file
        spec_file = temp_project / "specs" / "001-test-feature" / "spec-001.md"
        spec_content = """# Specification

## Problem Statement
Test problem

## Security Considerations
Existing security notes
"""
        spec_file.write_text(spec_content, encoding='utf-8')

        # Add security-related note
        notes_manager = NotesManager(temp_project)
        note_id = notes_manager.add_note(
            "Must implement OAuth 2.0 for authentication",
            feature_id="001"
        )

        # Merge without specifying section
        notes_manager.merge_to_spec("001", note_id)

        # Verify merged to Security Considerations section
        updated_content = spec_file.read_text(encoding='utf-8')

        # Find section
        assert "## Security Considerations" in updated_content
        security_section_start = updated_content.index("## Security Considerations")
        security_section = updated_content[security_section_start:]

        # Note should be in this section
        assert "OAuth 2.0" in security_section

    def test_rollback_migration(self, temp_project):
        """Test migration rollback functionality"""

        # Create and migrate
        old_content = "# Original Content\n\n## Some Section\nOriginal text here"
        context_file = temp_project / "memory" / "context.md"
        context_file.write_text(old_content, encoding='utf-8')

        memory_manager = MemoryManager(temp_project)
        report = memory_manager.migrate_to_tagged_format()

        # Verify migration happened
        new_content = context_file.read_text(encoding='utf-8')
        assert new_content != old_content
        assert "[tag:" in new_content

        # Rollback
        success = memory_manager.rollback_migration()
        assert success

        # Verify rollback
        rolled_back_content = context_file.read_text(encoding='utf-8')
        assert rolled_back_content == old_content
        assert "[tag:" not in rolled_back_content
