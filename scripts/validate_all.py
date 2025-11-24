#!/usr/bin/env python3
"""
Comprehensive Validation Runner
Runs all validation scripts for the BarrySharpProMover project.

This script orchestrates all validators to provide complete project validation.
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class ValidationRunner:
    """Orchestrates running all validation scripts."""

    def __init__(self, project_root: Path, verbose: bool = False):
        self.project_root = project_root
        self.verbose = verbose
        self.results: Dict[str, Tuple[int, str]] = {}

    def run_validator(self, name: str, script: str, args: List[str]) -> Tuple[int, str]:
        """Run a single validation script."""
        script_path = self.project_root / 'scripts' / 'validation' / script

        if not script_path.exists():
            logger.warning(f"⚠️  {name}: Script not found: {script}")
            return 2, f"Script not found: {script}"

        cmd = ['python3', str(script_path)] + args
        if self.verbose:
            cmd.append('-v')

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            return result.returncode, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            return 2, f"Validation timed out after 60s"
        except Exception as e:
            return 2, f"Error running validator: {e}"

    def validate_backgrounds(self) -> Tuple[int, str]:
        """Validate background images."""
        bg_path = self.project_root / 'assets' / 'backgrounds'
        if not bg_path.exists():
            logger.info("⏭️  No backgrounds directory, skipping")
            return 0, "No backgrounds to validate"

        bg_files = list(bg_path.glob('*.png'))
        if not bg_files:
            logger.info("⏭️  No background PNG files found")
            return 0, "No backgrounds found"

        logger.info(f"🔍 Validating {len(bg_files)} background(s)...")
        return self.run_validator(
            "Backgrounds",
            "check_bg_tiles.py",
            [str(f) for f in bg_files]
        )

    def validate_sprites(self) -> Tuple[int, str]:
        """Validate sprite images."""
        sprite_path = self.project_root / 'assets' / 'sprites'
        if not sprite_path.exists():
            logger.info("⏭️  No sprites directory, skipping")
            return 0, "No sprites to validate"

        sprite_files = list(sprite_path.glob('*.png'))
        if not sprite_files:
            logger.info("⏭️  No sprite PNG files found")
            return 0, "No sprites found"

        logger.info(f"🔍 Validating {len(sprite_files)} sprite(s)...")
        return self.run_validator(
            "Sprites",
            "check_sprites.py",
            [str(f) for f in sprite_files]
        )

    def validate_audio(self) -> Tuple[int, str]:
        """Validate music and sound files."""
        music_path = self.project_root / 'assets' / 'music'
        sounds_path = self.project_root / 'assets' / 'sounds'

        audio_files = []
        if music_path.exists():
            audio_files.extend(music_path.glob('*.mod'))
            audio_files.extend(music_path.glob('*.uge'))
        if sounds_path.exists():
            audio_files.extend(sounds_path.glob('*.wav'))
            audio_files.extend(sounds_path.glob('*.vgm'))

        if not audio_files:
            logger.info("⏭️  No audio files found")
            return 0, "No audio to validate"

        logger.info(f"🔍 Validating {len(audio_files)} audio file(s)...")
        return self.run_validator(
            "Audio",
            "check_audio.py",
            [str(f) for f in audio_files]
        )

    def validate_fonts(self) -> Tuple[int, str]:
        """Validate font files."""
        font_path = self.project_root / 'assets' / 'fonts'
        if not font_path.exists():
            logger.info("⏭️  No fonts directory, skipping")
            return 0, "No fonts to validate"

        font_files = list(font_path.glob('*.json'))
        if not font_files:
            logger.info("⏭️  No font JSON files found")
            return 0, "No fonts found"

        logger.info(f"🔍 Validating {len(font_files)} font(s)...")
        return self.run_validator(
            "Fonts",
            "check_fonts.py",
            [str(f) for f in font_files]
        )

    def validate_scenes(self) -> Tuple[int, str]:
        """Validate scene files."""
        scene_path = self.project_root / 'project' / 'scenes'
        if not scene_path.exists():
            logger.info("⏭️  No scenes directory, skipping")
            return 0, "No scenes to validate"

        logger.info("🔍 Validating scenes...")
        return self.run_validator(
            "Scenes",
            "check_scene_limits.py",
            [str(scene_path)]
        )

    def validate_project(self) -> Tuple[int, str]:
        """Validate GB Studio project file."""
        project_files = list(self.project_root.glob('*.gbsproj'))
        if not project_files:
            logger.warning("⚠️  No .gbsproj file found")
            return 1, "No project file found"

        logger.info("🔍 Validating project file...")
        return self.run_validator(
            "Project",
            "check_project.py",
            [str(f) for f in project_files]
        )

    def validate_build(self) -> Tuple[int, str]:
        """Validate ROM builds."""
        build_path = self.project_root / 'build'
        if not build_path.exists():
            logger.info("⏭️  No build directory, skipping")
            return 0, "No builds to validate"

        rom_files = list(build_path.glob('*.gb'))
        if not rom_files:
            logger.info("⏭️  No ROM files found")
            return 0, "No ROM builds found"

        logger.info(f"🔍 Validating {len(rom_files)} ROM build(s)...")
        return self.run_validator(
            "Build",
            "check_build.py",
            [str(f) for f in rom_files]
        )

    def run_all(self) -> int:
        """Run all validations."""
        logger.info("=" * 60)
        logger.info("🚀 Running comprehensive validation...")
        logger.info("=" * 60)
        print()

        # Run all validators
        validators = [
            ("Project File", self.validate_project),
            ("Backgrounds", self.validate_backgrounds),
            ("Sprites", self.validate_sprites),
            ("Audio", self.validate_audio),
            ("Fonts", self.validate_fonts),
            ("Scenes", self.validate_scenes),
            ("ROM Builds", self.validate_build),
        ]

        results = {}
        for name, validator in validators:
            try:
                exit_code, output = validator()
                results[name] = (exit_code, output)

                if self.verbose and output:
                    print(output)

            except Exception as e:
                logger.error(f"❌ {name}: Validation failed with error: {e}")
                results[name] = (2, str(e))

            print()  # Spacing between validators

        # Print summary
        logger.info("=" * 60)
        logger.info("📊 Validation Summary")
        logger.info("=" * 60)

        passed = 0
        failed = 0
        errors = 0
        skipped = 0

        for name, (exit_code, _) in results.items():
            if exit_code == 0:
                logger.info(f"✅ {name}: PASSED")
                passed += 1
            elif exit_code == 1:
                logger.warning(f"❌ {name}: FAILED")
                failed += 1
            elif exit_code == 2:
                logger.error(f"⚠️  {name}: ERROR")
                errors += 1
            else:
                logger.info(f"⏭️  {name}: SKIPPED")
                skipped += 1

        print()
        logger.info(f"Results: {passed} passed, {failed} failed, {errors} errors, {skipped} skipped")

        # Determine overall exit code
        if errors > 0:
            return 2
        elif failed > 0:
            return 1
        else:
            logger.info("✅ All validations passed!")
            return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run all validation scripts for BarrySharpProMover project",
        epilog="Exit codes: 0=all passed, 1=validation failures, 2=errors"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output with detailed validation results"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)"
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Validate we're in a project directory
    if not (args.project_root / '*.gbsproj'):
        logger.warning("⚠️  No .gbsproj file found. Are you in the project root?")

    # Run all validations
    runner = ValidationRunner(args.project_root, args.verbose)
    exit_code = runner.run_all()

    sys.exit(exit_code)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nValidation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(2)
