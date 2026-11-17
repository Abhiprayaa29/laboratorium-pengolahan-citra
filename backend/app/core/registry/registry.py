"""Centralized Modular Operation Registry.

Stores and manages all image operations registered across modules.
Allows dynamic discovery, isolation per member, and pipeline integration
without touching the core processing engine.
"""

from typing import Dict, List, Optional
from app.core.registry.base import BaseImageOperation
from app.schemas.operation import OperationMetadata


class OperationRegistry:
    """Singleton-capable Registry for all LPCD Image Operations."""

    def __init__(self):
        self._operations: Dict[str, BaseImageOperation] = {}

    def register(self, operation: BaseImageOperation) -> None:
        """Register a new operation into the system."""
        if not operation.id:
            raise ValueError("Operasi harus memiliki ID yang unik dan tidak kosong.")
        if operation.id in self._operations:
            # Overwrite allowed for hot-reloading / test mocking
            pass
        self._operations[operation.id] = operation

    def get(self, operation_id: str) -> Optional[BaseImageOperation]:
        """Retrieve operation instance by its unique identifier."""
        return self._operations.get(operation_id)

    def has(self, operation_id: str) -> bool:
        """Check if an operation ID is registered."""
        return operation_id in self._operations

    def list_operations(self) -> List[OperationMetadata]:
        """Return list of all registered operations metadata."""
        return [op.get_metadata() for op in self._operations.values()]

    def list_by_category(self, category: str) -> List[OperationMetadata]:
        """Filter operations by category."""
        return [
            op.get_metadata()
            for op in self._operations.values()
            if op.category.lower() == category.lower()
        ]

    def list_by_owner(self, owner: str) -> List[OperationMetadata]:
        """Filter operations by member/owner."""
        return [
            op.get_metadata()
            for op in self._operations.values()
            if op.owner.lower() == owner.lower()
        ]

    def clear(self) -> None:
        """Clear all registered operations (useful for test resets)."""
        self._operations.clear()


# Global Registry Instance
registry = OperationRegistry()
