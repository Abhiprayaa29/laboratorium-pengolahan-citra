# Panduan Detail Operasi Citra Digital — LPCD

Dokumen ini memuat dokumentasi matematis, algoritma OpenCV, parameter, dan karakteristik operasional dari seluruh algoritma yang tersedia di platform **Laboratorium Pengolahan Citra Digital (LPCD)**.

---

## Modul 3 — Operasi Morfologi dan Geometri (Orang 3)

### 1. Erosi (Erosion)
- **ID Operasi**: `morphology_erosion`
- **Fungsi OpenCV**: `cv2.getStructuringElement()` dan `cv2.erode()`
- **Tujuan**: Mengikis atau menipiskan batas terluar dari objek foreground putih (bernilai tinggi) serta mengeliminasi derau putih berukuran kecil.
- **Rumus Matematis**:
  $$g(x,y) = (f \ominus B)(x,y) = \min_{(i,j) \in B} \{ f(x+i, y+j) \}$$
- **Parameter Konfigurasi**:
  1. `kernel_shape`:
     - `rect`: Matriks persegi panjang $k \times k$ (`cv2.MORPH_RECT`).
     - `ellipse`: Elemen penstruktur elips/lingkaran (`cv2.MORPH_ELLIPSE`).
     - `cross`: Salib berpusat di tengah (`cv2.MORPH_CROSS`).
  2. `kernel_size`: $3 \times 3$, $5 \times 5$, $7 \times 7$.
  3. `iterations`: $1, 2, 3, 5$.
  4. `mode`:
     - `rgb`: Erosi diterapkan independen pada saluran R, G, dan B (mempertahankan struktur warna).
     - `grayscale`: Citra dikonversi ke luminansi monokromatik sebelum dierosi.
- **Penanganan Pixel Batas (Border Handling)**:
  Secara eksplisit menggunakan parameter `borderType=cv2.BORDER_CONSTANT` dengan `borderValue=0`. Hal ini menjamin bahwa batas luar citra diasumsikan sebagai latar belakang gelap (0), mencegah objek putih di tepi gambar memuai secara tidak terkendali.
- **Karakteristik Histogram**:
  Frekuensi piksel bergeser ke arah intensitas rendah (kiri). Frekuensi piksel gelap meningkat karena seleksi nilai minimum lokal pada area ketetanggaan.

---

### 2. Dilasi (Dilation)
- **ID Operasi**: `morphology_dilation`
- **Fungsi OpenCV**: `cv2.getStructuringElement()` dan `cv2.dilate()`
- **Tujuan**: Memperbesar dan memperluas area foreground putih, menutup lubang kecil (pepper noise), serta menjembatani celah yang terputus.
- **Rumus Matematis**:
  $$g(x,y) = (f \oplus B)(x,y) = \max_{(i,j) \in B} \{ f(x+i, y+j) \}$$
- **Parameter Konfigurasi**:
  1. `kernel_shape`: `rect`, `ellipse`, `cross`.
  2. `kernel_size`: $3 \times 3$, $5 \times 5$, $7 \times 7$.
  3. `iterations`: $1, 2, 3, 5$.
  4. `mode`: `rgb` atau `grayscale`.
- **Penanganan Pixel Batas (Border Handling)**:
  Menggunakan `borderType=cv2.BORDER_CONSTANT` dengan `borderValue=0` untuk konsistensi konvensi biner latar belakang hitam.
- **Karakteristik Histogram**:
  Distribusi histogram bergeser ke arah intensitas tinggi (kanan). Jumlah piksel terang bertambah karena seleksi nilai maksimum lingkungan piksel.

---

### 3. Pencerminan (Mirroring)
- **ID Operasi**: `geometry_mirroring`
- **Fungsi OpenCV**: `cv2.flip(image, flipCode)`
- **Tujuan**: Mentransformasikan posisi spasial piksel citra secara simetris terhadap sumbu horizontal, vertikal, atau kedua sumbu secara simultan.
- **Rumus Pemetaan Koordinat**:
  - Horizontal (`flipCode = 1`):
    $$x' = W - 1 - x, \quad y' = y$$
  - Vertikal (`flipCode = 0`):
    $$x' = x, \quad y' = H - 1 - y$$
  - Kedua Sumbu (`flipCode = -1`):
    $$x' = W - 1 - x, \quad y' = H - 1 - y$$
- **Sifat Involusi ($M \circ M = I$)**:
  Pencerminan dua kali berturut-turut pada sumbu yang sama mengembalikan citra 100% identik tepat ke keadaan awal:
  $$x'' = W - 1 - (W - 1 - x) = x$$
- **Karakteristik Histogram**:
  Histogram citra **100% IDENTIK dan TIDAK BERUBAH SAMA SEKALI**. Hal ini menjadi bukti fundamental dalam pembelajaran pengolahan citra bahwa histogram hanya mencatat frekuensi kemunculan intensitas secara global dan tidak memuat informasi posisi spasial piksel.

---

## Modul 1, 2, dan 4 (Rencana Implementasi Lanjutan)

### Modul 1 (Orang 1) — Transformasi Warna & Intensitas
1. **Grayscale**: $Y = 0.299R + 0.587G + 0.114B$ via `cv2.cvtColor(RGB2GRAY)`.
2. **Negative**: Inversi intensitas $s = 255 - r$.
3. **Sepia**: Perkalian matriks pembobotan warna hangat $3 \times 3$.
4. **Brightness**: Pergeseran intensitas aditif $g(x,y) = \text{clip}(f(x,y) + \beta, 0, 255)$.

### Modul 2 (Orang 2) — Filter dan Efek Visual
1. **Gaussian Blur**: Konvolusi kernel 2D $G(x,y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$.
2. **Sharpening**: Penajaman detail tepi menggunakan kernel turunan kedua Laplacian.
3. **Emboss**: Deteksi gradien diagonal dengan penambahan konstanta offset abu-abu 128.
4. **Pencil Sketch**: Non-photorealistic sketch via grayscale, inversi, blur, dan color dodge division.

### Modul 4 (Orang 4) — Segmentasi, Histogram, Deteksi Tepi
1. **Thresholding**: Binerisasi ambang batas menggunakan `cv2.threshold()`.
2. **Equalization**: Perataan distribusi kumulatif CDF menggunakan `cv2.equalizeHist()`.
3. **Edge Detection**: Deteksi kontur batas objek menggunakan operator gradien Sobel ($G = \sqrt{G_x^2 + G_y^2}$).
