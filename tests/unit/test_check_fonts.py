#!/usr/bin/env python3
"""
Unit Tests for check_fonts.py

Tests font file validation including:
- JSON structure validation
- Required fields checking
- Character mapping validation
- Error handling
"""

import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts' / 'validation'))

from check_fonts import validate_font_file


class TestValidateFontFile:
    """Test font file validation function."""

    @pytest.mark.unit
    def test_valid_font(self, valid_font_json):
        """Test validation of a valid font file."""
        is_valid, issues = validate_font_file(str(valid_font_json))
        assert is_valid is True
        assert len(issues) == 0

    @pytest.mark.unit
    def test_missing_required_fields(self, invalid_font_json_missing_fields):
        """Test validation fails for missing required fields."""
        is_valid, issues = validate_font_file(str(invalid_font_json_missing_fields))
        assert is_valid is False
        assert any("required" in issue.lower() or "missing" in issue.lower()
                   for issue in issues)

    @pytest.mark.unit
    def test_file_not_found(self, temp_dir):
        """Test error handling for non-existent file."""
        nonexistent = temp_dir / "nonexistent.json"
        is_valid, issues = validate_font_file(str(nonexistent))
        assert is_valid is False
        assert any("not found" in issue.lower() for issue in issues)

    @pytest.mark.unit
    def test_invalid_json(self, temp_dir):
        """Test error handling for invalid JSON."""
        invalid_json = temp_dir / "invalid.json"
        invalid_json.write_text("{ this is not valid JSON }")

        is_valid, issues = validate_font_file(str(invalid_json))
        assert is_valid is False
        assert any("json" in issue.lower() or "parse" in issue.lower()
                   for issue in issues)

    @pytest.mark.unit
    def test_empty_mapping(self, temp_dir):
        """Test validation warns about empty character mapping."""
        font_data = {
            "id": "empty-mapping",
            "name": "Empty Font",
            "filename": "empty.png",
            "mapping": {}
        }
        import json
        font_path = temp_dir / "empty_mapping.json"
        with open(font_path, 'w') as f:
            json.dump(font_data, f)

        is_valid, issues = validate_font_file(str(font_path))
        # Should warn about empty mapping
        assert any("mapping" in issue.lower() or "empty" in issue.lower()
                   for issue in issues)
