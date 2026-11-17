# Aplikasi Pengolahan Citra Digital (Tkinter GUI - 14 Fitur Manual, Slider Parameter & Realtime Kamera)

Aplikasi Desktop Pengolahan Citra Digital (*Digital Image Processing*) berbasis **Python**, **Tkinter**, dan **NumPy**.

> **Catatan Alur Pemrosesan**:
> - Ketika tombol fitur diklik, fitur tersebut **hanya dipilih/ditandai (tombol menyala biru)** dan **tidak langsung mengubah output**.
> - Output gambar olahan dan histogram baru akan muncul setelah pengguna menekan tombol **`▶ Process`**.

---

## 🚀 Fitur Lengkap Aplikasi

### 1. Panel Tombol Filter (14 Fitur Hitung Manual):
- **Kolom 1**: `Tresholding`, `Blur`, `Negative`, `Edge Detection`
- **Kolom 2**: `Equalization`, `Grayscale`, `Mirroring`, `Sepia`
- **Kolom 3**: `Sketch`, `Brightness`, `Sharpening`, `Emboss`
- **Kolom 4**: `Erosion`, `Dilation`

### 2. Panel Slider Parameter Interaktif:
- **Threshold**: Nilai ambang batas binerisasi (0 - 255)
- **Brightness**: Nilai bias kecerahan (-100 s/d +100)
- **Blur Radius**: Ukuran jangkauan Gaussian Blur (3 - 21)
- **Edge Thresh**: Ambang batas kontur tepi Sobel (20 - 200)

### 3. Kamera & Realtime Video:
- **`📷 Live Kamera`**: Streaming langsung dari webcam (otomatis flipped/natural). Klik fitur lalu tekan `▶ Process` untuk mengaktifkan filter pada video realtime.
- **`📸 Ambil Foto`**: Mengambil snapshot instan dari webcam.

---

## 🛠️ Alur Penggunaan

1. Buka aplikasi:
   ```bash
   python main.py
   ```
2. Buka gambar via menu **Open File** (atau nyalakan **📷 Live Kamera**).
3. Klik salah satu tombol fitur (misal: **Grayscale**, **Sketch**, atau **Blur**). Tombol yang Anda pilih akan **menyala biru**.
4. (Opsional) Sesuaikan nilai slider di panel **Kontrol Parameter**.
5. Klik tombol **`▶ Process`** di kanan bawah $\to$ **Hasil gambar dan histogram baru akan keluar**.
6. Simpan hasil melalui menu **Save File**.
