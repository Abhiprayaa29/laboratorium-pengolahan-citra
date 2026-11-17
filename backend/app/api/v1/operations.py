"""API Endpoints for Operations Metadata and Single Operation Execution."""

from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.core.histogram.engine import compute_histogram, compute_image_stats
from app.core.image_io.handler import decode_image, encode_image_to_base64
from app.core.registry.registry import registry
from app.schemas.histogram import HistogramData, ImageStats
from app.schemas.operation import OperationMetadata, OperationStatus

router = APIRouter(prefix="/operations", tags=["Operations"])


class SingleOperationExecuteRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded input image")
    config: Dict[str, Any] = Field(default_factory=dict, description="Operation configuration parameters")


class SingleOperationExecuteResponse(BaseModel):
    operation_id: str
    operation_name: str
    execution_time_ms: float
    processed_image_base64: str
    stats: ImageStats
    histogram: HistogramData
    kernel_preview: list[list[int]] | None = None


@router.get("", response_model=List[OperationMetadata])
def get_all_operations():
    """Retrieve metadata of all registered operations across all 4 member modules."""
    return registry.list_operations()


@router.get("/{operation_id}", response_model=OperationMetadata)
def get_operation_by_id(operation_id: str):
    """Retrieve detailed metadata, configuration schema, and academic explanation for a single operation."""
    op = registry.get(operation_id)
    if not op:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Operasi dengan ID '{operation_id}' tidak ditemukan di registry LPCD.",
        )
    return op.get_metadata()


@router.post("/{operation_id}/execute", response_model=SingleOperationExecuteResponse)
def execute_single_operation(operation_id: str, payload: SingleOperationExecuteRequest):
    """Execute a single operation directly on an image without full pipeline overhead."""
    import time

    op = registry.get(operation_id)
    if not op:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Operasi dengan ID '{operation_id}' tidak ditemukan.",
        )

    if op.status == OperationStatus.IN_DEVELOPMENT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operasi '{op.name}' saat ini masih Dalam Pengembangan oleh {op.owner}.",
        )

    try:
        image = decode_image(payload.image_base64)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    merged_config = dict(op.default_config)
    merged_config.update(payload.config)

    t0 = time.perf_counter()
    try:
        result = op.process(image, merged_config)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Kesalahan algoritma saat menjalankan {op.name}: {str(exc)}",
        )
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    stats = compute_image_stats(result)
    hist = compute_histogram(result, explanation=f"Hasil pasca eksekusi {op.name}.")
    b64_out = encode_image_to_base64(result)
    kernel_matrix = op.get_kernel_matrix(merged_config) if op.has_kernel_preview else None

    return SingleOperationExecuteResponse(
        operation_id=op.id,
        operation_name=op.name,
        execution_time_ms=round(elapsed_ms, 2),
        processed_image_base64=b64_out,
        stats=stats,
        histogram=hist,
        kernel_preview=kernel_matrix,
    )
