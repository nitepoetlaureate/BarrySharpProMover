#!/usr/bin/env python3
"""
Unit Tests for Path Validation Security Utilities

Tests path traversal prevention and secure path handling.
"""

import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))

from security.path_validator import (
    safe_path,
    validate_file_path,
    is_safe_filename,
    PathTraversalError
)


class TestSafePath:
    """Test safe_path function for path traversal prevention."""

    @pytest.mark.unit
    def test_safe_relative_path(self, temp_dir):
        """Test that safe relative paths are allowed."""
        result = safe_path("subdir/file.txt", temp_dir)
        assert result == temp_dir / "subdir/file.txt"

    @pytest.mark.unit
    def test_path_traversal_blocked(self, temp_dir):
        """Test that path traversal attempts are blocked."""
        with pytest.raises(PathTraversalError):
            safe_path("../../../etc/passwd", temp_dir)

    @pytest.mark.unit
    def test_absolute_path_blocked(self, temp_dir):
        """Test that absolute paths are blocked."""
        with pytest.raises(PathTraversalError):
            safe_path("/etc/passwd", temp_dir)

    @pytest.mark.unit
    def test_must_exist_validation(self, temp_dir):
        """Test must_exist flag."""
        # Non-existent path with must_exist=True should raise
        with pytest.raises(FileNotFoundError):
            safe_path("nonexistent.txt", temp_dir, must_exist=True)

        # Create file and test again
        test_file = temp_dir / "exists.txt"
        test_file.write_text("test")

        result = safe_path("exists.txt", temp_dir, must_exist=True)
        assert result == test_file

    @pytest.mark.unit
    def test_symlink_attack(self, temp_dir):
        """Test that symlinks pointing outside base_dir are blocked."""
        # Create a symlink pointing outside
        symlink = temp_dir / "evil_link"
        outside_dir = temp_dir.parent / "outside"
        outside_dir.mkdir(exist_ok=True)

        symlink.symlink_to(outside_dir)

        # Should raise PathTraversalError
        with pytest.raises(PathTraversalError):
            safe_path("evil_link", temp_dir)

    @pytest.mark.unit
    def test_current_directory_reference(self, temp_dir):
        """Test that ./ references work correctly."""
        result = safe_path("./file.txt", temp_dir)
        assert result == temp_dir / "file.txt"

    @pytest.mark.unit
    def test_parent_directory_in_middle(self, temp_dir):
        """Test paths with .. in the middle."""
        # This should be blocked if it escapes base_dir
        with pytest.raises(PathTraversalError):
            safe_path("subdir/../../outside.txt", temp_dir)


class TestValidateFilePath:
    """Test validate_file_path function."""

    @pytest.mark.unit
    def test_valid_file(self, temp_dir):
        """Test validation of valid file."""
        test_file = temp_dir / "test.png"
        test_file.write_bytes(b"fake image data")

        result = validate_file_path(test_file, allowed_extensions=['.png', '.jpg'])
        assert result == test_file

    @pytest.mark.unit
    def test_invalid_extension(self, temp_dir):
        """Test that invalid extensions are rejected."""
        test_file = temp_dir / "test.exe"
        test_file.write_bytes(b"fake executable")

        with pytest.raises(ValueError, match="not in allowed list"):
            validate_file_path(test_file, allowed_extensions=['.png', '.jpg'])

    @pytest.mark.unit
    def test_file_too_large(self, temp_dir):
        """Test file size validation."""
        test_file = temp_dir / "large.dat"
        # Create 2MB file
        test_file.write_bytes(b"0" * (2 * 1024 * 1024))

        with pytest.raises(ValueError, match="exceeds maximum"):
            validate_file_path(test_file, max_size_mb=1)

    @pytest.mark.unit
    def test_directory_rejected(self, temp_dir):
        """Test that directories are rejected."""
        subdir = temp_dir / "subdir"
        subdir.mkdir()

        with pytest.raises(ValueError, match="not a file"):
            validate_file_path(subdir)

    @pytest.mark.unit
    def test_nonexistent_file(self, temp_dir):
        """Test error for non-existent file."""
        with pytest.raises(FileNotFoundError):
            validate_file_path(temp_dir / "nonexistent.txt")


class TestIsSafeFilename:
    """Test is_safe_filename function."""

    @pytest.mark.unit
    def test_safe_filename(self):
        """Test that safe filenames are accepted."""
        assert is_safe_filename("image.png") is True
        assert is_safe_filename("my_file.txt") is True
        assert is_safe_filename("data-file.json") is True

    @pytest.mark.unit
    def test_path_separator_rejected(self):
        """Test that filenames with path separators are rejected."""
        assert is_safe_filename("../etc/passwd") is False
        assert is_safe_filename("subdir/file.txt") is False
        assert is_safe_filename("..\\windows\\system32") is False

    @pytest.mark.unit
    def test_hidden_file_rejected(self):
        """Test that hidden files (starting with .) are rejected."""
        assert is_safe_filename(".hidden") is False
        assert is_safe_filename(".bashrc") is False

    @pytest.mark.unit
    def test_parent_directory_rejected(self):
        """Test that . and .. are rejected."""
        assert is_safe_filename(".") is False
        assert is_safe_filename("..") is False

    @pytest.mark.unit
    def test_empty_filename_rejected(self):
        """Test that empty filenames are rejected."""
        assert is_safe_filename("") is False
        assert is_safe_filename("   ") is False

    @pytest.mark.unit
    def test_null_byte_rejected(self):
        """Test that filenames with null bytes are rejected."""
        assert is_safe_filename("file\x00.txt") is False


class TestPathValidatorIntegration:
    """Integration tests for path validation."""

    @pytest.mark.integration
    def test_complete_validation_workflow(self, temp_dir):
        """Test complete file validation workflow."""
        # Create a valid file
        test_file = temp_dir / "valid_image.png"
        test_file.write_bytes(b"PNG" * 1000)  # Small file

        # Validate filename
        assert is_safe_filename("valid_image.png") is True

        # Validate path
        safe_file = safe_path("valid_image.png", temp_dir, must_exist=True)

        # Validate file properties
        result = validate_file_path(safe_file, allowed_extensions=['.png'], max_size_mb=1)

        assert result == safe_file

    @pytest.mark.integration
    def test_malicious_filename_workflow(self, temp_dir):
        """Test that malicious filenames are caught."""
        malicious_names = [
            "../../../etc/passwd",
            ".hidden_backdoor",
            "file\x00.txt",
            "subdir/../../outside.txt",
        ]

        for name in malicious_names:
            # Filename check should fail
            assert is_safe_filename(name) is False

            # Path validation should also fail if filename check is bypassed
            with pytest.raises((PathTraversalError, ValueError, FileNotFoundError)):
                safe_path(name, temp_dir)
