"""Comprehensive integration test verifying all 14 operations across all 4 modules."""

import numpy as np
import pytest

from app.core.registry.registry import registry
from app.schemas.operation import OperationStatus


@pytest.fixture
def sample_rgb_image():
    """Create a 50x50 synthetic color image for algorithm testing."""
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    # Red rectangle
    img[10:30, 10:30, 0] = 200
    # Green circle / patch
    img[20:40, 20:40, 1] = 180
    # Blue background gradient
    img[:, :, 2] = np.linspace(20, 150, 50, dtype=np.uint8)
    return img


def test_registry_contains_all_14_ready_operations():
    all_ops = registry.list_operations()
    # At least 14 registered operations from all modules
    ready_ops = [op for op in all_ops if op.status == OperationStatus.READY]
    assert len(ready_ops) >= 14
    op_ids = {op.id for op in ready_ops}
    expected_ids = {
        "intensity_grayscale",
        "intensity_negative",
        "intensity_sepia",
        "intensity_brightness",
        "filter_blur",
        "filter_sharpen",
        "filter_emboss",
        "filter_sketch",
        "morphology_erosion",
        "morphology_dilation",
        "geometry_mirroring",
        "segmentation_threshold",
        "histogram_equalization",
        "edge_detection_sobel",
    }
    assert expected_ids.issubset(op_ids)


@pytest.mark.parametrize(
    "operation_id,config",
    [
        # Modul 1
        ("intensity_grayscale", {"method": "luminance"}),
        ("intensity_grayscale", {"method": "average"}),
        ("intensity_negative", {}),
        ("intensity_sepia", {"intensity": 0.8}),
        ("intensity_brightness", {"beta": 40}),
        # Modul 2
        ("filter_blur", {"kernel_size": 5, "sigma": 1.5}),
        ("filter_sharpen", {"strength": 1.5}),
        ("filter_emboss", {"direction": "top_left"}),
        ("filter_sketch", {"blur_radius": 15}),
        # Modul 3
        ("morphology_erosion", {"kernel_size": 3, "iterations": 1}),
        ("morphology_dilation", {"kernel_size": 3, "iterations": 1}),
        ("geometry_mirroring", {"direction": "horizontal"}),
        # Modul 4
        ("segmentation_threshold", {"thresh": 128, "type": "binary"}),
        ("histogram_equalization", {}),
        ("edge_detection_sobel", {"kernel_size": 3, "thresh": 80}),
    ],
)
def test_each_operation_processes_successfully(sample_rgb_image, operation_id, config):
    op = registry.get(operation_id)
    assert op is not None, f"Operation '{operation_id}' not found in registry."

    output = op.process(sample_rgb_image.copy(), config)

    assert isinstance(output, np.ndarray)
    assert output.dtype == np.uint8
    assert output.shape[0] == sample_rgb_image.shape[0]
    assert output.shape[1] == sample_rgb_image.shape[1]
    # Value range check
    assert output.min() >= 0
    assert output.max() <= 255


def test_full_cross_module_pipeline_execution(sample_rgb_image):
    """Test a 4-stage pipeline combining operations from all 4 modules."""
    from app.core.engine.pipeline import PipelineEngine
    from app.schemas.pipeline import PipelineExecuteRequest, PipelineStepConfig

    steps = [
        PipelineStepConfig(step_id="step-1", operation_id="intensity_brightness", config={"beta": 15}),
        PipelineStepConfig(step_id="step-2", operation_id="filter_blur", config={"kernel_size": 3, "sigma": 1.0}),
        PipelineStepConfig(step_id="step-3", operation_id="geometry_mirroring", config={"direction": "horizontal"}),
        PipelineStepConfig(step_id="step-4", operation_id="segmentation_threshold", config={"thresh": 100}),
    ]

    req = PipelineExecuteRequest(
        image_base64="",
        steps=steps,
        include_intermediate_images=True,
        include_histograms=True,
    )

    response = PipelineEngine.execute(sample_rgb_image, req)

    assert response.success is True
    assert response.total_steps == 4
    assert response.executed_steps == 4
    assert len(response.stages) == 4
    for stage in response.stages:
        assert stage.error is None
        assert stage.image_base64 is not None
        assert stage.histogram is not None
