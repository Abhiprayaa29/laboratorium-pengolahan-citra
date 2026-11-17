# Laboratorium Pengolahan Citra Digital (LPCD)
### Modular Academic Image Processing Platform | Python + OpenCV + FastAPI + React

[![CI Test & Build](https://github.com/Abhiprayaa29/laboratorium-pengolahan-citra/actions/workflows/ci.yml/badge.svg)](https://github.com/Abhiprayaa29/laboratorium-pengolahan-citra/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-Headless%204.10+-5C3EE8.svg?logo=opencv&logoColor=white)](https://opencv.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-v4-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License: Academic](https://img.shields.io/badge/License-Academic-blue.svg)](#lisensi)

**Laboratorium Pengolahan Citra Digital (LPCD)** adalah platform web akademik yang dirancang secara modular untuk praktikum universitas. Platform ini memungkinkan mahasiswa dan penguji menyusun rangkaian (*pipeline*) algoritma pengolahan citra digital berbasis **Python** dan **OpenCV** secara drag-and-drop, menginspeksi hasil tahapan *intermediate*, membandingkan gambar sebelum dan sesudah secara interaktif, menganalisis histogram 256-bin aktual, serta memahami teori dan rumus matematis di balik setiap operasi.

---

## 1. Fitur Utama Platform

1. **Pemrosesan Citra Asli OpenCV**: Seluruh algoritma berjalan di backend Python menggunakan OpenCV (`cv2`) dan NumPy murni. Tidak ada rekayasa tampilan semata atau filter CSS.
2. **Modular Operation Registry**: Desain terisolasi di mana 4 anggota kelompok praktikum dapat menambahkan modul masing-masing tanpa mengubah mesin pemrosesan utama (*Pipeline Engine*).
3. **Pipeline Builder Drag-and-Drop**: Penyusunan alur pemrosesan multi-tahap non-destruktif dengan dnd-kit. Mendukung penambahan, penghapusan, duplikasi, pengaktifan/penonaktifan, dan pengurutan ulang operasi.
4. **Interactive Before/After Comparison**: Bilah geser (*split slider*) dan mode perbandingan berdampingan (*side-by-side*) untuk melihat perbedaan spasial secara presisi.
5. **Analisis Histogram Aktual 256 Bin**: Perhitungan frekuensi piksel 256 bin untuk kanal Grayscale, Red, Green, Blue, serta statistik komprehensif (Min, Max, Mean, Standar Deviasi, Total Piksel).
6. **Visualisasi Elemen Penstruktur (Kernel 2D)**: Tampilan visual matriks ketetanggaan ($3\times 3, 5\times 5, 7\times 7$) untuk bentuk Rectangle, Ellipse, dan Cross pada operasi morfologi.
7. **Sistem Pembelajaran Akademik Interaktif**: Penjelasan mendalam bahasa Indonesia untuk setiap algoritma (Pengertian, Tujuan, Cara Kerja, Rumus KaTeX, Pengaruh Gambar, Pengaruh Histogram, dan *"Mengapa hasilnya seperti ini?"*).
8. **Preset Alur Kerja Siap Pakai**: Contoh alur kerja 1-klik untuk pembuktian konsep akademik (Opening, Closing, Involusi Pencerminan, Rotasi 180°).
9. **Ekspor Resolusi Penuh**: Unduh citra hasil akhir maupun intermediate dalam format biner PNG dan JPEG.

---

## 2. Pembagian Modul Kelompok

| Modul | Penanggung Jawab | Kategori Operasi | Daftar Operasi | Status Implementasi |
|---|---|---|---|---|
| **Modul 1** | **Orang 1** | Transformasi Warna & Intensitas | Grayscale, Negative, Sepia, Brightness | 🟡 *Dalam Pengembangan* |
| **Modul 2** | **Orang 2** | Filter dan Efek Visual | Blur (Gaussian), Sharpening, Emboss, Sketch | 🟡 *Dalam Pengembangan* |
| **Modul 3** | **Orang 3** | **Operasi Morfologi & Geometri** | **Erosion, Dilation, Mirroring** | 🟢 **Selesai & Teruji 100% (31 Tests Pass)** |
| **Modul 4** | **Orang 4** | Segmentasi, Histogram, Deteksi Tepi | Thresholding, Equalization, Sobel Edge Detection | 🟡 *Dalam Pengembangan* |

> **Catatan Akademik**: Operasi yang berstatus *Dalam Pengembangan* menampilkan informasi status secara transparan di antarmuka katalog operasi dan tidak dapat dijalankan hingga anggota yang bersangkutan mengimplementasikan algoritma OpenCV-nya.

---

## 3. Spesifikasi Teknologi (Tech Stack)

### Backend (Python 3.12 / 3.13)
- **FastAPI**: Kerangka kerja REST API berkinerja tinggi dengan validasi Pydantic otomatis.
- **opencv-python-headless**: Mesin pengolahan citra digital standar industri.
- **NumPy**: Manipulasi array multidimensi dan komputasi matriks piksel.
- **Pydantic v2**: Validasi skema parameter operasi dan pemodelan data respons.
- **Uvicorn**: Server ASGI berkemampuan asinkron.
- **Pytest & HTTPX**: Pengujian unit matematis dan integrasi API REST.

### Frontend (React + TypeScript)
- **React 19 & TypeScript**: Komponen antarmuka pengguna berbasis tipe statis yang aman.
- **Vite 8**: Build tool modern dan *Hot Module Replacement* (HMR) super cepat.
- **Tailwind CSS v4**: Desain minimalis elegan dengan aksen *Cobalt Blue* dan latar belakang bersih.
- **dnd-kit**: Drag-and-drop sortable list yang aksesibel dan mulus.
- **Recharts**: Grafik area interaktif untuk visualisasi sebaran histogram 256 bin.
- **Lucide React**: Ikon antarmuka yang modern dan konsisten.
- **Axios**: Klien HTTP untuk komunikasi dengan backend FastAPI.

---

## 4. Struktur Repositori (Monorepo)

```text
laboratorium-pengolahan-citra/
│
├── frontend/                        # Aplikasi Antarmuka React
│   ├── src/
│   │   ├── components/              # Header, Workspace, Pipeline, Inspector, dsb.
│   │   ├── services/api.ts          # Klien REST API Axios
│   │   ├── types/index.ts           # Definisi Interface TypeScript
│   │   ├── utils/sampleImages.ts    # Generator citra sampel praktikum
│   │   ├── App.tsx                  # Komponen Utama Studio LPCD
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── vercel.json                  # Konfigurasi deployment Vercel SPA
│
├── backend/                         # Mesin Komputasi Python & OpenCV
│   ├── app/
│   │   ├── api/v1/                  # Endpoint REST API (health, ops, images, pipeline, hist)
│   │   ├── core/
│   │   │   ├── engine/pipeline.py   # Mesin eksekusi alur multi-tahap
│   │   │   ├── histogram/engine.py  # Perhitungan histogram 256-bin aktual & statistik
│   │   │   ├── image_io/handler.py  # Konversi BGR ↔ RGB uint8 & validasi biner
│   │   │   └── registry/            # Registrasi terpusat & protokol BaseImageOperation
│   │   ├── features/
│   │   │   ├── orang_1/             # Modul 1 (Orang 1)
│   │   │   ├── orang_2/             # Modul 2 (Orang 2)
│   │   │   ├── orang_3/             # Modul 3 (Orang 3 - SELESAI)
│   │   │   └── orang_4/             # Modul 4 (Orang 4)
│   │   ├── schemas/                 # Skema Pydantic
│   │   └── main.py                  # Inisialisasi FastAPI & Middleware CORS
│   ├── tests/                       # 31 Pytest Unit & Integration Tests
│   ├── requirements.txt             # Dependensi Python
│   ├── Dockerfile                   # Kontainerisasi backend
│   └── render.yaml                  # Konfigurasi deployment hosting Python
│
├── docs/                            # Dokumentasi Lengkap
│   ├── ARSITEKTUR.md
│   ├── PANDUAN_ANGGOTA.md
│   ├── PANDUAN_OPERASI.md
│   ├── PANDUAN_API.md
│   └── PANDUAN_DEPLOYMENT.md
│
├── .github/workflows/ci.yml         # GitHub Actions CI
├── .gitignore
├── CONTRIBUTING.md
└── README.md
```

---

## 5. Panduan Instalasi dan Menjalankan Aplikasi

### Prasyarat Sistem
- **Python**: Versi 3.12 atau 3.13.
- **Node.js**: Versi 20 atau 24.
- **Git**

### A. Menjalankan Backend Python (FastAPI)
```bash
# 1. Masuk ke direktori backend
cd backend

# 2. Buat virtual environment
python -m venv .venv

# 3. Aktifkan virtual environment
# Pada Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Pada Linux / macOS:
source .venv/bin/activate

# 4. Instal dependensi pustaka
pip install --upgrade pip
pip install -r requirements.txt

# 5. Jalankan server backend Uvicorn
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Endpoint API Backend: `http://127.0.0.1:8000`
- Dokumentasi Interaktif Swagger UI: `http://127.0.0.1:8000/docs`
- Health Check: `http://127.0.0.1:8000/api/v1/health`

### B. Menjalankan Frontend React (Vite)
Buka terminal baru:
```bash
# 1. Masuk ke direktori frontend
cd frontend

# 2. Instal dependensi NPM
npm install

# 3. Jalankan server pengembangan Vite
npm run dev
```
Aplikasi web LPCD akan otomatis dapat diakses pada browser di: **`http://localhost:5173`**

---

## 6. Menjalankan Pengujian Kualitas (Testing & QA)

Seluruh logika matematika dan algoritma pengolahan citra Modul 3 telah diverifikasi secara ketat melalui 31 unit test Pytest:

```bash
cd backend
.\.venv\Scripts\python.exe -m pytest -v
```

Hasil Pengujian:
```text
tests/test_api_endpoints.py::test_health_endpoint PASSED
tests/test_api_endpoints.py::test_get_all_operations PASSED
tests/test_api_endpoints.py::test_get_operation_by_id PASSED
tests/test_api_endpoints.py::test_get_nonexistent_operation_404 PASSED
tests/test_api_endpoints.py::test_execute_single_operation PASSED
tests/test_api_endpoints.py::test_execute_in_development_rejected_or_handled PASSED
tests/test_api_endpoints.py::test_analyze_image_endpoint PASSED
tests/test_api_endpoints.py::test_pipeline_execution_endpoint PASSED
tests/test_api_endpoints.py::test_invalid_base64_returns_400 PASSED
tests/test_geometry_mirroring.py::test_mirroring_horizontal_flip PASSED
tests/test_geometry_mirroring.py::test_mirroring_vertical_flip PASSED
tests/test_geometry_mirroring.py::test_mirroring_both_axes_flip PASSED
tests/test_geometry_mirroring.py::test_mirroring_involution_identity PASSED
tests/test_geometry_mirroring.py::test_mirroring_preserves_histogram_identically PASSED
tests/test_histogram_engine.py::test_histogram_bins_count_and_range PASSED
tests/test_histogram_engine.py::test_histogram_total_pixel_sum_matches PASSED
tests/test_histogram_engine.py::test_histogram_pure_colors PASSED
tests/test_histogram_engine.py::test_image_stats_metrics PASSED
tests/test_morphology_dilation.py::test_dilation_expands_white_foreground PASSED
tests/test_morphology_dilation.py::test_dilation_kernel_size_impact PASSED
tests/test_morphology_dilation.py::test_dilation_kernel_shapes_differ PASSED
tests/test_morphology_dilation.py::test_dilation_iterations_impact PASSED
tests/test_morphology_erosion.py::test_erosion_shrinks_white_foreground PASSED
tests/test_morphology_erosion.py::test_erosion_kernel_size_impact PASSED
tests/test_morphology_erosion.py::test_erosion_kernel_shapes_differ PASSED
tests/test_morphology_erosion.py::test_erosion_iterations_impact PASSED
tests/test_morphology_erosion.py::test_erosion_grayscale_mode PASSED
tests/test_pipeline_engine.py::test_pipeline_sequential_execution PASSED
tests/test_pipeline_engine.py::test_pipeline_disabled_step_skipped PASSED
tests/test_pipeline_engine.py::test_pipeline_reordering_changes_result PASSED
tests/test_pipeline_engine.py::test_pipeline_handles_in_development_gracefully PASSED

======================== 31 passed in 0.78s ========================
```

---

## 7. Panduan Deployment

Rekomendasi arsitektur produksi:
1. **Frontend (Vercel)**:
   - Hubungkan repositori ke Vercel dengan direktori `frontend`.
   - Atur environment variable: `VITE_API_BASE_URL` mengarah ke URL backend Anda.
   - Konfigurasi `vercel.json` telah disediakan untuk penanganan routing SPA.
2. **Backend (Render / Railway / Docker)**:
   - Deploy backend ke platform berbasis container atau Python Web Service yang memiliki pustaka grafis sistem Linux (`libgl1`, `libglib2.0-0`).
   - File konfigurasi `backend/render.yaml` dan `backend/Dockerfile` telah disediakan.
   - Atur `ALLOWED_ORIGINS` untuk mengizinkan domain Vercel frontend.

Dokumentasi detail deployment dapat dibaca pada [PANDUAN_DEPLOYMENT.md](file:///D:/Projects/laboratorium-pengolahan-citra/docs/PANDUAN_DEPLOYMENT.md).

---

## 8. Lisensi & Hak Cipta

Proyek ini dikembangkan untuk keperluan praktikum akademik Pengolahan Citra Digital (Digital Image Processing) di lingkungan universitas. Bebas digunakan dan dikembangkan untuk tujuan pembelajaran dan riset akademik.
