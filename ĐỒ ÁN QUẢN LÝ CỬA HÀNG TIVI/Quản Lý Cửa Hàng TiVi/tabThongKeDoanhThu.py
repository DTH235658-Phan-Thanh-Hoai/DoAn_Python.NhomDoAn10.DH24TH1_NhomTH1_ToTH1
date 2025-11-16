import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from tkcalendar import DateEntry
from datetime import date, datetime

class tabThongKeDoanhThu(tk.Frame):
    def __init__(self, parent, conn):
        super().__init__(parent, bg="white")
        self.conn = conn

        # === Bộ lọc thống kê ===
        frame_filter = tk.LabelFrame(self, text="Bộ lọc thống kê", bg="white", font=("Segoe UI", 12, "bold"), fg="#0D47A1", padx=10, pady=10,)
        frame_filter.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_filter, text="Từ ngày:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.date_tungay = DateEntry(frame_filter, width=36, date_pattern="dd/mm/yyyy", background="#1565C0", foreground="white", borderwidth=2,)
        self.date_tungay.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_filter, text="Đến ngày:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=2, padx=5, pady=5)
        self.date_denngay = DateEntry(frame_filter, width=36, date_pattern="dd/mm/yyyy", background="#1565C0", foreground="white", borderwidth=2,)
        self.date_denngay.grid(row=0, column=3, padx=5, pady=5)

        btn_thongke = tk.Button(frame_filter, text="📈 Thống kê", bg="#1E88E5", fg="white", font=("Segoe UI", 11, "bold"), bd=0, padx=15, pady=5, command=self.thongke_doanhthu_loc,)
        btn_thongke.grid(row=0, column=4, padx=10)

        tk.Button(frame_filter, text="Hủy", font=("Segoe UI", 10, "bold"), bg="#E53935", fg="white", bd=0, padx=10, pady=5, command=self.huy,).grid(row=0, column=5, padx=10)

        # === Kết quả tổng hợp ===
        frame_result = tk.Frame(self, bg="white")
        frame_result.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_result, text="Tổng hóa đơn:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.lbl_tonghd = tk.Label(frame_result, text="0", bg="white", font=("Segoe UI", 12, "bold"), fg="#1565C0",)
        self.lbl_tonghd.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_result, text="Tổng doanh thu:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=2, padx=5, pady=5)
        self.lbl_doanhthu = tk.Label(frame_result, text="0 VNĐ", bg="white", font=("Segoe UI", 12, "bold"), fg="#E53935",)
        self.lbl_doanhthu.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_result, text="Lợi nhuận:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=4, padx=5, pady=5)
        self.lbl_loinhuan = tk.Label(frame_result, text="0 VNĐ", bg="white", font=("Segoe UI", 12, "bold"), fg="#43A047",)
        self.lbl_loinhuan.grid(row=0, column=5, padx=5, pady=5)

        # === Treeview hiển thị hóa đơn ===
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("MaHD", "MaKH", "TenKH", "NgayBan", "TongTien")

        scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")

        self.trHienThi = ttk.Treeview(frame_table, show="headings", columns=columns, height=12, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set,)

        scroll_y.config(command=self.trHienThi.yview)
        scroll_x.config(command=self.trHienThi.xview)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.trHienThi.pack(fill="both", expand=True)

        self.trHienThi.heading("MaHD", text="Mã hóa đơn")
        self.trHienThi.heading("MaKH", text="Mã KH")
        self.trHienThi.heading("TenKH", text="Tên khách hàng")
        self.trHienThi.heading("NgayBan", text="Ngày bán")
        self.trHienThi.heading("TongTien", text="Tổng tiền (VNĐ)")

        # Cấu hình cột
        self.trHienThi.column("MaHD", width=100, anchor="center")
        self.trHienThi.column("MaKH", width=100, anchor="center")
        self.trHienThi.column("TenKH", width=180, anchor="w")
        self.trHienThi.column("NgayBan", width=120, anchor="center")
        self.trHienThi.column("TongTien", width=150, anchor="center")
        # Style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
        style.map("Treeview", background=[("selected", "#1565C0")])

        self.thongke_doanhthu_tatca()

    def thongke_doanhthu_tatca(self):
        try:
            cursor = self.conn.cursor()

            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            cursor.execute("""
                SELECT hdb.MaHD, hdb.MaKH, kh.TenKH, hdb.NgayBan, hdb.TongTien
                FROM HoaDonBan hdb
                JOIN KhachHang kh ON kh.MaKH = hdb.MaKH
                WHERE hdb.TrangThai = N'Đã thanh toán'
                ORDER BY hdb.NgayBan DESC
                """)
            rows = cursor.fetchall()

            tong_hoadon = 0
            for mahd, makh, tenkh, ngayban, tongtien in rows:
                ngayban_str = self.chuyen_yyyy_sang_dd(ngayban)
                tongtien_str = f"{tongtien:,.0f}" if tongtien else "0"

                self.trHienThi.insert("", "end", values=(mahd, makh, tenkh or "", ngayban_str, tongtien_str))
                tong_hoadon += 1

            cursor.execute("""
                SELECT SUM(TongTien)
                FROM HoaDonBan
                WHERE TrangThai = N'Đã thanh toán'
                """)
            tong_doanhthu = cursor.fetchone()[0] or 0

            cursor.execute("""
                SELECT SUM(T1.SoLuong * T2.AvgGiaNhap)
                FROM ChiTietHoaDon T1
                JOIN HoaDonBan HDB ON T1.MaHD = HDB.MaHD
                JOIN (
                    SELECT MaTivi, AVG(GiaNhap) AS AvgGiaNhap 
                    FROM ChiTietPhieuNhap
                    GROUP BY MaTivi
                ) AS T2 ON T1.MaTivi = T2.MaTivi
                WHERE HDB.TrangThai = N'Đã thanh toán'""")
            tong_nhap = cursor.fetchone()[0] or 0

            loinhuan = tong_doanhthu - tong_nhap

            self.lbl_tonghd.config(text=str(tong_hoadon))
            self.lbl_doanhthu.config(text=f"{tong_doanhthu:,.0f} VNĐ")
            self.lbl_loinhuan.config(text=f"{loinhuan:,.0f} VNĐ")

            cursor.close()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thống kê: {str(e)}")

    def thongke_doanhthu_loc(self):
        try:
            cursor = self.conn.cursor()

            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            tungay = str(self.date_tungay.get_date())
            denngay = str(self.date_denngay.get_date())

            if tungay > denngay:
                messagebox.showwarning("Cảnh báo", "Từ ngày phải nhỏ hơn hoặc bằng đến ngày!")
                return

            cursor.execute("""
                SELECT hdb.MaHD, hdb.MaKH, kh.TenKH, hdb.NgayBan, hdb.TongTien
                FROM HoaDonBan hdb
                JOIN KhachHang kh ON kh.MaKH = hdb.MaKH
                WHERE hdb.NgayBan BETWEEN ? AND ?
                ORDER BY hdb.NgayBan DESC
                """,(tungay, denngay),)
            rows = cursor.fetchall()

            tong_hoadon = 0
            for mahd, makh, tenkh, ngayban, tongtien in rows:
                ngayban_str = self.chuyen_yyyy_sang_dd(ngayban)
                tongtien_str = f"{tongtien:,.0f}" if tongtien else "0"

                self.trHienThi.insert("", "end", values=(mahd, makh, tenkh or "", ngayban_str, tongtien_str),)
                tong_hoadon += 1

            cursor.execute("""
                SELECT SUM(TongTien)
                FROM HoaDonBan
                WHERE TrangThai = N'Đã thanh toán'
                AND NgayBan BETWEEN ? AND ?
                """,(tungay, denngay),)
            tong_doanhthu = cursor.fetchone()[0] or 0

            cursor.execute("""
                    SELECT SUM(T1.SoLuong * T2.AvgGiaNhap)
                FROM ChiTietHoaDon T1
                JOIN HoaDonBan HDB ON T1.MaHD = HDB.MaHD
                JOIN (
                    SELECT MaTivi, AVG(GiaNhap) AS AvgGiaNhap 
                    FROM ChiTietPhieuNhap
                    GROUP BY MaTivi
                ) AS T2 ON T1.MaTivi = T2.MaTivi
                WHERE HDB.TrangThai = N'Đã thanh toán'
                AND HDB.NgayBan BETWEEN ? AND ?""", (tungay, denngay))

            tong_nhap = cursor.fetchone()[0] or 0
            loinhuan = tong_doanhthu - tong_nhap

            self.lbl_tonghd.config(text=str(tong_hoadon))
            self.lbl_doanhthu.config(text=f"{tong_doanhthu:,.0f} VNĐ")
            self.lbl_loinhuan.config(text=f"{loinhuan:,.0f} VNĐ")

            cursor.close()

            if tong_hoadon == 0:
                messagebox.showinfo("Thông báo", "Không có hóa đơn nào trong khoảng thời gian này!")

        except Exception as e:
            messagebox.showerror("Lỗi", "Không thể thống kê: " + str(e))

    def huy(self):
        self.date_tungay.set_date(date.today())
        self.date_denngay.set_date(date.today())
        self.thongke_doanhthu_tatca()

    def chuyen_yyyy_sang_dd(self, ngay_db):
        if ngay_db is None:
            return ""
        ngay_str = str(ngay_db).strip()
        if "-" in ngay_str:
            parts = ngay_str.split("-")
        else:
            return ngay_str

        if len(parts) != 3:
            return ngay_str
        try:
            y, m, d = parts
            return f"{d.zfill(2)}/{m.zfill(2)}/{y}"
        except:
            return ngay_str

    def chuyen_dd_sang_datetime(self, ngay_entry):
        if not ngay_entry:
            return date.today()
        ngay_str = str(ngay_entry).strip()
        if "-" in ngay_str:
            parts = ngay_str.split("-")
        else:
            return ngay_str

        if len(parts) != 3:
            return date.today()
        try:
            d, m, y = map(int, parts)
            return datetime(y, m, d).date()
        except:
            return date.today()
