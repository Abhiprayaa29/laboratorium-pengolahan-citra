import React from 'react';
import {
  FlaskConical,
  BookOpen,
  Sparkles,
  Info,
  Server,
} from 'lucide-react';

interface HeaderProps {
  backendConnected: boolean | null;
  onOpenPresets: () => void;
  onOpenTheory: () => void;
  onOpenAbout: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  backendConnected,
  onOpenPresets,
  onOpenTheory,
  onOpenAbout,
}) => {
  return (
    <header className="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo and Titles */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-700 to-blue-500 text-white flex items-center justify-center shadow-md shadow-blue-500/20">
            <FlaskConical className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg text-slate-900 tracking-tight">LPCD</span>
              <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-blue-100 text-blue-800 border border-blue-200">
                v1.0.0
              </span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">
              Laboratorium Pengolahan Citra Digital — Platform Kolaboratif Akademik
            </p>
          </div>
        </div>

        {/* Status and Action Buttons */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Backend Health Pill */}
          <div
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${
              backendConnected === true
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                : backendConnected === false
                ? 'bg-rose-50 text-rose-700 border-rose-200'
                : 'bg-slate-50 text-slate-600 border-slate-200'
            }`}
            title={
              backendConnected === true
                ? 'Terhubung dengan Python FastAPI Backend (OpenCV)'
                : 'Tidak dapat terhubung ke Backend (Periksa server FastAPI)'
            }
          >
            <span
              className={`w-2 h-2 rounded-full ${
                backendConnected === true
                  ? 'bg-emerald-500 animate-pulse'
                  : backendConnected === false
                  ? 'bg-rose-500'
                  : 'bg-slate-400'
              }`}
            />
            <Server className="w-3.5 h-3.5 inline" />
            <span className="hidden md:inline">
              {backendConnected === true
                ? 'Backend Python Terhubung'
                : backendConnected === false
                ? 'Backend Terputus'
                : 'Memeriksa Backend...'}
            </span>
          </div>

          {/* Preset Workflows Button */}
          <button
            onClick={onOpenPresets}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg text-blue-700 bg-blue-50 hover:bg-blue-100 border border-blue-200 transition-colors"
            title="Muat alur kerja rekomendasi praktikum"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Preset Workflow</span>
          </button>

          {/* Theory / Documentation Button */}
          <button
            onClick={onOpenTheory}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 transition-colors"
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Teori & Rumus</span>
          </button>

          {/* About / Info Button */}
          <button
            onClick={onOpenAbout}
            className="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition-colors"
            title="Informasi Kelompok dan Arsitektur"
          >
            <Info className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
