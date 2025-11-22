# Build ROM with Performance Profiling

Build the Game Boy ROM and profile the build performance:

1. Run performance benchmark to establish baseline
2. Profile the build system for bottlenecks
3. Build the ROM
4. Analyze build cache effectiveness
5. Provide optimization recommendations

Execute:

```bash
# Benchmark current performance
python scripts/performance/benchmark_build.py

# Profile build system (with user confirmation)
python scripts/performance/profile_performance.py

# Check cache stats
python scripts/build/cache_manager.py stats

# Build ROM
make build-and-test
```

After completion, report:
- Build time (total and breakdown)
- Memory usage (peak)
- Cache hit rate
- Performance vs. targets
- Bottlenecks identified
- Optimization suggestions
