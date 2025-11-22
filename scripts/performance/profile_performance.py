#!/usr/bin/env python3
"""
Advanced Performance Profiler for Barry Sharp Pro Mover

Provides detailed profiling using cProfile and memory_profiler.
"""

import cProfile
import pstats
import io
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Callable, Any
import subprocess

PROJECT_ROOT = Path(__file__).parent.parent.parent
PROFILE_DIR = PROJECT_ROOT / "memory" / "profiles"


def profile_function(func: Callable, *args, **kwargs) -> tuple[Any, dict]:
    """Profile a function's execution time and memory usage.

    Args:
        func: Function to profile
        *args: Function arguments
        **kwargs: Function keyword arguments

    Returns:
        Tuple of (function_result, profile_stats)
    """
    # Create profile directory
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    # Start memory tracking
    tracemalloc.start()

    # CPU profiling
    profiler = cProfile.Profile()
    profiler.enable()

    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()

    profiler.disable()

    # Get memory stats
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Generate stats
    stats_stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stats_stream)
    stats.sort_stats('cumulative')
    stats.print_stats(30)  # Top 30 functions

    profile_data = {
        'execution_time': end_time - start_time,
        'memory_current': current / 1024 / 1024,  # MB
        'memory_peak': peak / 1024 / 1024,  # MB
        'cpu_profile': stats_stream.getvalue()
    }

    return result, profile_data


def profile_build_system():
    """Profile the entire build system."""
    print("🔍 Profiling Build System\n" + "=" * 60)

    def run_build():
        """Run the build process."""
        result = subprocess.run(
            ["make", "build-rom"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        return result.returncode == 0

    _, profile_data = profile_function(run_build)

    print(f"\n⏱️  Total Build Time: {profile_data['execution_time']:.2f}s")
    print(f"💾 Memory Usage (Current): {profile_data['memory_current']:.2f} MB")
    print(f"💾 Memory Usage (Peak): {profile_data['memory_peak']:.2f} MB")

    # Save detailed profile
    profile_file = PROFILE_DIR / f"build_profile_{int(time.time())}.txt"
    with open(profile_file, 'w') as f:
        f.write("Build System Performance Profile\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Execution Time: {profile_data['execution_time']:.2f}s\n")
        f.write(f"Memory (Current): {profile_data['memory_current']:.2f} MB\n")
        f.write(f"Memory (Peak): {profile_data['memory_peak']:.2f} MB\n\n")
        f.write("CPU Profile (Top 30 Functions):\n")
        f.write(profile_data['cpu_profile'])

    print(f"\n📝 Detailed profile saved to: {profile_file}")

    return profile_data


def profile_validation_scripts():
    """Profile validation scripts."""
    print("\n🔍 Profiling Validation Scripts\n" + "=" * 60)

    validation_scripts = [
        ("Background Tiles", "scripts/validation/check_bg_tiles.py"),
        ("Scene Limits", "scripts/validation/check_scene_limits.py"),
        ("JSON Schema", "scripts/validation/check_json_schema.py"),
    ]

    results = []

    for name, script_path in validation_scripts:
        full_path = PROJECT_ROOT / script_path
        if not full_path.exists():
            print(f"⚠️  {name}: Script not found")
            continue

        def run_validation():
            result = subprocess.run(
                ["python3", str(full_path)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True
            )
            return result.returncode == 0

        _, profile_data = profile_function(run_validation)

        print(f"\n{name}:")
        print(f"  Time: {profile_data['execution_time']:.3f}s")
        print(f"  Memory Peak: {profile_data['memory_peak']:.2f} MB")

        results.append({
            'name': name,
            'time': profile_data['execution_time'],
            'memory': profile_data['memory_peak']
        })

    # Save summary
    summary_file = PROFILE_DIR / f"validation_profile_{int(time.time())}.txt"
    with open(summary_file, 'w') as f:
        f.write("Validation Scripts Performance Profile\n")
        f.write("=" * 60 + "\n\n")
        for result in results:
            f.write(f"{result['name']}:\n")
            f.write(f"  Execution Time: {result['time']:.3f}s\n")
            f.write(f"  Memory Peak: {result['memory']:.2f} MB\n\n")

    print(f"\n📝 Summary saved to: {summary_file}")

    return results


def profile_test_suite():
    """Profile the test suite."""
    print("\n🔍 Profiling Test Suite\n" + "=" * 60)

    def run_tests():
        result = subprocess.run(
            ["pytest", "--tb=no", "-q"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        return result.returncode == 0

    _, profile_data = profile_function(run_tests)

    print(f"\n⏱️  Total Test Time: {profile_data['execution_time']:.2f}s")
    print(f"💾 Memory Peak: {profile_data['memory_peak']:.2f} MB")

    # Save profile
    profile_file = PROFILE_DIR / f"test_profile_{int(time.time())}.txt"
    with open(profile_file, 'w') as f:
        f.write("Test Suite Performance Profile\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Execution Time: {profile_data['execution_time']:.2f}s\n")
        f.write(f"Memory Peak: {profile_data['memory_peak']:.2f} MB\n\n")
        f.write("CPU Profile (Top 30 Functions):\n")
        f.write(profile_data['cpu_profile'])

    print(f"📝 Detailed profile saved to: {profile_file}")

    return profile_data


def analyze_bottlenecks():
    """Analyze and report performance bottlenecks."""
    print("\n📊 Performance Bottleneck Analysis\n" + "=" * 60)

    # This would analyze the saved profiles
    profile_files = sorted(PROFILE_DIR.glob("*.txt"))

    if not profile_files:
        print("⚠️  No profiles found. Run profiling first.")
        return

    print(f"\n✅ Found {len(profile_files)} profile(s)")
    print("\nRecent profiles:")
    for pf in profile_files[-5:]:
        print(f"  - {pf.name}")

    print("\n💡 Optimization Suggestions:")
    print("  1. Check CPU profiles for functions taking >10% of time")
    print("  2. Look for memory peaks >100MB")
    print("  3. Consider caching for repeated operations")
    print("  4. Profile before and after optimizations")


def main():
    """Run all profiling operations."""
    print("🚀 Barry Sharp Pro Mover - Advanced Performance Profiler")
    print("=" * 60)

    try:
        # Profile validation scripts (fast)
        profile_validation_scripts()

        # Profile test suite
        profile_test_suite()

        # Profile build system (slow - optional)
        print("\n⚠️  Build system profiling can take several minutes.")
        response = input("Profile build system? (y/N): ")
        if response.lower() == 'y':
            profile_build_system()
        else:
            print("Skipping build system profiling.")

        # Analyze bottlenecks
        analyze_bottlenecks()

        print("\n✅ Profiling complete!")
        print(f"📁 Profiles saved to: {PROFILE_DIR}")

    except KeyboardInterrupt:
        print("\n\n⚠️  Profiling interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error during profiling: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
