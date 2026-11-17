"""Integration Tests for FastAPI REST Endpoints."""

import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.core.image_io.handler import encode_image_to_base64
from app.main import app

client = TestClient(app)


@pytest.fixture
def sample_b64_image():
    """Create a sample 30x30 image encoded to base64 Data URL."""
    img = np.zeros((30, 30, 3), dtype=np.uint8)
    img[5:20, 5:20] = [255, 128, 64]
    return encode_image_to_base64(img, format="png")


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["total_operations"] >= 14
    assert data["ready_operations"] >= 3  # Erosion, Dilation, Mirroring


def test_get_all_operations():
    response = client.get("/api/v1/operations")
    assert response.status_code == 200
    ops = response.json()
    assert len(ops) >= 14
    op_ids = [op["id"] for op in ops]
    assert "morphology_erosion" in op_ids
    assert "morphology_dilation" in op_ids
    assert "geometry_mirroring" in op_ids
    assert "intensity_grayscale" in op_ids


def test_get_operation_by_id():
    response = client.get("/api/v1/operations/morphology_erosion")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "morphology_erosion"
    assert data["owner"] == "Modul 3"
    assert data["explanation"]["rumus_matematis"] is not None


def test_get_nonexistent_operation_404():
    response = client.get("/api/v1/operations/unknown_op_999")
    assert response.status_code == 404


def test_execute_single_operation(sample_b64_image):
    payload = {
        "image_base64": sample_b64_image,
        "config": {"kernel_size": 3, "iterations": 1},
    }
    response = client.post("/api/v1/operations/morphology_erosion/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["operation_id"] == "morphology_erosion"
    assert data["processed_image_base64"].startswith("data:image/png;base64,")
    assert data["histogram"]["grayscale"] is not None


def test_execute_ready_operations_all_modules(sample_b64_image):
    payload = {
        "image_base64": sample_b64_image,
        "config": {},
    }
    # Test Modul 1 (Grayscale)
    res_m1 = client.post("/api/v1/operations/intensity_grayscale/execute", json=payload)
    assert res_m1.status_code == 200
    assert res_m1.json()["operation_id"] == "intensity_grayscale"

    # Test Modul 2 (Blur)
    res_m2 = client.post("/api/v1/operations/filter_blur/execute", json=payload)
    assert res_m2.status_code == 200
    assert res_m2.json()["operation_id"] == "filter_blur"

    # Test Modul 4 (Thresholding)
    res_m4 = client.post("/api/v1/operations/segmentation_threshold/execute", json=payload)
    assert res_m4.status_code == 200
    assert res_m4.json()["operation_id"] == "segmentation_threshold"


def test_execute_in_development_rejected_or_handled(sample_b64_image):
    from app.core.registry.base import BaseImageOperation
    from app.core.registry.registry import registry
    from app.schemas.operation import AcademicExplanation, OperationStatus

    class DummyInDevOp(BaseImageOperation):
        id = "test_dummy_indev"
        name = "Dummy In Dev"
        category = "Testing"
        owner = "Tester"
        description = "Test op"
        status = OperationStatus.IN_DEVELOPMENT
        default_config = {}
        config_schema = []
        explanation = AcademicExplanation(
            pengertian="Test",
            tujuan="Test",
            cara_kerja="Test",
            rumus_matematis="T",
            parameter_info="T",
            pengaruh_gambar="T",
            pengaruh_histogram="T",
            contoh_penerapan="T",
            mengapa_seperti_ini="T",
        )

        def process(self, image, config):
            return image

    registry.register(DummyInDevOp())

    payload = {
        "image_base64": sample_b64_image,
        "config": {},
    }
    response = client.post("/api/v1/operations/test_dummy_indev/execute", json=payload)
    assert response.status_code == 400
    assert "Dalam Pengembangan" in response.json()["detail"]


def test_analyze_image_endpoint(sample_b64_image):
    response = client.post(
        "/api/v1/images/analyze",
        json={"image_base64": sample_b64_image},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stats"]["width"] == 30
    assert data["stats"]["height"] == 30
    assert len(data["histogram"]["grayscale"]) == 256


def test_pipeline_execution_endpoint(sample_b64_image):
    payload = {
        "image_base64": sample_b64_image,
        "steps": [
            {
                "step_id": "step-1",
                "operation_id": "geometry_mirroring",
                "enabled": True,
                "config": {"axis": "horizontal"},
            },
            {
                "step_id": "step-2",
                "operation_id": "morphology_erosion",
                "enabled": True,
                "config": {"kernel_size": 3},
            },
        ],
        "include_intermediate_images": True,
        "include_histograms": True,
    }
    response = client.post("/api/v1/pipeline/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_steps"] == 2
    assert len(data["stages"]) == 2
    assert data["final_image_base64"].startswith("data:image/png;base64,")


def test_invalid_base64_returns_400():
    response = client.post(
        "/api/v1/images/analyze",
        json={"image_base64": "invalid_not_base64_string_%%@@@"},
    )
    assert response.status_code == 400
