--- TẠO DATABASE QLTV ---
CREATE DATABASE QLTV
ON ( 
	NAME = 'QLTV', 
	FILENAME = 'D:\QLTV_data.mdf', 
	SIZE = 8MB, 
	MAXSIZE = 80MB, 
	FILEGROWTH = 5MB 
)
LOG ON ( 
	NAME = 'QLTV_log', 
	FILENAME = 'D:\QLTV_log.ldf', 
	SIZE = 8MB, 
	MAXSIZE = 80MB, 
	FILEGROWTH = 5MB 
);
GO
USE QLTV;
GO

--- TẠO CÁC TABLE ---
CREATE TABLE HangSanXuat (
    MaHang NVARCHAR(10) PRIMARY KEY,
    TenHang NVARCHAR(100) NOT NULL,
    QuocGia NVARCHAR(50),
    CONSTRAINT UQ_HangSanXuat_TenHang UNIQUE (TenHang)
);
GO

CREATE TABLE KhachHang (
    MaKH NVARCHAR(10) PRIMARY KEY,
    TenKH NVARCHAR(100) NOT NULL,
    SoDienThoai NVARCHAR(10) UNIQUE,
    DiaChi NVARCHAR(255),
    Email NVARCHAR(100) UNIQUE
);
GO

CREATE TABLE NhanVien (
    MaNV NVARCHAR(10) PRIMARY KEY,
    HinhAnh VARBINARY(MAX),
    TenNV NVARCHAR(100) NOT NULL,
    GioiTinh NVARCHAR(10) CHECK (GioiTinh IN (N'Nam', N'Nữ')),
    NgaySinh DATE,
    SoDienThoai NVARCHAR(10) UNIQUE,
    CCCD NVARCHAR(12) UNIQUE
);
GO

CREATE TABLE NhaCungCap (
    MaNCC NVARCHAR(10) PRIMARY KEY,
    TenNCC NVARCHAR(100) UNIQUE,
    DiaChi NVARCHAR(255),
    SoDienThoai NVARCHAR(10) UNIQUE,
    Email NVARCHAR(100) UNIQUE
);
GO

CREATE TABLE TaiKhoan (
    TenDangNhap NVARCHAR(10) PRIMARY KEY,
    MatKhau NVARCHAR(100) DEFAULT 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
);
GO

CREATE TABLE Tivi (
    MaTivi NVARCHAR(10) PRIMARY KEY,
    HinhAnh VARBINARY(MAX),
    TenTivi NVARCHAR(100) NOT NULL,
    MaHang NVARCHAR(10) NOT NULL,
    KichThuoc NVARCHAR(20),
    DoPhanGiai NVARCHAR(20),
    GiaBan DECIMAL(18,2) NOT NULL DEFAULT 0,
    SoLuongTon INT DEFAULT 0,
    NamSanXuat INT,
    MoTa NVARCHAR(255),
    CONSTRAINT FK_Tivi_Hang FOREIGN KEY (MaHang) REFERENCES HangSanXuat (MaHang)
);
GO

CREATE TABLE PhieuNhapHang (
    MaPhieuNhap NVARCHAR(10) PRIMARY KEY,
    NgayNhap DATE DEFAULT GETDATE(),
    MaNV NVARCHAR(10) NOT NULL,
    MaNCC NVARCHAR(10) NOT NULL,
    TrangThai NVARCHAR(20) DEFAULT N'Đợi duyệt',
    TongTien DECIMAL(18,2) DEFAULT 0,
    CONSTRAINT FK_PhieuNhap_NhanVien FOREIGN KEY (MaNV) REFERENCES NhanVien (MaNV),
    CONSTRAINT FK_PhieuNhap_NCC FOREIGN KEY (MaNCC) REFERENCES NhaCungCap (MaNCC)
);
GO

CREATE TABLE ChiTietPhieuNhap (
    MaPhieuNhap NVARCHAR(10) NOT NULL,
    MaTivi NVARCHAR(10) NOT NULL,
    SoLuong INT CHECK (SoLuong > 0),
    GiaNhap DECIMAL(18,2) CHECK (GiaNhap >= 0),
    ThanhTien AS (SoLuong * GiaNhap) PERSISTED,
    PRIMARY KEY (MaPhieuNhap, MaTivi),
    CONSTRAINT FK_CTPN_PhieuNhap FOREIGN KEY (MaPhieuNhap) REFERENCES PhieuNhapHang (MaPhieuNhap),
    CONSTRAINT FK_CTPN_Tivi FOREIGN KEY (MaTivi) REFERENCES Tivi (MaTivi)
);
GO

CREATE TABLE HoaDonBan (
    MaHD NVARCHAR(10) PRIMARY KEY,
    NgayBan DATE DEFAULT GETDATE(),
    MaNV NVARCHAR(10) NOT NULL,
    MaKH NVARCHAR(10) NULL,
    TongTien DECIMAL(18,2) DEFAULT 0,
    TrangThai NVARCHAR(20) DEFAULT N'Chờ thanh toán',
    CONSTRAINT FK_HoaDon_NhanVien FOREIGN KEY (MaNV) REFERENCES NhanVien (MaNV),
    CONSTRAINT FK_HoaDon_KhachHang FOREIGN KEY (MaKH) REFERENCES KhachHang (MaKH)
);
GO

CREATE TABLE ChiTietHoaDon (
    MaCTHD NVARCHAR(10) PRIMARY KEY,
    MaHD NVARCHAR(10) NOT NULL,
    MaTivi NVARCHAR(10) NOT NULL,
    SoLuong INT CHECK (SoLuong > 0),
    DonGia DECIMAL(18,2) CHECK (DonGia >= 0),
    ThanhTien AS (SoLuong * DonGia) PERSISTED,
    CONSTRAINT FK_CTHD_HoaDon FOREIGN KEY (MaHD) REFERENCES HoaDonBan (MaHD),
    CONSTRAINT FK_CTHD_Tivi FOREIGN KEY (MaTivi) REFERENCES Tivi (MaTivi),
    CONSTRAINT UQ_CTHD_MaHD_MaTivi UNIQUE (MaHD, MaTivi)
);
GO

CREATE TABLE BaoHanh (
    MaBH NVARCHAR(10) PRIMARY KEY,
    MaCTHD NVARCHAR(10) NOT NULL,
    ThoiGianBaoHanh INT CHECK (ThoiGianBaoHanh > 0),
    DieuKien NVARCHAR(255),
    NgayBaoHanh DATE NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_BaoHanh_ChiTietHoaDon FOREIGN KEY (MaCTHD) REFERENCES ChiTietHoaDon (MaCTHD)
);
GO

--- TẠO TRIGGER CẬP NHẬT TỔNG TIỀN CHO PHIẾU NHÂP HÀNG ---
CREATE TRIGGER trg_CapNhatTongTien_PhieuNhap 
ON ChiTietPhieuNhap AFTER INSERT, UPDATE, DELETE
AS BEGIN
    SET NOCOUNT ON;
    UPDATE p SET TongTien = ISNULL((
        SELECT SUM(ThanhTien) FROM ChiTietPhieuNhap c 
        WHERE c.MaPhieuNhap = p.MaPhieuNhap
    ), 0)
    FROM PhieuNhapHang p
    WHERE p.MaPhieuNhap IN (SELECT MaPhieuNhap FROM inserted UNION SELECT MaPhieuNhap FROM deleted);
END;
GO

--- TẠO TRIGGER CẬP NHẬT TỔNG TIỀN CHO HÓA ĐƠN ---
CREATE TRIGGER trg_CapNhatTongTien_HoaDon 
ON ChiTietHoaDon AFTER INSERT, UPDATE, DELETE
AS BEGIN
    SET NOCOUNT ON;
    UPDATE p SET TongTien = ISNULL((
        SELECT SUM(ThanhTien) FROM ChiTietHoaDon c 
        WHERE c.MaHD = p.MaHD
    ), 0)
    FROM HoaDonBan p
    WHERE p.MaHD IN (SELECT MaHD FROM inserted UNION SELECT MaHD FROM deleted);
END;
GO

--- INSERT DỮ LIỆU ---
INSERT INTO HangSanXuat (MaHang, TenHang, QuocGia) VALUES 
('H01', N'Samsung', N'Hàn Quốc'),('H02', N'LG', N'Hàn Quốc'),('H03', N'Sony', N'Nhật Bản'),
('H04', N'TCL', N'Trung Quốc'),('H05', N'Panasonic', N'Nhật Bản'),('H06', N'Toshiba', N'Nhật Bản'),
('H07', N'Xiaomi', N'Trung Quốc'),('H08', N'Philips', N'Hà Lan'),('H09', N'Sharp', N'Nhật Bản'),
('H10', N'Hisense', N'Trung Quốc'),('H11', N'Vizio', N'Mỹ'),('H12', N'Skyworth', N'Trung Quốc'),
('H13', N'Sanyo', N'Nhật Bản'),('H14', N'Hitachi', N'Nhật Bản'),('H15', N'Acer', N'Đài Loan'),
('H16', N'Lenovo', N'Trung Quốc'),('H17', N'Haier', N'Trung Quốc'),('H18', N'Asanzo', N'Việt Nam'),
('H19', N'Coocaa', N'Trung Quốc'),('H20', N'Polytron', N'Indonesia');
GO

INSERT INTO Tivi (MaTivi, TenTivi, MaHang, KichThuoc, DoPhanGiai, GiaBan, SoLuongTon, NamSanXuat, MoTa) VALUES
('TV01', N'Samsung QLED 55Q70A', 'H01', '55 inch', '4K', 25000000, 50, 2023, N'Tivi thông minh QLED'),
('TV02', N'LG OLED C1 65', 'H02', '65 inch', '4K', 45000000, 30, 2022, N'Tivi OLED cao cấp'),
('TV03', N'Sony Bravia X90J', 'H03', '55 inch', '4K', 30000000, 40, 2023, N'Tivi LED Full Array'),
('TV04', N'TCL 43S6500', 'H04', '43 inch', 'Full HD', 9000000, 60, 2021, N'Tivi Android giá rẻ'),
('TV05', N'Panasonic TH-50MX700', 'H05', '50 inch', '4K', 15000000, 45, 2023, N'Tivi LED tiết kiệm điện'),
('TV06', N'Toshiba 32V35KP', 'H06', '32 inch', 'HD', 5000000, 70, 2022, N'Tivi cơ bản'),
('TV07', N'Xiaomi Mi TV P1 55', 'H07', '55 inch', '4K', 12000000, 55, 2023, N'Tivi thông minh giá rẻ'),
('TV08', N'Philips 50PUS8505', 'H08', '50 inch', '4K', 18000000, 35, 2022, N'Tivi Ambilight'),
('TV09', N'Sharp 42CJ2X', 'H09', '42 inch', 'Full HD', 8500000, 50, 2021, N'Tivi LED cơ bản'),
('TV10', N'Hisense 65A6G', 'H10', '65 inch', '4K', 20000000, 25, 2023, N'Tivi ULED cao cấp'),
('TV11', N'Vizio M-Series 50', 'H11', '50 inch', '4K', 17000000, 30, 2022, N'Tivi Quantum Dot'),
('TV12', N'Skyworth 55SUC9300', 'H12', '55 inch', '4K', 14000000, 40, 2023, N'Tivi Android thông minh'),
('TV13', N'Sanyo 43FWN668', 'H13', '43 inch', 'Full HD', 8000000, 60, 2021, N'Tivi giá rẻ'),
('TV14', N'Hitachi 55HAL7350', 'H14', '55 inch', '4K', 16000000, 35, 2022, N'Tivi thông minh'),
('TV15', N'Acer 50ATV1', 'H15', '50 inch', '4K', 13000000, 45, 2023, N'Tivi LED thông minh'),
('TV16', N'Lenovo 43LTV2', 'H16', '43 inch', 'Full HD', 9500000, 50, 2022, N'Tivi cơ bản'),
('TV17', N'Haier 55H66', 'H17', '55 inch', '4K', 14500000, 40, 2023, N'Tivi thông minh'),
('TV18', N'Asanzo 32S606', 'H18', '32 inch', 'HD', 4500000, 80, 2021, N'Tivi giá rẻ Việt Nam'),
('TV19', N'Coocaa 50S7G', 'H19', '50 inch', '4K', 11000000, 55, 2023, N'Tivi Android giá rẻ'),
('TV20', N'Polytron 43PLD900', 'H20', '43 inch', 'Full HD', 9000000, 60, 2022, N'Tivi LED cơ bản');
GO

INSERT INTO KhachHang (MaKH, TenKH, SoDienThoai, DiaChi, Email) VALUES
('KH01', N'Nguyễn Văn An', '0912345671', N'123 Lê Lợi, Hà Nội', 'an.nguyen1@gmail.com'),
('KH02', N'Trần Thị Bình', '0912345672', N'45 Nguyễn Huệ, TP.HCM', 'binh.tran2@gmail.com'),
('KH03', N'Phạm Minh Châu', '0912345673', N'67 Trần Phú, Đà Nẵng', 'chau.pham3@gmail.com'),
('KH04', N'Lê Văn Đức', '0912345674', N'89 Hùng Vương, Huế', 'duc.le4@gmail.com'),
('KH05', N'Hoàng Thị E', '0912345675', N'12 Lý Thường Kiệt, Hà Nội', 'e.hoang5@gmail.com'),
('KH06', N'Vũ Văn Hùng', '0912345676', N'34 Nguyễn Trãi, TP.HCM', 'hung.vu6@gmail.com'),
('KH07', N'Đặng Thị Hồng', '0912345677', N'56 Phạm Văn Đồng, Đà Nẵng', 'hong.dang7@gmail.com'),
('KH08', N'Bùi Văn Khải', '0912345678', N'78 Nguyễn Văn Cừ, Hà Nội', 'khai.bui8@gmail.com'),
('KH09', N'Ngô Thị Lan', '0912345679', N'90 Lê Đại Hành, TP.HCM', 'lan.ngo9@gmail.com'),
('KH10', N'Tô Minh Nam', '0912345680', N'112 Hai Bà Trưng, Huế', 'nam.to10@gmail.com'),
('KH11', N'Đỗ Thị Oanh', '0912345681', N'134 Nguyễn Thị Minh Khai, TP.HCM', 'oanh.do11@gmail.com'),
('KH12', N'Phan Văn Phú', '0912345682', N'156 Lê Văn Sỹ, Đà Nẵng', 'phu.phan12@gmail.com'),
('KH13', N'Mai Thị Quyên', '0912345683', N'178 Trần Hưng Đạo, Hà Nội', 'quyen.mai13@gmail.com'),
('KH14', N'Nguyễn Văn Sơn', '0912345684', N'190 Lý Tự Trọng, TP.HCM', 'son.nguyen14@gmail.com'),
('KH15', N'Trần Thị Thanh', '0912345685', N'212 Nguyễn Đình Chiểu, Huế', 'thanh.tran15@gmail.com'),
('KH16', N'Phạm Văn Tín', '0912345686', N'234 Hùng Vương, Đà Nẵng', 'tin.pham16@gmail.com'),
('KH17', N'Lê Thị Uyên', '0912345687', N'256 Lê Lợi, Hà Nội', 'uyen.le17@gmail.com'),
('KH18', N'Hoàng Văn Vương', '0912345688', N'278 Nguyễn Huệ, TP.HCM', 'vuong.hoang18@gmail.com'),
('KH19', N'Đặng Thị Xuân', '0912345689', N'300 Trần Phú, Đà Nẵng', 'xuan.dang19@gmail.com'),
('KH20', N'Bùi Văn Ý', '0912345690', N'322 Hùng Vương, Huế', 'y.bui20@gmail.com');
GO

INSERT INTO NhanVien (MaNV, TenNV, GioiTinh, NgaySinh, SoDienThoai, CCCD) VALUES
('NV01', N'Nguyễn Văn Bình', N'Nam', '1990-01-15', '0987654321', '023456789001'),
('NV02', N'Trần Thị Cúc', N'Nữ', '1992-03-20', '0987654322', '023456789002'),
('NV03', N'Phạm Văn Dũng', N'Nam', '1988-05-10', '0987654323', '023456789003'),
('NV04', N'Lê Thị Hoa', N'Nữ', '1995-07-25', '0987654324', '023456789004'),
('NV05', N'Hoàng Văn Kiên', N'Nam', '1993-09-12', '0987654325', '023456789005'),
('NV06', N'Vũ Thị Lan', N'Nữ', '1991-11-30', '0987654326', '023456789006'),
('NV07', N'Đặng Văn Minh', N'Nam', '1989-02-14', '0987654327', '023456789007'),
('NV08', N'Bùi Thị Nga', N'Nữ', '1994-04-18', '0987654328', '023456789008'),
('NV09', N'Ngô Văn Phát', N'Nam', '1990-06-22', '0987654329', '023456789009'),
('NV10', N'Tô Thị Quyên', N'Nữ', '1992-08-05', '0987654330', '023456789010'),
('NV11', N'Đỗ Văn Sơn', N'Nam', '1993-10-10', '0987654331', '023456789011'),
('NV12', N'Phan Thị Thanh', N'Nữ', '1995-12-15', '0987654332', '023456789012'),
('NV13', N'Mai Văn Thắng', N'Nam', '1987-01-20', '0987654333', '023456789013'),
('NV14', N'Nguyễn Thị Uyên', N'Nữ', '1991-03-25', '0987654334', '023456789014'),
('NV15', N'Trần Văn Vinh', N'Nam', '1989-05-30', '0987654335', '023456789015'),
('NV16', N'Phạm Thị Xuân', N'Nữ', '1994-07-05', '0987654336', '023456789016'),
('NV17', N'Lê Văn Ý', N'Nam', '1990-09-10', '0987654337', '023456789017'),
('NV18', N'Hoàng Thị Z', N'Nữ', '1992-11-15', '0987654338', '023456789018'),
('NV19', N'Đặng Văn An', N'Nam', '1988-02-20', '0987654339', '023456789019'),
('NV20', N'Bùi Thị Bình', N'Nữ', '1993-04-25', '0987654340', '023456789020');
GO

INSERT INTO NhaCungCap (MaNCC, TenNCC, DiaChi, SoDienThoai, Email) VALUES
('NCC01', N'Công ty TNHH Điện Máy Samsung Việt Nam', N'Khu công nghiệp Yên Phong, Bắc Ninh', '0909123456', 'contact@samsungvn.com'),
('NCC02', N'Công ty Cổ phần LG Việt Nam', N'Khu công nghệ cao TP. Hồ Chí Minh', '0909988776', 'info@lgvn.com'),
('NCC03', N'Công ty TNHH Sony Electronics Việt Nam', N'Quận 9, TP. Hồ Chí Minh', '0912345678', 'info@sonyvn.com'),
('NCC04', N'Công ty Panasonic Việt Nam', N'Hà Đông, Hà Nội', '0909123123', 'contact@panasonic.vn'),
('NCC05', N'Công ty Sharp Việt Nam', N'Khu công nghiệp VSIP, Bình Dương', '0987654321', 'info@sharpvn.com'),
('NCC06', N'Công ty Toshiba Việt Nam', N'Tân Bình, TP. Hồ Chí Minh', '0911222333', 'support@toshiba.vn'),
('NCC07', N'Công ty TCL Việt Nam', N'Khu công nghiệp Nhơn Trạch, Đồng Nai', '0909888777', 'info@tclvn.com'),
('NCC08', N'Công ty Casper Việt Nam', N'Cầu Giấy, Hà Nội', '0911999888', 'support@casper.vn'),
('NCC09', N'Công ty Asanzo Việt Nam', N'Bình Tân, TP. Hồ Chí Minh', '0933222111', 'info@asanzo.vn'),
('NCC10', N'Công ty Điện Máy VTB', N'Thủ Dầu Một, Bình Dương', '0909345678', 'sales@vtb.vn'),
('NCC11', N'Công ty Skyworth Việt Nam', N'Đà Nẵng', '0911777888', 'info@skyworth.vn'),
('NCC12', N'Công ty Cổ phần Điện Máy Aqua Việt Nam', N'Hải Phòng', '0911002200', 'contact@aqua.vn'),
('NCC13', N'Công ty Philips Việt Nam', N'Nam Từ Liêm, Hà Nội', '0909222333', 'support@philips.vn'),
('NCC14', N'Công ty Hitachi Việt Nam', N'Quận 7, TP. Hồ Chí Minh', '0933555777', 'info@hitachi.vn'),
('NCC15', N'Công ty Beko Việt Nam', N'Tân Uyên, Bình Dương', '0911888999', 'sales@beko.vn'),
('NCC16', N'Công ty Xiaomi Việt Nam', N'Cầu Giấy, Hà Nội', '0909000111', 'contact@xiaomi.vn'),
('NCC17', N'Công ty Realme Việt Nam', N'TP. Thủ Đức, TP. Hồ Chí Minh', '0911444555', 'info@realme.vn'),
('NCC18', N'Công ty Điện Máy Midea Việt Nam', N'Hưng Yên', '0909777666', 'support@midea.vn'),
('NCC19', N'Công ty Cổ phần Kangaroo Việt Nam', N'Long Biên, Hà Nội', '0911555666', 'contact@kangaroo.vn'),
('NCC20', N'Công ty Điện Máy Sanaky Việt Nam', N'Tân Bình, TP. Hồ Chí Minh', '0909111222', 'info@sanaky.vn');
GO

INSERT INTO TaiKhoan (TenDangNhap, MatKhau) VALUES 
('admin', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3');
GO

INSERT INTO TaiKhoan (TenDangNhap) VALUES 
('NV01'),
('NV02'),
('NV03'),
('NV04'),
('NV05'),
('NV06'),
('NV07'),
('NV08'),
('NV09'),
('NV10'),
('NV11'),
('NV12'),
('NV13'),
('NV14'),
('NV15'),
('NV16'),
('NV17'),
('NV18'),
('NV19'),
('NV20');
GO

INSERT INTO PhieuNhapHang (MaPhieuNhap, NgayNhap, MaNV, MaNCC, TrangThai) VALUES
('PN001', '2023-06-10', 'NV01', 'NCC01', N'Đã duyệt'),
('PN002', '2023-07-15', 'NV02', 'NCC02', N'Đã duyệt'),
('PN003', '2023-08-20', 'NV03', 'NCC03', N'Đợi duyệt'),
('PN004', '2023-09-25', 'NV04', 'NCC04', N'Đã duyệt'),
('PN005', '2023-10-30', 'NV05', 'NCC05', N'Đã duyệt');
GO

INSERT INTO ChiTietPhieuNhap (MaPhieuNhap, MaTivi, SoLuong, GiaNhap) VALUES
('PN001', 'TV01', 10, 17500000),('PN001', 'TV07', 15, 8400000),('PN001', 'TV19', 12, 7700000),
('PN002', 'TV02', 8, 31500000),('PN002', 'TV05', 10, 10500000),('PN002', 'TV17', 7, 10150000),
('PN003', 'TV03', 6, 21000000),('PN003', 'TV11', 9, 11900000),('PN003', 'TV14', 5, 11200000),
('PN004', 'TV04', 20, 6300000),('PN004', 'TV06', 25, 3500000),('PN004', 'TV18', 30, 3150000),
('PN005', 'TV09', 18, 5950000),('PN005', 'TV10', 5, 14000000),('PN005', 'TV12', 10, 9800000),
('PN005', 'TV15', 12, 9100000),('PN005', 'TV20', 15, 6300000);
GO

INSERT INTO HoaDonBan (MaHD, NgayBan, MaNV, MaKH, TrangThai) VALUES
('HD001', '2023-06-15', 'NV01', 'KH01', N'Đã thanh toán'),
('HD002', '2023-06-18', 'NV02', 'KH02', N'Đã thanh toán'),
('HD003', '2023-07-01', 'NV03', 'KH03', N'Chờ thanh toán'),
('HD004', '2023-07-05', 'NV04', 'KH04', N'Đã thanh toán'),
('HD005', '2023-07-10', 'NV05', 'KH05', N'Đã Hủy'),
('HD006', '2023-08-12', 'NV06', 'KH06', N'Đã thanh toán'),
('HD007', '2023-08-20', 'NV07', 'KH07', N'Chờ thanh toán'),
('HD008', '2023-09-03', 'NV08', 'KH08', N'Đã thanh toán'),
('HD009', '2023-09-15', 'NV09', 'KH09', N'Đã thanh toán'),
('HD010', '2023-10-01', 'NV10', 'KH10', N'Chờ thanh toán'),
('HD011', '2023-10-18', 'NV11', 'KH11', N'Đã thanh toán'),
('HD012', '2023-11-05', 'NV12', 'KH12', N'Đã Hủy'),
('HD013', '2023-11-20', 'NV13', 'KH13', N'Đã thanh toán'),
('HD014', '2023-12-01', 'NV14', 'KH14', N'Chờ thanh toán'),
('HD015', '2023-12-15', 'NV15', 'KH15', N'Đã thanh toán'),
('HD016', '2024-01-10', 'NV16', 'KH16', N'Đã thanh toán'),
('HD017', '2024-02-05', 'NV17', 'KH17', N'Chờ thanh toán'),
('HD018', '2024-03-12', 'NV18', 'KH18', N'Đã thanh toán'),
('HD019', '2024-04-01', 'NV19', 'KH19', N'Đã Hủy'),
('HD020', '2024-05-20', 'NV20', 'KH20', N'Đã thanh toán');
GO

INSERT INTO ChiTietHoaDon (MaCTHD, MaHD, MaTivi, SoLuong, DonGia) VALUES
('CT001', 'HD001', 'TV01', 1, 25000000),('CT002', 'HD001', 'TV07', 1, 12000000),
('CT003', 'HD002', 'TV02', 1, 45000000),('CT004', 'HD003', 'TV03', 2, 30000000),
('CT005', 'HD004', 'TV04', 3, 9000000),('CT006', 'HD004', 'TV06', 1, 5000000),
('CT007', 'HD005', 'TV05', 1, 15000000),('CT008', 'HD006', 'TV08', 1, 18000000),
('CT009', 'HD006', 'TV12', 1, 14000000),('CT010', 'HD007', 'TV10', 1, 20000000),
('CT011', 'HD008', 'TV11', 2, 17000000),('CT012', 'HD009', 'TV15', 1, 13000000),
('CT013', 'HD009', 'TV19', 1, 11000000),('CT014', 'HD010', 'TV01', 1, 25000000),
('CT015', 'HD011', 'TV02', 1, 45000000),('CT016', 'HD011', 'TV03', 1, 30000000),
('CT017', 'HD012', 'TV04', 2, 9000000),('CT018', 'HD013', 'TV07', 3, 12000000),
('CT019', 'HD014', 'TV09', 1, 8500000),('CT020', 'HD014', 'TV13', 2, 8000000),
('CT021', 'HD015', 'TV17', 1, 14500000),('CT022', 'HD016', 'TV18', 5, 4500000),
('CT023', 'HD017', 'TV06', 2, 5000000),('CT024', 'HD017', 'TV04', 1, 9000000),
('CT025', 'HD018', 'TV20', 1, 9000000),('CT026', 'HD018', 'TV16', 1, 9500000),
('CT027', 'HD019', 'TV14', 1, 16000000),('CT028', 'HD020', 'TV01', 1, 25000000),
('CT029', 'HD020', 'TV07', 2, 12000000),('CT030', 'HD020', 'TV19', 1, 11000000);
GO

INSERT INTO BaoHanh (MaBH, MaCTHD, ThoiGianBaoHanh, DieuKien, NgayBaoHanh) VALUES
('BH01', 'CT001', 24, N'Bảo hành chính hãng Samsung 24 tháng', '2023-06-15'),
('BH02', 'CT002', 24, N'Bảo hành Xiaomi 24 tháng', '2023-06-15'),
('BH03', 'CT003', 36, N'Bảo hành OLED LG 36 tháng', '2023-06-18'),
('BH04', 'CT005', 12, N'Bảo hành TCL 12 tháng', '2023-07-05'),
('BH05', 'CT006', 12, N'Bảo hành Toshiba 12 tháng', '2023-07-05'),
('BH06', 'CT008', 24, N'Bảo hành Ambilight Philips', '2023-08-12'),
('BH07', 'CT009', 24, N'Bảo hành Skyworth Android', '2023-08-12'),
('BH08', 'CT011', 24, N'Bảo hành Vizio Quantum Dot', '2023-09-03'),
('BH09', 'CT012', 24, N'Bảo hành Acer 24 tháng', '2023-09-15'),
('BH10', 'CT013', 24, N'Bảo hành Coocaa Android', '2023-09-15'),
('BH11', 'CT015', 36, N'Bảo hành OLED LG (lần 2)', '2023-10-18'),
('BH12', 'CT016', 24, N'Bảo hành Sony 24 tháng', '2023-10-18'),
('BH13', 'CT018', 24, N'Bảo hành Xiaomi (lần 2)', '2023-11-20'),
('BH14', 'CT021', 24, N'Bảo hành Haier 24 tháng', '2023-12-15'),
('BH15', 'CT022', 12, N'Bảo hành Asanzo 12 tháng', '2024-01-10'),
('BH16', 'CT025', 12, N'Bảo hành Polytron 12 tháng', '2024-03-12'),
('BH17', 'CT026', 12, N'Bảo hành Lenovo 12 tháng', '2024-03-12'),
('BH18', 'CT028', 24, N'Bảo hành Samsung (lần 2)', '2024-05-20'),
('BH19', 'CT029', 24, N'Bảo hành Xiaomi (lần 3)', '2024-05-20'),
('BH20', 'CT030', 24, N'Bảo hành Coocaa (lần 2)', '2024-05-20');
GO

--- XEM CÁC BẢNG ---
SELECT * FROM HangSanXuat;
SELECT * FROM Tivi;
SELECT * FROM KhachHang;
SELECT * FROM NhanVien;
SELECT * FROM HoaDonBan;
SELECT * FROM ChiTietHoaDon;
SELECT * FROM BaoHanh;
SELECT * FROM TaiKhoan;
SELECT * FROM ChiTietPhieuNhap;
SELECT * FROM NhaCungCap
SELECT * FROM PhieuNhapHang
SELECT * FROM BaoHanh