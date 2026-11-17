"""Unit Tests for Morphology: Erosion Operation (Modul 3 - Orang 3)."""

import cv2
import numpy as np
import pytest
from app.features.orang_3.erosion import ErosionOperation


@pytest.fixture
def erosion_op():
    return ErosionOperation()


@pytest.fixture
def binary_test_image():
    """Create a 50x50 black image with a 20x20 white square in the center."""
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[15:35, 15:35] = 255  # White foreground: 20x20 = 400 pixels
    return img


@pytest.fixture
def circular_test_image():
    """Create a 50x50 image with a white filled circle to test shape sensitivities."""
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    cv2.circle(img, (25, 25), 15, (255, 255, 255), -1)
    return img


def test_erosion_shrinks_white_foreground(erosion_op, binary_test_image):
    """Test that white foreground pixels decrease after erosion."""
    initial_white_count = np.sum(binary_test_image[:, :, 0] == 255)
    assert initial_white_count == 400

    config = {"kernel_shape": "rect", "kernel_size": 3, "iterations": 1, "mode": "rgb"}
    result = erosion_op.process(binary_test_image, config)

    processed_white_count = np.sum(result[:, :, 0] == 255)
    assert processed_white_count < initial_white_count
    assert processed_white_count == 324


def test_erosion_kernel_size_impact(erosion_op, binary_test_image):
    """Larger kernel size should erode more aggressive foreground area."""
    config_3x3 = {"kernel_shape": "rect", "kernel_size": 3, "iterations": 1, "mode": "rgb"}
    config_5x5 = {"kernel_shape": "rect", "kernel_size": 5, "iterations": 1, "mode": "rgb"}

    res_3x3 = erosion_op.process(binary_test_image, config_3x3)
    res_5x5 = erosion_op.process(binary_test_image, config_5x5)

    white_3x3 = np.sum(res_3x3[:, :, 0] == 255)
    white_5x5 = np.sum(res_5x5[:, :, 0] == 255)

    assert white_5x5 < white_3x3


def test_erosion_kernel_shapes_differ(erosion_op, circular_test_image):
    """Rectangular and Cross kernels should yield distinct geometric boundaries on curved shapes."""
    config_rect = {"kernel_shape": "rect", "kernel_size": 5, "iterations": 1, "mode": "rgb"}
    config_cross = {"kernel_shape": "cross", "kernel_size": 5, "iterations": 1, "mode": "rgb"}

    res_rect = erosion_op.process(circular_test_image, config_rect)
    res_cross = erosion_op.process(circular_test_image, config_cross)

    assert not np.array_equal(res_rect, res_cross)
    # Cross kernel preserves diagonal points that rectangular kernel erodes
    assert np.sum(res_cross[:, :, 0] == 255) > np.sum(res_rect[:, :, 0] == 255)


def test_erosion_iterations_impact(erosion_op, binary_test_image):
    """Multiple iterations progressively erode foreground."""
    config_iter1 = {"kernel_shape": "rect", "kernel_size": 3, "iterations": 1, "mode": "rgb"}
    config_iter2 = {"kernel_shape": "rect", "kernel_size": 3, "iterations": 2, "mode": "rgb"}

    res_iter1 = erosion_op.process(binary_test_image, config_iter1)
    res_iter2 = erosion_op.process(binary_test_image, config_iter2)

    white_iter1 = np.sum(res_iter1[:, :, 0] == 255)
    white_iter2 = np.sum(res_iter2[:, :, 0] == 255)

    assert white_iter2 < white_iter1


def test_erosion_grayscale_mode(erosion_op, binary_test_image):
    """Test erosion in grayscale conversion mode."""
    config = {"kernel_shape": "rect", "kernel_size": 3, "iterations": 1, "mode": "grayscale"}
    res = erosion_op.process(binary_test_image, config)
    assert res.shape == binary_test_image.shape
    assert res.dtype == np.uint8
