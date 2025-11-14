import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

import tabThongKeDoanhThu as tkdt
import tabBaoCaoSanPham as bcsp

#=== Tạo class Thống Kê và Báo Cáo
class ThongKeVaBaoCao(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent, bg="white")

        # === CHUỖI KẾT NỐI  ====
        self.conn = conn

        self.controller = controller

        # === TITLE ===
        lbl_title = tk.Label(self, text="THỐNG KÊ & BÁO CÁO", font=("Segoe UI", 16, "bold"), bg="white", fg="#0D47A1")
        lbl_title.pack()

        # === Tab control ===
        tab_control = ttk.Notebook(self)
        tab_control.pack(fill="both", expand=True, padx=20, pady=10)

        #  KHỞI TẠO VÀ LƯU THAM CHIẾU VÀO self.tab_doanhthu_ref
        self.tab_doanhthu = tkdt.tabThongKeDoanhThu(tab_control, conn)
        self.tab_baocao  = bcsp.tabBaoCaoSanPham(tab_control, conn)

        tab_control.add(self.tab_doanhthu, text="💹 Thống kê Doanh thu")
        tab_control.add(self.tab_baocao , text="📊 Báo cáo Sản phẩm")

    # Hàm làm mới tab khi click vào
    def load_data(self):
        try:
            self.tab_doanhthu.thongke_doanhthu_tatca()
            self.tab_baocao.load_baocao_all()
            
        except Exception as e:
            messagebox.showerror("Lỗi khi làm mới tab con: " + str(e))