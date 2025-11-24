#!/usr/bin/env python3
"""
GB Studio Scene Limit Validator
Validates that scenes meet GB Studio limits for actors, triggers, and sprites.
"""

import os
import json
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

MAX_ACTORS = 20
MAX_TRIGGERS = 30
MAX_SPRITE_TILES = 96


def validate_scene(path: str) -> Tuple[bool, List[str]]:
    """
    Validate a single scene JSON file.

    Args:
        path: Path to the scene JSON file

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    try:
        # Check file exists
        if not os.path.isfile(path):
            logger.error(f"File not found: {path}")
            return False, ["File not found"]

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

        basename = os.path.basename(path)

        # Extract scene data
        actor_count = len(data.get("actors", []))
        trigger_count = len(data.get("triggers", []))
        sprite_tiles = data.get("spriteTilesUsed", 0)

        # Check limits
        issues = []
        if actor_count > MAX_ACTORS:
            issues.append(f"❌ {actor_count} actors (limit: {MAX_ACTORS})")
        if trigger_count > MAX_TRIGGERS:
            issues.append(f"❌ {trigger_count} triggers (limit: {MAX_TRIGGERS})")
        if sprite_tiles > MAX_SPRITE_TILES:
            issues.append(f"❌ {sprite_tiles} sprite tiles (limit: {MAX_SPRITE_TILES})")

        # Log results
        if issues:
            logger.warning(f"{basename}: {len(issues)} limit(s) exceeded")
            for issue in issues:
                logger.warning(f"  {issue}")
            return False, issues
        else:
            logger.info(
                f"{basename}: All limits OK "
                f"(actors: {actor_count}, triggers: {trigger_count}, sprites: {sprite_tiles})"
            )
            return True, []

    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        return False, ["File not found"]
    except PermissionError:
        logger.error(f"Permission denied: {path}")
        return False, ["Permission denied"]
    except Exception as e:
        logger.error(f"Unexpected error processing {path}: {e}")
        return False, [f"Unexpected error: {e}"]


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check GB Studio scene limits",
        epilog="Exit codes: 0=success, 1=validation failure, 2=error"
    )
    parser.add_argument("scene_dir", help="Directory of scene JSON files")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Validate directory exists
    if not os.path.isdir(args.scene_dir):
        logger.error(f"Directory not found: {args.scene_dir}")
        sys.exit(2)

    # Find JSON files
    try:
        json_files = [
            os.path.join(args.scene_dir, f)
            for f in os.listdir(args.scene_dir)
            if f.endswith(".json")
        ]
    except PermissionError:
        logger.error(f"Permission denied accessing directory: {args.scene_dir}")
        sys.exit(2)
    except Exception as e:
        logger.error(f"Error reading directory {args.scene_dir}: {e}")
        sys.exit(2)

    if not json_files:
        logger.warning(f"No JSON files found in {args.scene_dir}")
        sys.exit(0)

    logger.info(f"Validating {len(json_files)} scene(s)...")

    all_valid = True
    error_occurred = False

    for json_file in json_files:
        is_valid, issues = validate_scene(json_file)
        if not is_valid:
            # Check if it's a validation failure or an error
            if any("error" in issue.lower() or "not found" in issue.lower() for issue in issues):
                error_occurred = True
            all_valid = False

    # Exit with appropriate code
    if error_occurred:
        sys.exit(2)  # Error occurred
    elif not all_valid:
        sys.exit(1)  # Validation failure
    else:
        logger.info("✅ All scenes validated successfully")
        sys.exit(0)  # Success


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nValidation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(2)