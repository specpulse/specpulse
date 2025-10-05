"""
Tests for Memory Manager module
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil
import json
from datetime import datetime, timedelta

from specpulse.core.memory_manager import (
    MemoryManager, DecisionRecord, ContextEntry, MemoryStats
)


class TestMemoryManager:
    """Test MemoryManager functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

        # Create basic directory structure
        (self.project_path / "memory").mkdir(exist_ok=True)

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_memory_manager_initialization(self):
        """Test MemoryManager initialization"""
        manager = MemoryManager(self.project_path)
        assert manager.project_root == self.project_path
        assert manager.memory_dir.exists()
        assert manager.context_file.exists()
        assert manager.decisions_file.exists()
        assert manager.memory_index.exists()
        assert isinstance(manager.memory_index, dict)

    def test_initialize_memory_system(self):
        """Test memory system initialization creates required files"""
        # Remove existing files
        manager = MemoryManager(self.project_path)
        (manager.context_file).unlink()
        (manager.decisions_file).unlink()

        # Re-initialize
        manager._initialize_memory_system()

        assert manager.context_file.exists()
        assert manager.decisions_file.exists()
        assert "Project Context" in manager.context_file.read_text()
        assert "Architecture Decision Records" in manager.decisions_file.read_text()

    def test_update_context_basic(self):
        """Test basic context update"""
        manager = MemoryManager(self.project_path)

        success = manager.update_context(
            feature_name="Test Feature",
            feature_id="001",
            action="feature_created",
            details={"description": "Test feature description"},
            impact="medium",
            category="spec"
        )

        assert success
        assert len(manager.memory_index["context_entries"]) == 1

        entry = manager.memory_index["context_entries"][0]
        assert entry["feature_name"] == "Test Feature"
        assert entry["feature_id"] == "001"
        assert entry["action"] == "feature_created"

    def test_update_context_without_feature(self):
        """Test context update without feature information"""
        manager = MemoryManager(self.project_path)

        success = manager.update_context(
            action="general_update",
            details={"message": "General update"},
            impact="low"
        )

        assert success
        entry = manager.memory_index["context_entries"][0]
        assert entry["action"] == "general_update"
        assert entry["feature_name"] is None

    def test_update_feature_tracking(self):
        """Test feature tracking updates"""
        manager = MemoryManager(self.project_path)

        # Update context with feature
        manager.update_context(
            feature_name="Test Feature",
            feature_id="001",
            action="feature_created"
        )

        # Check feature tracking
        features = manager.memory_index["features"]
        assert "001" in features
        assert features["001"]["name"] == "Test Feature"
        assert features["001"]["status"] == "active"

        # Update with completion
        manager.update_context(
            feature_name="Test Feature",
            feature_id="001",
            action="feature_completed"
        )

        # Check status updated
        assert features["001"]["status"] == "completed"

    def test_add_decision_record(self):
        """Test adding decision record"""
        manager = MemoryManager(self.project_path)

        decision = DecisionRecord(
            id="001",
            title="Choose Technology Stack",
            status="accepted",
            date="2024-01-01",
            author="Team Lead",
            rationale="Chosen for scalability and team expertise",
            alternatives_considered=["Ruby on Rails", "Django"],
            consequences=["Learning curve", "Performance benefits"],
            related_decisions=[],
            tags=["technology", "architecture"]
        )

        success = manager.add_decision_record(decision)
        assert success

        # Check decision recorded
        decisions = manager.memory_index["decisions"]
        assert "001" in decisions
        assert decisions["001"]["title"] == "Choose Technology Stack"

    def test_add_decision_record_validation(self):
        """Test decision record validation"""
        manager = MemoryManager(self.project_path)

        # Invalid decision (missing ID)
        invalid_decision = DecisionRecord(
            id="",  # Empty ID
            title="Test Decision",
            status="proposed",
            date="2024-01-01",
            author="Test Author",
            rationale="Test rationale",
            alternatives_considered=[],
            consequences=[],
            related_decisions=[],
            tags=[]
        )

        success = manager.add_decision_record(invalid_decision)
        assert not success

    def test_search_memory_by_query(self):
        """Test memory search by query"""
        manager = MemoryManager(self.project_path)

        # Add some context entries
        manager.update_context(
            feature_name="Authentication System",
            action="feature_created",
            details={"type": "security"}
        )
        manager.update_context(
            feature_name="User Profile",
            action="feature_created",
            details={"type": "user_management"}
        )

        # Search for "authentication"
        results = manager.search_memory("authentication")
        assert len(results) == 1
        assert results[0]["type"] == "context"
        assert "Authentication System" in str(results[0]["data"])

    def test_search_memory_by_category(self):
        """Test memory search by category"""
        manager = MemoryManager(self.project_path)

        # Add entries with different categories
        manager.update_context(
            action="feature_created",
            category="spec"
        )
        manager.update_context(
            action="feature_created",
            category="infrastructure"
        )

        # Search by category
        results = manager.search_memory("", category="spec")
        assert len(results) == 1
        assert results[0]["data"]["category"] == "spec"

    def test_search_memory_by_date_range(self):
        """Test memory search by date range"""
        manager = MemoryManager(self.project_path)

        # Add entry
        manager.update_context(
            action="test_action",
            details={"test": True}
        )

        # Search in last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        results = manager.search_memory("", date_range=(start_date.isoformat(), end_date.isoformat()))
        assert len(results) == 1

        # Search in future date range (should return none)
        future_start = datetime.now() + timedelta(days=1)
        future_end = datetime.now() + timedelta(days=7)
        results = manager.search_memory("", date_range=(future_start.isoformat(), future_end.isoformat()))
        assert len(results) == 0

    def test_get_memory_summary(self):
        """Test memory summary generation"""
        manager = MemoryManager(self.project_path)

        # Add some data
        manager.update_context(
            feature_name="Test Feature",
            feature_id="001",
            action="feature_created"
        )

        decision = DecisionRecord(
            id="001",
            title="Test Decision",
            status="accepted",
            date="2024-01-01",
            author="Test Author",
            rationale="Test rationale",
            alternatives_considered=[],
            consequences=[],
            related_decisions=[],
            tags=[]
        )
        manager.add_decision_record(decision)

        summary = manager.get_memory_summary()
        assert "statistics" in summary
        assert "recent_activity" in summary
        assert "recent_decisions" in summary
        assert "active_features" in summary

        stats = summary["statistics"]
        assert stats["total_decisions"] == 1
        assert stats["active_features"] == 1

    def test_cleanup_old_entries(self):
        """Test cleanup of old memory entries"""
        manager = MemoryManager(self.project_path)

        # Add old entry (by manipulating timestamp)
        old_entry = ContextEntry(
            timestamp=(datetime.now() - timedelta(days=100)).isoformat(),
            feature_name="Old Feature",
            action="feature_created",
            details={},
            impact="low",
            category="spec"
        )
        manager.memory_index["context_entries"].append(old_entry.__dict__)

        # Add recent entry
        manager.update_context(
            feature_name="New Feature",
            action="feature_created"
        )

        # Cleanup entries older than 90 days
        removed_count = manager.cleanup_old_entries(days=90)
        assert removed_count == 1

        # Check only recent entry remains
        assert len(manager.memory_index["context_entries"]) == 1
        assert manager.memory_index["context_entries"][0]["feature_name"] == "New Feature"

    def test_validate_memory_structure(self):
        """Test memory structure validation"""
        manager = MemoryManager(self.project_path)

        # Valid structure should pass
        issues = manager.validate_memory_structure()
        assert len(issues) == 0

        # Break structure by removing context file
        manager.context_file.unlink()
        issues = manager.validate_memory_structure()
        assert len(issues) > 0
        assert any("Missing required file" in issue for issue in issues)

    def test_export_memory_json(self):
        """Test memory export in JSON format"""
        manager = MemoryManager(self.project_path)

        # Add some data
        manager.update_context(
            feature_name="Test Feature",
            action="feature_created"
        )

        # Export
        export_content = manager.export_memory("json")
        assert "export_timestamp" in export_content
        assert "memory_index" in export_content
        assert "statistics" in export_content

        # Verify it's valid JSON
        data = json.loads(export_content)
        assert data["version"] == "1.0.0"

    def test_export_memory_yaml(self):
        """Test memory export in YAML format"""
        manager = MemoryManager(self.project_path)

        # Add some data
        manager.update_context(
            feature_name="Test Feature",
            action="feature_created"
        )

        # Export
        export_content = manager.export_memory("yaml")
        assert "version: '1.0.0'" in export_content
        assert "export_timestamp:" in export_content

    def test_export_memory_to_file(self):
        """Test memory export to file"""
        manager = MemoryManager(self.project_path)

        # Add some data
        manager.update_context(
            feature_name="Test Feature",
            action="feature_created"
        )

        # Export to file
        output_path = self.project_path / "memory_export.json"
        export_path = manager.export_memory("json", str(output_path))

        assert export_path == str(output_path)
        assert output_path.exists()
        assert len(output_path.read_text()) > 0

    def test_calculate_memory_stats(self):
        """Test memory statistics calculation"""
        manager = MemoryManager(self.project_path)

        # Add some data
        manager.update_context(
            feature_name="Test Feature 1",
            action="feature_created"
        )
        manager.update_context(
            feature_name="Test Feature 2",
            action="feature_created"
        )

        decision = DecisionRecord(
            id="001",
            title="Test Decision",
            status="accepted",
            date="2024-01-01",
            author="Test Author",
            rationale="Test rationale",
            alternatives_considered=[],
            consequences=[],
            related_decisions=[],
            tags=[]
        )
        manager.add_decision_record(decision)

        stats = manager._calculate_memory_stats()
        assert stats.total_context_entries == 2
        assert stats.total_decisions == 1
        assert stats.active_features == 2
        assert isinstance(stats.memory_size_mb, float)
        assert stats.memory_size_mb >= 0

    def test_update_context_file(self):
        """Test context.md file update"""
        manager = MemoryManager(self.project_path)

        entry = ContextEntry(
            timestamp="2024-01-01T12:00:00",
            feature_name="Test Feature",
            action="feature_created",
            details={"description": "Test"},
            impact="medium",
            category="spec"
        )

        manager._update_context_file(entry)

        content = manager.context_file.read_text()
        assert "feature_created" in content
        assert "Test Feature" in content
        assert "2024-01-01" in content

    def test_update_decisions_file(self):
        """Test decisions.md file update"""
        manager = MemoryManager(self.project_path)

        decision = DecisionRecord(
            id="001",
            title="Test Decision",
            status="accepted",
            date="2024-01-01",
            author="Test Author",
            rationale="Test rationale",
            alternatives_considered=["Option A", "Option B"],
            consequences=["Consequence 1"],
            related_decisions=[],
            tags=["test"]
        )

        manager._update_decisions_file(decision)

        content = manager.decisions_file.read_text()
        assert "ADR-001: Test Decision" in content
        assert "Test rationale" in content
        assert "Option A" in content


class TestDecisionRecord:
    """Test DecisionRecord dataclass"""

    def test_decision_record_creation(self):
        """Test creating decision record"""
        record = DecisionRecord(
            id="001",
            title="Test Decision",
            status="accepted",
            date="2024-01-01",
            author="Test Author",
            rationale="Test rationale",
            alternatives_considered=["Option A"],
            consequences=["Consequence 1"],
            related_decisions=[],
            tags=["test"]
        )

        assert record.id == "001"
        assert record.title == "Test Decision"
        assert record.status == "accepted"
        assert len(record.alternatives_considered) == 1


class TestContextEntry:
    """Test ContextEntry dataclass"""

    def test_context_entry_creation(self):
        """Test creating context entry"""
        entry = ContextEntry(
            timestamp="2024-01-01T12:00:00",
            feature_name="Test Feature",
            feature_id="001",
            action="feature_created",
            details={"description": "Test"},
            impact="medium",
            category="spec"
        )

        assert entry.feature_name == "Test Feature"
        assert entry.feature_id == "001"
        assert entry.action == "feature_created"
        assert entry.impact == "medium"


class TestMemoryStats:
    """Test MemoryStats dataclass"""

    def test_memory_stats_creation(self):
        """Test creating memory stats"""
        stats = MemoryStats(
            total_decisions=5,
            active_features=2,
            completed_features=3,
            total_context_entries=10,
            last_updated="2024-01-01T12:00:00",
            memory_size_mb=1.5
        )

        assert stats.total_decisions == 5
        assert stats.active_features == 2
        assert stats.memory_size_mb == 1.5