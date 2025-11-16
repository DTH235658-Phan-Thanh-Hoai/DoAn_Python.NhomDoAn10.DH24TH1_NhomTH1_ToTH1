import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyodbc
from PIL import Image, ImageTk
import io


# === TAB TIVI ===
class tabTivi(tk.Frame):
    def __init__(self, parent, conn, user, controller):
        super().__init__(parent, bg="white")

        # === CHUỖI KẾT NỐI ===
        self.conn = conn
        self.cursor = conn.cursor()
        self.user = user
        self.controller = controller

        self.selected_item = None
        self.image_data = None 
        self.anh_hien_tai = None  

        self.ds_them = []
        self.ds_sua = []
        self.ds_xoa = []

        # === KHUNG TÌM KIẾM ===
        frame_search = tk.Frame(self, bg="#E3F2FD", padx=10, pady=10)
        frame_search.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_search, text="Tìm kiếm:", font=("Segoe UI", 10), bg="#E3F2FD").pack(side="left", padx=5)
        self.txt_timkiem = tk.Entry(frame_search, font=("Segoe UI", 10), width=60)
        self.txt_timkiem.pack(side="left", padx=5)
        self.txt_timkiem.bind("<Return>", lambda e: self.tim_kiem())

        self.search_option = tk.StringVar(value="ma")
        tk.Radiobutton(frame_search, text="Theo mã Tivi", variable=self.search_option, value="ma", bg="#E3F2FD", font=("Segoe UI", 10),).pack(side="left", padx=10)
        tk.Radiobutton(frame_search, text="Theo tên Tivi", variable=self.search_option, value="ten", bg="#E3F2FD", font=("Segoe UI", 10),).pack(side="left")

        tk.Button(frame_search, text="Tìm", font=("Segoe UI", 10, "bold"), bg="#1565C0", fg="white", bd=0,  padx=10, pady=5, command=self.tim_kiem,).pack(side="left", padx=10)
        tk.Button(frame_search,text="Hủy", font=("Segoe UI", 10, "bold"), bg="#E53935", fg="white", bd=0, padx=10, pady=5, command=self.huy,).pack(side="left", padx=10)

        # ==== KHUNG THÔNG TIN ====
        frame_form = tk.LabelFrame(self, text="Thông tin Tivi", bg="white", font=("Segoe UI", 12, "bold"), fg="#0D47A1",padx=10, pady=10,)
        frame_form.pack(fill="x", padx=20, pady=10)

        self.pic_anhtivi = tk.Canvas(frame_form, width=80, height=100, bg="#f0f0f0", highlightthickness=1, highlightbackground="#ccc", )
        self.pic_anhtivi.grid(row=0, column=0, rowspan=3, padx=5, pady=5)
        self.pic_anhtivi.create_text(30, 40, text="Ảnh\ntivi", font=("Segoe UI", 10), fill="#888", tags="placeholder",)

        self.btn_chonanh = tk.Button(frame_form, text="Chọn ảnh", bg="#42A5F5", fg="white", font=("Segoe UI", 7, "bold"), height=1, width=7, bd=0, padx=10, pady=10, command=self.chon_anh, )
        self.btn_chonanh.grid(row=3, column=0, pady=5)

        tk.Label(frame_form, text="Mã Tivi:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.txt_matv = ttk.Entry(frame_form, width=24)
        self.txt_matv.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(frame_form, text="Tên Tivi:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.txt_tentivi = ttk.Entry(frame_form, width=22)
        self.txt_tentivi.grid(row=0, column=4, padx=5, pady=5)

        tk.Label(frame_form, text="Hãng:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=5, sticky="w", padx=5, pady=5)
        self.cbo_hang = ttk.Combobox(frame_form, width=21, state="readonly")
        self.cbo_hang.grid(row=0, column=6, padx=5, pady=5)

        tk.Label(frame_form, text="Kích thước:", bg="white", font=("Segoe UI", 11)).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.txt_kichthuoc = ttk.Entry(frame_form, width=24)
        self.txt_kichthuoc.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(frame_form, text="Độ phân giải:", bg="white", font=("Segoe UI", 11)).grid(row=1, column=3, sticky="w", padx=5, pady=5)
        self.txt_dophangiai = ttk.Entry(frame_form, width=22)
        self.txt_dophangiai.grid(row=1, column=4, padx=5, pady=5)

        tk.Label(frame_form, text="Năm sản xuất:", bg="white", font=("Segoe UI", 11)).grid(row=1, column=5, sticky="w", padx=5, pady=5)
        self.txt_namsanxuat = ttk.Entry(frame_form, width=24)
        self.txt_namsanxuat.grid(row=1, column=6, padx=5, pady=5)

        tk.Label(frame_form, text="Giá bán:", bg="white", font=("Segoe UI", 11)).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.txt_giaban = ttk.Entry(frame_form, width=24)
        self.txt_giaban.grid(row=2, column=2, padx=5, pady=5)

        tk.Label(frame_form, text="Số lượng:", bg="white", font=("Segoe UI", 11)).grid(row=2, column=3, sticky="w", padx=5, pady=5)
        self.txt_soluong = ttk.Entry(frame_form, width=22, state="disabled")
        self.txt_soluong.grid(row=2, column=4, padx=5, pady=5)

        tk.Label(frame_form, text="Mô tả:", bg="white", font=("Segoe UI", 11)).grid( row=3, column=1, sticky="w", padx=5, pady=5)
        self.txt_mota = ttk.Entry(frame_form, width=110)
        self.txt_mota.grid(row=3, column=2, columnspan=6, padx=5, pady=5)

        # ==== NÚT CHỨC NĂNG ====
        frame_buttons = tk.Frame(self, bg="white")
        frame_buttons.pack(pady=10)

        btn_them = tk.Button(frame_buttons, text="➕ Thêm", bg="#EBDA42", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5,  bd=0, command=self.them_tivi,)
        btn_them.grid(row=0, column=0, padx=10)

        btn_sua = tk.Button(frame_buttons, text="✏️ Sửa", bg="#FB8C00", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5, bd=0, command=self.sua_tivi,)
        btn_sua.grid(row=0, column=1, padx=10)

        btn_xoa = tk.Button(frame_buttons, text="🗑️ Xóa", bg="#E53935", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5, bd=0, command=self.xoa_tivi,)
        btn_xoa.grid(row=0, column=2, padx=10)

        btn_lammoi = tk.Button(frame_buttons, text="🔄 Làm mới", bg="#1E88E5", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5, bd=0, command=self.lam_moi,)
        btn_lammoi.grid(row=0, column=3, padx=10)

        btn_luu = tk.Button(frame_buttons, text="💾 Lưu", bg="#449A2D", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5, bd=0, command=self.luu,)
        btn_luu.grid(row=0, column=4, padx=10)

        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        columns = ("MaTivi", "TenTivi", "TenHang", "KichThuoc", "DoPhanGiai", "GiaBan", "SoLuongTon", "NamSanXuat", "MoTa",)
        self.trHienThi = ttk.Treeview(frame_table, columns=columns, show="headings", height=12, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set,)

        scroll_y.config(command=self.trHienThi.yview)
        scroll_x.config(command=self.trHienThi.xview)

        self.trHienThi.heading("MaTivi", text="Mã Tivi")
        self.trHienThi.heading("TenTivi", text="Tên Tivi")
        self.trHienThi.heading("TenHang", text="Hãng")
        self.trHienThi.heading("KichThuoc", text="Kích thước")
        self.trHienThi.heading("DoPhanGiai", text="Độ phân giải")
        self.trHienThi.heading("GiaBan", text="Giá bán")
        self.trHienThi.heading("SoLuongTon", text="Số lượng")
        self.trHienThi.heading("NamSanXuat", text="Năm SX")
        self.trHienThi.heading("MoTa", text="Mô tả")

        self.trHienThi.column("MaTivi", width=80, anchor="center")
        self.trHienThi.column("TenTivi", width=200, anchor="w")
        self.trHienThi.column("TenHang", width=100, anchor="w")
        self.trHienThi.column("KichThuoc", width=100, anchor="center")
        self.trHienThi.column("DoPhanGiai", width=100, anchor="center")
        self.trHienThi.column("GiaBan", width=100, anchor="e")
        self.trHienThi.column("SoLuongTon", width=80, anchor="center")
        self.trHienThi.column("NamSanXuat", width=80, anchor="center")
        self.trHienThi.column("MoTa", width=200, anchor="w")

        self.trHienThi.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        if(self.user != "admin"):
            self.btn_chonanh.grid_forget()
            frame_buttons.pack_forget()

        self.trHienThi.bind("<<TreeviewSelect>>", self.chon_dong)

        self.load_hang_san_xuat()
        self.hienthi_dulieu()

    def load_hang_san_xuat(self):
        try:
            self.cursor.execute("SELECT MaHang, TenHang FROM HangSanXuat ORDER BY TenHang")

            self.hang_dict = {}
            hang_list = []

            for row in self.cursor.fetchall():
                ma_hang = row.MaHang
                ten_hang = row.TenHang
                self.hang_dict[ten_hang] = ma_hang
                hang_list.append(ten_hang)

            self.cbo_hang["values"] = hang_list

        except Exception as e:
            messagebox.showerror("Lỗi", "Không thể load danh sách hãng: " + str(e))

    def hienthi_dulieu(self):
        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            query = """
                SELECT t.MaTivi, t.HinhAnh, t.TenTivi, h.TenHang, t.KichThuoc, 
                       t.DoPhanGiai, t.GiaBan, t.SoLuongTon, t.NamSanXuat, t.MoTa, h.MaHang
                FROM Tivi t
                INNER JOIN HangSanXuat h ON t.MaHang = h.MaHang
                ORDER BY t.MaTivi """
            self.cursor.execute(query)

            for row in self.cursor.fetchall():
                ma_tivi = row.MaTivi

                self.trHienThi.insert("", "end", values=(ma_tivi, row.TenTivi, row.TenHang, row.KichThuoc or "", row.DoPhanGiai or "", f"{row.GiaBan:,.0f}" if row.GiaBan else "0", row.SoLuongTon or 0, row.NamSanXuat or "", row.MoTa or "",),)

        except Exception as e:
            messagebox.showerror("Lỗi", "Không thể load danh sách tivi: " + str(e))

    def chon_dong(self, event):
        selected = self.trHienThi.selection()
        if not selected:
            return

        self.selected_item = selected[0]
        values = self.trHienThi.item(self.selected_item)["values"]

        self.xoa_form()

        self.txt_matv.insert(0, values[0])
        self.txt_tentivi.insert(0, values[1])
        self.cbo_hang.set(values[2])
        self.txt_kichthuoc.insert(0, values[3])
        self.txt_dophangiai.insert(0, values[4])

        gia_ban = str(values[5]).replace(",", "")
        self.txt_giaban.insert(0, gia_ban)
        
        self.txt_soluong.config(state="normal")
        self.txt_soluong.delete(0, tk.END)
        self.txt_soluong.insert(0, values[6])
        self.txt_soluong.config(state="disabled")

        self.txt_namsanxuat.insert(0, values[7])
        self.txt_mota.insert(0, values[8])

        self.hienthi_anh(values[0])

    def hienthi_anh(self, ma_tivi):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT HinhAnh FROM Tivi WHERE MaTivi = ?", (ma_tivi,))
            row = cursor.fetchone()

            if row and row[0]:
                image_data = row[0]
                anh_pil = Image.open(io.BytesIO(image_data))
                anh_pil = anh_pil.resize((120, 120)) 

                self.anh_hien_tai = ImageTk.PhotoImage(anh_pil, master=self)

                self.pic_anhtivi.delete("all")
                self.pic_anhtivi.create_image(60, 60, image=self.anh_hien_tai, anchor="center")

                self.pic_anhtivi.image = self.anh_hien_tai

            else:
                self.pic_anhtivi.delete("all")
                self.pic_anhtivi.create_text(60, 60, text="(Không có ảnh)", fill="gray")

        except Exception as e:
            messagebox.showerror("Lỗi hiển thị ảnh: ", str(e))

    def chon_anh(self):
        if not self.selected_item:
            messagebox.showerror("Lỗi", "Vui long chọn tivi trên danh sách.")
            return
        file_path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")],)

        if file_path:
            try:
                with open(file_path, "rb") as file:
                    self.image_data = file.read()

                anh_pil = Image.open(io.BytesIO(self.image_data))
                anh_pil = anh_pil.resize((120, 120))

                self.anh_hien_tai = ImageTk.PhotoImage(anh_pil, master=self)

                self.pic_anhtivi.delete("all")
                self.pic_anhtivi.create_image(60, 60, image=self.anh_hien_tai, anchor="center")
                self.pic_anhtivi.image = self.anh_hien_tai

            except Exception as e:
                messagebox.showerror("Lỗi chọn ảnh", str(e))

    def them_tivi(self):
        if not self.xac_nhan_du_lieu():
            return

        ma = self.txt_matv.get().strip()
        ten = self.txt_tentivi.get().strip()
        ten_hang = self.cbo_hang.get()
        ma_hang = self.hang_dict.get(ten_hang)
        kichthuoc = self.txt_kichthuoc.get().strip()
        dophangiai = self.txt_dophangiai.get().strip()
        giaban = float(self.txt_giaban.get()) if self.txt_giaban.get().strip() else 0
        soluong = 0
        namsanxuat = (int(self.txt_namsanxuat.get())
            if self.txt_namsanxuat.get().strip()
            else None)
        mota = self.txt_mota.get().strip()

        for item in self.trHienThi.get_children():
            if self.trHienThi.item(item)["values"][0] == ma:
                messagebox.showwarning("Cảnh báo", f"Mã tivi '{ma}' đã tồn tại!")
                return

        self.trHienThi.insert("", "end",  values=(ma, ten, ten_hang, kichthuoc, dophangiai, f"{giaban:,.0f}", soluong, namsanxuat if namsanxuat else "", mota,),)

        self.ds_them.append(( ma, self.image_data, ten, ma_hang, kichthuoc or None, dophangiai or None, giaban, soluong, namsanxuat, mota or None,))

        self.xoa_form()
        messagebox.showinfo("Thành công", "Đã thêm dòng mới! Nhấn 'Lưu' để lưu vào CSDL.")

    def sua_tivi(self):
        if not self.selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần sửa!")
            return

        if not self.xac_nhan_du_lieu():
            return

        ma = self.txt_matv.get().strip()
        ten = self.txt_tentivi.get().strip()
        ten_hang = self.cbo_hang.get()
        ma_hang = self.hang_dict.get(ten_hang)
        kichthuoc = self.txt_kichthuoc.get().strip()
        dophangiai = self.txt_dophangiai.get().strip()
        giaban = float(self.txt_giaban.get()) if self.txt_giaban.get().strip() else 0
        soluong = 0
        namsanxuat = (int(self.txt_namsanxuat.get())
            if self.txt_namsanxuat.get().strip()
            else None)
        mota = self.txt_mota.get().strip()

        item = self.trHienThi.item(self.selected_item)
        ma_cu = item["values"][0]

        self.trHienThi.item(
            self.selected_item,
            values=(ma, ten, ten_hang, kichthuoc, dophangiai, f"{giaban:,.0f}", soluong, namsanxuat if namsanxuat else "", mota,),)

        is_new = any(item[0] == ma_cu for item in self.ds_them)

        if is_new:
            self.ds_them = [item for item in self.ds_them if item[0] != ma_cu]
            self.ds_them.append((ma, self.image_data,  ten, ma_hang, kichthuoc or None, dophangiai or None, giaban, soluong, namsanxuat, mota or None,))
        else:
            self.ds_sua = [item for item in self.ds_sua if item[10] != ma_cu]
            self.ds_sua.append((ma, self.image_data, ten, ma_hang, kichthuoc or None, dophangiai or None, giaban, soluong, namsanxuat, mota or None, ma_cu,))

        messagebox.showinfo("Thành công", "Đã cập nhật dòng! Nhấn 'Lưu' để lưu vào CSDL.")

    def xoa_tivi(self):
        if not self.selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần xóa!")
            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa dòng này?")
        if not confirm:
            return

        item = self.trHienThi.item(self.selected_item)
        ma = item["values"][0]

        self.trHienThi.delete(self.selected_item)

        is_new = any(item[0] == ma for item in self.ds_them)
        if is_new:
            self.ds_them = [item for item in self.ds_them if item[0] != ma]
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

            confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn lưu các thay đổi?")
            if not confirm:
                return

            for ma in self.ds_xoa:
                self.cursor.execute("DELETE FROM Tivi WHERE MaTivi = ?", (ma,))

            for item in self.ds_them:
                query = """
                    INSERT INTO Tivi (MaTivi, HinhAnh, TenTivi, MaHang, KichThuoc, 
                                      DoPhanGiai, GiaBan, SoLuongTon, NamSanXuat, MoTa)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
                self.cursor.execute(query, item)

            for item in self.ds_sua:
                query = """
                    UPDATE Tivi 
                    SET MaTivi = ?, HinhAnh = ?, TenTivi = ?, MaHang = ?, KichThuoc = ?, 
                        DoPhanGiai = ?, GiaBan = ?, SoLuongTon = ?, NamSanXuat = ?, MoTa = ?
                    WHERE MaTivi = ? """
                self.cursor.execute(query, item)

            self.conn.commit()
            messagebox.showinfo("Thành công", "Đã lưu thay đổi vào CSDL!")

        except pyodbc.IntegrityError as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", "Lỗi ràng buộc dữ liệu:" + str(e))
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", "Không thể lưu dữ liệu:" + str(e))

        self.hienthi_dulieu()
        self.xoa_form()
        self.ds_them.clear()
        self.ds_sua.clear()
        self.ds_xoa.clear()
        self.controller.load_form("NhapHangVaPhieuNhap")
        self.controller.load_form("BanHangVaHoaDon")

    def lam_moi(self):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn hủy các thay đổi?")
        if not confirm:
            return

        self.ds_them.clear()
        self.ds_sua.clear()
        self.ds_xoa.clear()

        self.hienthi_dulieu()
        self.load_hang_san_xuat()
        self.xoa_form()
        self.txt_timkiem.delete(0, tk.END)
        messagebox.showinfo("Thông báo", "Đã làm mới dữ liệu!")

    def tim_kiem(self):
        tu_tim_kiem = self.txt_timkiem.get().strip()
        if not tu_tim_kiem:
            messagebox.showinfo("Thông báo", "Vui lòng nhập từ khóa tìm kiếm.")
            self.hienthi_dulieu()
            return

        try:
            for item in self.trHienThi.get_children():
                self.trHienThi.delete(item)

            if self.search_option.get() == "ma":
                query = """
                    SELECT t.MaTivi, t.HinhAnh, t.TenTivi, h.TenHang, t.KichThuoc, 
                           t.DoPhanGiai, t.GiaBan, t.SoLuongTon, t.NamSanXuat, t.MoTa
                    FROM Tivi t
                    INNER JOIN HangSanXuat h ON t.MaHang = h.MaHang
                    WHERE t.MaTivi LIKE ?
                    ORDER BY t.MaTivi """
            else:
                query = """
                    SELECT t.MaTivi, t.HinhAnh, t.TenTivi, h.TenHang, t.KichThuoc, 
                           t.DoPhanGiai, t.GiaBan, t.SoLuongTon, t.NamSanXuat, t.MoTa
                    FROM Tivi t
                    INNER JOIN HangSanXuat h ON t.MaHang = h.MaHang
                    WHERE t.TenTivi LIKE ?
                    ORDER BY t.MaTivi """

            self.cursor.execute(query, (f"%{tu_tim_kiem}%",))
            rows = self.cursor.fetchall()

            for row in rows:
                ma_tivi = row.MaTivi

                self.trHienThi.insert("", "end", values=(ma_tivi, row.TenTivi, row.TenHang, row.KichThuoc or "", row.DoPhanGiai or "", f"{row.GiaBan:,.0f}" if row.GiaBan else "0", row.SoLuongTon or 0, row.NamSanXuat or "", row.MoTa or "",),)

            if not rows:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")

    def xac_nhan_du_lieu(self):
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

    def xoa_form(self):
        self.txt_matv.delete(0, tk.END)
        self.txt_tentivi.delete(0, tk.END)
        self.cbo_hang.set("")
        self.txt_kichthuoc.delete(0, tk.END)
        self.txt_dophangiai.delete(0, tk.END)
        self.txt_giaban.delete(0, tk.END)
        self.txt_soluong.delete(0, tk.END)
        self.txt_namsanxuat.delete(0, tk.END)
        self.txt_mota.delete(0, tk.END)

        self.image_data = None
        self.anh_hien_tai = None
        self.pic_anhtivi.delete("all")
        self.pic_anhtivi.create_text(30, 40, text="Ảnh\ntivi", font=("Segoe UI", 10), fill="#888")

    def huy(self):
        self.txt_timkiem.delete(0, tk.END)
        self.hienthi_dulieu()