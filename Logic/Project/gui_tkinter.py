"""
Antarmuka Pengguna (UI) - Tkinter Desktop GUI
Aplikasi GUI Desktop Pengolahan Citra Digital
Alur Pemrosesan: Pengguna memilih tombol fitur terlebih dahulu,
kemudian menekan tombol 'Process' agar output pemrosesan keluar.
Logika algoritma citra diimpor dari modul `image_processing.py`.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2  # Digunakan khusus sebagai driver pembaca hardware kamera (VideoCapture)

# Import fungsi logika dari modul image_processing
from image_processing import (
    process_thresholding,
    process_equalization,
    process_sketch,
    process_blur,
    process_grayscale,
    process_brightness,
    process_negative,
    process_mirroring,
    process_sharpening,
    process_edge_detection,
    process_sepia,
    process_emboss,
    process_erosion,
    process_dilation,
    draw_histogram
)

class ImageProcessingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("tk")
        self.root.geometry("1200x870")
        self.root.minsize(1000, 720)
        self.root.configure(bg="#F0F0F0")

        self.orig_image = None
        self.processed_image = None
        self.selected_action = None      # Fitur yang sedang dipilih oleh tombol
        self.active_camera_filter = None  # Fitur yang aktif diterapkan pada stream video
        self._resize_job = None
        self.filter_buttons = {}          # Dictionary penyimpan widget tombol filter

        # State Kamera
        self.cap = None
        self.is_camera_running = False
        self.camera_loop_id = None
        self.frame_counter = 0

        # Menu Bar
        menubar = tk.Menu(self.root)
        menubar.add_command(label="Open File", command=self.open_file)
        
        # Menu Kamera
        camera_menu = tk.Menu(menubar, tearoff=0)
        camera_menu.add_command(label="Mulai / Berhenti Live Kamera", command=self.toggle_camera)
        camera_menu.add_command(label="Ambil Foto dari Kamera", command=self.capture_photo)
        menubar.add_cascade(label="Kamera", menu=camera_menu)

        menubar.add_command(label="Save File", command=self.save_file)
        self.root.config(menu=menubar)

        self.setup_ui()

        # Deteksi resize jendela agar gambar otomatis membesar
        self.root.bind("<Configure>", self.on_window_resize)
        # Tangani penutupan jendela untuk melepas resource kamera dengan aman
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        # 1. Frame Atas: Gambar Asli & Gambar Hasil
        self.top_frame = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=(8, 2))

        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        self.lbl_orig = tk.Label(self.top_frame, bg="#FFFFFF", text="[ Gambar Asli / Live Kamera ]")
        self.lbl_orig.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        self.lbl_proc = tk.Label(self.top_frame, bg="#FFFFFF", text="[ Gambar Hasil / Live Filter ]")
        self.lbl_proc.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)

        # 2. Frame Tengah: Matplotlib Canvas Histogram Asli & Hasil
        hist_frame = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        hist_frame.pack(side=tk.TOP, fill=tk.X, expand=False, padx=8, pady=2)
        hist_frame.columnconfigure(0, weight=1)
        hist_frame.columnconfigure(1, weight=1)

        # Canvas Histogram Asli
        self.fig_orig, self.ax_orig = plt.subplots(figsize=(5.5, 1.6), dpi=85)
        self.fig_orig.patch.set_facecolor('#FFFFFF')
        self.canvas_orig = FigureCanvasTkAgg(self.fig_orig, master=hist_frame)
        self.canvas_orig.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=4, pady=2)

        # Canvas Histogram Hasil
        self.fig_proc, self.ax_proc = plt.subplots(figsize=(5.5, 1.6), dpi=85)
        self.fig_proc.patch.set_facecolor('#FFFFFF')
        self.canvas_proc = FigureCanvasTkAgg(self.fig_proc, master=hist_frame)
        self.canvas_proc.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=4, pady=2)

        self.clear_histograms()

        # 3. Status Bar di Bagian Bawah
        self.status_bar = tk.Label(self.root, text=" Status: Siap. Buka gambar atau nyalakan kamera.", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#E2E8F0", fg="#334155", font=("Segoe UI", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 4. Frame Kontrol Bawah: Tombol Fitur, Panel Slider Parameter, dan Tombol Aksi
        bottom_frame = tk.Frame(self.root, bg="#F0F0F0", bd=1, relief=tk.GROOVE)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=(4, 4))

        # Grid Tombol Fitur Citra (Kiri)
        grid_frame = tk.Frame(bottom_frame, bg="#F0F0F0")
        grid_frame.pack(side=tk.LEFT, padx=10, pady=4)

        # Konfigurasi 14 Tombol Fitur Citra
        buttons_config = [
            ("Tresholding", 0, 0), ("Blur", 1, 0), ("Negative", 2, 0), ("Edge Detection", 3, 0),
            ("Equalization", 0, 1), ("Grayscale", 1, 1), ("Mirroring", 2, 1), ("Sepia", 3, 1),
            ("Sketch", 0, 2), ("Brightness", 1, 2), ("Sharpening", 2, 2), ("Emboss", 3, 2),
            ("Erosion", 0, 3), ("Dilation", 1, 3)
        ]

        self.filter_buttons = {}
        for name, r, c in buttons_config:
            btn = tk.Button(
                grid_frame,
                text=name,
                width=12,
                relief=tk.RAISED,
                command=lambda n=name: self.select_filter(n)
            )
            btn.grid(row=r, column=c, padx=4, pady=2)
            self.filter_buttons[name] = btn

        # 5. Panel Slider Pengaturan Parameter Interaktif (Tengah)
        slider_frame = tk.LabelFrame(bottom_frame, text="⚙️ Kontrol Parameter", bg="#F0F0F0", font=("Segoe UI", 8, "bold"))
        slider_frame.pack(side=tk.LEFT, padx=12, pady=2, fill=tk.Y)

        # Slider Threshold (0 - 255)
        f_thresh = tk.Frame(slider_frame, bg="#F0F0F0")
        f_thresh.pack(fill=tk.X, padx=6, pady=1)
        tk.Label(f_thresh, text="Threshold:", width=9, anchor=tk.W, bg="#F0F0F0", font=("Segoe UI", 8)).pack(side=tk.LEFT)
        self.slider_thresh = tk.Scale(f_thresh, from_=0, to=255, orient=tk.HORIZONTAL, length=140, showvalue=1, bg="#F0F0F0", command=self.on_slider_change)
        self.slider_thresh.set(127)
        self.slider_thresh.pack(side=tk.RIGHT)

        # Slider Brightness (-100 - +100)
        f_bright = tk.Frame(slider_frame, bg="#F0F0F0")
        f_bright.pack(fill=tk.X, padx=6, pady=1)
        tk.Label(f_bright, text="Brightness:", width=9, anchor=tk.W, bg="#F0F0F0", font=("Segoe UI", 8)).pack(side=tk.LEFT)
        self.slider_bright = tk.Scale(f_bright, from_=-100, to=100, orient=tk.HORIZONTAL, length=140, showvalue=1, bg="#F0F0F0", command=self.on_slider_change)
        self.slider_bright.set(50)
        self.slider_bright.pack(side=tk.RIGHT)

        # Slider Blur Radius (3 - 21)
        f_blur = tk.Frame(slider_frame, bg="#F0F0F0")
        f_blur.pack(fill=tk.X, padx=6, pady=1)
        tk.Label(f_blur, text="Blur Radius:", width=9, anchor=tk.W, bg="#F0F0F0", font=("Segoe UI", 8)).pack(side=tk.LEFT)
        self.slider_blur = tk.Scale(f_blur, from_=3, to=21, orient=tk.HORIZONTAL, length=140, showvalue=1, bg="#F0F0F0", command=self.on_slider_change)
        self.slider_blur.set(7)
        self.slider_blur.pack(side=tk.RIGHT)

        # Slider Edge Threshold (20 - 200)
        f_edge = tk.Frame(slider_frame, bg="#F0F0F0")
        f_edge.pack(fill=tk.X, padx=6, pady=1)
        tk.Label(f_edge, text="Edge Thresh:", width=9, anchor=tk.W, bg="#F0F0F0", font=("Segoe UI", 8)).pack(side=tk.LEFT)
        self.slider_edge = tk.Scale(f_edge, from_=20, to=200, orient=tk.HORIZONTAL, length=140, showvalue=1, bg="#F0F0F0", command=self.on_slider_change)
        self.slider_edge.set(100)
        self.slider_edge.pack(side=tk.RIGHT)

        # 6. Tombol Aksi Kamera & Kontrol (Kanan)
        action_frame = tk.Frame(bottom_frame, bg="#F0F0F0")
        action_frame.pack(side=tk.RIGHT, padx=15, pady=4)

        self.btn_camera = tk.Button(action_frame, text="📷 Live Kamera", width=13, bg="#E0F2FE", fg="#0369A1", font=("Segoe UI", 9, "bold"), command=self.toggle_camera)
        self.btn_camera.pack(pady=2)

        self.btn_capture = tk.Button(action_frame, text="📸 Ambil Foto", width=13, command=self.capture_photo)
        self.btn_capture.pack(pady=2)

        # Tombol Process dengan visual menonjol agar jelas terlihat
        self.btn_proc = tk.Button(action_frame, text="▶ Process", width=13, bg="#DCFCE7", fg="#15803D", font=("Segoe UI", 9, "bold"), command=self.process_selected)
        self.btn_proc.pack(pady=2)

        btn_close = tk.Button(action_frame, text="Close", width=13, command=self.on_closing)
        btn_close.pack(pady=2)

    def set_status(self, text):
        """Memperbarui teks status bar di bagian bawah."""
        self.status_bar.config(text=f" Status: {text}")

    def select_filter(self, filter_name):
        """
        Ketika tombol fitur diklik:
        Hanya memilih/menandai fitur (highlight tombol), TIDAK langsung memproses output.
        Output baru akan muncul saat tombol 'Process' ditekan.
        """
        self.selected_action = filter_name

        # Berikan efek visual penanda tombol yang sedang aktif dipilih
        for name, btn in self.filter_buttons.items():
            if name == filter_name:
                btn.config(bg="#0284C7", fg="#FFFFFF", relief=tk.SUNKEN)  # Highlight biru aktif
            else:
                btn.config(bg="#F0F0F0", fg="#000000", relief=tk.RAISED)  # Normal

        self.set_status(f"Fitur [{filter_name}] dipilih. Klik tombol '▶ Process' untuk melihat hasil.")

    def process_selected(self):
        """
        Mengeksekusi pemrosesan citra HANYA setelah tombol 'Process' ditekan.
        """
        if self.orig_image is None and not self.is_camera_running:
            messagebox.showwarning("Peringatan", "Silakan buka gambar ('Open File') atau nyalakan kamera ('Live Kamera') terlebih dahulu.")
            return

        if not self.selected_action:
            messagebox.showinfo("Pilih Fitur", "Silakan klik salah satu tombol fitur terlebih dahulu, lalu klik tombol 'Process'.")
            return

        # Jika sedang dalam mode Live Kamera, aktifkan filter ke video streaming realtime
        if self.is_camera_running:
            self.active_camera_filter = self.selected_action
            self.set_status(f"Live Kamera — Memproses [{self.selected_action}] secara realtime.")
            return

        # Pemrosesan gambar statis
        self.set_status(f"Memproses [{self.selected_action}]...")
        self.root.update_idletasks()

        self.processed_image = self.compute_filter(self.orig_image, self.selected_action)
        self.display_image(self.processed_image, self.lbl_proc)
        draw_histogram(self.processed_image, self.ax_proc)
        self.canvas_proc.draw()
        self.set_status(f"Pemrosesan [{self.selected_action}] selesai.")

    def on_slider_change(self, val):
        """Saat slider parameter digeser, ingatkan pengguna untuk menekan 'Process'."""
        if not self.is_camera_running and self.orig_image is not None and self.selected_action:
            self.set_status(f"Parameter diubah. Klik tombol '▶ Process' untuk menerapkan ke [{self.selected_action}].")

    def get_display_target_size(self):
        """Menghitung batas ukuran gambar dinamis agar tampil besar dan proporsional."""
        self.root.update_idletasks()
        lbl_w = self.lbl_orig.winfo_width()
        lbl_h = self.lbl_orig.winfo_height()

        if lbl_w <= 150 or lbl_h <= 150:
            win_w = max(1100, self.root.winfo_width())
            win_h = max(780, self.root.winfo_height())
            target_w = (win_w // 2) - 25
            target_h = int(win_h * 0.48)
        else:
            target_w = lbl_w - 15
            target_h = lbl_h - 15

        return max(550, target_w), max(380, target_h)

    def display_image(self, img_array, label_widget):
        """Merender gambar dengan skala besar proporsional sesuai frame tampilan."""
        h, w = img_array.shape[:2]
        max_w, max_h = self.get_display_target_size()
        
        scale = min(max_w / w, max_h / h)
        new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale))

        if len(img_array.shape) == 2:
            pil_img = Image.fromarray(img_array)
        else:
            pil_img = Image.fromarray(img_array.astype(np.uint8))
        
        pil_img_resized = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(pil_img_resized)
        label_widget.config(image=tk_img, text="")
        label_widget.image = tk_img

    def on_window_resize(self, event):
        """Saat ukuran jendela diubah / dimaksimalkan, perbarui ukuran gambar."""
        if event.widget == self.root and self.orig_image is not None and not self.is_camera_running:
            if self._resize_job:
                self.root.after_cancel(self._resize_job)
            self._resize_job = self.root.after(150, self.refresh_display)

    def refresh_display(self):
        """Menampilkan kembali gambar dengan dimensi frame baru."""
        if self.orig_image is not None:
            self.display_image(self.orig_image, self.lbl_orig)
        if self.processed_image is not None:
            self.display_image(self.processed_image, self.lbl_proc)

    def open_file(self):
        if self.is_camera_running:
            self.stop_camera()

        file_path = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"), ("All files", "*.*")]
        )
        if file_path:
            pil_img = Image.open(file_path).convert('RGB')
            self.orig_image = np.array(pil_img)
            self.processed_image = self.orig_image.copy()
            self.selected_action = None
            self.active_camera_filter = None

            # Reset warna tombol filter ke normal
            for btn in self.filter_buttons.values():
                btn.config(bg="#F0F0F0", fg="#000000", relief=tk.RAISED)

            self.display_image(self.orig_image, self.lbl_orig)
            self.display_image(self.processed_image, self.lbl_proc)
            
            draw_histogram(self.orig_image, self.ax_orig)
            self.canvas_orig.draw()
            draw_histogram(self.processed_image, self.ax_proc)
            self.canvas_proc.draw()

            h, w = self.orig_image.shape[:2]
            self.set_status(f"Gambar berhasil dibuka ({w}x{h} piksel). Pilih fitur lalu klik '▶ Process'.")

    # ==========================================================================
    # MANAJEMEN INPUT KAMERA & REALTIME STREAMING
    # ==========================================================================
    def toggle_camera(self):
        """Menghidupkan atau mematikan stream realtime dari kamera webcam."""
        if self.is_camera_running:
            self.stop_camera()
        else:
            self.start_camera()

    def start_camera(self):
        """Menginisialisasi perangkat webcam dan memulai loop realtime."""
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
                
            if not self.cap.isOpened():
                messagebox.showerror("Error Kamera", "Tidak dapat mendeteksi atau membuka webcam pada komputer Anda.")
                self.set_status("Gagal mendeteksi webcam.")
                return

            self.is_camera_running = True
            self.active_camera_filter = None
            self.btn_camera.config(text="⏹ Stop Kamera", bg="#FEE2E2", fg="#B91C1C")
            self.set_status("Live Kamera Aktif. Pilih fitur lalu klik '▶ Process'.")
            self.update_camera_feed()

        except Exception as e:
            messagebox.showerror("Error Kamera", f"Terjadi kesalahan saat membuka kamera: {str(e)}")
            self.set_status("Error saat inisialisasi kamera.")

    def stop_camera(self):
        """Menghentikan pembacaan webcam dan melepas hardware kamera."""
        self.is_camera_running = False
        self.active_camera_filter = None
        if self.camera_loop_id:
            self.root.after_cancel(self.camera_loop_id)
            self.camera_loop_id = None

        if self.cap is not None:
            self.cap.release()
            self.cap = None

        self.btn_camera.config(text="📷 Live Kamera", bg="#E0F2FE", fg="#0369A1")
        self.set_status("Kamera dihentikan.")

    def capture_photo(self):
        """Menangkap frame saat ini dari kamera sebagai foto statis."""
        if not self.is_camera_running:
            try:
                temp_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                if not temp_cap.isOpened():
                    temp_cap = cv2.VideoCapture(0)
                ret, frame = temp_cap.read()
                temp_cap.release()
                if ret:
                    # BGR ke RGB + Flip horizontal
                    frame_rgb = frame[:, ::-1, ::-1].copy()

                    self.orig_image = frame_rgb
                    self.processed_image = self.orig_image.copy()
                    self.selected_action = None
                    self.active_camera_filter = None

                    for btn in self.filter_buttons.values():
                        btn.config(bg="#F0F0F0", fg="#000000", relief=tk.RAISED)

                    self.display_image(self.orig_image, self.lbl_orig)
                    self.display_image(self.processed_image, self.lbl_proc)
                    draw_histogram(self.orig_image, self.ax_orig)
                    self.canvas_orig.draw()
                    draw_histogram(self.processed_image, self.ax_proc)
                    self.canvas_proc.draw()
                    self.set_status("Foto berhasil diambil dari kamera! Pilih fitur lalu klik '▶ Process'.")
                    messagebox.showinfo("Berhasil", "Foto berhasil diambil dari kamera!")
                else:
                    messagebox.showwarning("Peringatan", "Gagal membaca gambar dari kamera.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengambil foto: {str(e)}")
            return

        # Jika sedang live kamera, freeze frame sekarang
        self.stop_camera()
        self.set_status("Foto berhasil ditangkap dari kamera. Pilih fitur lalu klik '▶ Process'.")
        messagebox.showinfo("Foto Tertangkap", "Foto berhasil ditangkap dari kamera! Silakan pilih fitur lalu klik '▶ Process'.")

    def update_camera_feed(self):
        """Loop eksekusi video realtime: membaca frame dan menerapkan filter HANYA jika sudah di-Process."""
        if not self.is_camera_running or self.cap is None:
            return

        ret, frame_bgr = self.cap.read()
        if ret:
            # BGR ke RGB + Flip horizontal
            frame_rgb = frame_bgr[:, ::-1, ::-1].copy()
            self.orig_image = frame_rgb

            # Terapkan filter manual aktif ke video realtime HANYA jika sudah ditekan Process
            if self.active_camera_filter:
                self.processed_image = self.compute_filter(frame_rgb, self.active_camera_filter)
            else:
                self.processed_image = frame_rgb.copy()

            self.display_image(self.orig_image, self.lbl_orig)
            self.display_image(self.processed_image, self.lbl_proc)

            # Update histogram periodik setiap 5 frame agar FPS tetap tinggi & halus
            self.frame_counter += 1
            if self.frame_counter % 5 == 0:
                draw_histogram(self.orig_image, self.ax_orig)
                self.canvas_orig.draw_idle()
                draw_histogram(self.processed_image, self.ax_proc)
                self.canvas_proc.draw_idle()

        self.camera_loop_id = self.root.after(30, self.update_camera_feed)

    def compute_filter(self, img, filter_name):
        """Menjalankan fungsi pengolahan citra manual berdasarkan nama filter dan slider parameter."""
        thresh_val = self.slider_thresh.get()
        bright_val = self.slider_bright.get()
        blur_val = self.slider_blur.get()
        edge_val = self.slider_edge.get()

        if filter_name == "Tresholding":
            return process_thresholding(img, thresh_val)
        elif filter_name == "Equalization":
            return process_equalization(img)
        elif filter_name == "Sketch":
            return process_sketch(img)
        elif filter_name == "Blur":
            return process_blur(img, blur_val)
        elif filter_name == "Grayscale":
            return process_grayscale(img)
        elif filter_name == "Brightness":
            return process_brightness(img, bright_val)
        elif filter_name == "Negative":
            return process_negative(img)
        elif filter_name == "Mirroring":
            return process_mirroring(img)
        elif filter_name == "Sharpening":
            return process_sharpening(img)
        elif filter_name == "Edge Detection":
            return process_edge_detection(img, edge_val)
        elif filter_name == "Sepia":
            return process_sepia(img)
        elif filter_name == "Emboss":
            return process_emboss(img)
        elif filter_name == "Erosion":
            return process_erosion(img)
        elif filter_name == "Dilation":
            return process_dilation(img)
        return img

    def save_file(self):
        if self.processed_image is None:
            messagebox.showwarning("Peringatan", "Belum ada gambar hasil untuk disimpan!")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            if len(self.processed_image.shape) == 2:
                img_to_save = Image.fromarray(self.processed_image)
            else:
                img_to_save = Image.fromarray(self.processed_image.astype(np.uint8))
            img_to_save.save(file_path)
            self.set_status("Gambar berhasil disimpan.")
            messagebox.showinfo("Berhasil", "Gambar berhasil disimpan!")

    def clear_histograms(self):
        self.ax_orig.clear()
        self.ax_orig.set_yticks([])
        self.canvas_orig.draw()
        self.ax_proc.clear()
        self.ax_proc.set_yticks([])
        self.canvas_proc.draw()

    def on_closing(self):
        """Membersihkan dan melepaskan koneksi webcam saat jendela ditutup."""
        self.stop_camera()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingGUI(root)
    root.mainloop()
