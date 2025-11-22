#!/usr/bin/env python3
"""
Enhanced Asset Validator with Intelligent Suggestions

Validates assets and provides actionable recommendations for improvement.
"""

import sys
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).parent.parent.parent


class AssetValidator:
    """Enhanced validator with intelligent suggestions."""

    def __init__(self):
        """Initialize the validator."""
        self.project_root = PROJECT_ROOT
        self.issues = []
        self.suggestions = []
        self.warnings = []

    def validate_all(self) -> int:
        """Run all validations.

        Returns:
            Exit code (0 = success, 1 = warnings, 2 = errors)
        """
        print("🔍 Enhanced Asset Validator")
        print("=" * 60)

        self._validate_sprites()
        self._validate_backgrounds()
        self._validate_naming_conventions()
        self._validate_project_structure()
        self._analyze_asset_usage()

        return self._print_report()

    def _validate_sprites(self):
        """Validate sprite assets."""
        sprites_dir = self.project_root / "assets" / "sprites"

        if not sprites_dir.exists():
            self.warnings.append("No sprites directory found")
            self.suggestions.append("Create assets/sprites/ directory for character and object sprites")
            return

        sprites = list(sprites_dir.glob("*.png"))
        print(f"\n📦 Found {len(sprites)} sprite(s)")

        if len(sprites) == 0:
            self.warnings.append("No sprite files found")
            self.suggestions.append("Add sprite images (.png) to assets/sprites/")
            return

        # Check for common issues
        for sprite in sprites:
            # Check naming
            if any(pattern in sprite.stem.lower() for pattern in ['sprite', 'image', 'untitled', 'new']):
                self.warnings.append(f"Generic name: {sprite.name}")
                self.suggestions.append(f"Rename {sprite.name} to something descriptive (e.g., player_walk_01.png)")

            # Check if file is very small (might be corrupt/empty)
            if sprite.stat().st_size < 100:
                self.issues.append(f"Suspiciously small file: {sprite.name} ({sprite.stat().st_size} bytes)")

        # Suggest organization
        if len(sprites) > 20:
            self.suggestions.append("Consider organizing sprites into subdirectories (characters/, objects/, ui/)")

    def _validate_backgrounds(self):
        """Validate background assets."""
        bg_dir = self.project_root / "assets" / "backgrounds"

        if not bg_dir.exists():
            self.warnings.append("No backgrounds directory found")
            self.suggestions.append("Create assets/backgrounds/ directory for scene backgrounds")
            return

        backgrounds = list(bg_dir.glob("*.png"))
        print(f"\n🖼️  Found {len(backgrounds)} background(s)")

        if len(backgrounds) == 0:
            self.warnings.append("No background files found")
            self.suggestions.append("Add background images (.png) to assets/backgrounds/")
            return

        for bg in backgrounds:
            # Check naming
            if any(pattern in bg.stem.lower() for pattern in ['background', 'bg', 'untitled', 'new']):
                self.warnings.append(f"Generic name: {bg.name}")
                self.suggestions.append(f"Rename {bg.name} descriptively (e.g., town_street.png)")

    def _validate_naming_conventions(self):
        """Check naming conventions across all assets."""
        print("\n📝 Checking Naming Conventions")

        assets_dir = self.project_root / "assets"
        if not assets_dir.exists():
            return

        all_assets = list(assets_dir.glob("**/*.png"))

        # Check for spaces in names
        spaces_found = [a for a in all_assets if ' ' in a.stem]
        if spaces_found:
            self.warnings.append(f"Found {len(spaces_found)} file(s) with spaces in names")
            self.suggestions.append("Replace spaces with underscores or hyphens for better compatibility")
            for asset in spaces_found[:3]:  # Show first 3 examples
                self.suggestions.append(f"  Example: {asset.name}")

        # Check for uppercase
        uppercase_found = [a for a in all_assets if a.stem != a.stem.lower()]
        if uppercase_found:
            self.suggestions.append(f"Consider using lowercase for all filenames ({len(uppercase_found)} files have uppercase)")

        # Check for consistent naming patterns
        stems = [a.stem for a in all_assets]
        if stems:
            # Detect common patterns
            patterns = self._detect_naming_patterns(stems)
            if patterns:
                print(f"   Detected patterns: {', '.join(patterns)}")
            else:
                self.suggestions.append("Consider adopting a consistent naming pattern (e.g., category_item_variation.png)")

    def _detect_naming_patterns(self, stems: List[str]) -> List[str]:
        """Detect common naming patterns in asset names."""
        patterns = []

        # Check for underscore separation
        underscore_count = sum(1 for s in stems if '_' in s)
        if underscore_count > len(stems) * 0.5:
            patterns.append("underscore_separated")

        # Check for dash separation
        dash_count = sum(1 for s in stems if '-' in s)
        if dash_count > len(stems) * 0.5:
            patterns.append("dash-separated")

        # Check for camelCase
        camel_count = sum(1 for s in stems if any(c.isupper() for c in s))
        if camel_count > len(stems) * 0.5:
            patterns.append("camelCase")

        return patterns

    def _validate_project_structure(self):
        """Validate overall project structure."""
        print("\n📁 Checking Project Structure")

        expected_dirs = [
            ("assets", "Asset files (sprites, backgrounds, music)"),
            ("scripts", "Build and validation scripts"),
            ("tests", "Test suite"),
            ("docs", "Documentation"),
        ]

        for dir_name, description in expected_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                print(f"   ✅ {dir_name}/ - {description}")
            else:
                self.warnings.append(f"Missing recommended directory: {dir_name}/")
                self.suggestions.append(f"Create {dir_name}/ for {description}")

        # Check for project file
        project_files = list(self.project_root.glob("*.gbsproj"))
        if not project_files:
            self.issues.append("No GB Studio project file (.gbsproj) found")
        elif len(project_files) > 1:
            self.warnings.append(f"Multiple project files found ({len(project_files)})")
            self.suggestions.append("Keep only one .gbsproj file per project")

    def _analyze_asset_usage(self):
        """Analyze asset usage and suggest optimizations."""
        print("\n📊 Analyzing Asset Usage")

        assets_dir = self.project_root / "assets"
        if not assets_dir.exists():
            return

        # Count assets by type
        asset_counts = {
            'sprites': len(list((assets_dir / "sprites").glob("*.png"))) if (assets_dir / "sprites").exists() else 0,
            'backgrounds': len(list((assets_dir / "backgrounds").glob("*.png"))) if (assets_dir / "backgrounds").exists() else 0,
            'music': len(list((assets_dir / "music").glob("*.*"))) if (assets_dir / "music").exists() else 0,
            'sounds': len(list((assets_dir / "sounds").glob("*.*"))) if (assets_dir / "sounds").exists() else 0,
        }

        print(f"   Sprites: {asset_counts['sprites']}")
        print(f"   Backgrounds: {asset_counts['backgrounds']}")
        print(f"   Music: {asset_counts['music']}")
        print(f"   Sounds: {asset_counts['sounds']}")

        # Provide suggestions based on counts
        if asset_counts['sprites'] > 100:
            self.suggestions.append("Large sprite count detected. Consider sprite atlasing or reuse")

        if asset_counts['backgrounds'] > 50:
            self.suggestions.append("Many backgrounds detected. Ensure tile reuse for optimization")

        total_assets = sum(asset_counts.values())
        if total_assets == 0:
            self.warnings.append("No assets found in project")
            self.suggestions.append("Start by adding sprites and backgrounds to assets/ directory")

    def _print_report(self) -> int:
        """Print validation report.

        Returns:
            Exit code
        """
        print("\n" + "=" * 60)
        print("📋 Validation Report")
        print("=" * 60)

        # Errors
        if self.issues:
            print(f"\n❌ Errors ({len(self.issues)}):")
            for issue in self.issues:
                print(f"   - {issue}")

        # Warnings
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   - {warning}")

        # Suggestions
        if self.suggestions:
            print(f"\n💡 Suggestions ({len(self.suggestions)}):")
            for suggestion in self.suggestions:
                if suggestion.startswith("  "):
                    print(f"   {suggestion}")
                else:
                    print(f"   - {suggestion}")

        # Summary
        print("\n" + "=" * 60)
        if not self.issues and not self.warnings:
            print("✅ All validations passed!")
            print("💯 Your project structure looks great!")
            return 0
        elif not self.issues:
            print("✅ No critical issues found")
            print("💡 Review suggestions above for improvements")
            return 1
        else:
            print("❌ Critical issues found")
            print("🔧 Fix errors before building")
            return 2


def main():
    """Main entry point."""
    validator = AssetValidator()
    return validator.validate_all()


if __name__ == "__main__":
    sys.exit(main())
