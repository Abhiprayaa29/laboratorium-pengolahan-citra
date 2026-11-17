"""API Endpoints for Pipeline Execution."""

from fastapi import APIRouter, HTTPException, status
from app.core.engine.pipeline import PipelineEngine
from app.core.image_io.handler import decode_image
from app.schemas.pipeline import PipelineExecuteRequest, PipelineExecuteResponse

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])


@router.post("/execute", response_model=PipelineExecuteResponse)
def execute_pipeline(request: PipelineExecuteRequest):
    """Execute an ordered series of image operations sequentially.

    Each stage operates on the output of the preceding stage.
    Returns final result along with optional intermediate images and histograms.
    """
    try:
        initial_image = decode_image(request.image_base64)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Citra masukan tidak dapat didekode: {str(exc)}",
        )

    response = PipelineEngine.execute(initial_image, request)
    return response
