"""Modul 1: Transformasi Warna dan Intensitas
Status: Terintegrasi & Aktif (Production Ready)
"""

from typing import Any, Dict
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


class GrayscaleOperation(BaseImageOperation):
    id = "intensity_grayscale"
    name = "Grayscale (Keabuan)"
    category = "Transformasi Warna dan Intensitas"
    owner = "Modul 1"
    description = "Mengonversi citra berwarna RGB menjadi citra monokromatik menggunakan formula luminansi standar."
    status = OperationStatus.READY

    default_config = {"method": "luminance"}
    config_schema = [
        ParameterSchema(
            name="method",
            label="Metode Konversi",
            type=ParameterType.SELECT,
            default="luminance",
            options=[
                ParameterOption(label="Luminansi ITU-R BT.601 (0.299R + 0.587G + 0.114B)", value="luminance"),
                ParameterOption(label="Average / Rata-rata Sederhana ((R+G+B)/3)", value="average"),
            ],
            description="Metode pembobotan saluran warna menjadi satu nilai intensitas keabuan.",
        )
    ]
    explanation = AcademicExplanation(
        pengertian="Konversi citra warna 3-channel ke 1-channel intensitas keabuan.",
        tujuan="Menyederhanakan data citra untuk pemrosesan tahap lanjut seperti segmentasi dan deteksi tepi.",
        cara_kerja="Menggabungkan nilai saluran R, G, B menggunakan bobot sensitivitas mata manusia.",
        rumus_matematis=r"Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B",
        parameter_info="Pilihan metode menentukan proporsi kontribusi tiap saluran warna.",
        pengaruh_gambar="Warna hilang menjadi tingkatan abu-abu antara hitam (0) dan putih (255).",
        pengaruh_histogram="Tiga grafik histogram RGB bergabung menjadi satu kurva distribusi luminansi tunggal.",
        contoh_penerapan="Pre-processing OCR, pengenalan wajah, dan deteksi plat nomor.",
        mengapa_seperti_ini="Mata manusia paling sensitif terhadap warna hijau, sehingga bobot hijau paling tinggi.",
    )

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        method = config.get("method", "luminance")
        if len(image.shape) == 2:
            gray = image
        else:
            r = image[:, :, 0].astype(np.float32)
            g = image[:, :, 1].astype(np.float32)
            b = image[:, :, 2].astype(np.float32)
            if method == "average":
                gray = (r + g + b) / 3.0
            else:
                gray = 0.299 * r + 0.587 * g + 0.114 * b
            gray = np.clip(gray, 0, 255).astype(np.uint8)

        # Kembalikan sebagai 3-channel RGB representasi monokromatik untuk chaining pipeline
        return np.stack([gray, gray, gray], axis=2)


class NegativeOperation(BaseImageOperation):
    id = "intensity_negative"
    name = "Citra Negatif (Negative)"
    category = "Transformasi Warna dan Intensitas"
    owner = "Modul 1"
    description = "Membalikkan nilai intensitas piksel citra sehingga warna terang menjadi gelap dan sebaliknya."
    status = OperationStatus.READY

    default_config = {}
    config_schema = []
    explanation = AcademicExplanation(
        pengertian="Transformasi inversi nilai intensitas piksel citra.",
        tujuan="Meningkatkan visibilitas detail objek tersembunyi pada area gelap.",
        cara_kerja="Setiap nilai piksel dikurangkan dari nilai maksimum 255.",
        rumus_matematis=r"s = (L - 1) - r = 255 - r",
        parameter_info="Tidak memerlukan parameter tambahan.",
        pengaruh_gambar="Warna dan kontras terbalik (seperti klise film fotografi).",
        pengaruh_histogram="Bentuk kurva histogram diputar balik secara horizontal 180 derajat terhadap sumbu tengah (127.5).",
        contoh_penerapan="Analisis citra rontgen/X-Ray dan mammografi medis.",
        mengapa_seperti_ini="Nilai intensitas dibalik: piksel putih (255) menjadi hitam (0), dan sebaliknya.",
    )

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        return (255 - image).astype(np.uint8)


class SepiaOperation(BaseImageOperation):
    id = "intensity_sepia"
    name = "Efek Sepia (Sepia Tone)"
    category = "Transformasi Warna dan Intensitas"
    owner = "Modul 1"
    description = "Memberikan nuansa warna cokelat hangat bergaya vintage fotografi klasik melalui transformasi matriks."
    status = OperationStatus.READY

    default_config = {"intensity": 1.0}
    config_schema = [
        ParameterSchema(
            name="intensity",
            label="Intensitas Efek Sepia",
            type=ParameterType.SLIDER,
            default=1.0,
            min_value=0.0,
            max_value=1.0,
            step=0.1,
            description="Kekuatan penerapan transformasi matriks sepia.",
        )
    ]
    explanation = AcademicExplanation(
        pengertian="Transformasi warna linier menggunakan perkalian matriks pembobotan RGB khusus sepia.",
        tujuan="Menghasilkan estetika retro/vintage pada citra.",
        cara_kerja="Mengalikan vektor [R, G, B] setiap piksel dengan matriks transformasi sepia standar.",
        rumus_matematis=(
            r"""\begin{bmatrix} R' \\ G' \\ B' \end{bmatrix} = \begin{bmatrix} 0.393 & 0.769 & 0.189 \\ 0.349 & 0.686 & 0.168 \\ 0.272 & 0.534 & 0.131 \end{bmatrix} \begin{bmatrix} R \\ G \\ B \end{bmatrix}"""
        ),
        parameter_info="Intensitas mengontrol blend antara citra asli dan citra bergradasi sepia.",
        pengaruh_gambar="Warna citra berubah dominan kecokelatan hangat.",
        pengaruh_histogram="Saluran Red dan Green meningkat secara signifikan dibanding Blue.",
        contoh_penerapan="Penyuntingan foto artistik dan restorasi arsip digital.",
        mengapa_seperti_ini="Pigmen warna cokelat dihasilkan dari dominasi nilai merah dan hijau yang lebih tinggi dari biru.",
    )

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        intensity = float(config.get("intensity", 1.0))
        if len(image.shape) == 2:
            rgb = np.stack([image, image, image], axis=2)
        else:
            rgb = image

        r = rgb[:, :, 0].astype(np.float32)
        g = rgb[:, :, 1].astype(np.float32)
        b = rgb[:, :, 2].astype(np.float32)

        tr = 0.393 * r + 0.769 * g + 0.189 * b
        tg = 0.349 * r + 0.686 * g + 0.168 * b
        tb = 0.272 * r + 0.534 * g + 0.131 * b

        sepia = np.stack(
            [np.clip(tr, 0, 255), np.clip(tg, 0, 255), np.clip(tb, 0, 255)],
            axis=2,
        ).astype(np.uint8)

        if intensity < 1.0:
            return cv2.addWeighted(sepia, intensity, rgb, 1.0 - intensity, 0)
        return sepia


class BrightnessOperation(BaseImageOperation):
    id = "intensity_brightness"
    name = "Kecerahan (Brightness Adjustment)"
    category = "Transformasi Warna dan Intensitas"
    owner = "Modul 1"
    description = "Menggeser nilai kecerahan citra secara aditif dengan pembatasan clipping rentang [0, 255]."
    status = OperationStatus.READY

    default_config = {"beta": 30}
    config_schema = [
        ParameterSchema(
            name="beta",
            label="Nilai Pergeseran Kecerahan (Offset)",
            type=ParameterType.SLIDER,
            default=30,
            min_value=-100,
            max_value=100,
            step=5,
            description="Nilai skalar yang ditambahkan atau dikurangkan pada setiap piksel.",
        )
    ]
    explanation = AcademicExplanation(
        pengertian="Penambahan skalar konstan pada seluruh piksel citra.",
        tujuan="Memperbaiki citra yang mengalami underexposure (terlalu gelap) atau overexposure (terlalu terang).",
        cara_kerja="Menambahkan nilai bias beta ke setiap piksel dan melakukan clipping pada rentang [0, 255].",
        rumus_matematis=r"g(x,y) = \text{clip}(f(x,y) + \beta, 0, 255)",
        parameter_info="Nilai beta positif mencerahkan citra, nilai beta negatif menggelapkan citra.",
        pengaruh_gambar="Seluruh gambar menjadi lebih terang atau lebih gelap secara merata.",
        pengaruh_histogram="Seluruh kurva histogram bergeser ke kanan (beta > 0) atau ke kiri (beta < 0).",
        contoh_penerapan="Koreksi pencahayaan pada kamera CCTV malam hari dan fotografi.",
        mengapa_seperti_ini="Operasi aditif menggeser seluruh spektrum nilai piksel tanpa mengubah kontras relatif antar piksel.",
    )

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        beta = int(config.get("beta", 30))
        bright = image.astype(np.int32) + beta
        return np.clip(bright, 0, 255).astype(np.uint8)
