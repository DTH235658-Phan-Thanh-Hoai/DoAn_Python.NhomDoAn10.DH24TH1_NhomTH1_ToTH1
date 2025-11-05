import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

PRIMARY_COLOR = "#0D47A1"
SECONDARY_COLOR = "#1565C0"
ACCENT_COLOR = "#42A5F5"
HIGHLIGHT_COLOR = "#BBDEFB"
TEXT_COLOR = "white"


class HeThong(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent, bg="white")
        self.user = user

        self.conn = conn
        self.cursor = conn.cursor()

        self.ds_them = []
        self.ds_sua = []
        self.ds_xoa = []

        lbl_title = tk.Label(
            self,
            text="QUẢN LÝ TÀI KHOẢN HỆ THỐNG",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#0D47A1",
        )
        lbl_title.pack()

        self.frame_search = tk.Frame(self, bg="#E3F2FD", padx=10, pady=10)
        self.frame_search.pack(fill="x", padx=20, pady=5)

        tk.Label(
            self.frame_search, text="🔍 Tìm kiếm:", font=("Segoe UI", 10), bg="#E3F2FD"
        ).pack(side="left", padx=5)
        self.txt_timkiem = tk.Entry(self.frame_search, font=("Segoe UI", 10), width=105)
        self.txt_timkiem.pack(side="left", padx=5)
        self.txt_timkiem.bind("<Return>", self.timkiem)
        tk.Button(
            self.frame_search,
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
            self.frame_search,
            text="Hủy",
            font=("Segoe UI", 10, "bold"),
            bg="#1565C0",
            fg="white",
            bd=0,
            padx=10,
            pady=5,
            command=self.huy,
        ).pack(side="left", padx=10)

        frame_form = tk.LabelFrame(
            self,
            text="Thông tin tài khoản",
            bg="white",
            font=("Segoe UI", 12, "bold"),
            fg="#0D47A1",
            padx=10,
            pady=10,
        )
        frame_form.pack(fill="x", padx=30, pady=10)

        tk.Label(
            frame_form, text="Tên đăng nhập:", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.txt_ten = ttk.Entry(frame_form, font=("Segoe UI", 10), width=48)
        self.txt_ten.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Mật khẩu:", bg="white", font=("Segoe UI", 10)).grid(
            row=0, column=2, sticky="w", pady=5, padx=5
        )
        self.txt_mk = ttk.Entry(frame_form, font=("Segoe UI", 10), width=48)
        self.txt_mk.grid(row=0, column=3, pady=5, padx=5)

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

        self.btn_sua = tk.Button(
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
        self.btn_sua.grid(row=0, column=1, padx=10)

        self.btn_xoa = tk.Button(
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
        self.btn_xoa.grid(row=0, column=2, padx=10)

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

        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("TenDangNhap", "MatKhau")
        self.trHienThi = ttk.Treeview(
            frame_table, show="headings", height=12, columns=columns
        )

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        self.trHienThi.heading("TenDangNhap", text="Tên đăng nhập", anchor="center")
        self.trHienThi.heading("MatKhau", text="Mật khẩu", anchor="center")

        self.trHienThi.column("TenDangNhap", width=400, anchor="center")
        self.trHienThi.column("MatKhau", width=400, anchor="center")

        self.trHienThi.pack(fill="both", expand=True)

        self.trHienThi.bind("<<TreeviewSelect>>", self.chon_dong)

        self.hienthi_dulieu()

    def hienthi_dulieu(self):
        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            if self.user != "admin":
                self.btn_sua.destroy()
                self.btn_xoa.destroy()
                self.trHienThi.destroy()
                self.frame_search.destroy()
                self.cursor.execute(
                    "SELECT TenDangNhap, MatKhau FROM TaiKhoan WHERE TenDangNhap = ?",
                    (self.user,),
                )
                row = self.cursor.fetchone()

                if row:
                    self.txt_ten.insert(0, row[0])
                    self.txt_ten.config(state="disabled")
                    self.txt_mk.insert(0, row[1])

            else:
                self.cursor.execute("SELECT TenDangNhap, MatKhau FROM TaiKhoan")
                rows = self.cursor.fetchall()

                for row in rows:
                    self.trHienThi.insert("", "end", values=(row[0], row[1]))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def chon_dong(self, event=None):
        selected = self.trHienThi.selection()
        if selected:
            item = self.trHienThi.item(selected[0])
            values = item["values"]

            self.xoa_form()

            self.txt_ten.insert(0, values[0])

            try:
                self.cursor.execute(
                    "SELECT MatKhau FROM TaiKhoan WHERE TenDangNhap = ?", (values[0],)
                )
                row = self.cursor.fetchone()
                if row:
                    self.txt_mk.insert(0, row[0])
            except Exception as e:
                print(f"Lỗi load mật khẩu: {str(e)}")

    def them(self):
        ten = self.txt_ten.get().strip()
        mk = self.txt_mk.get().strip()

        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Tên đăng nhập!")
            return

        if not mk:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mật khẩu!")
            return

        for item in self.trHienThi.get_children():
            if self.trHienThi.item(item)["values"][0] == ten:
                messagebox.showwarning("Cảnh báo", f"Tên đăng nhập '{ten}' đã tồn tại!")
                return

        self.trHienThi.insert("", "end", values=(ten, "●" * len(mk)))
        self.ds_them.append((ten, mk))

        self.xoa_form()
        messagebox.showinfo("Thêm tài khoản", "Thêm tài khoản thành công!")

    def sua(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần sửa!")
            return

        ten = self.txt_ten.get().strip()
        mk = self.txt_mk.get().strip()

        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Tên đăng nhập!")
            return

        if not mk:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mật khẩu!")
            return

        if self.user != "admin":
            self.ds_sua = [(mk, ten)]
            return

        item = self.trHienThi.item(selected[0])
        ten_cu = item["values"][0]

        self.trHienThi.item(selected[0], values=(ten, "●" * len(mk)))

        is_new = any(x[0] == ten_cu for x in self.ds_them)

        if not is_new:
            self.ds_sua = [x for x in self.ds_sua if x[0] != ten_cu]
            self.ds_sua.append((ten, mk, ten_cu))
        else:
            self.ds_them = [(ten, mk) if x[0] == ten_cu else x for x in self.ds_them]

        self.xoa_form()
        messagebox.showinfo("Cập nhật tài khoản", "Cập nhật tài khoản thành công!")

    def xoa(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần xóa!")
            return

        xacnhan = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa không?")
        if not xacnhan:
            return

        item = self.trHienThi.item(selected[0])
        ten = item["values"][0]

        self.trHienThi.delete(selected[0])

        is_new = any(x[0] == ten for x in self.ds_them)

        if is_new:
            self.ds_them = [x for x in self.ds_them if x[0] != ten]
        else:
            if ten not in self.ds_xoa:
                self.ds_xoa.append(ten)

        self.xoa_form()
        messagebox.showinfo("Xóa tài khoản", "Xóa tài khoản thành công!")

    def luu(self):
        try:
            if not self.ds_them and not self.ds_sua and not self.ds_xoa:
                messagebox.showinfo("Thông báo", "Không có thay đổi để lưu!")
                return

            xacnhan = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn lưu không?")
            if not xacnhan:
                return

            for ten in self.ds_xoa:
                self.cursor.execute(
                    "DELETE FROM TaiKhoan WHERE TenDangNhap = ?", (ten,)
                )

            for ten, mk in self.ds_them:
                self.cursor.execute(
                    "INSERT INTO TaiKhoan (TenDangNhap, MatKhau) VALUES (?, ?)",
                    (ten, mk),
                )

            for ten, mk, ten_cu in self.ds_sua:
                if ten == ten_cu:
                    self.cursor.execute(
                        "UPDATE TaiKhoan SET MatKhau=? WHERE TenDangNhap=?",
                        (mk, ten_cu),
                    )
                else:
                    self.cursor.execute(
                        "UPDATE TaiKhoan SET TenDangNhap=?, MatKhau=? WHERE TenDangNhap=?",
                        (ten, mk, ten_cu),
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

            self.cursor.execute(
                "SELECT TenDangNhap, MatKhau FROM TaiKhoan WHERE TenDangNhap LIKE ?",
                (f"%{tu_khoa_tim}%",),
            )
            rows = self.cursor.fetchall()

            for row in rows:
                self.trHienThi.insert("", "end", values=(row[0], len(row[1])))

            if not rows:
                messagebox.showinfo("Kết quả", "Không tìm thấy dữ liệu!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def xoa_form(self):
        self.txt_ten.delete(0, tk.END)
        self.txt_mk.delete(0, tk.END)

    def huy(self):
        self.txt_timkiem.delete(0, tk.END)
        self.hienthi_dulieu()
