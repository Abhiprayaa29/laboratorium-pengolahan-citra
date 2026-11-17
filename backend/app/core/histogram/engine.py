"""Histogram Analysis Engine: Computes actual 256-bin pixel distributions and statistics.

All calculations reflect REAL pixel data using OpenCV and NumPy:
- 256 bins ranging from 0 to 255.
- Grayscale distribution via luminance conversion (cv2.COLOR_RGB2GRAY).
- Channel-wise Red, Green, and Blue distributions for 3-channel RGB images.
- Precise statistical metrics (min, max, mean, standard deviation, total pixel count).
"""

from typing import Optional
import cv2
import numpy as np
from app.schemas.histogram import HistogramData, ImageStats


def compute_image_stats(image: np.ndarray) -> ImageStats:
    """Compute statistical intensity metrics directly from image ndarray."""
    if image is None or image.size == 0:
        raise ValueError("Citra kosong tidak dapat dihitung statistiknya.")

    is_gray = len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1)
    height, width = image.shape[:2]
    channels = 1 if is_gray else image.shape[2]
    total_pixels = width * height

    # If RGB/RGBA, compute stats across luminance grayscale for consistent scalar mean/std
    if not is_gray:
        if channels == 4:
            rgb_only = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
            gray = cv2.cvtColor(rgb_only, cv2.COLOR_RGB2GRAY)
        else:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.squeeze() if len(image.shape) == 3 else image

    min_val = int(np.min(gray))
    max_val = int(np.max(gray))
    mean_val = float(np.mean(gray))
    std_val = float(np.std(gray))

    return ImageStats(
        min_intensity=min_val,
        max_intensity=max_val,
        mean=round(mean_val, 2),
        std_dev=round(std_val, 2),
        total_pixels=total_pixels,
        width=width,
        height=height,
        channels=channels,
        is_grayscale=is_gray,
    )


def compute_histogram(image: np.ndarray, explanation: Optional[str] = None) -> HistogramData:
    """Compute 256-bin histogram for Grayscale, Red, Green, and Blue channels."""
    if image is None or image.size == 0:
        raise ValueError("Citra kosong tidak dapat dihitung histogramnya.")

    stats = compute_image_stats(image)
    bins_range = list(range(256))

    is_gray = stats.is_grayscale

    if is_gray:
        gray_2d = image.squeeze() if len(image.shape) == 3 else image
        hist_gray = cv2.calcHist([gray_2d], [0], None, [256], [0, 256])
        grayscale_bins = [int(x) for x in hist_gray.flatten()]

        return HistogramData(
            bins_range=bins_range,
            grayscale=grayscale_bins,
            red=None,
            green=None,
            blue=None,
            stats=stats,
            explanation=explanation,
        )

    # For RGB / RGBA image:
    if image.shape[2] == 4:
        rgb_img = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    else:
        rgb_img = image

    gray = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)
    hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])
    grayscale_bins = [int(x) for x in hist_gray.flatten()]

    hist_r = cv2.calcHist([rgb_img], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([rgb_img], [1], None, [256], [0, 256])
    hist_b = cv2.calcHist([rgb_img], [2], None, [256], [0, 256])

    red_bins = [int(x) for x in hist_r.flatten()]
    green_bins = [int(x) for x in hist_g.flatten()]
    blue_bins = [int(x) for x in hist_b.flatten()]

    return HistogramData(
        bins_range=bins_range,
        grayscale=grayscale_bins,
        red=red_bins,
        green=green_bins,
        blue=blue_bins,
        stats=stats,
        explanation=explanation,
    )
