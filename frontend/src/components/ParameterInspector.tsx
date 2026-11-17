import React from 'react';
import type { OperationMetadata, PipelineStep } from '../types';
import {
  Sliders,
  HelpCircle,
  Binary,
  ArrowRightLeft,
  BookOpen,
} from 'lucide-react';

interface ParameterInspectorProps {
  selectedStep: PipelineStep | null;
  operation: OperationMetadata | null;
  onUpdateConfig: (stepId: string, newConfig: Record<string, any>) => void;
  onOpenFullTheory: () => void;
}

export const ParameterInspector: React.FC<ParameterInspectorProps> = ({
  selectedStep,
  operation,
  onUpdateConfig,
  onOpenFullTheory,
}) => {
  if (!selectedStep || !operation) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-6 flex flex-col items-center justify-center text-center h-full">
        <div className="w-12 h-12 rounded-xl bg-slate-100 text-slate-400 flex items-center justify-center mb-3">
          <Sliders className="w-6 h-6" />
        </div>
        <h3 className="text-xs font-semibold text-slate-800">Tidak Ada Tahap Terpilih</h3>
        <p className="text-[11px] text-slate-400 mt-1 max-w-[240px] leading-relaxed">
          Pilih salah satu tahap pada Pipeline Builder untuk menyesuaikan parameter operasi dan melihat penjelasan teorinya.
        </p>
      </div>
    );
  }

  const currentConfig = {
    ...operation.default_config,
    ...selectedStep.config,
  };

  const handleParamChange = (paramName: string, value: any) => {
    const updated = {
      ...currentConfig,
      [paramName]: value,
    };
    onUpdateConfig(selectedStep.step_id, updated);
  };

  // Generate local structuring element matrix preview for Erosion and Dilation
  const renderKernelMatrixPreview = () => {
    if (!operation.has_kernel_preview) return null;

    const shape = currentConfig.kernel_shape || 'rect';
    const size = Number(currentConfig.kernel_size) || 3;

    const matrix: number[][] = [];
    const radius = Math.floor(size / 2);

    for (let r = 0; r < size; r++) {
      const row: number[] = [];
      for (let c = 0; c < size; c++) {
        let val = 0;
        if (shape === 'rect') {
          val = 1;
        } else if (shape === 'cross') {
          val = r === radius || c === radius ? 1 : 0;
        } else if (shape === 'ellipse') {
          const dy = r - radius;
          const dx = c - radius;
          val = (dx * dx) / ((radius + 0.1) * (radius + 0.1)) + (dy * dy) / ((radius + 0.1) * (radius + 0.1)) <= 1.05 ? 1 : 0;
        }
        row.push(val);
      }
      matrix.push(row);
    }

    return (
      <div className="mt-4 p-3 bg-slate-50 rounded-lg border border-slate-200">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[11px] font-semibold text-slate-700 flex items-center gap-1.5">
            <Binary className="w-3.5 h-3.5 text-blue-600" />
            Visualisasi Matriks Elemen Penstruktur ({size} × {size})
          </span>
          <span className="text-[10px] text-slate-400 uppercase font-mono">{shape}</span>
        </div>

        <div className="flex justify-center py-2">
          <div
            className="grid gap-1 bg-slate-200 p-1.5 rounded-md shadow-inner"
            style={{ gridTemplateColumns: `repeat(${size}, minmax(0, 1fr))` }}
          >
            {matrix.map((row, rIdx) =>
              row.map((cell, cIdx) => (
                <div
                  key={`${rIdx}-${cIdx}`}
                  className={`w-5 h-5 rounded flex items-center justify-center text-[10px] font-bold font-mono transition-colors ${
                    cell === 1
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'bg-white text-slate-300'
                  }`}
                  title={`(${rIdx}, ${cIdx}): ${cell}`}
                >
                  {cell}
                </div>
              ))
            )}
          </div>
        </div>
        <p className="text-[10px] text-slate-500 text-center mt-1">
          Piksel biru (1) mendefinisikan area tetangga yang diuji nilai minimum/maksimumnya.
        </p>
      </div>
    );
  };

  // Axis illustration for Mirroring
  const renderMirrorAxisPreview = () => {
    if (operation.id !== 'geometry_mirroring') return null;
    const axis = currentConfig.axis || 'horizontal';

    return (
      <div className="mt-4 p-3 bg-slate-50 rounded-lg border border-slate-200">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[11px] font-semibold text-slate-700 flex items-center gap-1.5">
            <ArrowRightLeft className="w-3.5 h-3.5 text-blue-600" />
            Ilustrasi Sumbu Transformasi
          </span>
          <span className="text-[10px] font-mono text-blue-600 uppercase font-semibold">{axis}</span>
        </div>

        <div className="flex items-center justify-center p-3">
          <div className="relative w-36 h-24 border-2 border-dashed border-slate-300 rounded bg-white flex items-center justify-center">
            {axis === 'horizontal' && (
              <>
                <div className="absolute top-0 bottom-0 left-1/2 w-0.5 bg-rose-500 shadow" />
                <span className="text-[10px] text-rose-600 font-bold absolute -top-4">Sumbu Y</span>
                <span className="text-xs font-semibold text-slate-700">Kiri ↔ Kanan</span>
              </>
            )}
            {axis === 'vertical' && (
              <>
                <div className="absolute left-0 right-0 top-1/2 h-0.5 bg-rose-500 shadow" />
                <span className="text-[10px] text-rose-600 font-bold absolute -right-5">Sumbu X</span>
                <span className="text-xs font-semibold text-slate-700">Atas ↕ Bawah</span>
              </>
            )}
            {axis === 'both' && (
              <>
                <div className="absolute top-0 bottom-0 left-1/2 w-0.5 bg-rose-500 shadow" />
                <div className="absolute left-0 right-0 top-1/2 h-0.5 bg-rose-500 shadow" />
                <span className="text-xs font-semibold text-slate-700">Rotasi 180°</span>
              </>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-slate-200 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-blue-600" />
            <h2 className="text-sm font-semibold text-slate-900">{operation.name}</h2>
          </div>
          <span className="text-[11px] text-slate-500">
            {operation.category}
          </span>
        </div>

        <button
          onClick={onOpenFullTheory}
          className="flex items-center gap-1 px-2.5 py-1 text-[11px] font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-md transition-colors"
          title="Baca seluruh teori akademik & rumus KaTeX"
        >
          <BookOpen className="w-3 h-3" />
          <span>Lihat Teori</span>
        </button>
      </div>

      {/* Content Form & Explanation */}
      <div className="p-4 overflow-y-auto space-y-4 flex-1">
        {/* Parameter Fields */}
        <div className="space-y-3">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
            Pengaturan Parameter
          </span>

          {operation.config_schema.length === 0 ? (
            <p className="text-xs text-slate-500 italic">
              Operasi ini tidak memerlukan parameter input tambahan.
            </p>
          ) : (
            operation.config_schema.map((field) => {
              const val = currentConfig[field.name] ?? field.default;

              return (
                <div key={field.name} className="space-y-1">
                  <div className="flex items-center justify-between">
                    <label className="text-xs font-medium text-slate-700">
                      {field.label}
                    </label>
                    {field.type === 'slider' && (
                      <span className="text-xs font-mono font-bold text-blue-600">
                        {val}
                      </span>
                    )}
                  </div>

                  {field.type === 'select' && field.options && (
                    <select
                      value={val}
                      onChange={(e) => {
                        const raw = e.target.value;
                        const num = Number(raw);
                        handleParamChange(field.name, isNaN(num) ? raw : num);
                      }}
                      className="w-full text-xs rounded-lg border border-slate-200 p-2 bg-slate-50/50 focus:bg-white focus:outline-none focus:ring-1 focus:ring-blue-500"
                    >
                      {field.options.map((opt) => (
                        <option key={String(opt.value)} value={String(opt.value)}>
                          {opt.label}
                        </option>
                      ))}
                    </select>
                  )}

                  {field.type === 'slider' && (
                    <input
                      type="range"
                      min={field.min_value ?? 0}
                      max={field.max_value ?? 100}
                      step={field.step ?? 1}
                      value={val}
                      onChange={(e) => handleParamChange(field.name, Number(e.target.value))}
                      className="w-full accent-blue-600 cursor-pointer"
                    />
                  )}

                  {field.description && (
                    <p className="text-[10px] text-slate-400">{field.description}</p>
                  )}
                </div>
              );
            })
          )}
        </div>

        {/* Custom Matrix / Visualizer Preview */}
        {renderKernelMatrixPreview()}
        {renderMirrorAxisPreview()}

        {/* Academic "Why is it like this?" Card */}
        <div className="p-3 rounded-lg bg-blue-50/60 border border-blue-200 text-xs">
          <div className="flex items-center gap-1.5 font-semibold text-blue-900 mb-1">
            <HelpCircle className="w-3.5 h-3.5 text-blue-600 shrink-0" />
            <span>Mengapa Hasilnya Seperti Ini?</span>
          </div>
          <p className="text-[11px] text-blue-800 leading-relaxed">
            {operation.explanation.mengapa_seperti_ini}
          </p>
        </div>
      </div>
    </div>
  );
};
