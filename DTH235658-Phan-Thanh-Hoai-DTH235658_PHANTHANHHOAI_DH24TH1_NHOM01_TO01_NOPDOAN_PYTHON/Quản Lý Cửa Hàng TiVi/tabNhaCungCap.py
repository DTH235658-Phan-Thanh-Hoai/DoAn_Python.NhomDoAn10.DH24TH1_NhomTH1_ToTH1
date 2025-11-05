import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# Khong co ScrollBar


# === TAB NHÀ CUNG CẤP ===
class tabNhaCungCap(tk.Frame):
    def __init__(self, parent, conn):
        super().__init__(parent, bg="white")

        # === CHUỖI KẾT NỐI  ====
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
        self.txt_timkiem = tk.Entry(frame_search, font=("Segoe UI", 10), width=54)
        self.txt_timkiem.pack(side="left", padx=5)

        self.search_option = tk.StringVar(value="ma")
        self.rad_mahang = tk.Radiobutton(
            frame_search,
            text="Theo mã nhà cung cấp",
            variable=self.search_option,
            value="ma",
            bg="#E3F2FD",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=10)
        self.rad_tenhang = tk.Radiobutton(
            frame_search,
            text="Theo tên nhà cung cấp",
            variable=self.search_option,
            value="ten",
            bg="#E3F2FD",
            font=("Segoe UI", 10),
        ).pack(side="left")
        self.btn_timkiem = tk.Button(
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
            text="Thông tin Nhà cung cấp",
            bg="white",
            font=("Segoe UI", 12, "bold"),
            fg="#0D47A1",
            padx=10,
            pady=10,
        )
        frame_form.pack(fill="x", padx=20, pady=10)

        tk.Label(
            frame_form, text="Mã nhà cung cấp", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_ma = ttk.Entry(frame_form, width=29)
        self.txt_ma.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            frame_form, text="Tên nhà cung cấp:", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.txt_ten = ttk.Entry(frame_form, width=70)
        self.txt_ten.grid(row=0, column=3, columnspan=3, padx=5, pady=5)

        tk.Label(
            frame_form, text="Số điện thoại:", bg="white", font=("Segoe UI", 10)
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.txt_sodienthoai = ttk.Entry(frame_form, width=29)
        self.txt_sodienthoai.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Email:", bg="white", font=("Segoe UI", 10)).grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )
        self.txt_email = ttk.Entry(frame_form, width=29)
        self.txt_email.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Địa chỉ:", bg="white", font=("Segoe UI", 10)).grid(
            row=1, column=4, sticky="w", padx=5, pady=5
        )
        self.txt_diachi = ttk.Entry(frame_form, width=29)
        self.txt_diachi.grid(row=1, column=5, padx=5, pady=5)

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

        # === BẢNG NHÀ CUNG CẤP ===
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("MaNCC", "TenNCC", "DiaChi", "SoDienThoai", "Email")
        self.trHienThi = ttk.Treeview(
            frame_table, show="headings", height=12, columns=columns
        )

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        self.trHienThi.heading("MaNCC", text="Mã nhà cung cấp", anchor="center")
        self.trHienThi.heading("TenNCC", text="Tên nhà cung cấp", anchor="center")
        self.trHienThi.heading("DiaChi", text="Địa chi", anchor="center")
        self.trHienThi.heading("SoDienThoai", text="Số điện thoại", anchor="center")
        self.trHienThi.heading("Email", text="Email", anchor="center")

        self.trHienThi.column("MaNCC", width=100, anchor="center")
        self.trHienThi.column("TenNCC", width=200, anchor="center")
        self.trHienThi.column("DiaChi", width=200, anchor="center")
        self.trHienThi.column("SoDienThoai", width=150, anchor="center")
        self.trHienThi.column("Email", width=200, anchor="center")

        self.trHienThi.pack(fill="both", expand=True)

        self.trHienThi.bind("<<TreeviewSelect>>", self.chon_dong)

        self.hienthi_dulieu()

    def hienthi_dulieu(self):
        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            self.cursor.execute(
                "SELECT MaNCC, TenNCC, DiaChi, SoDienThoai, Email FROM NhaCungCap"
            )

            rows = self.cursor.fetchall()

            for row in rows:
                self.trHienThi.insert(
                    "", "end", values=(row[0], row[1], row[2], row[3], row[4])
                )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def chon_dong(self, event=None):
        selected = self.trHienThi.selection()
        if selected:
            item = self.trHienThi.item(selected[0])
            values = item["values"]

            self.xoa_form()

            self.txt_ma.insert(0, values[0])
            self.txt_ten.insert(0, values[1])
            self.txt_diachi.insert(0, values[2])
            self.txt_sodienthoai.insert(0, values[3])
            self.txt_email.insert(0, values[4])

    def them(self):
        ma = self.txt_ma.get().strip()
        ten = self.txt_ten.get().strip()
        email = self.txt_email.get().strip()
        diachi = self.txt_diachi.get().strip()
        sodienthoai = self.txt_sodienthoai.get().strip()

        if not ma:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã nhà cung cấp!")
            return

        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Tên nhà cung cấp!")
            return

        for item in self.trHienThi.get_children():
            if self.trHienThi.item(item)["values"][0] == ma:
                messagebox.showwarning(
                    "Cảnh báo", f"Mã nhà cung cấp '{ma}' dã tốn tại!"
                )
                return

        self.trHienThi.insert("", "end", values=(ma, ten, diachi, sodienthoai, email))

        self.ds_them.append((ma, ten, diachi, sodienthoai, email))

        self.xoa_form()
        messagebox.showinfo("Thêm nhà cung cấp", "Thêm nhà cung cấp thành công!")

    def sua(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần sửa!")
            return

        ma = self.txt_ma.get().strip()
        ten = self.txt_ten.get().strip()
        email = self.txt_email.get().strip()
        sodienthoai = self.txt_sodienthoai.get().strip()
        diachi = self.txt_diachi.get().strip()

        if not ma:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã nhà cung cấp!")
            return

        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Tên nhà cung cấp!")
            return

        item = self.trHienThi.item(selected[0])
        ma_cu = item["values"][0]

        self.trHienThi.item(selected[0], values=(ma, ten, diachi, sodienthoai, email))

        is_new = any(x[0] == ma_cu for x in self.ds_them)

        if not is_new:
            self.ds_sua = [x for x in self.ds_sua if x[0] != ma_cu]
            self.ds_sua.append((ma, ten, diachi, sodienthoai, email, ma_cu))
        else:
            self.ds_them = [
                (ma, ten, diachi, sodienthoai, email) if x[0] == ma_cu else x
                for x in self.ds_them
            ]

        self.xoa_form()
        messagebox.showinfo(
            "Cập nhật nhà cung cấp", "Cập nhật nhà cung cấp thành công!"
        )

    def xoa(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui long chọn dòng cần xóa!")
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

            xacnhan = messagebox.askyesno("Xac nhan", "Ban co chac muon luu khong?")

            if not xacnhan:
                return

            for ma in self.ds_xoa:
                self.cursor.execute("DELETE FROM NhaCungCap WHERE MaNCC = ?", (ma))

            for ma, ten, diachi, sodienthoai, email in self.ds_them:
                self.cursor.execute(
                    "INSERT INTO NhaCungCap (MaNCC, TenNCC, DiaChi, SoDienThoai, Email) VALUES (?, ?, ?, ?, ?)",
                    (ma, ten, diachi, sodienthoai, email),
                )

            for ma, ten, diachi, sodienthoai, email, ma_cu in self.ds_sua:
                self.cursor.execute(
                    "UPDATE NhaCungCap SET MaNCC=?, TenNCC=?, DiaChi=?, SoDienThoai=?, Email=? WHERE MaNCC=?",
                    (ma, ten, diachi, sodienthoai, email, ma_cu),
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
                    "SELECT MaNCC, TenNCC, Email, SoDienThoai, DiaChi FROM NhaCungCap WHERE MaNCC LIKE ?",
                    (f"%{tu_khoa_tim}%",),
                )
            else:
                self.cursor.execute(
                    "SELECT MaNCC, TenNCC, Email, SoDienThoai, DiaChi FROM NhaCungCap WHERE TenNCC LIKE ?",
                    (f"%{tu_khoa_tim}%",),
                )

            rows = self.cursor.fetchall()

            for row in rows:
                self.trHienThi.insert(
                    "",
                    "end",
                    values=(
                        row.MaNCC,
                        row.TenNCC,
                        row.DiaChi,
                        row.SoDienThoai,
                        row.Email,
                    ),
                )

            if not rows:
                messagebox.showinfo("Kết quả", "Không tìm thể thay đổi!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def xoa_form(self):
        self.txt_ma.delete(0, tk.END)
        self.txt_ten.delete(0, tk.END)
        self.txt_sodienthoai.delete(0, tk.END)
        self.txt_email.delete(0, tk.END)
        self.txt_diachi.delete(0, tk.END)

    def huy(self):
        self.txt_timkiem.delete(0, tk.END)
        self.hienthi_dulieu()