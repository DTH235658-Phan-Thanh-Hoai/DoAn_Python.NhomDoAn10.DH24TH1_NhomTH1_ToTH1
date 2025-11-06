import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

import tabTivi as tv
import tabHangSanXuat as hsx
import tabNhaCungCap as ncc
import tabBaoHanh as bh

# === BẢNG MÀU ===
PRIMARY_COLOR = "#0D47A1"
SECONDARY_COLOR = "#1565C0"
ACCENT_COLOR = "#42A5F5"
HIGHLIGHT_COLOR = "#BBDEFB"
TEXT_COLOR = "white"


# === Tạo class Quản Lý Sản Phẩm ===
class QuanLySanPham(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent, bg="white")

        # === CHUỖI KẾT NỐI  ====
        self.conn = conn

        # === TITLE ===
        lbl_title = tk.Label(
            self,
            text="QUẢN LÝ SẢN PHẨM",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#0D47A1",
        )
        lbl_title.pack()

        # === Tạo Tab Control ===
        tab_control = ttk.Notebook(self)
        tab_control.pack(fill="both", expand=True, padx=20, pady=10)

        # === Các tab con ===
        tab_tivi = tv.tabTivi(tab_control, conn)
        tab_hang = hsx.tabHangSanXuat(tab_control, conn)
        tab_nhacungcap = ncc.tabNhaCungCap(tab_control, conn)
        tab_bh = bh.tabBaoHanh(tab_control, conn)

        # Thêm vào notebook
        tab_control.add(tab_tivi, text="📺 Tivi")
        tab_control.add(tab_hang, text="🏭 Hãng sản xuất")
        tab_control.add(tab_nhacungcap, text="🤝 Nhà cung cấp")
        tab_control.add(tab_bh, text="🧾 Bảo hành")
