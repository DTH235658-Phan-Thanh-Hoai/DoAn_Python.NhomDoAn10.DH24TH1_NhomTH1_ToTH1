import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from tkcalendar import DateEntry
from datetime import date, datetime


class tabThongKeDoanhThu(tk.Frame):
    def __init__(self, parent, conn):
        super().__init__(parent, bg="white")

        self.conn = conn

        frame_filter = tk.LabelFrame(
            self,
            text="Bộ lọc thống kê",
            bg="white",
            font=("Segoe UI", 12, "bold"),
            fg="#0D47A1",
            padx=10,
            pady=10,
        )
        frame_filter.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_filter, text="Từ ngày:", bg="white", font=("Segoe UI", 10)).grid(
            row=0, column=0, padx=5, pady=5
        )
        self.date_tungay = DateEntry(frame_filter, width=36, date_pattern="dd/mm/yyyy")
        self.date_tungay.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            frame_filter, text="Đến ngày:", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=2, padx=5, pady=5)
        self.date_denngay = DateEntry(frame_filter, width=36, date_pattern="dd/mm/yyyy")
        self.date_denngay.grid(row=0, column=3, padx=5, pady=5)

        btn_thongke = tk.Button(
            frame_filter,
            text="📅 Thống kê",
            bg="#1E88E5",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            padx=15,
            pady=5,
            command=self.thongke_doanhthu,
        )
        btn_thongke.grid(row=0, column=4, padx=10)
        
        tk.Button(
            frame_filter,
            text="Hủy",
            font=("Segoe UI", 10, "bold"),
            bg="#E53935",
            fg="white",
            bd=0,
            padx=10,
            pady=5,
            command=self.huy,
        ).grid(row=0, column=5, padx=10)

        frame_result = tk.Frame(self, bg="white")
        frame_result.pack(fill="x", padx=20, pady=10)

        tk.Label(
            frame_result, text="Tổng hóa đơn:", bg="white", font=("Segoe UI", 12)
        ).grid(row=0, column=0, padx=5, pady=5)
        self.lbl_tonghd = tk.Label(
            frame_result,
            text="0",
            bg="white",
            font=("Segoe UI", 12, "bold"),
            fg="#1565C0",
        )
        self.lbl_tonghd.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            frame_result, text="Tổng doanh thu:", bg="white", font=("Segoe UI", 12)
        ).grid(row=0, column=2, padx=5, pady=5)
        self.lbl_doanhthu = tk.Label(
            frame_result,
            text="0 VNĐ",
            bg="white",
            font=("Segoe UI", 12, "bold"),
            fg="#E53935",
        )
        self.lbl_doanhthu.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(
            frame_result, text="Lợi nhuận:", bg="white", font=("Segoe UI", 12)
        ).grid(row=0, column=4, padx=5, pady=5)
        self.lbl_loinhuan = tk.Label(
            frame_result,
            text="0 VNĐ",
            bg="white",
            font=("Segoe UI", 12, "bold"),
            fg="#43A047",
        )
        self.lbl_loinhuan.grid(row=0, column=5, padx=5, pady=5)

        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("MaHD", "NgayBan", "MaNV", "MaKH", "TongTien")

        # --- Tạo Scrollbar ---
        scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")

        self.trHienThi = ttk.Treeview( frame_table, show="headings",  columns=columns, height=12, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # --- Gắn Scrollbar ---
        scroll_y.config(command=self.trHienThi.yview)
        scroll_x.config(command=self.trHienThi.xview)

        # --- Bố trí Scrollbar ---
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.trHienThi.pack(fill="both", expand=True)

        self.trHienThi.column("MaHD", width=100)
        self.trHienThi.column("NgayBan", width=120)
        self.trHienThi.column("MaNV", width=100)
        self.trHienThi.column("MaKH", width=100)
        self.trHienThi.column("TongTien", width=150)

        self.trHienThi.heading("MaHD", text="Mã hóa đơn", anchor="center")
        self.trHienThi.heading("NgayBan", text="Ngày bán", anchor="center")
        self.trHienThi.heading("MaNV", text="Mã nhân viên", anchor="center")
        self.trHienThi.heading("MaKH", text="Mã khách hàng", anchor="center")
        self.trHienThi.heading("TongTien", text="Tổng tiền (VNĐ)", anchor="center")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        chart_frame = tk.Frame(self, bg="white")
        chart_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(
            chart_frame,
            text="📊 (Khu vực biểu đồ doanh thu theo tháng)",
            font=("Segoe UI", 11, "italic"),
            bg="white",
            fg="gray",
        ).pack()

        self.lay_tatca_hoadon()

    def lay_tatca_hoadon(self):
        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            cursor = self.conn.cursor()
            query = """
                SELECT MaHD, NgayBan, MaNV, MaKH, TongTien 
                FROM HoaDonBan 
                ORDER BY NgayBan DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            tong_hoadon = 0
            tong_doanhthu = 0

            for row in rows:
                mahd, ngayban, manv, makh, tongtien = row
                ngayban_str = ngayban if ngayban else ""
                tongtien_str = f"{tongtien:,.0f}" if tongtien else "0"

                self.trHienThi.insert(
                    "",
                    "end",
                    values=(
                        mahd,
                        ngayban_str,
                        manv,
                        makh if makh else "",
                        tongtien_str,
                    ),
                )

                tong_hoadon += 1
                tong_doanhthu += tongtien if tongtien else 0

            self.lbl_tonghd.config(text=str(tong_hoadon))
            self.lbl_doanhthu.config(text=f"{tong_doanhthu:,.0f} VNĐ")

            loinhuan = self.tinh_loinhuan()
            self.lbl_loinhuan.config(text=f"{loinhuan:,.0f} VNĐ")

            cursor.close()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def thongke_doanhthu(self):
        try:
            tungay = self.date_tungay.get_date()
            denngay = self.date_denngay.get_date()

            if tungay > denngay:
                messagebox.showwarning(
                    "Cảnh báo", "Từ ngày phải nhỏ hơn hoặc bằng đến ngày!"
                )
                return

            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            tungay_str = tungay.strftime("%Y-%m-%d")
            denngay_str = denngay.strftime("%Y-%m-%d")

            cursor = self.conn.cursor()
            query = """
                SELECT MaHD, NgayBan, MaNV, MaKH, TongTien 
                FROM HoaDonBan 
                WHERE NgayBan BETWEEN ? AND ?
                ORDER BY NgayBan DESC
            """
            cursor.execute(query, (tungay_str, denngay_str))
            rows = cursor.fetchall()

            tong_hoadon = 0
            tong_doanhthu = 0

            for row in rows:
                mahd, ngayban, manv, makh, tongtien = row
                ngayban_str = ngayban if ngayban else ""
                tongtien_str = f"{tongtien:,.0f}" if tongtien else "0"

                self.trHienThi.insert(
                    "",
                    "end",
                    values=(
                        mahd,
                        ngayban_str,
                        manv,
                        makh if makh else "",
                        tongtien_str,
                    ),
                )

                tong_hoadon += 1
                tong_doanhthu += tongtien if tongtien else 0

            self.lbl_tonghd.config(text=str(tong_hoadon))
            self.lbl_doanhthu.config(text=f"{tong_doanhthu:,.0f} VNĐ")

            loinhuan = self.tinh_loinhuan(tungay_str, denngay_str)
            self.lbl_loinhuan.config(text=f"{loinhuan:,.0f} VNĐ")

            cursor.close()

            if tong_hoadon == 0:
                messagebox.showinfo(
                    "Thông báo", "Không có hóa đơn nào trong khoảng thời gian này!"
                )

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thống kê: {str(e)}")
    
    def tinh_loinhuan(self, tungay=None, denngay=None):
        try:
            cursor = self.conn.cursor()

            if tungay and denngay:
                query = """
                    SELECT SUM(ct.SoLuong * (ct.DonGia - ISNULL(pn.GiaNhap, 0)))
                    FROM ChiTietHoaDon ct
                    INNER JOIN HoaDonBan hd ON ct.MaHD = hd.MaHD
                    LEFT JOIN (
                        SELECT MaTivi, AVG(GiaNhap) as GiaNhap
                        FROM ChiTietPhieuNhap
                        GROUP BY MaTivi
                    ) pn ON ct.MaTivi = pn.MaTivi
                    WHERE hd.NgayBan BETWEEN ? AND ?
                """
                cursor.execute(query, (tungay, denngay))
            else:
                query = """
                    SELECT SUM(ct.SoLuong * (ct.DonGia - ISNULL(pn.GiaNhap, 0)))
                    FROM ChiTietHoaDon ct
                    LEFT JOIN (
                        SELECT MaTivi, AVG(GiaNhap) as GiaNhap
                        FROM ChiTietPhieuNhap
                        GROUP BY MaTivi
                    ) pn ON ct.MaTivi = pn.MaTivi
                """
                cursor.execute(query)

            result = cursor.fetchone()
            loinhuan = result[0] if result[0] else 0

            cursor.close()
            return loinhuan

        except Exception as e:
            print(f"Lỗi tính lợi nhuận: {str(e)}")
            return 0

    def huy(self):
        self.date_tungay.set_date(datetime.now().date())
        self.date_denngay.set_date(datetime.now().date())
        self.lay_tatca_hoadon()
