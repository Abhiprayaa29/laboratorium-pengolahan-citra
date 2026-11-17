"""Unit Tests for Morphology: Dilation Operation (Modul 3 - Orang 3)."""

import numpy as np
import pytest
from app.features.orang_3.dilation import DilationOperation


@pytest.fixture
def dilation_op():
    return DilationOperation()


@pytest.fixture
def binary_test_image():
    """Create a 50x50 black image with a 10x10 white square in the center."""
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[20:30, 20:30] = 255  # 10x10 = 100 pixels
    return img


def test_dilation_expands_white_foreground(dilation_op, binary_test_image):
    """Test that white foreground pixels increase after dilation."""
    initial_white_count = np.sum(binary_test_image[:, :, 0] == 255)
    assert initial_white_count == 100

    config = {"kernel_shape": "rect", "kernel_size": 3, "iterations": 1, "mode": "rgb"}
    result = dilation_op.process(binary_test_image, config)

    processed_white_count = np.sum(result[:, :, 0] == 255)
    # 10x10 expanded by 1 pixel in each direction -> 12x12 = 144
    assert processed_white_count > initial_white_count
    assert processed_white_count == 144


def test_dilation_kernel_size_impact(dilation_op, binary_test_image):
    """Larger kernel size should expand foreground more significantly."""
    config_3x3 = {"kernel_shape": "rect", "kernel_size": 3, "iterations": 1, "mode": "rgb"}
    config_5x5 = {"kernel_shape": "rect", "kernel_size": 5, "iterations": 1, "mode": "rgb"}

    res_3x3 = dilation_op.process(binary_test_image, config_3x3)
    res_5x5 = dilation_op.process(binary_test_image, config_5x5)

    white_3x3 = np.sum(res_3x3[:, :, 0] == 255)
    white_5x5 = np.sum(res_5x5[:, :, 0] == 255)

    assert white_5x5 > white_3x3


def test_dilation_kernel_shapes_differ(dilation_op, binary_test_image):
    """Rectangular and Cross kernels should produce distinct dilation geometries."""
    config_rect = {"kernel_shape": "rect", "kernel_size": 5, "iterations": 1, "mode": "rgb"}
    config_cross = {"kernel_shape": "cross", "kernel_size": 5, "iterations": 1, "mode": "rgb"}

    res_rect = dilation_op.process(binary_test_image, config_rect)
    res_cross = dilation_op.process(binary_test_image, config_cross)

    assert not np.array_equal(res_rect, res_cross)
    assert np.sum(res_rect[:, :, 0] == 255) > np.sum(res_cross[:, :, 0] == 255)


def test_dilation_iterations_impact(dilation_op, binary_test_image):
    """Multiple iterations progressively expand foreground."""
    config_iter1 = {"kernel_shape": "rect", "kernel_size": 3, "iterations": 1, "mode": "rgb"}
    config_iter2 = {"kernel_shape": "rect", "kernel_size": 3, "iterations": 2, "mode": "rgb"}

    res_iter1 = dilation_op.process(binary_test_image, config_iter1)
    res_iter2 = dilation_op.process(binary_test_image, config_iter2)

    white_iter1 = np.sum(res_iter1[:, :, 0] == 255)
    white_iter2 = np.sum(res_iter2[:, :, 0] == 255)

    assert white_iter2 > white_iter1
