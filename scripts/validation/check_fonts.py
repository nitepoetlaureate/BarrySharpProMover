#!/usr/bin/env python3
"""
GB Studio Font Validator
Validates font files meet GB Studio requirements.

GB Studio Font Requirements:
- Format: JSON with specific structure
- Glyphs must reference valid image data
- Character mappings must be complete
"""

import os
import sys
import argparse
import logging
import json
from pathlib import Path
from typing import Tuple, List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Font constants
REQUIRED_FONT_FIELDS = ['id', 'name', 'mapping']
COMMON_ASCII_RANGE = range(32, 127)  # Printable ASCII


def validate_font_structure(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate font JSON structure."""
    issues = []

    # Check required fields
    for field in REQUIRED_FONT_FIELDS:
        if field not in data:
            issues.append(f"Missing required field: '{field}'")

    # Validate ID
    if 'id' in data:
        if not isinstance(data['id'], str) or not data['id']:
            issues.append("Invalid or empty 'id' field")

    # Validate name
    if 'name' in data:
        if not isinstance(data['name'], str) or not data['name']:
            issues.append("Invalid or empty 'name' field")

    # Validate mapping
    if 'mapping' in data:
        if not isinstance(data['mapping'], dict):
            issues.append("'mapping' field must be a dictionary")
        else:
            # Check that mapping has some characters
            if len(data['mapping']) == 0:
                issues.append("Font mapping is empty (no characters defined)")

            # Check for common ASCII characters
            mapped_chars = set(data['mapping'].keys())
            missing_common = []
            for code in COMMON_ASCII_RANGE:
                char = chr(code)
                if char not in mapped_chars:
                    missing_common.append(char)

            if missing_common and len(missing_common) > 20:
                logger.warning(
                    f"Font missing {len(missing_common)} common ASCII characters"
                )

    return len(issues) == 0, issues


def validate_font_file(path: str) -> Tuple[bool, List[str]]:
    """
    Validate a single font JSON file.

    Args:
        path: Path to the font JSON file

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    try:
        # Check file exists
        if not os.path.isfile(path):
            logger.error(f"File not found: {path}")
            return False, ["File not found"]

        basename = os.path.basename(path)
        file_ext = Path(path).suffix.lower()

        # Check format
        if file_ext != '.json':
            issues.append(f"Invalid format: {file_ext} (expected .json)")
            return False, issues

        # Load and parse JSON
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {path}: {e}")
            return False, [f"Invalid JSON: {e}"]
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error in {path}: {e}")
            return False, [f"Encoding error: {e}"]

        # Validate structure
        struct_valid, struct_issues = validate_font_structure(data)
        if not struct_valid:
            issues.extend(struct_issues)

        # Get font info
        font_id = data.get('id', 'unknown')
        font_name = data.get('name', 'unknown')
        char_count = len(data.get('mapping', {}))

        # Log results
        if issues:
            logger.warning(f"{basename}: {len(issues)} issue(s) found")
            for issue in issues:
                logger.warning(f"  ❌ {issue}")
            return False, issues
        else:
            logger.info(
                f"✅ {basename}: OK "
                f"(id: {font_id}, name: {font_name}, {char_count} characters)"
            )
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
        description="Validate GB Studio font files",
        epilog="Exit codes: 0=success, 1=validation failure, 2=error, 130=cancelled"
    )
    parser.add_argument(
        "files",
        nargs='+',
        help="Path(s) to font JSON files"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output with debug information"
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.info(f"Validating {len(args.files)} font(s)...")

    all_valid = True
    error_occurred = False

    for file_path in args.files:
        is_valid, issues = validate_font_file(file_path)

        if not is_valid:
            # Determine if it's a validation failure or an error
            error_issues = ["File not found", "Permission denied", "Unexpected error", "Invalid JSON"]
            if any(any(err in issue for err in error_issues) for issue in issues):
                error_occurred = True
            all_valid = False

    # Print summary
    print()
    if error_occurred:
        logger.error("Font validation completed with errors")
        sys.exit(2)
    elif not all_valid:
        logger.warning("Font validation completed with failures")
        sys.exit(1)
    else:
        logger.info("✅ All fonts validated successfully")
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
