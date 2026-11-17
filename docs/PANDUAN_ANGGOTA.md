# Panduan Kolaborasi Anggota Kelompok

Selamat datang di repositori bersama **Laboratorium Pengolahan Citra Digital (LPCD)**. Proyek ini dikerjakan oleh 4 anggota kelompok praktikum universitas. Dokumen ini adalah panduan kerja agar setiap anggota dapat mengembangkan modul masing-masing secara mandiri dan aman.

---

## 1. Pembagian Tugas dan Modul

| Anggota | Modul | Kategori Operasi | Algoritma yang Dikelola | Status Saat Ini |
|---|---|---|---|---|
| **Orang 1** | Modul 1 | Transformasi Warna & Intensitas | Grayscale, Negative, Sepia, Brightness | *Dalam Pengembangan* |
| **Orang 2** | Modul 2 | Filter dan Efek Visual | Gaussian Blur, Sharpening, Emboss, Sketch | *Dalam Pengembangan* |
| **Orang 3** | Modul 3 | Operasi Morfologi & Geometri | **Erosion, Dilation, Mirroring** | **Selesai & Teruji 100%** |
| **Orang 4** | Modul 4 | Segmentasi, Histogram, Deteksi Tepi | Thresholding, Equalization, Sobel Edge Detection | *Dalam Pengembangan* |

---

## 2. Aturan Branch Git

Setiap anggota dilarang melakukan `commit` langsung ke branch `main`. Seluruh pekerjaan wajib menggunakan branch fitur masing-masing:

- Orang 1: `feature/orang-1-transformasi`
- Orang 2: `feature/orang-2-filter`
- Orang 3: `feature/orang-3-morfologi-geometri`
- Orang 4: `feature/orang-4-segmentasi`

### Alur Kerja Git Standar:
```bash
# 1. Pastikan branch main lokal Anda mutakhir
git checkout main
git pull origin main

# 2. Pindah ke branch fitur Anda (contoh untuk Orang 1)
git checkout feature/orang-1-transformasi
git merge main

# 3. Kembangkan kode Anda di folder fitur masing-masing
# 4. Jalankan pengujian Pytest sebelum commit
cd backend
pytest

# 5. Commit dan push ke branch fitur Anda
git add .
git commit -m "feat(orang-1): implementasi algoritma grayscale dan penyesuaian kecerahan"
git push origin feature/orang-1-transformasi

# 6. Buat Pull Request (PR) di GitHub ke branch 'main' untuk direview anggota lain
```

---

## 3. Langkah Menambahkan Operasi Baru

Setiap anggota **hanya perlu bekerja di foldernya masing-masing**:
- Orang 1: `backend/app/features/orang_1/`
- Orang 2: `backend/app/features/orang_2/`
- Orang 3: `backend/app/features/orang_3/`
- Orang 4: `backend/app/features/orang_4/`

Anda **TIDAK PERLU** memodifikasi `app/core/engine/pipeline.py` atau kode frontend React.

### Langkah-langkah:
1. Buka file operasi Anda di dalam folder fitur (misal `app/features/orang_1/operations.py`).
2. Ubah `status = OperationStatus.IN_DEVELOPMENT` menjadi:
   ```python
   status = OperationStatus.READY
   ```
3. Implementasikan fungsi `process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray`:
   - Citra masukan `image` dijamin selalu berupa array NumPy bertipe `uint8` dalam format **RGB** (atau 2D grayscale).
   - Gunakan fungsi OpenCV yang relevan (misal `cv2.cvtColor`, `cv2.filter2D`, `cv2.threshold`, dll).
   - Pastikan nilai piksel hasil tetap dalam rentang $[0, 255]$ bertipe `np.uint8`.
4. Perbarui penjelasan akademik pada objek `explanation`:
   - Pengertian, Tujuan, Cara Kerja, Rumus KaTeX, Pengaruh Gambar, Pengaruh Histogram, Mengapa seperti ini.
5. Jalankan unit test Pytest:
   ```bash
   cd backend
   pytest tests/
   ```
6. Buka antarmuka web, operasi Anda secara otomatis akan tampil dengan status **"Siap"** dan tombol **"Pilih"** langsung aktif tanpa perlu membuat komponen React baru!

---

## 4. Menjalankan Lingkungan Lokal

### Backend Python:
```bash
cd backend
# Aktifkan virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Jalankan server FastAPI
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Dokumentasi interaktif Swagger API tersedia di: `http://127.0.0.1:8000/docs`

### Frontend React:
```bash
cd frontend
npm install
npm run dev
```
Aplikasi web dapat dibuka di browser pada: `http://localhost:5173`
