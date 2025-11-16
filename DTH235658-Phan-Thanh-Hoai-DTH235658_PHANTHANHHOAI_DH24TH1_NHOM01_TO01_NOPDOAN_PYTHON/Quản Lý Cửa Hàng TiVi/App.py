import tkinter as tk
from tkinter import messagebox
import ctypes
import pyodbc
import os
import sys
from PIL import Image, ImageTk

import frmTongQuan as tq
import frmBanHangVaHoaDon as bhvhd
import frmHeThong as ht
import frmQuanLyKhachHang as kh
import frmQuanLyNhanVien as nv
import frmThongKeVaBaoCao as tkvbc
import frmQuanLySanPham as sp
import frmNhapHangVaPhieuNhap as nhvpn
import frmLogin

# Hien: LAPTOP-IFECMD9V
# Hoai: DESKTOP-LJVV0KQ

# === BẢNG MÀU ===
PRIMARY_COLOR = "#0D47A1"
SECONDARY_COLOR = "#1565C0"
ACCENT_COLOR = "#42A5F5"
HIGHLIGHT_COLOR = "#BBDEFB"
TEXT_COLOR = "white"

# === LÀM NÉT GIAO DIỆN ===
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


class App(tk.Tk):
    # === CỬA SỐ CHÍNH ===
    def __init__(self, user):
        super().__init__()
        self.center_window(1500, 885)
        self.resizable(True, True)
        self.title("HỆ THỐNG QUẢN LÝ CỬA HÀNG TIVI")
        self.user = user

        # === CHUỖI KẾT NỐI ===
        try:
            self.conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=LAPTOP-IFECMD9V;"
                "DATABASE=QLTV;"
                "Trusted_Connection=yes;"
            )
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối CSDL:")
            self.destroy()
            return

        # === LẤY ĐƯỜNG DẪN CHO ẢNH ===
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.image_dir = os.path.join(base_dir, "images")

        icon_path = os.path.join(self.image_dir, "icon_tivi.ico")
        self.iconbitmap(icon_path)

        # Tạo dictionary lưu các frame nội dung
        self.frames = {}

        # --- Sidebar (Menu bên trái) ---
        self.TaoSidleBar()

        # Vùng nội dung chính
        container = tk.Frame(self, bg="white")
        container.pack(side="right", fill="both", expand=True)
        self.container = container

        self.frame_classes = {
            "TongQuan": tq.TongQuan,
            "QuanLySanPham": sp.QuanLySanPham,
            "QuanLyKhachHang": kh.QuanLyKhachHang,
            "QuanLyNhanVien": nv.QuanLyNhanVien,
            "BanHangVaHoaDon": bhvhd.BanHangVaHoaDon,
            "NhapHangVaPhieuNhap": nhvpn.NhapHangVaPhieuNhap,
            "ThongKeVaBaoCao": tkvbc.ThongKeVaBaoCao,
            "HeThong": ht.HeThong,
        }

        # Cho phép container giãn đầy vùng hiển thị
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Hiển thị trang đầu tiên
        if self.user == "admin":
            self.HienThiFrame("QuanLySanPham")
        else:
            self.HienThiFrame("QuanLyNhanVien")
        # === Đóng kết nối khi thoát app ===
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ==== HÀM CANH GIỮA CỬA SỔ ====
    def center_window(self, w=1500, h=885):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def TaoSidleBar(self):
        # ==== SIDEBAR BÊN TRÁI====
        pnlGiaoDien = tk.Frame(self, bg=SECONDARY_COLOR, width=250)
        pnlGiaoDien.pack(side="left", fill="y")

        # # Ảnh avatar (placeholder)
        avatar_path = os.path.join(self.image_dir, "tivi_user.png")
        original_avatar = Image.open(avatar_path)
        resized_avatar = original_avatar.resize((80, 80), Image.Resampling.LANCZOS)
        self.avatar_tk = ImageTk.PhotoImage(resized_avatar)

        lbl_avatar = tk.Label(pnlGiaoDien, image=self.avatar_tk, bg=SECONDARY_COLOR)
        lbl_avatar.pack(pady=(20, 5))

        lbl_XinChao = tk.Label(
            pnlGiaoDien,
            text=f"Xin chào {self.user}",
            bg=SECONDARY_COLOR,
            fg="white",
            font=("Segoe UI", 12, "bold"),
        ).pack()

        if self.user == "admin":
            # Danh mục bên trái
            btn_tongquan = tk.Button(
                pnlGiaoDien,
                text="🏠 Tổng quan",
                command=lambda: self.HienThiFrame("TongQuan"),
                **self.DinhDangNut(),
            )
            btn_tongquan.pack(fill="x")

        btn_quanlysanpham = tk.Button(
            pnlGiaoDien,
            text="📦 Quản lý Sản phẩm",
            command=lambda: self.HienThiFrame("QuanLySanPham"),
            **self.DinhDangNut(),
        )
        btn_quanlysanpham.pack(fill="x")

        btn_quanlykhachhang = tk.Button(
            pnlGiaoDien,
            text="👥 Quản lý Khách hàng",
            command=lambda: self.HienThiFrame("QuanLyKhachHang"),
            **self.DinhDangNut(),
        )
        btn_quanlykhachhang.pack(fill="x")

        btn_quanlynhanvien = tk.Button(
            pnlGiaoDien,
            text="🧑‍💼 Quản lý Nhân viên",
            command=lambda: self.HienThiFrame("QuanLyNhanVien"),
            **self.DinhDangNut(),
        )
        btn_quanlynhanvien.pack(fill="x")

        btn_banhangvahoadon = tk.Button(
            pnlGiaoDien,
            text="💰 Bán hàng & Hóa đơn",
            command=lambda: self.HienThiFrame("BanHangVaHoaDon"),
            **self.DinhDangNut(),
        )
        btn_banhangvahoadon.pack(fill="x")

        if self.user == "admin":

            btn_nhaphangvaphieunhap = tk.Button(
                pnlGiaoDien,
                text="📦 Nhập hàng & Phiếu nhập",
                command=lambda: self.HienThiFrame("NhapHangVaPhieuNhap"),
                **self.DinhDangNut(),
            )
            btn_nhaphangvaphieunhap.pack(fill="x")

            btn_thongkevabaocao = tk.Button(
                pnlGiaoDien,
                text="🧾 Thống kê & Báo cáo",
                command=lambda: self.HienThiFrame("ThongKeVaBaoCao"),
                **self.DinhDangNut(),
            )
            btn_thongkevabaocao.pack(fill="x")

        btn_hethong = tk.Button(
            pnlGiaoDien,
            text="⚙️ Hệ thống",
            command=lambda: self.HienThiFrame("HeThong"),
            **self.DinhDangNut(),
        )
        btn_hethong.pack(fill="x")

        btn_dangxuat = tk.Button(
            pnlGiaoDien,
            text="🚪Đăng xuất",
            command=self.dang_xuat,
            **self.DinhDangNut(),
        )
        btn_dangxuat.pack(fill="x")

    def DinhDangNut(self):
        return {
            "bg": ACCENT_COLOR,
            "fg": "white",
            "font": ("Arial", 12),
            "bd": 0,
            "relief": "flat",
            "anchor": "w",
            "padx": 20,
            "pady": 15,
        }

    def load_form(self, page_name):
        frame = self.frames.get(page_name)
        if frame and hasattr(frame, "load_data"):
            try:
                frame.load_data()
            except Exception as e:
                print(f"Lỗi khi load dữ liệu cho {page_name}: {e}")



    def HienThiFrame(self, page_name):
        # Tạo frame nếu nó chưa tồn tại
        if page_name not in self.frames:
            FrameClass = self.frame_classes[page_name]
            frame = FrameClass(
                parent=self.container, controller=self, conn=self.conn, user=self.user
            )
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #  Lấy frame đã được tạo/lưu trữ
        frame_to_show = self.frames[page_name]

        try:
            frame_to_show.load_data()
        except AttributeError:
            # Bỏ qua nếu frame không có hàm refresh_data
            pass
        except Exception as e:
            # Báo lỗi nếu hàm load_data chạy bị lỗi
            print(f"Lỗi khi làm mới {page_name}: {e}")

        #  Hiển thị frame lên trên cùng
        frame_to_show.tkraise()

    # ====== Đóng kết nối khi thoát ======
    def on_close(self):
        try:
            if hasattr(self, "conn") and self.conn:
                self.conn.close()
                print("Kết nối SQL đã được đóng.")
        except Exception as e:
            print("Lỗi khi đóng kết nối:", e)
        finally:
            self.destroy()

    def dang_xuat(self):
        if messagebox.askyesno(
            "Xác nhận đăng xuất", "Bạn có chắc chắn muốn đăng xuất?"
        ):
            # Đóng kết nối SQL
            try:
                if hasattr(self, "conn") and self.conn:
                    self.conn.close()
                    print("Kết nối SQL đã được đóng (do đăng xuất).")
            except Exception as e:
                print("Lỗi khi đóng kết nối:", e)

            self.destroy()
            login_window = frmLogin.Login()
            login_window.mainloop()
