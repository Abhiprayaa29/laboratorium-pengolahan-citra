"""
Entry Point Utama Aplikasi Pengolahan Citra Digital (Desktop GUI)
Menjalankan antarmuka Tkinter dari gui_tkinter.py
"""

import tkinter as tk
from gui_tkinter import ImageProcessingGUI

if __name__ == "__main__":
    # Optimalisasi ketajaman tampilan pada layar resolusi tinggi (Windows High-DPI)
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    root = tk.Tk()
    app = ImageProcessingGUI(root)
    root.mainloop()

