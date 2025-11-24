#!/usr/bin/env python3
"""
Unit Tests for validate_all.py

Tests comprehensive validation runner including:
- Running all validators
- Summary generation
- Exit code handling
- Error aggregation
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))

from validate_all import ValidationRunner


class TestValidationRunner:
    """Test ValidationRunner class."""

    @pytest.mark.unit
    def test_initialization(self, temp_dir):
        """Test ValidationRunner initialization."""
        runner = ValidationRunner(temp_dir, verbose=False)

        assert runner.project_root == temp_dir
        assert runner.verbose is False
        assert isinstance(runner.results, dict)

    @pytest.mark.unit
    def test_run_validator_success(self, temp_dir):
        """Test running a successful validator."""
        runner = ValidationRunner(temp_dir, verbose=False)

        # Create a simple test script that succeeds
        test_script = temp_dir / 'scripts' / 'validation' / 'test_success.py'
        test_script.parent.mkdir(parents=True, exist_ok=True)
        test_script.write_text("""#!/usr/bin/env python3
import sys
print("Validation passed")
sys.exit(0)
""")
        test_script.chmod(0o755)

        exit_code, output = runner.run_validator(
            "Test Success",
            "test_success.py",
            []
        )

        assert exit_code == 0
        assert "passed" in output.lower()

    @pytest.mark.unit
    def test_run_validator_failure(self, temp_dir):
        """Test running a failing validator."""
        runner = ValidationRunner(temp_dir, verbose=False)

        # Create a test script that fails
        test_script = temp_dir / 'scripts' / 'validation' / 'test_failure.py'
        test_script.parent.mkdir(parents=True, exist_ok=True)
        test_script.write_text("""#!/usr/bin/env python3
import sys
print("Validation failed")
sys.exit(1)
""")
        test_script.chmod(0o755)

        exit_code, output = runner.run_validator(
            "Test Failure",
            "test_failure.py",
            []
        )

        assert exit_code == 1
        assert "failed" in output.lower()

    @pytest.mark.unit
    def test_run_validator_script_not_found(self, temp_dir):
        """Test error handling when validator script doesn't exist."""
        runner = ValidationRunner(temp_dir, verbose=False)

        exit_code, output = runner.run_validator(
            "Missing Script",
            "nonexistent.py",
            []
        )

        assert exit_code == 2
        assert "not found" in output.lower()

    @pytest.mark.unit
    def test_validate_backgrounds_no_directory(self, temp_dir):
        """Test background validation when directory doesn't exist."""
        runner = ValidationRunner(temp_dir, verbose=False)

        exit_code, output = runner.validate_backgrounds()

        assert exit_code == 0
        assert "no backgrounds" in output.lower() or "skipping" in output.lower()

    @pytest.mark.unit
    def test_validate_backgrounds_no_files(self, project_structure):
        """Test background validation when directory is empty."""
        runner = ValidationRunner(project_structure, verbose=False)

        exit_code, output = runner.validate_backgrounds()

        assert exit_code == 0

    @pytest.mark.unit
    def test_validate_sprites_no_directory(self, temp_dir):
        """Test sprite validation when directory doesn't exist."""
        runner = ValidationRunner(temp_dir, verbose=False)

        exit_code, output = runner.validate_sprites()

        assert exit_code == 0

    @pytest.mark.unit
    def test_validate_project_no_file(self, temp_dir):
        """Test project validation when no .gbsproj file exists."""
        runner = ValidationRunner(temp_dir, verbose=False)

        exit_code, output = runner.validate_project()

        assert exit_code == 1
        assert "no project" in output.lower() or "not found" in output.lower()

    @pytest.mark.unit
    def test_run_all_returns_exit_code(self, temp_dir):
        """Test that run_all returns proper exit code."""
        runner = ValidationRunner(temp_dir, verbose=False)

        # Mock all validator methods to return success
        runner.validate_project = Mock(return_value=(0, "OK"))
        runner.validate_backgrounds = Mock(return_value=(0, "OK"))
        runner.validate_sprites = Mock(return_value=(0, "OK"))
        runner.validate_audio = Mock(return_value=(0, "OK"))
        runner.validate_fonts = Mock(return_value=(0, "OK"))
        runner.validate_scenes = Mock(return_value=(0, "OK"))
        runner.validate_build = Mock(return_value=(0, "OK"))

        exit_code = runner.run_all()

        assert exit_code == 0

    @pytest.mark.unit
    def test_run_all_with_failures(self, temp_dir):
        """Test run_all with validation failures."""
        runner = ValidationRunner(temp_dir, verbose=False)

        # Mock validators with one failure
        runner.validate_project = Mock(return_value=(1, "Failed"))
        runner.validate_backgrounds = Mock(return_value=(0, "OK"))
        runner.validate_sprites = Mock(return_value=(0, "OK"))
        runner.validate_audio = Mock(return_value=(0, "OK"))
        runner.validate_fonts = Mock(return_value=(0, "OK"))
        runner.validate_scenes = Mock(return_value=(0, "OK"))
        runner.validate_build = Mock(return_value=(0, "OK"))

        exit_code = runner.run_all()

        assert exit_code == 1  # Should return 1 for validation failures

    @pytest.mark.unit
    def test_run_all_with_errors(self, temp_dir):
        """Test run_all with errors."""
        runner = ValidationRunner(temp_dir, verbose=False)

        # Mock validators with one error
        runner.validate_project = Mock(return_value=(2, "Error"))
        runner.validate_backgrounds = Mock(return_value=(0, "OK"))
        runner.validate_sprites = Mock(return_value=(0, "OK"))
        runner.validate_audio = Mock(return_value=(0, "OK"))
        runner.validate_fonts = Mock(return_value=(0, "OK"))
        runner.validate_scenes = Mock(return_value=(0, "OK"))
        runner.validate_build = Mock(return_value=(0, "OK"))

        exit_code = runner.run_all()

        assert exit_code == 2  # Should return 2 for errors

    @pytest.mark.unit
    def test_verbose_mode(self, temp_dir):
        """Test verbose mode passes -v flag to validators."""
        runner = ValidationRunner(temp_dir, verbose=True)

        assert runner.verbose is True

        # Create a test script
        test_script = temp_dir / 'scripts' / 'validation' / 'test_verbose.py'
        test_script.parent.mkdir(parents=True, exist_ok=True)
        test_script.write_text("""#!/usr/bin/env python3
import sys
if '-v' in sys.argv:
    print("Verbose mode enabled")
else:
    print("Verbose mode disabled")
sys.exit(0)
""")
        test_script.chmod(0o755)

        exit_code, output = runner.run_validator(
            "Test Verbose",
            "test_verbose.py",
            []
        )

        assert "verbose mode enabled" in output.lower()
