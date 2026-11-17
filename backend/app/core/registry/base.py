"""Base Operation Protocol and Abstract Definition.

Every operation across all four member modules MUST inherit from or conform to this contract.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import numpy as np

from app.schemas.operation import (
    AcademicExplanation,
    OperationMetadata,
    OperationStatus,
    ParameterSchema,
)


class BaseImageOperation(ABC):
    """Abstract base class for all image processing operations in LPCD."""

    id: str
    name: str
    category: str
    owner: str
    description: str
    status: OperationStatus = OperationStatus.READY
    has_kernel_preview: bool = False

    default_config: Dict[str, Any]
    config_schema: List[ParameterSchema]
    explanation: AcademicExplanation

    @abstractmethod
    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        """Process the given image and return the resulting image array.

        Args:
            image: Standard RGB uint8 NumPy ndarray (or 2D grayscale array).
            config: User-provided parameter values matching config_schema.

        Returns:
            Processed RGB or Grayscale uint8 NumPy ndarray.
        """
        pass

    def get_kernel_matrix(self, config: Dict[str, Any]) -> Optional[List[List[int]]]:
        """Optional helper to return structuring element or convolution kernel for UI visualization."""
        return None

    def get_metadata(self) -> OperationMetadata:
        """Generate Pydantic metadata representation for frontend consumption."""
        return OperationMetadata(
            id=self.id,
            name=self.name,
            category=self.category,
            owner=self.owner,
            description=self.description,
            status=self.status,
            default_config=self.default_config,
            config_schema=self.config_schema,
            explanation=self.explanation,
            has_kernel_preview=self.has_kernel_preview,
        )
