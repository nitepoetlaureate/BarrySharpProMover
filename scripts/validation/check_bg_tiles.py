#!/usr/bin/env python3
"""
GB Studio Background Tile Validator
Validates that background images meet GB Studio tile count limits.
"""

from PIL import Image
import sys
import os
import argparse
import logging
from pathlib import Path
from typing import Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

TILE_SIZE = 8
MAX_TILES = 192
EXPECTED_WIDTH = 160
EXPECTED_HEIGHT = 144


def get_tiles(image: Image.Image) -> set:
    """Extract unique tiles from an image."""
    tiles = set()
    width, height = image.size
    for y in range(0, height, TILE_SIZE):
        for x in range(0, width, TILE_SIZE):
            tile = image.crop((x, y, x + TILE_SIZE, y + TILE_SIZE))
            tiles.add(tile.tobytes())
    return tiles


def validate_background(path: str) -> Tuple[bool, str]:
    """
    Validate a single background image.

    Args:
        path: Path to the PNG file

    Returns:
        Tuple of (is_valid, message)
    """
    try:
        # Check file exists
        if not os.path.isfile(path):
            logger.error(f"File not found: {path}")
            return False, f"File not found: {path}"

        # Load image
        try:
            img = Image.open(path)
        except Exception as e:
            logger.error(f"Failed to open image {path}: {e}")
            return False, f"Invalid image file: {e}"

        # Get dimensions
        width, height = img.size
        basename = os.path.basename(path)

        # Check dimensions
        if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
            logger.warning(
                f"{basename}: Size is {width}x{height}, expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
            )

        # Count unique tiles
        try:
            tiles = get_tiles(img)
            tile_count = len(tiles)
        except Exception as e:
            logger.error(f"Failed to count tiles in {basename}: {e}")
            return False, f"Tile counting error: {e}"

        # Validate tile count
        if tile_count > MAX_TILES:
            logger.error(f"{basename}: {tile_count} tiles (limit is {MAX_TILES})")
            return False, f"{tile_count} tiles exceeds limit of {MAX_TILES}"
        else:
            logger.info(f"{basename}: {tile_count} tiles OK")
            return True, f"{tile_count} tiles"

    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        return False, "File not found"
    except PermissionError:
        logger.error(f"Permission denied: {path}")
        return False, "Permission denied"
    except Exception as e:
        logger.error(f"Unexpected error processing {path}: {e}")
        return False, f"Unexpected error: {e}"


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check GB Studio background tile counts",
        epilog="Exit codes: 0=success, 1=validation failure, 2=error"
    )
    parser.add_argument("files", nargs='+', help="Path(s) to PNG files")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    all_valid = True
    error_occurred = False

    for path in args.files:
        is_valid, message = validate_background(path)
        if not is_valid:
            # Check if it's a validation failure or an error
            if "File not found" in message or "error" in message.lower():
                error_occurred = True
            all_valid = False

    # Exit with appropriate code
    if error_occurred:
        sys.exit(2)  # Error occurred
    elif not all_valid:
        sys.exit(1)  # Validation failure
    else:
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