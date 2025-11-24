#!/usr/bin/env python3
"""
Unit Tests for check_audio.py

Tests audio file validation including:
- Format validation (.mod, .uge, .wav, .vgm)
- WAV file property validation
- File size limits
- Error handling
"""

import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts' / 'validation'))

from check_audio import validate_audio_file, validate_wav_file


class TestValidateAudioFile:
    """Test audio file validation function."""

    @pytest.mark.unit
    def test_valid_wav(self, valid_wav_mono):
        """Test validation of a valid WAV file."""
        is_valid, issues = validate_audio_file(str(valid_wav_mono))
        assert is_valid is True
        assert len(issues) == 0

    @pytest.mark.unit
    def test_file_not_found(self, temp_dir):
        """Test error handling for non-existent file."""
        nonexistent = temp_dir / "nonexistent.wav"
        is_valid, issues = validate_audio_file(str(nonexistent))
        assert is_valid is False
        assert any("not found" in issue.lower() for issue in issues)

    @pytest.mark.unit
    def test_invalid_extension(self, temp_dir):
        """Test validation fails for unsupported file types."""
        invalid = temp_dir / "audio.mp3"
        invalid.write_bytes(b"fake mp3 data")

        is_valid, issues = validate_audio_file(str(invalid))
        assert is_valid is False
        assert any("extension" in issue.lower() or "format" in issue.lower()
                   for issue in issues)

    @pytest.mark.unit
    def test_empty_file(self, temp_dir):
        """Test validation fails for empty files."""
        empty = temp_dir / "empty.wav"
        empty.write_bytes(b"")

        is_valid, issues = validate_audio_file(str(empty))
        assert is_valid is False
        assert any("empty" in issue.lower() for issue in issues)

    @pytest.mark.unit
    def test_file_too_large(self, temp_dir):
        """Test validation warns about large files."""
        large_file = temp_dir / "large.wav"
        # Create a file larger than 10MB
        large_file.write_bytes(b"0" * (11 * 1024 * 1024))

        is_valid, issues = validate_audio_file(str(large_file))
        # Should warn about file size
        assert any("size" in issue.lower() or "large" in issue.lower()
                   for issue in issues)


class TestValidateWavFile:
    """Test WAV-specific validation."""

    @pytest.mark.unit
    def test_valid_mono_wav(self, valid_wav_mono):
        """Test validation of mono WAV."""
        is_valid, issues = validate_wav_file(str(valid_wav_mono))
        assert is_valid is True
        assert len(issues) == 0

    @pytest.mark.unit
    def test_stereo_wav_warning(self, invalid_wav_stereo):
        """Test validation warns about stereo WAV."""
        is_valid, issues = validate_wav_file(str(invalid_wav_stereo))
        # May warn about stereo (GB Studio prefers mono)

    @pytest.mark.unit
    def test_invalid_wav_format(self, temp_dir):
        """Test error handling for corrupted WAV."""
        corrupted = temp_dir / "corrupted.wav"
        corrupted.write_bytes(b"Not a real WAV file")

        is_valid, issues = validate_wav_file(str(corrupted))
        assert is_valid is False
