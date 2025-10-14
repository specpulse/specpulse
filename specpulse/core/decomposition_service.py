"""
Decomposition Service

Extracted from SpecPulse God Object - handles specification decomposition.

Implements IDecompositionService interface.
"""

from pathlib import Path
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class DecompositionService:
    """Decomposition service implementing IDecompositionService"""

    def __init__(self, resources_dir: Path, template_provider):
        self.resources_dir = resources_dir
        self.template_provider = template_provider

    def decompose_specification(self, spec_dir: Path, spec_content: str) -> Dict:
        """Decompose specification into microservices"""
        result = {
            "services": [],
            "api_contracts": [],
            "interfaces": [],
            "integration_points": [],
            "status": "success"
        }

        content_lower = spec_content.lower()

        # Service detection logic
        if "auth" in content_lower:
            result["services"].append("authentication")
        if "user" in content_lower:
            result["services"].append("user-management")
        if "product" in content_lower or "catalog" in content_lower:
            result["services"].append("product-catalog")
        if "payment" in content_lower:
            result["services"].append("payment-service")
        if "notification" in content_lower:
            result["services"].append("notification-service")

        result["services"] = list(dict.fromkeys(result["services"]))

        if len(result["services"]) > 1:
            result["integration_points"] = ["message-queue", "api-gateway"]

        # Create decomposition directory
        decomp_dir = spec_dir / "decomposition"
        decomp_dir.mkdir(exist_ok=True)

        (decomp_dir / "microservices.md").write_text("# Microservices\n")
        (decomp_dir / "api-contracts").mkdir(exist_ok=True)
        (decomp_dir / "interfaces").mkdir(exist_ok=True)

        return result

    def get_microservice_template(self) -> str:
        """Get microservice template"""
        return self.template_provider.get_microservice_template()

    def get_api_contract_template(self) -> str:
        """Get API contract template"""
        return self.template_provider.get_api_contract_template()

    def get_interface_template(self) -> str:
        """Get interface template"""
        return self.template_provider.get_interface_template()

    def get_service_plan_template(self) -> str:
        """Get service plan template"""
        return self.template_provider.get_service_plan_template()

    def get_integration_plan_template(self) -> str:
        """Get integration plan template"""
        return self.template_provider.get_integration_plan_template()

    def get_decomposition_template(self, template_name: str) -> str:
        """Get specific decomposition template"""
        template_path = self.resources_dir / "templates" / "decomposition" / template_name
        if template_path.exists():
            try:
                return template_path.read_text(encoding='utf-8')
            except Exception as e:
                logger.error(f"Failed to load decomposition template: {e}")
        return f"# Decomposition template '{template_name}' not found"


__all__ = ['DecompositionService']
