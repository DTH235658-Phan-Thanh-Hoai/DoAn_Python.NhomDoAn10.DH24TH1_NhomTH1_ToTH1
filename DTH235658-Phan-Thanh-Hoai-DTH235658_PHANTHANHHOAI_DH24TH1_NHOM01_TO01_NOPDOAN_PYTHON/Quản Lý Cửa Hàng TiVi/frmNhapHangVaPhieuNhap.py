import tkinter as tk
from tkinter import ttk, messagebox
import tabNhapHang as nh
import tabPhieuNhapHang as pnh
import pyodbc

# === BẢNG MÀU ===
PRIMARY_COLOR = "#0D47A1"    
SECONDARY_COLOR = "#1565C0" 
ACCENT_COLOR = "#42A5F5"     
HIGHLIGHT_COLOR = "#BBDEFB" 
TEXT_COLOR = "white" 

#=== Tạo class Bán Hàng và Hóa Đơn
class NhapHangVaPhieuNhap(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent, bg="white")
        self.conn = conn

        # === TITLE ===
        lbl_title = tk.Label(self, text="NHẬP HÀNG & PHIẾU NHẬP", font=("Segoe UI", 16, "bold"), bg="white", fg="#0D47A1")
        lbl_title.pack()

        # === Tạo tab control ===
        tab_control = ttk.Notebook(self)
        tab_control.pack(fill="both", expand=True, padx=20, pady=10)

        tab_phieunhap = pnh.tabPhieuNhapHang(tab_control, conn)
        tab_nhaphang = nh.tabNhapHang(tab_control, conn, tab_phieunhap) 

        tab_control.add(tab_nhaphang, text="📦 Nhập hàng")
        tab_control.add(tab_phieunhap, text="🧾 Danh sách Phiếu nhập")
