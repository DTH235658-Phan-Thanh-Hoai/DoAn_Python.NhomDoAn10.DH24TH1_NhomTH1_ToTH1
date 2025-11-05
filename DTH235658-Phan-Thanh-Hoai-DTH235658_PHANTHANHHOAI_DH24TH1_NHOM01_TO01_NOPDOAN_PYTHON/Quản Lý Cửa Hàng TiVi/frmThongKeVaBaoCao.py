import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

import tabThongKeDoanhThu as tkdt
import tabBaoCaoSanPham as bcsp

# === BẢNG MÀU ===
PRIMARY_COLOR = "#0D47A1"    
SECONDARY_COLOR = "#1565C0" 
ACCENT_COLOR = "#42A5F5"     
HIGHLIGHT_COLOR = "#BBDEFB" 
TEXT_COLOR = "white" 

#=== Tạo class Thống Kê và Báo Cáo
class ThongKeVaBaoCao(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent, bg="white")

        # === CHUỖI KẾT NỐI  ====
        self.conn = conn

        # === TITLE ===
        lbl_title = tk.Label(self, text="THỐNG KÊ & BÁO CÁO", font=("Segoe UI", 16, "bold"), bg="white", fg="#0D47A1")
        lbl_title.pack()

        # === Tab control ===
        tab_control = ttk.Notebook(self)
        tab_control.pack(fill="both", expand=True, padx=20, pady=10)

        tab_doanhthu = tkdt.tabThongKeDoanhThu(tab_control, conn)
        tab_sanpham = bcsp.tabBaoCaoSanPham(tab_control, conn)

        tab_control.add(tab_doanhthu, text="💹 Thống kê Doanh thu")
        tab_control.add(tab_sanpham, text="📊 Báo cáo Sản phẩm")
