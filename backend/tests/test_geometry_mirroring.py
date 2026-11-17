"""Unit Tests for Geometry: Mirroring Operation (Modul 3 - Orang 3)."""

import numpy as np
import pytest
from app.core.histogram.engine import compute_histogram
from app.features.orang_3.mirroring import MirroringOperation


@pytest.fixture
def mirroring_op():
    return MirroringOperation()


@pytest.fixture
def asymmetric_test_image():
    """Create an asymmetric 4x4 test matrix to verify exact pixel coordinate mapping."""
    # Pixel coordinates: value = row * 10 + col
    grid = np.array([
        [[10, 0, 0], [11, 0, 0], [12, 0, 0], [13, 0, 0]],
        [[20, 0, 0], [21, 0, 0], [22, 0, 0], [23, 0, 0]],
        [[30, 0, 0], [31, 0, 0], [32, 0, 0], [33, 0, 0]],
        [[40, 0, 0], [41, 0, 0], [42, 0, 0], [43, 0, 0]],
    ], dtype=np.uint8)
    return grid


def test_mirroring_horizontal_flip(mirroring_op, asymmetric_test_image):
    """Horizontal flip: x' = W - 1 - x (columns are inverted)."""
    result = mirroring_op.process(asymmetric_test_image, {"axis": "horizontal"})

    # Check top-left pixel originally [10, 0, 0] is now top-right
    assert np.array_equal(result[0, 3], asymmetric_test_image[0, 0])
    assert np.array_equal(result[0, 0], asymmetric_test_image[0, 3])
    # Rows should remain unchanged
    assert np.array_equal(result[3, 3], asymmetric_test_image[3, 0])


def test_mirroring_vertical_flip(mirroring_op, asymmetric_test_image):
    """Vertical flip: y' = H - 1 - y (rows are inverted)."""
    result = mirroring_op.process(asymmetric_test_image, {"axis": "vertical"})

    # Check top-left pixel originally [10, 0, 0] is now bottom-left
    assert np.array_equal(result[3, 0], asymmetric_test_image[0, 0])
    assert np.array_equal(result[0, 0], asymmetric_test_image[3, 0])


def test_mirroring_both_axes_flip(mirroring_op, asymmetric_test_image):
    """Both axes flip (equivalent to 180 degree rotation)."""
    result = mirroring_op.process(asymmetric_test_image, {"axis": "both"})

    # Top-left becomes bottom-right
    assert np.array_equal(result[3, 3], asymmetric_test_image[0, 0])
    assert np.array_equal(result[0, 0], asymmetric_test_image[3, 3])


def test_mirroring_involution_identity(mirroring_op, asymmetric_test_image):
    """Applying the same axis mirror twice must return EXACT original image (M o M = I)."""
    # Horizontal twice
    flip_h1 = mirroring_op.process(asymmetric_test_image, {"axis": "horizontal"})
    flip_h2 = mirroring_op.process(flip_h1, {"axis": "horizontal"})
    assert np.array_equal(flip_h2, asymmetric_test_image)

    # Vertical twice
    flip_v1 = mirroring_op.process(asymmetric_test_image, {"axis": "vertical"})
    flip_v2 = mirroring_op.process(flip_v1, {"axis": "vertical"})
    assert np.array_equal(flip_v2, asymmetric_test_image)

    # Both twice
    flip_b1 = mirroring_op.process(asymmetric_test_image, {"axis": "both"})
    flip_b2 = mirroring_op.process(flip_b1, {"axis": "both"})
    assert np.array_equal(flip_b2, asymmetric_test_image)


def test_mirroring_preserves_histogram_identically(mirroring_op):
    """Mirroring alters spatial arrangement but keeps intensity frequency 100% identical."""
    np.random.seed(42)
    random_image = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)

    hist_original = compute_histogram(random_image)

    for axis in ["horizontal", "vertical", "both"]:
        mirrored = mirroring_op.process(random_image, {"axis": axis})
        hist_mirrored = compute_histogram(mirrored)

        # Grayscale bins must be exactly identical
        assert hist_mirrored.grayscale == hist_original.grayscale
        # Channel bins must be exactly identical
        assert hist_mirrored.red == hist_original.red
        assert hist_mirrored.green == hist_original.green
        assert hist_mirrored.blue == hist_original.blue
        # Stats must match
        assert hist_mirrored.stats.mean == hist_original.stats.mean
        assert hist_mirrored.stats.min_intensity == hist_original.stats.min_intensity
        assert hist_mirrored.stats.max_intensity == hist_original.stats.max_intensity
