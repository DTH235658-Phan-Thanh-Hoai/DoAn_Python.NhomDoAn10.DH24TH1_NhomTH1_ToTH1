import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, timedelta, datetime
import pyodbc


class tabBaoHanh(tk.Frame):
    def __init__(self, parent, conn):
        super().__init__(parent, bg="white")

        self.conn = conn
        self.cursor = conn.cursor()

        self.ds_them = []
        self.ds_sua = []
        self.ds_xoa = []

        # === KHUNG TÌM KIẾM ===
        frame_search = tk.Frame(self, bg="#E3F2FD", padx=10, pady=10)
        frame_search.pack(fill="x", padx=20, pady=5)

        tk.Label(
            frame_search, text="Tìm kiếm:", font=("Segoe UI", 10), bg="#E3F2FD"
        ).pack(side="left", padx=5)
        self.txt_timkiem = tk.Entry(
            frame_search, font=("Segoe UI", 10), width=50, bg="white"
        )
        self.txt_timkiem.pack(side="left", padx=5)
        self.txt_timkiem.bind("<Return>", lambda e: self.timkiem())

        self.search_option = tk.StringVar(value="mabh")
        tk.Radiobutton(
            frame_search,
            text="Mã BH",
            variable=self.search_option,
            value="mabh",
            bg="#E3F2FD",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=5)
        tk.Radiobutton(
            frame_search,
            text="Mã Tivi",
            variable=self.search_option,
            value="mativi",
            bg="#E3F2FD",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=5)
        tk.Radiobutton(
            frame_search,
            text="Mã HD",
            variable=self.search_option,
            value="mahd",
            bg="#E3F2FD",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=5)

        tk.Button(
            frame_search,
            text="Tìm",
            font=("Segoe UI", 10, "bold"),
            bg="#1565C0",
            fg="white",
            bd=0,
            padx=10,
            pady=5,
            command=self.timkiem,
        ).pack(side="left", padx=10)
        tk.Button(
            frame_search,
            text="Hủy",
            font=("Segoe UI", 10, "bold"),
            bg="#E53935",
            fg="white",
            bd=0,
            padx=10,
            pady=5,
            command=self.huy,
        ).pack(side="left", padx=10)

        # === KHUNG THÔNG TIN ===
        frame_form = tk.LabelFrame(
            self,
            text="Thông tin Bảo hành",
            bg="white",
            font=("Segoe UI", 12, "bold"),
            fg="#0D47A1",
            padx=10,
            pady=10,
        )
        frame_form.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_form, text="Mã BH:", bg="white", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.txt_mabh = ttk.Entry(frame_form, width=20)
        self.txt_mabh.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Mã Tivi:", bg="white", font=("Segoe UI", 10)).grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )
        self.cb_mativi = ttk.Combobox(
            frame_form, width=18, font=("Segoe UI", 10), state="readonly"
        )
        self.cb_mativi.grid(row=0, column=3, padx=5, pady=5)
        self.cb_mativi.bind(
            "<<ComboboxSelected>>", lambda e: self.capnhat_mahd_theo_tivi()
        )

        tk.Label(frame_form, text="Mã HD:", bg="white", font=("Segoe UI", 10)).grid(
            row=0, column=4, sticky="w", padx=5, pady=5
        )
        self.cb_mahd = ttk.Combobox(
            frame_form, width=18, font=("Segoe UI", 10), state="readonly"
        )
        self.cb_mahd.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(
            frame_form, text="Thời gian (tháng):", bg="white", font=("Segoe UI", 10)
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.txt_thoigian = ttk.Entry(frame_form, width=20)
        self.txt_thoigian.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Điều kiện:", bg="white", font=("Segoe UI", 10)).grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )
        self.txt_dieukien = ttk.Entry(frame_form, width=40)
        self.txt_dieukien.grid(
            row=1, column=3, columnspan=3, padx=5, pady=5, sticky="we"
        )

        tk.Label(frame_form, text="Ngày BH:", bg="white", font=("Segoe UI", 10)).grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.date_ngaybaohanh = DateEntry(
            frame_form, width=17, font=("Segoe UI", 10), date_pattern="dd/mm/yyyy"
        )
        self.date_ngaybaohanh.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(
            frame_form, text="Trạng thái:", bg="white", font=("Segoe UI", 10)
        ).grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self.lbl_trangthai = tk.Label(
            frame_form, text="", bg="white", font=("Segoe UI", 10, "bold")
        )
        self.lbl_trangthai.grid(row=2, column=3, sticky="w", padx=5, pady=5)

        # === NÚT CHỨC NĂNG ===
        frame_buttons = tk.Frame(self, bg="white")
        frame_buttons.pack(pady=10)

        tk.Button(
            frame_buttons,
            text="Thêm",
            bg="#43A047",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=5,
            bd=0,
            command=self.them,
        ).grid(row=0, column=0, padx=8)
        tk.Button(
            frame_buttons,
            text="Sửa",
            bg="#FB8C00",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=5,
            bd=0,
            command=self.sua,
        ).grid(row=0, column=1, padx=8)
        tk.Button(
            frame_buttons,
            text="Xóa",
            bg="#E53935",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=5,
            bd=0,
            command=self.xoa,
        ).grid(row=0, column=2, padx=8)
        tk.Button(
            frame_buttons,
            text="Làm mới",
            bg="#1E88E5",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=5,
            bd=0,
            command=self.lammoi,
        ).grid(row=0, column=3, padx=8)
        tk.Button(
            frame_buttons,
            text="Lưu",
            bg="#8E24AA",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=5,
            bd=0,
            command=self.luu,
        ).grid(row=0, column=4, padx=8)

        # === BẢNG HIỂN THỊ ===
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "MaBH",
            "MaTivi",
            "MaHD",
            "ThoiGianBaoHanh",
            "DieuKien",
            "NgayBaoHanh",
            "TrangThai",
        )

        scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")

        self.trHienThi = ttk.Treeview(
            frame_table,
            columns=columns,
            show="headings",
            height=14,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.trHienThi.pack(fill="both", expand=True)

        self.trHienThi.heading("MaBH", text="Mã BH")
        self.trHienThi.heading("MaTivi", text="Mã Tivi")
        self.trHienThi.heading("MaHD", text="Mã HD")
        self.trHienThi.heading("ThoiGianBaoHanh", text="Thời gian (tháng)")
        self.trHienThi.heading("DieuKien", text="Điều kiện")
        self.trHienThi.heading("NgayBaoHanh", text="Ngày BH")
        self.trHienThi.heading("TrangThai", text="Trạng thái")

        self.trHienThi.column("MaBH", width=100, anchor="center")
        self.trHienThi.column("MaTivi", width=100, anchor="center")
        self.trHienThi.column("MaHD", width=100, anchor="center")
        self.trHienThi.column("ThoiGianBaoHanh", width=100, anchor="center")
        self.trHienThi.column("DieuKien", width=250, anchor="w")
        self.trHienThi.column("NgayBaoHanh", width=110, anchor="center")
        self.trHienThi.column("TrangThai", width=120, anchor="center")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)

        self.trHienThi.bind("<<TreeviewSelect>>", self.chon_dong)

        self.hien_thi_du_lieu_tivi_mahd()
        self.hienthi_dulieu()

    def hien_thi_du_lieu_tivi_mahd(self):
        try:
            self.cursor.execute(
                """
                SELECT DISTINCT cthd.MaTivi
                FROM ChiTietHoaDon cthd
                JOIN HoaDonBan hdb ON hdb.MaHD = cthd.MaHD
                WHERE hdb.TrangThai = N'Đã thanh toán'
                ORDER BY cthd.MaTivi
            """
            )
            rows = self.cursor.fetchall()
            self.cb_mativi["values"] = [row.MaTivi for row in rows]
            if rows:
                self.cb_mativi.current(0)
                self.capnhat_mahd_theo_tivi()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không tải được danh sách Tivi: {e}")

    def capnhat_mahd_theo_tivi(self):
        mativi = self.cb_mativi.get()
        if not mativi:
            self.cb_mahd["values"] = []
            return
        try:
            self.cursor.execute(
                """
                SELECT cthd.MaHD
                FROM ChiTietHoaDon cthd
                JOIN HoaDonBan hdb ON hdb.MaHD = cthd.MaHD
                WHERE cthd.MaTivi = ? AND hdb.TrangThai = N'Đã thanh toán'
                ORDER BY cthd.MaHD
            """,
                (mativi,),
            )
            rows = self.cursor.fetchall()
            self.cb_mahd["values"] = [row.MaHD for row in rows]
            if rows:
                self.cb_mahd.current(0)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không tải được danh sách HD: {e}")

    def hienthi_dulieu(self):
        for item in self.trHienThi.get_children():
            self.trHienThi.delete(item)

        try:
            self.cursor.execute(
                """
                SELECT MaBH, MaTivi, MaHD, ThoiGianBaoHanh, DieuKien, NgayBaoHanh
                FROM BaoHanh
                ORDER BY MaBH
            """
            )
            rows = self.cursor.fetchall()

            for row in rows:
                ngay_bh = (
                    row.NgayBaoHanh
                    if isinstance(row.NgayBaoHanh, date)
                    else date.fromisoformat(str(row.NgayBaoHanh).split()[0])
                )
                ngay_het = ngay_bh + timedelta(days=row.ThoiGianBaoHanh * 30)
                trangthai = "CÒN HẠN" if ngay_het >= date.today() else "HẾT HẠN"

                self.trHienThi.insert(
                    "",
                    "end",
                    values=(
                        row.MaBH,
                        row.MaTivi,
                        row.MaHD,
                        row.ThoiGianBaoHanh,
                        row.DieuKien or "",
                        self.chuyen_yyyy_sang_dd(row.NgayBaoHanh),
                        trangthai,
                    ),
                )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")
    
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

    def chon_dong(self, event):
        selected = self.trHienThi.selection()
        if not selected:
            return

        values = self.trHienThi.item(selected[0])["values"]
        self.xoa_form()

        self.txt_mabh.insert(0, values[0])
        self.cb_mativi.set(values[1])
        self.capnhat_mahd_theo_tivi()
        self.cb_mahd.set(values[2])
        self.txt_thoigian.insert(0, values[3])
        self.txt_dieukien.insert(0, values[4])

        d, m, y = map(int, values[5].split("/"))
        self.date_ngaybaohanh.set_date(date(y, m, d))

        self.lbl_trangthai.config(
            text=(
                "CÒN HẠN BẢO HÀNH" if values[6] == "CÒN HẠN" else "ĐÃ HẾT HẠN BẢO HÀNH"
            ),
            fg="green" if values[6] == "CÒN HẠN" else "red",
        )

    def them(self):
        mabh = self.txt_mabh.get().strip()
        mativi = self.cb_mativi.get()
        mahd = self.cb_mahd.get()
        thoigian = self.txt_thoigian.get().strip()
        dieukien = self.txt_dieukien.get().strip()
        ngaybh = self.date_ngaybaohanh.get_date()

        if not all([mabh, mativi, mahd, thoigian]):
            messagebox.showwarning(
                "Cảnh báo", "Vui lòng nhập đầy đủ thông tin bắt buộc!"
            )
            return

        try:
            thoigian_int = int(thoigian)
            if thoigian_int <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Cảnh báo", "Thời gian phải là số nguyên dương!")
            return

        for item in self.trHienThi.get_children():
            if self.trHienThi.item(item)["values"][0] == mabh:
                messagebox.showwarning("Cảnh báo", f"Mã BH '{mabh}' đã tồn tại!")
                return

        ngay_het = ngaybh + timedelta(days=thoigian_int * 30)
        trangthai = "CÒN HẠN" if ngay_het >= date.today() else "HẾT HẠN"

        self.trHienThi.insert(
            "",
            "end",
            values=(
                mabh,
                mativi,
                mahd,
                thoigian_int,
                dieukien,
                self.chuyen_yyyy_sang_dd(ngaybh),
                trangthai,
            ),
        )

        self.ds_them.append((mabh, mativi, mahd, thoigian_int, dieukien, ngaybh))
        self.xoa_form()
        messagebox.showinfo("Thành công", "Đã thêm! Nhấn 'Lưu' để lưu vào CSDL.")

    def sua(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Chọn dòng cần sửa!")
            return

        mabh = self.txt_mabh.get().strip()
        mativi = self.cb_mativi.get()
        mahd = self.cb_mahd.get()
        thoigian = self.txt_thoigian.get().strip()
        dieukien = self.txt_dieukien.get().strip()
        ngaybh = self.date_ngaybaohanh.get_date()

        if not all([mabh, mativi, mahd, thoigian]):
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ!")
            return

        try:
            thoigian_int = int(thoigian)
            if thoigian_int <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Cảnh báo", "Thời gian phải là số nguyên dương!")
            return

        old_mabh = self.trHienThi.item(selected[0])["values"][0]
        ngay_het = ngaybh + timedelta(days=thoigian_int * 30)
        trangthai = "CÒN HẠN" if ngay_het >= date.today() else "HẾT HẠN"

        self.trHienThi.item(
            selected[0],
            values=(
                mabh,
                mativi,
                mahd,
                thoigian_int,
                dieukien,
                self.chuyen_yyyy_sang_dd(ngaybh),
                trangthai,
            ),
        )

        self.ds_sua = [x for x in self.ds_sua if x[0] != old_mabh]
        self.ds_sua.append(
            (mabh, mativi, mahd, thoigian_int, dieukien, ngaybh, old_mabh)
        )

        self.xoa_form()
        messagebox.showinfo("Thành công", "Đã sửa! Nhấn 'Lưu' để cập nhật.")

    def xoa(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Chọn dòng cần xóa!")
            return

        if not messagebox.askyesno("Xác nhận", "Xóa dòng này?"):
            return

        mabh = self.trHienThi.item(selected[0])["values"][0]
        self.trHienThi.delete(selected[0])

        self.ds_them = [x for x in self.ds_them if x[0] != mabh]
        if mabh not in self.ds_xoa:
            self.ds_xoa.append(mabh)

        self.xoa_form()
        messagebox.showinfo("Thành công", "Đã xóa! Nhấn 'Lưu' để cập nhật CSDL.")

    def luu(self):
        if not (self.ds_them or self.ds_sua or self.ds_xoa):
            messagebox.showinfo("Thông báo", "Không có thay đổi!")
            return

        if not messagebox.askyesno("Xác nhận", "Lưu tất cả thay đổi?"):
            return

        try:
            for mabh in self.ds_xoa:
                self.cursor.execute("DELETE FROM BaoHanh WHERE MaBH = ?", (mabh,))

            for mabh, mativi, mahd, thoigian, dieukien, ngaybh in self.ds_them:
                ngaybh_str = ngaybh.strftime('%Y-%m-%d')
                self.cursor.execute(
                    """
                    INSERT INTO BaoHanh (MaBH, MaTivi, MaHD, ThoiGianBaoHanh, DieuKien, NgayBaoHanh)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (mabh, mativi, mahd, thoigian, dieukien, ngaybh_str),
                )

            for mabh, mativi, mahd, thoigian, dieukien, ngaybh, old_mabh in self.ds_sua:
                ngaybh_str = ngaybh.strftime('%Y-%m-%d')
                self.cursor.execute(
                    """
                    UPDATE BaoHanh SET MaBH=?, MaTivi=?, MaHD=?, ThoiGianBaoHanh=?, DieuKien=?, NgayBaoHanh=?
                    WHERE MaBH=?
                """,
                    (mabh, mativi, mahd, thoigian, dieukien, ngaybh_str, old_mabh),
                )

            self.conn.commit()
            messagebox.showinfo("Thành công", "Đã lưu tất cả thay đổi!")

        except pyodbc.IntegrityError as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi FK", f"Vi phạm ràng buộc:\n{e}")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi CSDL: {e}")

        self.hienthi_dulieu()
        self.xoa_form()
        self.ds_them.clear()
        self.ds_sua.clear()
        self.ds_xoa.clear()

    def lammoi(self):
        if messagebox.askyesno("Xác nhận", "Hủy tất cả thay đổi?"):
            self.ds_them.clear()
            self.ds_sua.clear()
            self.ds_xoa.clear()
            self.hienthi_dulieu()
            self.xoa_form()
            self.txt_timkiem.delete(0, tk.END)

    def timkiem(self):
        keyword = self.txt_timkiem.get().strip()
        if not keyword:
            self.hienthi_dulieu()
            return

        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            option = self.search_option.get()
            sql = ""
            param = f"%{keyword}%"

            if option == "mabh":
                sql = "SELECT * FROM BaoHanh WHERE MaBH LIKE ?"
            elif option == "mativi":
                sql = "SELECT * FROM BaoHanh WHERE MaTivi LIKE ?"
            elif option == "mahd":
                sql = "SELECT * FROM BaoHanh WHERE MaHD LIKE ?"

            self.cursor.execute(sql, (param,))
            rows = self.cursor.fetchall()

            for row in rows:
                ngay_bh = (
                    row.NgayBaoHanh
                    if isinstance(row.NgayBaoHanh, date)
                    else date.fromisoformat(str(row.NgayBaoHanh).split()[0])
                )
                ngay_het = ngay_bh + timedelta(days=row.ThoiGianBaoHanh * 30)
                tt = "CÒN HẠN" if ngay_het >= date.today() else "HẾT HẠN"

                self.trHienThi.insert(
                    "",
                    "end",
                    values=(
                        row.MaBH,
                        row.MaTivi,
                        row.MaHD,
                        row.ThoiGianBaoHanh,
                        row.DieuKien or "",
                        ngay_bh,
                        tt,
                    ),
                )

            if not rows:
                messagebox.showinfo("Thông báo", "Không tìm thấy!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Tìm kiếm lỗi: {e}")

    def xoa_form(self):
        self.txt_mabh.delete(0, tk.END)
        self.cb_mativi.set("")
        self.cb_mahd.set("")
        self.txt_thoigian.delete(0, tk.END)
        self.txt_dieukien.delete(0, tk.END)
        self.date_ngaybaohanh.set_date(date.today())
        self.lbl_trangthai.config(text="")

    def huy(self):
        self.txt_timkiem.delete(0, tk.END)
        self.hienthi_dulieu()
