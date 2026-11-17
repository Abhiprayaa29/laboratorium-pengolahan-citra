export type OperationStatus = 'ready' | 'in_development';

export type ParameterType = 'select' | 'slider' | 'number' | 'boolean' | 'radio';

export interface ParameterOption {
  label: string;
  value: string | number | boolean;
  description?: string;
}

export interface ParameterSchema {
  name: string;
  label: string;
  type: ParameterType;
  default: string | number | boolean;
  options?: ParameterOption[];
  min_value?: number;
  max_value?: number;
  step?: number;
  description?: string;
}

export interface AcademicExplanation {
  pengertian: string;
  tujuan: string;
  cara_kerja: string;
  rumus_matematis: string;
  parameter_info: string;
  pengaruh_gambar: string;
  pengaruh_histogram: string;
  contoh_penerapan: string;
  mengapa_seperti_ini: string;
}

export interface OperationMetadata {
  id: string;
  name: string;
  category: string;
  owner: string;
  description: string;
  status: OperationStatus;
  default_config: Record<string, any>;
  config_schema: ParameterSchema[];
  explanation: AcademicExplanation;
  has_kernel_preview: boolean;
}

export interface ImageStats {
  min_intensity: number;
  max_intensity: number;
  mean: number;
  std_dev: number;
  total_pixels: number;
  width: number;
  height: number;
  channels: number;
  is_grayscale: boolean;
}

export interface HistogramData {
  bins_range: number[];
  grayscale?: number[];
  red?: number[];
  green?: number[];
  blue?: number[];
  stats: ImageStats;
  explanation?: string;
}

export interface PipelineStep {
  step_id: string;
  operation_id: string;
  enabled: boolean;
  config: Record<string, any>;
}

export interface StepExecutionResult {
  step_id: string;
  operation_id: string;
  operation_name: string;
  enabled: boolean;
  execution_time_ms: number;
  error?: string;
  image_base64?: string;
  histogram?: HistogramData;
  stats?: ImageStats;
  kernel_preview?: number[][];
  note?: string;
}

export interface PipelineExecuteResponse {
  success: boolean;
  total_steps: number;
  executed_steps: number;
  total_execution_time_ms: number;
  initial_stats: ImageStats;
  initial_histogram?: HistogramData;
  stages: StepExecutionResult[];
  final_image_base64: string;
  final_stats: ImageStats;
  final_histogram?: HistogramData;
  error?: string;
}

export interface ImageAnalyzeResponse {
  stats: ImageStats;
  histogram: HistogramData;
  preview_base64: string;
}

export interface HealthResponse {
  status: string;
  application: string;
  version: string;
  timestamp: string;
  total_operations: number;
  ready_operations: number;
  in_development_operations: number;
}
