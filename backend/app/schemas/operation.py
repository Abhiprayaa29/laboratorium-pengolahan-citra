"""Pydantic schemas for Image Processing operations, metadata, and configurations."""

from enum import Enum
from typing import Any, List, Optional, Union
from pydantic import BaseModel, Field


class OperationStatus(str, Enum):
    READY = "ready"
    IN_DEVELOPMENT = "in_development"


class ParameterType(str, Enum):
    SELECT = "select"
    SLIDER = "slider"
    NUMBER = "number"
    BOOLEAN = "boolean"
    RADIO = "radio"


class ParameterOption(BaseModel):
    label: str
    value: Any
    description: Optional[str] = None


class ParameterSchema(BaseModel):
    name: str = Field(..., description="Parameter key in config dict")
    label: str = Field(..., description="Human readable label in Indonesian")
    type: ParameterType = Field(..., description="Input widget type")
    default: Any = Field(..., description="Default value")
    options: Optional[List[ParameterOption]] = Field(None, description="Choices for select/radio")
    min_value: Optional[Union[int, float]] = Field(None, description="Minimum value for slider/number")
    max_value: Optional[Union[int, float]] = Field(None, description="Maximum value for slider/number")
    step: Optional[Union[int, float]] = Field(None, description="Step increment for slider/number")
    description: Optional[str] = Field(None, description="Help text explaining this parameter")


class AcademicExplanation(BaseModel):
    pengertian: str = Field(..., description="Definisi fundamental")
    tujuan: str = Field(..., description="Tujuan penerapan operasi")
    cara_kerja: str = Field(..., description="Tahapan cara kerja algoritma")
    rumus_matematis: str = Field(..., description="Rumus KaTeX / LaTeX")
    parameter_info: str = Field(..., description="Penjelasan pengaruh parameter")
    pengaruh_gambar: str = Field(..., description="Perubahan visual pada citra")
    pengaruh_histogram: str = Field(..., description="Perubahan pada sebaran histogram")
    contoh_penerapan: str = Field(..., description="Kasus nyata penggunaan")
    mengapa_seperti_ini: str = Field(..., description="Penjelasan intuitif untuk mahasiswa")


class OperationMetadata(BaseModel):
    id: str
    name: str
    category: str
    owner: str
    description: str
    status: OperationStatus
    default_config: dict[str, Any]
    config_schema: List[ParameterSchema]
    explanation: AcademicExplanation
    has_kernel_preview: bool = False
