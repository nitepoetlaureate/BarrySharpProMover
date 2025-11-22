# Optimize Build Cache

Manage and optimize the build cache for faster builds:

1. Show current cache statistics
2. Identify cache effectiveness
3. Clean old/unused cache entries
4. Provide caching recommendations

Execute:

```bash
# Show cache stats
python scripts/build/cache_manager.py stats

# Clean old entries (keeps recent, removes old)
python scripts/build/cache_manager.py clean

# Clean all cache (complete reset)
# python scripts/build/cache_manager.py clean-all
```

Analyze and report:
- Total cache entries
- Cache size (MB)
- Cache hit rate
- Space savings from caching
- Recommendations for improving cache effectiveness

If cache hit rate is low (<50%), suggest:
- Verifying dependencies are stable
- Checking if assets change frequently
- Consider disabling cache for rapid development
- Re-enable cache for production builds

If cache is large (>400MB), suggest:
- Running clean to remove old entries
- Reviewing cache retention policy
- Considering cache size limits
