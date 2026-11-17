# Panduan Kontribusi — Laboratorium Pengolahan Citra Digital (LPCD)

Terima kasih atas kontribusi Anda dalam pengembangan platform **Laboratorium Pengolahan Citra Digital (LPCD)**! Dokumen ini memandu tata cara kontribusi kode, standarisasi commit, dan pengujian.

---

## 1. Aturan Umum Kontribusi

1. **Bahasa Antarmuka & Dokumentasi**: Gunakan Bahasa Indonesia baku dan istilah teknis citra digital yang akurat untuk antarmuka pengguna, penjelasan teori, rumus, dan dokumentasi.
2. **Implementasi OpenCV**: Seluruh operasi wajib mengimplementasikan algoritma pengolahan citra nyata menggunakan Python (`cv2` dan `numpy`). Tidak diperbolehkan simulasi tampilan CSS semata.
3. **Format Citra Internal**: Wajib menggunakan representasi `uint8` dengan format warna RGB atau 2D Grayscale.
4. **Isolasi Modul**: Kembangkan operasi Anda hanya di dalam subdirektori modul yang ditugaskan (`orang_1`, `orang_2`, `orang_3`, `orang_4`).

---

## 2. Standar Penulisan Operasi Baru

Setiap operasi baru wajib mewarisi kelas dasar `BaseImageOperation` (`app/core/registry/base.py`) dengan melengkapi atribut:

```python
class MyCustomOperation(BaseImageOperation):
    id = "kategori_nama_operasi"
    name = "Nama Operasi Bahasa Indonesia"
    category = "Kategori yang Sesuai"
    owner = "Orang X"
    description = "Deskripsi singkat fungsi algoritma."
    status = OperationStatus.READY  # atau IN_DEVELOPMENT

    default_config = { ... }
    config_schema = [ ... ]
    explanation = AcademicExplanation( ... )

    def process(self, image: np.ndarray, config: Dict[str, Any]) -> np.ndarray:
        # Algoritma OpenCV Anda
        ...
```

---

## 3. Protokol Pengujian & Validasi

Sebelum mengajukan Pull Request (PR), pastikan seluruh pengujian Pytest lolos 100%:

```bash
cd backend
pytest -v
```

Dan pastikan build frontend React berhasil tanpa *warning* atau *type error*:

```bash
cd frontend
npm run build
```

---

## 4. Konvensi Commit Git

Gunakan format Conventional Commits:
- `feat(orang-X): implementasi algoritma X`
- `fix(engine): perbaikan penanganan border pada operasi Y`
- `docs: pembaruan panduan kontribusi dan dokumentasi API`
- `test: penambahan unit test untuk modul Z`
