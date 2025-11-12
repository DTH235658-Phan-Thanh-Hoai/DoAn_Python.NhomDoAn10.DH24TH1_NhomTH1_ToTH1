import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc


class tabNhaCungCap(tk.Frame):
    def __init__(self, parent, conn, controller=None):
        super().__init__(parent, bg="white")
        self.conn = conn
        self.cursor = conn.cursor()
        self.ds_them = []
        self.ds_sua = []
        self.ds_xoa = []

        frame_search = tk.Frame(self, bg="#E3F2FD", padx=10, pady=10)
        frame_search.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_search, text="Tìm kiếm:", font=("Segoe UI", 10), bg="#E3F2FD").pack(side="left", padx=5)
        self.txt_timkiem = tk.Entry(frame_search, font=("Segoe UI", 10), width=42)
        self.txt_timkiem.pack(side="left", padx=5)

        self.search_option = tk.StringVar(value="ma")
        tk.Radiobutton(frame_search, text="Theo mã nhà cung cấp", variable=self.search_option,
                       value="ma", bg="#E3F2FD", font=("Segoe UI", 10)).pack(side="left", padx=10)
        tk.Radiobutton(frame_search, text="Theo tên nhà cung cấp", variable=self.search_option,
                       value="ten", bg="#E3F2FD", font=("Segoe UI", 10)).pack(side="left")

        tk.Button(frame_search, text="Tìm", font=("Segoe UI", 10, "bold"), bg="#1565C0",
                  fg="white", bd=0, padx=10, pady=5, command=self.timkiem).pack(side="left", padx=10)
        tk.Button(frame_search, text="Hủy", font=("Segoe UI", 10, "bold"), bg="#E53935",
                  fg="white", bd=0, padx=10, pady=5, command=self.huy_tim_kiem).pack(side="left", padx=10)

        frame_form = tk.LabelFrame(self, text="Thông tin Nhà cung cấp", bg="white",
                                   font=("Segoe UI", 12, "bold"), fg="#0D47A1", padx=10, pady=10)
        frame_form.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_form, text="Mã nhà cung cấp", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_ma = ttk.Entry(frame_form, width=28)
        self.txt_ma.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Tên nhà cung cấp:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.txt_ten = ttk.Entry(frame_form, width=68)
        self.txt_ten.grid(row=0, column=3, columnspan=3, padx=5, pady=5)

        tk.Label(frame_form, text="Số điện thoại:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.txt_sodienthoai = ttk.Entry(frame_form, width=28)
        self.txt_sodienthoai.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Email:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.txt_email = ttk.Entry(frame_form, width=28)
        self.txt_email.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Địa chỉ:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=4, sticky="w", padx=5, pady=5)
        self.txt_diachi = ttk.Entry(frame_form, width=28)
        self.txt_diachi.grid(row=1, column=5, padx=5, pady=5)

        frame_buttons = tk.Frame(self, bg="white")
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="➕ Thêm", bg="#EBDA42", fg="white",
                  font=("Segoe UI", 11, "bold"), padx=20, pady=5, bd=0, command=self.them).grid(row=0, column=0, padx=10)
        tk.Button(frame_buttons, text="✏️ Sửa", bg="#FB8C00", fg="white",
                  font=("Segoe UI", 11, "bold"), padx=20, pady=5, bd=0, command=self.sua).grid(row=0, column=1, padx=10)
        tk.Button(frame_buttons, text="🗑️ Xóa", bg="#E53935", fg="white",
                  font=("Segoe UI", 11, "bold"), padx=20, pady=5, bd=0, command=self.xoa).grid(row=0, column=2, padx=10)
        tk.Button(frame_buttons, text="🔄 Làm mới", bg="#1E88E5", fg="white",
                  font=("Segoe UI", 11, "bold"), padx=20, pady=5, bd=0, command=self.lammoi).grid(row=0, column=3, padx=10)
        tk.Button(frame_buttons, text="💾 Lưu", bg="#43A047", fg="white",
                  font=("Segoe UI", 10, "bold"), padx=20, pady=5, bd=0, command=self.luu).grid(row=0, column=4, padx=10)

        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("MaNCC", "TenNCC", "DiaChi", "SoDienThoai", "Email")
        scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")
        self.trHienThi = ttk.Treeview(frame_table, show="headings", columns=columns, height=12,
                                      yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.trHienThi.yview)
        scroll_x.config(command=self.trHienThi.xview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.trHienThi.pack(fill="both", expand=True)

        self.trHienThi.heading("MaNCC", text="Mã nhà cung cấp")
        self.trHienThi.heading("TenNCC", text="Tên nhà cung cấp")
        self.trHienThi.heading("DiaChi", text="Địa chỉ")
        self.trHienThi.heading("SoDienThoai", text="Số điện thoại")
        self.trHienThi.heading("Email", text="Email")

        self.trHienThi.column("MaNCC", width=120, anchor="center")
        self.trHienThi.column("TenNCC", width=250, anchor="w")
        self.trHienThi.column("DiaChi", width=200, anchor="w")
        self.trHienThi.column("SoDienThoai", width=150, anchor="center")
        self.trHienThi.column("Email", width=200, anchor="w")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        self.trHienThi.bind("<<TreeviewSelect>>", self.chon_dong)
        self.hienthi_dulieu()

    def hienthi_dulieu(self):
        for item in self.trHienThi.get_children():
            self.trHienThi.delete(item)
        self.cursor.execute("SELECT MaNCC, TenNCC, DiaChi, SoDienThoai, Email FROM NhaCungCap ORDER BY MaNCC")
        for row in self.cursor.fetchall():
            self.trHienThi.insert("", "end", values=(row.MaNCC, row.TenNCC, row.DiaChi, row.SoDienThoai, row.Email))

    def chon_dong(self, event=None):
        sel = self.trHienThi.selection()
        if sel:
            val = self.trHienThi.item(sel[0])["values"]
            self.xoa_form()
            self.txt_ma.insert(0, val[0])
            self.txt_ten.insert(0, val[1])
            self.txt_diachi.insert(0, val[2])
            if str(val[3][0]) == "0":
                sdt = str(val[3][0])
            else:
                sdt = "0" + str(val[3][0])
            self.txt_sodienthoai.insert(0, sdt)
            self.txt_email.insert(0, val[4])

    def kiemtra_trung(self, ma= "", ten= "", sdt= "", email= "", ma_hien_tai= ""):
        for iid in self.trHienThi.get_children():
            v = self.trHienThi.item(iid)["values"]
            if ma_hien_tai and v[0] == ma_hien_tai:
                continue
            if ma and v[0] == ma:
                return "Mã nhà cung cấp"
            if ten and v[1].strip().lower() == str(ten).strip().lower():
                return "Tên nhà cung cấp"
            if self.bo_so_0_dau(str(sdt)) and self.bo_so_0_dau(str(v[3])) == self.bo_so_0_dau(str(sdt)):
                return "Số điện thoại"
            if email and v[4].strip().lower() == str(email).strip().lower():
                return "Email"
        return None
    
    def bo_so_0_dau(self, chuoi):
        if isinstance(chuoi, str) and chuoi[0] == "0":
            return chuoi.lstrip("0") or "0"
        return str(chuoi)

    def them(self):
        ma = str(self.txt_ma.get()).strip()
        ten = str(self.txt_ten.get()).strip()
        diachi = str(self.txt_diachi.get()).strip()
        sdt = str(self.txt_sodienthoai.get()).strip()
        email = str(self.txt_email.get()).strip()

        if not ma:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã nhà cung cấp!")
            return
        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Tên nhà cung cấp!")
            return

        trung = self.kiemtra_trung(ma=ma, ten=ten, sdt=sdt, email=email)

        if trung:
            messagebox.showwarning("Cảnh báo", f"{trung} đã tồn tại!")
            return

        self.trHienThi.insert("", "end", values=(ma, ten, diachi, sdt, email))
        self.ds_them.append((ma, ten, diachi, sdt, email))
        self.xoa_form()
        messagebox.showinfo("Thêm nhà cung cấp", "Thêm nhà cung cấp thành công!")

    def sua(self):
        sel = self.trHienThi.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần sửa!")
            return

        ma = self.txt_ma.get().strip()
        ten = self.txt_ten.get().strip()
        diachi = self.txt_diachi.get().strip()
        sdt = self.txt_sodienthoai.get().strip()
        email = self.txt_email.get().strip()

        if not ma:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã nhà cung cấp!")
            return
        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Tên nhà cung cấp!")
            return

        ma_cu = self.trHienThi.item(sel[0])["values"][0]
        trung = self.kiemtra_trung(ma=ma, ten=ten, sdt=sdt, email=email, ma_hien_tai=ma_cu)
        if trung:
            messagebox.showwarning("Cảnh báo", f"{trung} đã tồn tại!")
            return

        self.trHienThi.item(sel[0], values=(ma, ten, diachi, sdt, email))
        if any(x[0] == ma_cu for x in self.ds_them):
            self.ds_them = [(ma, ten, diachi, sdt, email) if x[0] == ma_cu else x for x in self.ds_them]
        else:
            self.ds_sua = [x for x in self.ds_sua if x[0] != ma_cu]
            self.ds_sua.append((ma, ten, diachi, sdt, email, ma_cu))

        self.xoa_form()
        messagebox.showinfo("Cập nhật nhà cung cấp", "Cập nhật nhà cung cấp thành công!")

    def xoa(self):
        sel = self.trHienThi.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần xóa!")
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa dòng này?"):
            return
        ma = self.trHienThi.item(sel[0])["values"][0]
        self.trHienThi.delete(sel[0])
        if any(x[0] == ma for x in self.ds_them):
            self.ds_them = [x for x in self.ds_them if x[0] != ma]
        else:
            if ma not in self.ds_xoa:
                self.ds_xoa.append(ma)
        self.xoa_form()
        messagebox.showinfo("Thành công", "Đã xóa dòng! Nhấn 'Lưu' để lưu vào CSDL.")

    def luu(self):
        if not (self.ds_them or self.ds_sua or self.ds_xoa):
            messagebox.showinfo("Thông báo", "Không có thay đổi để lưu!")
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn lưu các thay đổi?"):
            return
        try:
            for ma in self.ds_xoa:
                self.cursor.execute("DELETE FROM NhaCungCap WHERE MaNCC = ?", (ma,))
            for ma, ten, diachi, sdt, email in self.ds_them:
                self.cursor.execute(
                    "INSERT INTO NhaCungCap (MaNCC, TenNCC, DiaChi, SoDienThoai, Email) VALUES (?, ?, ?, ?, ?)",
                    (ma, ten, diachi, sdt, email)
                )
            for ma, ten, diachi, sdt, email, ma_cu in self.ds_sua:
                self.cursor.execute(
                    "UPDATE NhaCungCap SET MaNCC=?, TenNCC=?, DiaChi=?, SoDienThoai=?, Email=? WHERE MaNCC=?",
                    (ma, ten, diachi, sdt, email, ma_cu)
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
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn hủy các thay đổi?"):
            self.ds_them.clear()
            self.ds_sua.clear()
            self.ds_xoa.clear()
            self.hienthi_dulieu()
            self.xoa_form()
            self.txt_timkiem.delete(0, tk.END)
            messagebox.showinfo("Thông báo", "Đã làm mới dữ liệu!")

    def timkiem(self):
        kw = self.txt_timkiem.get().strip()
        if not kw:
            messagebox.showinfo("Thông báo", "Vui lòng nhập từ khóa tìm kiếm.")
            self.hienthi_dulieu()
            return
        for item in self.trHienThi.get_children():
            self.trHienThi.delete(item)
        sql = ("SELECT MaNCC, TenNCC, DiaChi, SoDienThoai, Email FROM NhaCungCap "
               "WHERE MaNCC LIKE ? ORDER BY MaNCC" if self.search_option.get() == "ma"
               else "WHERE TenNCC LIKE ? ORDER BY MaNCC")
        self.cursor.execute(sql, (f"%{kw}%",))
        rows = self.cursor.fetchall()
        for r in rows:
            self.trHienThi.insert("", "end", values=(r.MaNCC, r.TenNCC, r.DiaChi, r.SoDienThoai, r.Email))
        if not rows:
            messagebox.showinfo("Kết quả", "Không tìm thấy kết quả!")

    def xoa_form(self):
        self.txt_ma.delete(0, tk.END)
        self.txt_ten.delete(0, tk.END)
        self.txt_sodienthoai.delete(0, tk.END)
        self.txt_email.delete(0, tk.END)
        self.txt_diachi.delete(0, tk.END)

    def huy_tim_kiem(self):
        self.txt_timkiem.delete(0, tk.END)
        self.hienthi_dulieu()