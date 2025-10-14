"""
Service Container for Dependency Injection

This module provides a lightweight dependency injection container that:
- Registers service implementations
- Resolves dependencies at runtime
- Supports singleton and factory patterns
- Enables loose coupling and testability

Usage:
    >>> container = ServiceContainer()
    >>> container.register(ITemplateProvider, TemplateProviderImpl())
    >>> template_provider = container.resolve(ITemplateProvider)
"""

from typing import Any, Callable, Dict, List, Optional, Type, TypeVar
import threading
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class ServiceNotFoundError(Exception):
    """Raised when a service is not registered"""
    pass


class ServiceContainer:
    """
    Lightweight dependency injection container.

    Supports:
    - Singleton services (single instance)
    - Factory services (new instance per resolution)
    - Lazy initialization
    - Thread-safe operations

    Example:
        >>> from specpulse.core.interfaces import ITemplateProvider
        >>> from specpulse.core.template_provider import TemplateProvider
        >>>
        >>> container = ServiceContainer()
        >>> container.register_singleton(ITemplateProvider, TemplateProvider(project_root))
        >>> template_provider = container.resolve(ITemplateProvider)
    """

    def __init__(self):
        """Initialize service container"""
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def register(self, interface: Type[T], implementation: T, singleton: bool = True):
        """
        Register a service implementation.

        Args:
            interface: Interface class/Protocol
            implementation: Implementation instance or factory function
            singleton: If True, use same instance; if False, call factory

        Example:
            >>> container.register(ITemplateProvider, template_provider)
            >>> container.register(IMemoryProvider, lambda: MemoryProvider(), singleton=False)
        """
        with self._lock:
            service_name = self._get_service_name(interface)

            if callable(implementation) and not hasattr(implementation, '__dict__'):
                # It's a factory function
                self._factories[service_name] = implementation
                logger.debug(f"Registered factory for: {service_name}")
            else:
                # It's an instance
                if singleton:
                    self._singletons[service_name] = implementation
                    logger.debug(f"Registered singleton for: {service_name}")
                else:
                    self._services[service_name] = implementation
                    logger.debug(f"Registered service for: {service_name}")

    def register_singleton(self, interface: Type[T], implementation: T):
        """
        Register a singleton service (convenience method).

        Args:
            interface: Interface class/Protocol
            implementation: Implementation instance

        Example:
            >>> container.register_singleton(ITemplateProvider, template_provider)
        """
        self.register(interface, implementation, singleton=True)

    def register_factory(self, interface: Type[T], factory: Callable[[], T]):
        """
        Register a factory for creating service instances.

        Args:
            interface: Interface class/Protocol
            factory: Factory function that creates instances

        Example:
            >>> container.register_factory(
            ...     IMemoryProvider,
            ...     lambda: MemoryProvider(project_root)
            ... )
        """
        with self._lock:
            service_name = self._get_service_name(interface)
            self._factories[service_name] = factory
            logger.debug(f"Registered factory for: {service_name}")

    def resolve(self, interface: Type[T]) -> T:
        """
        Resolve service implementation.

        Args:
            interface: Interface class/Protocol to resolve

        Returns:
            Service implementation instance

        Raises:
            ServiceNotFoundError: If service not registered

        Example:
            >>> template_provider = container.resolve(ITemplateProvider)
        """
        with self._lock:
            service_name = self._get_service_name(interface)

            # Check singletons first (most common)
            if service_name in self._singletons:
                logger.debug(f"Resolved singleton: {service_name}")
                return self._singletons[service_name]

            # Check factories
            if service_name in self._factories:
                logger.debug(f"Creating instance via factory: {service_name}")
                instance = self._factories[service_name]()
                return instance

            # Check regular services
            if service_name in self._services:
                logger.debug(f"Resolved service: {service_name}")
                return self._services[service_name]

            # Not found
            raise ServiceNotFoundError(
                f"Service not registered: {service_name}. "
                f"Available services: {self.list_services()}"
            )

    def is_registered(self, interface: Type) -> bool:
        """
        Check if service is registered.

        Args:
            interface: Interface class/Protocol

        Returns:
            True if registered, False otherwise
        """
        service_name = self._get_service_name(interface)
        return (
            service_name in self._singletons or
            service_name in self._factories or
            service_name in self._services
        )

    def list_services(self) -> List[str]:
        """
        List all registered services.

        Returns:
            List of service names
        """
        all_services = set()
        all_services.update(self._singletons.keys())
        all_services.update(self._factories.keys())
        all_services.update(self._services.keys())
        return sorted(all_services)

    def clear(self):
        """Clear all registered services"""
        with self._lock:
            self._services.clear()
            self._factories.clear()
            self._singletons.clear()
            logger.info("Service container cleared")

    def _get_service_name(self, interface: Type) -> str:
        """
        Get service name from interface.

        Args:
            interface: Interface class/Protocol

        Returns:
            Service name (interface name)
        """
        # Use __name__ for Protocol interfaces
        if hasattr(interface, '__name__'):
            return interface.__name__
        # Fallback to string representation
        return str(interface)


# Global service container instance
_global_container: Optional[ServiceContainer] = None
_container_lock = threading.Lock()


def get_global_container() -> ServiceContainer:
    """
    Get global shared service container.

    This ensures a single container is used throughout the application.

    Returns:
        Global ServiceContainer instance

    Example:
        >>> container = get_global_container()
        >>> container.register_singleton(ITemplateProvider, provider)
    """
    global _global_container

    with _container_lock:
        if _global_container is None:
            _global_container = ServiceContainer()
            logger.debug("Created global service container")

        return _global_container


__all__ = [
    'ServiceContainer',
    'ServiceNotFoundError',
    'get_global_container',
]
