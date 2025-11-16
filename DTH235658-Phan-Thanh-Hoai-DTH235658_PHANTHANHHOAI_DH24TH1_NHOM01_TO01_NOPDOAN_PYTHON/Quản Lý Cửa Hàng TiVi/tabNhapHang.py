import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from tkcalendar import DateEntry
from datetime import datetime

class tabNhapHang(tk.Frame):
    def __init__(self, parent, conn, tab_phieunhap=None):
        super().__init__(parent, bg="white")

        # === CHUỖI KẾT NỐI ===
        self.conn = conn

        # Khai báo trống cho các dict
        self.dict_nv = {}
        self.dict_ncc = {}
        self.dict_tivi = {}

        self.tab_phieunhap = tab_phieunhap

        # === KHUNG 1 – THÔNG TIN PHIẾU NHẬP ===
        frame_phieu = tk.LabelFrame(self, text="Thông tin Phiếu nhập", bg="white", font=("Segoe UI", 12, "bold"), fg="#0D47A1", padx=10, pady=10)
        frame_phieu.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_phieu, text="Mã phiếu:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_maphieunhap = ttk.Entry(frame_phieu, width=46)
        self.txt_maphieunhap.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_phieu, text="Ngày nhập:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.dt_ngaynhap = DateEntry(frame_phieu, width=44, date_pattern="dd/mm/yyyy", state="readonly")
        self.dt_ngaynhap.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_phieu, text="Mã nhân viên nhập:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cb_manhanvien = ttk.Combobox(frame_phieu, width=44, state="readonly")
        self.cb_manhanvien.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_phieu, text="Mã nhà cung cấp:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.cb_manhacungcap = ttk.Combobox(frame_phieu, width=44, state="readonly")
        self.cb_manhacungcap.grid(row=1, column=3, padx=5, pady=5)

        # === KHUNG 2 – SẢN PHẨM NHẬP ===
        frame_sanpham = tk.LabelFrame(self, text="Sản phẩm trong Phiếu nhập", bg="white", font=("Segoe UI", 12, "bold"), fg="#0D47A1", padx=10, pady=10)
        frame_sanpham.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_sanpham, text="Mã Tivi:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cb_mativi = ttk.Combobox(frame_sanpham, width=33, state="readonly")
        self.cb_mativi.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_sanpham, text="Số lượng:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.txt_soluong = ttk.Entry(frame_sanpham, width=33)
        self.txt_soluong.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_sanpham, text="Giá nhập:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.txt_gianhap = ttk.Entry(frame_sanpham, width=33)
        self.txt_gianhap.grid(row=0, column=5, padx=5, pady=5)

        # === NÚT CHỨC NĂNG ===
        frame_buttons = tk.Frame(self, bg="white")
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="➕ Thêm phiếu", bg="#EBDA42", fg="white", font=("Segoe UI", 11, "bold"), command=self.ThemPhieuNhapChiTiet, padx=20, pady=5, bd=0).grid(row=0, column=0, padx=10)
        tk.Button(frame_buttons, text="✏️ Sửa", bg="#FB8C00", fg="white", font=("Segoe UI", 11, "bold"), command=self.SuaPhieuNhapChiTiet, padx=20, pady=5, bd=0).grid(row=0, column=1, padx=10)
        tk.Button(frame_buttons, text="🗑️ Xóa", bg="#E53935", fg="white", font=("Segoe UI", 11, "bold"), command=self.XoaPhieuNhapChiTiet,padx=20, pady=5, bd=0).grid(row=0, column=2, padx=10)
        tk.Button(frame_buttons, text="🔄 Làm mới", bg="#1E88E5", fg="white", font=("Segoe UI", 11, "bold"), command=self.LamMoi, padx=20, pady=5, bd=0).grid(row=0, column=3, padx=10)

        # === BẢNG DANH SÁCH SẢN PHẨM ===
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("MaPhieu", "NgayNhap", "MaNV", "TenNV", "MaNCC", "TenNCC", "MaTivi", "TenTivi", "SoLuong", "GiaNhap", "ThanhTien")

        # --- Tạo Scrollbar ---
        scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")

        self.trHienThi = ttk.Treeview( frame_table, show="headings",  columns=columns, height=12, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # --- Gắn Scrollbar ---
        scroll_y.config(command=self.trHienThi.yview)
        scroll_x.config(command=self.trHienThi.xview)

        # --- Bố trí Scrollbar ---
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.trHienThi.pack(fill="both", expand=True)

        self.trHienThi.heading("MaPhieu", text="Mã phiếu")
        self.trHienThi.heading("NgayNhap", text="Ngày nhập")
        self.trHienThi.heading("MaNV", text="Mã nhân viên")
        self.trHienThi.heading("TenNV", text="Tên nhân viên")
        self.trHienThi.heading("MaNCC", text="Mã nhà cung cấp")
        self.trHienThi.heading("TenNCC", text="Tên nhà cung cấp")
        self.trHienThi.heading("MaTivi", text="Mã tivi")
        self.trHienThi.heading("TenTivi", text="Tên tivi")
        self.trHienThi.heading("SoLuong", text="Số lượng")
        self.trHienThi.heading("GiaNhap", text="Giá nhập")
        self.trHienThi.heading("ThanhTien", text="Thành tiền")

        self.trHienThi.column("MaPhieu", anchor="center", width=150)
        self.trHienThi.column("NgayNhap", anchor="center", width=150) 
        self.trHienThi.column("MaNV", anchor="center", width=150)
        self.trHienThi.column("MaNCC", anchor="center", width=200)
        self.trHienThi.column("MaTivi", anchor="center", width=150)
        self.trHienThi.column("SoLuong", anchor="center", width=120)
        self.trHienThi.column("TenNV", anchor="w", width=150)
        self.trHienThi.column("TenNCC", anchor="w", width=240)
        self.trHienThi.column("TenTivi", anchor="w", width=200)
        self.trHienThi.column("GiaNhap", anchor="e", width=150)
        self.trHienThi.column("ThanhTien", anchor="e", width=150)
        
        # Style Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        # ==== TỔNG TIỀN VÀ NÚT NHẬP HÀNG ====
        frame_bottom = tk.Frame(self, bg="white")
        frame_bottom.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_bottom, text="Tổng tiền:", bg="white", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.lbl_tongtien = tk.Label(frame_bottom, text="0 VNĐ", bg="white", font=("Segoe UI", 11, "bold"), fg="#E53935")
        self.lbl_tongtien.pack(side="left", padx=5)
        tk.Button(frame_bottom, text="📦 Nhập hàng", bg="#43A047", fg="white",font=("Segoe UI", 11, "bold"), command=self.TaoPhieuNhap, padx=15, pady=5, bd=0).pack(side="right", padx=5)

        self.trHienThi.bind("<<TreeviewSelect>>", self.HienThi_ChiTiet)
        
        self.Load_Comnobox()
    
    def Load_Comnobox(self):
        cursor = self.conn.cursor()

        # Load nhân viên
        cursor.execute("SELECT MaNV, TenNV FROM NHANVIEN")
        for ma, ten in cursor.fetchall():
            self.dict_nv[ma] = ten
        self.cb_manhanvien["values"] = list(self.dict_nv.keys())

        # Load nhà cung cấp
        cursor.execute("SELECT MaNCC, TenNCC FROM NHACUNGCAP")
        for ma, ten in cursor.fetchall():
            self.dict_ncc[ma] = ten
        self.cb_manhacungcap["values"] = list(self.dict_ncc.keys())

        # Load tivi
        cursor.execute("SELECT MaTiVi, TenTiVi FROM TIVI")
        for ma, ten in cursor.fetchall():
            self.dict_tivi[ma] = ten
        self.cb_mativi["values"] = list(self.dict_tivi.keys())

        cursor.close()

    def TinhTongTien(self):
        tong_tien = 0
        for item in self.trHienThi.get_children():
            values = self.trHienThi.item(item, "values")
            thanh_tien = float(values[10].replace(",", ""))
            tong_tien = tong_tien +  thanh_tien
        self.lbl_tongtien.config(text=f"{tong_tien:,.0f} VNĐ")

    def KiemTraMaPhieuNhapHang(self, ma_phieu):
        try:
            cursor = self.conn.cursor()
            cursor.execute(""" 
                    SELECT COUNT(*)
                    FROM PHIEUNHAPHANG
                    WHERE MaPhieuNhap = ?    
                           """, (ma_phieu,))
            
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0

        except Exception as e:
            messagebox.showerror("Cảnh báo", "Có lỗi xảy ra khi kiểm tra mã phiếu nhập hàng vừa nhập đã có tồn tại không:\n" + str(e))

    def kiemtradulieu(self):
        ma_phieu = self.txt_maphieunhap.get()
        ma_nv = self.cb_manhanvien.get()
        ma_ncc = self.cb_manhacungcap.get()

        if not ma_phieu:
            messagebox.showwarning("Cảnh báo", "Mã phiếu không được để trống!")
            self.txt_maphieunhap.focus()
            return False
        
        if not ma_nv:
            messagebox.showwarning("Cảnh báo", "Mã nhân viên nhập không được để trống!")
            self.cb_manhanvien.focus()
            return False
        
        if not ma_ncc:
            messagebox.showwarning("Cảnh báo", "Mã nhà cung cấp không được để trống!")
            self.cb_manhacungcap.focus()
            return False

        ma_tivi = self.cb_mativi.get()
        so_luong_str = self.txt_soluong.get().strip()
        gia_nhap_str = self.txt_gianhap.get().strip()
        
        if not ma_tivi:
            messagebox.showwarning("Cảnh báo", "Mã tivi không được trống!")
            self.cb_mativi.focus()
            return False
        
        if not so_luong_str:
            messagebox.showwarning("Cảnh báo", "Số lượng không được trống!")
            self.txt_soluong.focus()
            return False
            
        try:
            so_luong = int(so_luong_str)
            if so_luong <= 0:
                messagebox.showwarning("Cảnh báo", "Số lượng nhập phải lớn hơn 0!")
                self.txt_soluong.focus()
                return False
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Số lượng phải là số nguyên dương!")
            self.txt_soluong.focus()
            return False

        if not gia_nhap_str:
            messagebox.showwarning("Cảnh báo", "Giá nhập không được trống!")
            self.txt_gianhap.focus()
            return False

        try:
            gia_nhap = float(gia_nhap_str)
            if gia_nhap < 0:
                messagebox.showwarning("Cảnh báo", "Giá nhập phải lớn hơn hoặc bằng 0!")
                self.txt_gianhap.focus()
                return False
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Giá nhập phải là một con số!")
            self.txt_gianhap.focus()
            return False

        return True 
    
    def ThemPhieuNhapChiTiet(self):
        if not self.kiemtradulieu():
            return 

        ma_phieu = self.txt_maphieunhap.get()
        ngay_nhap = self.dt_ngaynhap.get_date()
        ma_nv = self.cb_manhanvien.get()
        ten_nv = self.dict_nv.get(ma_nv, "")
        ma_ncc = self.cb_manhacungcap.get()
        ten_ncc = self.dict_ncc.get(ma_ncc, "")
        ma_tivi = self.cb_mativi.get()
        ten_tivi = self.dict_tivi.get(ma_tivi, "")
        
        so_luong = int(self.txt_soluong.get())
        gia_nhap = float(self.txt_gianhap.get())
        thanh_tien = so_luong * gia_nhap

        if(self.KiemTraMaPhieuNhapHang(ma_phieu)):
            messagebox.showwarning("Cảnh báo", "Mã phiếu nhập hàng đã tồn tại!")
            self.txt_maphieunhap.delete(0, tk.END)
            self.txt_maphieunhap.focus()
            return
        
        else:
            try:

                # Kiểm tra trùng mã Tivi trong cùng phiếu
                for item in self.trHienThi.get_children():
                    values = self.trHienThi.item(item, "values")
                    if values[6] == ma_tivi:
                        traloi = messagebox.askyesno("Trùng sản phẩm", "Tivi" + ma_tivi+ " đã có trong phiếu này.\nBạn có muốn cộng dồn số lượng không?")
                        if traloi:
                            # Cộng dồn số lượng và cập nhật thành tiền
                            soluongcu = int(values[8])
                            soluongmoi = soluongcu + so_luong
                            thanhtienmoi = soluongmoi * gia_nhap
                            self.trHienThi.item(item, values=( ma_phieu, ngay_nhap.strftime("%d/%m/%Y"), ma_nv, ten_nv, ma_ncc, ten_ncc, ma_tivi, ten_tivi, soluongmoi, f"{gia_nhap:,.0f}", f"{thanhtienmoi:,.0f}"))
                        return

                # Thêm phiếu nhập vào trHienThi
                self.trHienThi.insert("", tk.END, values=(ma_phieu, ngay_nhap.strftime("%d/%m/%Y"), ma_nv, ten_nv, ma_ncc, ten_ncc, ma_tivi, ten_tivi, so_luong, f"{gia_nhap:,.0f}", f"{thanh_tien:,.0f}"))

                # Khóa phiếu nhập sau khi thêm
                self.txt_maphieunhap.config(state="disabled")
                self.dt_ngaynhap.config(state="disabled")
                self.cb_manhanvien.config(state="disabled")
                self.cb_manhacungcap.config(state="disabled")

                # Xóa dữ liệu chi tiết phiếu nhập sau khi thêm
                self.cb_mativi.set("")
                self.txt_soluong.delete(0, tk.END)
                self.txt_gianhap.delete(0, tk.END)

                # Cập nhật tổng tiền
                self.TinhTongTien()

            except Exception as e:
                messagebox.showerror("Lỗi", "Đã xảy ra lỗi:" + str(e))
        
    def HienThi_ChiTiet(self, event):
        selected = self.trHienThi.selection()
        if not selected:
            return
        item = self.trHienThi.item(selected[0], "values")
        if not item:
            return

        # Gán giá trị lên form
        self.txt_maphieunhap.delete(0, tk.END)
        self.txt_maphieunhap.insert(0, item[0])

        self.dt_ngaynhap.set_date(item[1])
        self.cb_manhanvien.set(item[2])
        self.cb_manhacungcap.set(item[4])
        self.cb_mativi.set(item[6])

        self.txt_soluong.delete(0, tk.END)
        self.txt_soluong.insert(0, item[8])

        self.txt_gianhap.delete(0, tk.END)
        gia_nhap = float(item[9].replace(",", ""))
        self.txt_gianhap.insert(0,  gia_nhap)

    def SuaPhieuNhapChiTiet(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu nhập để sửa!")
            return
        
        if not self.kiemtradulieu():
            return 
            
        ma_phieu = self.txt_maphieunhap.get()
        ngay_nhap = self.dt_ngaynhap.get_date()
        ma_nv = self.cb_manhanvien.get()
        ten_nv = self.dict_nv.get(ma_nv, "")
        ma_ncc = self.cb_manhacungcap.get()
        ten_ncc = self.dict_ncc.get(ma_ncc, "")
        ma_tivi = self.cb_mativi.get()
        ten_tivi = self.dict_tivi.get(ma_tivi, "")
        so_luong = int(self.txt_soluong.get())
        gia_nhap = float(self.txt_gianhap.get())
        thanh_tien = so_luong * gia_nhap
    
        try: 

            # Kiểm tra trùng mã Tivi trong cùng phiếu (trừ dòng hiện tại)
            for item in self.trHienThi.get_children():
                if item == selected[0]:
                    continue

                values = self.trHienThi.item(item, "values")
                if  values[6] == ma_tivi:
                    traloi = messagebox.askyesno("Trùng sản phẩm", "Tivi" + ma_tivi+ " đã có trong phiếu này.\nBạn có muốn cộng dồn số lượng không?")
                    if traloi:
                        # Cộng dồn số lượng và cập nhật thành tiền
                        soluongcu = int(values[8])
                        soluongmoi = soluongcu + so_luong
                        thanhtienmoi = soluongmoi * gia_nhap
                        self.trHienThi.item(item, values=( ma_phieu, ngay_nhap.strftime("%d/%m/%Y"), ma_nv, ten_nv, ma_ncc, ten_ncc, ma_tivi, ten_tivi, soluongmoi, f"{gia_nhap:,.0f}", f"{thanhtienmoi:,.0f}"))

                        # Xóa dòng đang sửa (vì đã gộp vào dòng kia)
                        self.trHienThi.delete(selected[0])

                        # Cập nhật tổng tiền
                        self.TinhTongTien()
                    return

            # Cập nhật phiếu nhập trong trHienThi
            self.trHienThi.item(selected[0], values=(ma_phieu, ngay_nhap.strftime("%d/%m/%Y"), ma_nv, ten_nv, ma_ncc, ten_ncc, ma_tivi, ten_tivi, so_luong, f"{gia_nhap:,.0f}", f"{thanh_tien:,.0f}"))

            # Xóa dữ liệu chi tiết phiếu nhập sau khi thêm
            self.cb_mativi.set("")
            self.txt_soluong.delete(0, tk.END)
            self.txt_gianhap.delete(0, tk.END)

            # Cập nhật tổng tiền
            self.TinhTongTien()

        except Exception as e:
            messagebox.showerror("Lỗi", "Đã xảy ra lỗi:" + str(e))
    
    def XoaPhieuNhapChiTiet(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu nhập để xóa!")
            return
        
        traloi = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa phiếu nhập này không?")
        if traloi:
            self.trHienThi.delete(selected[0])

            # Cập nhật tổng tiền
            self.TinhTongTien()
    
    def LamMoi(self):
        self.txt_maphieunhap.config(state="normal")
        self.dt_ngaynhap.config(state="normal")
        self.cb_manhanvien.config(state="readonly")
        self.cb_manhacungcap.config(state="readonly")

        self.txt_maphieunhap.delete(0, tk.END)
        self.dt_ngaynhap.set_date(datetime.today())
        self.cb_manhanvien.set("")
        self.cb_manhacungcap.set("")
        self.cb_mativi.set("")
        self.txt_soluong.delete(0, tk.END)
        self.txt_gianhap.delete(0, tk.END)

        self.trHienThi.delete(*self.trHienThi.get_children())
        self.lbl_tongtien.config(text="0 VNĐ")

    def TaoPhieuNhap(self):
        if not self.trHienThi.get_children():
            messagebox.showwarning("Cảnh báo", "Không có phiếu nhập nào để thực hiện tạo phiếu nhập hàng!")
            return
        
        ma_phieu = self.txt_maphieunhap.get()
        ngay_nhap = self.dt_ngaynhap.get_date().strftime("%Y-%m-%d")
        ma_nv = self.cb_manhanvien.get()
        ma_ncc = self.cb_manhacungcap.get()

        try:
            cursor = self.conn.cursor()

            # Thêm phiếu nhập hàng - vì 1 phiếu nhập có thể có nhiều chi tiết nên chỉ cần thêm 1 lần
            cursor.execute("""
                INSERT INTO PHIEUNHAPHANG (MaPhieuNhap, NgayNhap, MaNV, MaNCC)
                VALUES (?, ?, ?, ?)
            """, (ma_phieu, ngay_nhap, ma_nv, ma_ncc))

            for item in self.trHienThi.get_children():
                values = self.trHienThi.item(item, "values")
                ma_tivi = values[6]
                so_luong = int(values[8])
                gia_nhap = float(values[9].replace(",", ""))

                # Thêm chi tiết phiếu nhập hàng
                cursor.execute("""
                    INSERT INTO CHITIETPHIEUNHAP (MaPhieuNhap, MaTiVi, SoLuong, GiaNhap)
                    VALUES (?, ?, ?, ?)
                """, (ma_phieu, ma_tivi, so_luong, gia_nhap))

            self.conn.commit()
            cursor.close()
            messagebox.showinfo("Thành công", "Tạo phiếu nhập hàng thành công!")
            self.LamMoi()

            # Cập nhật lại tab phiếu nhập hàng nếu có
            if self.tab_phieunhap:
                self.tab_phieunhap.load_phieu_nhap()

        except Exception as e:
            messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi tạo phiếu nhập hàng:\n" + str(e))

    
