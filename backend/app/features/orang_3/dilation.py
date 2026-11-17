"""Modul 3: Operasi Morfologi - DILASI (Dilation)
Penanggung Jawab: Orang 3
Algoritma: OpenCV cv2.dilate() & cv2.getStructuringElement()
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


class DilationOperation(BaseImageOperation):
    id = "morphology_dilation"
    name = "Dilasi (Dilation)"
    category = "Operasi Morfologi dan Geometri"
    owner = "Modul 3"
    description = "Memperbesar atau memperluas area foreground objek berdasarkan elemen penstruktur (structuring element)."
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
            description="Frekuensi dilasi diaplikasikan berturut-turut pada citra.",
        ),
        ParameterSchema(
            name="mode",
            label="Mode Pemrosesan Warna",
            type=ParameterType.SELECT,
            default="rgb",
            options=[
                ParameterOption(label="RGB Channel-Wise (Pertahankan Warna)", value="rgb", description="Dilasi diterapkan pada setiap saluran R, G, B secara independen"),
                ParameterOption(label="Grayscale (Monokromatik)", value="grayscale", description="Citra diubah menjadi intensitas keabuan sebelum didilasi"),
            ],
            description="Cara citra berwarna diolah selama operasi morfologi.",
        ),
    ]

    explanation = AcademicExplanation(
        pengertian=(
            "Dilasi adalah operasi dasar morfologi citra yang bertujuan untuk memperbesar, mempertebal, "
            "atau menjembatani ruang antar objek foreground terang (piksel bernilai tinggi). "
            "Operasi ini merupakan kebalikan (dualitas) matematis dari operasi erosi."
        ),
        tujuan=(
            "1. Menjembatani atau menghubungkan bagian objek yang terputus (reconnecting fractures).\n"
            "2. Menutup lubang-lubang kecil (pepper noise) di dalam area objek putih.\n"
            "3. Mempertebal batas kontur objek agar lebih mudah dideteksi."
        ),
        cara_kerja=(
            "Elemen penstruktur B digeser di atas citra f(x, y). Pada setiap titik koordinat, nilai piksel pusat "
            "digantikan dengan nilai MAKSIMUM dari seluruh piksel yang tercakup oleh elemen penstruktur B. "
            "Penanganan piksel batas (border) menggunakan cv2.BORDER_CONSTANT dengan borderValue=0 secara konsisten."
        ),
        rumus_matematis=(
            r"g(x,y) = (f \oplus B)(x,y) = \max_{(i,j) \in B} \{ f(x+i, y+j) \}"
        ),
        parameter_info=(
            "Pemilihan kernel elips menghasilkan pemuaian objek yang lebih membulat halus, "
            "sedangkan kernel persegi menghasilkan sudut-sudut tegas. Jumlah iterasi melipatgandakan efek pemuaian."
        ),
        pengaruh_gambar=(
            "Objek putih/terang tampak membesar dan meluas ke latar belakang gelap. "
            "Celah sempit antar objek akan menyatu dan lubang gelap di dalam objek akan tertutup."
        ),
        pengaruh_histogram=(
            "Distribusi histogram bergeser ke arah intensitas yang lebih tinggi (kanan). Frekuensi nilai piksel terang "
            "meningkat secara signifikan karena piksel lokal digantikan oleh nilai maksimum tetangganya."
        ),
        contoh_penerapan=(
            "Digunakan dalam Optical Character Recognition (OCR) untuk menyambungkan garis huruf putus-putus, "
            "segmentasi pembuluh darah pada citra medis retina, dan deteksi plat nomor kendaraan."
        ),
        mengapa_seperti_ini=(
            "Objek berwarna putih tampak semakin luas karena setiap piksel dipengaruhi oleh nilai maksimum "
            "pada area tetangganya. Nilai piksel terang mendominasi area sekitarnya sesuai radius kernel."
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

        # Border handling
        border_type = cv2.BORDER_CONSTANT
        border_value = 0

        if mode == "grayscale":
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            dilated = cv2.dilate(
                gray,
                kernel,
                iterations=iterations,
                borderType=border_type,
                borderValue=border_value,
            )
            return cv2.cvtColor(dilated, cv2.COLOR_GRAY2RGB)
        else:
            if len(image.shape) == 2:
                return cv2.dilate(
                    image,
                    kernel,
                    iterations=iterations,
                    borderType=border_type,
                    borderValue=border_value,
                )
            channels = cv2.split(image)
            dilated_channels = [
                cv2.dilate(
                    ch,
                    kernel,
                    iterations=iterations,
                    borderType=border_type,
                    borderValue=border_value,
                )
                for ch in channels
            ]
            return cv2.merge(dilated_channels)
