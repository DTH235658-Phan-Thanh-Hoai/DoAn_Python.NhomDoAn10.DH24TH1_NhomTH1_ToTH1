import tkinter as tk
from tkinter import ttk, messagebox
import tabBanHang as bh
import tabHoaDon as hd
import pyodbc

# === BẢNG MÀU ===
PRIMARY_COLOR = "#0D47A1"    
SECONDARY_COLOR = "#1565C0" 
ACCENT_COLOR = "#42A5F5"     
HIGHLIGHT_COLOR = "#BBDEFB" 
TEXT_COLOR = "white" 

#=== Tạo class Bán Hàng và Hóa Đơn
class BanHangVaHoaDon(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent, bg="white")

        # === CHUỖI NÉT NỐI ===
        self.conn = conn

        # === LƯU THAM CHIẾU CONTROLLER ===
        self.controller = controller

        # === TITLE ===
        lbl_title = tk.Label(self, text="BÁN HÀNG & HÓA ĐƠN", font=("Segoe UI", 16, "bold"), bg="white", fg="#0D47A1")
        lbl_title.pack()

        # === Tạo tab control ===
        tab_control = ttk.Notebook(self)
        tab_control.pack(fill="both", expand=True, padx=20, pady=10)

        tab_hoadon = hd.tabHoaDon(tab_control, conn, controller = self.controller)
        tab_banhang = bh.tabBanHang(tab_control, conn, tab_hoadon)
        

        tab_control.add(tab_banhang, text="🛒 Bán hàng")
        tab_control.add(tab_hoadon, text="🧾 Danh sách Hóa đơn")
