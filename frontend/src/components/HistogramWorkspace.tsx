import React, { useState, useMemo } from 'react';
import type { HistogramData, ImageStats } from '../types';
import { BarChart3, Info } from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
} from 'recharts';

interface HistogramWorkspaceProps {
  originalHistogram: HistogramData | null;
  processedHistogram: HistogramData | null;
  activeStats: ImageStats | null;
  selectedOperationName?: string;
}

export const HistogramWorkspace: React.FC<HistogramWorkspaceProps> = ({
  originalHistogram,
  processedHistogram,
  activeStats,
  selectedOperationName,
}) => {
  const [selectedChannel, setSelectedChannel] = useState<'rgb' | 'gray' | 'red' | 'green' | 'blue'>('rgb');
  const [compareMode, setCompareMode] = useState<'processed' | 'original' | 'compare'>('compare');

  // Prepare chart dataset (256 bins)
  const chartData = useMemo(() => {
    const hist = processedHistogram || originalHistogram;
    if (!hist) return [];

    const orig = originalHistogram;
    const proc = processedHistogram;

    return hist.bins_range.map((bin) => ({
      bin,
      // Original
      orig_gray: orig?.grayscale?.[bin] ?? 0,
      orig_r: orig?.red?.[bin] ?? 0,
      orig_g: orig?.green?.[bin] ?? 0,
      orig_b: orig?.blue?.[bin] ?? 0,
      // Processed
      proc_gray: proc?.grayscale?.[bin] ?? (orig?.grayscale?.[bin] ?? 0),
      proc_r: proc?.red?.[bin] ?? (orig?.red?.[bin] ?? 0),
      proc_g: proc?.green?.[bin] ?? (orig?.green?.[bin] ?? 0),
      proc_b: proc?.blue?.[bin] ?? (orig?.blue?.[bin] ?? 0),
    }));
  }, [originalHistogram, processedHistogram]);

  const stats = activeStats || processedHistogram?.stats || originalHistogram?.stats;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs flex flex-col h-full overflow-hidden">
      {/* Header Bar */}
      <div className="px-4 py-3 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-blue-600" />
          <h2 className="text-sm font-semibold text-slate-900">
            Analisis Histogram & Statistik Citra
            {selectedOperationName && (
              <span className="text-xs font-normal text-blue-600 ml-2">
                (Tahap: {selectedOperationName})
              </span>
            )}
          </h2>
          <span className="text-[11px] px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-mono">
            256 Bin [0–255]
          </span>
        </div>

        {/* View Switchers */}
        <div className="flex items-center gap-2">
          {/* Comparison Mode */}
          <div className="flex items-center gap-0.5 bg-slate-100 p-0.5 rounded-lg text-xs font-medium text-slate-600">
            <button
              onClick={() => setCompareMode('compare')}
              className={`px-2 py-1 rounded-md transition-colors ${
                compareMode === 'compare' ? 'bg-white text-blue-700 shadow-2xs font-semibold' : 'hover:text-slate-900'
              }`}
            >
              Komparasi
            </button>
            <button
              onClick={() => setCompareMode('processed')}
              className={`px-2 py-1 rounded-md transition-colors ${
                compareMode === 'processed' ? 'bg-white text-blue-700 shadow-2xs font-semibold' : 'hover:text-slate-900'
              }`}
            >
              Hasil
            </button>
            <button
              onClick={() => setCompareMode('original')}
              className={`px-2 py-1 rounded-md transition-colors ${
                compareMode === 'original' ? 'bg-white text-blue-700 shadow-2xs font-semibold' : 'hover:text-slate-900'
              }`}
            >
              Asli
            </button>
          </div>

          {/* Channel Selectors */}
          <div className="flex items-center gap-0.5 bg-slate-100 p-0.5 rounded-lg text-xs font-medium">
            <button
              onClick={() => setSelectedChannel('rgb')}
              className={`px-2 py-1 rounded-md transition-colors ${
                selectedChannel === 'rgb' ? 'bg-white text-slate-900 shadow-2xs font-semibold' : 'text-slate-600'
              }`}
            >
              RGB
            </button>
            <button
              onClick={() => setSelectedChannel('gray')}
              className={`px-2 py-1 rounded-md transition-colors ${
                selectedChannel === 'gray' ? 'bg-white text-slate-900 shadow-2xs font-semibold' : 'text-slate-600'
              }`}
            >
              Abu-abu
            </button>
            <button
              onClick={() => setSelectedChannel('red')}
              className={`px-2 py-1 rounded-md transition-colors ${
                selectedChannel === 'red' ? 'bg-white text-rose-600 shadow-2xs font-semibold' : 'text-slate-600'
              }`}
            >
              R
            </button>
            <button
              onClick={() => setSelectedChannel('green')}
              className={`px-2 py-1 rounded-md transition-colors ${
                selectedChannel === 'green' ? 'bg-white text-emerald-600 shadow-2xs font-semibold' : 'text-slate-600'
              }`}
            >
              G
            </button>
            <button
              onClick={() => setSelectedChannel('blue')}
              className={`px-2 py-1 rounded-md transition-colors ${
                selectedChannel === 'blue' ? 'bg-white text-blue-600 shadow-2xs font-semibold' : 'text-slate-600'
              }`}
            >
              B
            </button>
          </div>
        </div>
      </div>

      {/* Statistical Summary Cards */}
      {stats && (
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 p-3 bg-slate-50/60 border-b border-slate-200">
          <div className="bg-white p-2 rounded-lg border border-slate-200 text-center">
            <span className="text-[10px] text-slate-400 block font-medium">Min Intensitas</span>
            <span className="text-sm font-bold text-slate-800 font-mono">{stats.min_intensity}</span>
          </div>

          <div className="bg-white p-2 rounded-lg border border-slate-200 text-center">
            <span className="text-[10px] text-slate-400 block font-medium">Maks Intensitas</span>
            <span className="text-sm font-bold text-slate-800 font-mono">{stats.max_intensity}</span>
          </div>

          <div className="bg-white p-2 rounded-lg border border-slate-200 text-center">
            <span className="text-[10px] text-slate-400 block font-medium">Rata-rata (Mean)</span>
            <span className="text-sm font-bold text-blue-600 font-mono">{stats.mean}</span>
          </div>

          <div className="bg-white p-2 rounded-lg border border-slate-200 text-center">
            <span className="text-[10px] text-slate-400 block font-medium">Standar Deviasi</span>
            <span className="text-sm font-bold text-slate-800 font-mono">{stats.std_dev}</span>
          </div>

          <div className="bg-white p-2 rounded-lg border border-slate-200 text-center col-span-2 sm:col-span-1">
            <span className="text-[10px] text-slate-400 block font-medium">Total Piksel</span>
            <span className="text-sm font-bold text-slate-800 font-mono">{stats.total_pixels.toLocaleString()}</span>
          </div>
        </div>
      )}

      {/* Main Chart Graphic Area */}
      <div className="p-4 flex-1 min-h-[220px]">
        {chartData.length === 0 ? (
          <div className="h-full flex items-center justify-center text-xs text-slate-400">
            Unggah citra untuk melihat distribusi 256-bin histogram aktual.
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <XAxis dataKey="bin" tick={{ fontSize: 10 }} interval={31} />
              <YAxis tick={{ fontSize: 10 }} />
              <Tooltip
                content={({ active, payload, label }) => {
                  if (active && payload && payload.length) {
                    return (
                      <div className="bg-slate-900/90 text-white p-2 rounded text-[11px] shadow">
                        <p className="font-bold border-b border-slate-700 pb-0.5">Bin Intensitas: {label}</p>
                        {payload.map((p) => (
                          <p key={p.name} style={{ color: p.color }}>
                            {p.name}: {Number(p.value).toLocaleString()} piksel
                          </p>
                        ))}
                      </div>
                    );
                  }
                  return null;
                }}
              />

              {/* Render Selected Channels */}
              {selectedChannel === 'rgb' && (
                <>
                  <Area
                    type="monotone"
                    dataKey={compareMode === 'original' ? 'orig_r' : 'proc_r'}
                    name="Red Channel"
                    stroke="#ef4444"
                    fill="#ef4444"
                    fillOpacity={0.2}
                  />
                  <Area
                    type="monotone"
                    dataKey={compareMode === 'original' ? 'orig_g' : 'proc_g'}
                    name="Green Channel"
                    stroke="#10b981"
                    fill="#10b981"
                    fillOpacity={0.2}
                  />
                  <Area
                    type="monotone"
                    dataKey={compareMode === 'original' ? 'orig_b' : 'proc_b'}
                    name="Blue Channel"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.2}
                  />
                </>
              )}

              {selectedChannel === 'gray' && (
                <>
                  {compareMode === 'compare' && (
                    <Area
                      type="monotone"
                      dataKey="orig_gray"
                      name="Asli (Grayscale)"
                      stroke="#94a3b8"
                      fill="#94a3b8"
                      fillOpacity={0.15}
                      strokeDasharray="3 3"
                    />
                  )}
                  <Area
                    type="monotone"
                    dataKey={compareMode === 'original' ? 'orig_gray' : 'proc_gray'}
                    name="Hasil (Grayscale)"
                    stroke="#334155"
                    fill="#334155"
                    fillOpacity={0.25}
                  />
                </>
              )}

              {selectedChannel === 'red' && (
                <Area
                  type="monotone"
                  dataKey={compareMode === 'original' ? 'orig_r' : 'proc_r'}
                  name="Saluran Merah (R)"
                  stroke="#ef4444"
                  fill="#ef4444"
                  fillOpacity={0.3}
                />
              )}

              {selectedChannel === 'green' && (
                <Area
                  type="monotone"
                  dataKey={compareMode === 'original' ? 'orig_g' : 'proc_g'}
                  name="Saluran Hijau (G)"
                  stroke="#10b981"
                  fill="#10b981"
                  fillOpacity={0.3}
                />
              )}

              {selectedChannel === 'blue' && (
                <Area
                  type="monotone"
                  dataKey={compareMode === 'original' ? 'orig_b' : 'proc_b'}
                  name="Saluran Biru (B)"
                  stroke="#2563eb"
                  fill="#2563eb"
                  fillOpacity={0.3}
                />
              )}
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Academic Explanatory Note Footer */}
      <div className="px-4 py-2 bg-slate-50 border-t border-slate-200 text-[11px] text-slate-500 flex items-start gap-2">
        <Info className="w-3.5 h-3.5 text-blue-600 shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <strong>Catatan Teori Akademik:</strong> Histogram hanya merepresentasikan frekuensi kemunculan intensitas piksel global secara non-spasial. Pada operasi <em>Pencerminan (Mirroring)</em>, histogram citra 100% identik karena letak spasial piksel bertukar tanpa mengubah nilai intensitasnya. Sebaliknya pada <em>Erosi</em> atau <em>Dilasi</em>, kurva histogram bergeser ke kiri atau kanan akibat seleksi nilai minimum atau maksimum lingkungan piksel.
        </p>
      </div>
    </div>
  );
};
