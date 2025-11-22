#!/usr/bin/env python3
"""
Build Cache Manager for Barry Sharp Pro Mover

Implements intelligent caching to speed up repeated builds.
"""

import hashlib
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent
CACHE_DIR = PROJECT_ROOT / ".build_cache"
CACHE_INDEX = CACHE_DIR / "cache_index.json"
MAX_CACHE_AGE_DAYS = 7
MAX_CACHE_SIZE_MB = 500


class BuildCache:
    """Manages build artifact caching."""

    def __init__(self):
        """Initialize the cache manager."""
        self.cache_dir = CACHE_DIR
        self.index_file = CACHE_INDEX
        self.index = self._load_index()

    def _load_index(self) -> Dict:
        """Load the cache index."""
        if self.index_file.exists():
            try:
                with open(self.index_file) as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                return {'entries': {}, 'stats': {'hits': 0, 'misses': 0}}
        return {'entries': {}, 'stats': {'hits': 0, 'misses': 0}}

    def _save_index(self):
        """Save the cache index."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of a file."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except OSError:
            return ""

    def _compute_directory_hash(self, directory: Path, patterns: list = None) -> str:
        """Compute hash of directory contents.

        Args:
            directory: Directory to hash
            patterns: List of glob patterns to include (default: all files)

        Returns:
            Combined hash of all matching files
        """
        if not directory.exists():
            return ""

        if patterns is None:
            patterns = ["**/*"]

        file_hashes = []
        for pattern in patterns:
            for file_path in sorted(directory.glob(pattern)):
                if file_path.is_file():
                    file_hash = self._compute_file_hash(file_path)
                    file_hashes.append(f"{file_path.relative_to(directory)}:{file_hash}")

        combined = "\n".join(file_hashes)
        return hashlib.sha256(combined.encode()).hexdigest()

    def get_cache_key(self, name: str, dependencies: Dict[str, str]) -> str:
        """Generate cache key from dependencies.

        Args:
            name: Cache entry name
            dependencies: Dict of dependency_name -> hash

        Returns:
            Cache key
        """
        dep_str = json.dumps(dependencies, sort_keys=True)
        key_hash = hashlib.sha256(dep_str.encode()).hexdigest()[:16]
        return f"{name}_{key_hash}"

    def get_cached_artifact(self, cache_key: str) -> Optional[Path]:
        """Retrieve cached artifact if available and valid.

        Args:
            cache_key: Cache key to look up

        Returns:
            Path to cached artifact or None if not found/invalid
        """
        if cache_key not in self.index['entries']:
            self.index['stats']['misses'] += 1
            self._save_index()
            return None

        entry = self.index['entries'][cache_key]
        cached_path = Path(entry['path'])

        # Check if cached file exists
        if not cached_path.exists():
            del self.index['entries'][cache_key]
            self.index['stats']['misses'] += 1
            self._save_index()
            return None

        # Check age
        cached_time = datetime.fromisoformat(entry['timestamp'])
        if datetime.now() - cached_time > timedelta(days=MAX_CACHE_AGE_DAYS):
            cached_path.unlink(missing_ok=True)
            del self.index['entries'][cache_key]
            self.index['stats']['misses'] += 1
            self._save_index()
            return None

        # Cache hit!
        self.index['stats']['hits'] += 1
        self._save_index()
        return cached_path

    def store_artifact(self, cache_key: str, artifact_path: Path, metadata: Dict = None):
        """Store an artifact in the cache.

        Args:
            cache_key: Cache key
            artifact_path: Path to artifact to cache
            metadata: Optional metadata to store
        """
        if not artifact_path.exists():
            return

        # Create cache directory
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Copy artifact to cache
        cached_path = self.cache_dir / f"{cache_key}_{artifact_path.name}"
        shutil.copy2(artifact_path, cached_path)

        # Update index
        self.index['entries'][cache_key] = {
            'path': str(cached_path),
            'timestamp': datetime.now().isoformat(),
            'original': str(artifact_path),
            'size': cached_path.stat().st_size,
            'metadata': metadata or {}
        }

        self._save_index()

    def clean_cache(self, force: bool = False):
        """Clean old or excessive cache entries.

        Args:
            force: If True, remove all cache entries
        """
        if force:
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
            self.index = {'entries': {}, 'stats': {'hits': 0, 'misses': 0}}
            self._save_index()
            return

        # Remove old entries
        current_time = datetime.now()
        entries_to_remove = []

        for key, entry in self.index['entries'].items():
            cached_time = datetime.fromisoformat(entry['timestamp'])
            if current_time - cached_time > timedelta(days=MAX_CACHE_AGE_DAYS):
                entries_to_remove.append(key)
                Path(entry['path']).unlink(missing_ok=True)

        for key in entries_to_remove:
            del self.index['entries'][key]

        # Check total cache size
        total_size = sum(Path(e['path']).stat().st_size
                        for e in self.index['entries'].values()
                        if Path(e['path']).exists())
        total_size_mb = total_size / 1024 / 1024

        # Remove oldest entries if over limit
        if total_size_mb > MAX_CACHE_SIZE_MB:
            sorted_entries = sorted(
                self.index['entries'].items(),
                key=lambda x: x[1]['timestamp']
            )

            while total_size_mb > MAX_CACHE_SIZE_MB and sorted_entries:
                key, entry = sorted_entries.pop(0)
                cached_path = Path(entry['path'])
                if cached_path.exists():
                    size_mb = cached_path.stat().st_size / 1024 / 1024
                    cached_path.unlink()
                    total_size_mb -= size_mb
                del self.index['entries'][key]

        self._save_index()

    def get_stats(self) -> Dict:
        """Get cache statistics."""
        stats = self.index['stats'].copy()
        stats['total_entries'] = len(self.index['entries'])

        total_size = sum(Path(e['path']).stat().st_size
                        for e in self.index['entries'].values()
                        if Path(e['path']).exists())
        stats['total_size_mb'] = total_size / 1024 / 1024

        total_requests = stats['hits'] + stats['misses']
        stats['hit_rate'] = (stats['hits'] / total_requests * 100) if total_requests > 0 else 0

        return stats

    def print_stats(self):
        """Print cache statistics."""
        stats = self.get_stats()

        print("📊 Build Cache Statistics")
        print("=" * 60)
        print(f"Total Entries: {stats['total_entries']}")
        print(f"Cache Size: {stats['total_size_mb']:.2f} MB / {MAX_CACHE_SIZE_MB} MB")
        print(f"Cache Hits: {stats['hits']}")
        print(f"Cache Misses: {stats['misses']}")
        print(f"Hit Rate: {stats['hit_rate']:.1f}%")
        print("=" * 60)


def example_usage():
    """Example of how to use the cache manager."""
    cache = BuildCache()

    # Example: Cache ROM build
    print("Example: Caching ROM build...")

    # Compute dependencies hash
    assets_hash = cache._compute_directory_hash(
        PROJECT_ROOT / "assets",
        patterns=["sprites/**/*.png", "backgrounds/**/*.png"]
    )

    project_file = PROJECT_ROOT / "BARRY-SHARP-PRO-MOVER-1.gbsproj"
    project_hash = cache._compute_file_hash(project_file) if project_file.exists() else ""

    dependencies = {
        'assets': assets_hash,
        'project': project_hash
    }

    cache_key = cache.get_cache_key("rom_build", dependencies)

    # Try to get cached ROM
    cached_rom = cache.get_cached_artifact(cache_key)

    if cached_rom:
        print(f"✅ Cache hit! Using cached ROM: {cached_rom}")
    else:
        print("❌ Cache miss. Build required.")
        # After building, you would call:
        # cache.store_artifact(cache_key, rom_path, {'build_time': time.time()})

    cache.print_stats()


def main():
    """Main CLI for cache management."""
    import sys

    cache = BuildCache()

    if len(sys.argv) < 2:
        print("Usage: cache_manager.py [stats|clean|clean-all]")
        print("\nCommands:")
        print("  stats     - Show cache statistics")
        print("  clean     - Clean old cache entries")
        print("  clean-all - Remove all cache entries")
        return 0

    command = sys.argv[1]

    if command == "stats":
        cache.print_stats()
    elif command == "clean":
        print("Cleaning old cache entries...")
        cache.clean_cache()
        print("✅ Cache cleaned")
        cache.print_stats()
    elif command == "clean-all":
        print("⚠️  This will remove ALL cache entries.")
        response = input("Continue? (y/N): ")
        if response.lower() == 'y':
            cache.clean_cache(force=True)
            print("✅ All cache entries removed")
        else:
            print("Cancelled")
    else:
        print(f"Unknown command: {command}")
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
