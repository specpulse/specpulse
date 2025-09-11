"""
Comprehensive test suite for SpecPulse Validator module.
Tests all validation functionality with proper mocking and edge cases.
"""

import pytest
import unittest
from unittest.mock import patch, mock_open, MagicMock, call
from pathlib import Path
import tempfile
import shutil
import yaml
import os
import re

from specpulse.core.validator import Validator


class TestValidator(unittest.TestCase):
    """Comprehensive tests for Validator class"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        self.validator = Validator()
        
        # Create basic project structure
        self.create_basic_project_structure()
        
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def create_basic_project_structure(self):
        """Create a basic project structure for testing"""
        (self.project_path / ".specpulse").mkdir(exist_ok=True)
        (self.project_path / "memory").mkdir(exist_ok=True)
        (self.project_path / "specs").mkdir(exist_ok=True)
        (self.project_path / "templates").mkdir(exist_ok=True)
        (self.project_path / "scripts").mkdir(exist_ok=True)
        (self.project_path / "plans").mkdir(exist_ok=True)
        
        # Create basic config
        config = {"version": "1.0.0"}
        with open(self.project_path / ".specpulse" / "config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(config, f)

    def test_validator_initialization(self):
        """Test Validator initialization"""
        validator = Validator()
        self.assertEqual(validator.results, [])

    def test_validate_all_complete_project(self):
        """Test validate_all with complete project structure"""
        # Add constitution
        with open(self.project_path / "memory" / "constitution.md", 'w', encoding='utf-8') as f:
            f.write("""# Project Constitution
## Immutable Principles

### Principle 1: Simplicity First
### Principle 2: Test-Driven Development
### Principle 3: Single Responsibility
### Principle 4: Documentation as Code
### Principle 5: Security by Design
""")
        
        # Add config with constitution enforcement
        config = {
            "version": "1.0.0",
            "constitution": {"enforce": True}
        }
        with open(self.project_path / ".specpulse" / "config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(config, f)
        
        results = self.validator.validate_all(self.project_path)
        
        # Should have all success results for structure
        structure_results = [r for r in results if r["status"] == "success" and "Directory" in r["message"]]
        self.assertTrue(len(structure_results) >= 5)  # 5 required directories
        
        # Should validate constitution
        constitution_results = [r for r in results if "Constitution" in r["message"]]
        self.assertTrue(len(constitution_results) > 0)

    def test_validate_all_missing_directories(self):
        """Test validate_all with missing directories"""
        # Remove required directories
        shutil.rmtree(self.project_path / "specs")
        shutil.rmtree(self.project_path / "memory")
        
        results = self.validator.validate_all(self.project_path)
        
        # Should have errors for missing directories
        error_results = [r for r in results if r["status"] == "error"]
        missing_specs = [r for r in error_results if "specs" in r["message"]]
        missing_memory = [r for r in error_results if "memory" in r["message"]]
        
        self.assertTrue(len(missing_specs) > 0)
        self.assertTrue(len(missing_memory) > 0)

    def test_validate_all_missing_config(self):
        """Test validate_all with missing configuration"""
        os.remove(self.project_path / ".specpulse" / "config.yaml")
        
        results = self.validator.validate_all(self.project_path)
        
        # Should have error for missing config
        config_errors = [r for r in results if r["status"] == "error" and "Configuration" in r["message"]]
        self.assertTrue(len(config_errors) > 0)

    def test_validate_spec_no_specs_directory(self):
        """Test validate_spec when specs directory doesn't exist"""
        shutil.rmtree(self.project_path / "specs")
        
        results = self.validator.validate_spec(self.project_path)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "error")
        self.assertIn("No specs directory found", results[0]["message"])

    def test_validate_spec_specific_spec_not_found(self):
        """Test validate_spec with specific spec that doesn't exist"""
        results = self.validator.validate_spec(self.project_path, spec_name="nonexistent-spec")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "error")
        self.assertIn("Specification nonexistent-spec not found", results[0]["message"])

    def test_validate_spec_specific_spec_found(self):
        """Test validate_spec with specific existing spec"""
        # Create a complete spec
        spec_dir = self.project_path / "specs" / "test-feature"
        spec_dir.mkdir(parents=True)
        
        spec_content = """# Test Specification

## Requirements
Some requirements

## User Stories
User story content

## Acceptance Criteria
- Criterion 1
- Criterion 2
"""
        
        with open(spec_dir / "spec.md", 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        results = self.validator.validate_spec(self.project_path, spec_name="test-feature")
        
        # Should find the spec and validate it
        success_results = [r for r in results if r["status"] == "success"]
        self.assertTrue(len(success_results) > 0)

    def test_validate_spec_all_specs(self):
        """Test validate_spec for all specs in directory"""
        # Create multiple specs
        for i in range(3):
            spec_dir = self.project_path / "specs" / f"feature-{i}"
            spec_dir.mkdir(parents=True)
            
            spec_content = f"""# Feature {i} Specification

## Requirements
Requirements for feature {i}

## User Stories
User stories for feature {i}

## Acceptance Criteria
- Criteria for feature {i}
"""
            
            with open(spec_dir / "spec.md", 'w', encoding='utf-8') as f:
                f.write(spec_content)
        
        results = self.validator.validate_spec(self.project_path)
        
        # Should validate all three specs
        feature_results = [r for r in results if "feature-" in r["message"]]
        self.assertEqual(len(feature_results), 3)

    def test_validate_spec_with_missing_sections(self):
        """Test spec validation with missing required sections"""
        spec_dir = self.project_path / "specs" / "incomplete-spec"
        spec_dir.mkdir(parents=True)
        
        # Spec missing required sections
        spec_content = """# Incomplete Specification

## Overview
Just an overview, missing required sections
"""
        
        with open(spec_dir / "spec.md", 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        results = self.validator.validate_spec(self.project_path, spec_name="incomplete-spec")
        
        # Should have error for missing sections
        error_results = [r for r in results if r["status"] == "error" and "Missing sections" in r["message"]]
        self.assertTrue(len(error_results) > 0)

    def test_validate_spec_with_fix_option(self):
        """Test spec validation with fix option enabled"""
        spec_dir = self.project_path / "specs" / "fixable-spec"
        spec_dir.mkdir(parents=True)
        
        # Create spec with missing sections
        spec_content = "# Fixable Specification\n\n## Overview\nJust an overview"
        
        with open(spec_dir / "spec.md", 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        results = self.validator.validate_spec(self.project_path, spec_name="fixable-spec", fix=True)
        
        # Should have warning about fixing
        fix_results = [r for r in results if r["status"] == "warning" and "Fixed missing sections" in r["message"]]
        self.assertTrue(len(fix_results) > 0)
        
        # Check that file was modified
        with open(spec_dir / "spec.md", 'r', encoding='utf-8') as f:
            updated_content = f.read()
        
        self.assertIn("## Requirements", updated_content)
        self.assertIn("## User Stories", updated_content)
        self.assertIn("## Acceptance Criteria", updated_content)

    def test_validate_spec_with_clarifications(self):
        """Test spec validation with clarification markers"""
        spec_dir = self.project_path / "specs" / "clarification-spec"
        spec_dir.mkdir(parents=True)
        
        spec_content = """# Specification with Clarifications

## Requirements
FR-001: Some requirement [NEEDS CLARIFICATION]

## User Stories
**As a** user
**I want** something [NEEDS CLARIFICATION] 
**So that** I can achieve a goal

## Acceptance Criteria
- Criterion 1
- Something unclear [NEEDS CLARIFICATION]
- Criterion 3
"""
        
        with open(spec_dir / "spec.md", 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        # Test with verbose=False
        results = self.validator.validate_spec(self.project_path, spec_name="clarification-spec", verbose=False)
        
        clarification_results = [r for r in results if "clarification" in r["message"]]
        self.assertTrue(len(clarification_results) > 0)
        self.assertIn("3 items needing clarification", clarification_results[0]["message"])
        
        # Test with verbose=True
        results_verbose = self.validator.validate_spec(self.project_path, spec_name="clarification-spec", verbose=True)
        
        clarification_results_verbose = [r for r in results_verbose if "CLARIFICATION" in r["message"]]
        self.assertEqual(len(clarification_results_verbose), 3)  # One for each clarification

    def test_validate_plan_no_plans_directory(self):
        """Test validate_plan when plans directory doesn't exist"""
        shutil.rmtree(self.project_path / "plans")
        
        results = self.validator.validate_plan(self.project_path)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "warning")
        self.assertIn("No plans directory found", results[0]["message"])

    def test_validate_plan_specific_plan_not_found(self):
        """Test validate_plan with specific plan that doesn't exist"""
        results = self.validator.validate_plan(self.project_path, plan_name="nonexistent-plan")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "error")
        self.assertIn("Plan nonexistent-plan not found", results[0]["message"])

    def test_validate_plan_complete_plan(self):
        """Test validate_plan with complete implementation plan"""
        plan_dir = self.project_path / "plans" / "test-plan"
        plan_dir.mkdir(parents=True)
        
        plan_content = """# Implementation Plan: Test Feature

## Specification Reference
- Spec ID: SPEC-001

## Architecture
High-level architecture description

## Technology Stack
Core technologies and rationale

## Implementation Phases
Phase 1: Setup
Phase 2: Implementation
"""
        
        with open(plan_dir / "plan.md", 'w', encoding='utf-8') as f:
            f.write(plan_content)
        
        results = self.validator.validate_plan(self.project_path, plan_name="test-plan")
        
        # Should pass validation
        success_results = [r for r in results if r["status"] == "success"]
        self.assertTrue(len(success_results) > 0)

    def test_validate_plan_missing_sections(self):
        """Test validate_plan with missing required sections"""
        plan_dir = self.project_path / "plans" / "incomplete-plan"
        plan_dir.mkdir(parents=True)
        
        plan_content = """# Incomplete Plan

## Overview
Just an overview
"""
        
        with open(plan_dir / "plan.md", 'w', encoding='utf-8') as f:
            f.write(plan_content)
        
        results = self.validator.validate_plan(self.project_path, plan_name="incomplete-plan")
        
        # Should have error for missing sections
        error_results = [r for r in results if r["status"] == "error" and "Missing sections" in r["message"]]
        self.assertTrue(len(error_results) > 0)

    def test_validate_plan_with_fix_option(self):
        """Test validate_plan with fix option"""
        plan_dir = self.project_path / "plans" / "fixable-plan"
        plan_dir.mkdir(parents=True)
        
        plan_content = "# Fixable Plan\n\n## Overview\nJust an overview"
        
        with open(plan_dir / "plan.md", 'w', encoding='utf-8') as f:
            f.write(plan_content)
        
        results = self.validator.validate_plan(self.project_path, plan_name="fixable-plan", fix=True)
        
        # Should have warning about fixing
        fix_results = [r for r in results if r["status"] == "warning" and "Fixed missing sections" in r["message"]]
        self.assertTrue(len(fix_results) > 0)
        
        # Check that file was modified
        with open(plan_dir / "plan.md", 'r', encoding='utf-8') as f:
            updated_content = f.read()
        
        self.assertIn("## Architecture", updated_content)
        self.assertIn("## Technology Stack", updated_content)
        self.assertIn("## Implementation Phases", updated_content)

    def test_validate_plan_missing_spec_reference(self):
        """Test validate_plan detects missing specification reference"""
        plan_dir = self.project_path / "plans" / "no-ref-plan"
        plan_dir.mkdir(parents=True)
        
        plan_content = """# Plan without Spec Reference

## Architecture
Architecture description

## Technology Stack
Tech stack

## Implementation Phases
Phases description
"""
        
        with open(plan_dir / "plan.md", 'w', encoding='utf-8') as f:
            f.write(plan_content)
        
        results = self.validator.validate_plan(self.project_path, plan_name="no-ref-plan")
        
        # Should have warning for missing spec reference
        warning_results = [r for r in results if r["status"] == "warning" and "No specification reference" in r["message"]]
        self.assertTrue(len(warning_results) > 0)

    def test_validate_constitution_no_constitution_file(self):
        """Test validate_constitution when constitution file doesn't exist"""
        results = self.validator.validate_constitution(self.project_path)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "error")
        self.assertIn("Constitution file not found", results[0]["message"])

    def test_validate_constitution_complete(self):
        """Test validate_constitution with complete constitution"""
        constitution_content = """# Project Constitution

## Immutable Principles

### Principle 1: Simplicity First
Every solution starts with the simplest approach.

### Principle 2: Test-Driven Development
No production code without tests.

### Principle 3: Single Responsibility
Each component does one thing well.

### Principle 4: Documentation as Code
Documentation lives with code.

### Principle 5: Security by Design
Security is considered from the start.
"""
        
        with open(self.project_path / "memory" / "constitution.md", 'w', encoding='utf-8') as f:
            f.write(constitution_content)
        
        # Config with enforcement enabled
        config = {
            "version": "1.0.0",
            "constitution": {"enforce": True}
        }
        with open(self.project_path / ".specpulse" / "config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(config, f)
        
        results = self.validator.validate_constitution(self.project_path, verbose=True)
        
        # Should have success for all principles
        principle_results = [r for r in results if r["status"] == "success" and "Constitution includes" in r["message"]]
        self.assertEqual(len(principle_results), 5)
        
        # Should have success for enforcement
        enforcement_results = [r for r in results if "enforcement enabled" in r["message"]]
        self.assertTrue(len(enforcement_results) > 0)

    def test_validate_constitution_missing_principles(self):
        """Test validate_constitution with missing principles"""
        constitution_content = """# Project Constitution

## Immutable Principles

### Principle 1: Simplicity First
### Principle 2: Test-Driven Development
"""
        
        with open(self.project_path / "memory" / "constitution.md", 'w', encoding='utf-8') as f:
            f.write(constitution_content)
        
        results = self.validator.validate_constitution(self.project_path)
        
        # Should have warnings for missing principles
        warning_results = [r for r in results if r["status"] == "warning" and "missing principle" in r["message"]]
        self.assertTrue(len(warning_results) >= 3)  # Missing at least 3 principles

    def test_validate_constitution_enforcement_disabled(self):
        """Test validate_constitution when enforcement is disabled"""
        constitution_content = """# Project Constitution

## Immutable Principles

### Principle 1: Simplicity First
### Principle 2: Test-Driven Development
### Principle 3: Single Responsibility
### Principle 4: Documentation as Code
### Principle 5: Security by Design
"""
        
        with open(self.project_path / "memory" / "constitution.md", 'w', encoding='utf-8') as f:
            f.write(constitution_content)
        
        # Config with enforcement disabled
        config = {
            "version": "1.0.0",
            "constitution": {"enforce": False}
        }
        with open(self.project_path / ".specpulse" / "config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(config, f)
        
        results = self.validator.validate_constitution(self.project_path)
        
        # Should have warning for disabled enforcement
        warning_results = [r for r in results if "enforcement disabled" in r["message"]]
        self.assertTrue(len(warning_results) > 0)

    def test_private_validate_structure(self):
        """Test _validate_structure method directly"""
        self.validator.results = []
        self.validator._validate_structure(self.project_path)
        
        # Should have success for all required directories
        success_results = [r for r in self.validator.results if r["status"] == "success"]
        self.assertTrue(len(success_results) >= 5)  # 5 required directories + config

    def test_private_validate_specs_no_specs(self):
        """Test _validate_specs when no specs exist"""
        self.validator.results = []
        self.validator._validate_specs(self.project_path, fix=False, verbose=False)
        
        # Should have warning for no specifications
        warning_results = [r for r in self.validator.results if "No specifications found" in r["message"]]
        self.assertTrue(len(warning_results) > 0)

    def test_private_validate_plans_no_plans(self):
        """Test _validate_plans when no plans exist"""
        self.validator.results = []
        self.validator._validate_plans(self.project_path, fix=False, verbose=False)
        
        # Should have info message for no plans
        info_results = [r for r in self.validator.results if "No implementation plans found" in r["message"]]
        self.assertTrue(len(info_results) > 0)

    def test_file_encoding_handling(self):
        """Test proper handling of UTF-8 encoding in validation"""
        # Create spec with unicode characters
        spec_dir = self.project_path / "specs" / "unicode-spec"
        spec_dir.mkdir(parents=True)
        
        spec_content = """# Spécification with Unicode: café

## Requirements
Résumé requirements with naïve approach

## User Stories
User stories with unicode: ñoño

## Acceptance Criteria
- Criterion with é, à, ü characters
"""
        
        with open(spec_dir / "spec.md", 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        # Should handle unicode content properly
        results = self.validator.validate_spec(self.project_path, spec_name="unicode-spec")
        
        success_results = [r for r in results if r["status"] == "success"]
        self.assertTrue(len(success_results) > 0)

    def test_regex_pattern_matching(self):
        """Test regex pattern matching for clarification markers"""
        spec_dir = self.project_path / "specs" / "regex-test"
        spec_dir.mkdir(parents=True)
        
        spec_content = """# Regex Test Specification

## Requirements
Normal requirement
Another requirement [NEEDS CLARIFICATION] with text after
Third requirement

## User Stories
Story with [NEEDS CLARIFICATION] in middle

## Acceptance Criteria
- [NEEDS CLARIFICATION] at start
- Criterion in middle [NEEDS CLARIFICATION] with more text
- [NEEDS CLARIFICATION] final marker at end
"""
        
        with open(spec_dir / "spec.md", 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        results = self.validator.validate_spec(self.project_path, spec_name="regex-test", verbose=True)
        
        # Should find all clarification markers
        clarification_results = [r for r in results if "CLARIFICATION" in r["message"]]
        self.assertEqual(len(clarification_results), 5)  # 5 clarification markers

    def test_yaml_error_handling(self):
        """Test YAML error handling in configuration validation"""
        # Create invalid YAML config
        with open(self.project_path / ".specpulse" / "config.yaml", 'w', encoding='utf-8') as f:
            f.write("invalid: yaml: content: [unclosed")
        
        # Should handle YAML errors gracefully
        results = self.validator.validate_constitution(self.project_path)
        
        # Should still work despite config error
        self.assertIsInstance(results, list)

    def test_directory_iteration_error_handling(self):
        """Test error handling when directory iteration fails"""
        # Create a directory that will cause iteration issues
        specs_dir = self.project_path / "specs"
        
        # Mock directory iteration to raise an exception
        with patch.object(specs_dir, 'iterdir', side_effect=PermissionError("Access denied")):
            results = self.validator.validate_spec(self.project_path)
            
        # Should handle the error gracefully
        self.assertIsInstance(results, list)

    def test_empty_spec_file_handling(self):
        """Test handling of empty specification files"""
        spec_dir = self.project_path / "specs" / "empty-spec"
        spec_dir.mkdir(parents=True)
        
        # Create empty spec file
        with open(spec_dir / "spec.md", 'w', encoding='utf-8') as f:
            f.write("")
        
        results = self.validator.validate_spec(self.project_path, spec_name="empty-spec")
        
        # Should detect missing sections
        error_results = [r for r in results if r["status"] == "error"]
        self.assertTrue(len(error_results) > 0)


if __name__ == '__main__':
    unittest.main()