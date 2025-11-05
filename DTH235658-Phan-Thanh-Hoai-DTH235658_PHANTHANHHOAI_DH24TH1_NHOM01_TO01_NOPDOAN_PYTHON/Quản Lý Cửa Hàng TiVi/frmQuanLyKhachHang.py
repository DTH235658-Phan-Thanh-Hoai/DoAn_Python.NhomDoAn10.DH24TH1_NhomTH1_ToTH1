import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc


# === TAB KHÁCH HÀNG ===
class QuanLyKhachHang(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent, bg="white")

        self.conn = conn
        self.cursor = conn.cursor()

        self.ds_them = []
        self.ds_sua = []
        self.ds_xoa = []

        lbl_title = tk.Label(self, text="QUẢN LÝ KHÁCH HÀNG", font=("Segoe UI", 16, "bold"), bg="white", fg="#0D47A1",)
        lbl_title.pack()

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

        self.search_option = tk.StringVar(value="ma")
        tk.Radiobutton(
            frame_search,
            text="Theo mã khách hàng",
            variable=self.search_option,
            value="ma",
            bg="#E3F2FD",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=10)
        tk.Radiobutton(
            frame_search,
            text="Theo tên khách hàng",
            variable=self.search_option,
            value="ten",
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
            text="Thông tin Khách hàng",
            bg="white",
            font=("Segoe UI", 12, "bold"),
            fg="#0D47A1",
            padx=10,
            pady=10,
        )
        frame_form.pack(fill="x", padx=20, pady=10)

        # Dòng 1
        tk.Label(
            frame_form, text="Mã khách hàng:", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_ma = ttk.Entry(frame_form, width=30)
        self.txt_ma.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            frame_form, text="Tên khách hàng:", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.txt_ten = ttk.Entry(frame_form, width=30)
        self.txt_ten.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(
            frame_form, text="Số điện thoại:", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.txt_sdt = ttk.Entry(frame_form, width=30)
        self.txt_sdt.grid(row=0, column=5, padx=5, pady=5)

        # Dòng 2
        tk.Label(frame_form, text="Email:", bg="white", font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.txt_email = ttk.Entry(frame_form, width=30)
        self.txt_email.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Địa chỉ:", bg="white", font=("Segoe UI", 10)).grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )
        self.txt_diachi = ttk.Entry(frame_form, width=66)
        self.txt_diachi.grid(row=1, column=3, columnspan=3, padx=5, pady=5, sticky="we")

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

        # === BẢNG KHÁCH HÀNG ===
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        self.trHienThi = ttk.Treeview(
            frame_table,
            columns=("MaKH", "TenKH", "SoDienThoai", "Email", "DiaChi"),
            show="headings",
            height=12,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )

        scroll_y.config(command=self.trHienThi.yview)
        scroll_x.config(command=self.trHienThi.xview)

        self.trHienThi.heading("MaKH", text="Mã Khách Hàng")
        self.trHienThi.heading("TenKH", text="Tên Khách Hàng")
        self.trHienThi.heading("SoDienThoai", text="Số Điện Thoại")
        self.trHienThi.heading("Email", text="Email")
        self.trHienThi.heading("DiaChi", text="Địa Chỉ")

        self.trHienThi.column("MaKH", width=120, anchor="center")
        self.trHienThi.column("TenKH", width=200, anchor="w")
        self.trHienThi.column("SoDienThoai", width=120, anchor="center")
        self.trHienThi.column("Email", width=200, anchor="w")
        self.trHienThi.column("DiaChi", width=250, anchor="w")

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
                "SELECT MaKH, TenKH, SoDienThoai, Email, DiaChi FROM KhachHang"
            )
            rows = self.cursor.fetchall()

            for row in rows:
                self.trHienThi.insert(
                    "",
                    "end",
                    values=(
                        row.MaKH,
                        row.TenKH,
                        row.SoDienThoai if row.SoDienThoai else "",
                        row.Email if row.Email else "",
                        row.DiaChi if row.DiaChi else "",
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

            self.txt_ma.insert(0, values[0])
            self.txt_ten.insert(0, values[1])
            self.txt_sdt.insert(0, values[2] if values[2] else "")
            self.txt_email.insert(0, values[3] if values[3] else "")
            self.txt_diachi.insert(0, values[4] if values[4] else "")

    def them(self):
        ma = self.txt_ma.get().strip()
        ten = self.txt_ten.get().strip()
        sdt = self.txt_sdt.get().strip()
        email = self.txt_email.get().strip()
        diachi = self.txt_diachi.get().strip()

        if not ma:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã khách hàng!")
            self.txt_ma.focus()
            return

        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Tên khách hàng!")
            self.txt_ten.focus()
            return

        for item in self.trHienThi.get_children():
            if self.trHienThi.item(item)["values"][0] == ma:
                messagebox.showwarning("Cảnh báo", f"Mã khách hàng '{ma}' đã tồn tại!")
                return

        self.trHienThi.insert("", "end", values=(ma, ten, sdt, email, diachi))

        self.ds_them.append((ma, ten, sdt, email, diachi))

        self.xoa_form()
        messagebox.showinfo(
            "Thành công", "Đã thêm dòng mới! Nhấn 'Lưu' để lưu vào CSDL."
        )

    def sua(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần sửa!")
            return

        ma = self.txt_ma.get().strip()
        ten = self.txt_ten.get().strip()
        sdt = self.txt_sdt.get().strip()
        email = self.txt_email.get().strip()
        diachi = self.txt_diachi.get().strip()

        if not ma:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã khách hàng!")
            return

        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Tên khách hàng!")
            return

        item = self.trHienThi.item(selected[0])
        ma_cu = item["values"][0]

        self.trHienThi.item(selected[0], values=(ma, ten, sdt, email, diachi))

        is_new = any(x[0] == ma_cu for x in self.ds_them)
        if not is_new:
            self.ds_sua = [x for x in self.ds_sua if x[0] != ma_cu]
            self.ds_sua.append((ma, ten, sdt, email, diachi, ma_cu))
        else:
            self.ds_them = [
                (ma, ten, sdt, email, diachi) if x[0] == ma_cu else x
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
        ma = item["values"][0]

        self.trHienThi.delete(selected[0])

        is_new = any(x[0] == ma for x in self.ds_them)
        if is_new:
            self.ds_them = [x for x in self.ds_them if x[0] != ma]
        else:
            if ma not in self.ds_xoa:
                self.ds_xoa.append(ma)

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

            for ma in self.ds_xoa:
                self.cursor.execute("DELETE FROM KhachHang WHERE MaKH = ?", (ma,))

            for ma, ten, sdt, email, diachi in self.ds_them:
                self.cursor.execute(
                    "INSERT INTO KhachHang (MaKH, TenKH, SoDienThoai, Email, DiaChi) VALUES (?, ?, ?, ?, ?)",
                    (ma, ten, sdt, email, diachi),
                )

            for ma, ten, sdt, email, diachi, ma_cu in self.ds_sua:
                self.cursor.execute(
                    "UPDATE KhachHang SET MaKH = ?, TenKH = ?, SoDienThoai = ?, Email = ?, DiaChi = ? WHERE MaKH = ?",
                    (ma, ten, sdt, email, diachi, ma_cu),
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

            if self.search_option.get() == "ma":
                self.cursor.execute(
                    "SELECT MaKH, TenKH, SoDienThoai, Email, DiaChi FROM KhachHang WHERE MaKH LIKE ? ORDER BY MaKH",
                    (f"%{tu_khoa_tim}%",),
                )
            else:
                self.cursor.execute(
                    "SELECT MaKH, TenKH, SoDienThoai, Email, DiaChi FROM KhachHang WHERE TenKH LIKE ? ORDER BY MaKH",
                    (f"%{tu_khoa_tim}%",),
                )

            rows = self.cursor.fetchall()

            for row in rows:
                self.trHienThi.insert(
                    "",
                    "end",
                    values=(
                        row.MaKH,
                        row.TenKH,
                        row.SoDienThoai if row.SoDienThoai else "",
                        row.Email if row.Email else "",
                        row.DiaChi if row.DiaChi else "",
                    ),
                )

            if not rows:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")

    def xoa_form(self):
        self.txt_ma.delete(0, tk.END)
        self.txt_ten.delete(0, tk.END)
        self.txt_sdt.delete(0, tk.END)
        self.txt_email.delete(0, tk.END)
        self.txt_diachi.delete(0, tk.END)

    def huy(self):
        self.txt_timkiem.delete(0, tk.END)
        self.hienthi_dulieu()
