# Panduan Deployment — Laboratorium Pengolahan Citra Digital (LPCD)

Dokumen ini menjelaskan strategi penerapan (*deployment*) produksi untuk frontend React dan backend Python FastAPI.

---

## 1. Analisis & Rekomendasi Arsitektur Hosting

Aplikasi pengolahan citra digital memiliki karakteristik komputasi intensif dan memerlukan dependensi biner C++ OpenCV (`opencv-python-headless`, NumPy).

### Evaluasi Runtime Vercel untuk Python OpenCV:
- **Kelebihan Vercel**: Sangat optimal untuk frontend Vite/React (Edge CDN global, build otomatis, SSL gratis).
- **Keterbatasan Vercel Serverless untuk OpenCV**:
  Vercel Serverless Function memiliki batas ukuran bundle tak terkompresi 250 MB dan batasan durasi eksekusi serta ketiadaan pustaka sistem Linux grafis tertentu pada lingkungan sandbox dasar. Paket OpenCV berukuran lebih dari 150 MB saat diekstrak, yang dapat memicu risiko kegagalan build atau *cold start latency*.

### Rekomendasi Strategi Produksi Terpisah (Dual-Target):
1. **Frontend**: Di-deploy ke **Vercel** sebagai Static Single-Page Application (SPA).
2. **Backend**: Di-deploy ke **Render**, **Railway**, atau **Koyeb** sebagai layanan Web Python yang stabil dengan akses CPU penuh dan dukungan pustaka OpenCV tanpa batas memori serverless.

Kedua layanan dihubungkan melalui REST API dengan environment variable `VITE_API_BASE_URL`.

---

## 2. Deployment Frontend ke Vercel

### Konfigurasi `frontend/vercel.json`:
```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Langkah Deployment Vercel:
1. Hubungkan repositori GitHub `laboratorium-pengolahan-citra` di dashboard Vercel.
2. Atur **Root Directory** ke: `frontend`.
3. Tambahkan **Environment Variable**:
   - `VITE_API_BASE_URL`: URL backend Python produksi Anda (misal `https://lpcd-backend.onrender.com`).
4. Klik **Deploy**.

---

## 3. Deployment Backend Python ke Render / Railway

### A. Konfigurasi `backend/render.yaml`:
```yaml
services:
  - type: web
    name: lpcd-backend
    env: python
    region: singapore
    plan: free
    rootDir: backend
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.13.2
      - key: ALLOWED_ORIGINS
        value: https://*.vercel.app,http://localhost:5173
```

### B. Opsi Dockerfile (`backend/Dockerfile`):
```dockerfile
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 4. Konfigurasi CORS & Keamanan

Pada backend (`app/main.py`), CORS dikonfigurasi melalui environment variable `ALLOWED_ORIGINS`:
```bash
ALLOWED_ORIGINS="https://laboratorium-pengolahan-citra.vercel.app,https://your-preview-domain.vercel.app"
```

Pastikan health check `GET /api/v1/health` mengembalikan status `200 OK` sebelum mengarahkan lalu lintas produksi.
