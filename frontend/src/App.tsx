import React, { useState, useEffect, useMemo } from 'react';
import type {
  HistogramData,
  ImageStats,
  OperationMetadata,
  PipelineStep,
  StepExecutionResult,
} from './types';
import { api } from './services/api';
import { Header } from './components/Header';
import { OperationLibrary } from './components/OperationLibrary';
import { PipelineBuilder } from './components/PipelineBuilder';
import { ImageWorkspace } from './components/ImageWorkspace';
import { ParameterInspector } from './components/ParameterInspector';
import { HistogramWorkspace } from './components/HistogramWorkspace';
import { AcademicTheoryModal } from './components/AcademicTheoryModal';
import { PresetModal } from './components/PresetModal';
import { AboutModal } from './components/AboutModal';
import { AlertCircle, CheckCircle } from 'lucide-react';

export const App: React.FC = () => {
  // Backend & Operations State
  const [backendConnected, setBackendConnected] = useState<boolean | null>(null);
  const [operations, setOperations] = useState<OperationMetadata[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Image & Processing State
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [processedImage, setProcessedImage] = useState<string | null>(null);
  const [imageStats, setImageStats] = useState<ImageStats | null>(null);
  const [originalHistogram, setOriginalHistogram] = useState<HistogramData | null>(null);
  const [processedHistogram, setProcessedHistogram] = useState<HistogramData | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  // Pipeline State
  const [pipelineSteps, setPipelineSteps] = useState<PipelineStep[]>([]);
  const [selectedStepId, setSelectedStepId] = useState<string | null>(null);
  const [stageResults, setStageResults] = useState<Map<string, StepExecutionResult>>(new Map());

  // Modals
  const [activeTheoryOp, setActiveTheoryOp] = useState<OperationMetadata | null>(null);
  const [isPresetModalOpen, setIsPresetModalOpen] = useState<boolean>(false);
  const [isAboutModalOpen, setIsAboutModalOpen] = useState<boolean>(false);

  // Map for fast operations lookup
  const operationsMap = useMemo(() => {
    const map = new Map<string, OperationMetadata>();
    for (const op of operations) {
      map.set(op.id, op);
    }
    return map;
  }, [operations]);

  // Selected step and operation
  const selectedStep = useMemo(() => {
    return pipelineSteps.find((s) => s.step_id === selectedStepId) || null;
  }, [pipelineSteps, selectedStepId]);

  const selectedOperation = useMemo(() => {
    if (!selectedStep) return null;
    return operationsMap.get(selectedStep.operation_id) || null;
  }, [selectedStep, operationsMap]);

  // Selected stage intermediate result
  const selectedStageResult = useMemo(() => {
    if (!selectedStepId) return null;
    return stageResults.get(selectedStepId) || null;
  }, [selectedStepId, stageResults]);

  // Initial Health & Operations Loading
  useEffect(() => {
    const initBackend = async () => {
      try {
        const health = await api.checkHealth();
        if (health.status === 'ok') {
          setBackendConnected(true);
        }
      } catch (err) {
        console.warn('Backend connection failed:', err);
        setBackendConnected(false);
      }

      try {
        const ops = await api.getOperations();
        setOperations(ops);
      } catch (err) {
        console.error('Failed to load operations:', err);
      }
    };

    initBackend();
  }, []);

  // Handle Image Selection / Upload
  const handleImageSelected = async (base64: string) => {
    setOriginalImage(base64);
    setProcessedImage(null);
    setStageResults(new Map());
    setProcessedHistogram(null);
    setErrorMessage(null);

    try {
      const analyzed = await api.analyzeImage(base64);
      setImageStats(analyzed.stats);
      setOriginalHistogram(analyzed.histogram);
      setProcessedHistogram(analyzed.histogram);
    } catch (err: any) {
      console.error('Failed to analyze initial image:', err);
      setErrorMessage(err.response?.data?.detail || 'Gagal menganalisis citra masukan.');
    }
  };

  // Add Operation to Pipeline
  const handleAddOperation = (op: OperationMetadata) => {
    if (op.status !== 'ready') return;

    const newStepId = `step-${Date.now()}-${Math.random().toString(36).substr(2, 4)}`;
    const newStep: PipelineStep = {
      step_id: newStepId,
      operation_id: op.id,
      enabled: true,
      config: { ...op.default_config },
    };

    setPipelineSteps((prev) => [...prev, newStep]);
    setSelectedStepId(newStepId);
  };

  // Update Config for a Step
  const handleUpdateConfig = (stepId: string, newConfig: Record<string, any>) => {
    setPipelineSteps((prev) =>
      prev.map((s) => (s.step_id === stepId ? { ...s, config: newConfig } : s))
    );
  };

  // Toggle Step Enabled/Disabled
  const handleToggleStep = (stepId: string) => {
    setPipelineSteps((prev) =>
      prev.map((s) => (s.step_id === stepId ? { ...s, enabled: !s.enabled } : s))
    );
  };

  // Remove Step
  const handleRemoveStep = (stepId: string) => {
    setPipelineSteps((prev) => prev.filter((s) => s.step_id !== stepId));
    if (selectedStepId === stepId) {
      setSelectedStepId(null);
    }
  };

  // Duplicate Step
  const handleDuplicateStep = (stepId: string) => {
    const target = pipelineSteps.find((s) => s.step_id === stepId);
    if (!target) return;

    const dupId = `step-${Date.now()}-${Math.random().toString(36).substr(2, 4)}`;
    const duplicated: PipelineStep = {
      step_id: dupId,
      operation_id: target.operation_id,
      enabled: target.enabled,
      config: { ...target.config },
    };

    const targetIdx = pipelineSteps.findIndex((s) => s.step_id === stepId);
    const updated = [...pipelineSteps];
    updated.splice(targetIdx + 1, 0, duplicated);
    setPipelineSteps(updated);
    setSelectedStepId(dupId);
  };

  // Clear Pipeline
  const handleClearPipeline = () => {
    setPipelineSteps([]);
    setSelectedStepId(null);
    setStageResults(new Map());
    setProcessedImage(null);
    if (originalHistogram) {
      setProcessedHistogram(originalHistogram);
    }
  };

  // Execute Pipeline
  const handleExecutePipeline = async () => {
    if (!originalImage || pipelineSteps.length === 0) return;

    setIsProcessing(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const response = await api.executePipeline(originalImage, pipelineSteps, true, true);

      if (response.success) {
        setProcessedImage(response.final_image_base64);
        setImageStats(response.final_stats);
        if (response.final_histogram) {
          setProcessedHistogram(response.final_histogram);
        }

        // Store stage results map
        const resultsMap = new Map<string, StepExecutionResult>();
        for (const stage of response.stages) {
          resultsMap.set(stage.step_id, stage);
        }
        setStageResults(resultsMap);
        setSuccessMessage(`Pipeline berhasil dieksekusi dalam ${response.total_execution_time_ms} ms!`);
        setTimeout(() => setSuccessMessage(null), 3500);
      } else {
        setErrorMessage(response.error || 'Terjadi kesalahan saat memproses pipeline.');
      }
    } catch (err: any) {
      console.error('Pipeline execution error:', err);
      const detail = err.response?.data?.detail || err.message || 'Gagal mengeksekusi pipeline.';
      setErrorMessage(detail);
    } finally {
      setIsProcessing(false);
    }
  };

  // Load Preset Workflow
  const handleLoadPreset = (presetSteps: PipelineStep[], presetName: string) => {
    setPipelineSteps(presetSteps);
    if (presetSteps.length > 0) {
      setSelectedStepId(presetSteps[0].step_id);
    }
    setSuccessMessage(`Preset '${presetName}' berhasil dimuat.`);
    setTimeout(() => setSuccessMessage(null), 3000);
  };

  // Download Image
  const handleDownloadImage = async (format: 'png' | 'jpg') => {
    const target = processedImage || originalImage;
    if (!target) return;
    try {
      await api.downloadImage(target, format, 'lpcd_hasil_pengolahan');
    } catch (err) {
      console.error('Download failed:', err);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      {/* Header */}
      <Header
        backendConnected={backendConnected}
        onOpenPresets={() => setIsPresetModalOpen(true)}
        onOpenTheory={() => {
          if (selectedOperation) {
            setActiveTheoryOp(selectedOperation);
          } else if (operations.length > 0) {
            setActiveTheoryOp(operations.find((op) => op.status === 'ready') || operations[0]);
          }
        }}
        onOpenAbout={() => setIsAboutModalOpen(true)}
      />

      {/* Toast Alert Notifications */}
      {errorMessage && (
        <div className="bg-rose-50 border-b border-rose-200 px-4 py-2.5 flex items-center justify-between text-xs text-rose-800 animate-in fade-in duration-200">
          <div className="flex items-center gap-2 max-w-4xl mx-auto w-full">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span><strong>Kesalahan:</strong> {errorMessage}</span>
          </div>
          <button
            onClick={() => setErrorMessage(null)}
            className="text-rose-500 hover:text-rose-800 font-bold ml-4"
          >
            ✕
          </button>
        </div>
      )}

      {successMessage && (
        <div className="bg-emerald-50 border-b border-emerald-200 px-4 py-2.5 flex items-center justify-between text-xs text-emerald-800 animate-in fade-in duration-200">
          <div className="flex items-center gap-2 max-w-4xl mx-auto w-full">
            <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>{successMessage}</span>
          </div>
          <button
            onClick={() => setSuccessMessage(null)}
            className="text-emerald-500 hover:text-emerald-800 font-bold ml-4"
          >
            ✕
          </button>
        </div>
      )}

      {/* Main Multi-Column Studio Workspace */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 space-y-4">
        {/* Row 1: Left (Library + Pipeline) and Right (Image Workspace + Inspector) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          {/* Left Column (5 Cols): Operation Library and Pipeline Builder */}
          <div className="lg:col-span-5 flex flex-col gap-4">
            {/* Operation Library */}
            <div className="h-[360px]">
              <OperationLibrary
                operations={operations}
                onAddOperation={handleAddOperation}
                onInspectOperation={(op) => setActiveTheoryOp(op)}
              />
            </div>

            {/* Pipeline Builder */}
            <div className="h-[380px]">
              <PipelineBuilder
                steps={pipelineSteps}
                operationsMap={operationsMap}
                selectedStepId={selectedStepId}
                stageResultsMap={stageResults}
                isProcessing={isProcessing}
                onSelectStep={(id) => setSelectedStepId(id)}
                onToggleStep={handleToggleStep}
                onRemoveStep={handleRemoveStep}
                onDuplicateStep={handleDuplicateStep}
                onReorderSteps={(newSteps) => setPipelineSteps(newSteps)}
                onClearPipeline={handleClearPipeline}
                onExecutePipeline={handleExecutePipeline}
              />
            </div>
          </div>

          {/* Right Column (7 Cols): Image Workspace & Parameter Inspector */}
          <div className="lg:col-span-7 flex flex-col gap-4">
            {/* Image Workspace */}
            <div className="h-[430px]">
              <ImageWorkspace
                originalImageBase64={originalImage}
                processedImageBase64={processedImage}
                selectedStageResult={selectedStageResult}
                imageStats={imageStats}
                isProcessing={isProcessing}
                onImageSelected={handleImageSelected}
                onDownloadFinal={handleDownloadImage}
                onResetOriginal={() => {
                  setOriginalImage(null);
                  setProcessedImage(null);
                  setStageResults(new Map());
                  setImageStats(null);
                  setOriginalHistogram(null);
                  setProcessedHistogram(null);
                }}
              />
            </div>

            {/* Parameter Inspector & Academic Explanation */}
            <div className="h-[310px]">
              <ParameterInspector
                selectedStep={selectedStep}
                operation={selectedOperation}
                onUpdateConfig={handleUpdateConfig}
                onOpenFullTheory={() => {
                  if (selectedOperation) setActiveTheoryOp(selectedOperation);
                }}
              />
            </div>
          </div>
        </div>

        {/* Row 2: Full Width Histogram & Statistics Workspace */}
        <div className="w-full">
          <HistogramWorkspace
            originalHistogram={originalHistogram}
            processedHistogram={processedHistogram}
            activeStats={imageStats}
            selectedOperationName={selectedOperation?.name}
          />
        </div>
      </main>

      {/* Academic Theory Modal */}
      <AcademicTheoryModal
        operation={activeTheoryOp}
        onClose={() => setActiveTheoryOp(null)}
      />

      {/* Preset Workflow Modal */}
      <PresetModal
        isOpen={isPresetModalOpen}
        onClose={() => setIsPresetModalOpen(false)}
        onLoadPreset={handleLoadPreset}
      />

      {/* About & Collaboration Modal */}
      <AboutModal
        isOpen={isAboutModalOpen}
        onClose={() => setIsAboutModalOpen(false)}
      />
    </div>
  );
};

export default App;
