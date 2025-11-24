#!/usr/bin/env python3
"""
Unit Tests for check_sprites.py

Tests sprite validation including:
- Dimension validation (8x8 or 16x16 multiples)
- Color count validation (max 4 colors including transparency)
- Format validation (PNG with alpha channel)
- Error handling
"""

import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts' / 'validation'))

from check_sprites import validate_sprite


class TestValidateSprite:
    """Test sprite validation function."""

    @pytest.mark.unit
    def test_valid_sprite(self, valid_sprite):
        """Test validation of a valid sprite."""
        is_valid, issues = validate_sprite(str(valid_sprite))
        assert is_valid is True
        assert len(issues) == 0

    @pytest.mark.unit
    def test_invalid_dimensions(self, temp_dir, create_test_image):
        """Test validation fails for invalid dimensions."""
        # Create sprite with non-8x8/16x16 dimensions
        sprite = temp_dir / "wrong_size.png"
        create_test_image(sprite, 15, 15, None, 'RGBA')

        is_valid, issues = validate_sprite(str(sprite))
        assert is_valid is False
        assert any("dimension" in issue.lower() or "size" in issue.lower()
                   for issue in issues)

    @pytest.mark.unit
    def test_too_many_colors(self, invalid_sprite_colors):
        """Test validation fails for too many colors."""
        is_valid, issues = validate_sprite(str(invalid_sprite_colors))
        assert is_valid is False
        assert any("color" in issue.lower() for issue in issues)

    @pytest.mark.unit
    def test_missing_alpha_channel(self, temp_dir, create_test_image):
        """Test validation warns about missing alpha channel."""
        sprite = temp_dir / "no_alpha.png"
        create_test_image(sprite, 16, 16, None, 'RGB')  # No alpha

        is_valid, issues = validate_sprite(str(sprite))
        # Should warn about missing alpha channel
        # (may still be valid if colors are ok)

    @pytest.mark.unit
    def test_file_not_found(self, temp_dir):
        """Test error handling for non-existent file."""
        nonexistent = temp_dir / "nonexistent.png"
        is_valid, issues = validate_sprite(str(nonexistent))
        assert is_valid is False
        assert any("not found" in issue.lower() for issue in issues)

    @pytest.mark.unit
    def test_valid_8x8_sprite(self, temp_dir, create_test_image):
        """Test validation of 8x8 sprite."""
        sprite = temp_dir / "8x8_sprite.png"
        colors = [(0, 0, 0, 0), (255, 255, 255, 255), (128, 128, 128, 255)]
        create_test_image(sprite, 8, 8, colors, 'RGBA')

        is_valid, issues = validate_sprite(str(sprite))
        assert is_valid is True

    @pytest.mark.unit
    def test_valid_16x16_sprite(self, temp_dir, create_test_image):
        """Test validation of 16x16 sprite."""
        sprite = temp_dir / "16x16_sprite.png"
        colors = [(0, 0, 0, 0), (255, 255, 255, 255)]
        create_test_image(sprite, 16, 16, colors, 'RGBA')

        is_valid, issues = validate_sprite(str(sprite))
        assert is_valid is True

    @pytest.mark.unit
    def test_multiframe_sprite(self, temp_dir, create_test_image):
        """Test validation of multi-frame sprite (32x16)."""
        sprite = temp_dir / "multiframe.png"
        colors = [(0, 0, 0, 0), (255, 255, 255, 255)]
        create_test_image(sprite, 32, 16, colors, 'RGBA')

        is_valid, issues = validate_sprite(str(sprite))
        # Should be valid (2 frames of 16x16)
        assert is_valid is True
