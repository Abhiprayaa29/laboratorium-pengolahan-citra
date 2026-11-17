"""Modul 2: Filter Spasial dan Efek Visual
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


class BlurOperation(BaseImageOperation):
    id = "filter_blur"
    name = "Pengaburan (Gaussian Blur)"
    category = "Filter dan Efek Visual"
    owner = "Modul 2"
    description = "Menghaluskan citra dan mereduksi derau menggunakan konvolusi kernel Gaussian 2D."
    status = OperationStatus.READY

    default_config = {"kernel_size": 5, "sigma": 1.0}
    config_schema = [
        ParameterSchema(
            name="kernel_size",
            label="Ukuran Kernel Ganjil",
            type=ParameterType.SELECT,
            default=5,
            options=[
                ParameterOption(label="3 × 3", value=3),
                ParameterOption(label="5 × 5", value=5),
                ParameterOption(label="7 × 7", value=7),
                ParameterOption(label="9 × 9", value=9),
            ],
            description="Dimensi matriks konvolusi Gaussian.",
        ),
        ParameterSchema(
            name="sigma",
            label="Standar Deviasi (Sigma)",
            type=ParameterType.SLIDER,
            default=1.0,
            min_value=0.5,
            max_value=5.0,
            step=0.5,
            description="Tingkat persebaran kurva Gaussian blur.",
        ),
    ]
    explanation = AcademicExplanation(
        pengertian="Penyaringan spasial low-pass filter menggunakan fungsi distribusi normal Gaussian.",
        tujuan="Mereduksi derau frekuensi tinggi dan menghaluskan transisi tepi tajam.",
        cara_kerja="Melakukan konvolusi matriks citra dengan kernel pembobotan berbasis jarak ke pusat.",
        rumus_matematis=r"G(x,y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}",
        parameter_info="Kernel size dan sigma menentukan radius dan kelembutan penghalusan.",
        pengaruh_gambar="Detail tajam dan bintik derau menjadi kabur dan halus.",
        pengaruh_histogram="Kurva histogram menyempit, standar deviasi intensitas menurun.",
        contoh_penerapan="Pra-pemrosesan sebelum edge detection (Canny) dan penghilangan artefak kompresi.",
        mengapa_seperti_ini="Nilai piksel tetangga dirata-ratakan secara tertimbang, mengurangi variasi ekstrem lokal.",
    )

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        ksize = int(config.get("kernel_size", 5))
        if ksize % 2 == 0:
            ksize += 1
        sigma = float(config.get("sigma", 1.0))
        return cv2.GaussianBlur(image, (ksize, ksize), sigmaX=sigma, sigmaY=sigma)


class SharpeningOperation(BaseImageOperation):
    id = "filter_sharpen"
    name = "Penajaman (Sharpening)"
    category = "Filter dan Efek Visual"
    owner = "Modul 2"
    description = "Memperjelas tepi objek dan meningkatkan kontras transisi frekuensi tinggi menggunakan kernel Laplacian."
    status = OperationStatus.READY
    has_kernel_preview = True

    default_config = {"strength": 1.0}
    config_schema = [
        ParameterSchema(
            name="strength",
            label="Kekuatan Penajaman",
            type=ParameterType.SLIDER,
            default=1.0,
            min_value=0.5,
            max_value=2.5,
            step=0.5,
            description="Skalasi magnitudo kernel high-pass.",
        )
    ]
    explanation = AcademicExplanation(
        pengertian="Penyaringan spasial high-pass filter untuk meningkatkan kontras detail lokal.",
        tujuan="Membuat gambar tampak lebih tajam dan menonjolkan fitur tekstur halus.",
        cara_kerja="Mengurangkan turunan kedua (Laplacian) dari citra asli.",
        rumus_matematis=(
            r"""K = \begin{bmatrix} 0 & -1 & 0 \\ -1 & 5 & -1 \\ 0 & -1 & 0 \end{bmatrix}"""
        ),
        parameter_info="Strength memperbesar koefisien tengah matriks kernel penajaman.",
        pengaruh_gambar="Garis tepi objek tampak lebih tegas dan tekstur lebih kontras.",
        pengaruh_histogram="Rentang dinamis histogram melebar, meningkatkan frekuensi piksel ekstrem dekat 0 dan 255.",
        contoh_penerapan="Penyempurnaan foto medis mikroskop dan fotografi digital.",
        mengapa_seperti_ini="Kernel menaikkan perbedaan nilai antara piksel terang dan gelap di perbatasan tepi.",
    )

    def _build_kernel(self, strength: float) -> np.ndarray:
        center = 1.0 + 4.0 * strength
        side = -1.0 * strength
        return np.array([
            [0.0, side, 0.0],
            [side, center, side],
            [0.0, side, 0.0],
        ], dtype=np.float32)

    def get_kernel_matrix(self, config: Dict[str, Any]) -> Optional[List[List[Union[int, float]]]]:
        strength = float(config.get("strength", 1.0))
        kernel = self._build_kernel(strength)
        return [[round(float(val), 2) for val in row] for row in kernel]

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        strength = float(config.get("strength", 1.0))
        kernel = self._build_kernel(strength)
        filtered = cv2.filter2D(image, -1, kernel)
        return np.clip(filtered, 0, 255).astype(np.uint8)


class EmbossOperation(BaseImageOperation):
    id = "filter_emboss"
    name = "Efek Timbul (Emboss)"
    category = "Filter dan Efek Visual"
    owner = "Modul 2"
    description = "Menciptakan ilusi 3D relief timbul dengan menonjolkan gradien arah mata angin dan menambahkan bias 128."
    status = OperationStatus.READY
    has_kernel_preview = True

    default_config = {"direction": "top_left"}
    config_schema = [
        ParameterSchema(
            name="direction",
            label="Arah Cahaya Relief",
            type=ParameterType.SELECT,
            default="top_left",
            options=[
                ParameterOption(label="Kiri Atas ke Kanan Bawah", value="top_left"),
                ParameterOption(label="Kanan Bawah ke Kiri Atas", value="bottom_right"),
            ],
            description="Sudut datang sumber cahaya bayangan emboss.",
        )
    ]
    explanation = AcademicExplanation(
        pengertian="Transformasi konvolusi terarah untuk mendeteksi gradien asimetris dengan offset abu-abu netral.",
        tujuan="Memberikan efek artistik ukiran logam/batu pada citra digital.",
        cara_kerja="Konvolusi kernel diferensial diagonal diikuti penambahan konstanta 128.",
        rumus_matematis=(
            r"""K = \begin{bmatrix} -2 & -1 & 0 \\ -1 & 1 & 1 \\ 0 & 1 & 2 \end{bmatrix} + 128"""
        ),
        parameter_info="Arah pencahayaan menentukan posisi bayangan dan sorotan terang relief.",
        pengaruh_gambar="Warna datar berubah menjadi abu-abu netral, tepi objek memiliki sorotan dan bayangan timbul.",
        pengaruh_histogram="Histogram terkonsentrasi sangat tinggi di sekitar nilai intensitas tengah (128).",
        contoh_penerapan="Pengenalan tekstur permukaan kasar dan efek grafis UI retro.",
        mengapa_seperti_ini="Area konstan menghasilkan nilai turunan nol yang ditambahkan bias 128 sehingga menjadi abu-abu.",
    )

    def _build_kernel(self, direction: str) -> np.ndarray:
        if direction == "bottom_right":
            return np.array([
                [2.0, 1.0, 0.0],
                [1.0, 1.0, -1.0],
                [0.0, -1.0, -2.0],
            ], dtype=np.float32)
        # default top_left
        return np.array([
            [-2.0, -1.0, 0.0],
            [-1.0, 1.0, 1.0],
            [0.0, 1.0, 2.0],
        ], dtype=np.float32)

    def get_kernel_matrix(self, config: Dict[str, Any]) -> Optional[List[List[Union[int, float]]]]:
        direction = config.get("direction", "top_left")
        kernel = self._build_kernel(direction)
        return [[int(val) for val in row] for row in kernel]

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        direction = config.get("direction", "top_left")
        kernel = self._build_kernel(direction)

        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image

        # Hitung konvolusi dengan kernel diferensial dan tambahkan bias 128
        embossed = cv2.filter2D(gray.astype(np.float32), -1, kernel) + 128.0
        clipped = np.clip(embossed, 0, 255).astype(np.uint8)

        # Kembalikan sebagai 3-channel RGB
        return np.stack([clipped, clipped, clipped], axis=2)


class SketchOperation(BaseImageOperation):
    id = "filter_sketch"
    name = "Efek Sketsa Pensil (Pencil Sketch)"
    category = "Filter dan Efek Visual"
    owner = "Modul 2"
    description = "Mengubah citra menjadi sketsa pensil hitam-putih artistik menggunakan kombinasi grayscale, inversi, blur, dan color dodge."
    status = OperationStatus.READY

    default_config = {"blur_radius": 21}
    config_schema = [
        ParameterSchema(
            name="blur_radius",
            label="Radius Kelembutan Goresan",
            type=ParameterType.SLIDER,
            default=21,
            min_value=3,
            max_value=51,
            step=2,
            description="Tingkat kehalusan bayangan pensil (harus bilangan ganjil).",
        )
    ]
    explanation = AcademicExplanation(
        pengertian="Simulasi visual gambar sketsa pensil manual menggunakan teknik Color Dodge blending.",
        tujuan="Menciptakan efek gambar sketsa tangan dari foto nyata.",
        cara_kerja="Mengonversi ke grayscale, membalik intensitas, menerapkan Gaussian Blur kuat, lalu melakukan pembagian Color Dodge.",
        rumus_matematis=r"\text{Sketch} = \min\left(255, \frac{I_{\text{gray}} \times 255}{255 - I_{\text{blur}} + \epsilon}\right)",
        parameter_info="Radius blur yang lebih besar menghasilkan arsiran sketsa yang lebih tebal dan berdimensi.",
        pengaruh_gambar="Citra berubah menjadi gambar garis sketsa pensil hitam di atas kertas putih.",
        pengaruh_histogram="Histogram didominasi warna putih (255) dengan sebaran goresan gelap di nilai rendah.",
        contoh_penerapan="Efek filter artistik foto profil, ilustrasi otomatis, dan komik grafis.",
        mengapa_seperti_ini="Color Dodge membagi citra dasar dengan citra terbalik yang diblur, menonjolkan tepian tajam sementara area datar memutih.",
    )

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        radius = int(config.get("blur_radius", 21))
        if radius % 2 == 0:
            radius += 1
        radius = max(3, radius)

        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image

        inverted = 255 - gray
        blurred = cv2.GaussianBlur(inverted, (radius, radius), sigmaX=0, sigmaY=0)

        # Color Dodge Blending formula
        denom = np.maximum(255.0 - blurred.astype(np.float32), 1.0)
        sketch = (gray.astype(np.float32) * 255.0) / denom
        clipped = np.clip(sketch, 0, 255).astype(np.uint8)

        return np.stack([clipped, clipped, clipped], axis=2)
