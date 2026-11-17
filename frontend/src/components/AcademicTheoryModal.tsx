import React from 'react';
import type { OperationMetadata } from '../types';
import {
  X,
  BookOpen,
  HelpCircle,
  Calculator,
  Compass,
  CheckCircle2,
  Sliders,
  BarChart,
  Lightbulb,
} from 'lucide-react';

interface AcademicTheoryModalProps {
  operation: OperationMetadata | null;
  onClose: () => void;
}

export const AcademicTheoryModal: React.FC<AcademicTheoryModalProps> = ({
  operation,
  onClose,
}) => {
  if (!operation) return null;

  const exp = operation.explanation;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl border border-slate-200 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/70">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center shadow-xs">
              <BookOpen className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">{operation.name}</h2>
              <p className="text-xs text-slate-500">
                {operation.category} • Penanggung Jawab: <span className="font-semibold text-slate-700">{operation.owner}</span>
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

        {/* Scrollable Academic Sections */}
        <div className="p-6 overflow-y-auto space-y-5 text-xs text-slate-700 leading-relaxed">
          {/* Section 1: Pengertian */}
          <div className="space-y-1">
            <span className="font-bold text-slate-900 text-xs flex items-center gap-1.5 text-blue-700">
              <Compass className="w-3.5 h-3.5" />
              1. Pengertian
            </span>
            <p className="text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-100">
              {exp.pengertian}
            </p>
          </div>

          {/* Section 2: Tujuan */}
          <div className="space-y-1">
            <span className="font-bold text-slate-900 text-xs flex items-center gap-1.5 text-blue-700">
              <CheckCircle2 className="w-3.5 h-3.5" />
              2. Tujuan
            </span>
            <div className="text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-100 whitespace-pre-line">
              {exp.tujuan}
            </div>
          </div>

          {/* Section 3 & 4: Cara Kerja & Rumus Matematis */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="space-y-1">
              <span className="font-bold text-slate-900 text-xs flex items-center gap-1.5 text-blue-700">
                <Sliders className="w-3.5 h-3.5" />
                3. Cara Kerja
              </span>
              <p className="text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-100 h-full">
                {exp.cara_kerja}
              </p>
            </div>

            <div className="space-y-1">
              <span className="font-bold text-slate-900 text-xs flex items-center gap-1.5 text-blue-700">
                <Calculator className="w-3.5 h-3.5" />
                4. Rumus Matematis
              </span>
              <div className="bg-slate-900 text-emerald-400 font-mono p-3 rounded-lg text-xs flex items-center justify-center text-center overflow-x-auto h-full">
                <code>{exp.rumus_matematis}</code>
              </div>
            </div>
          </div>

          {/* Section 5 & 6: Pengaruh Gambar & Histogram */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="space-y-1">
              <span className="font-bold text-slate-900 text-xs flex items-center gap-1.5 text-blue-700">
                <Lightbulb className="w-3.5 h-3.5" />
                5. Pengaruh pada Citra
              </span>
              <p className="text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-100">
                {exp.pengaruh_gambar}
              </p>
            </div>

            <div className="space-y-1">
              <span className="font-bold text-slate-900 text-xs flex items-center gap-1.5 text-blue-700">
                <BarChart className="w-3.5 h-3.5" />
                6. Pengaruh pada Histogram
              </span>
              <p className="text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-100">
                {exp.pengaruh_histogram}
              </p>
            </div>
          </div>

          {/* Section 7: Mengapa hasilnya seperti ini? */}
          <div className="p-4 rounded-xl bg-blue-50/80 border border-blue-200">
            <div className="flex items-center gap-1.5 font-bold text-blue-900 text-xs mb-1">
              <HelpCircle className="w-4 h-4 text-blue-600" />
              <span>Mengapa Hasilnya Seperti Ini?</span>
            </div>
            <p className="text-blue-800 text-xs leading-relaxed">
              {exp.mengapa_seperti_ini}
            </p>
          </div>

          {/* Section 8: Contoh Penerapan */}
          <div className="space-y-1">
            <span className="font-bold text-slate-900 text-xs flex items-center gap-1.5 text-slate-700">
              7. Contoh Penerapan di Dunia Nyata
            </span>
            <p className="text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-100">
              {exp.contoh_penerapan}
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-xs transition-colors"
          >
            Tutup Penjelasan
          </button>
        </div>
      </div>
    </div>
  );
};
