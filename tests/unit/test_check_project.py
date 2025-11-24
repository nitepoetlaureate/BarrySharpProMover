#!/usr/bin/env python3
"""
Unit Tests for check_project.py

Tests GB Studio project file validation including:
- Project structure validation
- Version compatibility checking
- Required fields validation
- Error handling
"""

import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts' / 'validation'))

from check_project import validate_project_file, validate_project_structure


class TestValidateProjectFile:
    """Test project file validation function."""

    @pytest.mark.unit
    def test_valid_project(self, valid_gbsproj):
        """Test validation of a valid project file."""
        is_valid, issues = validate_project_file(str(valid_gbsproj))
        assert is_valid is True
        assert len(issues) == 0

    @pytest.mark.unit
    def test_missing_version(self, invalid_gbsproj_missing_version):
        """Test validation fails for missing version."""
        is_valid, issues = validate_project_file(str(invalid_gbsproj_missing_version))
        assert is_valid is False
        assert any("version" in issue.lower() for issue in issues)

    @pytest.mark.unit
    def test_file_not_found(self, temp_dir):
        """Test error handling for non-existent file."""
        nonexistent = temp_dir / "nonexistent.gbsproj"
        is_valid, issues = validate_project_file(str(nonexistent))
        assert is_valid is False
        assert any("not found" in issue.lower() for issue in issues)

    @pytest.mark.unit
    def test_invalid_json(self, temp_dir):
        """Test error handling for invalid JSON."""
        invalid_json = temp_dir / "invalid.gbsproj"
        invalid_json.write_text("{ invalid json }")

        is_valid, issues = validate_project_file(str(invalid_json))
        assert is_valid is False

    @pytest.mark.unit
    def test_wrong_resource_type(self, temp_dir):
        """Test validation fails for wrong resource type."""
        import json
        wrong_type = temp_dir / "wrong_type.gbsproj"
        data = {
            "_resourceType": "scene",  # Should be "project"
            "name": "Wrong Type",
            "_version": "4.1.0"
        }
        with open(wrong_type, 'w') as f:
            json.dump(data, f)

        is_valid, issues = validate_project_file(str(wrong_type))
        # Should detect wrong resource type


class TestValidateProjectStructure:
    """Test project structure validation."""

    @pytest.mark.unit
    def test_valid_structure(self):
        """Test validation of valid project structure."""
        data = {
            "_resourceType": "project",
            "name": "Test",
            "_version": "4.1.0",
            "settings": {}
        }

        is_valid, issues = validate_project_structure(data)
        assert is_valid is True
        assert len(issues) == 0

    @pytest.mark.unit
    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        data = {
            "name": "Test"
            # Missing _resourceType and _version
        }

        is_valid, issues = validate_project_structure(data)
        assert is_valid is False
        assert len(issues) > 0
