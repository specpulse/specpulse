"""
Template Provider Service

Extracted from SpecPulse God Object - handles all template loading operations.

This service is responsible for:
- Loading specification templates
- Loading plan templates
- Loading task templates
- Loading decomposition templates
- Template caching and variable substitution

Implements ITemplateProvider interface for dependency injection.
"""

from pathlib import Path
from typing import Dict, Optional
import logging

from .template_cache import get_global_template_cache

logger = logging.getLogger(__name__)


class TemplateProvider:
    """
    Template provider service implementing ITemplateProvider.

    Handles all template loading with caching and fallback to embedded templates.
    """

    def __init__(self, resources_dir: Path, use_cache: bool = True):
        """
        Initialize template provider.

        Args:
            resources_dir: Path to resources directory
            use_cache: Whether to use template caching (default: True)
        """
        self.resources_dir = resources_dir
        self.templates_dir = resources_dir / "templates"
        self.use_cache = use_cache
        self._cache = get_global_template_cache() if use_cache else None

    def get_spec_template(self) -> str:
        """Get specification template from file (cached)"""
        def loader():
            return self._load_template_file(
                "templates/spec.md",
                self._get_embedded_spec_template()
            )

        if self.use_cache:
            return self._cache.get("spec_template", loader)
        return loader()

    def get_plan_template(self) -> str:
        """Get implementation plan template from file (cached)"""
        def loader():
            return self._load_template_file(
                "templates/plan.md",
                self._get_embedded_plan_template()
            )

        if self.use_cache:
            return self._cache.get("plan_template", loader)
        return loader()

    def get_task_template(self) -> str:
        """Get task list template from file (cached)"""
        def loader():
            return self._load_template_file(
                "templates/task.md",
                self._get_embedded_task_template()
            )

        if self.use_cache:
            return self._cache.get("task_template", loader)
        return loader()

    def get_template(self, template_name: str, variables: Optional[Dict] = None) -> str:
        """
        Get generic template by name with variable substitution.

        Args:
            template_name: Name of template file
            variables: Optional variables for substitution

        Returns:
            Template content with variables replaced
        """
        template_path = self.templates_dir / template_name

        if not template_path.exists():
            logger.warning(f"Template not found: {template_name}")
            return ""

        try:
            content = template_path.read_text(encoding='utf-8')

            # Variable substitution (Jinja2-style: {{ variable }})
            if variables:
                for key, value in variables.items():
                    content = content.replace(f"{{{{{key}}}}}", str(value))

            return content

        except Exception as e:
            logger.error(f"Failed to load template {template_name}: {e}")
            return ""

    def get_decomposition_template(self, template_type: str = "microservices") -> str:
        """
        Get decomposition template.

        Args:
            template_type: Type (microservices, api, interface)

        Returns:
            Decomposition template content
        """
        template_map = {
            "microservices": "microservices.md",
            "api": "api-contract.yaml",
            "interface": "interface.ts"
        }

        template_file = template_map.get(template_type, "microservices.md")
        template_path = self.resources_dir / "templates" / "decomposition" / template_file

        if template_path.exists():
            try:
                return template_path.read_text(encoding='utf-8')
            except Exception as e:
                logger.error(f"Failed to load decomposition template: {e}")

        # Fallback for microservices
        if template_type == "microservices":
            return self._get_embedded_microservices_template()

        return ""

    def get_microservice_template(self) -> str:
        """Get microservice template"""
        return self._load_template_file(
            "templates/decomposition/microservice.md",
            self._get_embedded_microservices_template()
        )

    def get_api_contract_template(self) -> str:
        """Get API contract template"""
        return self._load_template_file(
            "templates/decomposition/api-contract.yaml",
            self._get_embedded_api_contract_template()
        )

    def get_interface_template(self) -> str:
        """Get interface template"""
        return self._load_template_file(
            "templates/decomposition/interface.ts",
            self._get_embedded_interface_template()
        )

    def get_service_plan_template(self) -> str:
        """Get service plan template"""
        return self._load_template_file(
            "templates/decomposition/service-plan.md",
            self._get_embedded_service_plan_template()
        )

    def get_integration_plan_template(self) -> str:
        """Get integration plan template"""
        return self._load_template_file(
            "templates/decomposition/integration-plan.md",
            self._get_embedded_integration_plan_template()
        )

    # Private helper methods

    def _load_template_file(self, relative_path: str, fallback: str) -> str:
        """
        Load template file with fallback.

        Args:
            relative_path: Path relative to resources_dir
            fallback: Embedded template to use if file not found

        Returns:
            Template content
        """
        template_path = self.resources_dir / relative_path

        if not template_path.exists():
            logger.warning(
                f"Template file not found: {relative_path}. "
                "Using embedded fallback template. "
                "Run 'specpulse doctor' to restore template files."
            )
            try:
                from ..utils.console import Console
                console = Console()
                template_name = Path(relative_path).name
                console.warning(
                    f"⚠️  Template file missing: {template_name}\n"
                    f"   Using default embedded template.\n"
                    f"   Run 'specpulse doctor' to restore files."
                )
            except Exception:
                pass

            return fallback

        try:
            return template_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to read template file: {e}")
            return fallback

    # Embedded template fallbacks (keeping from original God Object)

    def _get_embedded_spec_template(self) -> str:
        """Get embedded spec template"""
        return """<!-- SpecPulse Specification Template v1.0 -->
# Specification: {{ feature_name }}

## Metadata
- **Feature ID**: {{ feature_id }}
- **Spec ID**: {{ spec_id }}
- **Created**: {{ date }}
- **Version**: 1.0.0

## Executive Summary
{{ description }}

## Problem Statement
[Detailed description of the problem]

## Functional Requirements
FR-001: [Requirement]
  - Acceptance: [Criteria]
  - Priority: MUST

## User Stories
**As a** [user type]
**I want** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Criterion 1]

## Technical Constraints
[Constraints and limitations]

## Dependencies
[Required dependencies]

## Success Criteria
- [ ] All requirements implemented
- [ ] Tests passing
"""

    def _get_embedded_plan_template(self) -> str:
        """Get embedded plan template"""
        return """<!-- SpecPulse Implementation Plan Template v1.0 -->
# Implementation Plan: {{ feature_name }}

## Specification Reference
- **Spec ID**: {{ feature_id }}
- **Plan ID**: {{ plan_id }}
- **Created**: {{ date }}

## Architecture Overview
[High-level architecture description]

## Technology Stack
- **Language**: [Choice]
- **Framework**: [Choice]
- **Database**: [Choice]

## Implementation Phases

### Phase 1: Foundation
**Duration**: [Estimate]
**Tasks**:
1. Setup environment
2. Initialize repository

### Phase 2: Core Features
**Duration**: [Estimate]
**Tasks**:
1. Implement features

## Testing Strategy
- Unit Tests: 80% coverage
- Integration Tests: Critical paths
"""

    def _get_embedded_task_template(self) -> str:
        """Get embedded task template"""
        return """<!-- SpecPulse Task List Template v1.0 -->
# Task List: {{ feature_name }}

## Metadata
- **Plan Reference**: {{ plan_id }}
- **Task ID**: {{ task_id }}
- **Created**: {{ date }}

## Tasks

### TASK-001: [Task Name]
- **Type**: development
- **Priority**: HIGH
- **Estimate**: [hours]
- **Status**: pending
- **Description**: [What to do]
- **Acceptance**: [How to verify]
"""

    def _get_embedded_microservices_template(self) -> str:
        """Get embedded microservices template"""
        return """# Microservice: {{service_name}}

## Service Overview
- **Name**: {{service_name}}
- **Domain**: {{domain}}
- **Type**: [API|Worker|Gateway]

## Responsibilities
- Primary responsibility

## API Endpoints
- GET /api/v1/{{resource}}
- POST /api/v1/{{resource}}

## Dependencies
- Service A

## Data Model
```json
{
  "id": "string",
  "field": "value"
}
```
"""

    def _get_embedded_api_contract_template(self) -> str:
        """Get embedded API contract template"""
        return """openapi: 3.0.0
info:
  title: {{service_name}} API
  version: 1.0.0
  description: API contract for {{service_name}}

servers:
  - url: http://localhost:3000/api/v1
    description: Development server

paths:
  /{{resource}}:
    get:
      summary: Get all {{resource}}
      responses:
        '200':
          description: Successful response
    post:
      summary: Create new {{resource}}
      responses:
        '201':
          description: Created
"""

    def _get_embedded_interface_template(self) -> str:
        """Get embedded interface template"""
        return """// Interface for {{service_name}}

export interface {{InterfaceName}} {
  id: string;
  createdAt: Date;
  updatedAt: Date;
  // Add fields
}

export interface {{ServiceName}}Service {
  create(data: Partial<{{InterfaceName}}>): Promise<{{InterfaceName}}>;
  findById(id: string): Promise<{{InterfaceName}} | null>;
  update(id: string, data: Partial<{{InterfaceName}}>): Promise<{{InterfaceName}}>;
  delete(id: string): Promise<boolean>;
}
"""

    def _get_embedded_service_plan_template(self) -> str:
        """Get embedded service plan template"""
        return """# Service Implementation Plan: {{service_name}}

## Service Context
- **Parent Spec**: {{spec_id}}
- **Service Type**: {{service_type}}
- **Priority**: {{priority}}

## Implementation Phases

### Phase 1: Foundation
- [ ] Set up service structure
- [ ] Configure dependencies

### Phase 2: Core Features
- [ ] Implement primary endpoints
- [ ] Add business logic

### Phase 3: Integration
- [ ] Connect to other services
- [ ] Add error handling

## Technical Decisions
- Framework: {{framework}}
- Database: {{database}}
"""

    def _get_embedded_integration_plan_template(self) -> str:
        """Get embedded integration plan template"""
        return """# Integration Plan

## Overview
Integration strategy for microservices in {{feature_name}}

## Service Communication Matrix
| Source Service | Target Service | Protocol | Pattern |
|---------------|---------------|----------|---------|
| Service A | Service B | REST | Request-Response |

## Integration Points
1. **Authentication Flow**
   - Service: auth-service
   - Integration: API Gateway
   - Protocol: OAuth2

## API Gateway Configuration
- Routes mapping
- Rate limiting
- Authentication

## Testing Strategy
- Integration tests
- Contract tests
- End-to-end tests
"""


__all__ = ['TemplateProvider']
