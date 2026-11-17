import React from 'react';
import type { PipelineStep } from '../types';
import { Sparkles, X, ArrowRight, Play } from 'lucide-react';

interface PresetModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLoadPreset: (steps: PipelineStep[], name: string) => void;
}

interface PresetItem {
  id: string;
  name: string;
  category: string;
  description: string;
  academicObjective: string;
  steps: { operation_id: string; config: Record<string, any>; label: string }[];
}

const PRESETS: PresetItem[] = [
  {
    id: 'preset-opening',
    name: 'Morfologi Opening (Erosi → Dilasi)',
    category: 'Operasi Morfologi',
    description: 'Menghilangkan bintik derau putih (salt noise) kecil di luar objek tanpa mengubah ukuran keseluruhan objek dominan.',
    academicObjective: 'Membuktikan sifat opening: f ○ B = (f ⊖ B) ⊕ B.',
    steps: [
      {
        operation_id: 'morphology_erosion',
        config: { kernel_shape: 'rect', kernel_size: 3, iterations: 1, mode: 'rgb' },
        label: '1. Erosi 3×3 (Mengikis derau kecil)',
      },
      {
        operation_id: 'morphology_dilation',
        config: { kernel_shape: 'rect', kernel_size: 3, iterations: 1, mode: 'rgb' },
        label: '2. Dilasi 3×3 (Memulihkan ukuran objek utama)',
      },
    ],
  },
  {
    id: 'preset-closing',
    name: 'Morfologi Closing (Dilasi → Erosi)',
    category: 'Operasi Morfologi',
    description: 'Menjembatani rekahan atau menutup lubang hitam (pepper noise) di dalam area objek putih.',
    academicObjective: 'Membuktikan sifat closing: f ● B = (f ⊕ B) ⊖ B.',
    steps: [
      {
        operation_id: 'morphology_dilation',
        config: { kernel_shape: 'rect', kernel_size: 3, iterations: 1, mode: 'rgb' },
        label: '1. Dilasi 3×3 (Menutup celah & lubang)',
      },
      {
        operation_id: 'morphology_erosion',
        config: { kernel_shape: 'rect', kernel_size: 3, iterations: 1, mode: 'rgb' },
        label: '2. Erosi 3×3 (Mengembalikan kontur batas semula)',
      },
    ],
  },
  {
    id: 'preset-mirror-involution',
    name: 'Involusi Geometri: Double Horizontal Flip',
    category: 'Transformasi Geometri',
    description: 'Pencerminan dua kali berturut-turut pada sumbu horizontal untuk membuktikan sifat involusi matematika citra.',
    academicObjective: 'Membuktikan M(M(I)) = I: citra kembali 100% tepat seperti aslinya dan histogram tetap identik.',
    steps: [
      {
        operation_id: 'geometry_mirroring',
        config: { axis: 'horizontal' },
        label: '1. Pencerminan Horizontal (x\' = W - 1 - x)',
      },
      {
        operation_id: 'geometry_mirroring',
        config: { axis: 'horizontal' },
        label: '2. Pencerminan Horizontal Ulang (x\'\' = x)',
      },
    ],
  },
  {
    id: 'preset-dual-axis-rotation',
    name: 'Rotasi 180°: Horizontal + Vertikal',
    category: 'Transformasi Geometri',
    description: 'Menggabungkan pencerminan sumbu horizontal dan vertikal secara berurutan menghasilkan rotasi simetris 180 derajat.',
    academicObjective: 'Membuktikan komposisi pemetaan koordinat (W - 1 - x, H - 1 - y).',
    steps: [
      {
        operation_id: 'geometry_mirroring',
        config: { axis: 'horizontal' },
        label: '1. Flip Horizontal (Sumbu Y)',
      },
      {
        operation_id: 'geometry_mirroring',
        config: { axis: 'vertical' },
        label: '2. Flip Vertikal (Sumbu X)',
      },
    ],
  },
  {
    id: 'preset-morphology-progressive',
    name: 'Erosi Progresif Multi-Iterasi',
    category: 'Operasi Morfologi',
    description: 'Melihat efek pengikisan bertingkat mulai dari kernel kecil ke kernel yang lebih besar.',
    academicObjective: 'Membandingkan degradasi ketebalan objek piksel putih pada setiap tahapan intermediate.',
    steps: [
      {
        operation_id: 'morphology_erosion',
        config: { kernel_shape: 'rect', kernel_size: 3, iterations: 1, mode: 'rgb' },
        label: '1. Erosi Ringan (3×3 Rect)',
      },
      {
        operation_id: 'morphology_erosion',
        config: { kernel_shape: 'ellipse', kernel_size: 5, iterations: 1, mode: 'rgb' },
        label: '2. Erosi Lanjutan (5×5 Ellipse)',
      },
    ],
  },
];

export const PresetModal: React.FC<PresetModalProps> = ({
  isOpen,
  onClose,
  onLoadPreset,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-xl w-full max-h-[85vh] flex flex-col shadow-2xl border border-slate-200 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/70">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center shadow-xs">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">Preset Alur Kerja Praktikum</h2>
              <p className="text-xs text-slate-500">
                Pilih kombinasi pipeline yang telah dirancang untuk pembuktian konsep akademik.
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Preset List */}
        <div className="p-6 overflow-y-auto space-y-4">
          {PRESETS.map((preset) => (
            <div
              key={preset.id}
              className="p-4 rounded-xl border border-slate-200 hover:border-blue-300 hover:shadow-xs transition-all bg-white"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-xs text-slate-900">{preset.name}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 font-medium">
                      {preset.category}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600">{preset.description}</p>
                  <p className="text-[11px] text-blue-600 font-medium">
                    🎯 {preset.academicObjective}
                  </p>
                </div>

                <button
                  onClick={() => {
                    const mappedSteps: PipelineStep[] = preset.steps.map((st, i) => ({
                      step_id: `step-${Date.now()}-${i}`,
                      operation_id: st.operation_id,
                      enabled: true,
                      config: { ...st.config },
                    }));
                    onLoadPreset(mappedSteps, preset.name);
                    onClose();
                  }}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shrink-0 shadow-xs transition-colors"
                >
                  <Play className="w-3 h-3 fill-current" />
                  <span>Terapkan</span>
                </button>
              </div>

              {/* Step Badges */}
              <div className="mt-3 pt-3 border-t border-slate-100 flex flex-wrap items-center gap-1.5">
                <span className="text-[10px] text-slate-400">Rangkaian:</span>
                {preset.steps.map((st, idx) => (
                  <React.Fragment key={idx}>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-mono">
                      {st.label}
                    </span>
                    {idx < preset.steps.length - 1 && (
                      <ArrowRight className="w-3 h-3 text-slate-300" />
                    )}
                  </React.Fragment>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-slate-600 hover:text-slate-800 text-xs font-medium"
          >
            Tutup
          </button>
        </div>
      </div>
    </div>
  );
};
