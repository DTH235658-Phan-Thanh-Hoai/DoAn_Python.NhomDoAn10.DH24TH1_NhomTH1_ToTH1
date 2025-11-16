import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from tkcalendar import DateEntry
from datetime import datetime

# === TAB BÁN HÀNG ===
class tabBanHang(tk.Frame):
    def __init__(self, parent, conn, user, tab_hoadon=None):
        super().__init__(parent, bg="white")

        # === CHUỖI KẾT NỐI ===
        self.conn = conn

        # === LƯU MÃ NHÂN VIÊN ===
        self.user = user

        # Khai báo trống cho các dict
        self.dict_nv = {}
        self.dict_kh = {}
        self.dict_tivi = {}

        # === LƯU THAM CHIẾU  ===
        self.tab_hoadon= tab_hoadon

        # === KHUNG 1 – THÔNG TIN HÓA ĐƠN ===
        frame_phieu = tk.LabelFrame(self, text="Thông tin Hóa đơn", bg="white", font=("Segoe UI", 12, "bold"), fg="#0D47A1", padx=10, pady=10)
        frame_phieu.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_phieu, text="Mã hóa đơn:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_mahoadonban = ttk.Entry(frame_phieu, width=46)
        self.txt_mahoadonban.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_phieu, text="Ngày bán:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.dt_ngayban = DateEntry(frame_phieu, width=44, date_pattern="dd/mm/yyyy", state="readonly")
        self.dt_ngayban.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_phieu, text="Mã nhân viên bán:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cb_manhanvien = ttk.Combobox(frame_phieu, width=44, state="readonly")
        self.cb_manhanvien.grid(row=1, column=1, padx=5, pady=5)

        if self.user != "admin":
            self.cb_manhanvien.config(state="readonly")

        tk.Label(frame_phieu, text="Mã khách hàng:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.cb_makhachhang = ttk.Combobox(frame_phieu, width=44, state="readonly")
        self.cb_makhachhang.grid(row=1, column=3, padx=5, pady=5)

        # === KHUNG 2 – SẢN PHẨM BÁN ===
        frame_sanpham = tk.LabelFrame(self, text="Sản phẩm trong Hóa đơn", bg="white", font=("Segoe UI", 12, "bold"), fg="#0D47A1", padx=10, pady=10)
        frame_sanpham.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_sanpham, text="Mã CTHD:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_macthd = ttk.Entry(frame_sanpham, width=20)
        self.txt_macthd.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_sanpham, text="Mã Tivi:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.cb_mativi = ttk.Combobox(frame_sanpham, width=20, state="readonly")
        self.cb_mativi.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_sanpham, text="Số lượng:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.txt_soluong = ttk.Entry(frame_sanpham, width=20)
        self.txt_soluong.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(frame_sanpham, text="Giá bán:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=6, sticky="w", padx=5, pady=5)
        self.txt_giaban = ttk.Entry(frame_sanpham, width=25, state="disabled")
        self.txt_giaban.grid(row=0, column=7, padx=5, pady=5)

        # === NÚT CHỨC NĂNG ===
        frame_buttons = tk.Frame(self, bg="white")
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="➕ Thêm hóa đơn", bg="#EBDA42", fg="white", font=("Segoe UI", 11, "bold"), command=self.ThemHoaDonChiTiet, padx=20, pady=5, bd=0).grid(row=0, column=0, padx=10)
        tk.Button(frame_buttons, text="✏️ Sửa", bg="#FB8C00", fg="white", font=("Segoe UI", 11, "bold"), command=self.SuaHoaDonChiTiet, padx=20, pady=5, bd=0).grid(row=0, column=1, padx=10)
        tk.Button(frame_buttons, text="🗑️ Xóa", bg="#E53935", fg="white", font=("Segoe UI", 11, "bold"), command=self.XoaHoaDonChiTiet, padx=20, pady=5, bd=0).grid(row=0, column=2, padx=10)
        tk.Button(frame_buttons, text="🔄 Làm mới", bg="#1E88E5", fg="white", font=("Segoe UI", 11, "bold"), command=self.LamMoi, padx=20, pady=5, bd=0).grid(row=0, column=3, padx=10)

        # === BẢNG DANH SÁCH SẢN PHẨM ===
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("MaHD", "NgayBan", "MaNV", "TenNV", "MaKH", "TenKH", "MaTivi", "TenTivi", "SoLuong", "GiaBan", "ThanhTien")

        # --- Tạo Scrollbar ---
        scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")

        self.trHienThi = ttk.Treeview(frame_table, show="headings", columns=columns, height=12, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # --- Gắn Scrollbar ---
        scroll_y.config(command=self.trHienThi.yview)
        scroll_x.config(command=self.trHienThi.xview)

        # --- Bố trí Scrollbar ---
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.trHienThi.pack(fill="both", expand=True)

        self.trHienThi.heading("MaHD", text="Mã hóa đơn")
        self.trHienThi.heading("NgayBan", text="Ngày bán")
        self.trHienThi.heading("MaNV", text="Mã nhân viên")
        self.trHienThi.heading("TenNV", text="Tên nhân viên")
        self.trHienThi.heading("MaKH", text="Mã khách hàng")
        self.trHienThi.heading("TenKH", text="Tên khách hàng")
        self.trHienThi.heading("MaTivi", text="Mã tivi")
        self.trHienThi.heading("TenTivi", text="Tên tivi")
        self.trHienThi.heading("SoLuong", text="Số lượng")
        self.trHienThi.heading("GiaBan", text="Giá bán")
        self.trHienThi.heading("ThanhTien", text="Thành tiền")

        self.trHienThi.column("MaHD", anchor="center", width=150)
        self.trHienThi.column("NgayBan", anchor="center", width=120)
        self.trHienThi.column("MaNV", anchor="center", width=150) 
        self.trHienThi.column("TenNV", anchor="w", width=200) 
        self.trHienThi.column("MaKH", anchor="center", width=150) 
        self.trHienThi.column("TenKH", anchor="w", width=200)
        self.trHienThi.column("MaTivi", anchor="center", width=150) 
        self.trHienThi.column("TenTivi", anchor="w", width=200)
        self.trHienThi.column("SoLuong", anchor="center", width=150)
        self.trHienThi.column("GiaBan", anchor="e", width=150)
        self.trHienThi.column("ThanhTien", anchor="e", width=150)

        # Style Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        # ==== TỔNG TIỀN VÀ NÚT TẠO ĐƠN HÀNG ====
        frame_bottom = tk.Frame(self, bg="white")
        frame_bottom.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_bottom, text="Tổng tiền:", bg="white", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.lbl_tongtien = tk.Label(frame_bottom, text="0 VNĐ", bg="white", font=("Segoe UI", 11, "bold"), fg="#E53935")
        self.lbl_tongtien.pack(side="left", padx=5)

        tk.Button(frame_bottom, text="📝 Tạo đơn hàng", bg="#43A047", fg="white",font=("Segoe UI", 11, "bold"), command=self.TaoHoaDon, padx=15, pady=5, bd=0).pack(side="right", padx=5)

        self.load_Combobox()

        # Cập nhật đơn giá tự động
        self.cb_mativi.bind("<<ComboboxSelected>>", self.HienThi_GiaBan)

        self.trHienThi.bind("<<TreeviewSelect>>", self.HienThi_ChiTiet)


    def load_Combobox(self):
        cursor = self.conn.cursor()

        # Load nhân viên
        if self.user == "admin":
            cursor.execute("SELECT MaNV, TenNV FROM NHANVIEN")
            for ma, ten in cursor.fetchall():
                self.dict_nv[ma] = ten
            self.cb_manhanvien["values"] = list(self.dict_nv.keys())
        else:
            self.cb_manhanvien.config(state="normal")
            self.cb_manhanvien.set(self.user)
            self.cb_manhanvien.config(state="readonly")

        # Load khách hàng
        cursor.execute("SELECT MaKH, TenKH FROM KHACHHANG")
        for ma, ten in cursor.fetchall():
            self.dict_kh[ma] = ten
        self.cb_makhachhang["values"] = list(self.dict_kh.keys())

        # Load tivi + đơn giá
        cursor.execute("SELECT MaTivi, TenTivi, GiaBan FROM TIVI WHERE SoLuongTon > 0 ")
        for ma, ten, gia in cursor.fetchall():
            self.dict_tivi[ma] = {"TenTivi": ten, "GiaBan": gia}
        self.cb_mativi["values"] = list(self.dict_tivi.keys())

        cursor.close()

    def HienThi_GiaBan(self, event=None):
        ma_tivi = self.cb_mativi.get()
        if ma_tivi in self.dict_tivi:
            gia_ban = self.dict_tivi[ma_tivi]["GiaBan"]
            self.txt_giaban.config(state="normal")
            self.txt_giaban.delete(0, tk.END)
            self.txt_giaban.insert(0, float(gia_ban))
            self.txt_giaban.config(state="disabled")

    def TinhTongTien(self):
        tong_tien = 0
        for item in self.trHienThi.get_children():
            values = self.trHienThi.item(item, "values")
            thanh_tien = float(values[10].replace(",", ""))
            tong_tien = tong_tien + thanh_tien
        self.lbl_tongtien.config(text=f"{tong_tien:,.0f} VNĐ")

    def KiemTraMaHoaDonBan(self, ma_hd):
        try:
            cursor = self.conn.cursor()
            cursor.execute(""" 
                    SELECT COUNT(*)
                    FROM HOADONBAN
                    WHERE MaHD = ?    
                           """, (ma_hd,))
            
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0

        except Exception as e:
            messagebox.showerror("Cảnh báo", "Có lỗi xảy ra khi kiểm tra mã hóa đơn vừa nhập đã có tồn tại không:\n" + str(e))

    def KiemTraMaCTHD(self, ma_cthd):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM ChiTietHoaDon WHERE MaCTHD = ?", (ma_cthd,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi kiểm tra MaCTHD:\n{str(e)}")
            return False

    def ThemHoaDonChiTiet(self):
        # Lấy dữ liệu
        ma_hd = self.txt_mahoadonban.get().strip()
        ma_nv = self.cb_manhanvien.get()
        ten_nv = self.dict_nv.get(ma_nv,"")
        ma_kh = self.cb_makhachhang.get()
        ten_kh = self.dict_kh.get(ma_kh, "")
        ngay_ban = self.dt_ngayban.get_date()
        ma_cthd = self.txt_macthd.get().strip()
        ma_tivi = self.cb_mativi.get()
        ten_tivi = self.dict_tivi[ma_tivi]["TenTivi"]
        so_luong_str = self.txt_soluong.get().strip()

        # Kiểm tra dữ liệu nhập
        if(ma_hd == ""):
            messagebox.showwarning("Cảnh báo", "Mã hóa đơn không được để trống!")
            return
        
        elif(ma_nv == ""):
            messagebox.showwarning("Cảnh báo", "Mã nhân viên không được trống!")
            return
        
        elif(ma_kh == ""):
            messagebox.showwarning("Cảnh báo", "Mã khách hàng không được trống!")
            return
        
        elif(ma_cthd == ""):
            messagebox.showwarning("Cảnh báo", "Mã CTHD không được để trống!")
            return
        
        elif(ma_tivi == ""):
            messagebox.showwarning("Cảnh báo", "Mã tivi không được trống!")
            return
        
        elif(so_luong_str == ""):
            messagebox.showwarning("Cảnh báo", "Số lượng không được trống!")
            return
        
        if not so_luong_str.isdigit():
            messagebox.showwarning("Cảnh báo", "Số lượng phải là số nguyên dương!")
            return
        
        if(self.KiemTraMaHoaDonBan(ma_hd)):
            messagebox.showwarning("Cảnh báo", "Mã hóa đơn đã tồn tại!")
            self.txt_mahoadonban.delete(0, tk.END)
            self.txt_mahoadonban.focus()
            return
        
        so_luong = int(so_luong_str)
        gia_ban = float(self.txt_giaban.get().replace(",", ""))
        thanh_tien = so_luong * gia_ban

        # === KIỂM TRA TỒN KHO TRƯỚC KHI THỰC HIỆN ===
        ton_kho_hien_tai = self.KiemTraTonKho(ma_tivi)
        
        if so_luong <= 0:
            messagebox.showwarning("Cảnh báo", "Số lượng bán phải lớn hơn 0!")
            return
            
        if so_luong > ton_kho_hien_tai:
            messagebox.showwarning("Cảnh báo", f"Số lượng tồn kho của {ma_tivi} chỉ còn {ton_kho_hien_tai}!")
            return
        
        if self.KiemTraMaCTHD(ma_cthd):
            messagebox.showwarning("Cảnh báo", f"Mã CTHD '{ma_cthd}' đã tồn tại trong hệ thống!")
            return
        
        else:
            try:
                # Kiểm tra trùng mã Tivi trong cùng phiếu
                for item in self.trHienThi.get_children():
                    values = self.trHienThi.item(item, "values")
                    if values[6] == ma_tivi:
                        traloi = messagebox.askyesno("Trùng sản phẩm", "Tivi " + ma_tivi + " dã có trong đơn này.\nBan có muốn cộng dồn số lượng không?")
                        if traloi:
                            # Cộng dồn số lượng và cập nhật thành tiền
                            soluongcu = int(values[8])
                            soluongmoi = soluongcu + so_luong

                            # === KIỂM TRA TỒN KHO CHO TRƯỜNG HỢP CỘNG DỒN ===
                            if soluongmoi > ton_kho_hien_tai:
                                messagebox.showwarning("Cảnh báo", f"Tổng số lượng ({soluongmoi}) vượt quá tồn kho ({ton_kho_hien_tai})! Không thể cộng dồn.")
                                return
                        
                            thanhtienmoi = soluongmoi * gia_ban
                            self.trHienThi.item(item, values=(ma_hd, ngay_ban.strftime("%d/%m/%Y"), ma_nv, ten_nv, ma_kh, ten_kh, ma_tivi, ten_tivi, soluongmoi, f"{gia_ban:,.0f}", f"{thanhtienmoi:,.0f}"))
                        return

                # Thêm hóa đơn vào trHienThi
                self.trHienThi.insert("", tk.END, text=ma_cthd, values=(ma_hd, ngay_ban.strftime("%d/%m/%Y"), ma_nv, ten_nv, ma_kh, ten_kh, ma_tivi, ten_tivi, so_luong, f"{gia_ban:,.0f}", f"{thanh_tien:,.0f}"))

                # Khóa hóa đơn bán sau khi thêm
                self.txt_mahoadonban.config(state="disabled")
                self.cb_makhachhang.config(state="disabled")
                self.dt_ngayban.config(state="disabled")
                self.cb_manhanvien.config(state="disabled")

                # Xóa dữ liệu chi tiết hóa đơn sau khi thêm
                self.txt_macthd.delete(0, tk.END)
                self.cb_mativi.set("")
                self.txt_soluong.delete(0, tk.END)
                
                self.txt_giaban.config(state="normal")
                self.txt_giaban.delete(0, tk.END)
                self.txt_giaban.config(state="disabled")
                
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
        self.txt_mahoadonban.config(state="normal")
        self.txt_mahoadonban.delete(0, tk.END)
        self.txt_mahoadonban.insert(0, item[0])
        self.txt_mahoadonban.config(state="disabled")

        self.dt_ngayban.set_date(item[1])
        self.cb_manhanvien.set(item[2])
        self.cb_makhachhang.set(item[4])
        self.cb_mativi.set(item[6])

        self.txt_soluong.delete(0, tk.END)
        self.txt_soluong.insert(0, item[8])

        self.txt_giaban.config(state="normal")
        self.txt_giaban.delete(0, tk.END)
        gia_ban = float(item[9].replace(",", ""))
        self.txt_giaban.insert(0, gia_ban)
        self.txt_giaban.config(state="disabled")

        # Hiển thị MaCTHD từ dòng được chọn (lấy từ Treeview)
        ma_cthd = self.trHienThi.item(selected[0], "text")
        self.txt_macthd.delete(0, tk.END)
        self.txt_macthd.insert(0, ma_cthd)

    def SuaHoaDonChiTiet(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn để sửa!")
            return
        
        ma_hd = self.txt_mahoadonban.get()
        ma_nv = self.cb_manhanvien.get()
        ten_nv = self.dict_nv.get(ma_nv,"")
        ma_kh = self.cb_makhachhang.get()
        ten_kh = self.dict_kh.get(ma_kh, "")
        ngay_ban = self.dt_ngayban.get_date()
        ma_cthd = self.txt_macthd.get().strip()
        ma_tivi = self.cb_mativi.get()
        ten_tivi = self.dict_tivi[ma_tivi]["TenTivi"]
        so_luong_str = self.txt_soluong.get().strip()

        if(ma_cthd == ""):
            messagebox.showwarning("Cảnh báo", "Mã CTHD không được trống!")
            return
        
        if(ma_tivi == ""):
            messagebox.showwarning("Cảnh báo", "Mã tivi không được trống!")
            return
        
        if(so_luong_str == ""):
            messagebox.showwarning("Cảnh báo", "Số lượng không được trống!")
            return
        
        if not so_luong_str.isdigit():
            messagebox.showwarning("Cảnh báo", "Số lượng phải là số nguyên dương!")
            return
        
        so_luong = int(so_luong_str)
        gia_ban = float(self.txt_giaban.get().replace(",", ""))
        thanh_tien = so_luong * gia_ban

        # === KIỂM TRA TỒN KHO TRƯỚC KHI SỬA ===
        ton_kho_hien_tai = self.KiemTraTonKho(ma_tivi)
        
        if so_luong <= 0:
            messagebox.showwarning("Cảnh báo", "Số lượng bán phải lớn hơn 0!")
            return
            
        if so_luong > ton_kho_hien_tai:
            messagebox.showwarning("Cảnh báo", f"Số lượng tồn kho của {ma_tivi} chỉ còn {ton_kho_hien_tai}! Không thể sửa với số lượng này.")
            return    

        # Kiểm tra MaCTHD trùng (trừ dòng hiện tại)
        old_ma_cthd = self.trHienThi.item(selected[0], "text")
        if ma_cthd != old_ma_cthd and self.KiemTraMaCTHD(ma_cthd):
            messagebox.showwarning("Cảnh báo", f"Mã CTHD '{ma_cthd}' đã tồn tại!")
            return

        try:
            # Kiểm tra trùng mã Tivi trong cùng hóa đơn(trừ dòng hiện tai)
            for item in self.trHienThi.get_children():
                if item == selected[0]:
                    continue

                values = self.trHienThi.item(item, "values")
                if values[6] == ma_tivi:
                    traloi = messagebox.askyesno("Trùng sản phẩm", "Tivi " + ma_tivi + " dã có trong đơn này.\nBan có muốn cộng dồn số lượng không?")

                    if traloi:
                        # Cộng dồn số lượng và cập nhật thành tiền
                        soluongcu = int(values[8])
                        soluongmoi = soluongcu + so_luong
                        thanhtienmoi = soluongmoi * gia_ban

                        if soluongmoi > ton_kho_hien_tai:
                            messagebox.showwarning("Cảnh báo", f"Tổng số lượng ({soluongmoi}) vượt quá tồn kho ({ton_kho_hien_tai})! Không thể gộp.")
                            return
                    
                        self.trHienThi.item(item, values=(ma_hd, ngay_ban.strftime("%d/%m/%Y"), ma_nv, ten_nv, ma_kh, ten_kh, ma_tivi, ten_tivi, int(soluongmoi), f"{gia_ban:,.0f}", f"{thanhtienmoi:,.0f}"))
                        self.trHienThi.item(item, text=ma_cthd)

                        # Xóa dòng đang sửa(vì đã gộp vào dòng kia)
                        self.trHienThi.delete(selected[0])

                        # Cập nhật tổng tiền
                        self.TinhTongTien()
                    return
                    
            # Cập nhật lại hóa đơn trong trHienThi
            self.trHienThi.item(selected[0], values=(ma_hd, ngay_ban.strftime("%d/%m/%Y"), ma_nv, ten_nv, ma_kh, ten_kh, ma_tivi, ten_tivi, int(so_luong), f"{gia_ban:,.0f}", f"{thanh_tien:,.0f}"))
            self.trHienThi.item(selected[0], text=ma_cthd)

            # Xóa dữ liệu chi tiết hóa đơn sau khi thêm
            self.txt_macthd.delete(0, tk.END)
            self.cb_mativi.set("")
            self.txt_soluong.delete(0, tk.END)

            self.txt_giaban.config(state="normal")
            self.txt_giaban.delete(0, tk.END)
            self.txt_giaban.config(state="disabled")
                    
            self.TinhTongTien()

        except Exception as e:
            messagebox.showerror("Lỗi", "Đã xảy ra lỗi:" + str(e))
    
    def XoaHoaDonChiTiet(self):
        selected = self.trHienThi.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn để xóa!")
            return
        
        traloi = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa hóa đơn này không?")
        if traloi:
            self.trHienThi.delete(selected[0])

            # Cập nhật lại tổng tiền
            self.TinhTongTien()

            # Xóa input chi tiết
            self.txt_macthd.delete(0, tk.END)
            self.cb_mativi.set("")
            self.txt_soluong.delete(0, tk.END)
            self.txt_giaban.config(state="normal")
            self.txt_giaban.delete(0, tk.END)
            self.txt_giaban.config(state="disabled")

    def LamMoi(self):
        self.txt_mahoadonban.config(state="normal")
        self.dt_ngayban.config(state="normal")
        self.cb_manhanvien.config(state="readonly")
        self.cb_makhachhang.config(state="readonly")

        self.txt_mahoadonban.delete(0, tk.END)
        self.dt_ngayban.set_date(datetime.today())
        if self.user == "admin":
            self.cb_manhanvien.set("")
        self.cb_makhachhang.set("")

        self.txt_macthd.delete(0, tk.END)
        self.cb_mativi.set("")
        self.txt_soluong.delete(0, tk.END)
        self.txt_soluong.insert(0, "")

        self.txt_soluong.config(state="normal")
        self.txt_giaban.delete(0, tk.END)
        self.txt_giaban.insert(0, "")
        self.txt_giaban.config(state="disabled")

        self.trHienThi.delete(*self.trHienThi.get_children())
        self.lbl_tongtien.config(text="0 VNĐ")

    def TaoHoaDon(self):
        if not self.trHienThi.get_children():
            messagebox.showwarning("Cảnh báo", "Không có hóa đơn nào để thực hiện tạo hóa đơn")
            return
        
        try:
            cursor = self.conn.cursor()
            ma_hd = self.txt_mahoadonban.get()
            ngay_ban = self.dt_ngayban.get_date().strftime("%Y-%m-%d")
            ma_nv = self.cb_manhanvien.get()
            ma_kh = self.cb_makhachhang.get()

            # Thêm hóa đơn - vì 1 hóa đơn sẽ có nhiều chi tiết hóa đơn
            cursor.execute("""
                INSERT INTO HOADONBAN (MaHD, NgayBan, MaNV, MaKH)
                VALUES (?, ?, ?, ?)
                """, (ma_hd, ngay_ban, ma_nv, ma_kh))
            
            for item in self.trHienThi.get_children():
                values = self.trHienThi.item(item, "values")
                ma_cthd = self.trHienThi.item(item, "text")
                ma_tivi = values[6]
                so_luong = int(values[8])
                gia_ban = float(values[9].replace(",", ""))
                
                # Thêm chi tiết hóa đơn
                cursor.execute("""
                    INSERT INTO CHITIETHOADON (MaCTHD, MaHD, MaTivi, SoLuong, DonGia)
                    VALUES(?, ?, ?, ?, ?)
                    """, (ma_cthd, ma_hd, ma_tivi, so_luong, gia_ban))
                
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("Thành công", "Tạo hóa đơn thành công!")
            self.LamMoi()

            if self.tab_hoadon:
                self.tab_hoadon.load_hoa_don()

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi tạo đơn hàng:\n" + str(e))\
            

    def KiemTraTonKho(self, ma_tivi):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT SoLuongTon FROM TIVI WHERE MaTivi = ?", (ma_tivi,))
            ton_kho = cursor.fetchone()
            cursor.close()
            return ton_kho[0] if ton_kho else 0
        except Exception as e:
            print(f"Lỗi truy vấn tồn kho: {e}")
            return 0