#!/usr/bin/env python3
"""
GB Studio Audio File Validator
Validates music and sound files meet GB Studio requirements.

GB Studio Audio Requirements:
- Music: .mod, .uge formats
- Sound Effects: .wav, .vgm formats
- WAV: Mono, 8-bit or 16-bit, various sample rates supported
- File size: Reasonable limits for GB hardware
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Tuple, List
import wave
import struct

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Audio constants
SUPPORTED_MUSIC_FORMATS = ['.mod', '.uge']
SUPPORTED_SOUND_FORMATS = ['.wav', '.vgm', '.sav']
MAX_FILE_SIZE_MB = 10  # Reasonable limit
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def validate_wav_file(path: str) -> Tuple[bool, List[str]]:
    """Validate WAV file properties."""
    issues = []

    try:
        with wave.open(path, 'rb') as wav:
            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            framerate = wav.getframerate()
            n_frames = wav.getnframes()

            # Check mono/stereo (GB is mono but can accept stereo)
            if channels > 2:
                issues.append(f"Too many channels: {channels} (GB supports mono or stereo)")

            # Check sample width
            if sample_width not in [1, 2]:
                issues.append(
                    f"Invalid sample width: {sample_width} bytes "
                    f"(supported: 1=8-bit, 2=16-bit)"
                )

            # Info logging
            duration = n_frames / float(framerate)
            logger.debug(
                f"WAV: {channels}ch, {sample_width*8}bit, {framerate}Hz, "
                f"{duration:.2f}s"
            )

    except wave.Error as e:
        issues.append(f"Invalid WAV file: {e}")
    except Exception as e:
        issues.append(f"Error reading WAV: {e}")

    return len(issues) == 0, issues


def validate_audio_file(path: str) -> Tuple[bool, List[str]]:
    """
    Validate a single audio file.

    Args:
        path: Path to the audio file

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

        # Check file format
        all_formats = SUPPORTED_MUSIC_FORMATS + SUPPORTED_SOUND_FORMATS
        if file_ext not in all_formats:
            issues.append(
                f"Unsupported format: {file_ext} "
                f"(supported: {', '.join(all_formats)})"
            )
            return False, issues

        # Check file size
        if file_size > MAX_FILE_SIZE_BYTES:
            size_mb = file_size / (1024 * 1024)
            issues.append(
                f"File too large: {size_mb:.2f}MB (limit: {MAX_FILE_SIZE_MB}MB)"
            )

        if file_size == 0:
            issues.append("File is empty (0 bytes)")
            return False, issues

        # Format-specific validation
        if file_ext == '.wav':
            wav_valid, wav_issues = validate_wav_file(path)
            if not wav_valid:
                issues.extend(wav_issues)

        # Determine file type for logging
        if file_ext in SUPPORTED_MUSIC_FORMATS:
            file_type = "music"
        else:
            file_type = "sound effect"

        # Log results
        if issues:
            logger.warning(f"{basename}: {len(issues)} issue(s) found")
            for issue in issues:
                logger.warning(f"  ❌ {issue}")
            return False, issues
        else:
            size_kb = file_size / 1024
            logger.info(f"✅ {basename}: OK ({file_type}, {size_kb:.1f}KB)")
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
        description="Validate GB Studio audio files (music and sound effects)",
        epilog="Exit codes: 0=success, 1=validation failure, 2=error, 130=cancelled"
    )
    parser.add_argument(
        "files",
        nargs='+',
        help="Path(s) to audio files (.mod, .uge, .wav, .vgm)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output with debug information"
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.info(f"Validating {len(args.files)} audio file(s)...")

    all_valid = True
    error_occurred = False

    for file_path in args.files:
        is_valid, issues = validate_audio_file(file_path)

        if not is_valid:
            # Determine if it's a validation failure or an error
            error_issues = ["File not found", "Permission denied", "Unexpected error"]
            if any(any(err in issue for err in error_issues) for issue in issues):
                error_occurred = True
            all_valid = False

    # Print summary
    print()
    if error_occurred:
        logger.error("Audio validation completed with errors")
        sys.exit(2)
    elif not all_valid:
        logger.warning("Audio validation completed with failures")
        sys.exit(1)
    else:
        logger.info("✅ All audio files validated successfully")
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
