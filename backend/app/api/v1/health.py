"""API Health and Readiness Endpoints."""

import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.registry.registry import registry

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    application: str
    version: str
    timestamp: str
    total_operations: int
    ready_operations: int
    in_development_operations: int


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Verify backend system status, registered operations, and uptime."""
    ops = registry.list_operations()
    ready_count = sum(1 for op in ops if op.status == "ready")
    in_dev_count = len(ops) - ready_count

    return HealthResponse(
        status="ok",
        application="Laboratorium Pengolahan Citra Digital (LPCD) API",
        version="1.0.0",
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        total_operations=len(ops),
        ready_operations=ready_count,
        in_development_operations=in_dev_count,
    )
