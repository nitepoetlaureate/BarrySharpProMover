# Create Release Package

Create a complete release package with checksums and optional GPG signing:

1. Build the ROM (if not already built)
2. Create release directory with version number
3. Generate checksums (MD5, SHA256, SHA512)
4. Optionally sign with GPG
5. Create release manifest
6. Generate release notes template

Usage:
```bash
# Create release with checksums (no signing)
python scripts/release/create_release.py create v1.0.0

# Create release with GPG signing
python scripts/release/create_release.py create v1.0.0 --sign

# Create release with specific GPG key
python scripts/release/create_release.py create v1.0.0 --sign --gpg-key YOUR_KEY_ID

# Verify a release
python scripts/release/create_release.py verify v1.0.0
```

Ask the user for:
- Version number (e.g., v1.0.0)
- Whether to GPG sign the release
- GPG key ID (if signing)

After creating the release:
- Show release directory location
- List all created artifacts
- Display checksums
- Remind user to edit RELEASE_NOTES before publishing
- Provide instructions for publishing to GitHub/itch.io
