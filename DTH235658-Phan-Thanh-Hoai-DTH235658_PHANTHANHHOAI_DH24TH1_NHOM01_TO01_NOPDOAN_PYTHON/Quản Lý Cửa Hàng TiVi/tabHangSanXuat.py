import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc


# === TAB HÃNG SẢN XUẤT ===
class tabHangSanXuat(tk.Frame):
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
            frame_search, font=("Segoe UI", 10), width=55, bg="white"
        )
        self.txt_timkiem.pack(side="left", padx=5)
        self.txt_timkiem.bind("<Return>", lambda event: self.timkiem())

        self.search_option = tk.StringVar(value="ma")
        tk.Radiobutton(
            frame_search,
            text="Theo mã hãng",
            variable=self.search_option,
            value="ma",
            bg="#E3F2FD",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=10)
        tk.Radiobutton(
            frame_search,
            text="Theo tên hãng",
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
            text="Thông tin Hãng sản xuất",
            bg="white",
            font=("Segoe UI", 12, "bold"),
            fg="#0D47A1",
            padx=10,
            pady=10,
        )
        frame_form.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_form, text="Mã hãng:", bg="white", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.txt_ma = ttk.Entry(frame_form, width=32)
        self.txt_ma.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Tên hãng:", bg="white", font=("Segoe UI", 10)).grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )
        self.txt_ten = ttk.Entry(frame_form, width=32)
        self.txt_ten.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Quốc gia:", bg="white", font=("Segoe UI", 10)).grid(
            row=0, column=5, pady=5, padx=5, sticky="w"
        )
        self.txt_quocgia = ttk.Entry(frame_form, width=32)
        self.txt_quocgia.grid(row=0, column=6, padx=5, pady=5)

        # ==== NÚT CHỨC NĂNG ====
        frame_buttons = tk.Frame(self, bg="white")
        frame_buttons.pack(pady=10)

        btn_them = tk.Button(
            frame_buttons,
            text="Thêm",
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
            text="Sửa",
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
            text="Xóa",
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
            text="Làm mới",
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
            text="Lưu",
            bg="#43A047",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=5,
            bd=0,
            command=self.luu,
        )
        btn_luu.grid(row=0, column=4, padx=10)

        # === BẢNG HÃNG SẢN XUẤT ===
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("MaHang", "TenHang", "QuocGia")

        scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")

        self.trHienThi = ttk.Treeview(
            frame_table,
            show="headings",
            columns=columns,
            height=12,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )

        scroll_y.config(command=self.trHienThi.yview)
        scroll_x.config(command=self.trHienThi.xview)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.trHienThi.pack(fill="both", expand=True)

        self.trHienThi.heading("MaHang", text="Mã Hãng")
        self.trHienThi.heading("TenHang", text="Tên Hãng")
        self.trHienThi.heading("QuocGia", text="Quốc Gia")

        self.trHienThi.column("MaHang", width=150, anchor="center")
        self.trHienThi.column("TenHang", width=300, anchor="center")
        self.trHienThi.column("QuocGia", width=200, anchor="center")

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
                "SELECT MaHang, TenHang, QuocGia FROM HangSanXuat ORDER BY MaHang"
            )
            rows = self.cursor.fetchall()
            for row in rows:
                self.trHienThi.insert(
                    "", "end", values=(row.MaHang, row.TenHang, row.QuocGia)
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
            self.txt_quocgia.insert(0, values[2] if values[2] else "")

    def kiemtra_trung_ten_hang(self, ten_hang, ma_hang_hien_tai=None):
        ten_hang = str(ten_hang).strip().lower()
        for item in self.trHienThi.get_children():
            values = self.trHienThi.item(item)["values"]
            ma_trong_bang = values[0]
            ten_trong_bang = values[1].lower() if values[1] else ""
            if ma_hang_hien_tai and ma_trong_bang == ma_hang_hien_tai:
                continue
            if ten_trong_bang == ten_hang:
                return True
        return False

    def them(self):
        ma = self.txt_ma.get().strip()
        ten = self.txt_ten.get().strip()
        quocgia = self.txt_quocgia.get().strip()

        if not ma:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã hãng!")
            self.txt_ma.focus()
            return
        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Tên hãng!")
            self.txt_ten.focus()
            return

        for item in self.trHienThi.get_children():
            if self.trHienThi.item(item)["values"][0] == ma:
                messagebox.showwarning("Cảnh báo", f"Mã hãng '{ma}' đã tồn tại!")
                return

        if self.kiemtra_trung_ten_hang(ten):
            messagebox.showwarning("Cảnh báo", f"Tên hãng '{ten}' đã tồn tại!")
            self.txt_ten.focus()
            return

        self.trHienThi.insert("", "end", values=(ma, ten, quocgia))
        self.ds_them.append((ma, ten, quocgia))
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
        quocgia = self.txt_quocgia.get().strip()

        if not ma:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã hãng!")
            return
        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Tên hãng!")
            return

        item = self.trHienThi.item(selected[0])
        ma_cu = item["values"][0]

        if self.kiemtra_trung_ten_hang(ten, ma_cu):
            messagebox.showwarning("Cảnh báo", f"Tên hãng '{ten}' đã tồn tại!")
            self.txt_ten.focus()
            return

        self.trHienThi.item(selected[0], values=(ma, ten, quocgia))

        is_new = any(x[0] == ma_cu for x in self.ds_them)
        if not is_new:
            self.ds_sua = [x for x in self.ds_sua if x[0] != ma_cu]
            self.ds_sua.append((ma, ten, quocgia, ma_cu))
        else:
            self.ds_them = [
                (ma, ten, quocgia) if x[0] == ma_cu else x for x in self.ds_them
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
                self.cursor.execute("DELETE FROM HangSanXuat WHERE MaHang = ?", (ma,))

            for ma, ten, quocgia in self.ds_them:
                self.cursor.execute(
                    "INSERT INTO HangSanXuat (MaHang, TenHang, QuocGia) VALUES (?, ?, ?)",
                    (ma, ten, quocgia),
                )

            for ma, ten, quocgia, ma_cu in self.ds_sua:
                self.cursor.execute(
                    "UPDATE HangSanXuat SET MaHang = ?, TenHang = ?, QuocGia = ? WHERE MaHang = ?",
                    (ma, ten, quocgia, ma_cu),
                )

            self.conn.commit()
            messagebox.showinfo("Thành công", "Đã lưu thay đổi vào CSDL!")

        except pyodbc.IntegrityError as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi ràng buộc dữ liệu: {str(e)}")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {str(e)}")

        finally:
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
            messagebox.showinfo("Thông báo", "Vui lòng nhập từ khóa tìm kiếm.")
            self.hienthi_dulieu()
            return

        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            if self.search_option.get() == "ma":
                self.cursor.execute(
                    "SELECT MaHang, TenHang, QuocGia FROM HangSanXuat WHERE MaHang LIKE ? ORDER BY MaHang",
                    (f"%{tu_khoa_tim}%",),
                )
            else:
                self.cursor.execute(
                    "SELECT MaHang, TenHang, QuocGia FROM HangSanXuat WHERE TenHang LIKE ? ORDER BY MaHang",
                    (f"%{tu_khoa_tim}%",),
                )

            rows = self.cursor.fetchall()
            for row in rows:
                self.trHienThi.insert(
                    "", "end", values=(row.MaHang, row.TenHang, row.QuocGia)
                )

            if not rows:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")

    def xoa_form(self):
        self.txt_ma.delete(0, tk.END)
        self.txt_ten.delete(0, tk.END)
        self.txt_quocgia.delete(0, tk.END)

    def huy(self):
        self.txt_timkiem.delete(0, tk.END)
        self.hienthi_dulieu()
