import tkinter as tk
from tkinter import ttk, messagebox
import tabNhapHang as nh
import tabPhieuNhapHang as pnh
import pyodbc

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

        self.tab_phieunhap = pnh.tabPhieuNhapHang(tab_control, conn)
        self.tab_nhaphang = nh.tabNhapHang(tab_control, conn, self.tab_phieunhap) 

        tab_control.add(self.tab_nhaphang, text="📦 Nhập hàng")
        tab_control.add(self.tab_phieunhap, text="🧾 Danh sách Phiếu nhập")

    # Hàm làm mới tab khi click vào
    def load_data(self):
        try:
            self.tab_phieunhap.load_phieu_nhap()
            
        except Exception as e:
            messagebox.showerror("Lỗi khi làm mới dữ liệu: " + str(e))
