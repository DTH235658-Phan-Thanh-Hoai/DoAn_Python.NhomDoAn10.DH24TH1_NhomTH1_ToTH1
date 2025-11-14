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

        self.controller = controller

        self.conn = conn
        self.cursor = conn.cursor()
        self.user = user

        self.selected_item = None
        self.image_data = None  
        self.anh_hien_tai = None 

        self.ds_them = []
        self.ds_sua = []
        self.ds_xoa = []

        lbl_title = tk.Label(self, text="QUẢN LÝ NHÂN VIÊN", font=("Segoe UI", 16, "bold"), bg="white", fg="#0D47A1",)
        lbl_title.pack()

        self.frame_search = tk.Frame(self, bg="#E3F2FD", padx=10, pady=10)
        self.frame_search.pack(fill="x", padx=20, pady=5)

        tk.Label(self.frame_search, text="Tìm kiếm:", font=("Segoe UI", 10), bg="#E3F2FD").pack(side="left", padx=5)
        self.txt_timkiem = tk.Entry(self.frame_search, font=("Segoe UI", 10), width=65)
        self.txt_timkiem.pack(side="left", padx=5)
        self.txt_timkiem.bind("<Return>", lambda e: self.timkiem())

        self.search_option = tk.StringVar(value="ma")
        tk.Radiobutton(self.frame_search, text="Theo mã nhân viên", variable=self.search_option, value="ma", bg="#E3F2FD", font=("Segoe UI", 10)).pack(side="left", padx=10)
        tk.Radiobutton(self.frame_search, text="Theo tên nhân viên", variable=self.search_option, value="ten", bg="#E3F2FD", font=("Segoe UI", 10)).pack(side="left")
        tk.Button(self.frame_search, text="Tìm", font=("Segoe UI", 10, "bold"), bg="#1565C0", fg="white", bd=0, padx=10, pady=5, command=self.timkiem).pack(side="left", padx=10)
        tk.Button(self.frame_search, text="Hủy", font=("Segoe UI", 10, "bold"), bg="#E53935", fg="white", bd=0, padx=10, pady=5, command=self.huy).pack(side="left", padx=10)

        frame_form = tk.LabelFrame(self, text="Thông tin nhân viên", bg="white", font=("Segoe UI", 12, "bold"), fg="#0D47A1", padx=10, pady=10)
        frame_form.pack(fill="x", padx=30, pady=10)

        self.pic_anhnhanvien = tk.Canvas(frame_form, width=60, height=80, bg="#f0f0f0", highlightthickness=1, highlightbackground="#ccc")
        self.pic_anhnhanvien.grid(row=0, column=0, rowspan=3, padx=5, pady=5)
        self.pic_anhnhanvien.create_text(30, 40, text="Ảnh\nnhân\nviên", font=("Segoe UI", 8), fill="#888", tags="placeholder")

        self.btn_chonanh = tk.Button(frame_form, text="Chọn ảnh", bg="#42A5F5", fg="white", font=("Segoe UI", 7, "bold"), height=1, width=7, bd=0, padx=10, pady=10, command=self.chon_anh)
        self.btn_chonanh.grid(row=3, column=0, pady=5)

        tk.Label(frame_form, text="Mã nhân viên:", font=("Segoe UI", 10), bg="white").grid(row=0, column=1, sticky="w", pady=5, padx=5)
        self.txt_manv = ttk.Entry(frame_form, font=("Segoe UI", 10), width=42)
        self.txt_manv.grid(row=0, column=2, pady=5, padx=5)

        tk.Label(frame_form, text="Tên nhân viên:", font=("Segoe UI", 10), bg="white").grid(row=0, column=3, sticky="w", pady=5, padx=5)
        self.txt_tennv = ttk.Entry(frame_form, font=("Segoe UI", 10), width=42)
        self.txt_tennv.grid(row=0, column=4, pady=5, padx=5)

        tk.Label(frame_form, text="Giới tính:", font=("Segoe UI", 10), bg="white").grid(row=1, column=1, sticky="w", pady=5, padx=5)
        self.cbo_gioitinh = ttk.Combobox(frame_form, font=("Segoe UI", 10), values=["Nam", "Nữ"], width=40, state="readonly")
        self.cbo_gioitinh.grid(row=1, column=2, pady=5, padx=5)

        tk.Label(frame_form, text="Ngày sinh:", font=("Segoe UI", 10), bg="white").grid(row=1, column=3, sticky="w", pady=5, padx=5)
        self.date_ngaysinh = DateEntry(frame_form, font=("Segoe UI", 10), width=40, date_pattern="dd/mm/yyyy")
        self.date_ngaysinh.grid(row=1, column=4, pady=5, padx=5)

        tk.Label(frame_form, text="Số điện thoại:", font=("Segoe UI", 10), bg="white").grid(row=2, column=1, sticky="w", pady=5, padx=5)
        self.txt_sodienthoai = ttk.Entry(frame_form, font=("Segoe UI", 10), width=42)
        self.txt_sodienthoai.grid(row=2, column=2, pady=5, padx=5)

        tk.Label(frame_form, text="CCCD:", font=("Segoe UI", 10), bg="white").grid(row=2, column=3, sticky="w", pady=5, padx=5)
        self.txt_cccd = ttk.Entry(frame_form, font=("Segoe UI", 10), width=42)
        self.txt_cccd.grid(row=2, column=4, pady=5, padx=5)

        self.frame_buttons = tk.Frame(self, bg="white")
        self.frame_buttons.pack(pady=10)

        self.btn_them = tk.Button(self.frame_buttons, text="➕ Thêm", bg="#EBDA42", fg="white", font=("Segoe UI", 11, "bold"), padx=20, pady=5, bd=0, command=self.them)
        self.btn_them.grid(row=0, column=0, padx=10)

        self.btn_sua = tk.Button(self.frame_buttons, text="✏️ Sửa", bg="#FB8C00", fg="white", font=("Segoe UI", 11, "bold"), padx=20, pady=5, bd=0, command=self.sua)
        self.btn_sua.grid(row=0, column=1, padx=10)

        self.btn_xoa = tk.Button(self.frame_buttons, text="🗑️ Xóa", bg="#E53935", fg="white", font=("Segoe UI", 11, "bold"), padx=20, pady=5, bd=0, command=self.xoa)
        self.btn_xoa.grid(row=0, column=2, padx=10)

        self.btn_lammoi = tk.Button(self.frame_buttons, text="🔄 Làm mới", bg="#1E88E5", fg="white", font=("Segoe UI", 11, "bold"), padx=20, pady=5, bd=0, command=self.lammoi)
        self.btn_lammoi.grid(row=0, column=3, padx=10)

        self.btn_luu = tk.Button(self.frame_buttons, text="💾 Lưu", bg="#43A047", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5, bd=0, command=self.luu)
        self.btn_luu.grid(row=0, column=4, padx=10)

        self.frame_table = tk.Frame(self, bg="white")
        self.frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("MaNV", "TenNV", "GioiTinh", "NgaySinh", "SoDienThoai", "CCCD")
        self.trHienThi = ttk.Treeview(self.frame_table, show="headings", height=12, columns=columns)

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

        self.load_data()

    def load_data(self):
        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            if self.user != "admin":
                self.cursor.execute(
                    "SELECT MaNV, TenNV, GioiTinh, NgaySinh, SoDienThoai, CCCD FROM NhanVien WHERE MaNV = ?",
                    (self.user)
                )
                row = self.cursor.fetchone()

                if row:
                    self.txt_manv.delete(0, tk.END)
                    self.txt_manv.insert(0, row[0])

                    self.hienthi_anh(row[0])

                    self.txt_tennv.delete(0, tk.END)
                    self.txt_tennv.insert(0, row[1])

                    self.cbo_gioitinh.set(row[2])

                    self.date_ngaysinh.set_date(self.chuyen_dd_sang_datetime(row[3]))

                    sdt = str(row[4])
                    if sdt and not sdt[0] == "0":
                        sdt = "0" + sdt
                    self.txt_sodienthoai.delete(0, tk.END)
                    self.txt_sodienthoai.insert(0, sdt)

                    cccd = str(row[5])
                    if cccd and not cccd[0] == "0":
                        cccd = "0" + cccd
                    self.txt_cccd.delete(0, tk.END)
                    self.txt_cccd.insert(0, cccd)

                    self.txt_manv.configure(state="disabled")
                    self.cbo_gioitinh.configure(state="disabled")
                    self.date_ngaysinh.configure(state="disabled")
                    self.txt_sodienthoai.configure(state="disabled")
                    self.txt_tennv.configure(state="disabled")
                    self.txt_cccd.configure(state="disabled")
                    self.btn_chonanh.configure(state="disabled")

                    self.frame_buttons.pack_forget()
                    self.frame_search.pack_forget()
                    self.frame_table.pack_forget()

            else:
                self.cursor.execute("SELECT MaNV, HinhAnh, TenNV, GioiTinh, NgaySinh, SoDienThoai, CCCD FROM NhanVien")
                rows = self.cursor.fetchall()

                for row in rows:
                    ma_nv = row[0]

                    if row[4]:
                        ngay_sinh_str = self.chuyen_yyyy_sang_dd(row[4])
                    else:
                        ngay_sinh_str = ""

                    sdt = str(row[5]) or ""
                    if sdt and not sdt[0] == "0":
                        sdt = "0" + sdt

                    cccd = str(row[6]) or ""
                    if cccd and not cccd[0] == "0":
                        cccd = "0" + cccd

                    self.trHienThi.insert("", "end", values=(ma_nv, row[2], row[3], ngay_sinh_str, sdt, cccd))
        except Exception as e:
            messagebox.showerror("Lỗi", "Không thể tải dữ liệu: " + str(e))

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

    def bo_so_0_dau(self, chuoi):
        if isinstance(chuoi, str) and chuoi[0] == "0":
            return chuoi.lstrip("0") or "0"
        return str(chuoi)

    def chon_dong(self, event=None):
        selected = self.trHienThi.selection()
        if not selected:
            return

        self.selected_item = selected[0]
        item = self.trHienThi.item(self.selected_item)
        values = item["values"]

        self.xoa_form()

        self.txt_manv.insert(0, values[0])
        self.txt_tennv.insert(0, values[1])
        self.cbo_gioitinh.set(values[2])
        self.date_ngaysinh.set_date(self.chuyen_dd_sang_datetime(values[3]))

        sdt = str(values[4])
        if sdt and not sdt[0] == "0":
            sdt = "0" + sdt
        self.txt_sodienthoai.insert(0, sdt)

        cccd = str(values[5])
        if cccd and not cccd[0] == "0":
            cccd = "0" + cccd
        self.txt_cccd.insert(0, cccd)

        self.hienthi_anh(values[0])

    def hienthi_anh(self, ma_nv):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT HinhAnh FROM NhanVien WHERE MaNV = ?", (ma_nv,))
            row = cursor.fetchone()

            if row and row[0]:
                image_data = row[0]
                anh_pil = Image.open(io.BytesIO(image_data))
                anh_pil = anh_pil.resize((120, 120))

                self.anh_hien_tai = ImageTk.PhotoImage(anh_pil, master=self)

                self.pic_anhnhanvien.delete("all")
                self.pic_anhnhanvien.create_image(60, 60, image=self.anh_hien_tai, anchor="center")

                self.pic_anhnhanvien.image = self.anh_hien_tai

            else:
                self.pic_anhnhanvien.delete("all")
                self.pic_anhnhanvien.create_text(60, 60, text="(Không có ảnh)", fill="gray")

        except Exception as e:
            messagebox.showerror("Lỗi hiển thị ảnh", str(e))

    def chon_anh(self):
        if not self.selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên trên danh sách.")
            return
            
        duong_dan_anh = filedialog.askopenfilename(title="Chọn ảnh",filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")],)

        if duong_dan_anh:
            try:
                with open(duong_dan_anh, "rb") as file:
                    self.image_data = file.read()

                anh_pil = Image.open(io.BytesIO(self.image_data))
                anh_pil = anh_pil.resize((120, 120))

                self.anh_hien_tai = ImageTk.PhotoImage(anh_pil, master=self)

                self.pic_anhnhanvien.delete("all")
                self.pic_anhnhanvien.create_image(60, 60, image=self.anh_hien_tai, anchor="center")
                self.pic_anhnhanvien.image = self.anh_hien_tai

            except Exception as e:
                messagebox.showerror("Lỗi chọn ảnh", str(e))

    def kiem_tra_du_lieu(self):
        ma = self.txt_manv.get().strip()
        ten = self.txt_tennv.get().strip()
        gioitinh = self.cbo_gioitinh.get()
        ngaysinh = str(self.date_ngaysinh.get_date())
        sdt = self.txt_sodienthoai.get().strip()
        cccd = self.txt_cccd.get().strip()

        if not ma:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã nhân viên!")
            return False
        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên nhân viên!")
            return False
        if not gioitinh:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn giới tính!")
            return False
        if not ngaysinh:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ngày sinh!")
            return False
        if not sdt or len(sdt) != 10 or not sdt.isdigit():
            messagebox.showwarning("Cảnh báo", "Số điện thoại phải có 10 chữ số!")
            return False
        if not cccd or len(cccd) not in (9, 12) or not cccd.isdigit():
            messagebox.showwarning("Cảnh báo", "CCCD phải là 9 hoặc 12 chữ số!")
            return False

        return True


    def them(self):
        if not self.kiem_tra_du_lieu():
            return

        ma = self.txt_manv.get().strip()
        ten = self.txt_tennv.get().strip()
        gioitinh = self.cbo_gioitinh.get()
        ngaysinh = str(self.date_ngaysinh.get_date())
        sdt = self.txt_sodienthoai.get().strip()
        cccd = self.txt_cccd.get().strip()

        for item in self.trHienThi.get_children():
            if self.trHienThi.item(item)["values"][0] == ma:
                messagebox.showwarning("Cảnh báo", f"Mã nhân viên '{ma}' đã tồn tại!")
                return

            if self.bo_so_0_dau(self.trHienThi.item(item)["values"][4]) == self.bo_so_0_dau(sdt):
                messagebox.showwarning("Cảnh báo", f"Số điện thoại '{sdt}' đã tồn tại!")
                return

            if self.bo_so_0_dau(self.trHienThi.item(item)["values"][5]) == self.bo_so_0_dau(cccd):
                messagebox.showwarning("Cảnh báo", f"Số CCCD '{cccd}' đã tồn tại!")
                return

        if sdt[0] == "0":
            sdt_hien_thi = sdt
        else:
            sdt_hien_thi = "0" + sdt

        if cccd[0] == "0":
            cccd_hien_thi = cccd
        else:
            cccd_hien_thi = "0" + cccd

        self.trHienThi.insert("", "end", values=(ma, ten, gioitinh, self.chuyen_yyyy_sang_dd(ngaysinh), sdt_hien_thi, cccd_hien_thi))

        self.ds_them.append((ma, self.image_data, ten, gioitinh, ngaysinh, sdt_hien_thi, cccd_hien_thi))

        self.xoa_form()
        messagebox.showinfo("Thành công", "Đã thêm dòng mới! Nhấn 'Lưu' để lưu vào CSDL.")

    def sua(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần sửa!")
            return

        if not self.kiem_tra_du_lieu():
            return

        ma = self.txt_manv.get().strip()
        ten = self.txt_tennv.get().strip()
        gioitinh = self.cbo_gioitinh.get()
        ngaysinh = str(self.date_ngaysinh.get_date())
        sdt = self.txt_sodienthoai.get().strip()
        cccd = self.txt_cccd.get().strip()

        item = self.trHienThi.item(selected[0])
        ma_cu = item["values"][0]

        for item in self.trHienThi.get_children():
            if self.trHienThi.item(item)["values"][0] == ma_cu:
                continue
            else:
                if self.trHienThi.item(item)["values"][0] == ma:
                    messagebox.showwarning("Cảnh báo", f"Mã nhân viên '{ma}' đã tồn tại!")
                    return

                if self.bo_so_0_dau(self.trHienThi.item(item)["values"][4]) == self.bo_so_0_dau(sdt):
                    messagebox.showwarning("Cảnh báo", f"Số điện thoại '{sdt}' đã tồn tại!")
                    return

                if self.bo_so_0_dau(self.trHienThi.item(item)["values"][5]) == self.bo_so_0_dau(cccd):
                    messagebox.showwarning("Cảnh báo", f"Số CCCD '{cccd}' đã tồn tại!")
                    return

        if sdt[0] == "0":
            sdt_hien_thi = sdt
        else:
            sdt_hien_thi = "0" + sdt

        if cccd[0] == "0":
            cccd_hien_thi = cccd
        else:
            cccd_hien_thi = "0" + cccd

        self.trHienThi.item(selected[0], values=(ma, ten, gioitinh, self.chuyen_yyyy_sang_dd(ngaysinh), sdt_hien_thi, cccd_hien_thi))

        is_new = any(item[0] == ma_cu for item in self.ds_them)

        if is_new:
            self.ds_them = [item for item in self.ds_them if item[0] != ma_cu]
            self.ds_them.append((ma, self.image_data, ten, gioitinh, ngaysinh, sdt_hien_thi, cccd_hien_thi))
        else:
            self.ds_sua = [item for item in self.ds_sua if item[7] != ma_cu]
            self.ds_sua.append((ma, self.image_data, ten, gioitinh, ngaysinh, sdt_hien_thi, cccd_hien_thi, ma_cu))

        messagebox.showinfo("Thành công", "Đã cập nhật dòng! Nhấn 'Lưu' để lưu vào CSDL.")

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
        self.selected_item = None
        messagebox.showinfo("Thành công", "Đã xóa dòng! Nhấn 'Lưu' để lưu vào CSDL.")

    def luu(self):
        try:
            if not self.ds_them and not self.ds_sua and not self.ds_xoa:
                messagebox.showinfo("Thông báo", "Không có thay đổi để lưu!")
                return

            xacnhan = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn lưu các thay đổi?")
            if not xacnhan:
                return

            for ma in self.ds_xoa:
                self.cursor.execute("DELETE FROM NhanVien WHERE MaNV = ?", (ma,))

            for item in self.ds_them:
                query = """
                    INSERT INTO NhanVien (MaNV, HinhAnh, TenNV, GioiTinh, NgaySinh, SoDienThoai, CCCD)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                self.cursor.execute(query, item)

            for item in self.ds_sua:
                query = """
                    UPDATE NhanVien 
                    SET MaNV = ?, HinhAnh = ?, TenNV = ?, GioiTinh = ?, NgaySinh = ?, SoDienThoai = ?, CCCD = ?
                    WHERE MaNV = ?
                """
                self.cursor.execute(query, item)

            self.conn.commit()
            messagebox.showinfo("Thành công", "Đã lưu thay đổi vào CSDL!")

        except pyodbc.IntegrityError as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi ràng buộc dữ liệu: {str(e)}")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {str(e)}")

        self.load_data()
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

        self.load_data()
        self.xoa_form()
        self.txt_timkiem.delete(0, tk.END)
        messagebox.showinfo("Thông báo", "Đã làm mới dữ liệu!")

    def timkiem(self):
        tu_khoa_tim = self.txt_timkiem.get().strip()
        if not tu_khoa_tim:
            messagebox.showinfo("Thông báo", "Vui lòng nhập từ khóa tìm kiếm.")
            self.load_data()
            return

        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            if self.search_option.get() == "ma":
                query = """
                    SELECT MaNV, HinhAnh, TenNV, GioiTinh, NgaySinh, SoDienThoai, CCCD 
                    FROM NhanVien 
                    WHERE MaNV LIKE ?
                    ORDER BY MaNV """
            else:
                query = """
                    SELECT MaNV, HinhAnh, TenNV, GioiTinh, NgaySinh, SoDienThoai, CCCD 
                    FROM NhanVien 
                    WHERE TenNV LIKE ?
                    ORDER BY MaNV"""

            self.cursor.execute(query, (f"%{tu_khoa_tim}%",))
            rows = self.cursor.fetchall()

            for row in rows:
                ma_nv = row[0]
                ngay_sinh_str = self.chuyen_yyyy_sang_dd(row[4]) if row[4] else ""

                sdt = str(row[5]) or ""
                if sdt and not sdt[0] == "0":
                    sdt = "0" + sdt

                cccd = str(row[6]) or ""
                if cccd and not cccd[0] == "0":
                    cccd = "0" + cccd

                self.trHienThi.insert("", "end", values=(ma_nv, row[2], row[3], ngay_sinh_str, sdt, cccd))

            if not rows:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")

    def xoa_form(self):
        self.txt_manv.delete(0, tk.END)
        self.txt_tennv.delete(0, tk.END)
        self.cbo_gioitinh.set("")
        self.date_ngaysinh.set_date(date.today())
        self.txt_sodienthoai.delete(0, tk.END)
        self.txt_cccd.delete(0, tk.END)

        self.image_data = None
        self.anh_hien_tai = None
        self.pic_anhnhanvien.delete("all")
        self.pic_anhnhanvien.create_text(30, 40, text="Ảnh\nnhân viên", font=("Segoe UI", 10), fill="#888")

    def huy(self):
        self.txt_timkiem.delete(0, tk.END)
        self.load_data()