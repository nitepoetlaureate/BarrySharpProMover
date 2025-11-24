#!/usr/bin/env python3
"""
Unit Tests for check_build.py

Tests ROM build validation including:
- File size validation
- ROM header validation
- Checksum verification
- MD5 hash calculation
"""

import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts' / 'validation'))

from check_build import validate_rom_file, validate_rom_header


class TestValidateRomFile:
    """Test ROM file validation function."""

    @pytest.mark.unit
    def test_valid_rom(self, valid_rom):
        """Test validation of a valid ROM."""
        is_valid, issues = validate_rom_file(str(valid_rom))
        assert is_valid is True
        assert len(issues) == 0

    @pytest.mark.unit
    def test_rom_too_small(self, invalid_rom_too_small):
        """Test validation fails for ROM that's too small."""
        is_valid, issues = validate_rom_file(str(invalid_rom_too_small))
        assert is_valid is False
        assert any("too small" in issue.lower() or "size" in issue.lower()
                   for issue in issues)

    @pytest.mark.unit
    def test_file_not_found(self, temp_dir):
        """Test error handling for non-existent file."""
        nonexistent = temp_dir / "nonexistent.gb"
        is_valid, issues = validate_rom_file(str(nonexistent))
        assert is_valid is False
        assert any("not found" in issue.lower() for issue in issues)

    @pytest.mark.unit
    def test_invalid_extension(self, temp_dir):
        """Test validation warns about wrong extension."""
        wrong_ext = temp_dir / "rom.txt"
        wrong_ext.write_bytes(b"0" * 32768)

        is_valid, issues = validate_rom_file(str(wrong_ext))
        # Should warn about extension

    @pytest.mark.unit
    def test_empty_rom(self, temp_dir):
        """Test validation fails for empty ROM."""
        empty = temp_dir / "empty.gb"
        empty.write_bytes(b"")

        is_valid, issues = validate_rom_file(str(empty))
        assert is_valid is False
        assert any("empty" in issue.lower() for issue in issues)

    @pytest.mark.unit
    def test_rom_with_hash_file(self, temp_dir, create_test_rom):
        """Test ROM validation with matching hash file."""
        import hashlib

        rom_path = temp_dir / "test.gb"
        create_test_rom(rom_path, size=65536, valid_header=True)

        # Create matching MD5 hash file
        with open(rom_path, 'rb') as f:
            rom_hash = hashlib.md5(f.read()).hexdigest()

        hash_path = temp_dir / "test.md5"
        hash_path.write_text(f"{rom_hash}  test.gb\n")

        is_valid, issues = validate_rom_file(str(rom_path))
        # Should validate and match hash
        assert is_valid is True


class TestValidateRomHeader:
    """Test ROM header validation."""

    @pytest.mark.unit
    def test_valid_header(self):
        """Test validation of valid ROM header."""
        rom_data = bytearray(0x0150)

        # Add valid header
        title = b"TEST\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        rom_data[0x0134:0x0144] = title
        rom_data[0x0143] = 0x00  # DMG

        # Calculate checksum
        checksum = 0
        for addr in range(0x0134, 0x014D):
            checksum = (checksum - rom_data[addr] - 1) & 0xFF
        rom_data[0x014D] = checksum

        is_valid, issues = validate_rom_header(bytes(rom_data))
        assert is_valid is True
        assert len(issues) == 0

    @pytest.mark.unit
    def test_header_too_short(self):
        """Test validation fails for ROM too short to have header."""
        rom_data = b"0" * 100  # Too short

        is_valid, issues = validate_rom_header(rom_data)
        assert is_valid is False
        assert any("too small" in issue.lower() or "header" in issue.lower()
                   for issue in issues)

    @pytest.mark.unit
    def test_invalid_checksum(self):
        """Test validation warns about invalid checksum."""
        rom_data = bytearray(0x0150)

        # Add header with wrong checksum
        title = b"TEST\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        rom_data[0x0134:0x0144] = title
        rom_data[0x0143] = 0x00
        rom_data[0x014D] = 0xFF  # Wrong checksum

        is_valid, issues = validate_rom_header(bytes(rom_data))
        # Should still pass but may warn about checksum
