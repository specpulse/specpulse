"""Tests for SpecPulse Core"""

import unittest
from pathlib import Path
import tempfile
import shutil
import os
import yaml

from specpulse.core.specpulse import SpecPulse
from specpulse.core.validator import Validator


class TestSpecPulse(unittest.TestCase):
    """Test SpecPulse core functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.specpulse = SpecPulse(Path(self.temp_dir))
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_load_config_returns_empty_if_no_config(self):
        """Test that load_config returns empty dict if no config exists"""
        config = self.specpulse._load_config()
        self.assertEqual(config, {})
    
    def test_load_config_reads_yaml(self):
        """Test that load_config reads YAML correctly"""
        # Create config directory and file
        config_dir = Path(self.temp_dir) / ".specpulse"
        config_dir.mkdir()
        
        config_data = {
            "version": "1.0.0",
            "project": {"name": "test"}
        }
        
        with open(config_dir / "config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        # Reload specpulse to read config
        self.specpulse = SpecPulse(Path(self.temp_dir))
        
        self.assertEqual(self.specpulse.config["version"], "1.0.0")
        self.assertEqual(self.specpulse.config["project"]["name"], "test")
    
    def test_get_spec_template(self):
        """Test that spec template is returned"""
        template = self.specpulse.get_spec_template()
        
        self.assertIn("# Specification:", template)
        self.assertIn("## Functional Requirements", template)
        self.assertIn("## User Stories", template)
        self.assertIn("[NEEDS CLARIFICATION]", template)
    
    def test_get_plan_template(self):
        """Test that plan template is returned"""
        template = self.specpulse.get_plan_template()
        
        self.assertIn("# Implementation Plan:", template)
        self.assertIn("## Technology Stack", template)
        self.assertIn("## Implementation Phases", template)
        self.assertIn("## API Contracts", template)
    
    def test_get_task_template(self):
        """Test that task template is returned"""
        template = self.specpulse.get_task_template()
        
        self.assertIn("# Task List:", template)
        self.assertIn("## Task Organization", template)
        self.assertIn("### Critical Path", template)  # Emoji removed from template
        self.assertIn("T001", template)  # Tasks now use T prefix instead of TASK-
    
    def test_get_constitution_template(self):
        """Test that constitution template is returned"""
        template = self.specpulse.get_constitution_template()
        
        self.assertIn("# Project Constitution", template)
        self.assertIn("## The Nine Articles", template)
        self.assertIn("Library-First Principle", template)
        self.assertIn("Test-First Imperative", template)
    
    def test_get_context_template(self):
        """Test that context template is returned"""
        template = self.specpulse.get_context_template()
        
        self.assertIn("# Project Context", template)
        self.assertIn("## Current State", template)
        self.assertIn("## Team Notes", template)
    
    def test_get_claude_instructions(self):
        """Test that Claude instructions are returned"""
        instructions = self.specpulse.get_claude_instructions()
        
        self.assertIn("# SpecPulse Commands for Claude", instructions)
        self.assertIn("/pulse init", instructions)
        self.assertIn("/spec create", instructions)
        self.assertIn("/plan generate", instructions)
    
    def test_get_gemini_instructions(self):
        """Test that Gemini instructions are returned"""
        instructions = self.specpulse.get_gemini_instructions()
        
        self.assertIn("# SpecPulse Commands for Gemini", instructions)
        self.assertIn("/pulse init", instructions)
        self.assertIn("/validate", instructions)


class TestValidator(unittest.TestCase):
    """Test Validator functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.validator = Validator()
        self.project_path = Path(self.temp_dir)
        
        # Create basic project structure
        (self.project_path / ".specpulse").mkdir()
        (self.project_path / "memory").mkdir()
        (self.project_path / "specs").mkdir()
        (self.project_path / "templates").mkdir()
        (self.project_path / "scripts").mkdir()
        
        # Create config
        config = {"version": "1.0.0"}
        with open(self.project_path / ".specpulse" / "config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(config, f)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_validate_structure(self):
        """Test that structure validation works"""
        results = self.validator.validate_all(self.project_path)
        
        # Check that structure validation passed
        structure_results = [r for r in results if "Directory" in r["message"] or "Configuration" in r["message"]]
        
        for result in structure_results:
            self.assertEqual(result["status"], "success")
    
    def test_validate_missing_structure(self):
        """Test that missing directories are detected"""
        # Remove a required directory
        shutil.rmtree(self.project_path / "specs")
        
        results = self.validator.validate_all(self.project_path)
        
        # Should have error for missing specs directory
        specs_error = [r for r in results if "specs" in r["message"] and r["status"] == "error"]
        self.assertTrue(len(specs_error) > 0)
    
    def test_validate_spec_with_missing_sections(self):
        """Test spec validation with missing sections"""
        # Create a spec with missing sections
        spec_dir = self.project_path / "specs" / "test-feature"
        spec_dir.mkdir(parents=True)
        
        with open(spec_dir / "spec.md", 'w', encoding='utf-8') as f:
            f.write("# Test Spec\n\n## Some Section\n")
        
        results = self.validator.validate_spec(self.project_path)
        
        # Should have error for missing sections
        missing_sections = [r for r in results if "Missing sections" in r["message"]]
        self.assertTrue(len(missing_sections) > 0)
    
    def test_validate_spec_with_clarifications(self):
        """Test spec validation detects clarification markers"""
        # Create a spec with clarification markers
        spec_dir = self.project_path / "specs" / "test-feature"
        spec_dir.mkdir(parents=True)
        
        with open(spec_dir / "spec.md", 'w', encoding='utf-8') as f:
            f.write("""# Test Spec
## Requirements
Some requirement

## User Stories
A story

## Acceptance Criteria
- Criteria 1
- Something [NEEDS CLARIFICATION]
""")
        
        results = self.validator.validate_spec(self.project_path, verbose=True)
        
        # Should have warning for clarification
        clarifications = [r for r in results if "CLARIFICATION" in r["message"]]
        self.assertTrue(len(clarifications) > 0)
    
    def test_validate_constitution_compliance(self):
        """Test constitution compliance validation"""
        # Create constitution file
        with open(self.project_path / "memory" / "constitution.md", 'w', encoding='utf-8') as f:
            f.write("""# Project Constitution
## Immutable Principles

### Principle 1: Simplicity First
### Principle 2: Test-Driven Development
### Principle 3: Single Responsibility
### Principle 4: Documentation as Code
### Principle 5: Security by Design
""")
        
        # Create config with constitution enforcement
        config = {
            "version": "1.0.0",
            "constitution": {
                "enforce": True
            }
        }
        with open(self.project_path / ".specpulse" / "config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(config, f)
        
        results = self.validator.validate_constitution(self.project_path, verbose=True)
        
        # Should have success for all principles
        principle_results = [r for r in results if "Constitution includes" in r["message"]]
        self.assertTrue(len(principle_results) >= 5)
        
        # Should have success for enforcement
        enforcement_results = [r for r in results if "enforcement enabled" in r["message"]]
        self.assertTrue(len(enforcement_results) > 0)


if __name__ == '__main__':
    unittest.main()