"""Pipeline Execution Engine.

Processes an ordered sequence of image operations non-destructively:
Original Image -> Stage 1 -> Stage 2 -> ... -> Stage N -> Final Output

Captures intermediate states, histograms, metrics, and kernel representations.
"""

import time
from typing import Optional
import numpy as np

from app.core.histogram.engine import compute_histogram, compute_image_stats
from app.core.image_io.handler import encode_image_to_base64
from app.core.registry.base import BaseImageOperation
from app.core.registry.registry import registry
from app.schemas.operation import OperationStatus
from app.schemas.pipeline import (
    PipelineExecuteRequest,
    PipelineExecuteResponse,
    StepExecutionResult,
)


class PipelineEngine:
    """Executes multi-step image operations sequentially with stage isolation."""

    @staticmethod
    def execute(
        initial_image: np.ndarray,
        request: PipelineExecuteRequest,
    ) -> PipelineExecuteResponse:
        start_pipeline_time = time.perf_counter()

        initial_stats = compute_image_stats(initial_image)
        initial_hist = (
            compute_histogram(initial_image, explanation="Histogram awal citra asli sebelum diproses.")
            if request.include_histograms
            else None
        )

        stages: list[StepExecutionResult] = []
        current_image = initial_image.copy()  # Non-destructive copy
        executed_count = 0
        fatal_error: Optional[str] = None

        for step in request.steps:
            step_start = time.perf_counter()
            op: Optional[BaseImageOperation] = registry.get(step.operation_id)

            if not op:
                error_msg = f"Operasi dengan ID '{step.operation_id}' tidak ditemukan di registry."
                stages.append(
                    StepExecutionResult(
                        step_id=step.step_id,
                        operation_id=step.operation_id,
                        operation_name=step.operation_id,
                        enabled=step.enabled,
                        execution_time_ms=0.0,
                        error=error_msg,
                        note="Operasi tidak terdaftar",
                    )
                )
                continue

            if not step.enabled:
                stages.append(
                    StepExecutionResult(
                        step_id=step.step_id,
                        operation_id=op.id,
                        operation_name=op.name,
                        enabled=False,
                        execution_time_ms=0.0,
                        note="Dilewati (Tahap dinonaktifkan oleh pengguna)",
                    )
                )
                continue

            if op.status == OperationStatus.IN_DEVELOPMENT:
                stages.append(
                    StepExecutionResult(
                        step_id=step.step_id,
                        operation_id=op.id,
                        operation_name=op.name,
                        enabled=True,
                        execution_time_ms=0.0,
                        error=f"Operasi '{op.name}' saat ini masih Dalam Pengembangan oleh {op.owner}.",
                        note="Dalam Pengembangan",
                    )
                )
                continue

            # Merge user config over default config
            merged_config = dict(op.default_config)
            merged_config.update(step.config)

            kernel_matrix = op.get_kernel_matrix(merged_config) if op.has_kernel_preview else None

            try:
                processed_output = op.process(current_image, merged_config)
                # Ensure uint8
                if processed_output.dtype != np.uint8:
                    processed_output = np.clip(processed_output, 0, 255).astype(np.uint8)

                step_elapsed = (time.perf_counter() - step_start) * 1000.0
                current_image = processed_output  # Forward to next stage
                executed_count += 1

                stage_stats = compute_image_stats(current_image)
                stage_hist = (
                    compute_histogram(current_image, explanation=f"Histogram pasca operasi {op.name}.")
                    if request.include_histograms
                    else None
                )

                stage_img_b64 = (
                    encode_image_to_base64(current_image)
                    if request.include_intermediate_images
                    else None
                )

                stages.append(
                    StepExecutionResult(
                        step_id=step.step_id,
                        operation_id=op.id,
                        operation_name=op.name,
                        enabled=True,
                        execution_time_ms=round(step_elapsed, 2),
                        image_base64=stage_img_b64,
                        histogram=stage_hist,
                        stats=stage_stats,
                        kernel_preview=kernel_matrix,
                        note="Berhasil dieksekusi",
                    )
                )

            except Exception as exc:
                step_elapsed = (time.perf_counter() - step_start) * 1000.0
                err_text = f"Terjadi kesalahan saat memproses '{op.name}': {str(exc)}"
                stages.append(
                    StepExecutionResult(
                        step_id=step.step_id,
                        operation_id=op.id,
                        operation_name=op.name,
                        enabled=True,
                        execution_time_ms=round(step_elapsed, 2),
                        error=err_text,
                        note="Eksekusi gagal",
                    )
                )
                fatal_error = err_text
                break  # Stop processing further stages if a fatal processing error occurs

        total_elapsed = (time.perf_counter() - start_pipeline_time) * 1000.0

        final_stats = compute_image_stats(current_image)
        final_hist = (
            compute_histogram(current_image, explanation="Histogram final citra hasil pengolahan.")
            if request.include_histograms
            else None
        )
        final_b64 = encode_image_to_base64(current_image)

        return PipelineExecuteResponse(
            success=fatal_error is None,
            total_steps=len(request.steps),
            executed_steps=executed_count,
            total_execution_time_ms=round(total_elapsed, 2),
            initial_stats=initial_stats,
            initial_histogram=initial_hist,
            stages=stages,
            final_image_base64=final_b64,
            final_stats=final_stats,
            final_histogram=final_hist,
            error=fatal_error,
        )
