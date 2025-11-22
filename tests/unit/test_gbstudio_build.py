"""Unit tests for GBStudioBuild component."""


# Import the component
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".langflow" / "components"))

from gbstudio_build import GBStudioBuild


class TestGBStudioBuild:
    """Test suite for GBStudioBuild component."""

    def test_successful_rom_build(self, temp_project_dir, mock_subprocess):
        """Test successful ROM build with default parameters."""
        # Setup
        builder = GBStudioBuild()

        # Create dist directory and mock ROM file
        dist_dir = temp_project_dir / "dist"
        dist_dir.mkdir(parents=True)

        with patch('subprocess.run', mock_subprocess), \
             patch.object(Path, 'rglob', return_value=iter([dist_dir / "game.gb"])):

            result = builder.build(
                project_dir=str(temp_project_dir),
                cli_path="gbstudio-cli"
            )

            # Verify subprocess was called with correct args
            assert mock_subprocess.called
            call_args = mock_subprocess.call_args[0][0]
            assert "gbstudio-cli" in call_args
            assert "--project" in call_args
            assert "--rom" in call_args
            assert "--open" in call_args  # Default is True

            # Verify result
            assert result.endswith("game.gb")

    def test_build_without_emulator(self, temp_project_dir, mock_subprocess):
        """Test build without opening emulator."""
        builder = GBStudioBuild()
        dist_dir = temp_project_dir / "dist"
        dist_dir.mkdir(parents=True)

        with patch('subprocess.run', mock_subprocess), \
             patch.object(Path, 'rglob', return_value=iter([dist_dir / "game.gb"])):

            builder.build(
                project_dir=str(temp_project_dir),
                open_emulator=False
            )

            call_args = mock_subprocess.call_args[0][0]
            assert "--open" not in call_args

    def test_build_with_web_target(self, temp_project_dir, mock_subprocess):
        """Test build with web target."""
        builder = GBStudioBuild()
        dist_dir = temp_project_dir / "dist"
        dist_dir.mkdir(parents=True)

        with patch('subprocess.run', mock_subprocess), \
             patch.object(Path, 'rglob', return_value=iter([dist_dir / "game.gb"])):

            builder.build(
                project_dir=str(temp_project_dir),
                target="web",
                open_emulator=False
            )

            call_args = mock_subprocess.call_args[0][0]
            assert "--web" in call_args
            assert "--rom" not in call_args

    def test_missing_project_directory(self):
        """Test error handling for missing project directory."""
        builder = GBStudioBuild()

        with pytest.raises(ValueError, match="Project dir not found"):
            builder.build(project_dir="/nonexistent/path")

    def test_subprocess_failure(self, temp_project_dir):
        """Test error handling when subprocess fails."""
        builder = GBStudioBuild()

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Build failed: syntax error"
        mock_result.stdout = ""

        with patch('subprocess.run', return_value=mock_result):
            with pytest.raises(RuntimeError, match="Build failed: syntax error"):
                builder.build(project_dir=str(temp_project_dir))

    def test_no_rom_produced(self, temp_project_dir, mock_subprocess):
        """Test error handling when build succeeds but no ROM is produced."""
        builder = GBStudioBuild()

        # Mock rglob to return no files
        with patch('subprocess.run', mock_subprocess), \
             patch.object(Path, 'rglob', return_value=iter([])):

            with pytest.raises(RuntimeError, match="no .gb file was produced"):
                builder.build(project_dir=str(temp_project_dir))

    def test_path_expansion(self, mock_subprocess):
        """Test that ~ in paths gets expanded."""
        builder = GBStudioBuild()

        with patch('subprocess.run', mock_subprocess), \
             patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'rglob', return_value=iter([Path("/expanded/dist/game.gb")])):

            result = builder.build(
                project_dir="~/test-project",
                open_emulator=False
            )

            # Verify path was expanded
            call_args = mock_subprocess.call_args[0][0]
            project_arg_index = call_args.index("--project") + 1
            assert "~" not in call_args[project_arg_index]

    def test_custom_cli_path(self, temp_project_dir, mock_subprocess):
        """Test using custom CLI path."""
        builder = GBStudioBuild()
        dist_dir = temp_project_dir / "dist"
        dist_dir.mkdir(parents=True)

        custom_cli = "/usr/local/bin/custom-gbstudio-cli"

        with patch('subprocess.run', mock_subprocess), \
             patch.object(Path, 'rglob', return_value=iter([dist_dir / "game.gb"])):

            builder.build(
                project_dir=str(temp_project_dir),
                cli_path=custom_cli,
                open_emulator=False
            )

            call_args = mock_subprocess.call_args[0][0]
            assert call_args[0] == custom_cli

    def test_timestamped_output_directory(self, temp_project_dir, mock_subprocess):
        """Test that output directory includes timestamp."""
        builder = GBStudioBuild()

        with patch('subprocess.run', mock_subprocess), \
             patch.object(Path, 'rglob', return_value=iter([temp_project_dir / "dist" / "20251121120000" / "game.gb"])), \
             patch('datetime.datetime') as mock_datetime:

            # Mock datetime to return fixed timestamp
            mock_datetime.now.return_value.strftime.return_value = "20251121120000"

            builder.build(
                project_dir=str(temp_project_dir),
                open_emulator=False
            )

            call_args = mock_subprocess.call_args[0][0]
            output_arg_index = call_args.index("--output") + 1
            assert "20251121120000" in call_args[output_arg_index]

    def test_code_parameter_ignored(self, temp_project_dir, mock_subprocess):
        """Test that code parameter is accepted but ignored (LangFlow compatibility)."""
        builder = GBStudioBuild()
        dist_dir = temp_project_dir / "dist"
        dist_dir.mkdir(parents=True)

        with patch('subprocess.run', mock_subprocess), \
             patch.object(Path, 'rglob', return_value=iter([dist_dir / "game.gb"])):

            # Should not raise error even with code parameter
            result = builder.build(
                project_dir=str(temp_project_dir),
                code="some code here",  # Should be ignored
                open_emulator=False
            )

            assert result.endswith("game.gb")

    def test_future_proof_kwargs(self, temp_project_dir, mock_subprocess):
        """Test that unknown kwargs are accepted (**_ future-proofing)."""
        builder = GBStudioBuild()
        dist_dir = temp_project_dir / "dist"
        dist_dir.mkdir(parents=True)

        with patch('subprocess.run', mock_subprocess), \
             patch.object(Path, 'rglob', return_value=iter([dist_dir / "game.gb"])):

            # Should not raise error with unknown parameters
            result = builder.build(
                project_dir=str(temp_project_dir),
                unknown_param="value",
                another_unknown=123,
                open_emulator=False
            )

            assert result.endswith("game.gb")

    def test_component_metadata(self):
        """Test component has correct metadata for LangFlow."""
        builder = GBStudioBuild()

        assert builder.display_name == "GBStudio Build"
        assert "GB Studio" in builder.description
        assert "ROM" in builder.description

    def test_subprocess_stderr_in_exception(self, temp_project_dir):
        """Test that stderr is included in exception message."""
        builder = GBStudioBuild()

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Detailed error message"
        mock_result.stdout = ""

        with patch('subprocess.run', return_value=mock_result):
            with pytest.raises(RuntimeError) as exc_info:
                builder.build(project_dir=str(temp_project_dir))

            assert "Detailed error message" in str(exc_info.value)

    def test_subprocess_stdout_fallback(self, temp_project_dir):
        """Test that stdout is used if stderr is empty."""
        builder = GBStudioBuild()

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = ""
        mock_result.stdout = "Error in stdout"

        with patch('subprocess.run', return_value=mock_result):
            with pytest.raises(RuntimeError) as exc_info:
                builder.build(project_dir=str(temp_project_dir))

            assert "Error in stdout" in str(exc_info.value)

    def test_dist_directory_creation(self, temp_project_dir, mock_subprocess):
        """Test that dist directory is created if it doesn't exist."""
        builder = GBStudioBuild()

        # Verify dist doesn't exist initially
        dist_dir = temp_project_dir / "dist"
        assert not dist_dir.exists()

        with patch('subprocess.run', mock_subprocess), \
             patch.object(Path, 'rglob', return_value=iter([dist_dir / "ts" / "game.gb"])):

            builder.build(
                project_dir=str(temp_project_dir),
                open_emulator=False
            )

            # Dist directory should be created
            assert dist_dir.exists()

    def test_all_target(self, temp_project_dir, mock_subprocess):
        """Test build with 'all' target."""
        builder = GBStudioBuild()
        dist_dir = temp_project_dir / "dist"
        dist_dir.mkdir(parents=True)

        with patch('subprocess.run', mock_subprocess), \
             patch.object(Path, 'rglob', return_value=iter([dist_dir / "game.gb"])):

            builder.build(
                project_dir=str(temp_project_dir),
                target="all",
                open_emulator=False
            )

            call_args = mock_subprocess.call_args[0][0]
            assert "--all" in call_args

    def test_langflow_import_fallback(self):
        """Test that component works even if LangFlow is not installed."""
        # This is tested by the fact that the import doesn't fail
        # when LangFlow is not available (try/except in gbstudio_build.py)
        builder = GBStudioBuild()
        assert builder is not None
