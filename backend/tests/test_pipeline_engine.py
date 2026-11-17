"""Unit Tests for Pipeline Processing Engine."""

import numpy as np
import pytest
from app.core.engine.pipeline import PipelineEngine
from app.core.registry.loader import register_all_operations
from app.schemas.pipeline import PipelineExecuteRequest, PipelineStepConfig


@pytest.fixture(autouse=True)
def setup_registry():
    register_all_operations()


@pytest.fixture
def test_canvas():
    """Create a 40x40 image with asymmetric shapes and small noise pixels."""
    img = np.zeros((40, 40, 3), dtype=np.uint8)
    img[10:25, 10:20] = 255  # rectangle
    # Add isolated noise pixels to demonstrate opening vs closing differences
    img[2, 2] = 255
    img[35, 35] = 255
    return img


def test_pipeline_sequential_execution(test_canvas):
    """Pipeline should execute steps sequentially and return intermediate stages."""
    steps = [
        PipelineStepConfig(
            step_id="step-1",
            operation_id="morphology_erosion",
            enabled=True,
            config={"kernel_size": 3, "iterations": 1},
        ),
        PipelineStepConfig(
            step_id="step-2",
            operation_id="geometry_mirroring",
            enabled=True,
            config={"axis": "horizontal"},
        ),
    ]

    req = PipelineExecuteRequest(
        image_base64="",  # Placeholder, direct ndarray passed to engine
        steps=steps,
        include_intermediate_images=True,
        include_histograms=True,
    )

    response = PipelineEngine.execute(test_canvas, req)

    assert response.success is True
    assert response.total_steps == 2
    assert response.executed_steps == 2
    assert len(response.stages) == 2

    # Stage 1: Erosion
    assert response.stages[0].operation_id == "morphology_erosion"
    assert response.stages[0].image_base64 is not None
    assert response.stages[0].histogram is not None

    # Stage 2: Mirroring
    assert response.stages[1].operation_id == "geometry_mirroring"
    assert response.stages[1].image_base64 is not None


def test_pipeline_disabled_step_skipped(test_canvas):
    """Disabled steps should be recorded as skipped without altering intermediate image."""
    steps = [
        PipelineStepConfig(
            step_id="step-1",
            operation_id="morphology_erosion",
            enabled=False,  # Skipped
            config={},
        ),
        PipelineStepConfig(
            step_id="step-2",
            operation_id="geometry_mirroring",
            enabled=True,
            config={"axis": "horizontal"},
        ),
    ]

    req = PipelineExecuteRequest(
        image_base64="",
        steps=steps,
        include_intermediate_images=True,
        include_histograms=True,
    )

    response = PipelineEngine.execute(test_canvas, req)

    assert response.total_steps == 2
    assert response.executed_steps == 1
    assert response.stages[0].enabled is False
    assert "Dilewati" in (response.stages[0].note or "")


def test_pipeline_reordering_changes_result(test_canvas):
    """Order of operations matters: Erode then Dilate (Opening) != Dilate then Erode (Closing)."""
    # Pipeline A: Erosion then Dilation (Opening removes isolated noise)
    steps_a = [
        PipelineStepConfig(step_id="1", operation_id="morphology_erosion", enabled=True, config={"kernel_size": 3}),
        PipelineStepConfig(step_id="2", operation_id="morphology_dilation", enabled=True, config={"kernel_size": 3}),
    ]
    # Pipeline B: Dilation then Erosion (Closing preserves or bridges noise)
    steps_b = [
        PipelineStepConfig(step_id="1", operation_id="morphology_dilation", enabled=True, config={"kernel_size": 3}),
        PipelineStepConfig(step_id="2", operation_id="morphology_erosion", enabled=True, config={"kernel_size": 3}),
    ]

    req_a = PipelineExecuteRequest(image_base64="", steps=steps_a)
    req_b = PipelineExecuteRequest(image_base64="", steps=steps_b)

    res_a = PipelineEngine.execute(test_canvas, req_a)
    res_b = PipelineEngine.execute(test_canvas, req_b)

    # Opening removes noise [2, 2]; Closing grows it. Final results MUST differ.
    assert res_a.final_image_base64 != res_b.final_image_base64


def test_pipeline_handles_in_development_gracefully(test_canvas):
    """Operations in development should be gracefully reported without crashing."""
    steps = [
        PipelineStepConfig(
            step_id="step-1",
            operation_id="intensity_grayscale",  # Orang 1: In Development
            enabled=True,
            config={},
        )
    ]

    req = PipelineExecuteRequest(image_base64="", steps=steps)
    response = PipelineEngine.execute(test_canvas, req)

    assert response.total_steps == 1
    assert response.executed_steps == 0
    assert "Dalam Pengembangan" in response.stages[0].note
