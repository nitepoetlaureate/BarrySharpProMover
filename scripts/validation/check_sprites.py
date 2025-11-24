#!/usr/bin/env python3
"""
GB Studio Sprite Validator
Validates sprite images meet GB Studio requirements.

GB Studio Sprite Requirements:
- Format: PNG with transparency
- Dimensions: 8x8 or 16x16 pixels (or multiples for animation frames)
- Colors: Maximum 4 colors per sprite (including transparency)
- Animation frames must be consistent sizes
"""

from PIL import Image
import sys
import os
import argparse
import logging
from pathlib import Path
from typing import Tuple, List, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Sprite constants
VALID_TILE_SIZES = [8, 16]  # 8x8 or 16x16
MAX_COLORS = 4  # Including transparency
EXPECTED_FORMAT = 'PNG'


def get_unique_colors(image: Image.Image) -> Set[tuple]:
    """Get unique colors from image."""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    colors = set()
    pixels = image.getdata()
    for pixel in pixels:
        colors.add(pixel)

    return colors


def validate_sprite(path: str) -> Tuple[bool, List[str]]:
    """
    Validate a single sprite image.

    Args:
        path: Path to the PNG file

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    try:
        # Check file exists
        if not os.path.isfile(path):
            logger.error(f"File not found: {path}")
            return False, ["File not found"]

        # Load image
        try:
            img = Image.open(path)
        except Exception as e:
            logger.error(f"Failed to open image {path}: {e}")
            return False, [f"Invalid image file: {e}"]

        basename = os.path.basename(path)
        width, height = img.size

        # Check format
        if img.format != EXPECTED_FORMAT:
            issues.append(f"Invalid format: {img.format} (expected PNG)")

        # Check dimensions (should be multiples of valid tile sizes)
        valid_width = any(width % size == 0 for size in VALID_TILE_SIZES)
        valid_height = any(height % size == 0 for size in VALID_TILE_SIZES)

        if not valid_width or not valid_height:
            issues.append(
                f"Invalid dimensions: {width}x{height} "
                f"(must be multiples of 8 or 16)"
            )

        # Check if sprite is too small
        if width < 8 or height < 8:
            issues.append(f"Sprite too small: {width}x{height} (minimum 8x8)")

        # Warn if very large (likely not a sprite)
        if width > 64 or height > 64:
            logger.warning(
                f"{basename}: Large sprite {width}x{height} "
                f"(are you sure this is a sprite and not a background?)"
            )

        # Check color count
        try:
            colors = get_unique_colors(img)
            color_count = len(colors)

            if color_count > MAX_COLORS:
                issues.append(
                    f"Too many colors: {color_count} (limit: {MAX_COLORS} including transparency)"
                )
            else:
                logger.debug(f"{basename}: {color_count} colors (OK)")
        except Exception as e:
            logger.warning(f"Could not count colors in {basename}: {e}")

        # Check for transparency
        if img.mode not in ['RGBA', 'LA', 'P']:
            logger.warning(f"{basename}: No alpha channel detected")

        # Log results
        if issues:
            logger.warning(f"{basename}: {len(issues)} issue(s) found")
            for issue in issues:
                logger.warning(f"  ❌ {issue}")
            return False, issues
        else:
            logger.info(
                f"✅ {basename}: OK "
                f"({width}x{height}, {color_count} colors)"
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
        description="Validate GB Studio sprite images",
        epilog="Exit codes: 0=success, 1=validation failure, 2=error, 130=cancelled"
    )
    parser.add_argument(
        "files",
        nargs='+',
        help="Path(s) to sprite PNG files"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output with debug information"
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.info(f"Validating {len(args.files)} sprite(s)...")

    all_valid = True
    error_occurred = False

    for file_path in args.files:
        is_valid, issues = validate_sprite(file_path)

        if not is_valid:
            # Determine if it's a validation failure or an error
            error_issues = ["File not found", "Permission denied", "Unexpected error", "Invalid image"]
            if any(any(err in issue for err in error_issues) for issue in issues):
                error_occurred = True
            all_valid = False

    # Print summary
    print()
    if error_occurred:
        logger.error("Sprite validation completed with errors")
        sys.exit(2)
    elif not all_valid:
        logger.warning("Sprite validation completed with failures")
        sys.exit(1)
    else:
        logger.info("✅ All sprites validated successfully")
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
