# Test Fixtures Directory

This directory contains static test data and sample files used by the test suite.

## Organization

- `sample_backgrounds/` - Sample background images for testing validation
- `sample_sprites/` - Sample sprite images for testing validation
- `sample_project/` - Sample GB Studio project files
- `sample_audio/` - Sample music and sound files
- `sample_fonts/` - Sample font files
- `sample_roms/` - Sample ROM files for build validation

## Usage

Test fixtures in this directory are used by the pytest test suite via the
fixtures defined in `conftest.py`. Dynamic fixtures (created programmatically
during test runs) are preferred for most tests to ensure isolation and
repeatability.

Static fixtures here are used for:
- Complex files that are hard to generate programmatically
- Reference files for comparison tests
- Edge cases and known problematic files
