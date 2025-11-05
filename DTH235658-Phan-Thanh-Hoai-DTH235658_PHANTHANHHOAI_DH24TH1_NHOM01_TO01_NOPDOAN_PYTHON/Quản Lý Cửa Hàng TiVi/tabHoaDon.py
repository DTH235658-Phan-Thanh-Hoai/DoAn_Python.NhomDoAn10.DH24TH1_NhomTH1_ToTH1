import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pyodbc

# === TAB HÓA ĐƠN ===
class tabHoaDon(tk.Frame):
    def __init__(self, parent, conn):
        super().__init__(parent, bg="white")

        # === CHUỖI KẾT NỐI ===
        self.conn = conn

        # === KHUNG TÌM KIẾM ===
        frame_search = tk.Frame(self, bg="#E3F2FD", padx=10, pady=10)
        frame_search.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_search, text="🔍 Tìm kiếm:", font=("Segoe UI", 10), bg="#E3F2FD").pack(side="left", padx=5)
        self.txt_timkiem = tk.Entry(frame_search, font=("Segoe UI", 10), width=20)
        self.txt_timkiem.pack(side="left", padx=5)

        self.search_option = tk.StringVar(value="ma")
        self.search_option = tk.StringVar(value="mahd")
        tk.Radiobutton(frame_search, text="Theo mã hóa đơn", variable=self.search_option, value="mahd", bg="#E3F2FD", font=("Segoe UI", 10)).pack(side="left", padx=10)
        tk.Radiobutton(frame_search, text="Theo mã khách hàng", variable=self.search_option, value="makh", bg="#E3F2FD", font=("Segoe UI", 10)).pack(side="left" , padx=10)
        tk.Radiobutton(frame_search, text="Theo trạng thái phiếu", variable=self.search_option, value="trangthai", bg="#E3F2FD", font=("Segoe UI", 10)).pack(side="left", padx=10)
        tk.Button(frame_search, text="Tìm", font=("Segoe UI", 10, "bold"), command=self.TimKiem, bg="#1565C0", fg="white", bd=0, padx=10, pady=5).pack(side="left", padx=10)
        tk.Button(frame_search, text="Hủy", font=("Segoe UI", 10, "bold"), command=self.load_hoa_don, bg="#E53935", fg="white", bd=0, padx=10, pady=5).pack(side="left", padx=10)

        # === BẢNG DANH SÁCH HÓA ĐƠN ===
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("MaHD", "NgayBan", "MaNV", "MaKH", "TongTien", "TrangThai")
        self.trHienThi = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
        self.trHienThi.pack(fill="both", expand=True)

        self.trHienThi.heading("MaHD", text="Mã hóa đơn")
        self.trHienThi.heading("NgayBan", text="Ngày bán")
        self.trHienThi.heading("MaNV", text="Mã nhân viên")
        self.trHienThi.heading("MaKH", text="Mã khách hàng")
        self.trHienThi.heading("TongTien", text="Tổng tiền")
        self.trHienThi.heading("TrangThai", text="Trạng thái")

        self.trHienThi.column("MaHD", width=100)
        self.trHienThi.column("NgayBan", width=100, anchor="center")
        self.trHienThi.column("MaNV", width=100)
        self.trHienThi.column("MaKH", width=100)
        self.trHienThi.column("TongTien", width=100, anchor="center")
        self.trHienThi.column("TrangThai", width=100)

        # Thêm style cho Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        # ==== Nút thao tác ====
        frame_btn = tk.Frame(self, bg="white")
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="🧐 Xem chi tiết", bg="#EC9428", fg="white", font=("Segoe UI", 10, "bold"),command=self.XemChiTiet, padx=15, pady=5, bd=0).pack(side="left", padx=5)
        tk.Button(frame_btn, text="✅ Thanh toán hóa đơn", bg="#43A047", fg="white",  font=("Segoe UI", 10, "bold"), command=self.ThanhToanHoaDonBan, padx=15, pady=5, bd=0).pack(side="left", padx=5)
        tk.Button(frame_btn, text="🗑 Hủy hóa đơn", bg="#E53935", fg="white",  font=("Segoe UI", 10, "bold"), padx=15, command=self.HuyHoaDonBan, pady=5, bd=0).pack(side="left", padx=5)
        tk.Button(frame_btn, text="🔄 Làm mới", bg="#1E88E5", fg="white", font=("Segoe UI", 10, "bold"), padx=15, command=self.load_hoa_don, pady=5, bd=0).pack(side="left", padx=5)
        tk.Button(frame_btn, text="🖨 In hóa đơn", bg="#E51E9C", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=5, bd=0).pack(side="left", padx=5)

        # === TẢI DỮ LIỆU HÓA ĐƠN ===
        self.load_hoa_don()

    def load_hoa_don(self):
        try:
            self.trHienThi.delete(*self.trHienThi.get_children())
            cursor = self.conn.cursor()
            cursor.execute("SELECT MaHD, NgayBan, MaNV, MaKH, TongTien, TrangThai FROM HOADONBAN")

            for row in cursor.fetchall():
                ngay_ban = datetime.strptime(str(row.NgayBan).split(" ")[0], "%Y-%m-%d")

                formatted_row = (
                    row.MaHD, ngay_ban.strftime("%d/%m/%Y"), row.MaNV, row.MaKH,
                    f"{float(row.TongTien):,.0f}" if row.TongTien else "0", row.TrangThai
                )
                self.trHienThi.insert("", tk.END, values=formatted_row)

            # Xóa txt_timkiem nếu có
            self.txt_timkiem.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Lỗi", "Không thể tải dữ liệu hóa đơn:\n" + str(e))

    # === Hàm xem chi tiết phiếu nhập ===
    def XemChiTiet(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn 1 hóa đơn để xem chi tiết.")
            return

        ma_hd = self.trHienThi.item(selected[0], "values")[0]

        try:
            chitiethoadon= tk.Toplevel(self)
            chitiethoadon.title("Chi tiết hóa đơn: " + ma_hd)
            chitiethoadon.geometry("700x800")
            chitiethoadon.resizable(False, False)
            chitiethoadon.configure(bg="white")
            

            tk.Label(chitiethoadon, text="Chi tiết hóa đơn bán " + ma_hd, font=("Segoe UI", 12, "bold"), bg="white", fg="#0D47A1").pack(pady=10)
            
            cursor = self.conn.cursor()
            cursor.execute("""SELECT nv.MaNV, nv.TenNV, kh.MaKH, kh.TenKH, hdb.NgayBan, hdb.TongTien, hdb.TrangThai
                              FROM HOADONBAN hdb JOIN NHANVIEN nv ON hdb.MaNV = nv.MaNV
                              JOIN KHACHHANG kh ON hdb.MaKH = kh.MaKH
                              WHERE hdb.MaHD = ?""", (ma_hd,))
            thong_tin = cursor.fetchone()

            Frame_thongtin = tk.Frame(chitiethoadon, bg="white")
            Frame_thongtin.pack(pady=5)
            tk.Label(Frame_thongtin, text="Mã nhân viên:", font=("Segoe UI", 10), bg="white").grid(row=0, column=0, padx=10, sticky="w")
            tk.Label(Frame_thongtin, text=thong_tin.MaNV, font=("Segoe UI", 10, "bold"), bg="white", fg="#1565C0").grid(row=0, column=1, padx=10, sticky="w")

            tk.Label(Frame_thongtin, text="Tên nhân viên:", font=("Segoe UI", 10), bg="white").grid(row=0, column=2, padx=10, sticky="w")
            tk.Label(Frame_thongtin, text=thong_tin.TenNV, font=("Segoe UI", 10, "bold"), bg="white", fg="#1565C0").grid(row=0, column=3, padx=10, sticky="w")

            tk.Label(Frame_thongtin, text="Mã khách hàng:", font=("Segoe UI", 10), bg="white").grid(row=1, column=0, padx=10, sticky="w")
            tk.Label(Frame_thongtin, text=thong_tin.MaKH, font=("Segoe UI", 10, "bold"), bg="white", fg="#1565C0").grid(row=1, column=1, padx=10, sticky="w")

            tk.Label(Frame_thongtin, text="Tên khách hàng:", font=("Segoe UI", 10), bg="white").grid(row=1, column=2, padx=10, sticky="w")
            tk.Label(Frame_thongtin, text=thong_tin.TenKH, font=("Segoe UI", 10, "bold"), bg="white", fg="#1565C0").grid(row=1, column=3, padx=10, sticky="w")

            tk.Label(Frame_thongtin, text="Ngày bán:", font=("Segoe UI", 10), bg="white").grid(row=2, column=0, padx=10, sticky="w")
            
            ngay_nhap = datetime.strptime(str(thong_tin.NgayBan).split(" ")[0], "%Y-%m-%d")
            tk.Label(Frame_thongtin, text=ngay_nhap.strftime("%d/%m/%Y"), font=("Segoe UI", 10, "bold"), bg="white", fg="#43A047").grid(row=2, column=1, padx=10, sticky="w")

            tk.Label(Frame_thongtin, text="Trạng thái:", font=("Segoe UI", 10), bg="white").grid(row=2, column=2, padx=10, sticky="w")
            tk.Label(Frame_thongtin, text=thong_tin.TrangThai, font=("Segoe UI", 10, "bold"), bg="white", fg="#43A047").grid(row=2, column=3, padx=10, sticky="w")
            
            columns = ("MaTivi", "TenTivi", "SoLuong", "DonGia", "ThanhTien")
            tree = ttk.Treeview(chitiethoadon, columns=columns, show="headings", height=10)
            tree.pack(fill="both", expand=True, padx=15, pady=10)

            tree.heading("MaTivi", text="Mã Tivi")
            tree.heading("TenTivi", text="Tên Tivi")
            tree.heading("SoLuong", text="Số Lượng")
            tree.heading("DonGia", text="Đơn Giá")
            tree.heading("ThanhTien", text="Thành Tiền")

            tree.column("MaTivi", width=100)
            tree.column("TenTivi", width=200)
            tree.column("SoLuong", width=100, anchor="center")
            tree.column("DonGia", width=100, anchor="center")
            tree.column("ThanhTien", width=100, anchor="center")

            tk.Label(chitiethoadon, text="Tổng tiền:", font=("Segoe UI", 10, "bold"), bg="white").pack(side="left", padx=20)
            tk.Label(chitiethoadon, text=f"{float(thong_tin.TongTien):,.0f} đ", font=("Segoe UI", 10, "bold"), bg="white", fg="red").pack(side="right", padx=20)
            
            cursor.execute("""
                SELECT cthd.MaTivi, tv.TenTivi, cthd.SoLuong, cthd.DonGia, cthd.ThanhTien
                FROM CHITIETHOADON cthd
                JOIN TIVI tv ON cthd.MaTivi = tv.MaTivi
                WHERE cthd.MaHD = ?
            """, (ma_hd,))
            rows = cursor.fetchall()

            if not rows:
                messagebox.showinfo("Thông báo", "Không có chi tiết cho phiếu" + ma_hd)
                chitiethoadon.destroy()
                return

            for r in rows:
                tree.insert("", tk.END, values=(
                    r.MaTivi,
                    r.TenTivi,
                    r.SoLuong,
                    f"{float(r.DonGia):,.0f} đ",
                    f"{float(r.ThanhTien):,.0f} đ"
                ))

            cursor.close()
        except Exception as e:
            messagebox.showerror("Lỗi", "Không thể xem chi tiết hóa đơn:\n" + str(e))

    def ThanhToanHoaDonBan(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn 1 hoa đơn để duyệt.")
            return
        ma_hd= self.trHienThi.item(selected[0], "values")[0]
        trang_thai = self.trHienThi.item(selected[0], "values")[5]

        if trang_thai != "Chờ thanh toán":
            messagebox.showwarning("Thông báo", "Chỉ có thể thanh toán hóa đơn chờ thanh toán.")
            return
        
        traloi = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn thanh toán hóa đơn " + ma_hd + " không?")
        if traloi:
            try:
                cursor = self.conn.cursor()
                # Cập nhật thanh toán
                cursor.execute("""
                    UPDATE HOADONBAN
                    SET TrangThai = N'Đã thanh toán'
                    WHERE MaHD = ?
                """, (ma_hd,))

                # Lấy chi tiết hóa đơn để cập nhật tồn kho
                cursor.execute("""
                    SELECT MaTivi, SoLuong
                    FROM CHITIETHOADON
                    WHERE MaHD = ?
                """, (ma_hd,))

                chitiet = cursor.fetchall()

                for item in chitiet:
                    ma_tivi = item.MaTivi
                    so_luong = item.SoLuong

                    # Cập nhật số lượng tồn kho của tivi
                    cursor.execute("""
                        UPDATE TIVI
                        SET SoLuongTon = SoLuongTon - ?
                        WHERE MaTivi = ? """, (so_luong, ma_tivi))
                
                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Thành công", "Hóa đơn đã thanh toán thành công!")

                # Làm mới lại danh sách hóa đơn
                self.load_hoa_don()

            except Exception as e:
                messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi thanh toán hóa đơn:\n" + str(e))

    def HuyHoaDonBan(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn 1 hóa đơn để hủy")
            return
        
        ma_hd = self.trHienThi.item(selected[0], "values")[0]
        trang_thai = self.trHienThi.item(selected[0], "values")[5]

        if trang_thai != "Chờ thanh toán":
            messagebox.showwarning("Thông báo", "Chỉ có thể hủy hóa đơn chưa thanh toán.")
            return
        
        traloi = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn hủy hóa đơn " + ma_hd + " không?")
        if traloi:
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    UPDATE HOADONBAN
                    SET TrangThai = N'Đã hủy'
                    WHERE MaHD = ?""", (ma_hd,))
                
                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Thành công", "Hóa đơn đã được hủy thành công!")
                self.load_hoa_don()

            except Exception as e:
                messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi hủy hóa đơn:\n" + str(e))


    def TimKiem(self):
        if self.txt_timkiem.get().strip() == "":
            messagebox.showwarning("Thông báo", "Vui lòng nhập từ khóa tìm kiếm.")
            return
        
        timkkiem = self.search_option.get().strip()
        self.trHienThi.delete(*self.trHienThi.get_children())

        try:
            cursor = self.conn.cursor()

            if timkkiem == "mahd":
                keyword = self.txt_timkiem.get()
                cursor.execute("""
                    SELECT MaHD, NgayBan, MaNV, MaKH, TongTien, TrangThai
                    FROM HOADONBAN
                    WHERE MaHD = ?""", (keyword,))
            
            elif timkkiem == "makh":
                keyword = self.txt_timkiem.get()
                cursor.execute("""
                    SELECT MaHD, NgayBan, MaNV, MaKH, TongTien, TrangThai
                    FROM HOADONBAN
                    WHERE MaKH = ?""", (keyword,))
            
            elif timkkiem == "trangthai":
                keyword = self.txt_timkiem.get()
                cursor.execute("""
                    SELECT MaHD, NgayBan, MaNV, MaKH, TongTien, TrangThai
                    FROM HOADONBAN
                    WHERE TrangThai = ?""", (keyword,))
                
            rows = cursor.fetchall()
            for row in rows:
                ngay_ban = datetime.strptime(str(row.NgayBan).split(" ")[0], "%Y-%m-%d")

                formatted_row = (
                    row.MaHD, ngay_ban.strftime("%d/%m/%y"), row.MaNV, row.MaKH,
                    f"{float(row.TongTien):,.0f}" if row.TongTien else "0", row.TrangThai
                )
                self.trHienThi.insert("", tk.END, values=formatted_row)
            cursor.close()

        except Exception as e:
            messagebox.showerror("Lỗi", "Không thể tìm kiếm hóa đơn:\n" + str(e))
