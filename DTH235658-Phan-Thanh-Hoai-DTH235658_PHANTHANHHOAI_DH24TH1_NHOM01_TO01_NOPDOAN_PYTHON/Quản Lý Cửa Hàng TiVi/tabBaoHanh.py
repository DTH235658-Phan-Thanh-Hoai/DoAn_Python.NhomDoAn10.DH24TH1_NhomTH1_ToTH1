import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, timedelta, datetime
import pyodbc


# === TAB BẢO HÀNH ===
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
            frame_search, text="🔍 Tìm kiếm:", font=("Segoe UI", 10), bg="#E3F2FD"
        ).pack(side="left", padx=5)
        self.txt_timkiem = tk.Entry(
            frame_search, font=("Segoe UI", 10), width=65, bg="white"
        )
        self.txt_timkiem.pack(side="left", padx=5)
        self.txt_timkiem.bind("<Return>", lambda e: self.timkiem())

        self.search_option = tk.StringVar(value="mabh")
        tk.Radiobutton(
            frame_search,
            text="Theo mã bảo hành",
            variable=self.search_option,
            value="mabh",
            bg="#E3F2FD",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=10)
        tk.Radiobutton(
            frame_search,
            text="Theo mã Tivi",
            variable=self.search_option,
            value="mativi",
            bg="#E3F2FD",
            font=("Segoe UI", 10),
        ).pack(side="left")
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
            bg="#1565C0",
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

        # Dòng 1
        tk.Label(
            frame_form, text="Mã bảo hành:", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_mabh = ttk.Entry(frame_form, width=32)
        self.txt_mabh.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Mã Tivi:", bg="white", font=("Segoe UI", 10)).grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )
        self.txt_mativi = ttk.Entry(frame_form, width=32)
        self.txt_mativi.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(
            frame_form, text="Thời gian BH (tháng):", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.txt_thoigian = ttk.Entry(frame_form, width=32)
        self.txt_thoigian.grid(row=0, column=5, padx=5, pady=5)

        # Dòng 2
        tk.Label(frame_form, text="Điều kiện:", bg="white", font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.txt_dieukien = ttk.Entry(frame_form, width=32)
        self.txt_dieukien.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(
            frame_form, text="Ngày bảo hành:", bg="white", font=("Segoe UI", 10)
        ).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.date_ngaybaohanh = DateEntry(
            frame_form, width=30, font=("Segoe UI", 10), date_pattern="dd/mm/yyyy"
        )
        self.date_ngaybaohanh.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(
            frame_form, text="Trạng thái:", bg="white", font=("Segoe UI", 10)
        ).grid(row=1, column=4, sticky="w", padx=5, pady=5)
        self.lbl_trangthai = tk.Label(
            frame_form, text="", bg="white", font=("Segoe UI", 10, "bold")
        )
        self.lbl_trangthai.grid(row=1, column=5, sticky="w", padx=5, pady=5)

        # ==== NÚT CHỨC NĂNG ====
        frame_buttons = tk.Frame(self, bg="white")
        frame_buttons.pack(pady=10)

        btn_them = tk.Button(
            frame_buttons,
            text="➕ Thêm",
            bg="#EBDA42",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=5,
            bd=0,
            command=self.them,
        )
        btn_them.grid(row=0, column=0, padx=10)

        btn_sua = tk.Button(
            frame_buttons,
            text="✏️ Sửa",
            bg="#FB8C00",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=5,
            bd=0,
            command=self.sua,
        )
        btn_sua.grid(row=0, column=1, padx=10)

        btn_xoa = tk.Button(
            frame_buttons,
            text="🗑️ Xóa",
            bg="#E53935",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=5,
            bd=0,
            command=self.xoa,
        )
        btn_xoa.grid(row=0, column=2, padx=10)

        btn_lammoi = tk.Button(
            frame_buttons,
            text="🔄 Làm mới",
            bg="#1E88E5",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=5,
            bd=0,
            command=self.lammoi,
        )
        btn_lammoi.grid(row=0, column=3, padx=10)

        btn_luu = tk.Button(
            frame_buttons,
            text="💾 Lưu",
            bg="#43A047",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=5,
            bd=0,
            command=self.luu,
        )
        btn_luu.grid(row=0, column=4, padx=10)

        # === BẢNG BẢO HÀNH ===
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        columns = (
            "MaBH",
            "MaTivi",
            "ThoiGianBaoHanh",
            "DieuKien",
            "NgayBaoHanh",
            "TrangThai",
        )
        self.trHienThi = ttk.Treeview(
            frame_table,
            show="headings",
            height=12,
            columns=columns,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )

        scroll_y.config(command=self.trHienThi.yview)
        scroll_x.config(command=self.trHienThi.xview)

        self.trHienThi.heading("MaBH", text="Mã Bảo Hành")
        self.trHienThi.heading("MaTivi", text="Mã Tivi")
        self.trHienThi.heading("ThoiGianBaoHanh", text="Thời Gian (tháng)")
        self.trHienThi.heading("DieuKien", text="Điều Kiện")
        self.trHienThi.heading("NgayBaoHanh", text="Ngày Bảo Hành")
        self.trHienThi.heading("TrangThai", text="Trạng Thái")

        self.trHienThi.column("MaBH", width=120, anchor="center")
        self.trHienThi.column("MaTivi", width=100, anchor="center")
        self.trHienThi.column("ThoiGianBaoHanh", width=130, anchor="center")
        self.trHienThi.column("DieuKien", width=200, anchor="w")
        self.trHienThi.column("NgayBaoHanh", width=120, anchor="center")
        self.trHienThi.column("TrangThai", width=120, anchor="center")

        self.trHienThi.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        self.trHienThi.bind("<<TreeviewSelect>>", self.chon_dong)

        self.hienthi_dulieu()

    def hienthi_dulieu(self):
        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            self.cursor.execute(
                "SELECT MaBH, MaTivi, ThoiGianBaoHanh, DieuKien, NgayBaoHanh FROM BaoHanh"
            )
            rows = self.cursor.fetchall()

            for row in rows:
                ngay_baohanh = row.NgayBaoHanh
                thoi_gian = row.ThoiGianBaoHanh

                if isinstance(ngay_baohanh, str):
                    ngay_baohanh = date.fromisoformat(ngay_baohanh)

                ngay_hethan = ngay_baohanh + timedelta(days=thoi_gian * 30)
                trangthai = "CÒN HẠN" if ngay_hethan >= date.today() else "HẾT HẠN"

                self.trHienThi.insert(
                    "",
                    "end",
                    values=(
                        row.MaBH,
                        row.MaTivi,
                        row.ThoiGianBaoHanh,
                        row.DieuKien if row.DieuKien else "",
                        ngay_baohanh.strftime("%d/%m/%Y"),
                        trangthai,
                    ),
                )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def chon_dong(self, event):
        selected = self.trHienThi.selection()
        if selected:
            item = self.trHienThi.item(selected[0])
            values = item["values"]

            self.xoa_form()

            self.txt_mabh.insert(0, values[0])
            self.txt_mativi.insert(0, values[1])
            self.txt_thoigian.insert(0, values[2])
            self.txt_dieukien.insert(0, values[3] if values[3] else "")

            ngay_parts = values[4].split("/")
            self.date_ngaybaohanh.set_date(
                date(int(ngay_parts[2]), int(ngay_parts[1]), int(ngay_parts[0]))
            )

            if values[5] == "CÒN HẠN":
                self.lbl_trangthai.config(text="CÒN HẠN BẢO HÀNH", fg="green")
            else:
                self.lbl_trangthai.config(text="ĐÃ HẾT HẠN BẢO HÀNH", fg="red")

    def them(self):
        mabh = self.txt_mabh.get().strip()
        mativi = self.txt_mativi.get().strip()
        thoigian = self.txt_thoigian.get().strip()
        dieukien = self.txt_dieukien.get().strip()
        ngaybaohanh = self.date_ngaybaohanh.get_date()

        if not mabh:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã bảo hành!")
            self.txt_mabh.focus()
            return

        if not mativi:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã Tivi!")
            self.txt_mativi.focus()
            return

        if not thoigian:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Thời gian bảo hành!")
            self.txt_thoigian.focus()
            return

        try:
            thoigian_int = int(thoigian)
            if thoigian_int <= 0:
                messagebox.showwarning("Cảnh báo", "Thời gian bảo hành phải lớn hơn 0!")
                self.txt_thoigian.focus()
                return
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Thời gian bảo hành phải là số!")
            self.txt_thoigian.focus()
            return

        for item in self.trHienThi.get_children():
            if self.trHienThi.item(item)["values"][0] == mabh:
                messagebox.showwarning("Cảnh báo", f"Mã bảo hành '{mabh}' đã tồn tại!")
                return

        ngay_hethan = ngaybaohanh + timedelta(days=thoigian_int * 30)
        trangthai = "CÒN HẠN" if ngay_hethan >= date.today() else "HẾT HẠN"

        self.trHienThi.insert(
            "",
            "end",
            values=(
                mabh,
                mativi,
                thoigian_int,
                dieukien,
                ngaybaohanh.strftime("%d/%m/%Y"),
                trangthai,
            ),
        )

        self.ds_them.append((mabh, mativi, thoigian_int, dieukien, ngaybaohanh))

        self.xoa_form()
        messagebox.showinfo(
            "Thành công", "Đã thêm dòng mới! Nhấn 'Lưu' để lưu vào CSDL."
        )

    def sua(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần sửa!")
            return

        mabh = self.txt_mabh.get().strip()
        mativi = self.txt_mativi.get().strip()
        thoigian = self.txt_thoigian.get().strip()
        dieukien = self.txt_dieukien.get().strip()
        ngaybaohanh = self.date_ngaybaohanh.get_date()

        if not mabh:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã bảo hành!")
            return

        if not mativi:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã Tivi!")
            return

        if not thoigian:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Thời gian bảo hành!")
            return

        try:
            thoigian_int = int(thoigian)
            if thoigian_int <= 0:
                messagebox.showwarning("Cảnh báo", "Thời gian bảo hành phải lớn hơn 0!")
                return
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Thời gian bảo hành phải là số!")
            return

        item = self.trHienThi.item(selected[0])
        mabh_cu = item["values"][0]

        ngay_hethan = ngaybaohanh + timedelta(days=thoigian_int * 30)
        trangthai = "CÒN HẠN" if ngay_hethan >= date.today() else "HẾT HẠN"

        self.trHienThi.item(
            selected[0],
            values=(
                mabh,
                mativi,
                thoigian_int,
                dieukien,
                ngaybaohanh.strftime("%d/%m/%Y"),
                trangthai,
            ),
        )

        is_new = any(x[0] == mabh_cu for x in self.ds_them)
        if not is_new:
            self.ds_sua = [x for x in self.ds_sua if x[0] != mabh_cu]
            self.ds_sua.append(
                (mabh, mativi, thoigian_int, dieukien, ngaybaohanh, mabh_cu)
            )
        else:
            self.ds_them = [
                (
                    (mabh, mativi, thoigian_int, dieukien, ngaybaohanh)
                    if x[0] == mabh_cu
                    else x
                )
                for x in self.ds_them
            ]

        self.xoa_form()
        messagebox.showinfo(
            "Thành công", "Đã cập nhật dòng! Nhấn 'Lưu' để lưu vào CSDL."
        )

    def xoa(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần xóa!")
            return

        xacnhan = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa dòng này?")
        if not xacnhan:
            return

        item = self.trHienThi.item(selected[0])
        mabh = item["values"][0]

        self.trHienThi.delete(selected[0])

        is_new = any(x[0] == mabh for x in self.ds_them)
        if is_new:
            self.ds_them = [x for x in self.ds_them if x[0] != mabh]
        else:
            if mabh not in self.ds_xoa:
                self.ds_xoa.append(mabh)

        self.xoa_form()
        messagebox.showinfo("Thành công", "Đã xóa dòng! Nhấn 'Lưu' để lưu vào CSDL.")

    def luu(self):
        try:
            if not self.ds_them and not self.ds_sua and not self.ds_xoa:
                messagebox.showinfo("Thông báo", "Không có thay đổi để lưu!")
                return

            confirm = messagebox.askyesno(
                "Xác nhận", "Bạn có chắc muốn lưu các thay đổi?"
            )
            if not confirm:
                return

            for mabh in self.ds_xoa:
                self.cursor.execute("DELETE FROM BaoHanh WHERE MaBH = ?", (mabh,))

            for mabh, mativi, thoigian, dieukien, ngaybaohanh in self.ds_them:
                if isinstance(ngaybaohanh, date):
                    ngaybaohanh_str = ngaybaohanh.strftime("%Y-%m-%d")
                else:
                    ngaybaohanh_str = ngaybaohanh

                self.cursor.execute(
                    """
                    INSERT INTO BaoHanh (MaBH, MaTivi, ThoiGianBaoHanh, DieuKien, NgayBaoHanh)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (mabh, mativi, thoigian, dieukien, ngaybaohanh_str),
                )

            for mabh, mativi, thoigian, dieukien, ngaybaohanh, mabh_cu in self.ds_sua:
                if isinstance(ngaybaohanh, date):
                    ngaybaohanh_str = ngaybaohanh.strftime("%Y-%m-%d")
                else:
                    ngaybaohanh_str = ngaybaohanh

                self.cursor.execute(
                    """
                    UPDATE BaoHanh
                    SET MaBH=?, MaTivi=?, ThoiGianBaoHanh=?, DieuKien=?, NgayBaoHanh=?
                    WHERE MaBH=?
                """,
                    (mabh, mativi, thoigian, dieukien, ngaybaohanh_str, mabh_cu),
                )

            self.conn.commit()

            messagebox.showinfo("Thành công", "Đã lưu thay đổi vào CSDL!")

        except pyodbc.IntegrityError as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi ràng buộc dữ liệu: {str(e)}")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {str(e)}")

        self.hienthi_dulieu()
        self.xoa_form()
        self.ds_them.clear()
        self.ds_sua.clear()
        self.ds_xoa.clear()

    def lammoi(self):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn hủy các thay đổi?")
        if not confirm:
            return

        self.ds_them.clear()
        self.ds_sua.clear()
        self.ds_xoa.clear()

        self.hienthi_dulieu()
        self.xoa_form()
        self.txt_timkiem.delete(0, tk.END)
        messagebox.showinfo("Thông báo", "Đã làm mới dữ liệu!")

    def timkiem(self):
        tu_khoa_tim = self.txt_timkiem.get().strip()
        if not tu_khoa_tim:
            messagebox.showinfo("Thông báo", "Vui lòng nhập từ khóa tìm kiếm.")
            self.hienthi_dulieu()
            return

        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            if self.search_option.get() == "mabh":
                self.cursor.execute(
                    "SELECT MaBH, MaTivi, ThoiGianBaoHanh, DieuKien, NgayBaoHanh FROM BaoHanh WHERE MaBH LIKE ? ORDER BY MaBH",
                    (f"%{tu_khoa_tim}%",),
                )
            else:
                self.cursor.execute(
                    "SELECT MaBH, MaTivi, ThoiGianBaoHanh, DieuKien, NgayBaoHanh FROM BaoHanh WHERE MaTivi LIKE ? ORDER BY MaBH",
                    (f"%{tu_khoa_tim}%",),
                )

            rows = self.cursor.fetchall()

            for row in rows:
                ngay_baohanh = row.NgayBaoHanh
                thoi_gian = row.ThoiGianBaoHanh

                if isinstance(ngay_baohanh, str):
                    ngay_baohanh = date.fromisoformat(ngay_baohanh)

                ngay_hethan = ngay_baohanh + timedelta(days=thoi_gian * 30)
                trangthai = "CÒN HẠN" if ngay_hethan >= date.today() else "HẾT HẠN"

                self.trHienThi.insert(
                    "",
                    "end",
                    values=(
                        row.MaBH,
                        row.MaTivi,
                        row.ThoiGianBaoHanh,
                        row.DieuKien if row.DieuKien else "",
                        ngay_baohanh.strftime("%d/%m/%Y"),
                        trangthai,
                    ),
                )

            if not rows:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")

    def xoa_form(self):
        self.txt_mabh.delete(0, tk.END)
        self.txt_mativi.delete(0, tk.END)
        self.txt_thoigian.delete(0, tk.END)
        self.txt_dieukien.delete(0, tk.END)
        self.date_ngaybaohanh.set_date(date.today())
        self.lbl_trangthai.config(text="")

    def huy(self):
        self.txt_timkiem.delete(0, tk.END)
        self.hienthi_dulieu()
