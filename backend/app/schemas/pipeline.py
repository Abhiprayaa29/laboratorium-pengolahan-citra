"""Pydantic schemas for Pipeline execution, steps, and intermediate responses."""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from app.schemas.histogram import HistogramData, ImageStats


class PipelineStepConfig(BaseModel):
    step_id: str = Field(..., description="Unique ID for this instance in the pipeline")
    operation_id: str = Field(..., description="Registered operation ID")
    enabled: bool = Field(True, description="Whether to execute this step")
    config: Dict[str, Any] = Field(default_factory=dict, description="Custom parameters")


class PipelineExecuteRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded input image")
    steps: List[PipelineStepConfig] = Field(..., description="Ordered list of operations")
    include_intermediate_images: bool = Field(True, description="Include intermediate preview images")
    include_histograms: bool = Field(True, description="Compute histogram for each stage")


class StepExecutionResult(BaseModel):
    step_id: str
    operation_id: str
    operation_name: str
    enabled: bool
    execution_time_ms: float
    error: Optional[str] = None
    image_base64: Optional[str] = None
    histogram: Optional[HistogramData] = None
    stats: Optional[ImageStats] = None
    kernel_preview: Optional[List[List[Union[int, float]]]] = None
    note: Optional[str] = None


class PipelineExecuteResponse(BaseModel):
    success: bool
    total_steps: int
    executed_steps: int
    total_execution_time_ms: float
    initial_stats: ImageStats
    initial_histogram: Optional[HistogramData] = None
    stages: List[StepExecutionResult]
    final_image_base64: str
    final_stats: ImageStats
    final_histogram: Optional[HistogramData] = None
    error: Optional[str] = None


class ImageAnalyzeRequest(BaseModel):
    image_base64: str


class ImageAnalyzeResponse(BaseModel):
    stats: ImageStats
    histogram: HistogramData
    preview_base64: str
