import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import date, datetime
import pyodbc
from PIL import Image, ImageTk
import io

PRIMARY_COLOR = "#0D47A1"
SECONDARY_COLOR = "#1565C0"
ACCENT_COLOR = "#42A5F5"
HIGHLIGHT_COLOR = "#BBDEFB"
TEXT_COLOR = "white"


class QuanLyNhanVien(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent, bg="white")

        self.conn = conn
        self.cursor = conn.cursor()
        self.user = user

        self.image_path = None
        self.image_data = None

        self.ds_them = []
        self.ds_sua = []
        self.ds_xoa = []

        self.dict_anh = {}

        lbl_title = tk.Label(self, text="QUẢN LÝ NHÂN VIÊN", font=("Segoe UI", 16, "bold"), bg="white", fg="#0D47A1",)
        lbl_title.pack()

        self.frame_search = tk.Frame(self, bg="#E3F2FD", padx=10, pady=10)
        self.frame_search.pack(fill="x", padx=20, pady=5)

        tk.Label(
            self.frame_search, text="🔍 Tìm kiếm:", font=("Segoe UI", 10), bg="#E3F2FD"
        ).pack(side="left", padx=5)
        self.txt_timkiem = tk.Entry(self.frame_search, font=("Segoe UI", 10), width=65)
        self.txt_timkiem.pack(side="left", padx=5)
        self.txt_timkiem.bind("<Return>", lambda e: self.timkiem())

        self.search_option = tk.StringVar(value="ma")
        tk.Radiobutton(
            self.frame_search,
            text="Theo mã nhân viên",
            variable=self.search_option,
            value="ma",
            bg="#E3F2FD",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=10)
        tk.Radiobutton(
            self.frame_search,
            text="Theo tên nhân viên",
            variable=self.search_option,
            value="ten",
            bg="#E3F2FD",
            font=("Segoe UI", 10),
        ).pack(side="left")
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
            text="Thông tin nhân viên",
            bg="white",
            font=("Segoe UI", 12, "bold"),
            fg="#0D47A1",
            padx=10,
            pady=10,
        )
        frame_form.pack(fill="x", padx=30, pady=10)

        self.pic_anhnhanvien = tk.Canvas(
            frame_form,
            width=60,
            height=80,
            bg="#f0f0f0",
            highlightthickness=1,
            highlightbackground="#ccc",
        )
        self.pic_anhnhanvien.grid(row=0, column=0, rowspan=3, padx=5, pady=5)
        self.pic_anhnhanvien.create_text(
            30,
            40,
            text="Ảnh\nnhân viên",
            font=("Segoe UI", 6),
            fill="#888",
            tags="placeholder",
        )

        self.btn_chonanh = tk.Button(
            frame_form,
            text="Chọn ảnh",
            bg="#42A5F5",
            fg="white",
            font=("Segoe UI", 7, "bold"),
            height=1,
            width=7,
            bd=0,
            padx=10,
            pady=10,
            command=self.chon_anh,
        )
        self.btn_chonanh.grid(row=3, column=0, pady=5)

        tk.Label(
            frame_form, text="Mã nhân viên:", font=("Segoe UI", 10), bg="white"
        ).grid(row=0, column=1, sticky="w", pady=5, padx=5)
        self.txt_manv = ttk.Entry(frame_form, font=("Segoe UI", 10), width=44)
        self.txt_manv.grid(row=0, column=2, pady=5, padx=5)

        tk.Label(
            frame_form, text="Tên nhân viên:", font=("Segoe UI", 10), bg="white"
        ).grid(row=0, column=3, sticky="w", pady=5, padx=5)
        self.txt_tennv = ttk.Entry(frame_form, font=("Segoe UI", 10), width=44)
        self.txt_tennv.grid(row=0, column=4, pady=5, padx=5)

        tk.Label(frame_form, text="Giới tính:", font=("Segoe UI", 10), bg="white").grid(
            row=1, column=1, sticky="w", pady=5, padx=5
        )
        self.cbo_gioitinh = ttk.Combobox(
            frame_form,
            font=("Segoe UI", 10),
            values=["Nam", "Nữ"],
            width=42,
            state="readonly",
        )
        self.cbo_gioitinh.grid(row=1, column=2, pady=5, padx=5)

        tk.Label(frame_form, text="Ngày sinh:", font=("Segoe UI", 10), bg="white").grid(
            row=1, column=3, sticky="w", pady=5, padx=5
        )
        self.date_ngaysinh = DateEntry(
            frame_form, font=("Segoe UI", 10), width=42, date_pattern="dd/mm/yyyy"
        )
        self.date_ngaysinh.grid(row=1, column=4, pady=5, padx=5)

        tk.Label(
            frame_form, text="Số điện thoại:", font=("Segoe UI", 10), bg="white"
        ).grid(row=2, column=1, sticky="w", pady=5, padx=5)
        self.txt_sodienthoai = ttk.Entry(frame_form, font=("Segoe UI", 10), width=44)
        self.txt_sodienthoai.grid(row=2, column=2, pady=5, padx=5)

        tk.Label(frame_form, text="CCCD:", font=("Segoe UI", 10), bg="white").grid(
            row=2, column=3, sticky="w", pady=5, padx=5
        )
        self.txt_cccd = ttk.Entry(frame_form, font=("Segoe UI", 10), width=44)
        self.txt_cccd.grid(row=2, column=4, pady=5, padx=5)

        frame_buttons = tk.Frame(self, bg="white")
        frame_buttons.pack(pady=10)

        self.btn_them = tk.Button(
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
        self.btn_them.grid(row=0, column=0, padx=10)

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

        self.btn_lammoi = tk.Button(
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
        self.btn_lammoi.grid(row=0, column=3, padx=10)

        self.btn_luu = tk.Button(
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
        self.btn_luu.grid(row=0, column=4, padx=10)

        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("MaNV", "TenNV", "GioiTinh", "NgaySinh", "SoDienThoai", "CCCD")
        self.trHienThi = ttk.Treeview(
            frame_table, show="headings", height=12, columns=columns
        )

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        self.trHienThi.heading("MaNV", text="Mã nhân viên", anchor="center")
        self.trHienThi.heading("TenNV", text="Tên nhân viên", anchor="center")
        self.trHienThi.heading("GioiTinh", text="Giới tính", anchor="center")
        self.trHienThi.heading("NgaySinh", text="Ngày sinh", anchor="center")
        self.trHienThi.heading("SoDienThoai", text="Số điện thoại", anchor="center")
        self.trHienThi.heading("CCCD", text="CCCD", anchor="center")

        self.trHienThi.column("MaNV", width=120, anchor="center")
        self.trHienThi.column("TenNV", width=200, anchor="center")
        self.trHienThi.column("GioiTinh", width=100, anchor="center")
        self.trHienThi.column("NgaySinh", width=120, anchor="center")
        self.trHienThi.column("SoDienThoai", width=150, anchor="center")
        self.trHienThi.column("CCCD", width=150, anchor="center")

        self.trHienThi.pack(fill="both", expand=True)

        self.trHienThi.bind("<<TreeviewSelect>>", self.chon_dong)

        self.hienthi_dulieu()

    def hienthi_dulieu(self):
        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            self.dict_anh.clear()

            if self.user != "admin":
                self.cursor.execute(
                    "SELECT MaNV, HinhAnh, TenNV, GioiTinh, NgaySinh, SoDienThoai, CCCD FROM NhanVien WHERE MaNV = ?",
                    (self.user,),
                )
                row = self.cursor.fetchone()

                if row:
                    self.txt_manv.delete(0, tk.END)
                    self.txt_manv.insert(0, row[0])

                    if row[1]:
                        self.dict_anh[row[0]] = row[1]

                    self.hienthi_anh(row[0])

                    self.txt_tennv.delete(0, tk.END)
                    self.txt_tennv.insert(0, row[2])

                    self.cbo_gioitinh.set(row[3])

                    ngay_sinh = row[4]
                    if isinstance(ngay_sinh, date):
                        self.date_ngaysinh.set_date(ngay_sinh)
                    elif isinstance(ngay_sinh, str) and ngay_sinh.strip():
                        try:
                            self.date_ngaysinh.set_date(
                                datetime.strptime(ngay_sinh, "%d/%m/%Y")
                            )
                        except:
                            self.date_ngaysinh.set_date(
                                datetime.strptime(ngay_sinh, "%Y-%m-%d")
                            )
                    else:
                        self.date_ngaysinh.set_date(date.today())

                    self.txt_sodienthoai.delete(0, tk.END)
                    self.txt_sodienthoai.insert(0, row[5] or "")

                    self.txt_cccd.delete(0, tk.END)
                    self.txt_cccd.insert(0, row[6] or "")

                    self.txt_manv.configure(state="disabled")
                    self.cbo_gioitinh.configure(state="disabled")
                    self.date_ngaysinh.configure(state="disabled")
                    self.txt_sodienthoai.configure(state="disabled")
                    self.txt_tennv.configure(state="disabled")
                    self.txt_cccd.configure(state="disabled")
                    self.btn_chonanh.configure(state="disabled")
                    self.btn_them.destroy()
                    self.btn_xoa.destroy()
                    self.btn_sua.destroy()
                    self.btn_lammoi.destroy()
                    self.btn_luu.destroy()
                    self.trHienThi.destroy()
                    self.frame_search.destroy()

            else:

                self.cursor.execute(
                    "SELECT MaNV, HinhAnh, TenNV, GioiTinh, NgaySinh, SoDienThoai, CCCD FROM NhanVien"
                )
                rows = self.cursor.fetchall()

                for row in rows:
                    ma_nv = row[0]

                    if row[1]:
                        self.dict_anh[ma_nv] = row[1]

                    ngay_sinh = row[4]
                    if isinstance(ngay_sinh, date):
                        ngay_sinh_str = ngay_sinh.strftime("%d/%m/%Y")
                    elif isinstance(ngay_sinh, str):
                        ngay_sinh_str = ngay_sinh
                    else:
                        ngay_sinh_str = ""

                    self.trHienThi.insert(
                        "",
                        "end",
                        values=(ma_nv, row[2], row[3], ngay_sinh_str, row[5], row[6]),
                    )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def chon_dong(self, event=None):
        selected = self.trHienThi.selection()
        if not selected:
            return

        item = self.trHienThi.item(selected[0])
        values = item["values"]

        self.xoa_form()

        self.txt_manv.insert(0, values[0])
        self.txt_tennv.insert(0, values[1])
        self.cbo_gioitinh.set(values[2])

        if values[3]:
            ngay_parts = values[3].split("/")
            if len(ngay_parts) == 3:
                self.date_ngaysinh.set_date(
                    date(int(ngay_parts[2]), int(ngay_parts[1]), int(ngay_parts[0]))
                )

        self.txt_sodienthoai.insert(0, values[4])
        self.txt_cccd.insert(0, values[5])

        self.hienthi_anh(values[0])

    def hienthi_anh(self, ma_nv):
        try:
            if ma_nv in self.dict_anh:
                image_data = self.dict_anh[ma_nv]
                self.image_data = image_data

                image = Image.open(io.BytesIO(image_data))
                image = image.resize((60, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                self.pic_anhnhanvien.delete("all")
                self.pic_anhnhanvien.create_image(30, 40, image=photo)
                self.pic_anhnhanvien.image = photo
            else:
                self.pic_anhnhanvien.delete("all")
                self.pic_anhnhanvien.create_text(
                    30, 40, text="Ảnh\nnhân viên", font=("Segoe UI", 10), fill="#888"
                )
                self.image_data = None
        except Exception as e:
            print(f"Lỗi hiển thị ảnh: {str(e)}")
            self.pic_anhnhanvien.delete("all")
            self.pic_anhnhanvien.create_text(
                30, 40, text="Lỗi\nảnh", font=("Segoe UI", 10), fill="#f00"
            )

    def them(self):
        if not self.xac_nhan_du_lieu():
            return

        ma = self.txt_manv.get().strip()
        ten = self.txt_tennv.get().strip()
        gioitinh = self.cbo_gioitinh.get()
        ngaysinh = self.date_ngaysinh.get_date()
        sdt = self.txt_sodienthoai.get().strip()
        cccd = self.txt_cccd.get().strip()

        for item in self.trHienThi.get_children():
            if self.trHienThi.item(item)["values"][0] == ma:
                messagebox.showwarning("Cảnh báo", f"Mã nhân viên '{ma}' đã tồn tại!")
                return

        self.trHienThi.insert(
            "",
            "end",
            values=(ma, ten, gioitinh, ngaysinh.strftime("%d/%m/%Y"), sdt, cccd),
        )

        if self.image_data:
            self.dict_anh[ma] = self.image_data

        self.ds_them.append(
            {
                "ma": ma,
                "anh": self.image_data,
                "ten": ten,
                "gioitinh": gioitinh,
                "ngaysinh": ngaysinh,
                "sdt": sdt,
                "cccd": cccd,
            }
        )

        self.xoa_form()
        messagebox.showinfo(
            "Thành công", "Đã thêm dòng mới! Nhấn 'Lưu' để lưu vào CSDL."
        )

    def sua(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần sửa!")
            return

        if not self.validate_input():
            return

        ma = self.txt_manv.get().strip()
        ten = self.txt_tennv.get().strip()
        gioitinh = self.cbo_gioitinh.get()
        ngaysinh = self.date_ngaysinh.get_date()
        sdt = self.txt_sodienthoai.get().strip()
        cccd = self.txt_cccd.get().strip()

        item = self.trHienThi.item(selected[0])
        ma_cu = item["values"][0]

        self.trHienThi.item(
            selected[0],
            values=(ma, ten, gioitinh, ngaysinh.strftime("%d/%m/%Y"), sdt, cccd),
        )

        if self.image_data:
            self.dict_anh[ma] = self.image_data
        elif ma in self.dict_anh:
            if ma != ma_cu and ma_cu in self.dict_anh:
                self.dict_anh[ma] = self.dict_anh[ma_cu]
                del self.dict_anh[ma_cu]

        is_new = any(x["ma"] == ma_cu for x in self.ds_them)

        if not is_new:
            self.ds_sua = [x for x in self.ds_sua if x["ma_cu"] != ma_cu]
            self.ds_sua.append(
                {
                    "ma": ma,
                    "anh": (
                        self.image_data if self.image_data else self.dict_anh.get(ma)
                    ),
                    "ten": ten,
                    "gioitinh": gioitinh,
                    "ngaysinh": ngaysinh,
                    "sdt": sdt,
                    "cccd": cccd,
                    "ma_cu": ma_cu,
                }
            )
        else:
            for i, item in enumerate(self.ds_them):
                if item["ma"] == ma_cu:
                    self.ds_them[i] = {
                        "ma": ma,
                        "anh": self.image_data if self.image_data else item["anh"],
                        "ten": ten,
                        "gioitinh": gioitinh,
                        "ngaysinh": ngaysinh,
                        "sdt": sdt,
                        "cccd": cccd,
                    }
                    break

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

        if ma in self.dict_anh:
            del self.dict_anh[ma]

        is_new = any(x["ma"] == ma for x in self.ds_them)

        if is_new:
            self.ds_them = [x for x in self.ds_them if x["ma"] != ma]
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

            xacnhan = messagebox.askyesno(
                "Xác nhận", "Bạn có chắc muốn lưu các thay đổi?"
            )
            if not xacnhan:
                return

            for ma in self.ds_xoa:
                self.cursor.execute("DELETE FROM NhanVien WHERE MaNV = ?", (ma,))

            for item in self.ds_them:
                ngaysinh_str = (
                    item["ngaysinh"].strftime("%Y-%m-%d")
                    if isinstance(item["ngaysinh"], date)
                    else item["ngaysinh"]
                )

                anh_binary = pyodbc.Binary(item["anh"]) if item["anh"] else None

                self.cursor.execute(
                    "INSERT INTO NhanVien (MaNV, HinhAnh, TenNV, GioiTinh, NgaySinh, SoDienThoai, CCCD) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        item["ma"],
                        anh_binary,
                        item["ten"],
                        item["gioitinh"],
                        ngaysinh_str,
                        item["sdt"],
                        item["cccd"],
                    ),
                )

            for item in self.ds_sua:
                ngaysinh_str = (
                    item["ngaysinh"].strftime("%Y-%m-%d")
                    if isinstance(item["ngaysinh"], date)
                    else item["ngaysinh"]
                )

                anh_binary = pyodbc.Binary(item["anh"]) if item["anh"] else None

                self.cursor.execute(
                    "UPDATE NhanVien SET MaNV=?, HinhAnh=?, TenNV=?, GioiTinh=?, NgaySinh=?, SoDienThoai=?, CCCD=? WHERE MaNV=?",
                    (
                        item["ma"],
                        anh_binary,
                        item["ten"],
                        item["gioitinh"],
                        ngaysinh_str,
                        item["sdt"],
                        item["cccd"],
                        item["ma_cu"],
                    ),
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

            self.dict_anh.clear()

            if self.search_option.get() == "ma":
                self.cursor.execute(
                    "SELECT MaNV, HinhAnh, TenNV, GioiTinh, NgaySinh, SoDienThoai, CCCD FROM NhanVien WHERE MaNV LIKE ?",
                    (f"%{tu_khoa_tim}%",),
                )
            else:
                self.cursor.execute(
                    "SELECT MaNV, HinhAnh, TenNV, GioiTinh, NgaySinh, SoDienThoai, CCCD FROM NhanVien WHERE TenNV LIKE ?",
                    (f"%{tu_khoa_tim}%",),
                )

            rows = self.cursor.fetchall()

            for row in rows:
                ma_nv = row[0]

                if row[1]:
                    self.dict_anh[ma_nv] = row[1]

                ngay_sinh = row[4]
                if isinstance(ngay_sinh, date):
                    ngay_sinh_str = ngay_sinh.strftime("%d/%m/%Y")
                else:
                    ngay_sinh_str = ""

                self.trHienThi.insert(
                    "",
                    "end",
                    values=(ma_nv, row[2], row[3], ngay_sinh_str, row[5], row[6]),
                )

            if not rows:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def chon_anh(self):
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")],
        )

        if file_path:
            try:
                with open(file_path, "rb") as file:
                    self.image_data = file.read()

                image = Image.open(file_path)
                image = image.resize((60, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                self.pic_anhnhanvien.delete("all")
                self.pic_anhnhanvien.create_image(30, 40, image=photo)
                self.pic_anhnhanvien.image = photo

                self.image_path = file_path

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể load ảnh: {str(e)}")

    def xac_nhan_du_lieu(self):
        if not self.txt_manv.get().strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã nhân viên!")
            self.txt_manv.focus()
            return False

        if not self.txt_tennv.get().strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên nhân viên!")
            self.txt_tennv.focus()
            return False

        if not self.cbo_gioitinh.get():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn giới tính!")
            self.cbo_gioitinh.focus()
            return False

        cccd = self.txt_cccd.get().strip()
        if cccd and len(cccd) != 12:
            messagebox.showwarning("Cảnh báo", "CCCD phải có 12 số!")
            self.txt_cccd.focus()
            return False

        return True

    def xoa_form(self):
        self.txt_manv.delete(0, tk.END)
        self.txt_tennv.delete(0, tk.END)
        self.cbo_gioitinh.set("")
        self.date_ngaysinh.set_date(date.today())
        self.txt_sodienthoai.delete(0, tk.END)
        self.txt_cccd.delete(0, tk.END)

        self.pic_anhnhanvien.delete("all")
        self.pic_anhnhanvien.create_text(
            30, 40, text="Ảnh\nnhân viên", font=("Segoe UI", 10), fill="#888"
        )
        self.image_path = None
        self.image_data = None
        self.selected_item = None

    def huy(self):
        self.txt_timkiem.delete(0, tk.END)
        self.hienthi_dulieu()