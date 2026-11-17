# Arsitektur Sistem — Laboratorium Pengolahan Citra Digital (LPCD)

Dokumen ini menjelaskan arsitektur teknis menyeluruh dari platform **Laboratorium Pengolahan Citra Digital (LPCD)**, standar format data internal, pola desain registrasi modular, alur kerja pipeline non-destruktif, serta mekanisme komputasi histogram dan statistik citra.

---

## 1. Prinsip Utama Arsitektur

Platform LPCD dibangun dengan 5 prinsip arsitektural inti:

1. **Komputasi Asli Python & OpenCV**: Seluruh algoritma pengolahan citra wajib dieksekusi di backend Python menggunakan OpenCV (`opencv-python-headless`) dan NumPy. Tidak diperkenankan melakukan manipulasi CSS filter atau simulasi semu di frontend.
2. **Modularitas Tanpa Efek Samping (Zero Engine Coupling)**: Setiap anggota kelompok bertanggung jawab atas fiturnya masing-masing (`orang_1`, `orang_2`, `orang_3`, `orang_4`). Menambah atau mengubah algoritma operasi tidak memerlukan modifikasi pada mesin inti (*Pipeline Engine* maupun *Image I/O Handler*).
3. **Standarisasi Ruang Warna Internal (RGB uint8)**: OpenCV secara *default* mendekode gambar ke urutan kanal BGR. Layer *Image I/O* LPCD bertindak sebagai gerbang terpusat yang menjamin seluruh gambar di memori backend selalu bertipe data `uint8` dan berformat **RGB** (atau 2D Grayscale).
4. **Eksekusi Pipeline Non-Destruktif**: Setiap tahap pemrosesan menghasilkan salinan (*copy*) citra independen, sehingga gambar masukan asli tidak termodifikasi, dan pengguna dapat menginspeksi hasil pada setiap tahapan *intermediate*.
5. **Transparansi Akademik**: Setiap algoritma mempublikasikan metadata matematis, cara kerja, visualisasi elemen penstruktur (kernel), serta penjelasan dinamis mengapa hasil citra dan histogram terbentuk sedemikian rupa.

---

## 2. Diagram Arsitektur Tingkat Tinggi

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                         │
│  - Drag & Drop Pipeline Builder (dnd-kit)                              │
│  - Dual View Image Workspace (Split Comparison Slider & Side-by-Side)  │
│  - Dynamic Parameter Inspector & 2D Kernel Visualizer                  │
│  - 256-Bin Interactive Histogram Chart (Recharts)                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ REST API (JSON / Multipart)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        BACKEND (FastAPI Core)                          │
│                                                                        │
│  ┌──────────────────────┐  ┌───────────────────┐  ┌────────────────┐  │
│  │   Image I/O Handler  │  │ Histogram Engine  │  │ Pipeline Engine│  │
│  │ (BGR ↔ RGB uint8)    │  │ (256-bin & Stats) │  │(Non-destructive│  │
│  └──────────┬───────────┘  └─────────▲─────────┘  └───────▲────────┘  │
│             │                        │                    │           │
│             ▼                        └─────────┬──────────┘           │
│  ┌─────────────────────────────────────────────┴──────────────────┐   │
│  │                     Operation Registry                         │   │
│  │  - Kontrak BaseImageOperation (Protocol)                       │   │
│  │  - Metadata, Skema Konfigurasi, Rumus KaTeX, Penjelasan        │   │
│  └───────▲─────────────────▲─────────────────▲────────────────▲───┘   │
│          │                 │                 │                │       │
│  ┌───────┴──────┐  ┌───────┴──────┐  ┌───────┴──────┐ ┌───────┴─────┐ │
│  │   Modul 1    │  │   Modul 2    │  │   Modul 3    │ │   Modul 4   │ │
│  │  (Orang 1)   │  │  (Orang 2)   │  │  (Orang 3)   │ │  (Orang 4)  │ │
│  │ Transformasi │  │   Filter &   │  │  Morfologi & │ │ Segmentasi, │ │
│  │    Warna     │  │  Efek Visual │  │   Geometri   │ │ Tepi, Hist  │ │
│  │ (In Progress)│  │ (In Progress)│  │ (SELESAI 100%)│ (InProgress) │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ └─────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Komponen Inti Backend

### A. Layer Image I/O (`app/core/image_io/handler.py`)
- **Fungsi Dekode**:
  Menerima input biner file atau string data URL Base64 (`data:image/png;base64,...`).
  Menggunakan `cv2.imdecode(..., cv2.IMREAD_UNCHANGED)`.
  Mengonversi BGR ke RGB menggunakan `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`.
- **Fungsi Enkode**:
  Menerima citra array RGB `uint8`. Mengonversi kembali ke BGR sebelum dipadatkan menggunakan `cv2.imencode('.png')` atau `cv2.imencode('.jpg')`.
- **Validasi Keamanan**:
  Membatasi ukuran citra maksimal 15 MB, memeriksa status *corrupt file*, serta memastikan integritas dimensi citra.

### B. Histogram Analysis Engine (`app/core/histogram/engine.py`)
Histogram dihitung secara aktual dari piksel citra:
- 256 bin intensitas $[0, 255]$:
  - Kanal Grayscale: Dihitung menggunakan `cv2.COLOR_RGB2GRAY` dan `cv2.calcHist`. Total penjumlahan frekuensi seluruh bin sama persis dengan $W \times H$.
  - Kanal Red: Indeks kanal 0 citra RGB.
  - Kanal Green: Indeks kanal 1 citra RGB.
  - Kanal Blue: Indeks kanal 2 citra RGB.
- Metrik Statistik:
  - $\text{Min} = \min(I)$
  - $\text{Max} = \max(I)$
  - $\text{Mean} (\mu) = \frac{1}{N} \sum I(x, y)$
  - $\text{Std Dev} (\sigma) = \sqrt{\frac{1}{N} \sum (I(x, y) - \mu)^2}$
  - $\text{Total Piksel} = W \times H$

### C. Operation Registry (`app/core/registry/`)
- Menerapkan kontrak standar `BaseImageOperation` yang mewajibkan atribut:
  - `id`: Pengenal unik *slug*.
  - `name`: Nama lengkap bahasa Indonesia.
  - `category`: Kategori dari 4 kategori praktikum.
  - `owner`: Anggota penanggung jawab (`Orang 1`, `Orang 2`, `Orang 3`, `Orang 4`).
  - `status`: `"ready"` atau `"in_development"`.
  - `default_config`: Dictionary parameter *default*.
  - `config_schema`: Daftar skema input dinamis (slider, dropdown select, number, switch).
  - `explanation`: Objek 8 poin akademik lengkap.
  - `process(image, config)`: Fungsi eksekusi OpenCV.

### D. Pipeline Engine (`app/core/engine/pipeline.py`)
Menerima citra awal dan daftar tahapan `steps`.
1. Membuat salinan citra `current_image = initial_image.copy()`.
2. Menghitung histogram awal.
3. Melakukan perulangan untuk setiap tahap:
   - Jika `enabled == False`, tahap dicatat sebagai dilewati (*skipped*).
   - Jika status operasi `"in_development"`, tahap dicatat aman tanpa menghentikan sistem.
   - Jika valid, jalankan `op.process(current_image, config)` dengan pengukuran waktu eksekusi presisi milidetik (`time.perf_counter()`).
   - Menyimpan *intermediate image preview*, histogram per tahap, statistik, dan matriks kernel 2D.
4. Mengembalikan respons komprehensif `PipelineExecuteResponse`.

---

## 4. Struktur Monorepo

```text
laboratorium-pengolahan-citra/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions: Pytest & Vite Build
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/              # Endpoint REST API (health, ops, images, pipeline, histogram)
│   │   ├── core/
│   │   │   ├── engine/          # Pipeline Engine
│   │   │   ├── histogram/       # Histogram & Stats Engine
│   │   │   ├── image_io/        # BGR ↔ RGB Decoder & Encoder
│   │   │   └── registry/        # Base Operation & Central Registry
│   │   ├── features/
│   │   │   ├── orang_1/         # Modul 1: Grayscale, Negative, Sepia, Brightness
│   │   │   ├── orang_2/         # Modul 2: Blur, Sharpening, Emboss, Sketch
│   │   │   ├── orang_3/         # Modul 3: Erosion, Dilation, Mirroring (SELESAI)
│   │   │   └── orang_4/         # Modul 4: Thresholding, Equalization, Edge Detection
│   │   ├── schemas/             # Pydantic Schemas
│   │   └── main.py              # FastAPI Application & Lifespan
│   ├── tests/                   # 31 Pytest Unit & Integration Tests
│   ├── requirements.txt         # Python Dependencies
│   └── .python-version          # Versi Python (3.13)
├── frontend/
│   ├── public/                  # Static assets & icons
│   ├── src/
│   │   ├── components/          # UI Components (Header, Workspace, Pipeline, Inspector, etc.)
│   │   ├── services/            # Axios API Client
│   │   ├── types/               # TypeScript Type Definitions
│   │   ├── utils/               # Sample canvas image generators
│   │   ├── App.tsx              # Main State Coordinator
│   │   └── main.tsx             # React DOM Mounting
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── docs/                        # Dokumentasi Sistem
│   ├── ARSITEKTUR.md
│   ├── PANDUAN_ANGGOTA.md
│   ├── PANDUAN_OPERASI.md
│   ├── PANDUAN_API.md
│   └── PANDUAN_DEPLOYMENT.md
├── .gitignore
├── CONTRIBUTING.md
└── README.md
```
