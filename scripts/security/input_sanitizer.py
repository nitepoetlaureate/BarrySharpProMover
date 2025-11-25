#!/usr/bin/env python3
"""
Input Sanitization Utilities

Sanitizes user input to prevent injection attacks and ensure data safety.
"""

import json
import re
from pathlib import Path
from typing import Any, Union, Dict


# Maximum file sizes for different asset types (in MB)
MAX_FILE_SIZES = {
    'image': 10,      # 10MB for images
    'audio': 50,      # 50MB for audio files
    'json': 5,        # 5MB for JSON files
    'rom': 8,         # 8MB for ROM files (Game Boy max)
    'default': 10,    # 10MB default
}


class InputValidationError(ValueError):
    """Raised when input validation fails."""
    pass


def sanitize_string(input_str: str, max_length: int = 1000,
                    allow_special_chars: bool = False) -> str:
    """
    Sanitize a string input.

    Args:
        input_str: Input string to sanitize
        max_length: Maximum allowed length
        allow_special_chars: If False, only allow alphanumeric, spaces, and basic punctuation

    Returns:
        Sanitized string

    Raises:
        InputValidationError: If input fails validation

    Examples:
        >>> sanitize_string("Hello World")
        'Hello World'

        >>> sanitize_string("A" * 2000, max_length=100)
        InputValidationError: String exceeds maximum length 100
    """
    if not isinstance(input_str, str):
        raise InputValidationError(f"Expected string, got {type(input_str)}")

    # Check length
    if len(input_str) > max_length:
        raise InputValidationError(f"String exceeds maximum length {max_length}")

    # Check for null bytes
    if '\x00' in input_str:
        raise InputValidationError("String contains null bytes")

    # If special characters not allowed, validate character set
    if not allow_special_chars:
        # Allow: alphanumeric, spaces, and basic punctuation
        allowed_pattern = r'^[a-zA-Z0-9\s\.\-_,;:!?()\[\]{}\'\"]+$'
        if not re.match(allowed_pattern, input_str):
            raise InputValidationError(
                "String contains disallowed characters. "
                "Only alphanumeric and basic punctuation allowed."
            )

    return input_str.strip()


def sanitize_json_input(json_str: str, max_depth: int = 10,
                        max_size_mb: float = 5) -> Dict[str, Any]:
    """
    Safely parse and validate JSON input.

    Args:
        json_str: JSON string to parse
        max_depth: Maximum nesting depth
        max_size_mb: Maximum size in megabytes

    Returns:
        Parsed JSON as dictionary

    Raises:
        InputValidationError: If JSON fails validation
        json.JSONDecodeError: If JSON is malformed

    Examples:
        >>> sanitize_json_input('{"name": "test"}')
        {'name': 'test'}

        >>> sanitize_json_input('{"a":' + '{"b":' * 50 + '1' + '}' * 50 + '}', max_depth=10)
        InputValidationError: JSON nesting depth exceeds maximum 10
    """
    # Check size
    size_mb = len(json_str.encode('utf-8')) / (1024 * 1024)
    if size_mb > max_size_mb:
        raise InputValidationError(
            f"JSON size {size_mb:.2f}MB exceeds maximum {max_size_mb}MB"
        )

    # Parse JSON
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise InputValidationError(f"Invalid JSON: {e}")

    # Check nesting depth
    def get_depth(obj, current_depth=0):
        if current_depth > max_depth:
            raise InputValidationError(
                f"JSON nesting depth exceeds maximum {max_depth}"
            )
        if isinstance(obj, dict):
            return max(
                (get_depth(v, current_depth + 1) for v in obj.values()),
                default=current_depth
            )
        elif isinstance(obj, list):
            return max(
                (get_depth(item, current_depth + 1) for item in obj),
                default=current_depth
            )
        return current_depth

    get_depth(data)

    return data


def validate_file_size(file_path: Union[str, Path],
                       asset_type: str = 'default') -> float:
    """
    Validate file size is within allowed limits.

    Args:
        file_path: Path to file
        asset_type: Type of asset ('image', 'audio', 'json', 'rom', 'default')

    Returns:
        File size in megabytes

    Raises:
        FileNotFoundError: If file doesn't exist
        InputValidationError: If file exceeds size limit

    Examples:
        >>> validate_file_size("small_file.png", "image")
        0.5

        >>> validate_file_size("huge_file.rom", "rom")
        InputValidationError: File size 10.5MB exceeds maximum 8MB for rom files
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Get file size in MB
    size_mb = file_path.stat().st_size / (1024 * 1024)

    # Get maximum size for this asset type
    max_size = MAX_FILE_SIZES.get(asset_type, MAX_FILE_SIZES['default'])

    # Validate size
    if size_mb > max_size:
        raise InputValidationError(
            f"File size {size_mb:.2f}MB exceeds maximum {max_size}MB for {asset_type} files"
        )

    return size_mb


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to make it safe for filesystem operations.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename

    Raises:
        InputValidationError: If filename cannot be sanitized

    Examples:
        >>> sanitize_filename("my file.png")
        'my_file.png'

        >>> sanitize_filename("../../../etc/passwd")
        InputValidationError: Filename contains path separators
    """
    # Check for path separators
    if '/' in filename or '\\' in filename:
        raise InputValidationError("Filename contains path separators")

    # Check for null bytes
    if '\x00' in filename:
        raise InputValidationError("Filename contains null bytes")

    # Replace spaces with underscores
    sanitized = filename.replace(' ', '_')

    # Remove any characters that aren't alphanumeric, dot, dash, or underscore
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '', sanitized)

    # Remove leading dots (hidden files)
    sanitized = sanitized.lstrip('.')

    # Check if anything is left
    if not sanitized:
        raise InputValidationError("Filename becomes empty after sanitization")

    return sanitized


def validate_command_input(command: str, allowed_commands: list) -> str:
    """
    Validate a command against an allowlist.

    Args:
        command: Command to validate
        allowed_commands: List of allowed commands

    Returns:
        Validated command

    Raises:
        InputValidationError: If command not in allowlist

    Examples:
        >>> validate_command_input("build", ["build", "test", "deploy"])
        'build'

        >>> validate_command_input("rm -rf /", ["build", "test"])
        InputValidationError: Command 'rm -rf /' not in allowed list
    """
    if command not in allowed_commands:
        raise InputValidationError(
            f"Command '{command}' not in allowed list: {allowed_commands}"
        )

    return command


def escape_shell_arg(arg: str) -> str:
    """
    Escape shell argument to prevent command injection.

    Note: It's better to use subprocess with shell=False and pass arguments
    as a list. This function is for cases where shell execution is necessary.

    Args:
        arg: Argument to escape

    Returns:
        Escaped argument safe for shell

    Examples:
        >>> escape_shell_arg("normal_arg")
        'normal_arg'

        >>> escape_shell_arg("arg; rm -rf /")
        "'arg; rm -rf /'"
    """
    # If argument contains special characters, quote it
    special_chars = r';&|$`\!<>(){}[]"\'*?~'

    if any(char in arg for char in special_chars):
        # Escape single quotes and wrap in single quotes
        arg = arg.replace("'", "'\"'\"'")
        return f"'{arg}'"

    return arg
