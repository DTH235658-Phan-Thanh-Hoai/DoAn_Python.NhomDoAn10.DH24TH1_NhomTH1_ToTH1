import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime


class tabBaoCaoSanPham(tk.Frame):
    def __init__(self, parent, conn):
        super().__init__(parent, bg="white")

        self.conn = conn

        frame_filter = tk.LabelFrame(self, text="Tùy chọn báo cáo", bg="white", font=("Segoe UI", 12, "bold"), fg="#0D47A1", padx=10, pady=10)
        frame_filter.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_filter, text="Chọn mã tivi:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=0, padx=5, pady=5)
        self.cbo_mativi = ttk.Combobox(frame_filter, width=31, state="readonly")
        self.cbo_mativi.grid(row=0, column=1, padx=5, pady=5)
        self.cbo_mativi.bind("<<ComboboxSelected>>", self.on_mativi_selected)

        tk.Label(frame_filter, text="Chọn tên tivi:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=2, padx=5, pady=5)
        self.cbo_tentivi = ttk.Combobox(frame_filter, width=31, state="readonly")
        self.cbo_tentivi.grid(row=0, column=3, padx=5, pady=5)
        self.cbo_tentivi.bind("<<ComboboxSelected>>", self.on_tentivi_selected)

        tk.Button(frame_filter, text="📊 Xem báo cáo", bg="#1E88E5", fg="white", font=("Segoe UI", 11, "bold"), bd=0, padx=15, pady=5, command=self.xem_baocao).grid(row=0, column=4, padx=10)
        tk.Button(frame_filter, text="Hủy", bg="#E53935", fg="white", font=("Segoe UI", 11, "bold"), bd=0, padx=15, pady=5, command=self.huy_xem_bao_cao).grid(row=0, column=5, padx=10)

        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("MaTivi", "TenTivi", "SoLuongBan", "TiLeBanChay", "DoanhThu", "LoiNhuan")

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

        self.trHienThi.heading("MaTivi", text="Mã Tivi")
        self.trHienThi.heading("TenTivi", text="Tên Tivi")
        self.trHienThi.heading("SoLuongBan", text="SL Bán")
        self.trHienThi.heading("TiLeBanChay", text="Tỉ Lệ (%)")
        self.trHienThi.heading("DoanhThu", text="Doanh Thu (VNĐ)")
        self.trHienThi.heading("LoiNhuan", text="Lợi Nhuận (VNĐ)")

        self.trHienThi.column("MaTivi", width=100, anchor="center")
        self.trHienThi.column("TenTivi", width=250, anchor="center")
        self.trHienThi.column("SoLuongBan", width=120, anchor="center")
        self.trHienThi.column("TiLeBanChay", width=120, anchor="center")
        self.trHienThi.column("DoanhThu", width=150, anchor="center")
        self.trHienThi.column("LoiNhuan", width=150, anchor="center")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        self.tivi_dict = {}
        self.load_combo_tivi()
        self.load_baocao_all()

    def load_combo_tivi(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT MaTivi, TenTivi FROM Tivi ORDER BY TenTivi")
            rows = cursor.fetchall()

            ma_list = ["-- Tất cả --"]
            ten_list = ["-- Tất cả --"]

            for row in rows:
                mativi, tentivi = row
                ma_list.append(mativi)
                ten_list.append(tentivi)
                self.tivi_dict[mativi] = tentivi
                self.tivi_dict[tentivi] = mativi

            self.cbo_mativi["values"] = ma_list
            self.cbo_tentivi["values"] = ten_list
            self.cbo_mativi.current(0)
            self.cbo_tentivi.current(0)

            cursor.close()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách tivi: {str(e)}")

    def on_mativi_selected(self, event):
        mativi = self.cbo_mativi.get()
        if mativi and mativi != "-- Tất cả --":
            tentivi = self.tivi_dict.get(mativi)
            if tentivi:
                idx = list(self.cbo_tentivi["values"]).index(tentivi)
                self.cbo_tentivi.current(idx)

    def on_tentivi_selected(self, event):
        tentivi = self.cbo_tentivi.get()
        if tentivi and tentivi != "-- Tất cả --":
            mativi = self.tivi_dict.get(tentivi)
            if mativi:
                idx = list(self.cbo_mativi["values"]).index(mativi)
                self.cbo_mativi.current(idx)

    def load_baocao_all(self):
        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            cursor = self.conn.cursor()

            query = """
                SELECT 
                    t.MaTivi,
                    t.TenTivi,
                    ISNULL(SUM(ct.SoLuong), 0) AS TongSoLuongBan,
                    ISNULL(SUM(ct.ThanhTien), 0) AS TongDoanhThu,
                    ISNULL(AVG(pn.DonGia), 0) AS GiaNhap
                FROM Tivi t
                JOIN ChiTietHoaDon ct ON t.MaTivi = ct.MaTivi
                JOIN HoaDonBan hd 
                    ON ct.MaHD = hd.MaHD
                    AND hd.TrangThai = N'Đã thanh toán'
                LEFT JOIN (
                    SELECT MaTivi, AVG(GiaNhap) AS DonGia
                    FROM ChiTietPhieuNhap
                    GROUP BY MaTivi
                ) pn 
                    ON t.MaTivi = pn.MaTivi
                GROUP BY t.MaTivi, t.TenTivi
                ORDER BY TongSoLuongBan DESC;"""

            cursor.execute(query)
            rows = cursor.fetchall()

            tong_soluong = sum(row[2] for row in rows)

            for row in rows:
                mativi, tentivi, soluongban, doanhthu, gianhap = row

                tile = (soluongban / tong_soluong * 100) if tong_soluong > 0 else 0
                loinhuan = (soluongban * (doanhthu / soluongban - gianhap)) if soluongban > 0 else 0

                self.trHienThi.insert("", "end", values=(mativi, tentivi, soluongban, f"{tile:.2f}%", f"{doanhthu:,.0f}", f"{loinhuan:,.0f}"))

            cursor.close()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải báo cáo: {str(e)}")

    def xem_baocao(self):
        mativi = self.cbo_mativi.get()
        tentivi = self.cbo_tentivi.get()

        if mativi == "-- Tất cả --" or not mativi:
            self.load_baocao_all()
            return

        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            cursor = self.conn.cursor()

            query_tong = """
                SELECT ISNULL(SUM(SoLuong), 0)
                FROM ChiTietHoaDon"""
            
            cursor.execute(query_tong)
            tong_soluong = cursor.fetchone()[0]

            query = """
                SELECT 
                    t.MaTivi,
                    t.TenTivi,
                    ISNULL(SUM(ct.SoLuong), 0) as TongSoLuongBan,
                    ISNULL(SUM(ct.ThanhTien), 0) as TongDoanhThu,
                    ISNULL(AVG(pn.DonGia), 0) as GiaNhap
                FROM Tivi t
                LEFT JOIN ChiTietHoaDon ct ON t.MaTivi = ct.MaTivi
                LEFT JOIN (
                    SELECT MaTivi, AVG(GiaNhap) as DonGia
                    FROM ChiTietPhieuNhap
                    GROUP BY MaTivi
                ) pn ON t.MaTivi = pn.MaTivi
                WHERE t.MaTivi = ?
                GROUP BY t.MaTivi, t.TenTivi"""

            cursor.execute(query, (mativi,))
            row = cursor.fetchone()

            if row:
                mativi, tentivi, soluongban, doanhthu, gianhap = row

                tile = (soluongban / tong_soluong * 100) if tong_soluong > 0 else 0
                loinhuan = (soluongban * (doanhthu / soluongban - gianhap) if soluongban > 0 else 0)

                self.trHienThi.insert("", "end", values=(mativi, tentivi, soluongban, f"{tile:.2f}%", f"{doanhthu:,.0f}", f"{loinhuan:,.0f}"))
            else:
                messagebox.showinfo("Thông báo", "Không tìm thấy dữ liệu cho sản phẩm này!")

            cursor.close()

        except Exception as e:
            messagebox.showerror("Lỗi", "Không thể xem báo cáo: " + str(e))

    def huy_xem_bao_cao(self):
        self.load_baocao_all()

        self.cbo_mativi.delete(0, tk.END)
        self.cbo_mativi.set("-- Tất cả --")

        self.cbo_tentivi.delete(0, tk.END)
        self.cbo_tentivi.set("-- Tất cả --")
