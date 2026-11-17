"""Modul 3: Transformasi Geometri - PENCERMINAN (Mirroring)
Penanggung Jawab: Orang 3
Algoritma: OpenCV cv2.flip()
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


class MirroringOperation(BaseImageOperation):
    id = "geometry_mirroring"
    name = "Pencerminan (Mirroring)"
    category = "Operasi Morfologi dan Geometri"
    owner = "Orang 3"
    description = "Membalikkan posisi spasial piksel citra secara horizontal, vertikal, atau kedua sumbu simetri."
    status = OperationStatus.READY
    has_kernel_preview = False

    default_config = {
        "axis": "horizontal",
    }

    config_schema = [
        ParameterSchema(
            name="axis",
            label="Sumbu Pencerminan",
            type=ParameterType.SELECT,
            default="horizontal",
            options=[
                ParameterOption(
                    label="Horizontal (Kiri ↔ Kanan)",
                    value="horizontal",
                    description="Membalik susunan piksel sepanjang sumbu vertikal Y (x' = W - 1 - x)",
                ),
                ParameterOption(
                    label="Vertikal (Atas ↕ Bawah)",
                    value="vertical",
                    description="Membalik susunan piksel sepanjang sumbu horizontal X (y' = H - 1 - y)",
                ),
                ParameterOption(
                    label="Kedua Sumbu (Horizontal & Vertikal)",
                    value="both",
                    description="Membalik secara simultan kedua sumbu (rotasi 180 derajat)",
                ),
            ],
            description="Pilihan sumbu koordinat geometri tempat pencerminan dilakukan.",
        ),
    ]

    explanation = AcademicExplanation(
        pengertian=(
            "Pencerminan (mirroring atau reflection) adalah transformasi geometri afine pada citra digital yang "
            "memetakan setiap piksel dari posisi spasial (x, y) ke posisi baru (x', y') terhadap suatu garis "
            "atau bidang simetri koordinat kartesius."
        ),
        tujuan=(
            "1. Augmentasi data pada machine learning dan deep learning untuk melipatgandakan variasi dataset.\n"
            "2. Mengoreksi orientasi citra hasil tangkapan kamera depan (selfie mirror correction).\n"
            "3. Efek visual simetri artistik dan analisis simetri objek."
        ),
        cara_kerja=(
            "Piksel citra dipindahkan ke koordinat baru tanpa memodifikasi nilai intensitas warna sedikit pun. "
            "Pencerminan horizontal membalik urutan kolom piksel. Pencerminan vertikal membalik urutan baris piksel. "
            "Pencerminan dua kali pada sumbu yang sama bersifat involusi f(f(I)) = I, mengembalikan citra tepat ke keadaan semula."
        ),
        rumus_matematis=(
            r"""\begin{aligned}
\text{Horizontal:} \quad & x' = W - 1 - x, \quad y' = y \\
\text{Vertikal:} \quad & x' = x, \quad y' = H - 1 - y \\
\text{Kedua Sumbu:} \quad & x' = W - 1 - x, \quad y' = H - 1 - y
\end{aligned}"""
        ),
        parameter_info=(
            "Parameter axis menentukan arah pemetaan koordinat: 'horizontal' menggunakan OpenCV flipCode=1, "
            "'vertical' menggunakan flipCode=0, dan 'both' menggunakan flipCode=-1."
        ),
        pengaruh_gambar=(
            "Objek citra tampak terbalik dari sisi kiri ke kanan, atas ke bawah, atau keduanya. "
            "Bentuk, proporsi ukuran, saturasi warna, dan ketajaman citra tetap terjaga secara sempurna."
        ),
        pengaruh_histogram=(
            "Histogram TIDAK BERUBAH SAMA SEKALI (100% IDENTIK). Hal ini membuktikan bahwa histogram hanya "
            "merepresentasikan frekuensi kemunculan intensitas piksel secara global dan TIDAK memuat informasi spasial atau posisi piksel."
        ),
        contoh_penerapan=(
            "Data augmentation untuk Computer Vision (misal deteksi pejalan kaki, klasifikasi citra), "
            "pembetulan hasil pemindaian dokumen terbalik, dan pemrosesan citra teleskop optik."
        ),
        mengapa_seperti_ini=(
            "Objek terlihat terbalik secara horizontal atau vertikal, tetapi histogramnya tetap sama karena "
            "nilai intensitas piksel tidak berubah sama sekali, hanya letak koordinatnya yang ditukar."
        ),
    )

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        axis = config.get("axis", self.default_config["axis"]).lower()

        if axis == "horizontal":
            flip_code = 1
        elif axis == "vertical":
            flip_code = 0
        elif axis in ("both", "both_axes"):
            flip_code = -1
        else:
            flip_code = 1

        return cv2.flip(image, flip_code)
