"""Modul 4: Segmentasi, Histogram, dan Deteksi Tepi
Status: Terintegrasi & Aktif (Production Ready)
"""

from typing import Any, Dict, List, Optional, Union
import cv2
import numpy as np

from app.core.registry.base import BaseImageOperation
from app.schemas.operation import (
    AcademicExplanation,
    OperationStatus,
    ParameterOption,
    ParameterSchema,
    ParameterType,
)


class ThresholdingOperation(BaseImageOperation):
    id = "segmentation_threshold"
    name = "Penambangan Citra (Thresholding)"
    category = "Segmentasi, Histogram, dan Deteksi Tepi"
    owner = "Modul 4"
    description = "Mengubah citra grayscale menjadi biner murni (0 atau 255) berdasarkan nilai ambang batas."
    status = OperationStatus.READY

    default_config = {"thresh": 128, "type": "binary"}
    config_schema = [
        ParameterSchema(
            name="thresh",
            label="Nilai Ambang (Threshold Value)",
            type=ParameterType.SLIDER,
            default=128,
            min_value=0,
            max_value=255,
            step=1,
            description="Nilai batas pemisahan foreground dan background.",
        ),
        ParameterSchema(
            name="type",
            label="Tipe Thresholding",
            type=ParameterType.SELECT,
            default="binary",
            options=[
                ParameterOption(label="Biner Standar (Binary)", value="binary"),
                ParameterOption(label="Biner Terbalik (Binary Inverted)", value="binary_inv"),
                ParameterOption(label="Truncate", value="trunc"),
            ],
            description="Aturan pemetaan piksel di atas dan di bawah nilai ambang.",
        ),
    ]
    explanation = AcademicExplanation(
        pengertian="Metode segmentasi citra paling mendasar untuk memisahkan objek dari latar belakang.",
        tujuan="Menghasilkan citra biner hitam-putih untuk ekstraksi bentuk dan kontur objek.",
        cara_kerja="Membandingkan setiap piksel dengan nilai ambang T; jika lebih besar menjadi 255, jika tidak menjadi 0.",
        rumus_matematis=(
            r"""g(x,y) = \begin{cases} 255 & \text{jika } f(x,y) \ge T \\ 0 & \text{jika } f(x,y) < T \end{cases}"""
        ),
        parameter_info="Nilai T menentukan seberapa terang piksel agar dikelompokkan sebagai objek foreground.",
        pengaruh_gambar="Semua warna dan gradasi hilang; hanya tersisa piksel hitam murni (0) dan putih murni (255).",
        pengaruh_histogram="Seluruh distribusi runtuh menjadi hanya 2 batang frekuensi ekstrem: di bin 0 dan bin 255.",
        contoh_penerapan="Segmentasi teks dokumen pindaian, pembacaan barcode/QR Code, dan penghitungan sel mikroskop.",
        mengapa_seperti_ini="Operasi biner memetakan seluruh rentang nilai kontinu ke dalam dua nilai diskrit mutlak.",
    )

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image

        thresh_val = int(config.get("thresh", 128))
        thresh_type_str = config.get("type", "binary")

        if thresh_type_str == "binary_inv":
            cv_flag = cv2.THRESH_BINARY_INV
        elif thresh_type_str == "trunc":
            cv_flag = cv2.THRESH_TRUNC
        else:
            cv_flag = cv2.THRESH_BINARY

        _, thresh_out = cv2.threshold(gray, thresh_val, 255, cv_flag)
        return np.stack([thresh_out, thresh_out, thresh_out], axis=2)


class EqualizationOperation(BaseImageOperation):
    id = "histogram_equalization"
    name = "Ekualisasi Histogram (Histogram Equalization)"
    category = "Segmentasi, Histogram, dan Deteksi Tepi"
    owner = "Modul 4"
    description = "Meratakan distribusi intensitas piksel secara nonlinier menggunakan CDF untuk meningkatkan kontras global."
    status = OperationStatus.READY

    default_config = {}
    config_schema = []
    explanation = AcademicExplanation(
        pengertian="Metode peningkatan kontras citra berbasis fungsi distribusi kumulatif (CDF) histogram.",
        tujuan="Memperjelas detail pada citra berkontras rendah (terlalu gelap, terlalu terang, atau pudar).",
        cara_kerja="Menghitung probabilitas frekuensi intensitas, lalu memetakan ulang nilai piksel secara kumulatif merata.",
        rumus_matematis=(
            r"""s_k = T(r_k) = (L - 1) \sum_{j=0}^{k} p_r(r_j) = \frac{L - 1}{MN} \sum_{j=0}^{k} n_j"""
        ),
        parameter_info="Operasi ini tidak memerlukan parameter manual karena dihitung otomatis dari statistik citra.",
        pengaruh_gambar="Kontras meningkat dramatis; tekstur dan objek tersembunyi menjadi jauh lebih jelas terlihat.",
        pengaruh_histogram="Puncak histogram yang awalnya menumpuk menyebar merata di sepanjang rentang 0 hingga 255.",
        contoh_penerapan="Pemrosesan foto rontgen medis, foto satelit cuaca, dan fotografi bawah laut.",
        mengapa_seperti_ini="Nilai intensitas dipetakan ulang sehingga setiap interval intensitas memiliki probabilitas kemunculan yang seimbang.",
    )

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        if len(image.shape) == 2:
            equalized = cv2.equalizeHist(image)
            return np.stack([equalized, equalized, equalized], axis=2)

        # Citra warna RGB: konversi ke YCrCb, ekualisasi channel Y (Luminansi), lalu konversi kembali ke RGB
        ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)


class EdgeDetectionOperation(BaseImageOperation):
    id = "edge_detection_sobel"
    name = "Deteksi Tepi Sobel (Sobel Edge Detection)"
    category = "Segmentasi, Histogram, dan Deteksi Tepi"
    owner = "Modul 4"
    description = "Mendeteksi diskontinuitas batas kontur objek menggunakan operator turunan gradien Sobel horizontal dan vertikal."
    status = OperationStatus.READY
    has_kernel_preview = True

    default_config = {"kernel_size": 3, "thresh": 100}
    config_schema = [
        ParameterSchema(
            name="kernel_size",
            label="Ukuran Kernel Sobel",
            type=ParameterType.SELECT,
            default=3,
            options=[
                ParameterOption(label="3 × 3", value=3),
                ParameterOption(label="5 × 5", value=5),
            ],
            description="Dimensi operator aproksimasi gradien spasial.",
        ),
        ParameterSchema(
            name="thresh",
            label="Ambang Magnitudo Tepi",
            type=ParameterType.SLIDER,
            default=100,
            min_value=0,
            max_value=255,
            step=5,
            description="Batas minimum kekuatan gradien agar dianggap sebagai garis tepi (0 = gradien lembut berskala penuh).",
        ),
    ]
    explanation = AcademicExplanation(
        pengertian="Operator diferensial orde pertama untuk mendeteksi tepi tajam pada arah horizontal dan vertikal.",
        tujuan="Mengekstraksi garis batas tepi bentuk objek dan mengabaikan area permukaan seragam.",
        cara_kerja="Menghitung gradien Gx dan Gy menggunakan kernel konvolusi terpisah, lalu menggabungkan magnitudonya.",
        rumus_matematis=(
            r"""G = \sqrt{G_x^2 + G_y^2}, \quad G_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix} * I"""
        ),
        parameter_info="Kernel 3x3 memberikan deteksi tepi tajam lokal; nilai thresh memfilter tepi halus.",
        pengaruh_gambar="Area datar menjadi hitam legam; garis batas kontur objek bersinar terang putih.",
        pengaruh_histogram="Histogram didominasi piksel gelap mendekati 0 dengan ekor panjang piksel terang di nilai tepi tinggi.",
        contoh_penerapan="Deteksi lajur jalan kendaraan otonom, pengukuran dimensi benda industri, dan face recognition.",
        mengapa_seperti_ini="Derivatif spasial menghasilkan nilai besar hanya ketika terjadi lonjakan intensitas mendadak antara dua piksel berdekatan.",
    )

    def get_kernel_matrix(self, config: Dict[str, Any]) -> Optional[List[List[Union[int, float]]]]:
        # Tampilkan kernel Sobel Horizontal 3x3 sebagai representasi visualizer
        return [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1],
        ]

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image

        ksize = int(config.get("kernel_size", 3))
        if ksize not in (1, 3, 5, 7):
            ksize = 3
        thresh = int(config.get("thresh", 100))

        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        magnitude = np.hypot(gx, gy)

        if thresh > 0:
            edges = np.zeros_like(gray, dtype=np.uint8)
            edges[magnitude >= thresh] = 255
        else:
            max_val = np.max(magnitude)
            edges = (magnitude / (max_val + 1e-5) * 255).astype(np.uint8)

        return np.stack([edges, edges, edges], axis=2)
