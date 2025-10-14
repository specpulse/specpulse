"""
Time-Based Template Cache with TTL (Time-To-Live)

This module provides a template caching system that:
- Caches templates for performance
- Expires cached templates after TTL (default 5 minutes)
- Allows manual cache invalidation
- Prevents stale cache issues when templates are updated

CRITICAL: This replaces @lru_cache to prevent serving stale templates
when users update template files.
"""

from typing import Dict, Tuple, Callable, Optional, Any
from pathlib import Path
import time
import threading
import logging

logger = logging.getLogger(__name__)


class TemplateCache:
    """
    Time-aware template cache with TTL expiration.

    Templates are cached in memory but expire after a configurable TTL.
    This prevents serving stale templates while maintaining performance.

    Thread-safe implementation using locks for concurrent access.

    Example:
        >>> cache = TemplateCache(ttl_seconds=300)  # 5 min TTL
        >>> def load_spec():
        ...     return Path("spec.md").read_text()
        >>> template = cache.get("spec_template", load_spec)
        >>> # Cached for 5 minutes, then reloaded
    """

    def __init__(self, ttl_seconds: int = 300):
        """
        Initialize template cache.

        Args:
            ttl_seconds: Time-to-live in seconds (default: 300 = 5 minutes)
        """
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._lock = threading.Lock()  # Thread-safe access
        self._hits = 0
        self._misses = 0

    def get(self, key: str, loader: Callable[[], Any]) -> Any:
        """
        Get item from cache or load it.

        If key exists and hasn't expired, return cached value.
        Otherwise, call loader function and cache the result.

        Args:
            key: Cache key
            loader: Function to call if cache miss (must return the value)

        Returns:
            Cached or freshly loaded value

        Example:
            >>> cache = TemplateCache()
            >>> def load_template():
            ...     return Path("template.md").read_text()
            >>> template = cache.get("my_template", load_template)
        """
        with self._lock:
            now = time.time()

            # Check if key exists and is not expired
            if key in self._cache:
                value, timestamp = self._cache[key]
                age = now - timestamp

                if age < self.ttl_seconds:
                    # Cache hit
                    self._hits += 1
                    logger.debug(f"Cache HIT for key '{key}' (age: {age:.1f}s)")
                    return value
                else:
                    # Cache expired
                    logger.debug(f"Cache EXPIRED for key '{key}' (age: {age:.1f}s, TTL: {self.ttl_seconds}s)")
                    del self._cache[key]

            # Cache miss or expired - load fresh value
            self._misses += 1
            logger.debug(f"Cache MISS for key '{key}' - loading fresh value")

            try:
                value = loader()
                self._cache[key] = (value, now)
                return value
            except Exception as e:
                logger.error(f"Failed to load value for key '{key}': {e}")
                raise

    def invalidate(self, key: Optional[str] = None):
        """
        Invalidate cache entry or entire cache.

        Args:
            key: Specific key to invalidate, or None to clear all

        Example:
            >>> cache.invalidate("spec_template")  # Invalidate one
            >>> cache.invalidate()  # Clear all
        """
        with self._lock:
            if key is None:
                # Clear entire cache
                count = len(self._cache)
                self._cache.clear()
                logger.info(f"Cache cleared ({count} items removed)")
            else:
                # Remove specific key
                if key in self._cache:
                    del self._cache[key]
                    logger.debug(f"Invalidated cache key: '{key}'")
                else:
                    logger.debug(f"Cache key not found: '{key}'")

    def contains(self, key: str) -> bool:
        """
        Check if key is in cache (and not expired).

        Args:
            key: Cache key to check

        Returns:
            True if key exists and is not expired
        """
        with self._lock:
            if key not in self._cache:
                return False

            _, timestamp = self._cache[key]
            age = time.time() - timestamp
            return age < self.ttl_seconds

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics:
            - size: Number of cached items
            - hits: Number of cache hits
            - misses: Number of cache misses
            - hit_rate: Cache hit rate (0-100%)

        Example:
            >>> stats = cache.get_stats()
            >>> print(f"Hit rate: {stats['hit_rate']:.1f}%")
        """
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = (self._hits / total_requests * 100) if total_requests > 0 else 0

            return {
                'size': len(self._cache),
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate': hit_rate,
                'ttl_seconds': self.ttl_seconds
            }

    def clear_expired(self):
        """
        Manually clear expired entries.

        This is called automatically during get(), but can be called
        manually for cleanup.
        """
        with self._lock:
            now = time.time()
            expired_keys = []

            for key, (_, timestamp) in self._cache.items():
                age = now - timestamp
                if age >= self.ttl_seconds:
                    expired_keys.append(key)

            for key in expired_keys:
                del self._cache[key]

            if expired_keys:
                logger.info(f"Cleared {len(expired_keys)} expired cache entries")

    def set_ttl(self, ttl_seconds: int):
        """
        Update TTL for future cache entries.

        Args:
            ttl_seconds: New TTL in seconds
        """
        self.ttl_seconds = ttl_seconds
        logger.info(f"Cache TTL updated to {ttl_seconds} seconds")


# Global template cache instance (shared across modules)
_global_template_cache: Optional[TemplateCache] = None


def get_global_template_cache(ttl_seconds: int = 300) -> TemplateCache:
    """
    Get global shared template cache instance.

    This ensures a single cache is shared across all SpecPulse instances
    for better memory efficiency.

    Args:
        ttl_seconds: TTL for cache (only used on first call)

    Returns:
        Global TemplateCache instance
    """
    global _global_template_cache

    if _global_template_cache is None:
        _global_template_cache = TemplateCache(ttl_seconds=ttl_seconds)
        logger.debug(f"Created global template cache (TTL: {ttl_seconds}s)")

    return _global_template_cache


__all__ = ['TemplateCache', 'get_global_template_cache']
