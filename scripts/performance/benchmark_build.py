#!/usr/bin/env python3
"""
Performance Benchmark for ROM Build Process

Measures build time, validation time, and resource usage.
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).parent.parent.parent
BENCHMARK_LOG = PROJECT_ROOT / "memory" / "benchmark_results.jsonl"


def run_command_timed(command: List[str], description: str) -> Dict:
    """Run a command and measure its execution time.

    Args:
        command: Command to execute as list of strings
        description: Human-readable description of the command

    Returns:
        Dictionary with timing and result information
    """
    print(f"⏱️  {description}...", end="", flush=True)

    start_time = time.time()
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        elapsed_time = time.time() - start_time
        print(f" ✅ {elapsed_time:.2f}s")

        return {
            "command": " ".join(command),
            "description": description,
            "duration_seconds": round(elapsed_time, 3),
            "status": "success",
            "stdout_lines": len(result.stdout.split("\n")),
            "stderr_lines": len(result.stderr.split("\n"))
        }
    except subprocess.CalledProcessError as e:
        elapsed_time = time.time() - start_time
        print(f" ❌ {elapsed_time:.2f}s (FAILED)")

        return {
            "command": " ".join(command),
            "description": description,
            "duration_seconds": round(elapsed_time, 3),
            "status": "failed",
            "error": str(e),
            "returncode": e.returncode
        }


def benchmark_validation() -> Dict:
    """Benchmark asset validation scripts."""
    print("\n📊 Benchmarking Asset Validation\n" + "=" * 50)

    validations = []

    # Background tiles validation
    if (PROJECT_ROOT / "scripts" / "validation" / "check_bg_tiles.py").exists():
        validations.append(run_command_timed(
            ["python3", "scripts/validation/check_bg_tiles.py"],
            "Background tile validation"
        ))

    # Scene limits validation
    if (PROJECT_ROOT / "scripts" / "validation" / "check_scene_limits.py").exists():
        validations.append(run_command_timed(
            ["python3", "scripts/validation/check_scene_limits.py"],
            "Scene limits validation"
        ))

    # JSON schema validation
    if (PROJECT_ROOT / "scripts" / "validation" / "check_json_schema.py").exists():
        validations.append(run_command_timed(
            ["python3", "scripts/validation/check_json_schema.py"],
            "JSON schema validation"
        ))

    total_time = sum(v["duration_seconds"] for v in validations)

    return {
        "total_duration_seconds": round(total_time, 3),
        "validations": validations,
        "validation_count": len(validations)
    }


def benchmark_testing() -> Dict:
    """Benchmark test suite execution."""
    print("\n🧪 Benchmarking Test Suite\n" + "=" * 50)

    test_result = run_command_timed(
        ["pytest", "--tb=no", "-q"],
        "Full test suite"
    )

    return test_result


def benchmark_linting() -> Dict:
    """Benchmark code quality checks."""
    print("\n🔍 Benchmarking Code Quality Checks\n" + "=" * 50)

    checks = []

    # Ruff linting
    checks.append(run_command_timed(
        ["ruff", "check", "."],
        "Ruff linting"
    ))

    # Type checking
    checks.append(run_command_timed(
        ["mypy", "."],
        "Type checking (mypy)"
    ))

    total_time = sum(c["duration_seconds"] for c in checks)

    return {
        "total_duration_seconds": round(total_time, 3),
        "checks": checks,
        "check_count": len(checks)
    }


def save_benchmark_results(results: Dict):
    """Save benchmark results to JSONL log."""
    BENCHMARK_LOG.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "results": results
    }

    with open(BENCHMARK_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"\n📝 Benchmark results saved to: {BENCHMARK_LOG}")


def print_summary(results: Dict):
    """Print benchmark summary."""
    print("\n" + "=" * 50)
    print("📊 BENCHMARK SUMMARY")
    print("=" * 50)

    total_time = 0.0

    if "validation" in results:
        val_time = results["validation"]["total_duration_seconds"]
        total_time += val_time
        print(f"Validation:    {val_time:>7.2f}s ({results['validation']['validation_count']} checks)")

    if "testing" in results:
        test_time = results["testing"]["duration_seconds"]
        total_time += test_time
        print(f"Testing:       {test_time:>7.2f}s")

    if "linting" in results:
        lint_time = results["linting"]["total_duration_seconds"]
        total_time += lint_time
        print(f"Code Quality:  {lint_time:>7.2f}s ({results['linting']['check_count']} checks)")

    print("-" * 50)
    print(f"TOTAL TIME:    {total_time:>7.2f}s")
    print("=" * 50)

    # Performance targets
    print("\n🎯 Performance Targets:")
    print(f"  Validation: {'✅' if results.get('validation', {}).get('total_duration_seconds', 999) < 5 else '❌'} <5s (Target)")
    print(f"  Testing:    {'✅' if results.get('testing', {}).get('duration_seconds', 999) < 15 else '❌'} <15s (Target)")
    print(f"  Linting:    {'✅' if results.get('linting', {}).get('total_duration_seconds', 999) < 10 else '❌'} <10s (Target)")
    print(f"  Total:      {'✅' if total_time < 30 else '❌'} <30s (Target)")


def main():
    """Run all benchmarks."""
    print("🚀 Barry Sharp Pro Mover - Performance Benchmark")
    print("=" * 50)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 50)

    results = {}

    # Benchmark validation
    try:
        results["validation"] = benchmark_validation()
    except Exception as e:
        print(f"❌ Validation benchmark failed: {e}")
        results["validation"] = {"error": str(e)}

    # Benchmark testing
    try:
        results["testing"] = benchmark_testing()
    except Exception as e:
        print(f"❌ Testing benchmark failed: {e}")
        results["testing"] = {"error": str(e)}

    # Benchmark linting
    try:
        results["linting"] = benchmark_linting()
    except Exception as e:
        print(f"❌ Linting benchmark failed: {e}")
        results["linting"] = {"error": str(e)}

    # Print summary
    print_summary(results)

    # Save results
    save_benchmark_results(results)

    print("\n✅ Benchmark complete!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
