"""Unit Tests for Histogram Analysis Engine."""

import numpy as np
import pytest
from app.core.histogram.engine import compute_histogram, compute_image_stats


def test_histogram_bins_count_and_range():
    """Histogram must contain exactly 256 bins ranging from 0 to 255."""
    img = np.zeros((30, 30, 3), dtype=np.uint8)
    hist = compute_histogram(img)

    assert len(hist.bins_range) == 256
    assert hist.bins_range[0] == 0
    assert hist.bins_range[255] == 255
    assert len(hist.grayscale) == 256
    assert len(hist.red) == 256
    assert len(hist.green) == 256
    assert len(hist.blue) == 256


def test_histogram_total_pixel_sum_matches():
    """Sum of all bins in grayscale histogram must strictly equal total pixel count (W x H)."""
    h, w = 45, 60
    total_pixels = h * w
    np.random.seed(123)
    img = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)

    hist = compute_histogram(img)

    assert sum(hist.grayscale) == total_pixels
    assert sum(hist.red) == total_pixels
    assert sum(hist.green) == total_pixels
    assert sum(hist.blue) == total_pixels
    assert hist.stats.total_pixels == total_pixels


def test_histogram_pure_colors():
    """A pure Red image should have non-zero bins in Red, but 0 in Blue/Green."""
    pure_red = np.zeros((20, 20, 3), dtype=np.uint8)
    pure_red[:, :, 0] = 255  # Red channel = 255

    hist = compute_histogram(pure_red)

    # In Red channel, bin 255 has 400 pixels, others 0
    assert hist.red[255] == 400
    assert sum(hist.red[:255]) == 0

    # In Green and Blue channels, bin 0 has 400 pixels
    assert hist.green[0] == 400
    assert hist.blue[0] == 400


def test_image_stats_metrics():
    """Verify min, max, mean, and standard deviation calculations."""
    matrix = np.full((10, 10), 100, dtype=np.uint8)
    stats = compute_image_stats(matrix)

    assert stats.min_intensity == 100
    assert stats.max_intensity == 100
    assert stats.mean == 100.0
    assert stats.std_dev == 0.0
    assert stats.is_grayscale is True
