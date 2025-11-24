#!/usr/bin/env python3
"""
Unit Tests for check_bg_tiles.py

Tests background tile validation including:
- Dimension validation (160x144)
- Tile count validation (max 192 tiles)
- Format validation (PNG)
- Error handling
"""

import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts' / 'validation'))

from check_bg_tiles import validate_background, get_tiles


class TestValidateBackground:
    """Test background validation function."""

    @pytest.mark.unit
    def test_valid_background(self, valid_background):
        """Test validation of a valid background image."""
        is_valid, message = validate_background(str(valid_background))
        assert is_valid is True
        assert "OK" in message or message == ""

    @pytest.mark.unit
    def test_invalid_size(self, invalid_background_size):
        """Test validation fails for incorrect dimensions."""
        is_valid, message = validate_background(str(invalid_background_size))
        assert is_valid is False
        assert "dimensions" in message.lower() or "size" in message.lower()

    @pytest.mark.unit
    def test_file_not_found(self, temp_dir):
        """Test error handling for non-existent file."""
        nonexistent = temp_dir / "nonexistent.png"
        is_valid, message = validate_background(str(nonexistent))
        assert is_valid is False
        assert "not found" in message.lower() or "no such file" in message.lower()

    @pytest.mark.unit
    def test_invalid_image_format(self, temp_dir):
        """Test error handling for non-image files."""
        text_file = temp_dir / "not_an_image.png"
        text_file.write_text("This is not an image")

        is_valid, message = validate_background(str(text_file))
        assert is_valid is False
        # Should catch PIL errors

    @pytest.mark.unit
    def test_permission_denied(self, temp_dir, valid_background, monkeypatch):
        """Test error handling for permission denied."""
        import os

        def mock_open(*args, **kwargs):
            raise PermissionError("Permission denied")

        monkeypatch.setattr('builtins.open', mock_open)

        # This should now trigger permission error handling
        is_valid, message = validate_background(str(valid_background))
        # The function should handle the error gracefully


class TestGetTiles:
    """Test tile extraction function."""

    @pytest.mark.unit
    def test_tile_extraction(self, valid_background):
        """Test unique tile extraction."""
        from PIL import Image
        img = Image.open(valid_background)

        # The function should return a set of unique tiles
        tiles = get_tiles(img)
        assert isinstance(tiles, set)
        assert len(tiles) > 0
        assert len(tiles) <= 192  # Should not exceed max tiles
