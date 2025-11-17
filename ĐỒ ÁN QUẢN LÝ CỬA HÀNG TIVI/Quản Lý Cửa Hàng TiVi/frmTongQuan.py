import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import datetime

class TongQuan(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent)
        self.conn = conn
        self.controller = controller  # (MỚI) Lưu controller
        self.user = user          # (MỚI) Lưu user
        self.configure(bg="#f5f9ff")

        lbl_title = tk.Label(self, text="TRANG TỔNG QUAN HỆ THỐNG", font=("Segoe UI", 16, "bold"), fg="#003366", bg="#f5f9ff")
        lbl_title.pack(pady=15)

        frame_cards = tk.Frame(self, bg="#f5f9ff")
        frame_cards.pack(pady=10)

        self.cards = {
            "nv": self.create_card(frame_cards, "👤 Tổng nhân viên", "0"),
            "kh": self.create_card(frame_cards, "👤 Tổng khách hàng", "0"),
            "hsx": self.create_card(frame_cards, "🏭 Hãng sản xuất", "0"),
            "ncc": self.create_card(frame_cards, "🏢 Nhà cung cấp", "0"),
            "sp": self.create_card(frame_cards, "📺 Sản phẩm", "0"),
            "pn": self.create_card(frame_cards, "📦 Phiếu nhập hàng", "0"),
        }

        self.hienthi_dulieu()

        # (MỚI) Khung chính cho biểu đồ VÀ điều khiển
        self.frame_chart = tk.Frame(self, bg="#f5f9ff")
        self.frame_chart.pack(pady=20, fill="x", expand=True)

        # (MỚI) Khung con 1: Chỉ để chứa biểu đồ (canvas)
        self.frame_ve = tk.Frame(self.frame_chart, bg="#f5f9ff")
        self.frame_ve.pack()

        # (MỚI) Khung con 2: Chứa các nút điều khiển
        self.frame_dieu_khien = tk.Frame(self.frame_chart, bg="#f5f9ff")
        self.frame_dieu_khien.pack(pady=5)

        self.btn_truoc = tk.Button(self.frame_dieu_khien, text="◀", font=("Segoe UI", 10, "bold"), command=self.nam_truoc, width=4)
        self.btn_truoc.pack(side="left", padx=10)

        self.lbl_nam = tk.Label(self.frame_dieu_khien, text="Năm: ...", font=("Segoe UI", 12, "bold"), bg="#f5f9ff", fg="#003366", width=20)
        self.lbl_nam.pack(side="left", padx=20)

        self.btn_sau = tk.Button(self.frame_dieu_khien, text="▶", font=("Segoe UI", 10, "bold"), command=self.nam_sau, width=4)
        self.btn_sau.pack(side="left", padx=10)
        
        # (MỚI) Khởi tạo biến năm
        self.danh_sach_nam = []
        self.vi_tri_nam_hien_tai = 0 # Index trong danh sách
        self.nam_hien_tai = datetime.now().year # Mặc định
        
        self.lay_danh_sach_nam() # Lấy danh sách năm
        self.ve_bieu_do()       # Vẽ biểu đồ cho năm đó

    # (MỚI) Hàm lấy danh sách các năm có doanh thu
    def lay_danh_sach_nam(self):
        try:
            cursor = self.conn.cursor()
            # Lấy các năm có hóa đơn đã thanh toán
            cursor.execute("""
                SELECT DISTINCT YEAR(NgayBan) 
                FROM HoaDonBan 
                WHERE TrangThai = N'Đã thanh toán'
                ORDER BY YEAR(NgayBan) ASC
            """)
            rows = cursor.fetchall()
            self.danh_sach_nam = [row[0] for row in rows if row[0] is not None]

            if not self.danh_sach_nam:
                # Nếu không có dữ liệu, lấy năm hiện tại
                self.nam_hien_tai = datetime.now().year
                self.danh_sach_nam = [self.nam_hien_tai]
                self.vi_tri_nam_hien_tai = 0
            else:
                # Mặc định hiển thị năm mới nhất (cuối danh sách)
                self.vi_tri_nam_hien_tai = len(self.danh_sach_nam) - 1
                self.nam_hien_tai = self.danh_sach_nam[self.vi_tri_nam_hien_tai]

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách năm:\n{e}")
            # Xử lý dự phòng nếu lỗi
            self.nam_hien_tai = datetime.now().year
            self.danh_sach_nam = [self.nam_hien_tai]
            self.vi_tri_nam_hien_tai = 0

    # (MỚI) Hàm xử lý nút "Năm Trước"
    def nam_truoc(self):
        if self.vi_tri_nam_hien_tai > 0:
            self.vi_tri_nam_hien_tai -= 1
            self.nam_hien_tai = self.danh_sach_nam[self.vi_tri_nam_hien_tai]
            self.ve_bieu_do() # Vẽ lại biểu đồ

    # (MỚI) Hàm xử lý nút "Năm Sau"
    def nam_sau(self):
        if self.vi_tri_nam_hien_tai < (len(self.danh_sach_nam) - 1):
            self.vi_tri_nam_hien_tai += 1
            self.nam_hien_tai = self.danh_sach_nam[self.vi_tri_nam_hien_tai]
            self.ve_bieu_do() # Vẽ lại biểu đồ

    # (SỬA) Hàm vẽ biểu đồ đã được nâng cấp
    def ve_bieu_do(self):
        # (MỚI) Cập nhật Label và trạng thái các nút
        self.lbl_nam.config(text=f"Doanh thu năm: {self.nam_hien_tai}")
        
        # Vô hiệu hóa nút "Trước" nếu đang ở năm đầu tiên
        self.btn_truoc.config(state="disabled" if self.vi_tri_nam_hien_tai == 0 else "normal")
        
        # Vô hiệu hóa nút "Sau" nếu đang ở năm cuối cùng
        self.btn_sau.config(state="disabled" if self.vi_tri_nam_hien_tai == (len(self.danh_sach_nam) - 1) else "normal")

        try:
            cursor = self.conn.cursor()

            # (SỬA) Thêm ĐIỀU KIỆN LỌC THEO NĂM vào câu query
            query = """
                SELECT 
                    MONTH(NgayBan) AS Thang,
                    SUM(TongTien) AS DoanhThu
                FROM HoaDonBan
                WHERE TrangThai = N'Đã thanh toán' AND YEAR(NgayBan) = ?
                GROUP BY MONTH(NgayBan)
                ORDER BY Thang;"""

            cursor.execute(query, (self.nam_hien_tai,)) # (SỬA) Truyền năm vào query
            data = cursor.fetchall()
            cursor.close()

            # (SỬA) Xử lý dữ liệu để luôn có đủ 12 tháng
            # Tạo một từ điển {tháng: doanh_thu}
            doanh_thu_dict = {row.Thang: float(row.DoanhThu) for row in data}
            
            # Tạo danh sách 12 tháng
            thang = list(range(1, 13))
            
            # Lấy doanh thu cho 12 tháng, nếu tháng nào không có thì gán là 0
            doanh_thu = [doanh_thu_dict.get(t, 0) for t in thang]

            # (Không đổi) Hàm format tiền
            def format_tien(x, pos):
                return f"{int(x):,}".replace(",", ".")

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.bar(thang, doanh_thu, color="#1565C0") # (SỬA) Thêm màu

            ax.yaxis.set_major_formatter(FuncFormatter(format_tien))

            # (SỬA) Cập nhật tiêu đề biểu đồ
            ax.set_title(f"Biểu đồ doanh thu năm {self.nam_hien_tai}", fontsize=12, fontweight="bold")
            ax.set_xlabel("Tháng", fontsize=11)
            ax.set_ylabel("Doanh thu (VNĐ)", fontsize=11)
            ax.set_xticks(range(1, 13)) # Đảm bảo hiện đủ 12 mốc tháng

            fig.tight_layout()

            # (SỬA) Chỉ xóa các widget trong frame_ve (để giữ lại các nút)
            for widget in self.frame_ve.winfo_children():
                widget.destroy()

            # (SỬA) Vẽ canvas vào frame_ve
            canvas = FigureCanvasTkAgg(fig, master=self.frame_ve)
            canvas.draw()
            canvas.get_tk_widget().pack()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải biểu đồ:\n{e}")

    # (Không đổi)
    def create_card(self, parent, title, value):
        card = tk.Frame(parent, bg="#d6eaff", width=180, height=100, relief="ridge", bd=2)
        card.pack(side="left", padx=10, pady=5)
        card.pack_propagate(False)

        lbl_title = tk.Label(card, text=title, font=("Segoe UI", 10, "bold"), fg="#003366", bg="#d6eaff")
        lbl_title.pack(pady=(10, 0))

        lbl_value = tk.Label(card, text=value, font=("Segoe UI", 20, "bold"), fg="#002b80", bg="#d6eaff")
        lbl_value.pack(pady=(5, 0))

        return lbl_value

    # (Không đổi)
    def hienthi_dulieu(self):
        try:
            cursor = self.conn.cursor()

            queries = {
                "nv": "SELECT COUNT(*) FROM NhanVien",
                "kh": "SELECT COUNT(*) FROM KHACHHANG",
                "hsx": "SELECT COUNT(*) FROM HangSanXuat",
                "ncc": "SELECT COUNT(*) FROM NhaCungCap",
                "sp": "SELECT COUNT(*) FROM Tivi",
                "pn": "SELECT COUNT(*) FROM PhieuNhapHang WHERE TrangThai = N'Đã duyệt'",}

            for key, query in queries.items():
                cursor.execute(query)
                count = cursor.fetchone()[0]
                self.cards[key].config(text=str(count))

        except Exception as e:
            messagebox.showerror("Lỗi", "Không thể tải dữ liệu tổng quan:\n" + str(e))
    # Hàm làm mới tab khi click vào
    def load_data(self):
        try:
            self.hienthi_dulieu()
            self.lay_danh_sach_nam()
            self.ve_bieu_do()
            
        except Exception as e:
            messagebox.showerror("Lỗi khi làm mới dữ liệu: " + str(e))

    
