"""Modul 3: Operasi Morfologi - EROSI (Erosion)
Penanggung Jawab: Orang 3
Algoritma: OpenCV cv2.erode() & cv2.getStructuringElement()
"""

from typing import Any, Dict, List, Optional
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


class ErosionOperation(BaseImageOperation):
    id = "morphology_erosion"
    name = "Erosi (Erosion)"
    category = "Operasi Morfologi dan Geometri"
    owner = "Orang 3"
    description = "Mengikis atau memperkecil area foreground objek berdasarkan elemen penstruktur (structuring element)."
    status = OperationStatus.READY
    has_kernel_preview = True

    default_config = {
        "kernel_shape": "rect",
        "kernel_size": 3,
        "iterations": 1,
        "mode": "rgb",
    }

    config_schema = [
        ParameterSchema(
            name="kernel_shape",
            label="Bentuk Elemen Penstruktur (Kernel)",
            type=ParameterType.SELECT,
            default="rect",
            options=[
                ParameterOption(label="Persegi Panjang (Rectangle)", value="rect", description="Elemen penstruktur persegi berukuran k x k"),
                ParameterOption(label="Elips (Ellipse)", value="ellipse", description="Elemen penstruktur berbentuk elips / lingkaran"),
                ParameterOption(label="Silang (Cross)", value="cross", description="Elemen penstruktur berbentuk salib berpusat di tengah"),
            ],
            description="Bentuk geometri structuring element yang menyapu citra.",
        ),
        ParameterSchema(
            name="kernel_size",
            label="Ukuran Kernel",
            type=ParameterType.SELECT,
            default=3,
            options=[
                ParameterOption(label="3 × 3 piksel", value=3),
                ParameterOption(label="5 × 5 piksel", value=5),
                ParameterOption(label="7 × 7 piksel", value=7),
            ],
            description="Dimensi matriks lokal ketetanggaan (neighborhood).",
        ),
        ParameterSchema(
            name="iterations",
            label="Jumlah Iterasi",
            type=ParameterType.SELECT,
            default=1,
            options=[
                ParameterOption(label="1 kali", value=1),
                ParameterOption(label="2 kali", value=2),
                ParameterOption(label="3 kali", value=3),
                ParameterOption(label="5 kali", value=5),
            ],
            description="Frekuensi erosi diaplikasikan berturut-turut pada citra.",
        ),
        ParameterSchema(
            name="mode",
            label="Mode Pemrosesan Warna",
            type=ParameterType.SELECT,
            default="rgb",
            options=[
                ParameterOption(label="RGB Channel-Wise (Pertahankan Warna)", value="rgb", description="Erosi diterapkan pada setiap saluran R, G, B secara independen"),
                ParameterOption(label="Grayscale (Monokromatik)", value="grayscale", description="Citra diubah menjadi intensitas keabuan sebelum dierosi"),
            ],
            description="Cara citra berwarna diolah selama operasi morfologi.",
        ),
    ]

    explanation = AcademicExplanation(
        pengertian=(
            "Erosi adalah salah satu operasi dasar morfologi matematika citra yang bertujuan untuk mengikis "
            "atau menyusutkan batas-batas objek foreground (biasanya piksel bernilai tinggi/putih). "
            "Operasi ini bekerja dengan menggeser elemen penstruktur (structuring element) ke seluruh piksel citra."
        ),
        tujuan=(
            "1. Menghilangkan derau (noise) putih berukuran kecil (salt noise).\n"
            "2. Memisahkan dua objek yang saling bersinggungan secara tipis.\n"
            "3. Memperkecil atau menipiskan ukuran objek biner/grayscale."
        ),
        cara_kerja=(
            "Elemen penstruktur B digeser di atas citra f(x, y). Pada setiap posisi piksel, nilai piksel pusat "
            "digantikan dengan nilai MINIMUM dari seluruh piksel yang tertutupi oleh elemen penstruktur B. "
            "Pixel batas (border) ditangani secara eksplisit menggunakan borderType=cv2.BORDER_CONSTANT dengan "
            "borderValue=0 (konvensi latar belakang gelap)."
        ),
        rumus_matematis=(
            r"g(x,y) = (f \ominus B)(x,y) = \min_{(i,j) \in B} \{ f(x+i, y+j) \}"
        ),
        parameter_info=(
            "Ukuran kernel (3x3, 5x5, 7x7) menentukan seberapa luas radius tetangga yang diperiksa. "
            "Semakin besar ukuran kernel atau semakin banyak iterasi, semakin agresif pengikisan objek putih."
        ),
        pengaruh_gambar=(
            "Objek foreground terang tampak menyusut atau menipis. Lubang-lubang kecil berwarna gelap di dalam objek "
            "akan membesar, dan tonjolan-tonjolan kecil di tepi objek akan terhapus."
        ),
        pengaruh_histogram=(
            "Distribusi histogram bergeser ke arah intensitas yang lebih rendah (kiri). Frekuensi nilai piksel gelap "
            "meningkat karena nilai lokal piksel digantikan dengan nilai minimum tetangganya."
        ),
        contoh_penerapan=(
            "Digunakan dalam pemisahan karakter tulisan tangan yang terhubung (character segmentation), "
            "penghilangan artefak debu pada citra biner dokumen, dan inspeksi PCB manufaktur."
        ),
        mengapa_seperti_ini=(
            "Objek berwarna putih tampak semakin mengecil karena setiap piksel dipengaruhi oleh nilai minimum "
            "pada area tetangganya. Semakin besar kernel dan semakin banyak iterasi, semakin banyak piksel putih "
            "yang tereliminasi oleh piksel hitam di sekitarnya."
        ),
    )

    def _get_structuring_element(self, shape_name: str, size: int) -> np.ndarray:
        shapes = {
            "rect": cv2.MORPH_RECT,
            "ellipse": cv2.MORPH_ELLIPSE,
            "cross": cv2.MORPH_CROSS,
        }
        shape_flag = shapes.get(shape_name.lower(), cv2.MORPH_RECT)
        return cv2.getStructuringElement(shape_flag, (int(size), int(size)))

    def get_kernel_matrix(self, config: Dict[str, Any]) -> Optional[List[List[int]]]:
        shape = config.get("kernel_shape", self.default_config["kernel_shape"])
        size = int(config.get("kernel_size", self.default_config["kernel_size"]))
        kernel = self._get_structuring_element(shape, size)
        return kernel.tolist()

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        shape_name = config.get("kernel_shape", self.default_config["kernel_shape"])
        kernel_size = int(config.get("kernel_size", self.default_config["kernel_size"]))
        iterations = int(config.get("iterations", self.default_config["iterations"]))
        mode = config.get("mode", self.default_config["mode"]).lower()

        kernel = self._get_structuring_element(shape_name, kernel_size)

        # Border handling: explicit cv2.BORDER_CONSTANT with borderValue=0
        border_type = cv2.BORDER_CONSTANT
        border_value = 0

        if mode == "grayscale":
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            eroded = cv2.erode(
                gray,
                kernel,
                iterations=iterations,
                borderType=border_type,
                borderValue=border_value,
            )
            # Return as 3-channel RGB for unified UI rendering if desired
            return cv2.cvtColor(eroded, cv2.COLOR_GRAY2RGB)
        else:
            # RGB channel-wise or single channel
            if len(image.shape) == 2:
                return cv2.erode(
                    image,
                    kernel,
                    iterations=iterations,
                    borderType=border_type,
                    borderValue=border_value,
                )
            # Channel-wise erosion preserves color structure
            channels = cv2.split(image)
            eroded_channels = [
                cv2.erode(
                    ch,
                    kernel,
                    iterations=iterations,
                    borderType=border_type,
                    borderValue=border_value,
                )
                for ch in channels
            ]
            return cv2.merge(eroded_channels)
