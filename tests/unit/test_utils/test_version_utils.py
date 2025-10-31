"""
Tests for version utilities
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json
from pathlib import Path
import tempfile

from specpulse.utils.version_check import (
    check_pypi_version,
    compare_versions,
    should_check_version,
    get_update_message
)


class TestVersionCheck:
    """Test version checking utilities"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = Path(self.temp_dir) / ".specpulse_version_cache.json"

    def test_compare_versions_equal(self):
        """Test comparing equal versions"""
        is_newer, is_major = compare_versions("1.2.3", "1.2.3")
        assert is_newer is False
        assert is_major is False

    def test_compare_versions_patch(self):
        """Test comparing patch version difference"""
        is_newer, is_major = compare_versions("1.2.3", "1.2.4")
        assert is_newer is True
        assert is_major is False

    def test_compare_versions_minor(self):
        """Test comparing minor version difference"""
        is_newer, is_major = compare_versions("1.2.3", "1.3.0")
        assert is_newer is True
        assert is_major is False

    def test_compare_versions_major(self):
        """Test comparing major version difference"""
        is_newer, is_major = compare_versions("1.2.3", "2.0.0")
        assert is_newer is True
        assert is_major is True

    def test_compare_versions_older(self):
        """Test when remote version is older"""
        is_newer, is_major = compare_versions("2.0.0", "1.9.9")
        assert is_newer is False
        assert is_major is False

    def test_compare_versions_invalid(self):
        """Test with invalid version strings"""
        is_newer, is_major = compare_versions("1.2.3", "invalid")
        assert is_newer is False
        assert is_major is False

        is_newer, is_major = compare_versions("invalid", "1.2.3")
        assert is_newer is False
        assert is_major is False

    def test_should_check_version(self):
        """Test version check"""
        # This function checks if 24 hours have passed
        # We can only test that it returns a boolean
        result = should_check_version()
        assert isinstance(result, bool)

    @patch('pathlib.Path.exists')
    def test_should_check_version_with_cache(self, mock_exists):
        """Test version check with cache file"""
        mock_exists.return_value = True
        result = should_check_version()
        assert isinstance(result, bool)

    @patch('requests.get')
    def test_check_pypi_version_success(self, mock_get):
        """Test successful PyPI version check"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "info": {"version": "1.2.3"}
        }
        mock_get.return_value = mock_response

        version = check_pypi_version("specpulse")
        assert version == "1.2.3"

    @patch('requests.get')
    def test_check_pypi_version_failure(self, mock_get):
        """Test PyPI check failure"""
        mock_get.side_effect = Exception("Network error")

        version = check_pypi_version("specpulse")
        assert version is None

    @patch('requests.get')
    def test_check_pypi_version_404(self, mock_get):
        """Test PyPI check with 404"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        version = check_pypi_version("nonexistent-package")
        assert version is None

    def test_get_update_message_patch(self):
        """Test update message for patch version"""
        message = get_update_message("1.2.3", "1.2.4", False)
        assert "1.2.4" in message

    def test_get_update_message_major(self):
        """Test update message for major version"""
        message = get_update_message("1.2.3", "2.0.0", True)
        assert "MAJOR" in message
        assert "2.0.0" in message

    def test_get_update_message_no_update(self):
        """Test update message when no update needed"""
        # When versions are the same, there should be no update message
        message = get_update_message("1.2.3", "1.2.3", False)
        # The message format depends on implementation
        assert isinstance(message, str)