"""Image I/O Handler: Centralized color space translation, validation, and encoding/decoding.

OpenCV natively decodes images in BGR color space. This module guarantees that:
1. All images entering the core engine are standard RGB uint8.
2. Grayscale images are 2D arrays or single-channel uint8.
3. All images exported or encoded to Base64 are cleanly converted back from RGB to BGR before OpenCV compression.
"""

import base64
import re
from typing import Tuple, Union
import cv2
import numpy as np


MAX_IMAGE_BYTES = 15 * 1024 * 1024  # 15 MB
ALLOWED_FORMATS = {"png", "jpg", "jpeg", "webp"}


class ImageProcessingError(Exception):
    """Custom exception for image decoding/encoding errors."""
    pass


def clean_base64_string(data_url: str) -> Tuple[bytes, str]:
    """Extract raw bytes and format from a Base64 string or Data URL."""
    if not data_url or not isinstance(data_url, str):
        raise ImageProcessingError("String gambar Base64 kosong atau tidak valid.")

    match = re.match(r"^data:image/([a-zA-Z0-9\+\-]+);base64,(.+)$", data_url, re.DOTALL)
    if match:
        fmt = match.group(1).lower()
        if fmt == "jpeg":
            fmt = "jpg"
        raw_b64 = match.group(2)
    else:
        fmt = "png"
        raw_b64 = data_url

    try:
        image_bytes = base64.b64decode(raw_b64)
    except Exception as exc:
        raise ImageProcessingError(f"Gagal melakukan decode Base64: {str(exc)}")

    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise ImageProcessingError(f"Ukuran citra melebihi batas maksimal {MAX_IMAGE_BYTES // (1024 * 1024)} MB.")

    return image_bytes, fmt


def decode_image_bytes(image_bytes: bytes) -> np.ndarray:
    """Decode raw bytes into an RGB uint8 NumPy ndarray."""
    if not image_bytes:
        raise ImageProcessingError("Data biner gambar kosong.")

    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise ImageProcessingError("Ukuran gambar melebihi batas 15 MB.")

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ImageProcessingError("Format file tidak didukung atau file gambar rusak/tidak dapat didekode.")

    # Convert color spaces
    if len(img.shape) == 2:
        # Grayscale image (2D)
        return img.astype(np.uint8)
    elif len(img.shape) == 3:
        channels = img.shape[2]
        if channels == 3:
            # OpenCV decodes as BGR -> Convert to standard RGB
            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.uint8)
        elif channels == 4:
            # BGRA -> Convert to RGBA
            return cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA).astype(np.uint8)
        elif channels == 1:
            return img.squeeze(axis=2).astype(np.uint8)

    return img.astype(np.uint8)


def decode_image(image_input: Union[bytes, str]) -> np.ndarray:
    """Universal decoder: accepts either bytes or base64 data string."""
    if isinstance(image_input, str):
        image_bytes, _ = clean_base64_string(image_input)
    elif isinstance(image_input, bytes):
        image_bytes = image_input
    else:
        raise ImageProcessingError("Tipe input gambar tidak didukung (harus bytes atau string base64).")

    return decode_image_bytes(image_bytes)


def encode_image(image: np.ndarray, format: str = "png", quality: int = 90) -> bytes:
    """Encode an RGB uint8 image array into bytes of specified format."""
    if image is None or not isinstance(image, np.ndarray):
        raise ImageProcessingError("Array citra tidak valid untuk dienkode.")

    fmt = format.lower().strip()
    if fmt == "jpeg":
        fmt = "jpg"
    if fmt not in ALLOWED_FORMATS:
        fmt = "png"

    # Convert RGB back to BGR for OpenCV encoding
    if len(image.shape) == 2:
        export_img = image
    elif len(image.shape) == 3:
        if image.shape[2] == 3:
            export_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        elif image.shape[2] == 4:
            export_img = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
        else:
            export_img = image
    else:
        export_img = image

    params = []
    if fmt in ("jpg", "jpeg"):
        params = [int(cv2.IMWRITE_JPEG_QUALITY), max(10, min(100, quality))]
    elif fmt == "webp":
        params = [int(cv2.IMWRITE_WEBP_QUALITY), max(10, min(100, quality))]
    elif fmt == "png":
        params = [int(cv2.IMWRITE_PNG_COMPRESSION), 4]

    success, encoded = cv2.imencode(f".{fmt}", export_img, params)
    if not success:
        raise ImageProcessingError("Gagal mengenkode citra ke format yang diminta.")

    return encoded.tobytes()


def encode_image_to_base64(image: np.ndarray, format: str = "png") -> str:
    """Encode RGB image array directly to a Data URL string."""
    img_bytes = encode_image(image, format=format)
    mime = "jpeg" if format.lower() in ("jpg", "jpeg") else format.lower()
    b64_str = base64.b64encode(img_bytes).decode("utf-8")
    return f"data:image/{mime};base64,{b64_str}"
