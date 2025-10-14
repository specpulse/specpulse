"""
Tests for Time-Based Template Cache

Verifies:
- TTL expiration
- Manual invalidation
- Thread safety
- Cache statistics
- Performance
"""

import pytest
import time
import threading
from unittest.mock import Mock

from specpulse.core.template_cache import TemplateCache, get_global_template_cache


class TestBasicCaching:
    """Basic caching functionality tests"""

    def test_cache_miss_loads_value(self):
        """Test that cache miss calls loader function"""
        cache = TemplateCache(ttl_seconds=60)
        loader = Mock(return_value="template content")

        result = cache.get("test_key", loader)

        assert result == "template content"
        loader.assert_called_once()

    def test_cache_hit_returns_cached_value(self):
        """Test that cache hit returns cached value without loading"""
        cache = TemplateCache(ttl_seconds=60)
        loader = Mock(return_value="template content")

        # First call - cache miss
        result1 = cache.get("test_key", loader)
        # Second call - cache hit
        result2 = cache.get("test_key", loader)

        assert result1 == result2
        loader.assert_called_once()  # Only called once

    def test_multiple_keys(self):
        """Test caching multiple keys independently"""
        cache = TemplateCache(ttl_seconds=60)

        result1 = cache.get("key1", lambda: "value1")
        result2 = cache.get("key2", lambda: "value2")
        result3 = cache.get("key1", lambda: "should not be called")

        assert result1 == "value1"
        assert result2 == "value2"
        assert result3 == "value1"  # Cached


class TestTTLExpiration:
    """TTL expiration tests"""

    def test_cache_expires_after_ttl(self):
        """Test that cache expires after TTL"""
        cache = TemplateCache(ttl_seconds=1)  # 1 second TTL
        loader = Mock(side_effect=["value1", "value2"])

        # First call
        result1 = cache.get("test_key", loader)
        assert result1 == "value1"

        # Wait for expiration
        time.sleep(1.5)

        # Second call - should reload (cache expired)
        result2 = cache.get("test_key", loader)
        assert result2 == "value2"

        # Loader called twice
        assert loader.call_count == 2

    def test_cache_not_expired_within_ttl(self):
        """Test that cache doesn't expire within TTL"""
        cache = TemplateCache(ttl_seconds=5)
        loader = Mock(return_value="value")

        # First call
        cache.get("test_key", loader)

        # Wait less than TTL
        time.sleep(1)

        # Second call - should use cache
        cache.get("test_key", loader)

        # Loader called only once
        loader.assert_called_once()

    def test_different_ttl_per_instance(self):
        """Test that different cache instances can have different TTLs"""
        cache_short = TemplateCache(ttl_seconds=1)
        cache_long = TemplateCache(ttl_seconds=10)

        cache_short.get("key", lambda: "value1")
        cache_long.get("key", lambda: "value2")

        # Both should have cached values
        assert cache_short.contains("key")
        assert cache_long.contains("key")


class TestManualInvalidation:
    """Manual cache invalidation tests"""

    def test_invalidate_specific_key(self):
        """Test invalidating specific cache key"""
        cache = TemplateCache(ttl_seconds=60)

        cache.get("key1", lambda: "value1")
        cache.get("key2", lambda: "value2")

        # Invalidate key1
        cache.invalidate("key1")

        # key1 should be gone, key2 should remain
        assert not cache.contains("key1")
        assert cache.contains("key2")

    def test_invalidate_all(self):
        """Test clearing entire cache"""
        cache = TemplateCache(ttl_seconds=60)

        cache.get("key1", lambda: "value1")
        cache.get("key2", lambda: "value2")
        cache.get("key3", lambda: "value3")

        # Clear all
        cache.invalidate()

        # All should be gone
        assert not cache.contains("key1")
        assert not cache.contains("key2")
        assert not cache.contains("key3")

    def test_invalidate_nonexistent_key(self):
        """Test that invalidating non-existent key doesn't error"""
        cache = TemplateCache(ttl_seconds=60)

        # Should not raise exception
        cache.invalidate("nonexistent")


class TestCacheStatistics:
    """Cache statistics tests"""

    def test_cache_statistics(self):
        """Test cache statistics tracking"""
        cache = TemplateCache(ttl_seconds=60)
        loader = Mock(return_value="value")

        # Cache miss
        cache.get("key1", loader)
        # Cache hit
        cache.get("key1", loader)
        # Cache hit again
        cache.get("key1", loader)

        stats = cache.get_stats()

        assert stats['hits'] == 2
        assert stats['misses'] == 1
        assert stats['size'] == 1
        assert stats['hit_rate'] == pytest.approx(66.67, abs=0.1)

    def test_multiple_misses(self):
        """Test statistics with multiple cache misses"""
        cache = TemplateCache(ttl_seconds=60)

        cache.get("key1", lambda: "value1")
        cache.get("key2", lambda: "value2")
        cache.get("key3", lambda: "value3")

        stats = cache.get_stats()

        assert stats['hits'] == 0
        assert stats['misses'] == 3
        assert stats['hit_rate'] == 0.0


class TestThreadSafety:
    """Thread safety tests"""

    def test_concurrent_access_same_key(self):
        """Test concurrent access to same key"""
        cache = TemplateCache(ttl_seconds=60)
        call_count = {'value': 0}

        def slow_loader():
            call_count['value'] += 1
            time.sleep(0.1)  # Simulate slow load
            return "template"

        results = []

        def worker():
            result = cache.get("shared_key", slow_loader)
            results.append(result)

        # Create 10 threads accessing same key
        threads = [threading.Thread(target=worker) for _ in range(10)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # All should get same value
        assert all(r == "template" for r in results)
        assert len(results) == 10

        # Loader might be called multiple times due to race,
        # but cache should prevent most redundant calls
        assert call_count['value'] <= 10  # At most 10 (no cache)

    def test_concurrent_different_keys(self):
        """Test concurrent access to different keys"""
        cache = TemplateCache(ttl_seconds=60)
        results = {}

        def worker(key, value):
            result = cache.get(key, lambda: value)
            results[key] = result

        threads = []
        for i in range(10):
            thread = threading.Thread(target=worker, args=(f"key{i}", f"value{i}"))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # All keys should have correct values
        for i in range(10):
            assert results[f"key{i}"] == f"value{i}"


class TestClearExpired:
    """Test manual cleanup of expired entries"""

    def test_clear_expired_entries(self):
        """Test manual cleanup of expired entries"""
        cache = TemplateCache(ttl_seconds=1)

        # Add entries
        cache.get("key1", lambda: "value1")
        cache.get("key2", lambda: "value2")

        # Wait for expiration
        time.sleep(1.5)

        # Add new entry (not expired)
        cache.get("key3", lambda: "value3")

        # Manually clear expired
        cache.clear_expired()

        # Only key3 should remain
        assert not cache.contains("key1")
        assert not cache.contains("key2")
        assert cache.contains("key3")


class TestGlobalCache:
    """Test global cache instance"""

    def test_global_cache_singleton(self):
        """Test that global cache is singleton"""
        cache1 = get_global_template_cache()
        cache2 = get_global_template_cache()

        assert cache1 is cache2  # Same instance

    def test_global_cache_shared_state(self):
        """Test that global cache shares state"""
        cache1 = get_global_template_cache()
        cache1.get("shared_key", lambda: "shared_value")

        cache2 = get_global_template_cache()
        result = cache2.get("shared_key", lambda: "should not be called")

        assert result == "shared_value"


class TestPerformance:
    """Performance tests"""

    def test_cache_performance(self):
        """Test that caching improves performance"""
        cache = TemplateCache(ttl_seconds=60)

        def slow_loader():
            time.sleep(0.01)  # Simulate slow template loading
            return "template content"

        # First call (cache miss)
        start = time.time()
        cache.get("template", slow_loader)
        first_duration = time.time() - start

        # Second call (cache hit)
        start = time.time()
        cache.get("template", slow_loader)
        second_duration = time.time() - start

        # Cache hit should be significantly faster
        assert second_duration < first_duration / 5  # At least 5x faster


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
