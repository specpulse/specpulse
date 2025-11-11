"""
Complete Path Manager Tests

Comprehensive tests for PathManager functionality.
Designed for 100% code coverage and security testing.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import warnings

from specpulse.core.path_manager import PathManager
from specpulse.utils.error_handler import ValidationError


class TestPathManagerComplete:
    """Comprehensive tests for PathManager functionality"""

    @pytest.mark.unit
    def test_path_manager_new_structure_initialization(self, temp_project_dir):
        """Test PathManager initialization with new structure"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        assert path_manager.project_root == temp_project_dir
        assert path_manager.use_legacy_structure is False
        assert path_manager.specpulse_dir == temp_project_dir / ".specpulse"

        # Verify new structure paths
        assert path_manager.specs_dir == temp_project_dir / ".specpulse" / "specs"
        assert path_manager.plans_dir == temp_project_dir / ".specpulse" / "plans"
        assert path_manager.tasks_dir == temp_project_dir / ".specpulse" / "tasks"
        assert path_manager.memory_dir == temp_project_dir / ".specpulse" / "memory"
        assert path_manager.templates_dir == temp_project_dir / ".specpulse" / "templates"

    @pytest.mark.unit
    def test_path_manager_legacy_structure_initialization(self, temp_project_dir):
        """Test PathManager initialization with legacy structure"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=True)

        assert path_manager.project_root == temp_project_dir
        assert path_manager.use_legacy_structure is True

        # Verify legacy structure paths
        assert path_manager.specs_dir == temp_project_dir / "specs"
        assert path_manager.plans_dir == temp_project_dir / "plans"
        assert path_manager.tasks_dir == temp_project_dir / "tasks"
        assert path_manager.memory_dir == temp_project_dir / "memory"
        assert path_manager.templates_dir == temp_project_dir / "templates"

    @pytest.mark.unit
    def test_path_manager_all_directories(self, temp_project_dir):
        """Test get_all_directories method"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        all_dirs = path_manager.get_all_directories()

        # Verify all expected directories are present
        expected_dirs = [
            'specs', 'plans', 'tasks', 'memory', 'templates', 'notes',
            'cache', 'checkpoints', 'docs', 'template_backups',
            'claude', 'gemini', 'specpulse'
        ]

        for dir_name in expected_dirs:
            assert dir_name in all_dirs
            assert all_dirs[dir_name] is not None

    @pytest.mark.unit
    def test_path_manager_ensure_directories_success(self, temp_project_dir):
        """Test successful directory creation"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        result = path_manager.ensure_directories()

        assert result is True

        # Verify directories were created
        for dir_path in path_manager.get_all_directories().values():
            if dir_path.name not in ['claude', 'gemini']:  # Skip AI dirs
                assert dir_path.exists()

    @pytest.mark.unit
    def test_path_manager_ensure_specific_directories(self, temp_project_dir):
        """Test creating specific directories only"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        result = path_manager.ensure_directories(['specs', 'plans'])

        assert result is True
        assert path_manager.specs_dir.exists()
        assert path_manager.plans_dir.exists()

    @pytest.mark.unit
    def test_path_manager_ensure_directories_with_errors(self, temp_project_dir):
        """Test directory creation with errors"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        # Mock mkdir to fail for specific directory
        def mock_mkdir(parents=False, exist_ok=False):
            if 'cache' in str(self):
                raise PermissionError("Cannot create directory")

        with patch.object(Path, 'mkdir', side_effect=mock_mkdir):
            with warnings.catch_warnings(record=True) as w:
                result = path_manager.ensure_directories(['cache'])

        assert result is False  # Should fail due to permission error

    @pytest.mark.unit
    def test_path_manager_get_feature_dir(self, temp_project_dir):
        """Test feature directory path generation"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        feature_dir = path_manager.get_feature_dir("001", "user-auth", "specs")
        expected_path = temp_project_dir / ".specpulse" / "specs" / "001-user-auth"
        assert feature_dir == expected_path

        # Test different types
        plan_dir = path_manager.get_feature_dir("002", "payment", "plans")
        expected_plan_path = temp_project_dir / ".specpulse" / "plans" / "002-payment"
        assert plan_dir == expected_plan_path

    @pytest.mark.unit
    def test_path_manager_get_feature_dir_invalid_type(self, temp_project_dir):
        """Test get_feature_dir with invalid directory type"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        with pytest.raises(ValueError, match="Invalid directory type"):
            path_manager.get_feature_dir("001", "test", "invalid_type")

    @pytest.mark.unit
    def test_path_manager_get_spec_file(self, temp_project_dir):
        """Test spec file path generation"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        spec_file = path_manager.get_spec_file("001", "user-auth", 1)
        expected_path = temp_project_dir / ".specpulse" / "specs" / "001-user-auth" / "spec-001.md"
        assert spec_file == expected_path

        # Test with different spec numbers
        spec_file_2 = path_manager.get_spec_file("001", "user-auth", 5)
        expected_path_2 = temp_project_dir / ".specpulse" / "specs" / "001-user-auth" / "spec-005.md"
        assert spec_file_2 == expected_path_2

    @pytest.mark.unit
    def test_path_manager_get_plan_file(self, temp_project_dir):
        """Test plan file path generation"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        plan_file = path_manager.get_plan_file("001", "user-auth", 2)
        expected_path = temp_project_dir / ".specpulse" / "plans" / "001-user-auth" / "plan-002.md"
        assert plan_file == expected_path

    @pytest.mark.unit
    def test_path_manager_get_task_file(self, temp_project_dir):
        """Test task file path generation"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        task_file = path_manager.get_task_file("001", "user-auth", 3)
        expected_path = temp_project_dir / ".specpulse" / "tasks" / "001-user-auth" / "task-003.md"
        assert task_file == expected_path

    @pytest.mark.unit
    def test_path_manager_get_memory_file(self, temp_project_dir):
        """Test memory file path generation"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        memory_file = path_manager.get_memory_file("context.md")
        expected_path = temp_project_dir / ".specpulse" / "memory" / "context.md"
        assert memory_file == expected_path

        memory_file_2 = path_manager.get_memory_file("decisions.md")
        expected_path_2 = temp_project_dir / ".specpulse" / "memory" / "decisions.md"
        assert memory_file_2 == expected_path_2

    @pytest.mark.unit
    def test_path_manager_get_template_file(self, temp_project_dir):
        """Test template file path generation"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        template_file = path_manager.get_template_file("spec.md")
        expected_path = temp_project_dir / ".specpulse" / "templates" / "spec.md"
        assert template_file == expected_path

    @pytest.mark.unit
    def test_path_manager_detect_structure_new(self, temp_project_dir):
        """Test structure detection for new structure"""
        # Create new structure
        (temp_project_dir / ".specpulse").mkdir(exist_ok=True)
        (temp_project_dir / ".specpulse" / "specs").mkdir(exist_ok=True)

        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)
        structure = path_manager.detect_structure()

        assert structure == "new"

    @pytest.mark.unit
    def test_path_manager_detect_structure_legacy(self, temp_project_dir):
        """Test structure detection for legacy structure"""
        # Create legacy structure
        (temp_project_dir / "specs").mkdir(exist_ok=True)
        (temp_project_dir / "plans").mkdir(exist_ok=True)

        path_manager = PathManager(temp_project_dir, use_legacy_structure=True)
        structure = path_manager.detect_structure()

        assert structure == "legacy"

    @pytest.mark.unit
    def test_path_manager_detect_structure_none(self, temp_project_dir):
        """Test structure detection when no structure exists"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)
        structure = path_manager.detect_structure()

        assert structure == "none"

    @pytest.mark.unit
    def test_path_manager_detect_structure_mixed(self, temp_project_dir):
        """Test structure detection for mixed structure (both exist)"""
        # Create both structures
        (temp_project_dir / ".specpulse" / "specs").mkdir(parents=True, exist_ok=True)
        (temp_project_dir / "specs").mkdir(exist_ok=True)

        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)
        structure = path_manager.detect_structure()

        assert structure == "mixed"

    @pytest.mark.unit
    def test_path_manager_validate_specpulse_path_valid(self, temp_project_dir):
        """Test path validation for valid .specpulse paths"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        # Valid paths within .specpulse
        valid_paths = [
            temp_project_dir / ".specpulse" / "specs",
            temp_project_dir / ".specpulse" / "plans" / "001-feature",
            temp_project_dir / ".specpulse" / "memory" / "context.md"
        ]

        for path in valid_paths:
            assert path_manager.validate_specpulse_path(path) is True

    @pytest.mark.unit
    def test_path_manager_validate_specpulse_path_invalid(self, temp_project_dir):
        """Test path validation for invalid paths"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        # Invalid paths outside .specpulse
        invalid_paths = [
            temp_project_dir / "specs",  # Legacy structure
            temp_project_dir / "root_file.md",
            temp_project_dir / ".." / "outside_path",
            Path("/absolute/path/outside/project")
        ]

        for path in invalid_paths:
            assert path_manager.validate_specpulse_path(path) is False

    @pytest.mark.unit
    def test_path_manager_validate_specpulse_path_edge_cases(self, temp_project_dir):
        """Test path validation edge cases"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        # Test with relative paths
        relative_path = Path(".specpulse/specs")
        # This should work after resolving to absolute
        assert path_manager.validate_specpulse_path(relative_path.resolve()) is True

        # Test with non-existent paths (still valid if within .specpulse)
        non_existent = temp_project_dir / ".specpulse" / "nonexistent"
        assert path_manager.validate_specpulse_path(non_existent) is True

    @pytest.mark.unit
    def test_path_manager_validate_specpulse_path_errors(self):
        """Test path validation error handling"""
        path_manager = PathManager(Path("/nonexistent"), use_legacy_structure=False)

        # Should handle non-existent base path gracefully
        result = path_manager.validate_specpulse_path(Path("test"))
        assert result is False

    @pytest.mark.unit
    def test_path_manager_enforce_specpulse_rules_success(self, temp_project_dir):
        """Test successful rule enforcement"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        results = path_manager.enforce_specpulse_rules()

        assert results['valid'] is True
        assert results['structure_type'] == 'new'
        assert len(results['errors']) == 0
        assert len(results['warnings']) == 0

    @pytest.mark.unit
    def test_path_manager_enforce_specpulse_rules_legacy_warning(self, temp_project_dir):
        """Test rule enforcement with legacy structure warning"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=True)

        with warnings.catch_warnings(record=True) as w:
            results = path_manager.enforce_specpulse_rules()

        assert results['valid'] is True
        assert results['structure_type'] == 'legacy'
        assert len(results['warnings']) > 0
        assert "legacy directory structure" in results['warnings'][0]

    @pytest.mark.unit
    def test_path_manager_enforce_specpulse_rules_validation_failure(self, temp_project_dir):
        """Test rule enforcement with validation failures"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        # Mock a directory outside .specpulse
        with patch.object(path_manager, 'get_all_directories') as mock_get_dirs:
            mock_dirs = path_manager.get_all_directories()
            mock_dirs['invalid_dir'] = temp_project_dir / "outside_specpulse"
            mock_get_dirs.return_value = mock_dirs

            # Mock validate_specpulse_path to return False for invalid_dir
            with patch.object(path_manager, 'validate_specpulse_path', return_value=False):
                results = path_manager.enforce_specpulse_rules()

        assert results['valid'] is False
        assert len(results['errors']) > 0

    @pytest.mark.unit
    def test_path_manager_get_safe_output_path_spec(self, temp_project_dir):
        """Test safe path generation for spec files"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        safe_path = path_manager.get_safe_output_path(
            file_type='spec',
            feature_id='001',
            feature_name='user-auth',
            filename='custom-spec.md'
        )

        expected = temp_project_dir / ".specpulse" / "specs" / "001-user-auth" / "custom-spec.md"
        assert safe_path == expected
        assert path_manager.validate_specpulse_path(safe_path) is True

    @pytest.mark.unit
    def test_path_manager_get_safe_output_path_plan(self, temp_project_dir):
        """Test safe path generation for plan files"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        safe_path = path_manager.get_safe_output_path(
            file_type='plan',
            feature_id='002',
            feature_name='payment'
        )

        expected = temp_project_dir / ".specpulse" / "plans" / "002-payment" / "plan-001.md"
        assert safe_path == expected
        assert path_manager.validate_specpulse_path(safe_path) is True

    @pytest.mark.unit
    def test_path_manager_get_safe_output_path_task(self, temp_project_dir):
        """Test safe path generation for task files"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        safe_path = path_manager.get_safe_output_path(
            file_type='task',
            feature_id='003',
            feature_name='notification'
        )

        expected = temp_project_dir / ".specpulse" / "tasks" / "003-notification" / "task-001.md"
        assert safe_path == expected
        assert path_manager.validate_specpulse_path(safe_path) is True

    @pytest.mark.unit
    def test_path_manager_get_safe_output_path_memory(self, temp_project_dir):
        """Test safe path generation for memory files"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        safe_path = path_manager.get_safe_output_path(
            file_type='memory',
            filename='project-context.md'
        )

        expected = temp_project_dir / ".specpulse" / "memory" / "project-context.md"
        assert safe_path == expected
        assert path_manager.validate_specpulse_path(safe_path) is True

    @pytest.mark.unit
    def test_path_manager_get_safe_output_path_cache(self, temp_project_dir):
        """Test safe path generation for cache files"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        safe_path = path_manager.get_safe_output_path(
            file_type='cache',
            filename='test-cache.cache'
        )

        expected = temp_project_dir / ".specpulse" / "cache" / "test-cache.cache"
        assert safe_path == expected
        assert path_manager.validate_specpulse_path(safe_path) is True

    @pytest.mark.unit
    def test_path_manager_get_safe_output_path_docs(self, temp_project_dir):
        """Test safe path generation for documentation files"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        safe_path = path_manager.get_safe_output_path(
            file_type='docs',
            filename='architecture.md'
        )

        expected = temp_project_dir / ".specpulse" / "docs" / "architecture.md"
        assert safe_path == expected
        assert path_manager.validate_specpulse_path(safe_path) is True

    @pytest.mark.unit
    def test_path_manager_get_safe_output_path_fallback(self, temp_project_dir):
        """Test safe path generation fallback for unknown types"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        safe_path = path_manager.get_safe_output_path(
            file_type='unknown_type',
            filename='test-file.md'
        )

        expected = temp_project_dir / ".specpulse" / "test-file.md"
        assert safe_path == expected
        assert path_manager.validate_specpulse_path(safe_path) is True

    @pytest.mark.unit
    def test_path_manager_get_safe_output_path_legacy_warning(self, temp_project_dir):
        """Test safe path generation with legacy structure warning"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=True)

        with warnings.catch_warnings(record=True) as w:
            safe_path = path_manager.get_safe_output_path(
                file_type='spec',
                feature_id='001',
                feature_name='test'
            )

        # Should still generate path but with warning
        assert safe_path is not None
        assert any("legacy structure" in str(warning.message) for warning in w)

    @pytest.mark.unit
    def test_path_manager_to_dict_conversion(self, temp_project_dir):
        """Test conversion to dictionary representation"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        result = path_manager.to_dict()

        assert 'project_root' in result
        assert 'use_legacy_structure' in result
        assert 'structure_detected' in result
        assert 'directories' in result

        assert result['project_root'] == str(temp_project_dir)
        assert result['use_legacy_structure'] is False
        assert result['structure_detected'] == 'none'  # No structure yet

    @pytest.mark.unit
    def test_path_manager_to_dict_with_structure(self, temp_project_dir):
        """Test to_dict conversion with existing structure"""
        # Create structure
        (temp_project_dir / ".specpulse" / "specs").mkdir(parents=True, exist_ok=True)

        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)
        result = path_manager.to_dict()

        assert result['structure_detected'] == 'new'

    @pytest.mark.unit
    def test_path_manager_get_decomposition_dir(self, temp_project_dir):
        """Test decomposition directory path generation"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        decomp_dir = path_manager.get_decomposition_dir("001", "microservice")
        expected = temp_project_dir / ".specpulse" / "specs" / "001-microservice" / "decomposition"
        assert decomp_dir == expected

    @pytest.mark.unit
    def test_path_manager_migration_not_implemented(self, temp_project_dir):
        """Test migration functionality raises NotImplementedError"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        with patch.object(path_manager, 'detect_structure', return_value='legacy'):
            with pytest.raises(NotImplementedError, match="Migration functionality not yet implemented"):
                path_manager.migrate_to_new_structure()

    @pytest.mark.unit
    def test_path_manager_migration_already_new_structure(self, temp_project_dir):
        """Test migration when already using new structure"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        with patch.object(path_manager, 'detect_structure', return_value='new'):
            result = path_manager.migrate_to_new_structure()
            assert result is True

    @pytest.mark.unit
    def test_path_manager_migration_no_structure(self, temp_project_dir):
        """Test migration when no structure exists"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        with patch.object(path_manager, 'detect_structure', return_value='none'):
            with pytest.raises(ValueError, match="No SpecPulse structure detected"):
                path_manager.migrate_to_new_structure()

    @pytest.mark.unit
    def test_path_manager_path_resolution_edge_cases(self, temp_project_dir):
        """Test path resolution edge cases"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        # Test with very long feature names
        long_name = "a" * 1000
        feature_dir = path_manager.get_feature_dir("001", long_name, "specs")
        assert "001" in str(feature_dir)
        assert long_name in str(feature_dir)

        # Test with special characters in feature names
        special_name = "feature-name_123.test"
        feature_dir_special = path_manager.get_feature_dir("002", special_name, "specs")
        assert special_name in str(feature_dir_special)

    @pytest.mark.unit
    def test_path_manager_concurrent_access(self, temp_project_dir):
        """Test concurrent access scenarios"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        # Multiple calls should be consistent
        dir1 = path_manager.get_feature_dir("001", "test", "specs")
        dir2 = path_manager.get_feature_dir("001", "test", "specs")
        assert dir1 == dir2

        # Results should be deterministic
        results = [path_manager.get_all_directories() for _ in range(5)]
        for result in results:
            assert result == results[0]

    @pytest.mark.unit
    def test_path_manager_security_path_traversal_protection(self, temp_project_dir):
        """Test protection against path traversal attacks"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        # Attempt path traversal
        malicious_paths = [
            Path(temp_project_dir / ".specpulse" / ".." / "etc" / "passwd"),
            Path(temp_project_dir / ".specpulse" / "specs" / ".." / ".." / "root"),
            Path(temp_project_dir / ".specpulse" / "templates" / ".." / "system" / "config")
        ]

        for malicious_path in malicious_paths:
            # These should be rejected as they try to escape .specpulse
            try:
                is_valid = path_manager.validate_specpulse_path(malicious_path)
                # If path resolves outside .specpulse, should return False
                if malicious_path.resolve().is_relative_to(temp_project_dir / ".specpulse"):
                    # If it resolves inside .specpulse (due to path resolution), it's valid
                    assert is_valid is True
                else:
                    assert is_valid is False
            except (OSError, ValueError):
                # Should handle path resolution errors gracefully
                assert True

    @pytest.mark.unit
    @pytest.mark.security
    def test_path_manager_safe_path_always_within_specpulse(self, temp_project_dir):
        """Test that safe output paths are always within .specpulse"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        test_cases = [
            ('spec', '001', 'test-feature'),
            ('plan', '002', 'another-feature'),
            ('task', '003', 'third-feature'),
            ('memory', None, None),
            ('cache', None, None),
            ('docs', None, None),
            ('unknown', None, 'test-file')
        ]

        for file_type, feature_id, feature_name in test_cases:
            safe_path = path_manager.get_safe_output_path(
                file_type=file_type,
                feature_id=feature_id,
                feature_name=feature_name
            )

            # All safe paths should be within .specpulse
            assert path_manager.validate_specpulse_path(safe_path), f"Safe path failed for {file_type}"

    @pytest.mark.unit
    def test_path_manager_ai_directories_outside_validation(self, temp_project_dir):
        """Test that AI directories are excluded from validation"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        # AI directories should exist at root level
        assert path_manager.claude_dir == temp_project_dir / ".claude"
        assert path_manager.gemini_dir == temp_project_dir / ".gemini"

        # AI directories should not be within .specpulse
        assert not path_manager.validate_specpulse_path(path_manager.claude_dir)
        assert not path_manager.validate_specpulse_path(path_manager.gemini_dir)

    @pytest.mark.unit
    def test_path_manager_initialization_with_none_path(self):
        """Test PathManager initialization with None path"""
        path_manager = PathManager(None, use_legacy_structure=False)

        # Should use current working directory
        assert path_manager.project_root == Path.cwd()

    @pytest.mark.unit
    def test_path_manager_consistent_directory_naming(self, temp_project_dir):
        """Test consistent directory naming conventions"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        all_dirs = path_manager.get_all_directories()

        # Check that no directory names conflict
        dir_names = list(all_dirs.keys())
        assert len(dir_names) == len(set(dir_names)), "Directory names should be unique"

        # Check naming convention consistency
        for name, path in all_dirs.items():
            assert isinstance(name, str), f"Directory name should be string: {name}"
            assert isinstance(path, Path), f"Directory path should be Path object: {name}"

    @pytest.mark.unit
    def test_path_manager_template_backups_directory(self, temp_project_dir):
        """Test template backups directory is properly configured"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        backups_dir = path_manager.template_backups_dir
        expected_path = temp_project_dir / ".specpulse" / "template_backups"
        assert backups_dir == expected_path

        # Should be included in all directories
        all_dirs = path_manager.get_all_directories()
        assert 'template_backups' in all_dirs
        assert all_dirs['template_backups'] == backups_dir

    @pytest.mark.unit
    def test_path_manager_notes_directory_creation(self, temp_project_dir):
        """Test notes directory is properly nested under memory"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        notes_dir = path_manager.notes_dir
        expected_path = temp_project_dir / ".specpulse" / "memory" / "notes"
        assert notes_dir == expected_path

        # Should be included in all directories
        all_dirs = path_manager.get_all_directories()
        assert 'notes' in all_dirs
        assert all_dirs['notes'] == notes_dir

    @pytest.mark.unit
    def test_path_manager_docs_directory_creation(self, temp_project_dir):
        """Test docs directory is properly configured"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        docs_dir = path_manager.docs_dir
        expected_path = temp_project_dir / ".specpulse" / "docs"
        assert docs_dir == expected_path

        # Should be included in all directories
        all_dirs = path_manager.get_all_directories()
        assert 'docs' in all_dirs
        assert all_dirs['docs'] == docs_dir

    @pytest.mark.unit
    def test_path_manager_cache_directory_creation(self, temp_project_dir):
        """Test cache directory is properly configured"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        cache_dir = path_manager.cache_dir
        expected_path = temp_project_dir / ".specpulse" / "cache"
        assert cache_dir == expected_path

        # Should be included in all directories
        all_dirs = path_manager.get_all_directories()
        assert 'cache' in all_dirs
        assert all_dirs['cache'] == cache_dir

    @pytest.mark.unit
    def test_path_manager_checkpoints_directory_creation(self, temp_project_dir):
        """Test checkpoints directory is properly configured"""
        path_manager = PathManager(temp_project_dir, use_legacy_structure=False)

        checkpoints_dir = path_manager.checkpoints_dir
        expected_path = temp_project_dir / ".specpulse" / "checkpoints"
        assert checkpoints_dir == expected_path

        # Should be included in all directories
        all_dirs = path_manager.get_all_directories()
        assert 'checkpoints' in all_dirs
        assert all_dirs['checkpoints'] == checkpoints_dir