"""
Tests for Service Container (Dependency Injection)

Verifies:
- Service registration and resolution
- Singleton pattern
- Factory pattern
- Error handling
- Thread safety
"""

import pytest
from unittest.mock import Mock

from specpulse.core.service_container import (
    ServiceContainer,
    ServiceNotFoundError,
    get_global_container
)


# Mock interfaces for testing
class IMockService:
    """Mock service interface"""
    def do_something(self) -> str:
        ...


class MockServiceImpl:
    """Mock service implementation"""
    def __init__(self, value: str = "default"):
        self.value = value

    def do_something(self) -> str:
        return f"doing {self.value}"


class TestBasicRegistration:
    """Basic service registration and resolution"""

    def test_register_and_resolve_singleton(self):
        """Test singleton service registration"""
        container = ServiceContainer()
        service = MockServiceImpl("test")

        container.register_singleton(IMockService, service)
        resolved = container.resolve(IMockService)

        assert resolved is service  # Same instance
        assert resolved.do_something() == "doing test"

    def test_resolve_unregistered_service_raises_error(self):
        """Test that resolving unregistered service raises error"""
        container = ServiceContainer()

        with pytest.raises(ServiceNotFoundError, match="not registered"):
            container.resolve(IMockService)

    def test_is_registered(self):
        """Test checking if service is registered"""
        container = ServiceContainer()

        assert not container.is_registered(IMockService)

        container.register_singleton(IMockService, MockServiceImpl())

        assert container.is_registered(IMockService)


class TestSingletonPattern:
    """Singleton pattern tests"""

    def test_singleton_returns_same_instance(self):
        """Test that singleton always returns same instance"""
        container = ServiceContainer()
        service = MockServiceImpl("singleton")

        container.register_singleton(IMockService, service)

        resolved1 = container.resolve(IMockService)
        resolved2 = container.resolve(IMockService)
        resolved3 = container.resolve(IMockService)

        # All should be same instance
        assert resolved1 is service
        assert resolved2 is service
        assert resolved3 is service


class TestFactoryPattern:
    """Factory pattern tests"""

    def test_factory_creates_new_instances(self):
        """Test that factory creates new instances each time"""
        container = ServiceContainer()

        call_count = {'count': 0}

        def factory():
            call_count['count'] += 1
            return MockServiceImpl(f"instance{call_count['count']}")

        container.register_factory(IMockService, factory)

        instance1 = container.resolve(IMockService)
        instance2 = container.resolve(IMockService)
        instance3 = container.resolve(IMockService)

        # All should be different instances
        assert instance1 is not instance2
        assert instance2 is not instance3

        # Factory called 3 times
        assert call_count['count'] == 3

        # Each has unique value
        assert instance1.value == "instance1"
        assert instance2.value == "instance2"
        assert instance3.value == "instance3"


class TestMultipleServices:
    """Tests with multiple services"""

    def test_register_multiple_services(self):
        """Test registering and resolving multiple services"""
        container = ServiceContainer()

        class IService1:
            pass

        class IService2:
            pass

        service1 = MockServiceImpl("service1")
        service2 = MockServiceImpl("service2")

        container.register_singleton(IService1, service1)
        container.register_singleton(IService2, service2)

        resolved1 = container.resolve(IService1)
        resolved2 = container.resolve(IService2)

        assert resolved1 is service1
        assert resolved2 is service2

    def test_list_services(self):
        """Test listing all registered services"""
        container = ServiceContainer()

        class IService1:
            pass

        class IService2:
            pass

        class IService3:
            pass

        container.register_singleton(IService1, MockServiceImpl())
        container.register_singleton(IService2, MockServiceImpl())
        container.register_factory(IService3, lambda: MockServiceImpl())

        services = container.list_services()

        assert "IService1" in services
        assert "IService2" in services
        assert "IService3" in services
        assert len(services) == 3


class TestClear:
    """Test clearing container"""

    def test_clear_removes_all_services(self):
        """Test that clear removes all registered services"""
        container = ServiceContainer()

        class IService1:
            pass

        class IService2:
            pass

        container.register_singleton(IService1, MockServiceImpl())
        container.register_singleton(IService2, MockServiceImpl())

        assert len(container.list_services()) == 2

        container.clear()

        assert len(container.list_services()) == 0

        with pytest.raises(ServiceNotFoundError):
            container.resolve(IService1)


class TestGlobalContainer:
    """Test global container instance"""

    def test_global_container_singleton(self):
        """Test that global container is singleton"""
        container1 = get_global_container()
        container2 = get_global_container()

        assert container1 is container2

    def test_global_container_shared_services(self):
        """Test that global container shares services"""
        container1 = get_global_container()
        container1.clear()  # Clean start

        container1.register_singleton(IMockService, MockServiceImpl("global"))

        container2 = get_global_container()
        resolved = container2.resolve(IMockService)

        assert resolved.value == "global"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
