import React from 'react';
import {
  X,
  FlaskConical,
  Layers,
  Code2,
  CheckCircle2,
  Clock,
} from 'lucide-react';

interface AboutModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AboutModal: React.FC<AboutModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl border border-slate-200 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/70">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center shadow-xs">
              <FlaskConical className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">Tentang Laboratorium LPCD</h2>
              <p className="text-xs text-slate-500">
                Laboratorium Pengolahan Citra Digital — Platform Akademik Terpadu
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

        {/* Content */}
        <div className="p-6 overflow-y-auto space-y-5 text-xs text-slate-600 leading-relaxed">
          {/* Deskripsi */}
          <div>
            <h3 className="font-bold text-slate-900 text-xs mb-1">Tujuan & Filosofi Platform</h3>
            <p>
              <strong>Laboratorium Pengolahan Citra Digital (LPCD)</strong> adalah platform web akademik yang dirancang secara modular untuk memfasilitasi praktikum dan riset pengolahan citra digital di perguruan tinggi. Seluruh algoritma pengolahan citra dijalankan secara murni pada backend <strong>Python 3.13 dan OpenCV (`opencv-python-headless`)</strong>, menjamin hasil komputasi matematis yang akurat tanpa manipulasi tampilan semata.
            </p>
          </div>

          {/* Cakupan Bidang Ilmu */}
          <div>
            <h3 className="font-bold text-slate-900 text-xs mb-2 flex items-center gap-1.5 text-blue-700">
              <Layers className="w-4 h-4" />
              Cakupan Kategori Pengolahan Citra
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {/* Morfologi & Geometri (Selesai) */}
              <div className="p-3 rounded-lg border border-emerald-200 bg-emerald-50/40">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-slate-900">Morfologi & Transformasi Geometri</span>
                  <span className="text-[10px] font-semibold text-emerald-700 flex items-center gap-0.5">
                    <CheckCircle2 className="w-3 h-3" />
                    Siap Digunakan
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 mb-1">Manipulasi bentuk objek & koordinat spasial</p>
                <ul className="text-[10px] text-slate-700 list-disc list-inside space-y-0.5">
                  <li>Erosi (Erosion) — rect, ellipse, cross</li>
                  <li>Dilasi (Dilation) — rect, ellipse, cross</li>
                  <li>Pencerminan (Mirroring) — horiz, vert, both</li>
                </ul>
              </div>

              {/* Transformasi Warna */}
              <div className="p-3 rounded-lg border border-slate-200 bg-slate-50/60">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-slate-900">Transformasi Warna & Intensitas</span>
                  <span className="text-[10px] font-medium text-amber-700 flex items-center gap-0.5">
                    <Clock className="w-3 h-3" />
                    Dalam Pengembangan
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 mb-1">Manipulasi kanal dan spektrum warna</p>
                <p className="text-[10px] text-slate-400">Grayscale, Negative, Sepia, Brightness</p>
              </div>

              {/* Filter Spasial */}
              <div className="p-3 rounded-lg border border-slate-200 bg-slate-50/60">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-slate-900">Penyaringan Spasial & Efek Visual</span>
                  <span className="text-[10px] font-medium text-amber-700 flex items-center gap-0.5">
                    <Clock className="w-3 h-3" />
                    Dalam Pengembangan
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 mb-1">Konvolusi kernel frekuensi spasial</p>
                <p className="text-[10px] text-slate-400">Gaussian Blur, Sharpening, Emboss, Sketch</p>
              </div>

              {/* Segmentasi & Tepi */}
              <div className="p-3 rounded-lg border border-slate-200 bg-slate-50/60">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-slate-900">Segmentasi, Histogram & Deteksi Tepi</span>
                  <span className="text-[10px] font-medium text-amber-700 flex items-center gap-0.5">
                    <Clock className="w-3 h-3" />
                    Dalam Pengembangan
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 mb-1">Pemisahan objek & batas kontur</p>
                <p className="text-[10px] text-slate-400">Thresholding, Equalization, Edge Detection</p>
              </div>
            </div>
          </div>

          {/* Arsitektur Teknologi */}
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-1">
            <h4 className="font-bold text-slate-800 text-xs flex items-center gap-1.5">
              <Code2 className="w-3.5 h-3.5 text-blue-600" />
              Spesifikasi Teknologi
            </h4>
            <div className="grid grid-cols-2 gap-2 text-[11px]">
              <div>
                <strong>Backend:</strong> Python 3.13, FastAPI, OpenCV, NumPy, Pydantic, Pytest.
              </div>
              <div>
                <strong>Frontend:</strong> React 19, TypeScript, Vite, Tailwind CSS, dnd-kit, Recharts.
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-between">
          <span className="text-[11px] text-slate-400">Lisensi Akademik Bebas • Laboratorium Pengolahan Citra Digital</span>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-semibold"
          >
            Tutup
          </button>
        </div>
      </div>
    </div>
  );
};
