"""Operation Loader: Automatically discovers and registers operations from all feature modules."""

import logging
from app.core.registry.registry import registry
from app.features.orang_1 import operations as orang_1_ops
from app.features.orang_2 import operations as orang_2_ops
from app.features.orang_3 import operations as orang_3_ops
from app.features.orang_4 import operations as orang_4_ops

logger = logging.getLogger("lpcd.registry")


def register_all_operations() -> None:
    """Register all modular operations from team member directories."""
    all_module_lists = [
        ("Modul 1 (Orang 1)", orang_1_ops),
        ("Modul 2 (Orang 2)", orang_2_ops),
        ("Modul 3 (Orang 3)", orang_3_ops),
        ("Modul 4 (Orang 4)", orang_4_ops),
    ]

    for module_name, ops in all_module_lists:
        for op in ops:
            registry.register(op)
            logger.info("Registered operation '%s' (%s) from %s", op.id, op.name, module_name)
