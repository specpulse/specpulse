"""
Tests for SpecPulse core module
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from specpulse.core.specpulse import SpecPulse


class TestSpecPulse:
    """Test SpecPulse core functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        self.specpulse = SpecPulse()

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test SpecPulse initialization"""
        sp = SpecPulse()
        assert sp.resources_dir.exists()
        assert sp.templates_dir == sp.resources_dir / "templates"

    def test_get_template(self):
        """Test template retrieval"""
        # Create a test template
        template_file = self.specpulse.templates_dir / "test.md"
        template_file.parent.mkdir(parents=True, exist_ok=True)
        template_file.write_text("# Test Template\n{{variable}}")

        content = self.specpulse.get_template("test.md")
        assert "# Test Template" in content

    def test_get_template_not_found(self):
        """Test getting non-existent template"""
        content = self.specpulse.get_template("nonexistent.md")
        assert content == ""

    def test_get_template_with_variables(self):
        """Test template with variable substitution"""
        template_file = self.specpulse.templates_dir / "var.md"
        template_file.parent.mkdir(parents=True, exist_ok=True)
        template_file.write_text("Hello {{name}}")

        content = self.specpulse.get_template("var.md", variables={"name": "World"})
        assert "Hello World" in content

    def test_get_decomposition_template(self):
        """Test decomposition template retrieval"""
        # Create decomposition template
        decomp_dir = self.specpulse.templates_dir / "decomposition"
        decomp_dir.mkdir(parents=True, exist_ok=True)
        template_file = decomp_dir / "test.md"
        template_file.write_text("# Decomposition")

        content = self.specpulse.get_decomposition_template("test.md")
        assert "# Decomposition" in content

    def test_generate_claude_commands(self):
        """Test Claude command generation"""
        commands = self.specpulse.generate_claude_commands()

        assert isinstance(commands, list)
        assert len(commands) > 0

        # Check structure
        for cmd in commands:
            assert "name" in cmd
            assert "description" in cmd
            assert "script" in cmd

        # Check required commands exist
        command_names = [cmd["name"] for cmd in commands]
        assert "sp-pulse" in command_names
        assert "sp-spec" in command_names
        assert "sp-plan" in command_names
        assert "sp-task" in command_names

    def test_generate_gemini_commands(self):
        """Test Gemini command generation"""
        commands = self.specpulse.generate_gemini_commands()

        assert isinstance(commands, list)
        assert len(commands) > 0

        # Check structure
        for cmd in commands:
            assert "name" in cmd
            assert "description" in cmd
            assert "script" in cmd

        # Check commands match Claude commands
        command_names = [cmd["name"] for cmd in commands]
        assert "sp-pulse" in command_names
        assert "sp-spec" in command_names

    def test_decompose_specification(self):
        """Test specification decomposition"""
        spec_content = """
        # E-Commerce System

        ## Services
        - User authentication
        - Product catalog
        - Shopping cart
        - Payment processing
        """

        spec_dir = self.project_path / "specs" / "001-ecommerce"
        spec_dir.mkdir(parents=True)

        result = self.specpulse.decompose_specification(spec_dir, spec_content)

        assert isinstance(result, dict)
        assert "services" in result
        assert "api_contracts" in result
        assert "integration_points" in result
        assert len(result["services"]) > 0

    def test_decompose_empty_specification(self):
        """Test decomposing empty specification"""
        spec_dir = self.project_path / "specs" / "001-empty"
        spec_dir.mkdir(parents=True)

        result = self.specpulse.decompose_specification(spec_dir, "")

        assert result["services"] == []
        assert result["api_contracts"] == []

    def test_extract_services(self):
        """Test service extraction from specification"""
        spec_content = """
        ## Services
        - Authentication Service
        - User Management Service
        - Product Catalog Service
        """

        result = self.specpulse.decompose_specification(
            self.project_path, spec_content
        )

        assert len(result["services"]) == 3
        assert "authentication" in result["services"]
        assert "user-management" in result["services"]
        assert "product-catalog" in result["services"]

    def test_extract_api_contracts(self):
        """Test API contract extraction"""
        spec_content = """
        ## API Endpoints
        - POST /api/auth/login
        - GET /api/users/{id}
        - POST /api/products
        """

        result = self.specpulse.decompose_specification(
            self.project_path, spec_content
        )

        assert "api_contracts" in result

    def test_create_decomposition_files(self):
        """Test creation of decomposition files"""
        spec_dir = self.project_path / "specs" / "001-test"
        spec_dir.mkdir(parents=True)

        spec_content = """
        ## Services
        - Auth Service
        - User Service
        """

        result = self.specpulse.decompose_specification(spec_dir, spec_content)

        # Check if decomposition directory is created
        decomp_dir = spec_dir / "decomposition"
        assert decomp_dir.exists()

    def test_template_loading_fallback(self):
        """Test template loading with fallback"""
        # Remove templates directory to test fallback
        if self.specpulse.templates_dir.exists():
            shutil.rmtree(self.specpulse.templates_dir)

        content = self.specpulse.get_template("nonexistent.md")
        assert content == ""

    def test_resource_directory_creation(self):
        """Test that resource directories are properly set"""
        sp = SpecPulse()
        assert sp.resources_dir is not None
        assert sp.templates_dir is not None
        # Templates dir is a path object pointing to resources/templates
        assert str(sp.templates_dir).endswith("templates")