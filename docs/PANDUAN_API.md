# Panduan REST API — Laboratorium Pengolahan Citra Digital (LPCD)

Backend LPCD menyediakan antarmuka REST API berbasis **FastAPI** dengan dokumentasi interaktif Swagger UI di `/docs` dan ReDoc di `/redoc`.

Base URL lokal: `http://127.0.0.1:8000/api/v1`

---

## 1. Daftar Endpoint

| Metode | Path | Deskripsi |
|---|---|---|
| `GET` | `/health` | Memeriksa status kesehatan server dan ringkasan operasi |
| `GET` | `/operations` | Mengambil seluruh metadata dan skema konfigurasi operasi |
| `GET` | `/operations/{id}` | Mengambil detail metadata dan teori akademik satu operasi |
| `POST` | `/operations/{id}/execute` | Menjalankan satu operasi secara langsung pada citra |
| `POST` | `/images/analyze` | Mengunggah citra untuk mendapatkan dimensi, metadata, dan histogram awal |
| `POST` | `/images/download` | Mengunduh biner citra resolusi penuh (PNG / JPG) |
| `POST` | `/pipeline/execute` | Menjalankan pipeline multi-tahap non-destruktif |
| `POST` | `/histogram` | Menghitung histogram 256 bin mandiri |

---

## 2. Rincian Endpoint

### A. Health Check
`GET /api/v1/health`

**Contoh Respons (200 OK):**
```json
{
  "status": "ok",
  "application": "Laboratorium Pengolahan Citra Digital (LPCD) API",
  "version": "1.0.0",
  "timestamp": "2026-11-17T11:28:34.990734+00:00",
  "total_operations": 14,
  "ready_operations": 3,
  "in_development_operations": 11
}
```

---

### B. Analisis Citra Awal
`POST /api/v1/images/analyze`

Mendukung unggahan file biner melalui `multipart/form-data` (`file`) atau payload JSON (`image_base64`).

**Contoh Request JSON:**
```json
{
  "image_base64": "data:image/png;base64,iVBORw0KGgoAAA..."
}
```

**Contoh Respons (200 OK):**
```json
{
  "stats": {
    "min_intensity": 0,
    "max_intensity": 255,
    "mean": 128.45,
    "std_dev": 48.21,
    "total_pixels": 57600,
    "width": 240,
    "height": 240,
    "channels": 3,
    "is_grayscale": false
  },
  "histogram": {
    "bins_range": [0, 1, 2, ..., 255],
    "grayscale": [120, 55, ..., 80],
    "red": [100, 20, ..., 45],
    "green": [15, 30, ..., 12],
    "blue": [5, 12, ..., 90],
    "stats": { ... },
    "explanation": "Distribusi histogram awal citra asli."
  },
  "preview_base64": "data:image/png;base64,..."
}
```

---

### C. Eksekusi Pipeline Multi-Tahap
`POST /api/v1/pipeline/execute`

Menjalankan serangkaian operasi secara berurutan. Output tahap ke-$k$ otomatis menjadi input tahap ke-$(k+1)$.

**Contoh Request Body:**
```json
{
  "image_base64": "data:image/png;base64,...",
  "steps": [
    {
      "step_id": "step-1",
      "operation_id": "morphology_erosion",
      "enabled": true,
      "config": {
        "kernel_shape": "rect",
        "kernel_size": 3,
        "iterations": 1,
        "mode": "rgb"
      }
    },
    {
      "step_id": "step-2",
      "operation_id": "geometry_mirroring",
      "enabled": true,
      "config": {
        "axis": "horizontal"
      }
    }
  ],
  "include_intermediate_images": true,
  "include_histograms": true
}
```

**Contoh Respons (200 OK):**
```json
{
  "success": true,
  "total_steps": 2,
  "executed_steps": 2,
  "total_execution_time_ms": 1.45,
  "initial_stats": { ... },
  "initial_histogram": { ... },
  "stages": [
    {
      "step_id": "step-1",
      "operation_id": "morphology_erosion",
      "operation_name": "Erosi (Erosion)",
      "enabled": true,
      "execution_time_ms": 0.82,
      "image_base64": "data:image/png;base64,...",
      "histogram": { ... },
      "stats": { ... },
      "kernel_preview": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
      "note": "Berhasil dieksekusi"
    },
    {
      "step_id": "step-2",
      "operation_id": "geometry_mirroring",
      "operation_name": "Pencerminan (Mirroring)",
      "enabled": true,
      "execution_time_ms": 0.41,
      "image_base64": "data:image/png;base64,...",
      "histogram": { ... },
      "stats": { ... },
      "kernel_preview": null,
      "note": "Berhasil dieksekusi"
    }
  ],
  "final_image_base64": "data:image/png;base64,...",
  "final_stats": { ... },
  "final_histogram": { ... },
  "error": null
}
```

---

### D. Ekspor Citra Resolusi Penuh
`POST /api/v1/images/download`

Mengembalikan file unduhan biner langsung (*attachment*) dengan header `Content-Disposition`.

**Request Body:**
```json
{
  "image_base64": "data:image/png;base64,...",
  "format": "png",
  "filename": "lpcd_hasil_praktikum"
}
```
Respons bertipe `image/png` atau `image/jpeg`.
