import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

import tabTivi as tv
import tabHangSanXuat as hsx
import tabNhaCungCap as ncc
import tabBaoHanh as bh

# === Tạo class Quản Lý Sản Phẩm ===
class QuanLySanPham(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent, bg="white")

        # === CHUỖI KẾT NỐI  ====
        self.conn = conn

        self.controller = controller
        self.user = user

        # === TITLE ===
        lbl_title = tk.Label(self, text="QUẢN LÝ SẢN PHẨM", font=("Segoe UI", 16, "bold"), bg="white", fg="#0D47A1")
        lbl_title.pack()

        # === Tạo Tab Control ===
        tab_control = ttk.Notebook(self)
        tab_control.pack(fill="both", expand=True, padx=20, pady=10)

        # === Các tab con ===
        self.tab_tivi = tv.tabTivi(tab_control, conn, self.user, self.controller)
        self.tab_hang = hsx.tabHangSanXuat(tab_control, conn, self.load_data)
        self.tab_nhacungcap = ncc.tabNhaCungCap(tab_control, conn, self.controller)
        self.tab_bh = bh.tabBaoHanh(tab_control, conn, self.user)
        
        tab_control.add(self.tab_tivi, text="📺 Tivi")
        # Thêm vào notebook
        if(user == "admin"):
            tab_control.add(self.tab_hang, text="🏭 Hãng sản xuất")
            tab_control.add(self.tab_nhacungcap, text="🤝 Nhà cung cấp")
            
        tab_control.add(self.tab_bh, text="🧾 Bảo hành")

    # Hàm làm mới tab khi click vào
    def load_data(self):
        try:
            self.tab_tivi.hienthi_dulieu()
            self.tab_tivi.load_hang_san_xuat()

            self.tab_hang.hienthi_dulieu()
            self.tab_nhacungcap.hienthi_dulieu()
            self.tab_bh.hienthi_dulieu()
            self.tab_bh.hien_thi_du_lieu_cthd()
            
        except Exception as e:
            messagebox.showerror("Lỗi khi load tab con: " + str(e))
