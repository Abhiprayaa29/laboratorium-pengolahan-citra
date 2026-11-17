import React, { useState } from 'react';
import type { OperationMetadata } from '../types';
import {
  Layers,
  Sparkles,
  Scissors,
  BarChart3,
  Plus,
  Info,
  Clock,
  CheckCircle2,
  Lock,
} from 'lucide-react';

interface OperationLibraryProps {
  operations: OperationMetadata[];
  onAddOperation: (op: OperationMetadata) => void;
  onInspectOperation: (op: OperationMetadata) => void;
}

const CATEGORIES = [
  {
    id: 'Operasi Morfologi dan Geometri',
    name: 'Morfologi & Geometri',
    icon: Scissors,
  },
  {
    id: 'Transformasi Warna dan Intensitas',
    name: 'Warna & Intensitas',
    icon: Layers,
  },
  {
    id: 'Filter dan Efek Visual',
    name: 'Filter & Efek',
    icon: Sparkles,
  },
  {
    id: 'Segmentasi, Histogram, dan Deteksi Tepi',
    name: 'Segmentasi & Tepi',
    icon: BarChart3,
  },
];

export const OperationLibrary: React.FC<OperationLibraryProps> = ({
  operations,
  onAddOperation,
  onInspectOperation,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>(
    'Operasi Morfologi dan Geometri'
  );

  const filteredOps = operations.filter(
    (op) => op.category.toLowerCase() === selectedCategory.toLowerCase()
  );

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs flex flex-col h-full overflow-hidden">
      {/* Panel Header */}
      <div className="px-4 py-3 border-b border-slate-200">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-slate-900">
            Katalog Operasi Citra
          </h2>
          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-medium">
            {operations.length} Operasi
          </span>
        </div>
        <p className="text-xs text-slate-500 mt-0.5">
          Pilih operasi pengolahan citra digital untuk ditambahkan ke pipeline pemrosesan.
        </p>
      </div>

      {/* Category Tabs - Clean, without member labels */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-1 p-2 bg-slate-50/70 border-b border-slate-200">
        {CATEGORIES.map((cat) => {
          const Icon = cat.icon;
          const isActive = selectedCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`flex items-center justify-center gap-1.5 py-2 px-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-white text-blue-700 shadow-xs border border-blue-200 ring-1 ring-blue-500/20'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
              }`}
            >
              <Icon className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-blue-600' : 'text-slate-400'}`} />
              <span className="truncate">{cat.name}</span>
            </button>
          );
        })}
      </div>

      {/* Operations List */}
      <div className="p-3 overflow-y-auto space-y-2.5 flex-1">
        {filteredOps.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-400">
            Memuat daftar operasi dari backend...
          </div>
        ) : (
          filteredOps.map((op) => {
            const isReady = op.status === 'ready';

            return (
              <div
                key={op.id}
                className={`p-3 rounded-lg border transition-all ${
                  isReady
                    ? 'border-slate-200 hover:border-blue-300 hover:shadow-xs bg-white'
                    : 'border-dashed border-slate-200 bg-slate-50/60 opacity-80'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-semibold text-xs text-slate-900 truncate">
                        {op.name}
                      </span>

                      {/* Status Badge */}
                      {isReady ? (
                        <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                          <CheckCircle2 className="w-2.5 h-2.5" />
                          Siap
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-medium bg-amber-50 text-amber-700 border border-amber-200">
                          <Clock className="w-2.5 h-2.5" />
                          Dalam Pengembangan
                        </span>
                      )}
                    </div>

                    <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed">
                      {op.description}
                    </p>

                    {op.has_kernel_preview && (
                      <div className="mt-2 text-[11px] text-blue-600 font-medium">
                        ✓ Dilengkapi Visualisasi Matriks Kernel 2D
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex flex-col gap-1.5 shrink-0">
                    <button
                      onClick={() => onInspectOperation(op)}
                      className="p-1 rounded text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
                      title="Lihat Teori, Rumus KaTeX, dan Parameter"
                    >
                      <Info className="w-3.5 h-3.5" />
                    </button>

                    <button
                      onClick={() => onAddOperation(op)}
                      disabled={!isReady}
                      className={`flex items-center gap-1 px-2.5 py-1 rounded text-xs font-medium transition-all ${
                        isReady
                          ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-xs active:scale-95'
                          : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                      }`}
                      title={
                        isReady
                          ? 'Tambahkan operasi ke Pipeline'
                          : 'Operasi ini sedang dalam pengembangan'
                      }
                    >
                      {isReady ? (
                        <>
                          <Plus className="w-3 h-3" />
                          <span>Pilih</span>
                        </>
                      ) : (
                        <>
                          <Lock className="w-3 h-3" />
                          <span>Terkunci</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
