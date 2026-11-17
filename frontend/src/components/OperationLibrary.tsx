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
    member: 'Modul 3 (Orang 3) — Siap',
    color: 'border-blue-500 text-blue-600',
    highlight: true,
  },
  {
    id: 'Transformasi Warna dan Intensitas',
    name: 'Warna & Intensitas',
    icon: Layers,
    member: 'Modul 1 (Orang 1)',
    color: 'border-slate-300 text-slate-600',
    highlight: false,
  },
  {
    id: 'Filter dan Efek Visual',
    name: 'Filter & Efek',
    icon: Sparkles,
    member: 'Modul 2 (Orang 2)',
    color: 'border-slate-300 text-slate-600',
    highlight: false,
  },
  {
    id: 'Segmentasi, Histogram, dan Deteksi Tepi',
    name: 'Segmentasi & Tepi',
    icon: BarChart3,
    member: 'Modul 4 (Orang 4)',
    color: 'border-slate-300 text-slate-600',
    highlight: false,
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
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs flex flex-col h-full">
      {/* Panel Header */}
      <div className="px-4 py-3 border-b border-slate-200">
        <h2 className="text-sm font-semibold text-slate-900 flex items-center justify-between">
          <span>Katalog Operasi Citra</span>
          <span className="text-xs font-normal text-slate-500">
            {operations.length} Algoritma Terdaftar
          </span>
        </h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Pilih algoritma pengolahan citra dari 4 modul kelompok untuk ditambahkan ke pipeline.
        </p>
      </div>

      {/* Category Tabs */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-1 p-2 bg-slate-50/70 border-b border-slate-200">
        {CATEGORIES.map((cat) => {
          const Icon = cat.icon;
          const isActive = selectedCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`flex flex-col items-center justify-center py-2 px-2 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-white text-blue-700 shadow-xs border border-blue-200 ring-1 ring-blue-500/20'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
              }`}
            >
              <div className="flex items-center gap-1.5 mb-0.5">
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-blue-600' : 'text-slate-400'}`} />
                <span className="truncate">{cat.name}</span>
              </div>
              <span className="text-[10px] text-slate-400 scale-95">{cat.member.split('—')[0]}</span>
            </button>
          );
        })}
      </div>

      {/* Operations List */}
      <div className="p-3 overflow-y-auto space-y-2.5 flex-1 max-h-[380px]">
        {filteredOps.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-400">
            Memuat daftar operasi dari backend registry...
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

                    <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
                      <span>Penanggung Jawab: <strong className="text-slate-600">{op.owner}</strong></span>
                      {op.has_kernel_preview && (
                        <span className="text-blue-600 font-medium">Kernel 2D Visualizer</span>
                      )}
                    </div>
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
                      className={`flex items-center gap-1 px-2 py-1 rounded text-xs font-medium transition-all ${
                        isReady
                          ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-xs'
                          : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                      }`}
                      title={
                        isReady
                          ? 'Tambahkan operasi ke Pipeline'
                          : 'Operasi ini belum dapat dijalankan (sedang dikerjakan oleh anggota kelompok)'
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
