#!/usr/bin/env python3
"""
Security Audit Script

Runs security checks on the codebase and dependencies.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def check_safety():
    """Run safety check on dependencies."""
    print("🔍 Running dependency security scan...")
    try:
        result = subprocess.run(
            ['safety', 'check', '--json'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ No known security vulnerabilities found")
        else:
            print("⚠️  Security vulnerabilities detected:")
            print(result.stdout)
        return result.returncode
    except FileNotFoundError:
        print("❌ safety not installed. Install with: pip install safety")
        print("   Then run: safety check")
        return 1


def check_secrets():
    """Check for accidentally committed secrets."""
    print("\n🔍 Checking for hardcoded secrets...")
    patterns = [
        ('password', 'Possible password'),
        ('api_key', 'Possible API key'),
        ('secret', 'Possible secret'),
        ('token', 'Possible token'),
    ]

    issues_found = 0
    for pattern, description in patterns:
        try:
            result = subprocess.run(
                ['grep', '-r', '-i', '-n', pattern, 'scripts/', 'langflow_components/'],
                capture_output=True,
                text=True
            )
            # Filter out comments and test files
            lines = [
                line for line in result.stdout.split('\n')
                if line and not line.strip().startswith('#') and 'test' not in line.lower()
            ]
            if lines:
                print(f"⚠️  {description} found:")
                for line in lines[:5]:  # Show first 5 matches
                    print(f"   {line}")
                if len(lines) > 5:
                    print(f"   ... and {len(lines) - 5} more")
                issues_found += len(lines)
        except Exception as e:
            print(f"   Error checking {pattern}: {e}")

    if issues_found == 0:
        print("✅ No hardcoded secrets detected")

    return issues_found


def check_file_permissions():
    """Check for overly permissive file permissions."""
    print("\n🔍 Checking file permissions...")

    suspicious_files = []
    for py_file in PROJECT_ROOT.rglob('*.py'):
        if py_file.stat().st_mode & 0o002:  # World-writable
            suspicious_files.append(py_file)

    if suspicious_files:
        print("⚠️  World-writable Python files found:")
        for f in suspicious_files:
            print(f"   {f}")
        return len(suspicious_files)
    else:
        print("✅ No overly permissive file permissions found")
        return 0


def check_requirements():
    """Check that requirements.txt exists and has pinned versions."""
    print("\n🔍 Checking requirements.txt...")

    req_file = PROJECT_ROOT / 'requirements.txt'
    if not req_file.exists():
        print("❌ requirements.txt not found")
        return 1

    with open(req_file) as f:
        lines = f.readlines()

    unpinned = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and '==' not in line:
            unpinned.append(line)

    if unpinned:
        print(f"⚠️  {len(unpinned)} unpinned dependencies found:")
        for dep in unpinned:
            print(f"   {dep}")
        return len(unpinned)
    else:
        print("✅ All dependencies pinned with versions")
        return 0


def main():
    """Run all security checks."""
    print("=" * 60)
    print("BarrySharpProMover Security Audit")
    print("=" * 60)

    issues = 0

    # Run checks
    issues += check_safety()
    issues += check_secrets()
    issues += check_file_permissions()
    issues += check_requirements()

    # Summary
    print("\n" + "=" * 60)
    if issues == 0:
        print("✅ Security audit passed - no issues found")
        return 0
    else:
        print(f"⚠️  Security audit found {issues} potential issue(s)")
        print("\nRecommendations:")
        print("1. Review and address flagged issues")
        print("2. Run 'safety check' for detailed vulnerability report")
        print("3. Ensure all secrets are in .env (not committed)")
        print("4. Pin all dependency versions in requirements.txt")
        return 1


if __name__ == '__main__':
    sys.exit(main())
