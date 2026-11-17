import React, { useState, useRef, useEffect } from 'react';
import type { ImageStats, StepExecutionResult } from '../types';
import {
  Upload,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Download,
  RotateCcw,
  Sparkles,
  SplitSquareVertical,
  ImageIcon,
  Columns,
} from 'lucide-react';
import {
  generateSampleBinaryImage,
  generateSampleColorImage,
} from '../utils/sampleImages';

interface ImageWorkspaceProps {
  originalImageBase64: string | null;
  processedImageBase64: string | null;
  selectedStageResult: StepExecutionResult | null;
  imageStats: ImageStats | null;
  isProcessing: boolean;
  onImageSelected: (base64: string) => void;
  onDownloadFinal: (format: 'png' | 'jpg') => void;
  onResetOriginal: () => void;
}

export const ImageWorkspace: React.FC<ImageWorkspaceProps> = ({
  originalImageBase64,
  processedImageBase64,
  selectedStageResult,
  imageStats,
  isProcessing,
  onImageSelected,
  onDownloadFinal,
  onResetOriginal,
}) => {
  const [viewMode, setViewMode] = useState<'split' | 'sideBySide' | 'processedOnly'>('split');
  const [splitPos, setSplitPos] = useState<number>(50); // percentage 0-100
  const [zoomLevel, setZoomLevel] = useState<number>(1);
  const [isDraggingSlider, setIsDraggingSlider] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Active processed image: either selected stage intermediate result or final output
  const activeProcessed = selectedStageResult?.image_base64 || processedImageBase64;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        if (typeof reader.result === 'string') {
          onImageSelected(reader.result);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = () => {
        if (typeof reader.result === 'string') {
          onImageSelected(reader.result);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  // Slider dragging logic for Before/After split
  const handleMouseMove = (e: MouseEvent) => {
    if (!isDraggingSlider || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const offsetX = e.clientX - rect.left;
    const percent = Math.max(5, Math.min(95, (offsetX / rect.width) * 100));
    setSplitPos(percent);
  };

  const handleMouseUp = () => {
    setIsDraggingSlider(false);
  };

  useEffect(() => {
    if (isDraggingSlider) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
    }
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDraggingSlider]);

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs flex flex-col h-full overflow-hidden">
      {/* Top Workspace Toolbar */}
      <div className="px-4 py-2.5 border-b border-slate-200 bg-slate-50/50 flex flex-wrap items-center justify-between gap-2 text-xs">
        {/* Left: View Mode Toggles */}
        <div className="flex items-center gap-1 bg-white p-0.5 rounded-lg border border-slate-200 shadow-2xs">
          <button
            onClick={() => setViewMode('split')}
            className={`flex items-center gap-1 px-2.5 py-1 rounded-md font-medium transition-colors ${
              viewMode === 'split' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:text-slate-900'
            }`}
            title="Garis geser Before / After interaktif"
          >
            <SplitSquareVertical className="w-3.5 h-3.5" />
            <span>Slider Perbandingan</span>
          </button>

          <button
            onClick={() => setViewMode('sideBySide')}
            className={`flex items-center gap-1 px-2.5 py-1 rounded-md font-medium transition-colors ${
              viewMode === 'sideBySide' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:text-slate-900'
            }`}
            title="Tampilkan citra asli dan hasil secara berdampingan"
          >
            <Columns className="w-3.5 h-3.5" />
            <span>Berdampingan</span>
          </button>

          <button
            onClick={() => setViewMode('processedOnly')}
            className={`flex items-center gap-1 px-2.5 py-1 rounded-md font-medium transition-colors ${
              viewMode === 'processedOnly' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:text-slate-900'
            }`}
            title="Lihat hanya citra hasil pemrosesan"
          >
            <ImageIcon className="w-3.5 h-3.5" />
            <span>Citra Hasil</span>
          </button>
        </div>

        {/* Right: Zoom & Image Controls */}
        <div className="flex items-center gap-1.5">
          {/* Zoom Controls */}
          <div className="flex items-center gap-0.5 bg-white px-1 py-0.5 rounded-lg border border-slate-200 text-slate-600">
            <button
              onClick={() => setZoomLevel((z) => Math.max(0.5, Number((z - 0.25).toFixed(2))))}
              className="p-1 hover:text-slate-900 rounded"
              title="Zoom Out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <span className="text-[11px] font-mono px-1 min-w-[40px] text-center">
              {Math.round(zoomLevel * 100)}%
            </span>
            <button
              onClick={() => setZoomLevel((z) => Math.min(3.0, Number((z + 0.25).toFixed(2))))}
              className="p-1 hover:text-slate-900 rounded"
              title="Zoom In"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setZoomLevel(1)}
              className="p-1 hover:text-slate-900 rounded border-l border-slate-200 ml-0.5"
              title="Fit to Normal"
            >
              <Maximize2 className="w-3 h-3" />
            </button>
          </div>

          {/* Export Dropdown / Button */}
          {activeProcessed && (
            <div className="flex items-center gap-1">
              <button
                onClick={() => onDownloadFinal('png')}
                className="flex items-center gap-1 px-2.5 py-1 rounded-lg font-medium text-slate-700 bg-white hover:bg-slate-100 border border-slate-200 shadow-2xs transition-colors"
                title="Unduh Citra Hasil Resolusi Penuh PNG"
              >
                <Download className="w-3.5 h-3.5 text-blue-600" />
                <span>PNG</span>
              </button>
              <button
                onClick={() => onDownloadFinal('jpg')}
                className="flex items-center gap-1 px-2.5 py-1 rounded-lg font-medium text-slate-700 bg-white hover:bg-slate-100 border border-slate-200 shadow-2xs transition-colors"
                title="Unduh Citra Hasil Resolusi Penuh JPG"
              >
                <Download className="w-3.5 h-3.5 text-blue-600" />
                <span>JPG</span>
              </button>
            </div>
          )}

          {/* Reset Image */}
          {originalImageBase64 && (
            <button
              onClick={onResetOriginal}
              className="p-1 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
              title="Ganti gambar"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Main Display Area */}
      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
        className="flex-1 min-h-[380px] bg-slate-900/5 relative flex items-center justify-center p-4 overflow-hidden select-none"
      >
        {!originalImageBase64 ? (
          /* Empty Upload Dropzone */
          <div className="max-w-md w-full border-2 border-dashed border-slate-300 hover:border-blue-400 rounded-2xl p-8 bg-white/80 backdrop-blur-xs text-center transition-all shadow-sm">
            <div className="w-14 h-14 mx-auto rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mb-4 shadow-inner">
              <Upload className="w-7 h-7" />
            </div>
            <h3 className="font-semibold text-sm text-slate-900 mb-1">
              Unggah Citra Pengolahan
            </h3>
            <p className="text-xs text-slate-500 mb-4 max-w-xs mx-auto">
              Seret dan lepaskan file citra di sini, atau pilih file dari komputer Anda (PNG, JPG, JPEG, WEBP).
            </p>

            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="image/png, image/jpeg, image/webp"
              className="hidden"
            />

            <button
              onClick={() => fileInputRef.current?.click()}
              className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-xs transition-all active:scale-98"
            >
              Pilih Citra dari Komputer
            </button>

            {/* Quick Sample Buttons */}
            <div className="mt-6 pt-5 border-t border-slate-200">
              <span className="text-[11px] text-slate-400 block mb-2">
                Atau gunakan citra contoh praktikum:
              </span>
              <div className="flex items-center justify-center gap-2">
                <button
                  onClick={() => onImageSelected(generateSampleBinaryImage())}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-medium transition-colors"
                >
                  <Sparkles className="w-3 h-3 text-amber-500" />
                  <span>Citra Biner Morfologi (LPCD)</span>
                </button>
                <button
                  onClick={() => onImageSelected(generateSampleColorImage())}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-medium transition-colors"
                >
                  <Sparkles className="w-3 h-3 text-blue-500" />
                  <span>Citra Warna RGB</span>
                </button>
              </div>
            </div>
          </div>
        ) : (
          /* Active Image Viewers */
          <div
            ref={containerRef}
            className="relative w-full h-full flex items-center justify-center overflow-hidden"
          >
            {/* View Mode: Split Comparison Slider */}
            {viewMode === 'split' && (
              <div
                className="relative max-w-full max-h-full overflow-hidden shadow-md rounded-lg border border-slate-200 bg-white"
                style={{
                  transform: `scale(${zoomLevel})`,
                  transition: isDraggingSlider ? 'none' : 'transform 0.15s ease',
                }}
              >
                {/* Processed Image (Background Full) */}
                <img
                  src={activeProcessed || originalImageBase64}
                  alt="Processed Stage"
                  className="max-h-[380px] w-auto object-contain block pointer-events-none"
                />

                {/* Original Image (Clipped Left Side) */}
                <div
                  className="absolute inset-0 overflow-hidden"
                  style={{ width: `${splitPos}%` }}
                >
                  <img
                    src={originalImageBase64}
                    alt="Original Image"
                    className="max-h-[380px] w-auto object-contain block pointer-events-none max-w-none"
                  />
                  <div className="absolute top-2 left-2 bg-slate-900/80 text-white text-[10px] font-semibold px-2 py-0.5 rounded shadow">
                    SEBELUM (ASLI)
                  </div>
                </div>

                <div className="absolute top-2 right-2 bg-blue-700/85 text-white text-[10px] font-semibold px-2 py-0.5 rounded shadow">
                  SESUDAH ({selectedStageResult ? selectedStageResult.operation_name : 'HASIL'})
                </div>

                {/* Split Handle Divider Line */}
                <div
                  className="absolute top-0 bottom-0 w-0.5 bg-white cursor-ew-resize flex items-center justify-center shadow-lg"
                  style={{ left: `${splitPos}%` }}
                  onMouseDown={(e) => {
                    e.preventDefault();
                    setIsDraggingSlider(true);
                  }}
                >
                  <div className="w-6 h-6 rounded-full bg-white shadow-md border border-slate-300 flex items-center justify-center text-slate-600 text-[10px] font-bold">
                    ↔
                  </div>
                </div>
              </div>
            )}

            {/* View Mode: Side by Side */}
            {viewMode === 'sideBySide' && (
              <div
                className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-full max-h-full overflow-auto p-2"
                style={{
                  transform: `scale(${zoomLevel})`,
                  transition: 'transform 0.15s ease',
                }}
              >
                <div className="flex flex-col items-center">
                  <span className="text-[11px] font-semibold text-slate-500 mb-1">
                    Citra Asli
                  </span>
                  <div className="rounded-lg border border-slate-200 overflow-hidden shadow-xs bg-white">
                    <img
                      src={originalImageBase64}
                      alt="Original"
                      className="max-h-[320px] w-auto object-contain"
                    />
                  </div>
                </div>

                <div className="flex flex-col items-center">
                  <span className="text-[11px] font-semibold text-blue-600 mb-1">
                    {selectedStageResult
                      ? `Tahap: ${selectedStageResult.operation_name}`
                      : 'Citra Hasil Pengolahan'}
                  </span>
                  <div className="rounded-lg border border-slate-200 overflow-hidden shadow-xs bg-white">
                    <img
                      src={activeProcessed || originalImageBase64}
                      alt="Processed"
                      className="max-h-[320px] w-auto object-contain"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* View Mode: Processed Only */}
            {viewMode === 'processedOnly' && (
              <div
                className="max-w-full max-h-full overflow-hidden shadow-md rounded-lg border border-slate-200 bg-white"
                style={{
                  transform: `scale(${zoomLevel})`,
                  transition: 'transform 0.15s ease',
                }}
              >
                <img
                  src={activeProcessed || originalImageBase64}
                  alt="Processed Full"
                  className="max-h-[380px] w-auto object-contain block"
                />
              </div>
            )}

            {/* Processing Spinner Overlay */}
            {isProcessing && (
              <div className="absolute inset-0 bg-slate-900/30 backdrop-blur-xs flex items-center justify-center z-10">
                <div className="bg-white px-4 py-3 rounded-xl shadow-lg border border-slate-200 flex items-center gap-3">
                  <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                  <span className="text-xs font-semibold text-slate-800">
                    Memproses Algoritma OpenCV...
                  </span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Bottom Metadata Bar */}
      {imageStats && (
        <div className="px-4 py-2 border-t border-slate-200 bg-white flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-500">
          <div className="flex items-center gap-3">
            <span>
              Resolusi: <strong className="text-slate-800">{imageStats.width} × {imageStats.height}</strong> px
            </span>
            <span>
              Total Piksel: <strong className="text-slate-800">{imageStats.total_pixels.toLocaleString()}</strong>
            </span>
            <span>
              Kanal: <strong className="text-slate-800">{imageStats.is_grayscale ? 'Grayscale (1 Kanal)' : `${imageStats.channels} Saluran (RGB)`}</strong>
            </span>
          </div>

          <div className="flex items-center gap-2">
            {selectedStageResult && (
              <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded border border-blue-200 font-medium">
                Tahap Aktif: {selectedStageResult.operation_name} ({selectedStageResult.execution_time_ms} ms)
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
