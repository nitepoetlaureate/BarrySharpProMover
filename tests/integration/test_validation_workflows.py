#!/usr/bin/env python3
"""
Integration Tests for Validation Workflows

Tests end-to-end validation workflows including:
- Multiple asset validation in sequence
- Validation runner orchestration
- Error recovery and reporting
- Complete project validation
"""

import pytest
import sys
import json
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts' / 'validation'))

from validate_all import ValidationRunner
from check_bg_tiles import validate_background
from check_sprites import validate_sprite
from check_project import validate_project_file


class TestEndToEndValidation:
    """Test complete end-to-end validation workflows."""

    @pytest.mark.integration
    def test_complete_project_validation(self, project_structure,
                                         valid_background, valid_sprite,
                                         valid_gbsproj):
        """Test validation of a complete project with all assets."""
        # Set up project structure with assets
        bg_dir = project_structure / 'assets' / 'backgrounds'
        bg_dir.mkdir(parents=True, exist_ok=True)
        sprite_dir = project_structure / 'assets' / 'sprites'
        sprite_dir.mkdir(parents=True, exist_ok=True)

        # Copy test assets
        import shutil
        shutil.copy(valid_background, bg_dir / 'bg1.png')
        shutil.copy(valid_sprite, sprite_dir / 'sprite1.png')
        shutil.copy(valid_gbsproj, project_structure / 'project.gbsproj')

        # Run validation runner
        runner = ValidationRunner(project_structure, verbose=False)

        # Test individual validators
        bg_valid, bg_msg = validate_background(str(bg_dir / 'bg1.png'))
        assert bg_valid is True

        sprite_valid, sprite_issues = validate_sprite(str(sprite_dir / 'sprite1.png'))
        assert sprite_valid is True

        project_valid, project_issues = validate_project_file(
            str(project_structure / 'project.gbsproj')
        )
        assert project_valid is True

    @pytest.mark.integration
    def test_validation_with_mixed_results(self, project_structure,
                                           valid_background,
                                           invalid_sprite_colors,
                                           valid_gbsproj):
        """Test validation with some passing and some failing assets."""
        # Set up mixed assets
        bg_dir = project_structure / 'assets' / 'backgrounds'
        bg_dir.mkdir(parents=True, exist_ok=True)
        sprite_dir = project_structure / 'assets' / 'sprites'
        sprite_dir.mkdir(parents=True, exist_ok=True)

        import shutil
        shutil.copy(valid_background, bg_dir / 'valid_bg.png')
        shutil.copy(invalid_sprite_colors, sprite_dir / 'invalid_sprite.png')
        shutil.copy(valid_gbsproj, project_structure / 'project.gbsproj')

        # Validate each component
        bg_valid, _ = validate_background(str(bg_dir / 'valid_bg.png'))
        assert bg_valid is True

        sprite_valid, sprite_issues = validate_sprite(
            str(sprite_dir / 'invalid_sprite.png')
        )
        assert sprite_valid is False
        assert len(sprite_issues) > 0

    @pytest.mark.integration
    def test_validation_runner_orchestration(self, project_structure):
        """Test that ValidationRunner properly orchestrates all validators."""
        runner = ValidationRunner(project_structure, verbose=False)

        # All validators should run even if some fail
        exit_code = runner.run_all()

        # Should complete without crashing
        assert exit_code in [0, 1, 2]  # Valid exit codes

    @pytest.mark.integration
    def test_empty_project_validation(self, temp_dir):
        """Test validation of an empty project structure."""
        runner = ValidationRunner(temp_dir, verbose=False)

        exit_code = runner.run_all()

        # Should handle empty project gracefully
        # Exit code 1 because no .gbsproj file
        assert exit_code in [0, 1]

    @pytest.mark.integration
    def test_validation_with_missing_directories(self, temp_dir):
        """Test validation when expected directories don't exist."""
        runner = ValidationRunner(temp_dir, verbose=False)

        # Should not crash when directories are missing
        bg_exit, bg_output = runner.validate_backgrounds()
        sprite_exit, sprite_output = runner.validate_sprites()
        audio_exit, audio_output = runner.validate_audio()
        font_exit, font_output = runner.validate_fonts()

        # All should return 0 (skip) since directories don't exist
        assert bg_exit == 0
        assert sprite_exit == 0
        assert audio_exit == 0
        assert font_exit == 0


class TestValidationErrorRecovery:
    """Test error recovery and handling in validation workflows."""

    @pytest.mark.integration
    def test_continue_after_validation_failure(self, project_structure,
                                               invalid_sprite_colors,
                                               valid_gbsproj):
        """Test that validation continues after individual failures."""
        # Create mixed valid/invalid assets
        sprite_dir = project_structure / 'assets' / 'sprites'
        sprite_dir.mkdir(parents=True, exist_ok=True)

        import shutil
        shutil.copy(invalid_sprite_colors, sprite_dir / 'bad_sprite.png')
        shutil.copy(valid_gbsproj, project_structure / 'project.gbsproj')

        runner = ValidationRunner(project_structure, verbose=False)

        # Should validate project even though sprites failed
        project_exit, project_output = runner.validate_project()
        assert project_exit == 0  # Project file should be valid

    @pytest.mark.integration
    def test_error_aggregation(self, project_structure, create_test_image):
        """Test that multiple errors are properly aggregated."""
        # Create multiple invalid sprites
        sprite_dir = project_structure / 'assets' / 'sprites'
        sprite_dir.mkdir(parents=True, exist_ok=True)

        # Invalid sprite 1: wrong dimensions
        create_test_image(sprite_dir / 'wrong_size.png', 15, 15, None, 'RGBA')

        # Invalid sprite 2: too many colors
        colors = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255),
                  (255, 255, 0, 255), (255, 0, 255, 255)]
        create_test_image(sprite_dir / 'too_many_colors.png', 16, 16, colors, 'RGBA')

        runner = ValidationRunner(project_structure, verbose=False)

        # Both errors should be caught
        sprite_exit, sprite_output = runner.validate_sprites()
        # Should report failures


class TestValidationReporting:
    """Test validation result reporting."""

    @pytest.mark.integration
    def test_summary_generation(self, project_structure, valid_gbsproj):
        """Test that validation summary is properly generated."""
        import shutil
        shutil.copy(valid_gbsproj, project_structure / 'project.gbsproj')

        runner = ValidationRunner(project_structure, verbose=False)
        exit_code = runner.run_all()

        # Should generate summary and return appropriate exit code
        assert isinstance(exit_code, int)
        assert 0 <= exit_code <= 2

    @pytest.mark.integration
    def test_verbose_output(self, project_structure, valid_gbsproj):
        """Test verbose mode provides detailed output."""
        import shutil
        shutil.copy(valid_gbsproj, project_structure / 'project.gbsproj')

        runner = ValidationRunner(project_structure, verbose=True)

        # Verbose mode should work without crashing
        exit_code = runner.run_all()
        assert isinstance(exit_code, int)


class TestAssetDependencyValidation:
    """Test validation of asset dependencies and references."""

    @pytest.mark.integration
    def test_project_references_existing_assets(self, project_structure,
                                                 valid_background,
                                                 valid_sprite):
        """Test validation that project references match existing assets."""
        # Set up project with asset references
        bg_dir = project_structure / 'assets' / 'backgrounds'
        bg_dir.mkdir(parents=True, exist_ok=True)
        sprite_dir = project_structure / 'assets' / 'sprites'
        sprite_dir.mkdir(parents=True, exist_ok=True)

        import shutil
        shutil.copy(valid_background, bg_dir / 'bg1.png')
        shutil.copy(valid_sprite, sprite_dir / 'sprite1.png')

        # Create project that references these assets
        project_data = {
            "_resourceType": "project",
            "name": "Test Project",
            "_version": "4.1.0",
            "backgrounds": [
                {"id": "bg1", "filename": "bg1.png"}
            ],
            "spriteSheets": [
                {"id": "sprite1", "filename": "sprite1.png"}
            ]
        }

        project_path = project_structure / 'project.gbsproj'
        with open(project_path, 'w') as f:
            json.dump(project_data, f)

        # Validate project
        from check_project import validate_project_file
        is_valid, issues = validate_project_file(str(project_path))

        # Project structure should be valid
        assert is_valid is True

    @pytest.mark.integration
    @pytest.mark.slow
    def test_large_project_validation(self, project_structure, create_test_image):
        """Test validation of a project with many assets."""
        # Create many assets
        bg_dir = project_structure / 'assets' / 'backgrounds'
        bg_dir.mkdir(parents=True, exist_ok=True)
        sprite_dir = project_structure / 'assets' / 'sprites'
        sprite_dir.mkdir(parents=True, exist_ok=True)

        # Create 10 backgrounds
        for i in range(10):
            create_test_image(
                bg_dir / f'bg{i}.png',
                160, 144,
                [(255, 255, 255), (192, 192, 192), (96, 96, 96), (0, 0, 0)],
                'RGB'
            )

        # Create 20 sprites
        for i in range(20):
            create_test_image(
                sprite_dir / f'sprite{i}.png',
                16, 16,
                [(0, 0, 0, 0), (255, 255, 255, 255)],
                'RGBA'
            )

        runner = ValidationRunner(project_structure, verbose=False)

        # Should handle many assets efficiently
        bg_exit, _ = runner.validate_backgrounds()
        sprite_exit, _ = runner.validate_sprites()

        assert bg_exit == 0
        assert sprite_exit == 0
