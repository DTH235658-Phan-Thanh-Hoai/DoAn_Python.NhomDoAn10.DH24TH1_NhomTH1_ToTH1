import tkinter as tk
from tkinter import ttk, messagebox
import tabBanHang as bh
import tabHoaDon as hd
import pyodbc

#=== Tạo class Bán Hàng và Hóa Đơn
class BanHangVaHoaDon(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent, bg="white")

        # === CHUỖI NÉT NỐI ===
        self.conn = conn

        # === LẤY USER ===
        self.user = user

        # === LƯU THAM CHIẾU CONTROLLER ===
        self.controller = controller

        # === TITLE ===
        lbl_title = tk.Label(self, text="BÁN HÀNG & HÓA ĐƠN", font=("Segoe UI", 16, "bold"), bg="white", fg="#0D47A1")
        lbl_title.pack()

        # === Tạo tab control ===
        tab_control = ttk.Notebook(self)
        tab_control.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_hoadon = hd.tabHoaDon(tab_control, conn, user, self.controller)
        self.tab_banhang = bh.tabBanHang(tab_control, conn, user, self.tab_hoadon)

        tab_control.add(self.tab_banhang, text="🛒 Bán hàng")
        tab_control.add(self.tab_hoadon, text="🧾 Danh sách Hóa đơn")
        

    # Hàm làm mới tab khi click vào
    def load_data(self):
        try:
            self.tab_hoadon.load_hoa_don()
            
            self.tab_banhang.load_Combobox()
            
        except Exception as e:
            messagebox.showerror("Lỗi khi làm mới dữ liệu: " + str(e))