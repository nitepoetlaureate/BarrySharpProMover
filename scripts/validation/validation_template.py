#!/usr/bin/env python3
"""
Template for Validation Scripts
Copy this file and modify for specific validation needs.

Usage:
    python3 validation_template.py <files...>
    python3 validation_template.py -v <files...>  # verbose mode

Exit Codes:
    0 - All validations passed
    1 - Validation failure (files don't meet criteria)
    2 - Error occurred (file not found, permission denied, etc.)
    130 - User cancelled (Ctrl+C)
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Tuple, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Validation constants
# TODO: Define your validation limits here
MAX_SIZE = 1024 * 1024  # Example: 1MB max file size


def validate_item(path: Path) -> Tuple[bool, List[str]]:
    """
    Validate a single item.

    Args:
        path: Path to item to validate

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    try:
        # Check file exists
        if not path.exists():
            logger.error(f"File not found: {path}")
            return False, ["File not found"]

        if not path.is_file():
            logger.error(f"Not a file: {path}")
            return False, ["Not a file"]

        # TODO: Add your validation logic here
        # Example: Check file size
        file_size = path.stat().st_size
        if file_size > MAX_SIZE:
            issues.append(f"File too large: {file_size} bytes (max: {MAX_SIZE})")

        # Example: Check file extension
        # if path.suffix.lower() not in ['.png', '.jpg']:
        #     issues.append(f"Invalid file type: {path.suffix}")

        # Log results
        if issues:
            logger.warning(f"{path.name}: {len(issues)} issue(s) found")
            for issue in issues:
                logger.warning(f"  ❌ {issue}")
            return False, issues
        else:
            logger.info(f"✅ {path.name}: OK")
            return True, []

    except PermissionError:
        logger.error(f"Permission denied: {path}")
        return False, ["Permission denied"]
    except Exception as e:
        logger.error(f"Unexpected error processing {path}: {e}")
        return False, [f"Unexpected error: {e}"]


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate items (customize this description)",
        epilog="Exit codes: 0=success, 1=validation failure, 2=error, 130=cancelled"
    )
    parser.add_argument(
        "files",
        nargs='+',
        help="Path(s) to files to validate"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output with debug information"
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.debug(f"Validating {len(args.files)} file(s)...")

    all_valid = True
    error_occurred = False

    for file_path in args.files:
        path = Path(file_path)
        is_valid, issues = validate_item(path)

        if not is_valid:
            # Determine if it's a validation failure or an error
            error_issues = ["File not found", "Permission denied", "Unexpected error", "Not a file"]
            if any(any(err in issue for err in error_issues) for issue in issues):
                error_occurred = True
            all_valid = False

    # Print summary
    print()
    if error_occurred:
        logger.error("Validation completed with errors")
        sys.exit(2)
    elif not all_valid:
        logger.warning("Validation completed with failures")
        sys.exit(1)
    else:
        logger.info("✅ All validations passed")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nValidation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(2)
