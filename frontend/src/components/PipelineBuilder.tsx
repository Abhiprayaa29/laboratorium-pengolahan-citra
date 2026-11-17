import React from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from '@dnd-kit/core';
import {
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
  useSortable,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import type { OperationMetadata, PipelineStep, StepExecutionResult } from '../types';
import {
  GripVertical,
  Play,
  Trash2,
  Copy,
  Sliders,
  CheckCircle,
  AlertCircle,
  RotateCcw,
  Layers,
  Eye,
  EyeOff,
} from 'lucide-react';

interface PipelineBuilderProps {
  steps: PipelineStep[];
  operationsMap: Map<string, OperationMetadata>;
  selectedStepId: string | null;
  stageResultsMap: Map<string, StepExecutionResult>;
  isProcessing: boolean;
  onSelectStep: (stepId: string) => void;
  onToggleStep: (stepId: string) => void;
  onRemoveStep: (stepId: string) => void;
  onDuplicateStep: (stepId: string) => void;
  onReorderSteps: (newSteps: PipelineStep[]) => void;
  onClearPipeline: () => void;
  onExecutePipeline: () => void;
}

interface SortableItemProps {
  step: PipelineStep;
  index: number;
  operation?: OperationMetadata;
  stageResult?: StepExecutionResult;
  isSelected: boolean;
  onSelect: () => void;
  onToggle: () => void;
  onRemove: () => void;
  onDuplicate: () => void;
}

const SortableStepItem: React.FC<SortableItemProps> = ({
  step,
  index,
  operation,
  stageResult,
  isSelected,
  onSelect,
  onToggle,
  onRemove,
  onDuplicate,
}) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: step.step_id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    zIndex: isDragging ? 20 : 1,
  };

  const opName = operation?.name || step.operation_id;
  const isEnabled = step.enabled;

  return (
    <div
      ref={setNodeRef}
      style={style}
      onClick={onSelect}
      className={`group relative flex items-center gap-2 p-2.5 rounded-lg border text-xs transition-all cursor-pointer ${
        isDragging
          ? 'opacity-60 shadow-lg border-blue-400 bg-blue-50/50'
          : isSelected
          ? 'border-blue-600 bg-blue-50/40 ring-1 ring-blue-500 shadow-xs'
          : isEnabled
          ? 'border-slate-200 hover:border-slate-300 bg-white'
          : 'border-slate-200 bg-slate-50/80 opacity-60'
      }`}
    >
      {/* Drag Handle */}
      <button
        type="button"
        {...attributes}
        {...listeners}
        className="p-1 text-slate-400 hover:text-slate-700 cursor-grab active:cursor-grabbing rounded"
        title="Geser untuk mengubah urutan tahapan"
        onClick={(e) => e.stopPropagation()}
      >
        <GripVertical className="w-4 h-4" />
      </button>

      {/* Step Number Badge */}
      <div
        className={`w-5 h-5 rounded-full flex items-center justify-center font-bold text-[10px] shrink-0 ${
          isEnabled ? 'bg-blue-600 text-white' : 'bg-slate-300 text-slate-600'
        }`}
      >
        {index + 1}
      </div>

      {/* Operation Title */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-1.5">
          <span className={`font-semibold truncate ${isEnabled ? 'text-slate-900' : 'text-slate-500 line-through'}`}>
            {opName}
          </span>
        </div>

        {/* Execution indicator */}
        {stageResult && (
          <div className="flex items-center gap-1.5 mt-0.5 text-[10px]">
            {stageResult.error ? (
              <span className="text-rose-600 flex items-center gap-0.5">
                <AlertCircle className="w-2.5 h-2.5" />
                Error
              </span>
            ) : stageResult.enabled ? (
              <span className="text-emerald-600 flex items-center gap-0.5">
                <CheckCircle className="w-2.5 h-2.5" />
                Selesai ({stageResult.execution_time_ms} ms)
              </span>
            ) : (
              <span className="text-slate-400">Dilewati</span>
            )}
          </div>
        )}
      </div>

      {/* Action Controls */}
      <div className="flex items-center gap-1 shrink-0" onClick={(e) => e.stopPropagation()}>
        {/* Toggle Enabled */}
        <button
          type="button"
          onClick={onToggle}
          className={`p-1 rounded transition-colors ${
            isEnabled ? 'text-blue-600 hover:bg-blue-100' : 'text-slate-400 hover:bg-slate-200'
          }`}
          title={isEnabled ? 'Nonaktifkan operasi ini' : 'Aktifkan kembali operasi ini'}
        >
          {isEnabled ? <Eye className="w-3.5 h-3.5" /> : <EyeOff className="w-3.5 h-3.5" />}
        </button>

        {/* Configure / Inspect */}
        <button
          type="button"
          onClick={onSelect}
          className={`p-1 rounded transition-colors ${
            isSelected ? 'text-blue-600 bg-blue-100' : 'text-slate-400 hover:bg-slate-100'
          }`}
          title="Atur parameter dan lihat teori"
        >
          <Sliders className="w-3.5 h-3.5" />
        </button>

        {/* Duplicate */}
        <button
          type="button"
          onClick={onDuplicate}
          className="p-1 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded transition-colors"
          title="Duplikat tahap ini"
        >
          <Copy className="w-3.5 h-3.5" />
        </button>

        {/* Remove */}
        <button
          type="button"
          onClick={onRemove}
          className="p-1 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded transition-colors"
          title="Hapus dari pipeline"
        >
          <Trash2 className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};

export const PipelineBuilder: React.FC<PipelineBuilderProps> = ({
  steps,
  operationsMap,
  selectedStepId,
  stageResultsMap,
  isProcessing,
  onSelectStep,
  onToggleStep,
  onRemoveStep,
  onDuplicateStep,
  onReorderSteps,
  onClearPipeline,
  onExecutePipeline,
}) => {
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 4,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (over && active.id !== over.id) {
      const oldIndex = steps.findIndex((s) => s.step_id === active.id);
      const newIndex = steps.findIndex((s) => s.step_id === over.id);
      if (oldIndex !== -1 && newIndex !== -1) {
        const reordered = [...steps];
        const [moved] = reordered.splice(oldIndex, 1);
        reordered.splice(newIndex, 0, moved);
        onReorderSteps(reordered);
      }
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-slate-200 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-blue-600" />
          <h2 className="text-sm font-semibold text-slate-900">Pipeline Pemrosesan</h2>
          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-medium">
            {steps.length} Tahap
          </span>
        </div>

        {steps.length > 0 && (
          <button
            onClick={onClearPipeline}
            className="flex items-center gap-1 text-[11px] font-medium text-slate-500 hover:text-rose-600 transition-colors"
            title="Kosongkan seluruh tahap"
          >
            <RotateCcw className="w-3 h-3" />
            <span>Reset</span>
          </button>
        )}
      </div>

      {/* Pipeline Steps List (Sortable) */}
      <div className="p-3 overflow-y-auto space-y-2 flex-1">
        {steps.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-6 border-2 border-dashed border-slate-200 rounded-lg bg-slate-50/50">
            <Layers className="w-8 h-8 text-slate-300 mb-2" />
            <p className="text-xs font-medium text-slate-700">Pipeline Masih Kosong</p>
            <p className="text-[11px] text-slate-400 mt-1 max-w-[220px]">
              Klik tombol "Pilih" pada Katalog Operasi atau gunakan Preset Alur Kerja untuk menambahkan tahapan.
            </p>
          </div>
        ) : (
          <DndContext
            sensors={sensors}
            collisionDetection={closestCenter}
            onDragEnd={handleDragEnd}
          >
            <SortableContext
              items={steps.map((s) => s.step_id)}
              strategy={verticalListSortingStrategy}
            >
              <div className="space-y-2">
                {steps.map((step, index) => {
                  const op = operationsMap.get(step.operation_id);
                  const stageRes = stageResultsMap.get(step.step_id);

                  return (
                    <SortableStepItem
                      key={step.step_id}
                      step={step}
                      index={index}
                      operation={op}
                      stageResult={stageRes}
                      isSelected={selectedStepId === step.step_id}
                      onSelect={() => onSelectStep(step.step_id)}
                      onToggle={() => onToggleStep(step.step_id)}
                      onRemove={() => onRemoveStep(step.step_id)}
                      onDuplicate={() => onDuplicateStep(step.step_id)}
                    />
                  );
                })}
              </div>
            </SortableContext>
          </DndContext>
        )}
      </div>

      {/* Execution Footer Bar */}
      <div className="p-3 border-t border-slate-200 bg-slate-50/60 flex items-center justify-between gap-3">
        <div className="text-[11px] text-slate-500">
          Alur: <span className="font-medium text-slate-700">Asli → 1 → 2 → ... → Final</span>
        </div>

        <button
          onClick={onExecutePipeline}
          disabled={steps.length === 0 || isProcessing}
          className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold shadow-xs transition-all ${
            steps.length === 0 || isProcessing
              ? 'bg-slate-300 text-slate-500 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 text-white shadow-blue-500/20 active:scale-98'
          }`}
        >
          <Play className={`w-3.5 h-3.5 fill-current ${isProcessing ? 'animate-spin' : ''}`} />
          <span>{isProcessing ? 'Memproses di Python...' : 'Jalankan Pipeline'}</span>
        </button>
      </div>
    </div>
  );
};
