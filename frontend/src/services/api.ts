import axios from 'axios';
import type {
  HealthResponse,
  ImageAnalyzeResponse,
  OperationMetadata,
  PipelineExecuteResponse,
  PipelineStep,
} from '../types';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export const apiClient = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000,
});

export const api = {
  checkHealth: async (): Promise<HealthResponse> => {
    const res = await apiClient.get<HealthResponse>('/health');
    return res.data;
  },

  getOperations: async (): Promise<OperationMetadata[]> => {
    const res = await apiClient.get<OperationMetadata[]>('/operations');
    return res.data;
  },

  getOperation: async (id: string): Promise<OperationMetadata> => {
    const res = await apiClient.get<OperationMetadata>(`/operations/${id}`);
    return res.data;
  },

  analyzeImage: async (imageBase64: string): Promise<ImageAnalyzeResponse> => {
    const res = await apiClient.post<ImageAnalyzeResponse>('/images/analyze', {
      image_base64: imageBase64,
    });
    return res.data;
  },

  analyzeImageFile: async (file: File): Promise<ImageAnalyzeResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post<ImageAnalyzeResponse>('/images/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  executePipeline: async (
    imageBase64: string,
    steps: PipelineStep[],
    includeIntermediate = true,
    includeHistograms = true
  ): Promise<PipelineExecuteResponse> => {
    const res = await apiClient.post<PipelineExecuteResponse>('/pipeline/execute', {
      image_base64: imageBase64,
      steps,
      include_intermediate_images: includeIntermediate,
      include_histograms: includeHistograms,
    });
    return res.data;
  },

  executeSingleOperation: async (
    operationId: string,
    imageBase64: string,
    config: Record<string, any> = {}
  ) => {
    const res = await apiClient.post(`/operations/${operationId}/execute`, {
      image_base64: imageBase64,
      config,
    });
    return res.data;
  },

  downloadImage: async (
    imageBase64: string,
    format: 'png' | 'jpg' = 'png',
    filename = 'lpcd_citra'
  ) => {
    const res = await apiClient.post(
      '/images/download',
      { image_base64: imageBase64, format, filename },
      { responseType: 'blob' }
    );

    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${filename}.${format}`);
    document.body.appendChild(link);
    link.click();
    link.parentNode?.removeChild(link);
    window.URL.revokeObjectURL(url);
  },
};
