#!/usr/bin/env python3
"""
Pytest Configuration and Shared Fixtures

This module provides common test fixtures used across all tests in the
BarrySharpProMover test suite.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from PIL import Image
import json
import wave
import struct


# =============================================================================
# Directory Fixtures
# =============================================================================

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    tmpdir = tempfile.mkdtemp()
    yield Path(tmpdir)
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def project_structure(temp_dir):
    """Create a mock project directory structure."""
    structure = {
        'assets': ['backgrounds', 'sprites', 'music', 'sounds', 'fonts'],
        'project': ['scenes'],
        'build': [],
        'scripts': ['validation'],
        'langflow_components': ['tools'],
    }

    for parent, children in structure.items():
        parent_path = temp_dir / parent
        parent_path.mkdir(exist_ok=True)
        for child in children:
            (parent_path / child).mkdir(exist_ok=True)

    return temp_dir


# =============================================================================
# Image Fixtures
# =============================================================================

@pytest.fixture
def create_test_image():
    """Factory fixture to create test images."""
    def _create_image(path: Path, width: int, height: int,
                      colors: list = None, mode: str = 'RGB'):
        """
        Create a test image with specified parameters.

        Args:
            path: Where to save the image
            width: Image width in pixels
            height: Image height in pixels
            colors: List of RGB tuples to use (default: [(255,0,0), (0,255,0)])
            mode: PIL image mode ('RGB', 'RGBA', etc.)
        """
        if colors is None:
            colors = [(255, 0, 0), (0, 255, 0)]

        img = Image.new(mode, (width, height), colors[0])

        # Create a simple pattern with multiple colors
        pixels = img.load()
        for y in range(height):
            for x in range(width):
                color_idx = (x // 8 + y // 8) % len(colors)
                pixels[x, y] = colors[color_idx]

        img.save(path)
        return path

    return _create_image


@pytest.fixture
def valid_background(temp_dir, create_test_image):
    """Create a valid GB Studio background image (160x144, <=4 colors)."""
    bg_path = temp_dir / "valid_background.png"
    colors = [(255, 255, 255), (192, 192, 192), (96, 96, 96), (0, 0, 0)]
    return create_test_image(bg_path, 160, 144, colors, 'RGB')


@pytest.fixture
def invalid_background_size(temp_dir, create_test_image):
    """Create an invalid background (wrong size)."""
    bg_path = temp_dir / "invalid_size.png"
    return create_test_image(bg_path, 100, 100, None, 'RGB')


@pytest.fixture
def valid_sprite(temp_dir, create_test_image):
    """Create a valid sprite image (16x16, <=4 colors with transparency)."""
    sprite_path = temp_dir / "valid_sprite.png"
    colors = [(0, 0, 0, 0), (255, 255, 255, 255), (128, 128, 128, 255), (0, 0, 0, 255)]
    return create_test_image(sprite_path, 16, 16, colors, 'RGBA')


@pytest.fixture
def invalid_sprite_colors(temp_dir, create_test_image):
    """Create a sprite with too many colors."""
    sprite_path = temp_dir / "too_many_colors.png"
    colors = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255),
              (255, 255, 0, 255), (255, 0, 255, 255)]
    return create_test_image(sprite_path, 16, 16, colors, 'RGBA')


# =============================================================================
# Audio Fixtures
# =============================================================================

@pytest.fixture
def create_test_wav():
    """Factory fixture to create test WAV files."""
    def _create_wav(path: Path, duration: float = 1.0,
                    sample_rate: int = 44100, channels: int = 1,
                    sample_width: int = 2):
        """
        Create a test WAV file.

        Args:
            path: Where to save the WAV file
            duration: Duration in seconds
            sample_rate: Samples per second (44100, 22050, etc.)
            channels: Number of channels (1=mono, 2=stereo)
            sample_width: Bytes per sample (1=8-bit, 2=16-bit)
        """
        with wave.open(str(path), 'wb') as wav:
            wav.setnchannels(channels)
            wav.setsampwidth(sample_width)
            wav.setframerate(sample_rate)

            # Generate simple sine wave
            num_frames = int(duration * sample_rate)
            for i in range(num_frames):
                value = int(32767 * 0.5)  # Simple constant value
                packed = struct.pack('<h', value)
                wav.writeframes(packed)

        return path

    return _create_wav


@pytest.fixture
def valid_wav_mono(temp_dir, create_test_wav):
    """Create a valid mono WAV file."""
    wav_path = temp_dir / "valid_mono.wav"
    return create_test_wav(wav_path, duration=0.5, channels=1)


@pytest.fixture
def invalid_wav_stereo(temp_dir, create_test_wav):
    """Create an invalid stereo WAV file (GB Studio prefers mono)."""
    wav_path = temp_dir / "invalid_stereo.wav"
    return create_test_wav(wav_path, duration=0.5, channels=2)


# =============================================================================
# Font Fixtures
# =============================================================================

@pytest.fixture
def valid_font_json(temp_dir):
    """Create a valid GB Studio font JSON file."""
    font_data = {
        "id": "test-font-001",
        "name": "Test Font",
        "filename": "test-font.png",
        "width": 128,
        "height": 112,
        "mapping": {
            "A": [0, 0, 8, 8],
            "B": [8, 0, 8, 8],
            "C": [16, 0, 8, 8],
        }
    }
    font_path = temp_dir / "valid_font.json"
    with open(font_path, 'w') as f:
        json.dump(font_data, f, indent=2)
    return font_path


@pytest.fixture
def invalid_font_json_missing_fields(temp_dir):
    """Create an invalid font JSON (missing required fields)."""
    font_data = {
        "name": "Incomplete Font",
        # Missing 'id', 'filename', 'mapping'
    }
    font_path = temp_dir / "invalid_font.json"
    with open(font_path, 'w') as f:
        json.dump(font_data, f, indent=2)
    return font_path


# =============================================================================
# Project File Fixtures
# =============================================================================

@pytest.fixture
def valid_gbsproj(temp_dir):
    """Create a valid GB Studio project file."""
    project_data = {
        "_resourceType": "project",
        "name": "Test Project",
        "_version": "4.1.0",
        "author": "Test Author",
        "notes": "Test project for unit testing",
        "scenes": [],
        "backgrounds": [],
        "spriteSheets": [],
        "variables": [],
        "settings": {
            "startSceneId": "",
            "startX": 0,
            "startY": 0,
            "playerSpriteSheetId": ""
        }
    }
    project_path = temp_dir / "test_project.gbsproj"
    with open(project_path, 'w') as f:
        json.dump(project_data, f, indent=2)
    return project_path


@pytest.fixture
def invalid_gbsproj_missing_version(temp_dir):
    """Create an invalid project file (missing version)."""
    project_data = {
        "_resourceType": "project",
        "name": "Invalid Project",
        # Missing '_version'
    }
    project_path = temp_dir / "invalid_project.gbsproj"
    with open(project_path, 'w') as f:
        json.dump(project_data, f, indent=2)
    return project_path


# =============================================================================
# ROM Fixtures
# =============================================================================

@pytest.fixture
def create_test_rom():
    """Factory fixture to create test ROM files."""
    def _create_rom(path: Path, size: int = 32768, valid_header: bool = True):
        """
        Create a test ROM file.

        Args:
            path: Where to save the ROM
            size: ROM size in bytes (minimum 32KB)
            valid_header: Whether to include a valid GB ROM header
        """
        rom_data = bytearray(size)

        if valid_header and size >= 0x0150:
            # Add valid GB ROM header
            # Title at 0x0134
            title = b"TEST ROM\x00\x00\x00\x00\x00\x00\x00\x00"
            rom_data[0x0134:0x0144] = title

            # CGB flag at 0x0143 (0x00 = DMG only)
            rom_data[0x0143] = 0x00

            # Calculate and set header checksum at 0x014D
            header_checksum = 0
            for addr in range(0x0134, 0x014D):
                header_checksum = (header_checksum - rom_data[addr] - 1) & 0xFF
            rom_data[0x014D] = header_checksum

        with open(path, 'wb') as f:
            f.write(rom_data)

        return path

    return _create_rom


@pytest.fixture
def valid_rom(temp_dir, create_test_rom):
    """Create a valid ROM file."""
    rom_path = temp_dir / "valid.gb"
    return create_test_rom(rom_path, size=65536, valid_header=True)


@pytest.fixture
def invalid_rom_too_small(temp_dir, create_test_rom):
    """Create an invalid ROM (too small)."""
    rom_path = temp_dir / "too_small.gb"
    return create_test_rom(rom_path, size=1024, valid_header=False)


# =============================================================================
# Environment Fixtures
# =============================================================================

@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables for testing."""
    env_vars = {
        'GB_STUDIO_CLI_PATH': '/usr/local/bin/gb-studio-cli',
        'OLLAMA_HOST': 'http://localhost:11434',
        'LANGFLOW_PORT': '7860',
        'LANGFLOW_HOST': '127.0.0.1',
        'LOG_LEVEL': 'INFO',
    }

    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)

    return env_vars


@pytest.fixture
def mock_empty_env(monkeypatch):
    """Clear all environment variables for testing."""
    env_vars = [
        'GB_STUDIO_CLI_PATH',
        'OLLAMA_HOST',
        'LANGFLOW_PORT',
        'LANGFLOW_HOST',
        'LOG_LEVEL',
    ]

    for var in env_vars:
        monkeypatch.delenv(var, raising=False)


# =============================================================================
# Logging Fixtures
# =============================================================================

@pytest.fixture
def capture_logs(caplog):
    """Fixture to capture and inspect log messages."""
    import logging
    caplog.set_level(logging.DEBUG)
    return caplog
