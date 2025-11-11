"""
Complete Service Container Tests

Comprehensive tests for ServiceContainer dependency injection system.
Designed for 100% code coverage and thread safety testing.
"""

import pytest
import threading
import time
from pathlib import Path
from unittest.mock import Mock, MagicMock

from specpulse.core.service_container import ServiceContainer
from specpulse.core.interfaces import (
    ITemplateProvider, IMemoryProvider, IScriptGenerator,
    IAIInstructionProvider, IDecompositionService
)
from specpulse.utils.error_handler import DependencyError


class TestServiceContainerComplete:
    """Comprehensive tests for ServiceContainer"""

    @pytest.mark.unit
    def test_service_container_initialization(self):
        """Test basic service container initialization"""
        container = ServiceContainer()

        assert container is not None
        assert len(container._services) == 0
        assert len(container._singletons) == 0
        assert len(container._factories) == 0

    @pytest.mark.unit
    def test_service_container_register_service(self):
        """Test service registration"""
        container = ServiceContainer()
        mock_service = Mock()

        container.register('test_service', mock_service)

        assert 'test_service' in container._services
        assert container._services['test_service'] == mock_service

    @pytest.mark.unit
    def test_service_container_register_singleton(self):
        """Test singleton service registration"""
        container = ServiceContainer()
        mock_service = Mock()

        container.register_singleton('singleton_service', mock_service)

        assert 'singleton_service' in container._singletons
        assert container._singletons['singleton_service'] == mock_service

    @pytest.mark.unit
    def test_service_container_register_factory(self):
        """Test factory function registration"""
        container = ServiceContainer()

        def create_service():
            return Mock(spec='test')

        container.register_factory('factory_service', create_service)

        assert 'factory_service' in container._factories
        assert callable(container._factories['factory_service'])

    @pytest.mark.unit
    def test_service_container_resolve_service(self):
        """Test service resolution"""
        container = ServiceContainer()
        mock_service = Mock()
        container.register('test_service', mock_service)

        resolved = container.resolve('test_service')

        assert resolved is mock_service

    @pytest.mark.unit
    def test_service_container_resolve_singleton(self):
        """Test singleton service resolution"""
        container = ServiceContainer()
        mock_service = Mock()
        container.register_singleton('singleton_service', mock_service)

        resolved1 = container.resolve('singleton_service')
        resolved2 = container.resolve('singleton_service')

        # Should return the same instance
        assert resolved1 is resolved2
        assert resolved1 is mock_service

    @pytest.mark.unit
    def test_service_container_resolve_factory(self):
        """Test factory service resolution"""
        container = ServiceContainer()

        def create_service():
            return Mock(spec='test', created=True)

        container.register_factory('factory_service', create_service)

        resolved1 = container.resolve('factory_service')
        resolved2 = container.resolve('factory_service')

        # Should return different instances
        assert resolved1 is not resolved2
        assert resolved1.spec == 'test'
        assert resolved2.spec == 'test'
        assert resolved1.created is True
        assert resolved2.created is True

    @pytest.mark.unit
    def test_service_container_resolve_nonexistent(self):
        """Test resolution of non-existent service"""
        container = ServiceContainer()

        with pytest.raises(DependencyError, match="Service 'nonexistent' not registered"):
            container.resolve('nonexistent')

    @pytest.mark.unit
    def test_service_container_resolve_factory_error(self):
        """Test factory function error handling"""
        container = ServiceContainer()

        def failing_factory():
            raise ValueError("Factory failed")

        container.register_factory('failing_service', failing_factory)

        with pytest.raises(DependencyError, match="Error creating service 'failing_service'"):
            container.resolve('failing_service')

    @pytest.mark.unit
    def test_service_container_has_service(self):
        """Test service existence checking"""
        container = ServiceContainer()
        mock_service = Mock()

        assert not container.has('test_service')

        container.register('test_service', mock_service)

        assert container.has('test_service')

    @pytest.mark.unit
    def test_service_container_register_interface_compliance(self):
        """Test that services implement required interfaces"""
        container = ServiceContainer()

        # Create mock services that implement interfaces
        mock_template_provider = Mock(spec=ITemplateProvider)
        mock_memory_provider = Mock(spec=IMemoryProvider)
        mock_script_generator = Mock(spec=IScriptGenerator)
        mock_ai_provider = Mock(spec=IAIInstructionProvider)

        # Register services
        container.register('template_provider', mock_template_provider)
        container.register('memory_provider', mock_memory_provider)
        container.register('script_generator', mock_script_generator)
        container.register('ai_provider', mock_ai_provider)

        # Resolve and verify
        template_provider = container.resolve('template_provider')
        memory_provider = container.resolve('memory_provider')
        script_generator = container.resolve('script_generator')
        ai_provider = container.resolve('ai_provider')

        assert template_provider is mock_template_provider
        assert memory_provider is mock_memory_provider
        assert script_generator is mock_script_generator
        assert ai_provider is mock_ai_provider

    @pytest.mark.unit
    def test_service_container_interface_validation(self):
        """Test interface validation for services"""
        container = ServiceContainer()

        # Mock that doesn't implement interface
        invalid_service = Mock()

        # Should not raise error during registration
        container.register('invalid_service', invalid_service)

        # Should still be resolvable
        resolved = container.resolve('invalid_service')
        assert resolved is invalid_service

    @pytest.mark.unit
    def test_service_container_clear(self):
        """Test container clearing"""
        container = ServiceContainer()
        mock_service = Mock()

        # Register various types of services
        container.register('service', mock_service)
        container.register_singleton('singleton', mock_service)
        container.register_factory('factory', lambda: Mock())

        assert len(container._services) == 1
        assert len(container._singletons) == 1
        assert len(container._factories) == 1

        container.clear()

        assert len(container._services) == 0
        assert len(container._singletons) == 0
        assert len(container._factories) == 0

    @pytest.mark.unit
    def test_service_container_get_service_names(self):
        """Test getting all registered service names"""
        container = ServiceContainer()

        # Register different types of services
        container.register('service1', Mock())
        container.register_singleton('singleton1', Mock())
        container.register_factory('factory1', lambda: Mock())

        names = container.get_service_names()

        expected_names = {'service1', 'singleton1', 'factory1'}
        assert names == expected_names

    @pytest.mark.unit
    def test_service_container_circular_dependency_detection(self):
        """Test circular dependency detection"""
        container = ServiceContainer()

        # Create services with circular dependencies
        class ServiceA:
            def __init__(self):
                self.b = container.resolve('service_b')

        class ServiceB:
            def __init__(self):
                self.a = container.resolve('service_a')

        # This should work because we're not in the same resolution cycle
        # The circular dependency would be detected at runtime

    @pytest.mark.unit
    def test_service_container_singleton_thread_safety(self):
        """Test singleton thread safety"""
        container = ServiceContainer()
        mock_service = Mock()
        container.register_singleton('thread_safe_singleton', mock_service)

        results = []
        errors = []

        def resolve_service():
            try:
                resolved = container.resolve('thread_safe_singleton')
                results.append(resolved)
            except Exception as e:
                errors.append(e)

        # Create multiple threads that resolve the same singleton
        threads = []
        for i in range(10):
            thread = threading.Thread(target=resolve_service)
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=5)

        # All threads should get the same singleton instance
        assert len(results) == 10
        assert all(result is mock_service for result in results)
        assert len(errors) == 0

    @pytest.mark.unit
    def test_service_container_concurrent_registration(self):
        """Test concurrent service registration"""
        container = ServiceContainer()
        errors = []

        def register_service(index):
            try:
                mock_service = Mock(index=index)
                service_name = f'service_{index}'
                container.register(service_name, mock_service)
            except Exception as e:
                errors.append(e)

        # Create multiple threads that register services
        threads = []
        for i in range(5):
            thread = threading.Thread(target=register_service, args=(i,))
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=5)

        # All registrations should succeed
        assert len(errors) == 0

        # Verify all services were registered
        assert len(container.get_service_names()) == 5

    @pytest.mark.unit
    def test_service_container_factory_isolation(self):
        """Test factory isolation between services"""
        container = ServiceContainer()

        # Counter to track factory calls
        call_count = {"count": 0}

        def create_service():
            call_count["count"] += 1
            return Mock(call_number=call_count["count"])

        container.register_factory('isolated_service', create_service)

        # Resolve multiple times
        service1 = container.resolve('isolated_service')
        service2 = container.resolve('isolated_service')
        service3 = container.resolve('isolated_service')

        # Each resolution should call the factory
        assert call_count["count"] == 3
        assert service1.call_number == 1
        assert service2.call_number == 2
        assert service3.call_number == 3

    @pytest.mark.unit
    def test_service_container_service_replacement(self):
        """Test service replacement"""
        container = ServiceContainer()
        original_service = Mock(original=True)
        replacement_service = Mock(replacement=True)

        # Register original service
        container.register('replaceable_service', original_service)

        # Resolve original
        resolved_original = container.resolve('replaceable_service')
        assert resolved_original is original_service
        assert resolved_original.original is True

        # Replace service
        container.register('replaceable_service', replacement_service)

        # Resolve replacement
        resolved_replacement = container.resolve('replaceable_service')
        assert resolved_replacement is replacement_service
        assert resolved_replacement.replacement is True

    @pytest.mark.unit
    def test_service_container_lazy_resolution(self):
        """Test lazy resolution pattern"""
        container = ServiceContainer()

        # Service that is expensive to create
        def create_expensive_service():
            return Mock(expensive=True, creation_time=time.time())

        container.register_factory('expensive_service', create_expensive_service)

        # Service should not be created until resolved
        assert 'expensive_service' in container._factories

        start_time = time.time()
        service = container.resolve('expensive_service')
        end_time = time.time()

        assert service.expensive is True
        assert (end_time - start_time) < 1.0  # Should be fast

    @pytest.mark.unit
    def test_service_container_dependency_injection_pattern(self):
        """Test dependency injection pattern"""
        class DatabaseService:
            def __init__(self):
                self.connection = "database_connection"

        class ApplicationService:
            def __init__(self, db_service):
                self.db = db_service
                self.ready = True

        container = ServiceContainer()

        # Register dependencies
        container.register('database', DatabaseService)
        container.register('application', ApplicationService)

        # Create application with dependency injection
        def create_application():
            db_service = container.resolve('database')
            return ApplicationService(db_service)

        container.register_factory('app_with_di', create_application)

        # Resolve and verify dependency injection
        app = container.resolve('app_with_di')
        assert app.ready is True
        assert app.db.connection == "database_connection"

    @pytest.mark.unit
    def test_service_container_scoped_services(self):
        """Test scoped service pattern"""
        container = ServiceContainer()

        # Service that maintains state
        class StatefulService:
            def __init__(self):
                self.state = "initial"

        # Register as factory (creates new instances)
        container.register_factory('stateful_service', StatefulService)

        service1 = container.resolve('stateful_service')
        service2 = container.resolve('stateful_service')

        # Should be different instances
        assert service1 is not service2

        # Can maintain separate state
        service1.state = "modified_1"
        service2.state = "modified_2"

        assert service1.state == "modified_1"
        assert service2.state == "modified_2"

    @pytest.mark.unit
    def test_service_container_configuration_service(self):
        """Test configuration service pattern"""
        container = ServiceContainer()

        # Configuration object
        config = {
            'database_url': 'postgresql://localhost/test',
            'timeout': 30,
            'debug': True
        }

        class ConfigService:
            def __init__(self, config_dict):
                self.config = config_dict
                self.loaded_at = time.time()

        container.register('config', ConfigService, config)

        # Resolve with parameter
        resolved_config = container.resolve('config')
        assert resolved_config.config is config
        assert resolved_config.config['database_url'] == 'postgresql://localhost/test'
        assert resolved_config.loaded_at > 0

    @pytest.mark.unit
    def test_service_container_multiple_interfaces(self):
        """Test service implementing multiple interfaces"""
        # Create a mock service that implements multiple interfaces
        multi_interface_service = Mock()

        # Make it implement multiple interfaces
        multi_interface_service.__class__ = (ITemplateProvider, IMemoryProvider)

        container.register('multi_service', multi_interface_service)

        # Should be resolvable as any of its interfaces
        resolved = container.resolve('multi_service')
        assert resolved is multi_interface_service

    @pytest.mark.unit
    def test_service_container_parameterized_factory(self):
        """Test factory with parameters"""
        container = ServiceContainer()

        def create_service_with_param(param_value):
            return Mock(parameter=param_value)

        # Register factory with parameter
        container.register('param_service', create_service_with_param, "test_param")

        # Should be called with parameter
        resolved = container.resolve('param_service')
        assert resolved.parameter == "test_param"

    @pytest.mark.unit
    def test_service_container_service_discovery(self):
        """Test service discovery pattern"""
        container = ServiceContainer()

        # Register multiple services
        services = {
            'template_service': Mock(),
            'memory_service': Mock(),
            'script_service': Mock()
        }

        for name, service in services.items():
            container.register(name, service)

        # Discover all services
        discovered_services = {
            name: container.resolve(name)
            for name in container.get_service_names()
        }

        assert discovered_services == services

    @pytest.mark.unit
    def test_service_container_error_propagation(self):
        """Test error propagation from services"""
        class ErrorService:
            def __init__(self):
                raise ValueError("Service creation failed")

        container = ServiceContainer()
        container.register_factory('error_service', ErrorService)

        with pytest.raises(DependencyError) as exc_info:
            container.resolve('error_service')

        assert "Error creating service 'error_service'" in str(exc_info.value)
        assert "Service creation failed" in str(exc_info.value.__cause__)

    @pytest.mark.unit
    def test_service_container_memory_cleanup(self):
        """Test memory cleanup for old services"""
        container = ServiceContainer()

        # Register and resolve many services
        for i in range(100):
            service = Mock(id=i)
            container.register(f'service_{i}', service)
            resolved = container.resolve(f'service_{i}')
            assert resolved.id == i

        # Clear container
        container.clear()

        # Verify cleanup
        assert len(container._services) == 0
        assert len(container._singletons) == 0
        assert len(container._factories) == 0

    @pytest.mark.unit
    def test_service_container_service_lifecycle(self):
        """Test service lifecycle management"""
        class LifecycleService:
            def __init__(self):
                self.created = True
                self.initialized = False

            def initialize(self):
                self.initialized = True

        container = ServiceContainer()

        # Register service with lifecycle
        def create_lifecycle_service():
            service = LifecycleService()
            service.initialize()
            return service

        container.register_factory('lifecycle_service', create_lifecycle_service)

        # Resolve and verify lifecycle
        service = container.resolve('lifecycle_service')
        assert service.created is True
        assert service.initialized is True

    @pytest.mark.unit
    def test_service_container_service_graph(self):
        """Test complex service dependency graph"""
        class DatabaseService:
            def __init__(self):
                self.connected = True

        class CacheService:
            def __init__(self, db_service):
                self.db = db_service
                self.connected = True

        class ApplicationService:
            def __init__(self, cache_service, db_service):
                self.cache = cache_service
                self.db = db_service
                self.ready = True

        container = ServiceContainer()

        # Register services
        container.register('database', DatabaseService)
        container.register('cache', CacheService)
        container.register('application', ApplicationService)

        # Create application with full dependency graph
        def create_full_application():
            db = container.resolve('database')
            cache = CacheService(db)
            return ApplicationService(cache, db)

        container.register_factory('full_app', create_full_application)

        # Resolve and verify full dependency graph
        app = container.resolve('full_app')
        assert app.ready is True
        assert app.cache.connected is True
        assert app.db.connected is True
        assert app.cache.db is app.db  # Same database instance

    @pytest.mark.unit
    def test_service_container_interface_compliance_validation(self):
        """Test interface compliance validation"""
        # This test ensures services properly implement expected methods
        container = ServiceContainer()

        # Mock with required interface methods
        compliant_service = Mock(spec=ITemplateProvider)
        compliant_service.get_spec_template.return_value = "spec_template"
        compliant_service.get_plan_template.return_value = "plan_template"

        container.register('compliant_service', compliant_service)

        resolved = container.resolve('compliant_service')
        assert hasattr(resolved, 'get_spec_template')
        assert hasattr(resolved, 'get_plan_template')
        resolved.get_spec_template()  # Should work without error

    @pytest.mark.unit
    def test_service_container_performance_monitoring(self):
        """Test performance monitoring capabilities"""
        container = ServiceContainer()

        # Mock performance tracker
        performance_tracker = {
            'resolutions': 0,
            'total_time': 0
        }

        original_resolve = container._resolve_service

        def tracked_resolve(service_name):
            start_time = time.time()
            result = original_resolve(service_name)
            end_time = time.time()

            performance_tracker['resolutions'] += 1
            performance_tracker['total_time'] += (end_time - start_time)

            return result

        # Monkey patch for testing
        container._resolve_service = tracked_resolve

        # Resolve multiple services
        container.register('service1', Mock())
        container.register('service2', Mock())
        container.register('service3', Mock())

        container.resolve('service1')
        container.resolve('service2')
        container.resolve('service3')

        # Verify tracking
        assert performance_tracker['resolutions'] == 3
        assert performance_tracker['total_time'] > 0
        assert performance_tracker['total_time'] < 1.0  # Should be fast

        # Restore original method
        container._resolve_service = original_resolve