"""Pydantic schemas for Histogram data and image statistics."""

from typing import List, Optional
from pydantic import BaseModel, Field


class ImageStats(BaseModel):
    min_intensity: int = Field(..., description="Intensitas terendah [0-255]")
    max_intensity: int = Field(..., description="Intensitas tertinggi [0-255]")
    mean: float = Field(..., description="Rata-rata intensitas citra")
    std_dev: float = Field(..., description="Standar deviasi intensitas citra")
    total_pixels: int = Field(..., description="Total pixel pada citra")
    width: int
    height: int
    channels: int
    is_grayscale: bool


class HistogramChannel(BaseModel):
    name: str = Field(..., description="grayscale, red, green, or blue")
    bins: List[int] = Field(..., description="256 bins frekuensi pixel [0..255]")


class HistogramData(BaseModel):
    bins_range: List[int] = Field(default_factory=lambda: list(range(256)))
    grayscale: Optional[List[int]] = None
    red: Optional[List[int]] = None
    green: Optional[List[int]] = None
    blue: Optional[List[int]] = None
    stats: ImageStats
    explanation: Optional[str] = None
