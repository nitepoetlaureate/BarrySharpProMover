#!/usr/bin/env python3
"""
Path Validation Utilities

Prevents path traversal attacks and ensures file operations stay within
allowed directories.
"""

import os
from pathlib import Path
from typing import Union, Optional


class PathTraversalError(ValueError):
    """Raised when a path traversal attempt is detected."""
    pass


def safe_path(user_path: Union[str, Path], base_dir: Union[str, Path],
              must_exist: bool = False) -> Path:
    """
    Validate that a user-provided path is within the allowed base directory.

    This prevents path traversal attacks like:
    - ../../../etc/passwd
    - /absolute/path/outside/project
    - symlinks pointing outside base_dir

    Args:
        user_path: User-provided path (relative or absolute)
        base_dir: Base directory that user_path must be within
        must_exist: If True, raise error if path doesn't exist

    Returns:
        Resolved absolute Path object within base_dir

    Raises:
        PathTraversalError: If path escapes base_dir
        FileNotFoundError: If must_exist=True and path doesn't exist

    Examples:
        >>> safe_path("assets/bg.png", "/project")
        PosixPath('/project/assets/bg.png')

        >>> safe_path("../../../etc/passwd", "/project")
        PathTraversalError: Path '../../../etc/passwd' escapes base directory
    """
    base_dir = Path(base_dir).resolve()

    # Handle absolute paths by making them relative
    if Path(user_path).is_absolute():
        # Absolute paths are suspicious - reject them
        raise PathTraversalError(
            f"Absolute path '{user_path}' not allowed. Use relative paths only."
        )

    # Resolve the full path
    try:
        full_path = (base_dir / user_path).resolve()
    except (OSError, ValueError) as e:
        raise PathTraversalError(f"Invalid path '{user_path}': {e}")

    # Check if resolved path is within base_dir
    try:
        full_path.relative_to(base_dir)
    except ValueError:
        raise PathTraversalError(
            f"Path '{user_path}' escapes base directory '{base_dir}'"
        )

    # Check existence if required
    if must_exist and not full_path.exists():
        raise FileNotFoundError(f"Path does not exist: {full_path}")

    return full_path


def validate_file_path(file_path: Union[str, Path],
                       allowed_extensions: Optional[list] = None,
                       max_size_mb: Optional[float] = None) -> Path:
    """
    Validate a file path with security checks.

    Args:
        file_path: Path to validate
        allowed_extensions: List of allowed extensions (e.g., ['.png', '.jpg'])
        max_size_mb: Maximum file size in megabytes

    Returns:
        Validated Path object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file fails validation checks

    Examples:
        >>> validate_file_path("image.png", allowed_extensions=['.png', '.jpg'])
        PosixPath('image.png')

        >>> validate_file_path("script.sh", allowed_extensions=['.png'])
        ValueError: File extension '.sh' not in allowed list
    """
    file_path = Path(file_path)

    # Check file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Check it's a file (not a directory)
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    # Check extension if provided
    if allowed_extensions is not None:
        if file_path.suffix.lower() not in [ext.lower() for ext in allowed_extensions]:
            raise ValueError(
                f"File extension '{file_path.suffix}' not in allowed list: {allowed_extensions}"
            )

    # Check file size if provided
    if max_size_mb is not None:
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > max_size_mb:
            raise ValueError(
                f"File size {file_size_mb:.2f}MB exceeds maximum {max_size_mb}MB"
            )

    return file_path


def is_safe_filename(filename: str) -> bool:
    """
    Check if a filename is safe (no path separators, no hidden files).

    Args:
        filename: Filename to check

    Returns:
        True if filename is safe, False otherwise

    Examples:
        >>> is_safe_filename("image.png")
        True

        >>> is_safe_filename("../etc/passwd")
        False

        >>> is_safe_filename(".hidden")
        False
    """
    # Reject empty filenames
    if not filename or not filename.strip():
        return False

    # Reject path separators
    if '/' in filename or '\\' in filename:
        return False

    # Reject parent directory references
    if filename in ('.', '..'):
        return False

    # Reject hidden files (starting with .)
    if filename.startswith('.'):
        return False

    # Reject null bytes
    if '\x00' in filename:
        return False

    return True


def get_project_root() -> Path:
    """
    Get the project root directory safely.

    Returns:
        Path to project root
    """
    # This file is in scripts/security/, so project root is 2 levels up
    return Path(__file__).parent.parent.parent.resolve()


def get_allowed_directories() -> dict:
    """
    Get dictionary of allowed directories for different asset types.

    Returns:
        Dict mapping asset type to allowed directory path
    """
    project_root = get_project_root()

    return {
        'backgrounds': project_root / 'assets' / 'backgrounds',
        'sprites': project_root / 'assets' / 'sprites',
        'music': project_root / 'assets' / 'music',
        'sounds': project_root / 'assets' / 'sounds',
        'fonts': project_root / 'assets' / 'fonts',
        'scenes': project_root / 'project' / 'scenes',
        'build': project_root / 'build',
        'project': project_root,
    }
