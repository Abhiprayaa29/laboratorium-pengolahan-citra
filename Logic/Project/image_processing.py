"""
Modul Logika Pengolahan Citra Digital (Digital Image Processing)
100% DIHITUNG MANUAL SECARA MATEMATIS TANPA MENGGUNAKAN LIBRARY CV2.

Seluruh operasi (Thresholding, Equalization, Sketch, Blur, Grayscale,
Brightness, Negative, Mirroring, Sharpening, Edge Detection, Sepia,
Emboss, Morfologi Erosi & Dilatasi, dan Histogram) dihitung manual
menggunakan operasi matematika array dan formula standar pengolahan citra.
"""

import numpy as np

# ==============================================================================
# FUNGSI DASAR: OPERASI KONVOLUSI MATRIKS 2D (SPATIAL FILTERING MANUAL)
# ==============================================================================
def manual_convolve2d(channel: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    Melakukan operasi konvolusi 2D secara manual pada 1 kanal citra dengan matriks kernel spasial.
    Menggunakan teknik replicate edge padding agar dimensi citra tidak menyusut.
    Rumus: output(y, x) = sum(padded(y+i, x+j) * kernel(i, j))
    """
    kh, kw = kernel.shape
    pad_y = kh // 2
    pad_x = kw // 2
    
    padded = np.pad(channel.astype(np.float32), ((pad_y, pad_y), (pad_x, pad_x)), mode='edge')
    h, w = channel.shape
    output = np.zeros((h, w), dtype=np.float32)
    
    for i in range(kh):
        for j in range(kw):
            output += padded[i:i + h, j:j + w] * kernel[i, j]
            
    return output

def manual_separable_convolve2d(channel: np.ndarray, k1d: np.ndarray) -> np.ndarray:
    """
    Konvolusi spasial terpisah manual (1D Horizontal kemudian 1D Vertikal).
    Metode matematis cepat O(K) daripada O(K^2) untuk kernel Gaussian/Box berukuran besar.
    """
    k_len = len(k1d)
    pad = k_len // 2
    h, w = channel.shape

    # 1. Konvolusi pada arah Horizontal
    padded_h = np.pad(channel.astype(np.float32), ((0, 0), (pad, pad)), mode='edge')
    temp = np.zeros((h, w), dtype=np.float32)
    for j in range(k_len):
        temp += padded_h[:, j:j + w] * k1d[j]

    # 2. Konvolusi pada arah Vertikal
    padded_v = np.pad(temp, ((pad, pad), (0, 0)), mode='edge')
    output = np.zeros((h, w), dtype=np.float32)
    for i in range(k_len):
        output += padded_v[i:i + h, :] * k1d[i]

    return output

# ==============================================================================
# 1. GRAYSCALE (DERAJAT KEABUAN MANUAL)
# ==============================================================================
def process_grayscale(img_rgb: np.ndarray) -> np.ndarray:
    """
    Konversi citra warna RGB ke Grayscale secara manual.
    Rumus standar luminansi manusia (ITU-R BT.601):
    Y = 0.299*R + 0.587*G + 0.114*B
    """
    r = img_rgb[:, :, 0].astype(np.float32)
    g = img_rgb[:, :, 1].astype(np.float32)
    b = img_rgb[:, :, 2].astype(np.float32)
    
    gray = 0.299 * r + 0.587 * g + 0.114 * b
    return np.clip(gray, 0, 255).astype(np.uint8)

# ==============================================================================
# 2. TRESHOLDING (SEGMENTASI BINER AMBANG BATAS MANUAL)
# ==============================================================================
def process_thresholding(img_rgb: np.ndarray, thresh_val: int = 127) -> np.ndarray:
    """
    Segmentasi biner (hitam-putih) secara manual:
    Piksel >= thresh_val -> 255 (putih)
    Piksel < thresh_val  -> 0 (hitam)
    """
    gray = process_grayscale(img_rgb)
    h, w = gray.shape
    thresh = np.zeros((h, w), dtype=np.uint8)
    thresh[gray >= thresh_val] = 255
    return thresh

# ==============================================================================
# 3. EQUALIZATION (PEMERATAAN HISTOGRAM MANUAL DENGAN CDF)
# ==============================================================================
def process_equalization(img_rgb: np.ndarray) -> np.ndarray:
    """
    Pemerataan Histogram (Histogram Equalization) manual:
    1. Hitung frekuensi kemunculan intensitas piksel (Histogram 0..255).
    2. Hitung Cumulative Distribution Function (CDF).
    3. Normalisasi CDF ke skala [0, 255].
    4. Petakan intensitas piksel lama ke nilai baru menggunakan Look-Up Table (LUT).
    """
    gray = process_grayscale(img_rgb)
    h, w = gray.shape
    total_pixels = h * w

    hist = np.bincount(gray.flatten(), minlength=256)
    cdf = hist.cumsum()
    cdf_masked = np.ma.masked_equal(cdf, 0)
    cdf_min = cdf_masked.min()
    
    cdf_normalized = ((cdf_masked - cdf_min) * 255.0) / (total_pixels - cdf_min)
    lut = np.ma.filled(cdf_normalized, 0).astype(np.uint8)

    equalized = lut[gray]
    return equalized

# ==============================================================================
# 4. SKETCH (EFEK SKETSA PENSIL ARTISTIK MANUAL)
# ==============================================================================
def process_sketch(img_rgb: np.ndarray) -> np.ndarray:
    """
    Efek Sketsa Pensil manual:
    1. Konversi ke Grayscale: I_gray
    2. Inversi citra negatif: I_inv = 255 - I_gray
    3. Gaussian Blur manual pada I_inv
    4. Color Dodge Blending manual: (I_gray * 255) / (255 - I_blur + epsilon)
    """
    gray = process_grayscale(img_rgb).astype(np.float32)
    inv = 255.0 - gray

    # Kernel Gaussian 1D radius 5 untuk sketsa
    radius = 5
    x = np.arange(-radius, radius + 1)
    k1d = np.exp(-x**2 / (2.0 * 2.5**2))
    k1d /= np.sum(k1d)

    blurred_inv = manual_separable_convolve2d(inv, k1d)

    denom = 255.0 - blurred_inv
    denom[denom == 0] = 1e-5
    sketch = (gray * 255.0) / denom

    return np.clip(sketch, 0, 255).astype(np.uint8)

# ==============================================================================
# 5. BLUR (GAUSSIAN BLUR KUAT & JELAS TERLIHAT SECARA MANUAL)
# ==============================================================================
def process_blur(img_rgb: np.ndarray, radius: int = 7) -> np.ndarray:
    """
    Filter Gaussian Blur berkekuatan tinggi (radius parameter dinamis) secara manual.
    Menghasilkan efek blur yang terlihat jelas dan lembut tanpa lag/lambat.
    """
    sigma = max(1.0, radius / 2.0)
    x = np.arange(-radius, radius + 1)
    k1d = np.exp(-x**2 / (2.0 * sigma**2))
    k1d /= np.sum(k1d)

    if len(img_rgb.shape) == 2:
        return np.clip(manual_separable_convolve2d(img_rgb, k1d), 0, 255).astype(np.uint8)

    h, w, c = img_rgb.shape
    blurred = np.zeros((h, w, c), dtype=np.uint8)
    for ch in range(c):
        conv = manual_separable_convolve2d(img_rgb[:, :, ch], k1d)
        blurred[:, :, ch] = np.clip(conv, 0, 255).astype(np.uint8)

    return blurred

# ==============================================================================
# 6. BRIGHTNESS (PENGATURAN KECERAHAN MANUAL)
# ==============================================================================
def process_brightness(img_rgb: np.ndarray, beta: int = 50) -> np.ndarray:
    """
    Pengaturan kecerahan manual:
    Piksel_baru = clip(Piksel_lama + beta, 0, 255)
    """
    bright = img_rgb.astype(np.int32) + beta
    return np.clip(bright, 0, 255).astype(np.uint8)

# ==============================================================================
# 7. NEGATIVE (INVERSI CITRA MANUAL)
# ==============================================================================
def process_negative(img_rgb: np.ndarray) -> np.ndarray:
    """
    Citra negatif (klise) manual:
    Piksel_baru = 255 - Piksel_lama
    """
    return (255 - img_rgb).astype(np.uint8)

# ==============================================================================
# 8. MIRRORING (PENCERMINAN HORIZONTAL MANUAL)
# ==============================================================================
def process_mirroring(img_rgb: np.ndarray) -> np.ndarray:
    """
    Pencerminan horizontal manual:
    Membalik urutan kolom citra dari kanan ke kiri (x' = Width - 1 - x).
    """
    return img_rgb[:, ::-1].copy()

# ==============================================================================
# 9. SHARPENING (PENAJAMAN CITRA MANUAL DENGAN KERNEL LAPLACIAN)
# ==============================================================================
def process_sharpening(img_rgb: np.ndarray) -> np.ndarray:
    """
    Penajaman citra manual menggunakan konvolusi kernel High-pass Laplacian 3x3:
    [ 0, -1,  0]
    [-1,  5, -1]
    [ 0, -1,  0]
    """
    kernel_sharpening = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0]
    ], dtype=np.float32)

    if len(img_rgb.shape) == 2:
        return np.clip(manual_convolve2d(img_rgb, kernel_sharpening), 0, 255).astype(np.uint8)

    h, w, c = img_rgb.shape
    sharpened = np.zeros((h, w, c), dtype=np.uint8)
    for ch in range(c):
        conv = manual_convolve2d(img_rgb[:, :, ch], kernel_sharpening)
        sharpened[:, :, ch] = np.clip(conv, 0, 255).astype(np.uint8)

    return sharpened

# ==============================================================================
# 10. EDGE DETECTION (DETEKSI TEPI MANUAL OPERATOR SOBEL)
# ==============================================================================
def process_edge_detection(img_rgb: np.ndarray, thresh: int = 100) -> np.ndarray:
    """
    Deteksi Tepi manual menggunakan Operator Gradien Sobel:
    Gx: Kernel Sobel Horizontal
    Gy: Kernel Sobel Vertikal
    Magnitudo G = sqrt(Gx^2 + Gy^2)
    Binerisasi tepi berdasarkan nilai ambang thresh.
    """
    gray = process_grayscale(img_rgb)

    sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32)

    sobel_y = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ], dtype=np.float32)

    gx = manual_convolve2d(gray, sobel_x)
    gy = manual_convolve2d(gray, sobel_y)

    magnitude = np.sqrt(gx**2 + gy**2)

    edges = np.zeros_like(gray, dtype=np.uint8)
    edges[magnitude >= thresh] = 255

    return edges

# ==============================================================================
# FITUR BARU: 11. SEPIA TONE (EFEK KLASIK VINTAGE MANUAL)
# ==============================================================================
def process_sepia(img_rgb: np.ndarray) -> np.ndarray:
    """
    Efek warna Sepia Vintage secara manual menggunakan matriks transformasi warna:
    R' = 0.393*R + 0.769*G + 0.189*B
    G' = 0.349*R + 0.686*G + 0.168*B
    B' = 0.272*R + 0.534*G + 0.131*B
    """
    r = img_rgb[:, :, 0].astype(np.float32)
    g = img_rgb[:, :, 1].astype(np.float32)
    b = img_rgb[:, :, 2].astype(np.float32)

    tr = 0.393 * r + 0.769 * g + 0.189 * b
    tg = 0.349 * r + 0.686 * g + 0.168 * b
    tb = 0.272 * r + 0.534 * g + 0.131 * b

    sepia = np.stack([np.clip(tr, 0, 255), np.clip(tg, 0, 255), np.clip(tb, 0, 255)], axis=2)
    return sepia.astype(np.uint8)

# ==============================================================================
# FITUR BARU: 12. EMBOSS (EFEK UKIRAN / RELIEF 3D MANUAL)
# ==============================================================================
def process_emboss(img_rgb: np.ndarray) -> np.ndarray:
    """
    Efek Emboss / Timbul 3D menggunakan konvolusi kernel diagonal berarah:
    [-2, -1, 0]
    [-1,  1, 1]
    [ 0,  1, 2] + 128 bias keabuan
    """
    kernel_emboss = np.array([
        [-2, -1, 0],
        [-1,  1, 1],
        [ 0,  1, 2]
    ], dtype=np.float32)

    gray = process_grayscale(img_rgb)
    embossed = manual_convolve2d(gray, kernel_emboss) + 128.0
    return np.clip(embossed, 0, 255).astype(np.uint8)

# ==============================================================================
# FITUR BARU: 13. MORFOLOGI EROSI (EROSION MANUAL 3x3)
# ==============================================================================
def process_erosion(img_rgb: np.ndarray) -> np.ndarray:
    """
    Operasi morfologi Erosi manual: mengambil nilai MINIMUM piksel pada tetangga 3x3.
    Mengikis batas objek biner / memperbesar area gelap.
    """
    gray = process_grayscale(img_rgb)
    h, w = gray.shape
    padded = np.pad(gray, ((1, 1), (1, 1)), mode='edge')
    
    # Ambil nilai minimum dari 9 tetangga 3x3
    eroded = np.min([padded[i:i + h, j:j + w] for i in range(3) for j in range(3)], axis=0)
    return eroded.astype(np.uint8)

# ==============================================================================
# FITUR BARU: 14. MORFOLOGI DILATASI (DILATION MANUAL 3x3)
# ==============================================================================
def process_dilation(img_rgb: np.ndarray) -> np.ndarray:
    """
    Operasi morfologi Dilatasi manual: mengambil nilai MAKSIMUM piksel pada tetangga 3x3.
    Mempertebal batas objek biner / memperbesar area terang.
    """
    gray = process_grayscale(img_rgb)
    h, w = gray.shape
    padded = np.pad(gray, ((1, 1), (1, 1)), mode='edge')
    
    # Ambil nilai maksimum dari 9 tetangga 3x3
    dilated = np.max([padded[i:i + h, j:j + w] for i in range(3) for j in range(3)], axis=0)
    return dilated.astype(np.uint8)

# ==============================================================================
# VISUALISASI HISTOGRAM: PERHITUNGAN FREKUENSI PIKSEL MANUAL
# ==============================================================================
def draw_histogram(img: np.ndarray, ax) -> None:
    """
    Menghitung distribusi frekuensi intensitas kemunculan piksel [0..255]
    secara manual tanpa fungsi library cv2.calcHist, lalu menggambarnya ke plot.
    """
    ax.clear()
    
    if len(img.shape) == 2:
        hist = np.bincount(img.flatten(), minlength=256)
        ax.plot(hist, color='#111111', linewidth=1.0)
        ax.fill_between(range(256), hist, color='#333333', alpha=0.7)
    else:
        colors = ('#D00000', '#009900', '#0044CC')
        for i, col in enumerate(colors):
            channel = img[:, :, i]
            hist = np.bincount(channel.flatten(), minlength=256)
            ax.plot(hist, color=col, linewidth=1.0, alpha=0.9)
            ax.fill_between(range(256), hist, color=col, alpha=0.3)

    ax.set_xlim([0, 256])
    ax.set_yticks([])
    ax.tick_params(axis='x', labelsize=7)
    ax.grid(True, linestyle=':', alpha=0.3)
