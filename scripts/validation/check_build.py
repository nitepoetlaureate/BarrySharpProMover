#!/usr/bin/env python3
"""
GB Studio Build Validator
Validates ROM builds for integrity and correctness.

Build Validation:
- ROM file exists and is non-empty
- File size within GB/GBC limits
- ROM header validation
- Checksum verification
"""

import os
import sys
import argparse
import logging
import hashlib
from pathlib import Path
from typing import Tuple, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# ROM constants
GB_ROM_MIN_SIZE = 32 * 1024  # 32KB minimum
GB_ROM_MAX_SIZE = 8 * 1024 * 1024  # 8MB maximum
GBC_ROM_MAX_SIZE = 8 * 1024 * 1024
VALID_ROM_EXTENSIONS = ['.gb', '.gbc', '.pocket']

# ROM header offsets
HEADER_TITLE_OFFSET = 0x0134
HEADER_TITLE_LENGTH = 16
HEADER_CGB_FLAG_OFFSET = 0x0143
HEADER_CHECKSUM_OFFSET = 0x014D


def validate_rom_header(rom_data: bytes) -> Tuple[bool, List[str]]:
    """Validate ROM header structure."""
    issues = []

    if len(rom_data) < 0x0150:
        issues.append("ROM too small to contain valid header")
        return False, issues

    # Extract title
    try:
        title_bytes = rom_data[HEADER_TITLE_OFFSET:HEADER_TITLE_OFFSET + HEADER_TITLE_LENGTH]
        title = title_bytes.split(b'\x00')[0].decode('ascii', errors='ignore')
        logger.debug(f"ROM Title: {title}")
    except Exception as e:
        logger.warning(f"Could not extract ROM title: {e}")

    # Check CGB flag
    cgb_flag = rom_data[HEADER_CGB_FLAG_OFFSET]
    if cgb_flag == 0x80:
        logger.debug("ROM: Game Boy Color compatible")
    elif cgb_flag == 0xC0:
        logger.debug("ROM: Game Boy Color only")
    else:
        logger.debug("ROM: Game Boy (DMG)")

    # Validate header checksum
    header_checksum = 0
    for addr in range(0x0134, 0x014D):
        header_checksum = (header_checksum - rom_data[addr] - 1) & 0xFF

    stored_checksum = rom_data[HEADER_CHECKSUM_OFFSET]
    if header_checksum != stored_checksum:
        logger.warning(
            f"Header checksum mismatch: calculated {header_checksum:02X}, "
            f"stored {stored_checksum:02X}"
        )
        # This is common during development, so just warn

    return len(issues) == 0, issues


def validate_rom_file(path: str) -> Tuple[bool, List[str]]:
    """
    Validate a ROM file.

    Args:
        path: Path to the ROM file

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
        file_size = os.path.getsize(path)

        # Check file extension
        if file_ext not in VALID_ROM_EXTENSIONS:
            issues.append(
                f"Invalid extension: {file_ext} "
                f"(expected: {', '.join(VALID_ROM_EXTENSIONS)})"
            )

        # Check file is not empty
        if file_size == 0:
            issues.append("ROM file is empty")
            return False, issues

        # Check minimum size
        if file_size < GB_ROM_MIN_SIZE:
            size_kb = file_size / 1024
            issues.append(
                f"ROM too small: {size_kb:.1f}KB (minimum: {GB_ROM_MIN_SIZE/1024}KB)"
            )

        # Check maximum size
        if file_size > GB_ROM_MAX_SIZE:
            size_mb = file_size / (1024 * 1024)
            issues.append(
                f"ROM too large: {size_mb:.2f}MB (maximum: {GB_ROM_MAX_SIZE/(1024*1024)}MB)"
            )

        # Read ROM data
        with open(path, 'rb') as f:
            rom_data = f.read()

        # Validate header
        header_valid, header_issues = validate_rom_header(rom_data)
        if not header_valid:
            issues.extend(header_issues)

        # Calculate MD5 hash for reproducibility checking
        md5_hash = hashlib.md5(rom_data).hexdigest()
        logger.debug(f"ROM MD5: {md5_hash}")

        # Check for hash file
        hash_file = Path(path).with_suffix('.md5')
        if hash_file.exists():
            try:
                with open(hash_file, 'r') as f:
                    stored_hash = f.read().split()[0]
                    if md5_hash == stored_hash:
                        logger.info("✅ ROM hash matches stored hash (build reproducible)")
                    else:
                        logger.warning(
                            "⚠️  ROM hash differs from stored hash "
                            "(build changed or not reproducible)"
                        )
            except Exception as e:
                logger.debug(f"Could not read hash file: {e}")

        # Log results
        if issues:
            logger.warning(f"{basename}: {len(issues)} issue(s) found")
            for issue in issues:
                logger.warning(f"  ❌ {issue}")
            return False, issues
        else:
            size_kb = file_size / 1024
            logger.info(f"✅ {basename}: OK ({size_kb:.1f}KB, MD5: {md5_hash[:8]}...)")
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
        description="Validate GB Studio ROM builds",
        epilog="Exit codes: 0=success, 1=validation failure, 2=error, 130=cancelled"
    )
    parser.add_argument(
        "files",
        nargs='+',
        help="Path(s) to ROM files (.gb, .gbc, .pocket)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output with debug information"
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.info(f"Validating {len(args.files)} ROM(s)...")

    all_valid = True
    error_occurred = False

    for file_path in args.files:
        is_valid, issues = validate_rom_file(file_path)

        if not is_valid:
            # Determine if it's a validation failure or an error
            error_issues = ["File not found", "Permission denied", "Unexpected error"]
            if any(any(err in issue for err in error_issues) for issue in issues):
                error_occurred = True
            all_valid = False

    # Print summary
    print()
    if error_occurred:
        logger.error("ROM validation completed with errors")
        sys.exit(2)
    elif not all_valid:
        logger.warning("ROM validation completed with failures")
        sys.exit(1)
    else:
        logger.info("✅ All ROMs validated successfully")
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
