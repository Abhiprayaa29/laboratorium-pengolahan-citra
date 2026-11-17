"""API Endpoints for Standalone Histogram Calculation."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.core.histogram.engine import compute_histogram
from app.core.image_io.handler import decode_image
from app.schemas.histogram import HistogramData

router = APIRouter(prefix="/histogram", tags=["Histogram"])


class HistogramCalculateRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image string")
    channel: str = Field("all", description="Channel selector: all, grayscale, red, green, blue")


@router.post("", response_model=HistogramData)
def calculate_histogram_endpoint(payload: HistogramCalculateRequest):
    """Calculate actual 256-bin pixel distribution histogram and statistical metrics."""
    try:
        image = decode_image(payload.image_base64)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Gagal mendecode citra: {str(exc)}",
        )

    hist_data = compute_histogram(image, explanation="Perhitungan histogram aktual.")
    return hist_data
