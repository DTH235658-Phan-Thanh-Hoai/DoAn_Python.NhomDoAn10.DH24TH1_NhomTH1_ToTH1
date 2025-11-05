import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyodbc
from PIL import Image, ImageTk
import io

# === TAB TIVI ===
class tabTivi(tk.Frame):
    def __init__(self, parent, conn):
        super().__init__(parent, bg="white")
        
        # Biến lưu đường dẫn ảnh và dữ liệu ảnh
        self.image_path = None
        self.image_data = None
        self.selected_item = None

        # === CHUỖI KẾT NỐI ===
        self.conn = conn

        # === KHUNG TÌM KIẾM ===
        frame_search = tk.Frame(self, bg="#E3F2FD", padx=10, pady=10)
        frame_search.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_search, text="🔍 Tìm kiếm:", font=("Segoe UI", 10), bg="#E3F2FD").pack(side="left", padx=5)
        self.txt_timkiem = tk.Entry(frame_search, font=("Segoe UI", 10), width=65)
        self.txt_timkiem.pack(side="left", padx=5)

        self.search_option = tk.StringVar(value="ma")
        tk.Radiobutton(frame_search, text="Theo mã Tivi", variable=self.search_option, value="ma", bg="#E3F2FD", font=("Segoe UI", 10)).pack(side="left", padx=10)
        tk.Radiobutton(frame_search, text="Theo tên Tivi", variable=self.search_option, value="ten", bg="#E3F2FD", font=("Segoe UI", 10)).pack(side="left")
        tk.Button(frame_search, text="Tìm", font=("Segoe UI", 10, "bold"), bg="#1565C0", fg="white", bd=0, padx=10, pady=5, command=self.tim_kiem).pack(side="left", padx=10)

        # ==== KHUNG THÔNG TIN ====
        frame_form = tk.LabelFrame(self, text="Thông tin Tivi", bg="white", font=("Segoe UI", 12, "bold"), fg="#0D47A1", padx=10, pady=10)
        frame_form.pack(fill="x", padx=20, pady=10)

        self.pic_anhtivi = tk.Canvas(frame_form, width=60, height=80, bg="#f0f0f0", highlightthickness=1, highlightbackground="#ccc")
        self.pic_anhtivi.grid(row=0, column=0, rowspan=3, padx=5, pady=5)
        self.pic_anhtivi.create_text(30, 40, text="Ảnh\ntivi", font=("Segoe UI", 10), fill="#888", tags="placeholder")

        self.btn_chonanh = tk.Button(frame_form, text="Chọn ảnh", bg="#42A5F5", fg="white", font=("Segoe UI", 7, "bold"), height=1, width=7, bd=0, padx=10, pady=10, command=self.chon_anh)
        self.btn_chonanh.grid(row=3, column=0, pady=5)
        
        tk.Label(frame_form, text="Mã Tivi:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.txt_matv = ttk.Entry(frame_form, width=24)
        self.txt_matv.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(frame_form, text="Tên Tivi:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.txt_tentivi = ttk.Entry(frame_form, width=24)
        self.txt_tentivi.grid(row=0, column=4, padx=5, pady=5)

        tk.Label(frame_form, text="Hãng:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=5, sticky="w", padx=5, pady=5)
        self.cbo_hang = ttk.Combobox(frame_form, width=22, state="readonly")
        self.cbo_hang.grid(row=0, column=6, padx=5, pady=5)

        tk.Label(frame_form, text="Kích thước:", bg="white", font=("Segoe UI", 11)).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.txt_kichthuoc = ttk.Entry(frame_form, width=24)
        self.txt_kichthuoc.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(frame_form, text="Độ phân giải:", bg="white", font=("Segoe UI", 11)).grid(row=1, column=3, sticky="w", padx=5, pady=5)
        self.txt_dophangiai = ttk.Entry(frame_form, width=24)
        self.txt_dophangiai.grid(row=1, column=4, padx=5, pady=5)
        
        tk.Label(frame_form, text="Năm sản xuất:", bg="white", font=("Segoe UI", 11)).grid(row=1, column=5, sticky="w", padx=5, pady=5)
        self.txt_namsanxuat = ttk.Entry(frame_form, width=24)
        self.txt_namsanxuat.grid(row=1, column=6, padx=5, pady=5)

        tk.Label(frame_form, text="Giá bán:", bg="white", font=("Segoe UI", 11)).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.txt_giaban = ttk.Entry(frame_form, width=24)
        self.txt_giaban.grid(row=2, column=2, padx=5, pady=5)

        tk.Label(frame_form, text="Số lượng:", bg="white", font=("Segoe UI", 11)).grid(row=2, column=3, sticky="w", padx=5, pady=5)
        self.txt_soluong = ttk.Entry(frame_form, width=24)
        self.txt_soluong.grid(row=2, column=4, padx=5, pady=5)
        
        tk.Label(frame_form, text="Mô tả:", bg="white", font=("Segoe UI", 11)).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.txt_mota = ttk.Entry(frame_form, width=115)
        self.txt_mota.grid(row=3, column=2, columnspan=6, padx=5, pady=5)

        # ==== NÚT CHỨC NĂNG ====
        frame_buttons = tk.Frame(self, bg="white")
        frame_buttons.pack(pady=10)
        
        btn_them = tk.Button(frame_buttons, text="➕ Thêm", bg="#EBDA42", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5, bd=0, command=self.them_tivi)
        btn_them.grid(row=0, column=0, padx=10)

        btn_sua = tk.Button(frame_buttons, text="✏️ Sửa", bg="#FB8C00", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5, bd=0, command=self.sua_tivi)
        btn_sua.grid(row=0, column=1, padx=10)

        btn_xoa = tk.Button(frame_buttons, text="🗑️ Xóa", bg="#E53935", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5, bd=0, command=self.xoa_tivi)
        btn_xoa.grid(row=0, column=2, padx=10)

        btn_lammoi = tk.Button(frame_buttons, text="🔄 Làm mới", bg="#1E88E5", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5, bd=0, command=self.lam_moi)
        btn_lammoi.grid(row=0, column=3, padx=10)

        btn_luu = tk.Button(frame_buttons, text="💾 Lưu", bg="#449A2D", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5, bd=0, command=self.lam_moi)
        btn_luu.grid(row=0, column=4, padx=10)

        # === BẢNG DANH SÁCH TIVI ===
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        # Định nghĩa các cột
        columns = ("MaTivi", "TenTivi", "TenHang", "KichThuoc", "DoPhanGiai", "GiaBan", "SoLuongTon", "NamSanXuat", "MoTa")
        self.trHienThi = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
        
        # Đặt tiêu đề cột
        self.trHienThi.heading("MaTivi", text="Mã Tivi")
        self.trHienThi.heading("TenTivi", text="Tên Tivi")
        self.trHienThi.heading("TenHang", text="Hãng")
        self.trHienThi.heading("KichThuoc", text="Kích thước")
        self.trHienThi.heading("DoPhanGiai", text="Độ phân giải")
        self.trHienThi.heading("GiaBan", text="Giá bán")
        self.trHienThi.heading("SoLuongTon", text="Số lượng")
        self.trHienThi.heading("NamSanXuat", text="Năm SX")
        self.trHienThi.heading("MoTa", text="Mô tả")
        
        # Đặt độ rộng cột
        self.trHienThi.column("MaTivi", width=80)
        self.trHienThi.column("TenTivi", width=150)
        self.trHienThi.column("TenHang", width=100)
        self.trHienThi.column("KichThuoc", width=80)
        self.trHienThi.column("DoPhanGiai", width=100)
        self.trHienThi.column("GiaBan", width=100)
        self.trHienThi.column("SoLuongTon", width=80)
        self.trHienThi.column("NamSanXuat", width=80)
        self.trHienThi.column("MoTa", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.trHienThi.yview)
        self.trHienThi.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.trHienThi.pack(fill="both", expand=True)

        # Style cho Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        # Bind sự kiện click vào dòng
        self.trHienThi.bind("<<TreeviewSelect>>", self.chon_dong)

        self.load_hang_san_xuat()
        self.load_danh_sach_tivi()

    def load_hang_san_xuat(self):
        """Load dữ liệu hãng sản xuất vào combobox"""
        try:
            #conn = pyodbc.connect(self.conn)
            cursor = self.conn.cursor()
            cursor.execute("SELECT MaHang, TenHang FROM HangSanXuat")
            
            self.hang_dict = {}
            hang_list = []
            
            for row in cursor.fetchall():
                ma_hang = row.MaHang
                ten_hang = row.TenHang
                self.hang_dict[ten_hang] = ma_hang
                hang_list.append(ten_hang)
            
            self.cbo_hang['values'] = hang_list
            
            #self.conn.close()
            cursor.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể load danh sách hãng: {str(e)}")

    def load_danh_sach_tivi(self):
        """Load dữ liệu tivi vào Treeview"""
        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)
            
            #conn = pyodbc.connect(self.conn)
            cursor = self.conn.cursor()
            
            query = """
                SELECT t.MaTivi, t.TenTivi, h.TenHang, t.KichThuoc, t.DoPhanGiai, 
                       t.GiaBan, t.SoLuongTon, t.NamSanXuat, t.MoTa
                FROM Tivi t
                INNER JOIN HangSanXuat h ON t.MaHang = h.MaHang
            """
            cursor.execute(query)
            
            for row in cursor.fetchall():
                self.trHienThi.insert("", "end", values=(
                    row.MaTivi,
                    row.TenTivi,
                    row.TenHang,
                    row.KichThuoc or "",
                    row.DoPhanGiai or "",
                    f"{row.GiaBan:,.0f}" if row.GiaBan else "0",
                    row.SoLuongTon or 0,
                    row.NamSanXuat or "",
                    row.MoTa or ""
                ))
            
            cursor.close()
            #self.conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể load danh sách tivi: {str(e)}")

    def chon_dong(self, event):
        """Hiển thị thông tin tivi khi click vào dòng"""
        selected = self.trHienThi.selection()
        if not selected:
            return
        
        self.selected_item = selected[0]
        values = self.trHienThi.item(self.selected_item)['values']
        
        self.txt_matv.delete(0, tk.END)
        self.txt_matv.insert(0, values[0])
        
        self.txt_tentivi.delete(0, tk.END)
        self.txt_tentivi.insert(0, values[1])
        
        self.cbo_hang.set(values[2])
        
        self.txt_kichthuoc.delete(0, tk.END)
        self.txt_kichthuoc.insert(0, values[3])
        
        self.txt_dophangiai.delete(0, tk.END)
        self.txt_dophangiai.insert(0, values[4])
        
        gia_ban = str(values[5]).replace(",", "")
        self.txt_giaban.delete(0, tk.END)
        self.txt_giaban.insert(0, gia_ban)
        
        self.txt_soluong.delete(0, tk.END)
        self.txt_soluong.insert(0, values[6])
        
        self.txt_namsanxuat.delete(0, tk.END)
        self.txt_namsanxuat.insert(0, values[7])
        
        self.txt_mota.delete(0, tk.END)
        self.txt_mota.insert(0, values[8])
        
        self.load_hinh_anh(values[0])

    def load_hinh_anh(self, ma_tivi):
        """Load hình ảnh từ database"""
        try:
            #conn = pyodbc.connect(self.conn)
            cursor = self.conn.cursor()
            cursor.execute("SELECT HinhAnh FROM Tivi WHERE MaTivi = ?", (ma_tivi,))
            row = cursor.fetchone()
            
            if row and row.HinhAnh:
                image_data = row.HinhAnh
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((60, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.pic_anhtivi.delete("all")
                self.pic_anhtivi.create_image(30, 40, image=photo)
                self.pic_anhtivi.image = photo  
                self.image_data = row.HinhAnh
            else:
                # Hiển thị placeholder
                self.pic_anhtivi.delete("all")
                self.pic_anhtivi.create_text(30, 40, text="Ảnh\ntivi", font=("Segoe UI", 10), fill="#888")
                self.image_data = None
            
            cursor.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể load hình ảnh: {str(e)}")

    def them_tivi(self):
        """Thêm tivi mới"""
        if not self.validate_input():
            return
        
        try:
            #conn = pyodbc.connect(self.conn)
            cursor = self.conn.cursor()
            
            ten_hang = self.cbo_hang.get()
            ma_hang = self.hang_dict.get(ten_hang)
            
            if not ma_hang:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn hãng!")
                return
            
            cursor.execute("SELECT COUNT(*) FROM Tivi WHERE MaTivi = ?", (self.txt_matv.get(),))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Cảnh báo", "Mã tivi đã tồn tại!")
                cursor.close()
                return
            
            query = """
                INSERT INTO Tivi (MaTivi, HinhAnh, TenTivi, MaHang, KichThuoc, DoPhanGiai, 
                                  GiaBan, SoLuongTon, NamSanXuat, MoTa)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (
                self.txt_matv.get(),
                self.image_data,
                self.txt_tentivi.get(),
                ma_hang,
                self.txt_kichthuoc.get() or None,
                self.txt_dophangiai.get() or None,
                float(self.txt_giaban.get()) if self.txt_giaban.get() else 0,
                int(self.txt_soluong.get()) if self.txt_soluong.get() else 0,
                int(self.txt_namsanxuat.get()) if self.txt_namsanxuat.get() else None,
                self.txt_mota.get() or None
            ))
            
            cursor.commit()
            cursor.close()
            
            messagebox.showinfo("Thành công", "Thêm tivi thành công!")
            self.load_danh_sach_tivi()
            self.lam_moi()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm tivi: {str(e)}")

    def sua_tivi(self):
        """Cập nhật thông tin tivi"""
        if not self.selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tivi cần sửa!")
            return
        
        if not self.validate_input():
            return
        
        try:
            #conn = pyodbc.connect(self.conn)
            cursor = self.conn.cursor()
            
            ten_hang = self.cbo_hang.get()
            ma_hang = self.hang_dict.get(ten_hang)
            
            query = """
                UPDATE Tivi 
                SET HinhAnh = ?, TenTivi = ?, MaHang = ?, KichThuoc = ?, 
                    DoPhanGiai = ?, GiaBan = ?, SoLuongTon = ?, NamSanXuat = ?, MoTa = ?
                WHERE MaTivi = ?
            """
            
            cursor.execute(query, (
                self.image_data,
                self.txt_tentivi.get(),
                ma_hang,
                self.txt_kichthuoc.get() or None,
                self.txt_dophangiai.get() or None,
                float(self.txt_giaban.get()) if self.txt_giaban.get() else 0,
                int(self.txt_soluong.get()) if self.txt_soluong.get() else 0,
                int(self.txt_namsanxuat.get()) if self.txt_namsanxuat.get() else None,
                self.txt_mota.get() or None,
                self.txt_matv.get()
            ))
            
            self.commit()
            self.close()
            
            messagebox.showinfo("Thành công", "Cập nhật tivi thành công!")
            self.load_danh_sach_tivi()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật tivi: {str(e)}")

    def xoa_tivi(self):
        """Xóa tivi"""
        if not self.selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tivi cần xóa!")
            return
        
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa tivi này?")
        if not confirm:
            return
        
        try:
            conn = pyodbc.connect(self.conn)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM Tivi WHERE MaTivi = ?", (self.txt_matv.get(),))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Thành công", "Xóa tivi thành công!")
            self.load_danh_sach_tivi()
            self.lam_moi()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa tivi: {str(e)}")

    def lam_moi(self):
        """Xóa các ô nhập và reset form"""
        self.txt_matv.delete(0, tk.END)
        self.txt_tentivi.delete(0, tk.END)
        self.cbo_hang.set("")
        self.txt_kichthuoc.delete(0, tk.END)
        self.txt_dophangiai.delete(0, tk.END)
        self.txt_giaban.delete(0, tk.END)
        self.txt_soluong.delete(0, tk.END)
        self.txt_namsanxuat.delete(0, tk.END)
        self.txt_mota.delete(0, tk.END)
        self.txt_timkiem.delete(0, tk.END)
        
        self.pic_anhtivi.delete("all")
        self.pic_anhtivi.create_text(30, 40, text="Ảnh\ntivi", font=("Segoe UI", 10), fill="#888")
        self.image_path = None
        self.image_data = None
        self.selected_item = None
        
        for item in self.trHienThi.selection():
            self.trHienThi.selection_remove(item)

    def tim_kiem(self):
        """Tìm kiếm tivi"""
        keyword = self.txt_timkiem.get().strip()
        if not keyword:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return
        
        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)
            
            #conn = pyodbc.connect(self.conn)
            cursor = self.conn.cursor()
            
            if self.search_option.get() == "ma":
                query = """
                    SELECT t.MaTivi, t.TenTivi, h.TenHang, t.KichThuoc, t.DoPhanGiai, 
                           t.GiaBan, t.SoLuongTon, t.NamSanXuat, t.MoTa
                    FROM Tivi t
                    INNER JOIN HangSanXuat h ON t.MaHang = h.MaHang
                    WHERE t.MaTivi LIKE ?
                """
            else:
                query = """
                    SELECT t.MaTivi, t.TenTivi, h.TenHang, t.KichThuoc, t.DoPhanGiai, 
                           t.GiaBan, t.SoLuongTon, t.NamSanXuat, t.MoTa
                    FROM Tivi t
                    INNER JOIN HangSanXuat h ON t.MaHang = h.MaHang
                    WHERE t.TenTivi LIKE ?
                """
            
            cursor.execute(query, (f"%{keyword}%",))
            
            count = 0
            for row in cursor.fetchall():
                self.trHienThi.insert("", "end", values=(
                    row.MaTivi,
                    row.TenTivi,
                    row.TenHang,
                    row.KichThuoc or "",
                    row.DoPhanGiai or "",
                    f"{row.GiaBan:,.0f}" if row.GiaBan else "0",
                    row.SoLuongTon or 0,
                    row.NamSanXuat or "",
                    row.MoTa or ""
                ))
                count += 1
            
            self.close()
            
            if count == 0:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả!")
            else:
                messagebox.showinfo("Thông báo", f"Tìm thấy {count} kết quả!")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")

    def chon_anh(self):
        """Chọn ảnh từ máy tính"""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    self.image_data = file.read()
                
                image = Image.open(file_path)
                image = image.resize((60, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.pic_anhtivi.delete("all")
                self.pic_anhtivi.create_image(30, 40, image=photo)
                self.pic_anhtivi.image = photo
                
                self.image_path = file_path
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể load ảnh: {str(e)}")

    def validate_input(self):
        """Kiểm tra dữ liệu nhập"""
        if not self.txt_matv.get().strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã tivi!")
            self.txt_matv.focus()
            return False
        
        if not self.txt_tentivi.get().strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên tivi!")
            self.txt_tentivi.focus()
            return False
        
        if not self.cbo_hang.get():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hãng!")
            self.cbo_hang.focus()
            return False
        
        if self.txt_giaban.get().strip():
            try:
                gia = float(self.txt_giaban.get())
                if gia < 0:
                    messagebox.showwarning("Cảnh báo", "Giá bán phải >= 0!")
                    self.txt_giaban.focus()
                    return False
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Giá bán phải là số!")
                self.txt_giaban.focus()
                return False
        
        if self.txt_soluong.get().strip():
            try:
                sl = int(self.txt_soluong.get())
                if sl < 0:
                    messagebox.showwarning("Cảnh báo", "Số lượng phải >= 0!")
                    self.txt_soluong.focus()
                    return False
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Số lượng phải là số nguyên!")
                self.txt_soluong.focus()
                return False
        
        if self.txt_namsanxuat.get().strip():
            try:
                nam = int(self.txt_namsanxuat.get())
                if nam < 1900 or nam > 2025:
                    messagebox.showwarning("Cảnh báo", "Năm sản xuất không hợp lệ!")
                    self.txt_namsanxuat.focus()
                    return False
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Năm sản xuất phải là số nguyên!")
                self.txt_namsanxuat.focus()
                return False
        
        return True