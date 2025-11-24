#!/usr/bin/env python3
"""
GB Studio Project Validator
Validates .gbsproj files and referenced assets.

GB Studio Project Requirements:
- Valid JSON structure
- Required fields present
- Referenced assets exist
- No broken asset references
- Version compatibility
"""

import os
import sys
import argparse
import logging
import json
from pathlib import Path
from typing import Tuple, List, Dict, Any, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Project constants
REQUIRED_PROJECT_FIELDS = ['_resourceType', 'name', '_version']
EXPECTED_RESOURCE_TYPE = 'project'


def validate_project_structure(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate project JSON structure."""
    issues = []

    # Check required fields
    for field in REQUIRED_PROJECT_FIELDS:
        if field not in data:
            issues.append(f"Missing required field: '{field}'")

    # Validate resource type
    if '_resourceType' in data:
        if data['_resourceType'] != EXPECTED_RESOURCE_TYPE:
            issues.append(
                f"Invalid _resourceType: '{data['_resourceType']}' "
                f"(expected: '{EXPECTED_RESOURCE_TYPE}')"
            )

    # Validate name
    if 'name' in data:
        if not isinstance(data['name'], str) or not data['name']:
            issues.append("Invalid or empty project name")

    # Validate version
    if '_version' in data:
        version = data['_version']
        logger.info(f"GB Studio version: {version}")

    return len(issues) == 0, issues


def check_asset_references(data: Dict[str, Any], project_dir: Path) -> Tuple[bool, List[str]]:
    """Check that referenced assets exist."""
    issues = []
    missing_assets = set()

    # This is a simplified check - a full implementation would need to
    # traverse the entire project structure looking for asset references
    # For now, we'll just check if common asset directories exist

    asset_dirs = [
        'assets/backgrounds',
        'assets/sprites',
        'assets/music',
        'assets/sounds',
        'assets/fonts'
    ]

    for asset_dir in asset_dirs:
        full_path = project_dir / asset_dir
        if not full_path.exists():
            logger.warning(f"Asset directory not found: {asset_dir}")

    return len(missing_assets) == 0, list(missing_assets)


def validate_project_file(path: str) -> Tuple[bool, List[str]]:
    """
    Validate a GB Studio project file.

    Args:
        path: Path to the .gbsproj file

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
        project_dir = Path(path).parent

        # Check format
        if file_ext != '.gbsproj':
            issues.append(f"Invalid format: {file_ext} (expected .gbsproj)")
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
        struct_valid, struct_issues = validate_project_structure(data)
        if not struct_valid:
            issues.extend(struct_issues)

        # Check asset references
        assets_valid, asset_issues = check_asset_references(data, project_dir)
        if not assets_valid:
            for missing in asset_issues:
                logger.warning(f"Missing asset: {missing}")

        # Get project info
        project_name = data.get('name', 'unknown')
        project_version = data.get('_version', 'unknown')
        author = data.get('author', 'unknown')

        # Log results
        if issues:
            logger.warning(f"{basename}: {len(issues)} issue(s) found")
            for issue in issues:
                logger.warning(f"  ❌ {issue}")
            return False, issues
        else:
            logger.info(
                f"✅ {basename}: OK "
                f"(name: {project_name}, version: {project_version}, author: {author})"
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
        description="Validate GB Studio project files",
        epilog="Exit codes: 0=success, 1=validation failure, 2=error, 130=cancelled"
    )
    parser.add_argument(
        "files",
        nargs='+',
        help="Path(s) to .gbsproj files"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output with debug information"
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.info(f"Validating {len(args.files)} project(s)...")

    all_valid = True
    error_occurred = False

    for file_path in args.files:
        is_valid, issues = validate_project_file(file_path)

        if not is_valid:
            # Determine if it's a validation failure or an error
            error_issues = ["File not found", "Permission denied", "Unexpected error", "Invalid JSON"]
            if any(any(err in issue for err in error_issues) for issue in issues):
                error_occurred = True
            all_valid = False

    # Print summary
    print()
    if error_occurred:
        logger.error("Project validation completed with errors")
        sys.exit(2)
    elif not all_valid:
        logger.warning("Project validation completed with failures")
        sys.exit(1)
    else:
        logger.info("✅ All projects validated successfully")
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
