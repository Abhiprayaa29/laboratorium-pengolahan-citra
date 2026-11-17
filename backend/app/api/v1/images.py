"""API Endpoints for Image Analysis and High-Resolution Export."""

from typing import Optional
from fastapi import APIRouter, File, HTTPException, Request, Response, UploadFile, status
from pydantic import BaseModel, Field

from app.core.histogram.engine import compute_histogram, compute_image_stats
from app.core.image_io.handler import decode_image, decode_image_bytes, encode_image, encode_image_to_base64
from app.schemas.pipeline import ImageAnalyzeRequest, ImageAnalyzeResponse

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/analyze", response_model=ImageAnalyzeResponse)
async def analyze_image(
    request: Request,
    file: Optional[UploadFile] = File(None),
):
    """Analyze an uploaded image from either multipart/form-data or JSON base64 body."""
    image = None

    # Check content-type
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            body = await request.json()
            b64 = body.get("image_base64")
            if not b64:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Field 'image_base64' wajib diisi pada payload JSON.",
                )
            image = decode_image(b64)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Format JSON atau Base64 tidak valid: {str(exc)}",
            )
    elif file is not None:
        try:
            contents = await file.read()
            image = decode_image_bytes(contents)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Gagal membaca file gambar: {str(exc)}",
            )
    else:
        # Fallback: check if multipart had file or json
        try:
            form = await request.form()
            if "file" in form and hasattr(form["file"], "read"):
                contents = await form["file"].read()
                image = decode_image_bytes(contents)
            elif "image_base64" in form:
                image = decode_image(form["image_base64"])
        except Exception:
            pass

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wajib menyertakan gambar melalui unggahan file (multipart/form-data) atau JSON {'image_base64': '...'}.",
        )

    stats = compute_image_stats(image)
    hist = compute_histogram(image, explanation="Distribusi histogram awal citra asli.")
    preview_b64 = encode_image_to_base64(image)

    return ImageAnalyzeResponse(
        stats=stats,
        histogram=hist,
        preview_base64=preview_b64,
    )


class DownloadRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image to download")
    format: str = Field("png", description="Target file extension: png or jpg")
    filename: Optional[str] = Field("lpcd_hasil_pengolahan", description="Exported filename prefix")


@router.post("/download")
def download_image(payload: DownloadRequest):
    """Export full-resolution image binary as a downloadable attachment."""
    try:
        image = decode_image(payload.image_base64)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    fmt = payload.format.lower().strip()
    if fmt in ("jpg", "jpeg"):
        mime_type = "image/jpeg"
        ext = "jpg"
    else:
        mime_type = "image/png"
        ext = "png"

    image_bytes = encode_image(image, format=ext)
    clean_filename = f"{payload.filename or 'lpcd_processed'}.{ext}"

    return Response(
        content=image_bytes,
        media_type=mime_type,
        headers={
            "Content-Disposition": f'attachment; filename="{clean_filename}"',
            "Cache-Control": "no-cache",
        },
    )
