#!/usr/bin/env python3
"""
Release Automation for Barry Sharp Pro Mover

Creates releases with checksums and optional GPG signing.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

PROJECT_ROOT = Path(__file__).parent.parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
RELEASE_DIR = PROJECT_ROOT / "releases"


def compute_checksums(file_path: Path) -> Dict[str, str]:
    """Compute multiple checksums for a file.

    Args:
        file_path: Path to file

    Returns:
        Dictionary of algorithm -> checksum
    """
    checksums = {}

    # MD5
    md5 = hashlib.md5()
    # SHA256
    sha256 = hashlib.sha256()
    # SHA512
    sha512 = hashlib.sha512()

    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
            sha256.update(chunk)
            sha512.update(chunk)

    checksums['md5'] = md5.hexdigest()
    checksums['sha256'] = sha256.hexdigest()
    checksums['sha512'] = sha512.hexdigest()

    return checksums


def create_checksum_file(file_path: Path) -> Path:
    """Create a checksum file for an artifact.

    Args:
        file_path: Path to artifact

    Returns:
        Path to checksum file
    """
    checksums = compute_checksums(file_path)

    checksum_file = file_path.with_suffix(file_path.suffix + '.checksums')

    with open(checksum_file, 'w') as f:
        f.write(f"# Checksums for {file_path.name}\n")
        f.write(f"# Generated: {datetime.now().isoformat()}\n\n")
        f.write(f"MD5:    {checksums['md5']}\n")
        f.write(f"SHA256: {checksums['sha256']}\n")
        f.write(f"SHA512: {checksums['sha512']}\n")

    print(f"✅ Created checksums: {checksum_file.name}")
    return checksum_file


def sign_file(file_path: Path, gpg_key: str = None) -> Path:
    """Sign a file with GPG.

    Args:
        file_path: Path to file to sign
        gpg_key: GPG key ID (optional, uses default if not specified)

    Returns:
        Path to signature file
    """
    sig_file = file_path.with_suffix(file_path.suffix + '.sig')

    cmd = ["gpg", "--detach-sign", "--armor"]
    if gpg_key:
        cmd.extend(["--local-user", gpg_key])
    cmd.extend(["--output", str(sig_file), str(file_path)])

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Created signature: {sig_file.name}")
        return sig_file
    except subprocess.CalledProcessError as e:
        print(f"⚠️  GPG signing failed: {e.stderr.decode()}")
        print("   Continuing without signature...")
        return None
    except FileNotFoundError:
        print("⚠️  GPG not found. Install GPG to enable signing.")
        print("   Continuing without signature...")
        return None


def verify_signature(file_path: Path, sig_file: Path) -> bool:
    """Verify a GPG signature.

    Args:
        file_path: Path to file
        sig_file: Path to signature file

    Returns:
        True if signature is valid
    """
    try:
        result = subprocess.run(
            ["gpg", "--verify", str(sig_file), str(file_path)],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("⚠️  GPG not found")
        return False


def create_release_manifest(version: str, artifacts: List[Path]) -> Path:
    """Create a release manifest file.

    Args:
        version: Release version
        artifacts: List of artifact paths

    Returns:
        Path to manifest file
    """
    manifest = {
        'version': version,
        'timestamp': datetime.now().isoformat(),
        'artifacts': []
    }

    for artifact in artifacts:
        if artifact.exists():
            checksums = compute_checksums(artifact)
            manifest['artifacts'].append({
                'filename': artifact.name,
                'size': artifact.stat().st_size,
                'checksums': checksums
            })

    manifest_file = RELEASE_DIR / version / f"manifest_{version}.json"
    manifest_file.parent.mkdir(parents=True, exist_ok=True)

    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Created manifest: {manifest_file.name}")
    return manifest_file


def create_release(version: str, sign: bool = False, gpg_key: str = None):
    """Create a release with all artifacts.

    Args:
        version: Release version (e.g., "v1.0.0")
        sign: Whether to GPG sign artifacts
        gpg_key: GPG key ID for signing
    """
    print(f"🚀 Creating Release: {version}")
    print("=" * 60)

    # Create release directory
    release_dir = RELEASE_DIR / version
    release_dir.mkdir(parents=True, exist_ok=True)

    # Find ROM files
    rom_files = list(DIST_DIR.glob("**/*.gb")) + list(DIST_DIR.glob("**/*.gbc"))

    if not rom_files:
        print("⚠️  No ROM files found in dist/")
        print("   Run 'make build-rom' first")
        return 1

    artifacts = []

    for rom_file in rom_files:
        print(f"\n📦 Processing: {rom_file.name}")

        # Copy to release directory
        release_artifact = release_dir / rom_file.name
        import shutil
        shutil.copy2(rom_file, release_artifact)
        print(f"   Copied to: {release_artifact}")

        artifacts.append(release_artifact)

        # Create checksums
        create_checksum_file(release_artifact)

        # Sign if requested
        if sign:
            sig_file = sign_file(release_artifact, gpg_key)
            if sig_file:
                artifacts.append(sig_file)

    # Create manifest
    manifest = create_release_manifest(version, artifacts)

    # Create release notes template
    notes_file = release_dir / f"RELEASE_NOTES_{version}.md"
    if not notes_file.exists():
        with open(notes_file, 'w') as f:
            f.write(f"# Barry Sharp Pro Mover {version}\n\n")
            f.write(f"Release Date: {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write("## What's New\n\n")
            f.write("- \n\n")
            f.write("## Bug Fixes\n\n")
            f.write("- \n\n")
            f.write("## Downloads\n\n")
            for artifact in artifacts:
                if artifact.suffix in ['.gb', '.gbc']:
                    f.write(f"- [{artifact.name}]({artifact.name})\n")
            f.write("\n## Verification\n\n")
            f.write("See `manifest_*.json` for checksums.\n")
        print(f"\n✅ Created release notes template: {notes_file.name}")
        print(f"   Edit this file before publishing!")

    print("\n" + "=" * 60)
    print(f"✅ Release {version} created successfully!")
    print(f"📁 Location: {release_dir}")
    print(f"📦 Artifacts: {len([a for a in artifacts if a.suffix in ['.gb', '.gbc']])}")
    print(f"📝 Checksums: ✅")
    print(f"🔐 Signatures: {'✅' if sign else '❌ (use --sign to enable)'}")

    return 0


def verify_release(version: str):
    """Verify a release's integrity.

    Args:
        version: Release version to verify
    """
    print(f"🔍 Verifying Release: {version}")
    print("=" * 60)

    release_dir = RELEASE_DIR / version

    if not release_dir.exists():
        print(f"❌ Release {version} not found")
        return 1

    # Load manifest
    manifest_files = list(release_dir.glob("manifest_*.json"))
    if not manifest_files:
        print("❌ No manifest found")
        return 1

    with open(manifest_files[0], 'r') as f:
        manifest = json.load(f)

    print(f"Version: {manifest['version']}")
    print(f"Date: {manifest['timestamp']}")
    print(f"\n📦 Verifying {len(manifest['artifacts'])} artifact(s)...\n")

    all_valid = True

    for artifact_info in manifest['artifacts']:
        filename = artifact_info['filename']
        artifact_path = release_dir / filename

        print(f"Checking {filename}...")

        if not artifact_path.exists():
            print(f"  ❌ File not found")
            all_valid = False
            continue

        # Verify checksums
        actual_checksums = compute_checksums(artifact_path)
        expected_checksums = artifact_info['checksums']

        for algo in ['md5', 'sha256', 'sha512']:
            if actual_checksums[algo] == expected_checksums[algo]:
                print(f"  ✅ {algo.upper()}: OK")
            else:
                print(f"  ❌ {algo.upper()}: MISMATCH")
                all_valid = False

        # Verify signature if present
        sig_file = artifact_path.with_suffix(artifact_path.suffix + '.sig')
        if sig_file.exists():
            if verify_signature(artifact_path, sig_file):
                print(f"  ✅ GPG Signature: VALID")
            else:
                print(f"  ❌ GPG Signature: INVALID")
                all_valid = False

    print("\n" + "=" * 60)
    if all_valid:
        print("✅ Release verification PASSED")
        return 0
    else:
        print("❌ Release verification FAILED")
        return 1


def main():
    """Main CLI."""
    import argparse

    parser = argparse.ArgumentParser(description="Release automation for Barry Sharp Pro Mover")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new release')
    create_parser.add_argument('version', help='Release version (e.g., v1.0.0)')
    create_parser.add_argument('--sign', action='store_true', help='Sign artifacts with GPG')
    create_parser.add_argument('--gpg-key', help='GPG key ID to use for signing')

    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify a release')
    verify_parser.add_argument('version', help='Release version to verify')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'create':
        return create_release(args.version, args.sign, args.gpg_key)
    elif args.command == 'verify':
        return verify_release(args.version)

    return 0


if __name__ == "__main__":
    sys.exit(main())
