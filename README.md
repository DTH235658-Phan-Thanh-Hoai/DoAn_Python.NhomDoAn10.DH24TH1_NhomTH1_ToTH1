
---

## Giới thiệu

> *"Chào mừng bạn đến với **màn hình đăng nhập** của **Hệ thống Quản lý Nhân sự**!  
> Đây là cửa ngõ đầu tiên để truy cập vào hệ thống.  
> Giao diện được thiết kế **đẹp mắt**, **dễ dùng**, **chuyên nghiệp**, chạy mượt trên **Windows** với **Python** và **Tkinter**."*

---

## Tính năng nổi bật

### 1. **Giao diện hiện đại, bắt mắt**
> *"Bên trái là hình nền đẹp kích thước 300x580, bên phải là form đăng nhập trắng tinh tế.  
> Màu xanh dương chủ đạo, avatar tròn 120x120, chữ SIGNIN in đậm – nhìn là muốn đăng nhập ngay!"*

### 2. **Tự động căn giữa màn hình**
> *"Dù bạn dùng màn hình 15 inch hay 27 inch, cửa sổ luôn **căn chính giữa** – chuẩn UX!"*

### 3. **Hình ảnh sắc nét trên mọi màn hình**
> *"Hỗ trợ **DPI Scaling** – không bị mờ trên laptop 4K, Retina hay màn hình độ phân giải cao!"*

### 4. **Kết nối SQL Server an toàn**
> *"Dùng **Windows Authentication** – không cần nhập tài khoản SQL.  
> Kết nối trực tiếp đến máy cá nhân, database **QLTV**."*

### 5. **Đăng nhập nhanh bằng phím Enter**
> *"Gõ xong tên đăng nhập → nhấn **Enter**.  
> Gõ mật khẩu → nhấn **Enter** → **Đăng nhập ngay** – không cần click chuột!"*

### 6. **Ẩn / Hiện mật khẩu bằng nút con mắt**
> *"Click vào biểu tượng 👁 để **hiện mật khẩu**, click lại thành 🚫 để **ẩn**.  
> Rất tiện khi bạn gõ sai!"*

### 7. **Thông báo lỗi rõ ràng, thân thiện**
> *"Thiếu tên đăng nhập? → 'Vui lòng nhập...'  
> Sai tài khoản? → 'Sai tài khoản hoặc mật khẩu!'  
> Hiển thị **màu đỏ**, ngay dưới form – không thể bỏ sót!"*

### 8. **Nút Đăng nhập & Thoát chuyên nghiệp**
> *"Nút **Đăng nhập** màu xanh dương, hover sáng lên.  
> Nút **Thoát** màu đỏ, click là thoát chương trình ngay lập tức."*

### 9. **Chuyển sang form chính khi đăng nhập thành công**
> *"Đăng nhập đúng → cửa sổ tự đóng → mở ngay **App chính** với tham số người dùng!"*

---

## Cấu trúc thư mục cần có


# QUẢN LÝ HỆ THỐNG – README

## 1. TRANG BẢNG ĐIỀU KHIỂN TỔNG QUAN

### 1.1. Phân quyền truy cập
| Người dùng            | Quyền hạn                                      |
|-----------------------|------------------------------------------------|
| **admin**             | **Toàn quyền**: Xem toàn bộ thẻ, biểu đồ, điều hướng năm |
| **nhân viên bán hàng**| **Không truy cập được**                        |
| **nhân viên kho**     | **Không truy cập được**                        |

> **Chỉ admin** được vào trang `Tổng Quan`.

### 1.2. Tiêu đề trang
- **Text**: `TRANG TỔNG QUAN HỆ THỐNG`
- **Font**: Segoe UI, **16**, **bold**
- **Màu**: `#003366`
- **Căn giữa** trên cùng

### 1.3. Bố cục tổng thể
| Phần trên (30%) | Phần dưới (70%)                          |
|------------------|------------------------------------------|
| **6 thẻ thống kê** | **Biểu đồ doanh thu + Điều khiển năm** |

### 1.4. Các thẻ thống kê (3x2)
| Thẻ                | Icon     | Truy vấn                              | Ý nghĩa                     |
|--------------------|----------|---------------------------------------|-----------------------------|
| **Tổng nhân viên** | Person   | `COUNT(*) FROM NhanVien`              | Số NV đang làm              |
| **Tổng khách hàng**| People   | `COUNT(*) FROM KhachHang`             | Tổng KH trong hệ thống      |
| **Hãng sản xuất**  | Factory  | `COUNT(*) FROM HangSanXuat`           | Số thương hiệu              |
| **Nhà cung cấp**   | Building | `COUNT(*) FROM NhaCungCap`            | Số đối tác                  |
| **Sản phẩm**       | TV       | `COUNT(*) FROM Tivi`                  | Tổng TV trong kho           |
| **Phiếu nhập hàng**| Box      | `COUNT(*) FROM PhieuNhapHang`         | Tổng lần nhập               |

**Thiết kế thẻ**:
- Nền: `#d6eaff`
- Viền: `ridge`, `bd=2`
- Kích thước: `180x100`
- Số liệu: **font 20, bold**, màu `#002b80`
- Tiêu đề: **font 10, bold**, màu `#003366`

> **Tự động cập nhật** khi vào trang.

### 1.5. Biểu đồ doanh thu
- **Khung chính**: `frame_chart` → chia 2 khung con  

  | Khung con 1 (`frame_ve`) | Khung con 2 (`frame_dieu_khien`) |
  |--------------------------|----------------------------------|
  | **Chứa canvas biểu đồ**  | **Nút điều khiển năm**           |

- **Loại**: Cột (`bar chart`)
- **Kích thước**: `7x4 inches`
- **Trục X**: Tháng 1–12
- **Trục Y**: Doanh thu (VNĐ)
- **Màu cột**: `#1565C0`
- **Tooltip**: Hiển thị giá trị khi hover
- **Định dạng tiền**: `1.250.000` (ngăn cách bằng dấu chấm)

**Truy vấn dữ liệu**:
```sql
SELECT MONTH(NgayBan), SUM(TongTien)
FROM HoaDonBan
WHERE TrangThai = N'Đã thanh toán' AND YEAR(NgayBan) = ?
GROUP BY MONTH(NgayBan)

# QUẢN LÝ SẢN PHẨM TIVI – README

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò       | Quyền hạn |
|---------------|-----------|
| **admin**     | **Toàn quyền**: Thêm, Sửa, Xóa, Tìm kiếm, Xem bảng |
| **nhân viên** | **Không truy cập được trang này** |

> **Chỉ admin** mới thấy menu `Quản lý Tivi`

---

## 2. GIAO DIỆN CHÍNH

### Tiêu đề trang
- **Text**: `QUẢN LÝ SẢN PHẨM TIVI`
- **Font**: `Segoe UI`, **16pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Khu vực tìm kiếm
- **Label**: `"Tìm kiếm:"` + biểu tượng kính lúp
- **Ô nhập**: Rộng, hỗ trợ phím **Enter**
- **Placeholder**: `"Nhập mã, tên, hãng, kích thước..."`
- **Nút**:
  - **Tìm** (màu xanh dương)
  - **Hủy** (màu đỏ) → xóa điều kiện, tải lại dữ liệu

---

## 3. FORM NHẬP THÔNG TIN SẢN PHẨM

> **Tiêu đề**: `"Thông tin sản phẩm"` – màu xanh, font 12pt, **Bold**

| Trường             | Kiểu dữ liệu       | Kiểm tra bắt buộc |
|--------------------|--------------------|-------------------|
| **Mã Tivi**        | `Entry`            | Bắt buộc, **không trùng**, 5–15 ký tự, chỉ chứa chữ/số/gạch ngang |
| **Tên Tivi**       | `Entry`            | Bắt buộc, ≥ 5 ký tự |
| **Hãng sản xuất**  | `Combobox`         | `Samsung`, `LG`, `Sony`, `TCL`, `Xiaomi`, `Panasonic`, `Khác` |
| **Kích thước**     | `Entry`            | Số nguyên, từ **24 đến 100** inch |
| **Độ phân giải**   | `Combobox`         | `HD`, `Full HD`, `4K UHD`, `8K` |
| **Loại màn hình**  | `Combobox`         | `LED`, `OLED`, `QLED`, `Mini-LED` |
| **Tần số quét**    | `Entry`            | Số nguyên, từ **60 đến 240** Hz |
| **Giá bán (VNĐ)**  | `Entry`            | Số dương, định dạng tiền tệ |
| **Mô tả**          | `Text` (nhiều dòng)| Không bắt buộc |

---

## 4. BẢNG HIỂN THỊ SẢN PHẨM (Treeview)

| Cột               | Nội dung ví dụ         | Căn chỉnh |
|-------------------|------------------------|---------|
| Mã Tivi           | `TV-2025-SAM-001`      | Giữa    |
| Tên Tivi          | `Samsung Crystal UHD`  | Trái    |
| Hãng              | `Samsung`              | Giữa    |
| Kích thước        | `55 inch`              | Giữa    |
| Độ phân giải      | `4K UHD`               | Giữa    |
| Loại màn          | `QLED`                 | Giữa    |
| Tần số            | `120 Hz`               | Giữa    |
| Giá bán           | `15,990,000 VNĐ`       | Phải    |

**Tính năng bảng:**
- Cuộn dọc + ngang
- Dòng **striped** (xen kẽ màu)
- **Click chọn dòng** → tự động điền toàn bộ dữ liệu vào form
- **Sắp xếp mặc định** theo **Mã Tivi**

---

## 5. NÚT CHỨC NĂNG

| Nút         | Màu         | Chức năng |
|-------------|-------------|---------|
| **Thêm**    | Vàng        | Kiểm tra → thêm vào bảng + `ds_them` |
| **Sửa**     | Cam         | Cập nhật dòng → `ds_sua` |
| **Xóa**     | Đỏ          | Xác nhận → xóa + `ds_xoa` |
| **Làm mới** | Xanh dương  | Hủy buffer → tải lại CSDL |
| **Lưu**     | Xanh lá     | **Transaction**: Xóa → Thêm → Sửa |

---

## 6. TÍNH NĂNG CHI TIẾT

### Click chọn dòng → Tự động điền form
Khi người dùng **bấm vào bất kỳ dòng nào trên bảng**:

1. Lấy dữ liệu từ dòng được chọn
2. Điền tự động vào **tất cả các ô input**:
   - `Mã Tivi` → `txt_maTivi`
   - `Tên Tivi` → `txt_tenTivi`
   - `Hãng` → `cb_hangSX.set(...)`
   - `Kích thước` → `txt_kichThuoc`
   - `Độ phân giải` → `cb_doPhanGiai.set(...)`
   - `Loại màn hình` → `cb_loaiManHinh.set(...)`
   - `Tần số quét` → `txt_tanSoQuet`
   - `Giá bán` → `txt_giaBan` (định dạng `#,##0`)
   - `Mô tả` → `txt_moTa.insert(...)`
3. **Tự động focus** về ô **Tên Tivi**
4. Sẵn sàng **Sửa** hoặc **Xóa** mà không cần nhấn nút khác

---

### Thêm sản phẩm
1. Kiểm tra **tất cả trường bắt buộc**
2. **Mã Tivi**: không trùng, hợp lệ (chữ/số/gạch ngang)
3. **Kích thước**, **Tần số quét**: số nguyên hợp lệ
4. **Giá bán**: > 0
5. Thêm dòng vào bảng
6. Thêm vào `ds_them`
7. Xóa form + thông báo thành công

---

### Sửa sản phẩm
1. Phải **chọn dòng**
2. Kiểm tra **Mã Tivi mới không trùng** (ngoại trừ chính nó)
3. Cập nhật dòng trên bảng
4. Nếu trong `ds_them` → cập nhật
5. Nếu không → thêm vào `ds_sua = [(dữ liệu mới..., MaTivi_cũ)]`
6. Xóa form + thông báo

---

### Xóa sản phẩm
1. Phải chọn dòng
2. **Không cho xóa** nếu Tivi đang có trong **hóa đơn** hoặc **phiếu nhập**
3. Xác nhận: `"Xóa sản phẩm [Tên Tivi]?"`
4. Xóa dòng khỏi bảng
5. Nếu trong `ds_them` → xóa khỏi danh sách
6. Nếu không → thêm `MaTivi` vào `ds_xoa`
7. Xóa form + thông báo

---

### Lưu thay đổi (Transaction an toàn)
- **Nút**: `"Lưu"` – màu xanh lá, chữ trắng, font đậm
- **Khi nhấn**:
  1. Hộp thoại: *"Bạn có chắc muốn lưu tất cả thay đổi?"*
  2. Nếu **Có**:
     - Mở **transaction**
     - **Bước 1**: Xóa các sản phẩm trong `ds_xoa`
     - **Bước 2**: Thêm các sản phẩm trong `ds_them`
     - **Bước 3**: Cập nhật các sản phẩm trong `ds_sua`
     - **Thành công**: Commit, tải lại dữ liệu, xóa buffer, thông báo *"Lưu thành công!"*
     - **Lỗi** (trùng mã, ràng buộc...): `rollback()`, giữ buffer, thông báo lỗi chi tiết
  3. Nếu **Không**: Hủy thao tác

---

## 7. CẤU TRÚC BUFFER THAY ĐỔI

| Danh sách   | Cấu trúc |
|-------------|---------|
| `ds_them`   | `(MaTivi, TenTivi, HangSX, KichThuoc, DoPhanGiai, LoaiManHinh, TanSoQuet, GiaBan, MoTa)` |
| `ds_sua`    | `(dữ liệu mới..., MaTivi_cũ)` |
| `ds_xoa`    | `(MaTivi,)` |

---

## 8. XỬ LÝ LỖI

| Trường hợp                  | Thông báo |
|-----------------------------|----------|
| **Mã Tivi trùng**           | `"Mã Tivi đã tồn tại!"` |
| **Giá bán ≤ 0**             | `"Giá bán phải lớn hơn 0"` |
| **Kích thước không hợp lệ** | `"Kích thước từ 24 đến 100 inch"` |
| **Xóa Tivi có giao dịch**   | `"Không thể xóa do có hóa đơn/phiếu nhập"` |
| **Lỗi CSDL**                | `rollback()` + `"Lỗi hệ thống, thay đổi đã được hủy"` |

---

## 9. HÀM TẢI DỮ LIỆU (`load_data()`)
Gọi khi:
- Vào trang
- Sau khi **Lưu thành công**
- Nhấn **Làm mới**
- Nhấn **Hủy tìm kiếm**

---

# QUẢN LÝ HÃNG SẢN XUẤT TIVI – README

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò       | Quyền hạn |
|---------------|-----------|
| **admin**     | **Toàn quyền**: Thêm, Sửa, Xóa, Tìm kiếm, Xem bảng |
| **nhân viên** | **Không truy cập được trang này** |

> **Chỉ admin** mới thấy menu `Quản lý Hãng Sản Xuất`

---

## 2. GIAO DIỆN CHÍNH

### Tiêu đề trang
- **Text**: `QUẢN LÝ HÃNG SẢN XUẤT`
- **Font**: `Segoe UI`, **16pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Khu vực tìm kiếm
- **Label**: `"Tìm kiếm:"` + biểu tượng kính lúp
- **Ô nhập**: Rộng, hỗ trợ phím **Enter**
- **Placeholder**: `"Nhập mã, tên, quốc gia..."`
- **Nút**:
  - **Tìm** (màu xanh dương)
  - **Hủy** (màu đỏ) → xóa điều kiện, tải lại dữ liệu

---

## 3. FORM NHẬP THÔNG TIN HÃNG

> **Tiêu đề**: `"Thông tin hãng sản xuất"` – màu xanh, font 12pt, **Bold**

| Trường             | Kiểu dữ liệu       | Kiểm tra bắt buộc |
|--------------------|--------------------|-------------------|
| **Mã hãng**        | `Entry`            | Bắt buộc, **không trùng**, 2–10 ký tự, chỉ **chữ hoa, số, gạch dưới** |
| **Tên hãng**       | `Entry`            | Bắt buộc, ≥ 2 ký tự, **không chứa số** |
| **Quốc gia**       | `Combobox`         | `Hàn Quốc`, `Nhật Bản`, `Trung Quốc`, `Mỹ`, `Việt Nam`, `Đài Loan`, `Khác` |
| **Website**        | `Entry`            | URL hợp lệ |
| **Email liên hệ**  | `Entry`            | Định dạng email, **không trùng** |
| **Số điện thoại**  | `Entry`            | 10–12 số, bắt đầu bằng `0` hoặc `+` |
| **Mô tả**          | `Text` (nhiều dòng)| Không bắt buộc |

---

## 4. BẢNG HIỂN THỊ HÃNG (Treeview)

| Cột               | Nội dung ví dụ         | Căn chỉnh |
|-------------------|------------------------|---------|
| Mã hãng           | `SAM`                  | Giữa    |
| Tên hãng          | `Samsung`              | Trái    |
| Quốc gia          | `Hàn Quốc`             | Giữa    |
| Website           | `https://samsung.com`  | Trái    |
| Email             | `support@samsung.com`  | Trái    |
| SĐT               | `1800-588-888`         | Giữa    |

**Tính năng bảng:**
- Cuộn dọc + ngang
- Dòng **striped** (xen kẽ màu)
- **Click chọn dòng** → tự động điền toàn bộ dữ liệu vào form
- **Sắp xếp mặc định** theo **Mã hãng**

---

## 5. NÚT CHỨC NĂNG

| Nút         | Màu         | Chức năng |
|-------------|-------------|---------|
| **Thêm**    | Vàng        | Kiểm tra → thêm vào bảng + `ds_them` |
| **Sửa**     | Cam         | Cập nhật dòng → `ds_sua` |
| **Xóa**     | Đỏ          | Xác nhận → xóa + `ds_xoa` |
| **Làm mới** | Xanh dương  | Hủy buffer → tải lại CSDL |
| **Lưu**     | Xanh lá     | **Transaction**: Xóa → Thêm → Sửa |

---

## 6. TÍNH NĂNG CHI TIẾT

### Click chọn dòng → Tự động điền form
Khi người dùng **bấm vào bất kỳ dòng nào trên bảng**:

1. Lấy dữ liệu từ dòng được chọn
2. Điền tự động vào **tất cả các ô input**:
   - `Mã hãng` → `txt_maHang`
   - `Tên hãng` → `txt_tenHang`
   - `Quốc gia` → `cb_quocGia.set(...)`
   - `Website` → `txt_website`
   - `Email liên hệ` → `txt_email`
   - `Số điện thoại` → `txt_sdt`
   - `Mô tả` → `txt_moTa.insert(...)`
3. **Tự động focus** về ô **Tên hãng**
4. Sẵn sàng **Sửa** hoặc **Xóa** mà không cần nhấn nút khác

---

### Thêm hãng
1. Kiểm tra **tất cả trường bắt buộc**
2. **Mã hãng**: không trùng, chỉ chữ hoa/số/gạch dưới
3. **Tên hãng**: không chứa số
4. **Website**: URL hợp lệ
5. **Email**: định dạng + không trùng
6. **SĐT**: 10–12 số, bắt đầu `0` hoặc `+`
7. Thêm dòng vào bảng
8. Thêm vào `ds_them = [(MaHang, TenHang, QuocGia, Website, Email, SoDienThoai, MoTa)]`
9. Xóa form + thông báo thành công

---

### Sửa hãng
1. Phải **chọn dòng**
2. Kiểm tra **Mã hãng mới không trùng** (ngoại trừ chính nó)
3. Cập nhật dòng trên bảng
4. Nếu trong `ds_them` → cập nhật
5. Nếu không → thêm vào `ds_sua = [(dữ liệu mới..., MaHang_cũ)]`
6. Xóa form + thông báo

---

### Xóa hãng
1. Phải chọn dòng
2. **Không cho xóa** nếu hãng đang có **sản phẩm Tivi liên kết**
3. Xác nhận: `"Xóa hãng [Tên hãng]?"`
4. Xóa dòng khỏi bảng
5. Nếu trong `ds_them` → xóa khỏi danh sách
6. Nếu không → thêm `MaHang` vào `ds_xoa`
7. Xóa form + thông báo

---

### Lưu thay đổi (Transaction an toàn)
- **Nút**: `"Lưu"` – màu xanh lá, chữ trắng, font đậm
- **Khi nhấn**:
  1. Hộp thoại: *"Bạn có chắc muốn lưu tất cả thay đổi?"*
  2. Nếu **Có**:
     - Mở **transaction**
     - **Bước 1**: Xóa các hãng trong `ds_xoa`
     - **Bước 2**: Thêm các hãng trong `ds_them`
     - **Bước 3**: Cập nhật các hãng trong `ds_sua`
     - **Thành công**: Commit, tải lại dữ liệu, xóa buffer, thông báo *"Lưu thành công!"*
     - **Lỗi** (trùng mã, ràng buộc...): `rollback()`, giữ buffer, thông báo lỗi chi tiết
  3. Nếu **Không**: Hủy thao tác

---

## 7. CẤU TRÚC BUFFER THAY ĐỔI

| Danh sách   | Cấu trúc |
|-------------|---------|
| `ds_them`   | `(MaHang, TenHang, QuocGia, Website, Email, SoDienThoai, MoTa)` |
| `ds_sua`    | `(dữ liệu mới..., MaHang_cũ)` |
| `ds_xoa`    | `(MaHang,)` |

---

## 8. XỬ LÝ LỖI & BẢO MẬT

| Trường hợp                  | Thông báo |
|-----------------------------|----------|
| **Mã hãng trùng**           | `"Mã hãng đã tồn tại!"` |
| **Tên hãng chứa số**        | `"Tên hãng không được chứa số"` |
| **Website không hợp lệ**    | `"Vui lòng nhập URL đầy đủ (http:// hoặc https://)"` |
| **Email không hợp lệ**      | `"Email không đúng định dạng"` |
| **Email trùng**             | `"Email này đã được sử dụng"` |
| **SĐT không hợp lệ**        | `"Số điện thoại phải có 10–12 số, bắt đầu bằng 0 hoặc +"` |
| **Xóa hãng có sản phẩm**    | `"Không thể xóa do có sản phẩm Tivi liên kết"` |
| **Lỗi CSDL**                | `rollback()` + `"Lỗi hệ thống, thay đổi đã được hủy"` |

---

## 9. HÀM TẢI DỮ LIỆU (`load_data()`)
Gọi khi:
- Vào trang
- Sau khi **Lưu thành công**
- Nhấn **Làm mới**
- Nhấn **Hủy tìm kiếm**

---

## 10. GIAO DIỆN CHO NHÂN VIÊN THƯỜNG
> **Không có quyền truy cập** → **Ẩn hoàn toàn trang**  
> (Không hiển thị menu, không route, không load dữ liệu)

---

# QUẢN LÝ NHÀ CUNG CẤP – README

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò       | Quyền hạn |
|---------------|-----------|
| **admin**     | **Toàn quyền**: Thêm, Sửa, Xóa, Tìm kiếm, Xem bảng |
| **nhân viên** | **Không truy cập được trang này** |

> **Chỉ admin** mới thấy menu `Quản lý Nhà Cung Cấp`

---

## 2. GIAO DIỆN CHÍNH

### Tiêu đề trang
- **Text**: `QUẢN LÝ NHÀ CUNG CẤP`
- **Font**: `Segoe UI`, **16pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Khu vực tìm kiếm
- **Label**: `"Tìm kiếm:"` + biểu tượng kính lúp
- **Ô nhập**: Rộng, hỗ trợ phím **Enter**
- **Placeholder**: `"Nhập mã, tên, SĐT, email..."`
- **Nút**:
  - **Tìm** (màu xanh dương)
  - **Hủy** (màu đỏ) → xóa điều kiện, tải lại dữ liệu

---

## 3. FORM NHẬP THÔNG TIN NHÀ CUNG CẤP

> **Tiêu đề**: `"Thông tin nhà cung cấp"` – màu xanh, font 12pt, **Bold**

| Trường              | Kiểu dữ liệu       | Kiểm tra bắt buộc |
|---------------------|--------------------|-------------------|
| **Mã NCC**          | `Entry`            | Bắt buộc, **không trùng**, 3–10 ký tự, chỉ **chữ hoa, số, gạch dưới** |
| **Tên công ty**     | `Entry`            | Bắt buộc, ≥ 3 ký tự |
| **Người liên hệ**   | `Entry`            | Bắt buộc, chỉ **chữ cái và khoảng trắng** |
| **Số điện thoại**   | `Entry`            | Bắt buộc, **10–12 số**, bắt đầu bằng `0` hoặc `+` |
| **Email**           | `Entry`            | Định dạng email, **không trùng** |
| **Địa chỉ**         | `Entry`            | Bắt buộc |
| **Website**         | `Entry`            | URL hợp lệ (`http://` hoặc `https://`) |
| **Mã số thuế**      | `Entry`            | 10–13 số, định dạng hợp lệ |
| **Ghi chú**         | `Text` (nhiều dòng)| Không bắt buộc |

---

## 4. BẢNG HIỂN THỊ NHÀ CUNG CẤP (Treeview)

| Cột               | Nội dung ví dụ               | Căn chỉnh |
|-------------------|------------------------------|---------|
| Mã NCC            | `NCC001`                     | Giữa    |
| Tên công ty       | `Công ty TNHH Samsung VN`    | Trái    |
| Người LH          | `Nguyễn Văn A`               | Trái    |
| SĐT               | `0901234567`                 | Giữa    |
| Email             | `contact@samsung.vn`         | Trái    |
| Địa chỉ           | `Lô E2, KCN Thăng Long`      | Trái    |
| Mã số thuế        | `0101234567`                 | Giữa    |

**Tính năng bảng:**
- Cuộn dọc + ngang
- Dòng **striped** (xen kẽ màu)
- **Click chọn dòng** → tự động điền toàn bộ dữ liệu vào form
- **Sắp xếp mặc định** theo **Mã NCC**

---

## 5. NÚT CHỨC NĂNG

| Nút         | Màu         | Chức năng |
|-------------|-------------|---------|
| **Thêm**    | Vàng        | Kiểm tra → thêm vào bảng + `ds_them` |
| **Sửa**     | Cam         | Cập nhật dòng → `ds_sua` |
| **Xóa**     | Đỏ          | Xác nhận → xóa + `ds_xoa` |
| **Làm mới** | Xanh dương  | Hủy buffer → tải lại CSDL |
| **Lưu**     | Xanh lá     | **Transaction**: Xóa → Thêm → Sửa |

---

## 6. TÍNH NĂNG CHI TIẾT

### Click chọn dòng → Tự động điền form
Khi người dùng **bấm vào bất kỳ dòng nào trên bảng**:

1. Lấy dữ liệu từ dòng được chọn
2. Điền tự động vào **tất cả các ô input**:
   - `Mã NCC` → `txt_maNCC`
   - `Tên công ty` → `txt_tenCongTy`
   - `Người liên hệ` → `txt_nguoiLienHe`
   - `Số điện thoại` → `txt_sdt`
   - `Email` → `txt_email`
   - `Địa chỉ` → `txt_diaChi`
   - `Website` → `txt_website`
   - `Mã số thuế` → `txt_maSoThue`
   - `Ghi chú` → `txt_ghiChu.insert(...)`
3. **Tự động focus** về ô **Tên công ty**
4. Sẵn sàng **Sửa** hoặc **Xóa** mà không cần nhấn nút khác

---

### Thêm nhà cung cấp
1. Kiểm tra **tất cả trường bắt buộc**
2. **Mã NCC**: không trùng, chỉ chữ hoa/số/gạch dưới
3. **SĐT**: 10–12 số, hợp lệ
4. **Email**: định dạng + không trùng
5. **Website**: URL hợp lệ (nếu có)
6. **Mã số thuế**: 10–13 số
7. Thêm dòng vào bảng
8. Thêm vào `ds_them = [(MaNCC, TenCongTy, NguoiLienHe, SoDienThoai, Email, DiaChi, Website, MaSoThue, GhiChu)]`
9. Xóa form + thông báo thành công

---

### Sửa nhà cung cấp
1. Phải **chọn dòng**
2. Kiểm tra **Mã NCC mới không trùng** (ngoại trừ chính nó)
3. Cập nhật dòng trên bảng
4. Nếu trong `ds_them` → cập nhật
5. Nếu không → thêm vào `ds_sua = [(dữ liệu mới..., MaNCC_cũ)]`
6. Xóa form + thông báo

---

### Xóa nhà cung cấp
1. Phải chọn dòng
2. **Không cho xóa** nếu NCC đang có **phiếu nhập**
3. Xác nhận: `"Xóa nhà cung cấp [Tên công ty]?"`
4. Xóa dòng khỏi bảng
5. Nếu trong `ds_them` → xóa khỏi danh sách
6. Nếu không → thêm `MaNCC` vào `ds_xoa`
7. Xóa form + thông báo

---

### Lưu thay đổi (Transaction an toàn)
- **Nút**: `"Lưu"` – màu xanh lá, chữ trắng, font đậm
- **Khi nhấn**:
  1. Hộp thoại: *"Bạn có chắc muốn lưu tất cả thay đổi?"*
  2. Nếu **Có**:
     - Mở **transaction**
     - **Bước 1**: Xóa các NCC trong `ds_xoa`
     - **Bước 2**: Thêm các NCC trong `ds_them`
     - **Bước 3**: Cập nhật các NCC trong `ds_sua`
     - **Thành công**: Commit, tải lại dữ liệu, xóa buffer, thông báo *"Lưu thành công!"*
     - **Lỗi** (trùng mã, ràng buộc...): `rollback()`, giữ buffer, thông báo lỗi chi tiết
  3. Nếu **Không**: Hủy thao tác

---

## 7. CẤU TRÚC BUFFER THAY ĐỔI

| Danh sách   | Cấu trúc |
|-------------|---------|
| `ds_them`   | `(MaNCC, TenCongTy, NguoiLienHe, SoDienThoai, Email, DiaChi, Website, MaSoThue, GhiChu)` |
| `ds_sua`    | `(dữ liệu mới..., MaNCC_cũ)` |
| `ds_xoa`    | `(MaNCC,)` |

---

## 8. XỬ LÝ LỖI & BẢO MẬT

| Trường hợp                     | Thông báo |
|--------------------------------|----------|
| **Mã NCC trùng**               | `"Mã NCC đã tồn tại!"` |
| **SĐT không hợp lệ**           | `"SĐT phải có 10–12 số, bắt đầu bằng 0 hoặc +"` |
| **Email sai định dạng**        | `"Email không đúng định dạng"` |
| **Email trùng**                | `"Email này đã được sử dụng"` |
| **Mã số thuế không hợp lệ**    | `"Mã số thuế phải có 10–13 số"` |
| **Xóa NCC có phiếu nhập**      | `"Không thể xóa do có phiếu nhập liên kết"` |
| **Lỗi CSDL**                   | `rollback()` + `"Lỗi hệ thống, thay đổi đã được hủy"` |

---

## 9. HÀM TẢI DỮ LIỆU (`load_data()`)
Gọi khi:
- Vào trang
- Sau khi **Lưu thành công**
- Nhấn **Làm mới**
- Nhấn **Hủy tìm kiếm**

---

## 10. GIAO DIỆN CHO NHÂN VIÊN THƯỜNG
> **Không có quyền truy cập** → **Ẩn hoàn toàn trang**  

---

# QUẢN LÝ CHÍNH SÁCH BẢO HÀNH – README

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò       | Quyền hạn |
|---------------|-----------|
| **admin**     | **Toàn quyền**: Thêm, Sửa, Xóa, Tìm kiếm, Xem bảng |
| **nhân viên** | **Không truy cập được trang này** |

> **Chỉ admin** mới thấy menu `Quản lý Bảo Hành`

---

## 2. GIAO DIỆN CHÍNH

### Tiêu đề trang
- **Text**: `QUẢN LÝ CHÍNH SÁCH BẢO HÀNH`
- **Font**: `Segoe UI`, **16pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Khu vực tìm kiếm
- **Label**: `"Tìm kiếm:"` + biểu tượng kính lúp
- **Ô nhập**: Rộng, hỗ trợ phím **Enter**
- **Placeholder**: `"Nhập mã, tên chính sách, thời gian..."`
- **Nút**:
  - **Tìm** (màu xanh dương)
  - **Hủy** (màu đỏ) → xóa điều kiện, tải lại dữ liệu

---

## 3. FORM NHẬP THÔNG TIN CHÍNH SÁCH

> **Tiêu đề**: `"Thông tin chính sách bảo hành"` – màu xanh, font 12pt, **Bold**

| Trường                        | Kiểu dữ liệu       | Kiểm tra bắt buộc |
|-------------------------------|--------------------|-------------------|
| **Mã chính sách**             | `Entry`            | Bắt buộc, **không trùng**, 3–10 ký tự, chỉ **chữ hoa, số, gạch dưới** |
| **Tên chính sách**            | `Entry`            | Bắt buộc, ≥ 5 ký tự |
| **Thời gian bảo hành**        | `Entry`            | Số nguyên, **1–60 tháng** |
| **Loại bảo hành**             | `Combobox`         | `Bảo hành điện tử`, `Bảo hành giấy`, `Bảo hành VIP`, `Bảo hành mở rộng` |
| **Điều kiện áp dụng**         | `Text` (nhiều dòng)| Bắt buộc |
| **Lỗi được bảo hành**         | `Text` (nhiều dòng)| Không bắt buộc |
| **Lỗi không được bảo hành**   | `Text` (nhiều dòng)| Không bắt buộc |
| **Trạng thái**                | `Combobox`         | `Đang áp dụng`, `Hết hiệu lực`, `Tạm ngưng` |

---

## 4. BẢNG HIỂN THỊ CHÍNH SÁCH (Treeview)

| Cột               | Nội dung ví dụ               | Căn chỉnh |
|-------------------|------------------------------|---------|
| Mã CS             | `BH001`                      | Giữa    |
| Tên chính sách    | `Bảo hành điện tử 24 tháng`  | Trái    |
| Thời gian         | `24 tháng`                   | Giữa    |
| Loại BH           | `Bảo hành điện tử`           | Giữa    |
| Trạng thái        | `Đang áp dụng`               | Giữa    |

**Tính năng bảng:**
- Cuộn dọc + ngang
- Dòng **striped** (xen kẽ màu)
- **Click chọn dòng** → tự động điền toàn bộ dữ liệu vào form
- **Sắp xếp mặc định** theo **Mã chính sách**

---

## 5. NÚT CHỨC NĂNG

| Nút         | Màu         | Chức năng |
|-------------|-------------|---------|
| **Thêm**    | Vàng        | Kiểm tra → thêm vào bảng + `ds_them` |
| **Sửa**     | Cam         | Cập nhật dòng → `ds_sua` |
| **Xóa**     | Đỏ          | Xác nhận → xóa + `ds_xoa` |
| **Làm mới** | Xanh dương  | Hủy buffer → tải lại CSDL |
| **Lưu**     | Xanh lá     | **Transaction**: Xóa → Thêm → Sửa |

---

## 6. TÍNH NĂNG CHI TIẾT

### Click chọn dòng → Tự động điền form
Khi người dùng **bấm vào bất kỳ dòng nào trên bảng**:

1. Lấy dữ liệu từ dòng được chọn
2. Điền tự động vào **tất cả các ô input**:
   - `Mã chính sách` → `txt_maCS`
   - `Tên chính sách` → `txt_tenCS`
   - `Thời gian bảo hành` → `txt_thoiGian`
   - `Loại bảo hành` → `cb_loaiBH.set(...)`
   - `Điều kiện áp dụng` → `txt_dieuKien.insert(...)`
   - `Lỗi được bảo hành` → `txt_loiDuocBH.insert(...)`
   - `Lỗi không được bảo hành` → `txt_loiKhongBH.insert(...)`
   - `Trạng thái` → `cb_trangThai.set(...)`
3. **Tự động focus** về ô **Tên chính sách**
4. Sẵn sàng **Sửa** hoặc **Xóa** mà không cần nhấn nút khác

---

### Thêm chính sách
1. Kiểm tra **tất cả trường bắt buộc**
2. **Mã chính sách**: không trùng, định dạng hợp lệ
3. **Thời gian**: 1–60 tháng
4. **Điều kiện áp dụng**: không để trống
5. Thêm dòng vào bảng
6. Thêm vào `ds_them = [(MaCS, TenCS, ThoiGian, LoaiBH, DieuKien, LoiDuocBH, LoiKhongBH, TrangThai)]`
7. Xóa form + thông báo thành công

---

### Sửa chính sách
1. Phải **chọn dòng**
2. Kiểm tra **Mã chính sách mới không trùng** (ngoại trừ chính nó)
3. Cập nhật dòng trên bảng
4. Nếu trong `ds_them` → cập nhật
5. Nếu không → thêm vào `ds_sua = [(dữ liệu mới..., MaCS_cũ)]`
6. Xóa form + thông báo

---

### Xóa chính sách
1. Phải chọn dòng
2. **Không cho xóa** nếu chính sách đang **được áp dụng cho sản phẩm**
3. Xác nhận: `"Xóa chính sách [Tên chính sách]?"`
4. Xóa dòng khỏi bảng
5. Nếu trong `ds_them` → xóa khỏi danh sách
6. Nếu không → thêm `MaCS` vào `ds_xoa`
7. Xóa form + thông báo

---

### Lưu thay đổi (Transaction an toàn)
- **Nút**: `"Lưu"` – màu xanh lá, chữ trắng, font đậm
- **Khi nhấn**:
  1. Hộp thoại: *"Bạn có chắc muốn lưu tất cả thay đổi?"*
  2. Nếu **Có**:
     - Mở **transaction**
     - **Bước 1**: Xóa các chính sách trong `ds_xoa`
     - **Bước 2**: Thêm các chính sách trong `ds_them`
     - **Bước 3**: Cập nhật các chính sách trong `ds_sua`
     - **Thành công**: Commit, tải lại dữ liệu, xóa buffer, thông báo *"Lưu thành công!"*
     - **Lỗi** (trùng mã, ràng buộc...): `rollback()`, giữ buffer, thông báo lỗi chi tiết
  3. Nếu **Không**: Hủy thao tác

---

## 7. CẤU TRÚC BUFFER THAY ĐỔI

| Danh sách   | Cấu trúc |
|-------------|---------|
| `ds_them`   | `(MaCS, TenCS, ThoiGian, LoaiBH, DieuKien, LoiDuocBH, LoiKhongBH, TrangThai)` |
| `ds_sua`    | `(dữ liệu mới..., MaCS_cũ)` |
| `ds_xoa`    | `(MaCS,)` |

---

## 8. XỬ LÝ LỖI & BẢO MẬT

| Trường hợp                        | Thông báo |
|-----------------------------------|----------|
| **Mã chính sách trùng**           | `"Mã chính sách đã tồn tại!"` |
| **Thời gian không hợp lệ**        | `"Thời gian bảo hành từ 1 đến 60 tháng"` |
| **Điều kiện áp dụng trống**       | `"Vui lòng nhập điều kiện áp dụng"` |
| **Xóa chính sách đang dùng**      | `"Không thể xóa do có sản phẩm đang áp dụng"` |
| **Lỗi CSDL**                      | `rollback()` + `"Lỗi hệ thống, thay đổi đã được hủy"` |

---

## 9. HÀM TẢI DỮ LIỆU (`load_data()`)
Gọi khi:
- Vào trang
- Sau khi **Lưu thành công**
- Nhấn **Làm mới**
- Nhấn **Hủy tìm kiếm**

---

## 10. GIAO DIỆN CHO NHÂN VIÊN THƯỜNG
> **Không có quyền truy cập** → **Ẩn hoàn toàn trang**  

---

# QUẢN LÝ KHÁCH HÀNG – README

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò       | Quyền hạn |
|---------------|-----------|
| **admin**     | **Toàn quyền**: Thêm, Sửa, Xóa, Tìm kiếm, Xem bảng |
| **nhân viên** | **Không truy cập được trang này** |

> **Chỉ admin** mới thấy menu `Quản lý Khách Hàng`

---

## 2. GIAO DIỆN CHÍNH

### Tiêu đề trang
- **Text**: `QUẢN LÝ KHÁCH HÀNG`
- **Font**: `Segoe UI`, **16pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Khu vực tìm kiếm
- **Label**: `"Tìm kiếm:"` + biểu tượng kính lúp  
- **Ô nhập**: Rộng, hỗ trợ phím **Enter**  
- **Placeholder**: `"Nhập mã, tên, SĐT, email..."`  
- **Nút**:
  - **Tìm** (màu xanh dương)
  - **Hủy** (màu đỏ) → xóa điều kiện, tải lại dữ liệu

---

## 3. FORM NHẬP THÔNG TIN KHÁCH HÀNG

> **Tiêu đề**: `"Thông tin khách hàng"` – màu xanh, font 12pt, **Bold**

| Trường                | Kiểu dữ liệu       | Kiểm tra bắt buộc |
|-----------------------|--------------------|-------------------|
| **Mã khách hàng**     | `Entry`            | Bắt buộc, **không trùng**, 3–10 ký tự, chỉ **chữ hoa, số, gạch dưới** |
| **Họ tên**            | `Entry`            | Bắt buộc, **chỉ chữ & khoảng trắng**, ≥ 2 từ |
| **Giới tính**         | `Combobox`         | `Nam`, `Nữ`, `Khác` |
| **Ngày sinh**         | `DateEntry`        | **13–100 tuổi** (tính đến hiện tại) |
| **Số điện thoại**     | `Entry`            | Bắt buộc, **chính xác 10 số**, bắt đầu bằng `0` |
| **Email**             | `Entry`            | Định dạng email, **không trùng** |
| **Địa chỉ**           | `Entry`            | Bắt buộc |
| **Loại khách hàng**   | `Combobox`         | `Thường`, `Thân thiết`, `VIP`, `Đại lý` |
| **Ghi chú**           | `Text` (nhiều dòng)| Không bắt buộc |

---

## 4. BẢNG HIỂN THỊ KHÁCH HÀNG (Treeview)

| Cột            | Nội dung ví dụ               | Căn chỉnh |
|----------------|------------------------------|---------|
| Mã KH          | `KH001`                      | Giữa    |
| Họ tên         | `Nguyễn Văn An`              | Trái    |
| Giới tính      | `Nam`                        | Giữa    |
| Ngày sinh      | `15/03/1995`                 | Giữa    |
| SĐT            | `0901234567`                 | Giữa    |
| Email          | `an.nguyen@gmail.com`        | Trái    |
| Loại KH        | `VIP`                        | Giữa    |
| Địa chỉ        | `123 Lê Lợi, Q.1, TP.HCM`    | Trái    |

**Tính năng bảng:**
- Cuộn dọc + ngang
- Dòng **striped** (xen kẽ màu)
- **Click chọn dòng** → tự động điền toàn bộ dữ liệu vào form
- **Sắp xếp mặc định** theo **Mã KH**

---

## 5. NÚT CHỨC NĂNG

| Nút         | Màu         | Chức năng |
|-------------|-------------|---------|
| **Thêm**    | Vàng        | Kiểm tra → thêm vào bảng + `ds_them` |
| **Sửa**     | Cam         | Cập nhật dòng → `ds_sua` |
| **Xóa**     | Đỏ          | Xác nhận → xóa + `ds_xoa` |
| **Làm mới** | Xanh dương  | Hủy buffer → tải lại CSDL |
| **Lưu**     | Xanh lá     | **Transaction**: Xóa → Thêm → Sửa |

---

## 6. TÍNH NĂNG CHI TIẾT

### Click chọn dòng → Tự động điền form
Khi người dùng **bấm vào bất kỳ dòng nào trên bảng**:

1. Lấy dữ liệu từ dòng được chọn
2. Điền tự động vào **tất cả các ô input**:
   - `Mã khách hàng` → `txt_maKH`
   - `Họ tên` → `txt_tenKH`
   - `Giới tính` → `cb_gioiTinh.set(...)`
   - `Ngày sinh` → `date_ngaySinh.set_date(...)`
   - `Số điện thoại` → `txt_sdt`
   - `Email` → `txt_email`
   - `Địa chỉ` → `txt_diaChi`
   - `Loại khách hàng` → `cb_loaiKH.set(...)`
   - `Ghi chú` → `txt_ghiChu.insert(...)`
3. **Tự động focus** về ô **Họ tên**
4. Sẵn sàng **Sửa** hoặc **Xóa** mà không cần nhấn nút khác

> **Mục đích**: Tăng tốc độ thao tác, giảm lỗi nhập tay

---

### Thêm khách hàng
1. Kiểm tra **tất cả trường bắt buộc**
2. **Mã KH**: không trùng, định dạng hợp lệ
3. **Họ tên**: ≥ 2 từ, chỉ chữ và khoảng trắng
4. **SĐT**: đúng 10 số, bắt đầu bằng `0`
5. **Email**: định dạng + không trùng
6. **Ngày sinh**: 13–100 tuổi
7. Thêm dòng vào bảng
8. Thêm vào `ds_them = [(MaKH, TenKH, GioiTinh, NgaySinh, SoDienThoai, Email, DiaChi, LoaiKH, GhiChu)]`
9. Xóa form + thông báo thành công

---

### Sửa khách hàng
1. Phải **chọn dòng**
2. Kiểm tra **Mã KH mới không trùng** (ngoại trừ chính nó)
3. Cập nhật dòng trên bảng
4. Nếu trong `ds_them` → cập nhật
5. Nếu không → thêm vào `ds_sua = [(dữ liệu mới..., MaKH_cũ)]`
6. Xóa form + thông báo

---

### Xóa khách hàng
1. Phải chọn dòng
2. **Không cho xóa** nếu khách hàng đang có **hóa đơn**
3. Xác nhận: `"Xóa khách hàng [Tên KH]?"`
4. Xóa dòng khỏi bảng
5. Nếu trong `ds_them` → xóa khỏi danh sách
6. Nếu không → thêm `MaKH` vào `ds_xoa`
7. Xóa form + thông báo

---

### Lưu thay đổi (Transaction an toàn)
- **Nút**: `"Lưu"` – màu xanh lá, chữ trắng, font đậm
- **Khi nhấn**:
  1. Hộp thoại: *"Bạn có chắc muốn lưu tất cả thay đổi?"*
  2. Nếu **Có**:
     - Mở **transaction**
     - **Bước 1**: Xóa các khách hàng trong `ds_xoa`
     - **Bước 2**: Thêm các khách hàng trong `ds_them`
     - **Bước 3**: Cập nhật các khách hàng trong `ds_sua`
     - **Thành công**: Commit, tải lại dữ liệu, xóa buffer, thông báo *"Lưu thành công!"*
     - **Lỗi** (trùng mã, ràng buộc...): `rollback()`, giữ buffer, thông báo lỗi chi tiết
  3. Nếu **Không**: Hủy thao tác

---

## 7. CẤU TRÚC BUFFER THAY ĐỔI

| Danh sách   | Cấu trúc |
|-------------|---------|
| `ds_them`   | `(MaKH, TenKH, GioiTinh, NgaySinh, SoDienThoai, Email, DiaChi, LoaiKH, GhiChu)` |
| `ds_sua`    | `(dữ liệu mới..., MaKH_cũ)` |
| `ds_xoa`    | `(MaKH,)` |

---

## 8. XỬ LÝ LỖI & BẢO MẬT

| Trường hợp                     | Thông báo |
|--------------------------------|----------|
| **Mã KH trùng**                | `"Mã khách hàng đã tồn tại!"` |
| **Họ tên không hợp lệ**        | `"Họ tên phải có ít nhất 2 từ, chỉ chứa chữ và khoảng trắng"` |
| **SĐT sai định dạng**          | `"SĐT phải có đúng 10 số, bắt đầu bằng 0"` |
| **Email không hợp lệ**         | `"Email không đúng định dạng"` |
| **Email trùng**                | `"Email này đã được sử dụng"` |
| **Ngày sinh không hợp lệ**     | `"Tuổi phải từ 13 đến 100"` |
| **Xóa KH có hóa đơn**          | `"Không thể xóa do có hóa đơn liên kết"` |
| **Lỗi CSDL**                   | `rollback()` + `"Lỗi hệ thống, thay đổi đã được hủy"` |

---

## 9. HÀM TẢI DỮ LIỆU (`load_data()`)
Gọi khi:
- Vào trang
- Sau khi **Lưu thành công**
- Nhấn **Làm mới**
- Nhấn **Hủy tìm kiếm**

---

## 10. GIAO DIỆN CHO NHÂN VIÊN THƯỜNG
> **Không có quyền truy cập** → **Ẩn hoàn toàn trang**  
> (Không hiển thị menu, không route, không load dữ liệu)

---

# QUẢN LÝ NHÂN VIÊN – README

---

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò       | Quyền hạn |
|---------------|-----------|
| **admin**     | **Toàn quyền**: Thêm, Sửa, Xóa, Tìm kiếm, Xem bảng |
| **nhân viên** | **Không truy cập được trang này** |

> **Chỉ admin** mới thấy menu `Quản lý Nhân Viên`

---

## 2. GIAO DIỆN CHÍNH

### Tiêu đề trang
- **Text**: `QUẢN LÝ NHÂN VIÊN`
- **Font**: `Segoe UI`, **16pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Khu vực tìm kiếm
- **Label**: `"Tìm kiếm:"` + biểu tượng kính lúp  
- **Ô nhập**: Rộng, hỗ trợ phím **Enter**  
- **Placeholder**: `"Nhập mã, tên, SĐT, email..."`  
- **Nút**:
  - **Tìm** (màu xanh dương)
  - **Hủy** (màu đỏ) → xóa điều kiện, tải lại dữ liệu

---

## 3. FORM NHẬP THÔNG TIN NHÂN VIÊN

> **Tiêu đề**: `"Thông tin nhân viên"` – màu xanh, font 12pt, **Bold**

| Trường               | Kiểu dữ liệu       | Kiểm tra bắt buộc |
|----------------------|--------------------|-------------------|
| **Mã nhân viên**     | `Entry`            | Bắt buộc, **không trùng**, 3–10 ký tự, chỉ **chữ/số/gạch dưới** |
| **Họ tên**           | `Entry`            | Bắt buộc, **chỉ chữ & khoảng trắng**, ≥ 2 từ |
| **Giới tính**        | `Combobox`         | `Nam`, `Nữ` |
| **Ngày sinh**        | `DateEntry`        | **Cảnh báo nếu < 18 tuổi** (không chặn) |
| **Số điện thoại**    | `Entry`            | Bắt buộc, **chính xác 10 số**, bắt đầu bằng `0` |
| **Email**            | `Entry`            | Định dạng `*@*.*`, **không trùng** |
| **Địa chỉ**          | `Entry`            | Bắt buộc |
| **Chức vụ**          | `Combobox`         | `Nhân viên bán hàng`, `Thu ngân`, `Quản lý kho`, `Kế toán` |
| **Lương cơ bản**     | `Entry`            | Số dương, định dạng tiền tệ (VNĐ) |

---

## 4. BẢNG HIỂN THỊ NHÂN VIÊN (Treeview)

| Cột            | Nội dung ví dụ               | Căn chỉnh |
|----------------|------------------------------|---------|
| Mã NV          | `NV001`                      | Giữa    |
| Họ tên         | `Trần Thị Bích Ngọc`         | Trái    |
| Giới tính      | `Nữ`                         | Giữa    |
| Ngày sinh      | `20/05/1998`                 | Giữa    |
| SĐT            | `0908765432`                 | Giữa    |
| Email          | `ngoc.tran@store.com`        | Trái    |
| Chức vụ        | `Nhân viên bán hàng`         | Trái    |
| Lương          | `8,500,000 VNĐ`              | Phải    |

**Tính năng bảng:**
- Cuộn dọc + ngang
- Dòng **striped** (xen kẽ màu)
- **Click chọn dòng** → tự động điền toàn bộ dữ liệu vào form
- **Sắp xếp mặc định** theo **Mã NV**

---

## 5. NÚT CHỨC NĂNG

| Nút         | Màu         | Chức năng |
|-------------|-------------|---------|
| **Thêm**    | Vàng        | Kiểm tra → thêm vào bảng + `ds_them` |
| **Sửa**     | Cam         | Cập nhật dòng → `ds_sua` |
| **Xóa**     | Đỏ          | Xác nhận → xóa + `ds_xoa` |
| **Làm mới** | Xanh dương  | Hủy buffer → tải lại CSDL |
| **Lưu**     | Xanh lá     | **Transaction**: Xóa → Thêm → Sửa |

---

## 6. TÍNH NĂNG CHI TIẾT

### Click chọn dòng → Tự động điền form
Khi người dùng **bấm vào bất kỳ dòng nào trên bảng**:

1. Lấy dữ liệu từ dòng được chọn
2. Điền tự động vào **tất cả các ô input**:
   - `Mã nhân viên` → `txt_maNV`
   - `Họ tên` → `txt_tenNV`
   - `Giới tính` → `cb_gioiTinh.set(...)`
   - `Ngày sinh` → `date_ngaySinh.set_date(...)`
   - `SĐT` → `txt_sdt`
   - `Email` → `txt_email`
   - `Địa chỉ` → `txt_diaChi`
   - `Chức vụ` → `cb_chucVu.set(...)`
   - `Lương` → `txt_luong` (định dạng `#,##0`)
3. **Tự động focus** về ô **Họ tên**
4. Sẵn sàng **Sửa** hoặc **Xóa** mà không cần nhấn nút khác

---

### Thêm nhân viên
1. Kiểm tra **tất cả trường bắt buộc**
2. **Mã NV**: không trùng, định dạng hợp lệ (chữ/số/gạch dưới)
3. **Họ tên**: ≥ 2 từ, chỉ chữ và khoảng trắng
4. **SĐT**: đúng 10 số, bắt đầu bằng `0`
5. **Email**: định dạng hợp lệ + không trùng
6. **Lương**: > 0
7. **Ngày sinh**: Cảnh báo nếu < 18 tuổi
8. Thêm dòng vào bảng
9. Thêm vào `ds_them = [(MaNV, TenNV, GioiTinh, NgaySinh, SoDienThoai, Email, DiaChi, ChucVu, Luong)]`
10. Xóa form + thông báo thành công

---

### Sửa nhân viên
1. Phải **chọn dòng**
2. Kiểm tra **Mã NV mới không trùng** (ngoại trừ chính nó)
3. Cập nhật dòng trên bảng
4. Nếu trong `ds_them` → cập nhật
5. Nếu không → thêm vào `ds_sua = [(dữ liệu mới..., MaNV_cũ)]`
6. Xóa form + thông báo

---

### Xóa nhân viên
1. Phải chọn dòng
2. **Không cho xóa** nếu nhân viên đang có **hóa đơn** hoặc **phiếu nhập**
3. Xác nhận: `"Xóa nhân viên [Tên NV]?"`
4. Xóa dòng khỏi bảng
5. Nếu trong `ds_them` → xóa khỏi danh sách
6. Nếu không → thêm `MaNV` vào `ds_xoa`
7. Xóa form + thông báo

---

### Lưu thay đổi (Transaction an toàn)
- **Nút**: `"Lưu"` – màu xanh lá, chữ trắng, font đậm
- **Khi nhấn**:
  1. Hộp thoại: *"Bạn có chắc muốn lưu tất cả thay đổi?"*
  2. Nếu **Có**:
     - Mở **transaction**
     - **Bước 1**: Xóa các nhân viên trong `ds_xoa`
     - **Bước 2**: Thêm các nhân viên trong `ds_them`
     - **Bước 3**: Cập nhật các nhân viên trong `ds_sua`
     - **Thành công**: Commit, tải lại dữ liệu, xóa buffer, thông báo *"Lưu thành công!"*
     - **Lỗi** (trùng mã, ràng buộc...): `rollback()`, giữ buffer, thông báo lỗi chi tiết
  3. Nếu **Không**: Hủy thao tác

---

## 7. CẤU TRÚC BUFFER THAY ĐỔI

| Danh sách   | Cấu trúc |
|-------------|---------|
| `ds_them`   | `(MaNV, TenNV, GioiTinh, NgaySinh, SoDienThoai, Email, DiaChi, ChucVu, Luong)` |
| `ds_sua`    | `(dữ liệu mới..., MaNV_cũ)` |
| `ds_xoa`    | `(MaNV,)` |

---

## 8. XỬ LÝ LỖI & BẢO MẬT

| Trường hợp                        | Thông báo |
|-----------------------------------|----------|
| **Mã NV trùng**                   | `"Mã nhân viên đã tồn tại!"` |
| **Họ tên không hợp lệ**           | `"Họ tên phải có ít nhất 2 từ, chỉ chứa chữ và khoảng trắng"` |
| **SĐT sai định dạng**             | `"SĐT phải có đúng 10 số, bắt đầu bằng 0"` |
| **Email không hợp lệ**            | `"Email không đúng định dạng"` |
| **Email trùng**                   | `"Email này đã được sử dụng"` |
| **Lương ≤ 0**                     | `"Lương cơ bản phải lớn hơn 0"` |
| **Ngày sinh < 18 tuổi**           | **Cảnh báo**: `"Nhân viên dưới 18 tuổi – vui lòng xác nhận"` |
| **Xóa NV có giao dịch**           | `"Không thể xóa do có hóa đơn hoặc phiếu nhập liên kết"` |
| **Lỗi CSDL**                      | `rollback()` + `"Lỗi hệ thống, thay đổi đã được hủy"` |

---

## 9. HÀM TẢI DỮ LIỆU (`load_data()`)
Gọi khi:
- Vào trang
- Sau khi **Lưu thành công**
- Nhấn **Làm mới**
- Nhấn **Hủy tìm kiếm**

---

## 10. GIAO DIỆN CHO NHÂN VIÊN THƯỜNG
> **Không có quyền truy cập** → **Ẩn hoàn toàn trang**  

---

# BÁN HÀNG – README

---

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò                | Quyền hạn |
|------------------------|----------|
| **admin**              | **Toàn quyền**: Bán, Hủy đơn, Xem lịch sử, Giảm giá > 10% |
875| **nhân viên bán hàng** | **Chỉ bán hàng + in hóa đơn** |
| **nhân viên kho**      | **Không truy cập được trang này** |

> **Tất cả nhân viên bán hàng** đều được dùng trang này

---

## 2. GIAO DIỆN CHÍNH

### Tiêu đề trang
- **Text**: `BÁN HÀNG TẠI QUẦY`
- **Font**: `Segoe UI`, **18pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Thông tin người dùng
- **Hiển thị**: `Xin chào, [Tên NV] (admin/nhân viên)`
- **Màu**:
  - Xanh lá: **admin**
  - Xanh dương: **nhân viên bán hàng**
- **Vị trí**: Góc trên bên **phải**

---

## 3. BỐ CỤC 3 CỘT (Tối ưu thao tác)

| **Cột trái (30%)** | **Cột giữa (40%)** | **Cột phải (30%)** |
|--------------------|--------------------|--------------------|
| **Tìm kiếm sản phẩm** | **Giỏ hàng** | **Tổng tiền & Thanh toán** |

---

### Cột trái: Tìm kiếm sản phẩm

- **Ô tìm kiếm lớn**:
  - **Placeholder**: `"Nhập mã Tivi, tên, hãng..."`
  - **Hỗ trợ**:
    - Phím **Enter**
    - **Quét mã vạch** (tự động thêm)
- **Nút "Tìm"** (màu xanh dương)

#### Danh sách gợi ý (Treeview nhỏ)
| Cột        | Nội dung ví dụ       |
|------------|----------------------|
| Mã         | `TV-SAM-001`         |
| Tên        | `Samsung Crystal 4K` |
| Hãng       | `Samsung`            |
| Giá bán    | `15,990,000 VNĐ`     |

- **Click** → thêm vào giỏ
- **Enter** → thêm nhanh
- **Tự động lọc** theo: **mã, tên, hãng**

---

### Cột giữa: Giỏ hàng (Treeview)

| Cột           | Nội dung ví dụ       | Căn chỉnh |
|---------------|----------------------|---------|
| **STT**       | `1`                  | Giữa    |
 kill| **Mã SP**     | `TV-SAM-001`         | Giữa    |
| **Tên SP**    | `Samsung 55" 4K`     | Trái    |
| **SL**        | `1` (có thể chỉnh)   | Giữa    |
| **Đơn giá**   | `15,990,000`         | Phải    |
| **Thành tiền**| `15,990,000`         | Phải    |
| **Xóa**       | Nút **X** đỏ         | Giữa    |

**Tính năng:**
- **Tự động cập nhật tổng tiền**
- **Click ô SL** → nhập số mới → **Enter** xác nhận
- **Phím mũi tên** → tăng/giảm SL
- **Phím Delete / Nút X** → xóa dòng
- **Kiểm tra tồn kho real-time**

---

### Cột phải: Tổng tiền & Thanh toán

| Thành phần             | Mô tả |
|------------------------|------|
| **Tổng tiền hàng**     | `15,990,000 VNĐ` |
| **Giảm giá (%)**       | Ô nhập + nút **Áp dụng** |
| **Giảm giá (VNĐ)**     | Ô nhập (ưu tiên nếu có) |
| **Tổng thanh toán**    | **Màu đỏ, font 18pt, bold** |
| **Tiền khách đưa**     | Ô nhập lớn |
| **Tiền thừa**          | **Tự động tính**, màu xanh lá |
| **Khách hàng**         | Combobox – tìm theo **SĐT/tên** |
| **Ghi chú**            | Ô nhỏ |
| **Nút "Thanh toán"**   | **Xanh lá, lớn, nổi bật** |
| **Nút "Hủy đơn"**      | **Đỏ** |

---

## 4. TÍNH NĂNG CHI TIẾT

### Tìm kiếm & thêm sản phẩm
1. Nhập từ khóa → **lọc tức thì** theo:
   - Mã Tivi
   - Tên Tivi
   - Hãng sản xuất
2. **Quét mã vạch** → thêm ngay vào giỏ
3. **Click hoặc Enter** → thêm sản phẩm:
   - SL mặc định = **1**
   - **Kiểm tra tồn kho**
   - **Cảnh báo đỏ** nếu **hết hàng**

---

### Chỉnh sửa giỏ hàng
- **Click ô SL** → nhập số → **Enter**
- **Phím ↑/↓** → tăng/giảm
- **Nút X / Delete** → xóa dòng
- **Tự động cập nhật**:
  - Thành tiền
  - Tổng tiền hàng
  - Tiền thừa

---

### Giảm giá linh hoạt
- **Nhập %** hoặc **số tiền**
- **Tự động tính lại tổng**
- **Admin mới được giảm > 10%** → yêu cầu **xác nhận mật khẩu admin**

---

### Chọn khách hàng
- Gõ **SĐT** → **tự động tìm**
- Hiển thị:
  - Tên khách
  - Loại KH (`Thường`, `VIP`, ...)
  - Điểm tích lũy
- **Tự động áp dụng ưu đãi** nếu là **VIP/Thân thiết**

---

### Thanh toán
1. Nhấn **"Thanh toán"**
2. **Popup xác nhận**:
   - Tóm tắt đơn hàng
   - Hỏi: **"In hóa đơn?"** (Có / Không)
3. Nếu **Có**:
   - Lưu vào CSDL:
     - `HoaDon`
     - `ChiTietHoaDon`
   - Cập nhật **tồn kho**
   - Cộng **điểm tích lũy**
   - **In hóa đơn tự động**
4. Nếu **Không**: Hủy đơn, xóa giỏ

---

## 5. IN HÓA ĐƠN (Tự động)

> **Hỗ trợ**:
> - In trực tiếp (máy in nhiệt)
> - Lưu PDF
> - Gửi email (nếu có)

---

## 6. XỬ LÝ LỖI & BẢO MẬT

| Trường hợp                  | Xử lý |
|-----------------------------|------|
| **Hết hàng**                | **Cảnh báo đỏ**, không cho thêm |
| **SL > tồn kho**            | **Tự động giới hạn**, thông báo |
| **Giảm giá > 10%**          | **Yêu cầu mật khẩu admin** |
| **Mất kết nối CSDL**        | **Lưu tạm vào local**, thử lại |
| **In lỗi**                  | **Thông báo + lưu PDF tự động** |
| **Hủy đơn**                 | Xóa giỏ, không lưu CSDL |

---

## 7. TỰ ĐỘNG HÓA

| Tính năng                   | Mô tả |
|-----------------------------|------|
| **Tổng tiền**               | Cập nhật **real-time** |
| **Tiền thừa**               | Tính ngay khi nhập tiền khách |
| **Mã hóa đơn**              | Tự tăng: `HD + YYYYMMDD + STT` |
| **Thời gian**               | Lấy từ hệ thống |
| **Tìm kiếm khách hàng**     | Gõ SĐT → tự động điền |
| **In hóa đơn**              | Tự động sau khi xác nhận |

---

## 8. GHI CHÚ PHÁT TRIỂN

- **Tối ưu phím tắt**:
  - `F1` → Tìm kiếm
  - `F2` → Thanh toán
  - `Esc` → Hủy đơn
- **Hỗ trợ quét mã vạch** (USB scanner)
- **Tích hợp máy in nhiệt 80mm**
- **Lưu log thao tác** (ai bán, khi nào, giảm giá bao nhiêu)
- **Backup tự động** khi mất kết nối

---

# TRA CỨU & QUẢN LÝ HÓA ĐƠN – README

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò                  | Quyền hạn |
|--------------------------|----------|
| **admin**                | **Toàn quyền**: Xem, Tìm, In lại, Xóa (nếu cần), Xuất Excel |
| **nhân viên bán hàng**   | **Xem + In lại** hóa đơn **do mình lập** |
| **nhân viên kho**        | **Không truy cập được trang này** |

> **Tất cả nhân viên bán hàng** đều có thể tra cứu hóa đơn của mình

---

## 2. GIAO DIỆN CHÍNH

### Tiêu đề trang
- **Text**: `TRA CỨU & QUẢN LÝ HÓA ĐƠN`
- **Font**: `Segoe UI`, **18pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Thông tin người dùng
- **Hiển thị**: `Xin chào, [Tên NV] (admin/nhân viên)`
- **Màu**:
  - Xanh lá: **admin**
  - Xanh dương: **nhân viên bán hàng**
- **Vị trí**: Góc trên bên **phải**

---

## 3. BỐ CỤC 2 PHẦN

| **Phần trên (30%)**       | **Phần dưới (70%)**           |
|----------------------------|-------------------------------|
| **Bộ lọc tìm kiếm**        | **Bảng danh sách hóa đơn**    |

---

### Phần trên: Bộ lọc tìm kiếm

> **LabelFrame**: `"Tìm kiếm hóa đơn"` – màu xanh, font 12pt, **Bold**

| Trường lọc               | Kiểu dữ liệu       | Ghi chú |
|--------------------------|--------------------|-------|
| **Mã hóa đơn**           | `Entry`            | Nhập chính xác |
| **Nhân viên**            | `Combobox`         | Admin: **tất cả NV**<br>NV bán hàng: **chỉ mình** |
| **Khách hàng (SĐT)**     | `Entry`            | Tự động tìm theo SĐT |
| **Ngày lập**             | `DateEntry` (từ - đến) | Chọn khoảng thời gian |
| **Tổng tiền (từ - đến)** | 2 `Entry`          | VNĐ, có dấu phẩy |
| **Trạng thái**           | `Combobox`         | `Đã thanh toán`, `Đã hủy` |

- **Nút "Tìm kiếm"** (màu xanh dương)
- **Nút "Xóa bộ lọc"** (màu đỏ) → tải lại toàn bộ

---

### Phần dưới: Bảng danh sách hóa đơn (Treeview)

| Cột               | Nội dung ví dụ               | Căn chỉnh |
|-------------------|------------------------------|---------|
| Mã HD             | `HD001234`                   | Giữa    |
| Ngày lập          | `16/11/2025 11:21`           | Giữa    |
| Nhân viên         | `Nguyễn Văn An`              | Trái    |
| Khách hàng        | `Trần Thị Lan`                | Trái    |
| SĐT               | `0901234567`                 | Giữa    |
| Số SP             | `2`                          | Giữa    |
| Tổng tiền         | `28,990,000 VNĐ`             | Phải    |
| Giảm giá          | `5%`                         | Giữa    |
| Thanh toán        | `27,540,500 VNĐ`             | Phải    |
| Trạng thái        | `Đã thanh toán`              | Giữa    |
| Hành động         | Nút **Xem** + **In**         | Giữa    |

**Tính năng bảng:**
- Cuộn dọc + ngang
- Dòng **striped** (xen kẽ màu)
- **Sắp xếp** khi click tiêu đề cột
- **Màu nền**:
  - **Xanh nhạt**: `Đã thanh toán`
  - **Đỏ nhạt**: `Đã hủy`
- **Hiển thị số kết quả**: `"Tìm thấy 128 hóa đơn"`

---

## 4. TÍNH NĂNG CHI TIẾT

### Tìm kiếm đa tiêu chí
- **Kết hợp nhiều điều kiện** (AND logic)
- **Tự động làm mới bảng** khi nhấn **Tìm kiếm**
- **Hiển thị số kết quả** ở góc dưới bảng

---

### Xem chi tiết hóa đơn
1. Nhấn nút **"Xem"** trên dòng
2. Mở **popup chi tiết**:

#### **Thông tin chung**
- Mã HD, Ngày giờ, Nhân viên, Khách hàng, SĐT

#### **Bảng sản phẩm**
| STT | Mã SP       | Tên sản phẩm         | SL | Đơn giá      | Thành tiền     |
|-----|-------------|----------------------|----|--------------|----------------|
| 1   | `TV-SAM-001`| `Samsung 55" 4K`     | 1  | 15,990,000   | 15,990,000     |
| 2   | `TV-LG-002` | `LG OLED 65"`        | 1  | 13,000,000   | 13,000,000     |

#### **Tổng cộng**
- **Tổng tiền hàng**: `28,990,000 VNĐ`
- **Giảm giá**: `5%` → `1,449,500 VNĐ`
- **TỔNG THANH TOÁN**: `27,540,500 VNĐ` (**in đậm**)
- **Tiền khách đưa**: `28,000,000 VNĐ`
- **Tiền thừa**: `459,500 VNĐ`
- **Ghi chú**: `Khách VIP, tặng kèm remote`

#### **Nút chức năng**
- **In lại** (xanh lá)
- **Đóng** (xám)

---

### In lại hóa đơn
- **Từ bảng**: Nhấn nút **"In"** → in ngay
- **Từ popup chi tiết**: Nhấn **"In lại"**
- **Nội dung in giống hệt lúc bán**:
  - Logo, thông tin cửa hàng
  - Bảng sản phẩm
  - Tổng tiền, giảm giá, thanh toán
  - QR code tra cứu online
  - Lời cảm ơn
- **Hỗ trợ**:
  - In trực tiếp (máy in nhiệt 80mm)
  - Lưu PDF
  - Gửi email (nếu có)

---

### Xuất báo cáo (chỉ admin)
- **Nút "Xuất Excel"** (màu xanh lá, góc phải)
- Xuất **toàn bộ kết quả tìm kiếm**
- **File tên**: `HoaDon_YYYYMMDD_HHMM.xlsx`
- **Nội dung**:
  - Tất cả cột trong bảng
  - Dòng tổng: **Tổng doanh thu**, **Tổng giảm giá**
- **Tự động mở thư mục lưu**

---

## 5. XỬ LÝ LỖI & BẢO MẬT

| Trường hợp                  | Xử lý |
|-----------------------------|------|
| **Không có kết quả**        | `"Không tìm thấy hóa đơn nào"` |
| **Lỗi in ấn**               | **Thông báo + tự động lưu PDF** |
| **Xóa hóa đơn (nếu cần)**   | **Chỉ admin** + **xác nhận 2 bước** |
| **Lỗi CSDL**                | **Thông báo chi tiết**, không làm treo ứng dụng |
| **Truy cập trái phép**      | **Ẩn bảng**, hiển thị `"Bạn không có quyền truy cập"` |

---

## 6. TỰ ĐỘNG HÓA

| Tính năng                   | Mô tả |
|-----------------------------|------|
| **Lọc theo NV**             | Tự động giới hạn nếu là nhân viên |
| **Tổng tiền**               | Định dạng `#,##0 VNĐ` |
| **Ngày giờ**                | Định dạng `dd/MM/yyyy HH:mm` |
| **QR Code**                 | Tự sinh link tra cứu: `https://hd.abc/[MaHD]` |
| **Log thao tác**            | Ghi lại: ai xem, ai in, khi nào |

---

## 7. GHI CHÚ PHÁT TRIỂN

- **Tối ưu phím tắt**:
  - `F3` → Tìm kiếm
  - `Ctrl + P` → In lại
  - `Ctrl + E` → Xuất Excel
- **Hỗ trợ in nhiệt 80mm**
- **Tích hợp QR code** (dùng `qrcode` library)
- **Phân trang** nếu > 1000 kết quả
- **Lưu bộ lọc gần nhất** (local storage)

---

# NHẬP HÀNG TỪ NHÀ CUNG CẤP – README

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò                | Quyền hạn |
|------------------------|----------|
| **admin**              | **Toàn quyền**: Nhập, Hủy phiếu, Xem lịch sử, In phiếu, Chiết khấu > 5% |
| **nhân viên kho**      | **Chỉ nhập hàng + in phiếu** |
| **nhân viên bán hàng** | **Không truy cập được trang này** |

> **Chỉ nhân viên kho và admin** được sử dụng

---

## 2. GIAO DIỆN CHÍNH

### Tiêu đề trang
- **Text**: `NHẬP HÀNG TỪ NHÀ CUNG CẤP`
- **Font**: `Segoe UI`, **18pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Thông tin người dùng
- **Hiển thị**: `Xin chào, [Tên NV] (admin/nhân viên kho)`
- **Màu**:
  - Xanh lá: **admin**
  - Tím: **nhân viên kho**
- **Vị trí**: Góc trên bên **phải**

---

## 3. BỐ CỤC 3 CỘT (Tối ưu thao tác)

| **Cột trái (30%)** | **Cột giữa (40%)** | **Cột phải (30%)** |
|--------------------|--------------------|--------------------|
| **Tìm kiếm sản phẩm** | **Chi tiết nhập hàng** | **Tổng tiền & Xác nhận** |

---

### Cột trái: Tìm kiếm sản phẩm

- **Ô tìm kiếm lớn**:
  - **Placeholder**: `"Nhập mã Tivi, tên, hãng..."`
  - **Hỗ trợ**:
    - Phím **Enter**
    - **Quét mã vạch** (tự động thêm)
- **Nút "Tìm"** (màu xanh dương)

#### Danh sách gợi ý (Treeview nhỏ)
| Cột               | Nội dung ví dụ       |
|-------------------|----------------------|
| Mã                | `TV-SAM-001`         |
| Tên               | `Samsung Crystal 4K` |
| Hãng              | `Samsung`            |
| Giá nhập hiện tại | `12,500,000 VNĐ`     |

- **Click** → thêm vào danh sách nhập
- **Enter** → thêm nhanh
- **Tự động lọc** theo: **mã, tên, hãng**

---

### Cột giữa: Chi tiết nhập hàng (Treeview)

| Cột           | Nội dung ví dụ       | Căn chỉnh |
|---------------|----------------------|---------|
| **STT**       | `1`                  | Giữa    |
| **Mã SP**     | `TV-SAM-001`         | Giữa    |
| **Tên SP**    | `Samsung 55" 4K`     | Trái    |
| **SL**        | `10` (có thể chỉnh)  | Giữa    |
| **Đơn giá**   | `12,500,000`         | Phải    |
| **Thành tiền**| `125,000,000`        | Phải    |
| **Xóa**       | Nút **X** đỏ         | Giữa    |

**Tính năng:**
- **Tự động cập nhật tổng tiền**
- **Click ô SL / Đơn giá** → nhập số mới → **Enter** xác nhận
- **Phím mũi tên** → tăng/giảm SL
- **Phím Delete / Nút X** → xóa dòng
- **Đơn giá mặc định** = giá nhập gần nhất

---

### Cột phải: Tổng tiền & Xác nhận

| Thành phần             | Mô tả |
|------------------------|------|
| **Nhà cung cấp**       | `Combobox` – tìm theo **tên/mã** |
| **Số phiếu nhập**      | Tự động: `PN251115001` |
| **Ngày nhập**          | Tự động: `16/11/2025` |
| **Tổng tiền hàng**     | `125,000,000 VNĐ` |
| **Chiết khấu (%)**     | Ô nhập + nút **Áp dụng** |
| **Chiết khấu (VNĐ)**   | Ô nhập (ưu tiên nếu có) |
| **Tổng thanh toán**    | **Màu đỏ, font 18pt, bold** |
| **Ghi chú**            | Ô nhỏ |
| **Nút "Xác nhận nhập"**| **Xanh lá, lớn, nổi bật** |
| **Nút "Hủy phiếu"**    | **Đỏ** |

---

## 4. TÍNH NĂNG CHI TIẾT

### Tìm kiếm & thêm sản phẩm
1. Nhập từ khóa → **lọc tức thì** theo:
   - Mã Tivi
   - Tên Tivi
   - Hãng sản xuất
2. **Quét mã vạch** → thêm ngay vào danh sách
3. **Click hoặc Enter** → thêm sản phẩm:
   - SL mặc định = **1**
   - Đơn giá mặc định = **giá nhập gần nhất**
   - **Cho phép chỉnh sửa SL & đơn giá**

---

### Chỉnh sửa danh sách nhập
- **Click ô SL / Đơn giá** → nhập số → **Enter**
- **Phím mũi tên** → tăng/giảm
- **Nút X / Delete** → xóa dòng
- **Tự động cập nhật**:
  - Thành tiền
  - Tổng tiền hàng

---

### Chọn nhà cung cấp
- Gõ **tên/mã** → **tự động tìm**
- Hiển thị:
  - Tên công ty
  - Mã số thuế
  - Người liên hệ, SĐT
- **Bắt buộc chọn** trước khi xác nhận

---

### Chiết khấu linh hoạt
- **Nhập %** hoặc **số tiền**
- **Tự động tính lại tổng**
- **Admin mới được chiết khấu > 5%** → yêu cầu **xác nhận mật khẩu admin**

---

### Xác nhận nhập hàng
1. Nhấn **"Xác nhận nhập"**
2. **Popup xác nhận**:
   - Tóm tắt phiếu nhập
   - Hỏi: **"In phiếu nhập?"** (Có / Không)
3. Nếu **Có**:
   - Lưu vào CSDL:
     - `PhieuNhap`
     - `ChiTietPhieuNhap`
   - Cập nhật **tồn kho**
   - Cập nhật **giá nhập mới** cho sản phẩm
   - **In phiếu nhập tự động**
4. Nếu **Không**: Hủy phiếu, xóa danh sách

---

## 5. IN PHIẾU NHẬP (Tự động)

> **Hỗ trợ**:
> - In trực tiếp (máy in nhiệt 80mm)
> - Lưu PDF

---

## 6. XỬ LÝ LỖI & BẢO MẬT

| Trường hợp                  | Xử lý |
|-----------------------------|------|
| **Sản phẩm không tồn tại**  | **Cảnh báo đỏ**, không cho thêm |
| **SL âm hoặc = 0**          | **Không cho nhập** |
| **Chiết khấu > 5%**         | **Yêu cầu mật khẩu admin** |
| **Chưa chọn NCC**           | **Không cho xác nhận** |
| **Mất kết nối CSDL**        | **Lưu tạm vào local**, thử lại |
| **In lỗi**                  | **Thông báo + lưu PDF tự động** |
| **Hủy phiếu**               | Xóa danh sách, không lưu CSDL |

---

## 7. TỰ ĐỘNG HÓA

| Tính năng                   | Mô tả |
|-----------------------------|------|
| **Số phiếu nhập**           | Tự tăng: `PN + YYMMDD + STT` |
| **Ngày nhập**               | Lấy từ hệ thống |
| **Tổng tiền**               | Cập nhật **real-time** |
| **Tìm kiếm NCC**            | Gõ tên/mã → tự động điền |
| **Giá nhập mặc định**       | Lấy từ phiếu nhập gần nhất |
| **In phiếu nhập**           | Tự động sau khi xác nhận |

---

# TRA CỨU & QUẢN LÝ PHIẾU NHẬP – README

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò                  | Quyền hạn |
|--------------------------|----------|
| **admin**                | **Toàn quyền**: Xem, Tìm, In lại, Xóa (nếu cần), Xuất Excel |
| **nhân viên kho**        | **Xem + In lại** phiếu **do mình lập** |
| **nhân viên bán hàng**   | **Không truy cập được trang này** |

> **Chỉ nhân viên kho và admin** được tra cứu phiếu nhập

---

## 2. GIAO DIỆN CHÍNH

### Tiêu đề trang
- **Text**: `TRA CỨU & QUẢN LÝ PHIẾU NHẬP`
- **Font**: `Segoe UI`, **18pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Thông tin người dùng
- **Hiển thị**: `Xin chào, [Tên NV] (admin/nhân viên kho)`
- **Màu**:
  - Xanh lá: **admin**
  - Tím: **nhân viên kho**
- **Vị trí**: Góc trên bên **phải**

---

## 3. BỐ CỤC 2 PHẦN

| **Phần trên (30%)**       | **Phần dưới (70%)**           |
|----------------------------|-------------------------------|
| **Bộ lọc tìm kiếm**        | **Bảng danh sách phiếu nhập** |

---

### Phần trên: Bộ lọc tìm kiếm

> **LabelFrame**: `"Tìm kiếm phiếu nhập"` – màu xanh, font 12pt, **Bold**

| Trường lọc                  | Kiểu dữ liệu       | Ghi chú |
|-----------------------------|--------------------|-------|
| **Số phiếu nhập**           | `Entry`            | Nhập chính xác |
| **Nhân viên nhập**          | `Combobox`         | Admin: **tất cả NV kho**<br>NV kho: **chỉ mình** |
| **Nhà cung cấp**            | `Combobox`         | Tìm theo **tên/mã** |
| **Ngày nhập**               | `DateEntry` (từ - đến) | Chọn khoảng thời gian |
| **Tổng tiền (từ - đến)**    | 2 `Entry`          | VNĐ, có dấu phẩy |
| **Sản phẩm trong phiếu**    | `Entry`            | Tìm phiếu **có chứa** mã/tên Tivi |

- **Nút "Tìm kiếm"** (màu xanh dương)
- **Nút "Xóa bộ lọc"** (màu đỏ) → tải lại toàn bộ

---

### Phần dưới: Bảng danh sách phiếu nhập (Treeview)

| Cột               | Nội dung ví dụ               | Căn chỉnh |
|-------------------|------------------------------|---------|
| Số phiếu          | `PN251115001`                | Giữa    |
| Ngày nhập         | `16/11/2025 11:21`           | Giữa    |
| Nhân viên         | `Lê Văn C`                   | Trái    |
| Nhà cung cấp      | `Công ty Samsung VN`         | Trái    |
| Số SP             | `3`                          | Giữa    |
| Tổng tiền         | `125,000,000 VNĐ`            | Phải    |
| Chiết khấu        | `2%`                         | Giữa    |
| Thanh toán        | `122,500,000 VNĐ`            | Phải    |
| Ghi chú           | `Lô Q4`                      | Trái    |
| Hành động         | Nút **Xem** + **In**         | Giữa    |

**Tính năng bảng:**
- Cuộn dọc + ngang
- Dòng **striped** (xen kẽ màu)
- **Sắp xếp** khi click tiêu đề cột
- **Màu nền**:
  - **Xanh nhạt**: `Đã nhập kho`
  - **Xám**: `Đã hủy` (nếu có)
- **Hiển thị số kết quả**: `"Tìm thấy 89 phiếu nhập"`

---

## 4. TÍNH NĂNG CHI TIẾT

### Tìm kiếm đa tiêu chí
- **Kết hợp nhiều điều kiện** (AND logic)
- **Tự động làm mới bảng** khi nhấn **Tìm kiếm**
- **Hiển thị số kết quả** ở góc dưới bảng

---

### Xem chi tiết phiếu nhập
1. Nhấn nút **"Xem"** trên dòng
2. Mở **popup chi tiết**:

#### **Thông tin chung**
- Số phiếu, Ngày giờ, Nhân viên, Nhà cung cấp, Mã số thuế

#### **Bảng sản phẩm**
| STT | Mã SP       | Tên sản phẩm         | SL | Đơn giá nhập | Thành tiền     |
|-----|-------------|----------------------|----|--------------|----------------|
| 1   | `TV-SAM-001`| `Samsung 55" 4K`     | 10 | 12,500,000   | 125,000,000    |

#### **Tổng cộng**
- **Tổng tiền hàng**: `125,000,000 VNĐ`
- **Chiết khấu**: `2%` → `2,500,000 VNĐ`
- **TỔNG THANH TOÁN**: `122,500,000 VNĐ` (**in đậm**)
- **Ghi chú**: `Nhập lô mới Q4`

#### **Nút chức năng**
- **In lại** (xanh lá)
- **Đóng** (xám)

---

### In lại phiếu nhập
- **Từ bảng**: Nhấn nút **"In"** → in ngay
- **Từ popup chi tiết**: Nhấn **"In lại"**
- **Nội dung in giống hệt lúc nhập**:
  - Logo, thông tin cửa hàng
  - Bảng sản phẩm
  - Tổng tiền, chiết khấu, thanh toán
  - QR code tra cứu online
  - Chữ ký: Người lập + Nhà cung cấp

---

### Xuất báo cáo (chỉ admin)
- **Nút "Xuất Excel"** (màu xanh lá, góc phải)
- Xuất **toàn bộ kết quả tìm kiếm**
- **File tên**: `PhieuNhap_YYYYMMDD_HHMM.xlsx`
- **Nội dung**:
  - Tất cả cột trong bảng
  - Dòng tổng: **Tổng nhập hàng**, **Tổng chiết khấu**
- **Tự động mở thư mục lưu**

---

## 5. XỬ LÝ LỖI & BẢO MẬT

| Trường hợp                  | Xử lý |
|-----------------------------|------|
| **Không có kết quả**        | `"Không tìm thấy phiếu nhập nào"` |
| **Lỗi in ấn**               | **Thông báo + tự động lưu PDF** |
| **Xóa phiếu (nếu cần)**     | **Chỉ admin** + **xác nhận 2 bước** |
| **Lỗi CSDL**                | **Thông báo chi tiết**, không làm treo ứng dụng |
| **Truy cập trái phép**      | **Ẩn bảng**, hiển thị `"Bạn không có quyền truy cập"` |

---

## 6. TỰ ĐỘNG HÓA

| Tính năng                   | Mô tả |
|-----------------------------|------|
| **Lọc theo NV**             | Tự động giới hạn nếu là nhân viên kho |
| **Tổng tiền**               | Định dạng `#,##0 VNĐ` |
| **Ngày giờ**                | Định dạng `dd/MM/yyyy HH:mm` |
| **QR Code**                 | Tự sinh link tra cứu: `https://pn.abc/[SoPhieu]` |
| **Log thao tác**            | Ghi lại: ai xem, ai in, khi nào |

---

# BẢNG ĐIỀU KHIỂN & BÁO CÁO DOANH THU – README

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò                  | Tab Thống Kê | Tab Báo Cáo |
|--------------------------|--------------|-------------|
| **admin**                | **Toàn quyền** | **Toàn quyền** |
| **nhân viên bán hàng**   | **Không truy cập** | **Không truy cập** |
| **nhân viên kho**        | **Không truy cập** | **Không truy cập** |

> **Chỉ admin** được vào cả hai trang

---

## 2. TAB THỐNG KÊ – DASHBOARD TỔNG QUAN

### Tiêu đề trang
- **Text**: `BẢNG ĐIỀU KHIỂN - THỐNG KÊ DOANH SỐ`
- **Font**: `Segoe UI`, **20pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Bộ lọc thời gian (trên cùng)

> **LabelFrame**: `"Chọn khoảng thời gian"` – màu xanh, font 12pt, **Bold**

| Lọc nhanh              | Kiểu |
|------------------------|------|
| **Hôm nay** / **Hôm qua** | Radio |
| **7 ngày gần nhất**    | Nút |
| **Tháng này** / **Tháng trước** | Nút |
| **Quý này**            | Nút |
| **Tùy chỉnh**          | 2 `DateEntry` (Từ - Đến) |

- **Nút "Cập nhật"** (xanh dương) → làm mới toàn bộ

---

### BỐ CỤC DASHBOARD (4 phần)

| **Trên trái** | **Trên phải** | **Dưới trái** | **Dưới phải** |
|---------------|---------------|---------------|---------------|
| **Tổng quan** | **Biểu đồ doanh thu** | **Top sản phẩm** | **Hiệu suất nhân viên** |

---

#### 1. Tổng quan (4 ô thẻ)

| Thẻ               | Nội dung ví dụ        | Màu nền |
|-------------------|-----------------------|--------|
| **Doanh thu**     | `1,285,990,000 VNĐ`   | Xanh lá |
| **Số hóa đơn**    | `128`                 | Xanh dương |
| **Số sản phẩm bán** | `256`               | Cam |
| **Lợi nhuận**     | `485,500,000 VNĐ`     | Tím |

- **So sánh kỳ trước**: ↑12.5% / ↓5.3%

---

#### 2. Biểu đồ doanh thu
- **Loại**: Cột (ngày) / Đường (tuần/tháng)
- **Trục X**: Thời gian
- **Trục Y**: Doanh thu (VNĐ)
- **Chức năng**:
  - Zoom, kéo
  - Tooltip khi hover
  - **Chuyển đổi**: Doanh thu / Số lượng / Lợi nhuận
- **Nút "Xuất ảnh"** (PNG)

---

#### 3. Top 10 sản phẩm bán chạy
> **Treeview + Mini bar chart**

| Xếp hạng | Mã SP       | Tên SP             | SL bán | Doanh thu        | Thanh % |
|---------|-------------|--------------------|--------|------------------|--------|
| 1       | `TV-SAM-001`| `Samsung 55" 4K`   | 45     | `715,500,000`    | ████████ 78% |
| 2       | `TV-LG-002` | `LG OLED 65"`      | 38     | `494,000,000`    | ██████ 68% |

- **Top 3**: Màu **vàng, bạc, đồng**
- **Click dòng** → mở chi tiết sản phẩm

---

#### 4. Hiệu suất nhân viên
> **Bảng xếp hạng**

| NV             | Số HD | Doanh thu       | TB/HD         | Đánh giá |
|----------------|-------|-----------------|---------------|----------|
| Nguyễn Văn A   | 42    | `485,000,000`   | `11,547,619`  | ★★★★☆ |
| Trần Thị B     | 35    | `398,500,000`   | `11,385,714`  | ★★★★☆ |

- **Sắp xếp mặc định**: Doanh thu giảm dần
- **Lọc theo ca làm việc** (gợi ý)

---

### BÁO CÁO CHI TIẾT (Tab con)

| Tab         | Nội dung |
|-------------|--------|
| **Doanh thu** | Theo ngày/tuần/tháng/quý |
| **Tồn kho**   | Tivi: Tồn, Giá trị, Trạng thái (Cảnh báo < 5) |
| **Nhập hàng** | Tổng nhập, theo NCC, theo sản phẩm |
| **Lợi nhuận** | Doanh thu – Giá vốn – Chi phí |

- **Mỗi tab có nút**:
  - **Xuất Excel**
  - **In PDF**

---

### XUẤT BÁO CÁO

| Nút             | Chức năng |
|-----------------|---------|
| **Xuất Excel**  | Toàn bộ dữ liệu lọc → `.xlsx` |
| **In báo cáo**  | PDF A4: Logo, tiêu đề, biểu đồ, bảng |
| **Lưu mẫu**     | Lưu bộ lọc để dùng lại |

---

## 3. TAB BÁO CÁO – CHI TIẾT CHUYÊN NGHIỆP

### Tiêu đề trang
- **Text**: `BÁO CÁO DOANH THU & HOẠT ĐỘNG KINH DOANH`
- **Font**: `Segoe UI`, **20pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

### Bộ lọc báo cáo (trên cùng)

> **LabelFrame**: `"Cấu hình báo cáo"` – màu xanh, font 12pt, **Bold**

| Trường lọc             | Kiểu |
|------------------------|------|
| **Loại báo cáo**       | `Combobox`:  
  - Doanh thu theo ngày  
  - Doanh thu theo nhân viên  
  - Doanh thu theo sản phẩm  
  - Nhập hàng theo NCC  
  - Tồn kho hiện tại  
  - Lợi nhuận theo tháng  
  - Hóa đơn theo trạng thái |
| **Khoảng thời gian**   | 2 `DateEntry` (Từ - Đến) |
| **Nhân viên**          | `Combobox` |
| **Nhà cung cấp**       | `Combobox` |
| **Sản phẩm**           | `Entry` (mã/tên) |

- **Nút "Xem báo cáo"** (xanh dương)
- **Nút "Làm mới"** (xám)

---

### BỐ CỤC BÁO CÁO

| **Phần trên (60%)**       | **Phần dưới (40%)**           |
|----------------------------|-------------------------------|
| **Bảng dữ liệu chi tiết**  | **Tổng hợp & Hành động**      |

---

#### Bảng dữ liệu (Treeview) – Tự động thay đổi theo loại báo cáo

**Ví dụ: Doanh thu theo ngày**

| Ngày         | Số HD | SL SP | Doanh thu      | Giảm giá | Thanh toán     | Lợi nhuận     |
|--------------|-------|-------|----------------|----------|----------------|---------------|
| 15/11/2025   | 12    | 24    | `285,990,000`  | 5%       | `271,690,500`  | `108,500,000` |

**Ví dụ: Doanh thu theo nhân viên**

| NV             | Số HD | SL SP | Doanh thu      | TB/HD         | % Tổng |
|----------------|-------|-------|----------------|---------------|--------|
| Nguyễn Văn A   | 42    | 86    | `485,000,000`  | `11,547,619`  | 37.8%  |

- **Tổng cộng** ở dòng cuối (in đậm)
- **Sắp xếp** khi click cột

---

#### Tổng hợp & Hành động

| Thành phần             | Mô tả |
|------------------------|------|
| **Tổng quan nhanh**    |  
  - Tổng doanh thu: `1,285,990,000`  
  - Tổng hóa đơn: `128`  
  - Tổng lợi nhuận: `485,500,000` |
| **Nút hành động**      |  
  - **Xuất Excel**  
  - **In PDF**  
  - **Lưu mẫu báo cáo** |

---

### XUẤT & IN BÁO CÁO

#### **Xuất Excel**
- **File**: `BaoCao_DoanThu_20251115.xlsx`
- **Nội dung**:
  - Tiêu đề báo cáo
  - Bộ lọc đã chọn
  - Bảng dữ liệu đầy đủ
  - Dòng tổng cộng
- **Tự động mở thư mục**

#### **In PDF**
- **Định dạng**: A4 dọc
- **Nội dung**:
  - **Logo cửa hàng**, tên, địa chỉ
  - **Tiêu đề báo cáo**
  - **Thời gian lập**: `16/11/2025 11:30`
  - **Người lập**: `Admin`
  - **Bộ lọc**
  - **Bảng dữ liệu** (căn chỉnh đẹp)
  - **Tổng cộng**
  - **Chữ ký điện tử**
- **Xem trước** trước khi in

---

## 4. TÍNH NĂNG NỔI BẬT

| Tính năng                     | Mô tả |
|-------------------------------|------|
| **Tự động cập nhật**          | Mỗi 5 phút |
| **Cảnh báo thông minh**       |  
  - Tồn kho < 5 → **màu đỏ**  
  - Doanh thu giảm > 20% → **hộp thoại**  
  - Nhân viên vắng → **icon cảnh báo** |
| **Giao diện responsive**      | PC + Tablet |
| **Dark mode**                 | Gợi ý (toggle) |
| **Lưu mẫu báo cáo**           | Dùng lại nhanh |

---

## 5. XỬ LÝ LỖI & BẢO MẬT

| Trường hợp                  | Xử lý |
|-----------------------------|------|
| **Không có dữ liệu**        | `"Chưa có dữ liệu trong khoảng thời gian này"` |
| **Lỗi biểu đồ**             | Tự fallback về bảng |
| **Lỗi xuất file**           | Thông báo + thử lại |
| **Quyền truy cập**          | Kiểm tra nghiêm ngặt, **log hành động** |

---

## 6. GHI CHÚ PHÁT TRIỂN

- **Biểu đồ**: Dùng `matplotlib` / `Plotly` (embedded)
- **Xuất Excel**: `pandas.to_excel()`
- **PDF**: `reportlab` hoặc `weasyprint`
- **Tự động cập nhật**: `threading` + `after()`
- **Phân quyền**: Kiểm tra ở **menu**, **route**, **backend**
- **Log**: `INSERT INTO LogThaoTac (NguoiDung, HanhDong, ThoiGian)`

---

**ĐÃ HOÀN THIỆN – SẴN SÀNG TRIỂN KHAI**

---

### Hướng dẫn sử dụng file:
1. Tạo 2 file:
   - `README_THONG_KE.md`
   - `README_BAO_CAO.md`
2. Dán nội dung tương ứng
3. Mở bằng **VS Code** → Xem trước: **Ctrl + Shift + V**
4. Đẩy lên GitHub → hiển thị **chuẩn, đẹp, chuyên nghiệp**

**HOÀN TẤT!**  
**Thống Kê + Báo Cáo** – **Mạnh mẽ, Trực quan, Chuyên nghiệp, Dành cho Quản lý**

### XỬ LÝ LỖI & BẢO MẬT

| Trường hợp | Xử lý |
|----------|------|
| **Không có dữ liệu** | `"Không có dữ liệu phù hợp với bộ lọc"` |
| **Lỗi xuất file** | Thông báo + cho thử lại |
| **Lỗi in** | Tự động lưu PDF dự phòng |
| **Quyền truy cập** | Kiểm tra nghiêm ngặt, ghi log |

---

# QUẢN LÝ TÀI KHOẢN HỆ THỐNG – README

## 1. PHÂN QUYỀN TRUY CẬP

| Vai trò                     | Quyền hạn |
|-----------------------------|----------|
| **admin**                   | **Toàn quyền**: Thêm, Sửa, Xóa, Tìm kiếm, Xem bảng, Lưu |
| **nhân viên (bán hàng/kho)**| **Chỉ xem + đổi mật khẩu của chính mình** |

> **Chỉ admin** thấy bảng danh sách và các nút thao tác  
> **Nhân viên** chỉ thấy **form cá nhân**, không thấy bảng, không thấy nút Thêm/Xóa

---

## 2. GIAO DIỆN CHÍNH

### Tiêu đề trang
- **Text**: `QUẢN LÝ TÀI KHOẢN HỆ THỐNG`
- **Font**: `Segoe UI`, **16pt**, **Bold**
- **Màu**: `#0D47A1`
- **Căn giữa** trên cùng

---

## 3. GIAO DIỆN CHO ADMIN

### Khu vực tìm kiếm
- **Label**: `"Tìm kiếm:"` + biểu tượng kính lúp  
- **Ô nhập**: Rộng, hỗ trợ phím **Enter**  
- **Placeholder**: `"Nhập tên đăng nhập..."`  
- **Nút**:
  - **Tìm** (màu xanh dương)
  - **Hủy** (màu đỏ) → xóa điều kiện, tải lại dữ liệu

---

### Form nhập liệu

> **Tiêu đề**: `"Thông tin tài khoản"` – màu xanh, font 12pt, **Bold**

| Trường               | Kiểu dữ liệu       | Kiểm tra bắt buộc |
|----------------------|--------------------|-------------------|
| **Tên đăng nhập**    | `Entry`            | Bắt buộc, **không trùng**, 3–20 ký tự, chỉ **chữ/số/gạch dưới** |
| **Mật khẩu**         | `Entry` (show='*')  | Bắt buộc, **≥ 6 ký tự**, **có chữ + số** |

---

### Bảng danh sách tài khoản (Treeview)

| Cột               | Nội dung ví dụ       | Căn chỉnh |
|-------------------|----------------------|---------|
| Tên đăng nhập     | `admin`              | Giữa    |
| Mật khẩu          | `******` (ẩn)        | Giữa    |

**Tính năng bảng:**
- Cuộn dọc + ngang
- Dòng **striped** (xen kẽ màu)
- **Click chọn dòng** → tự động điền form
- **Sắp xếp mặc định** theo **Tên đăng nhập**

---

### Nút chức năng (chỉ admin)

| Nút         | Màu         | Chức năng |
|-------------|-------------|---------|
| **Thêm**    | Vàng        | Kiểm tra → thêm vào bảng + `ds_them` |
| **Sửa**     | Cam         | Cập nhật dòng → `ds_sua` |
| **Xóa**     | Đỏ          | Xác nhận → xóa + `ds_xoa` |
| **Làm mới** | Xanh dương  | Hủy buffer → tải lại CSDL |
| **Lưu**     | Xanh lá     | **Transaction**: Xóa → Thêm → Sửa |

---

## 4. GIAO DIỆN CHO NHÂN VIÊN (user != admin)

> **Ẩn hoàn toàn**:
> - Ô tìm kiếm
> - Bảng danh sách
> - Nút **Thêm**, **Xóa**, **Làm mới**, **Lưu**

> **Chỉ hiển thị**:
> - Tiêu đề trang
> - Form nhập liệu:
>   - **Tên đăng nhập**: Tự động điền + **disabled**
>   - **Mật khẩu**: Có thể thay đổi
> - Nút **Sửa** (chỉ đổi mật khẩu)

---

## 5. TÍNH NĂNG CHI TIẾT

### Click chọn dòng → Tự động điền form (chỉ admin)
Khi người dùng **bấm vào bất kỳ dòng nào trên bảng**:

1. Lấy dữ liệu từ dòng được chọn
2. Điền tự động vào form:
   - `Tên đăng nhập` → `txt_ten`
   - `Mật khẩu` → `txt_mk` (**hiển thị thật**, không ẩn)
3. **Tự động focus** về ô **Mật khẩu**
4. Sẵn sàng **Sửa** hoặc **Xóa** mà không cần nhấn nút khác

---

### Thêm tài khoản (chỉ admin)
1. Kiểm tra **tất cả trường bắt buộc**
2. **Tên đăng nhập**: không trùng, định dạng hợp lệ (regex)
3. **Mật khẩu**: ≥ 6 ký tự, có chữ + số
4. Thêm dòng vào bảng
5. Thêm vào `ds_them = [(TenDangNhap, MatKhau)]`
6. Xóa form + thông báo thành công

---

### Sửa tài khoản

#### **Admin**
1. Phải **chọn dòng**
2. Kiểm tra **Tên đăng nhập mới không trùng** (ngoại trừ chính nó)
3. Cập nhật dòng trên bảng
4. Nếu trong `ds_them` → cập nhật
5. Nếu không → thêm vào `ds_sua = [(TenDangNhap_moi, MatKhau, TenDangNhap_cu)]`
6. Xóa form + thông báo

#### **Nhân viên**
1. **Không cần chọn dòng**
2. Chỉ đổi **mật khẩu**
3. Lưu vào `ds_sua = [(MatKhau_moi, TenDangNhap)]`
4. Thông báo thành công

---

### Xóa tài khoản (chỉ admin)
1. Phải chọn dòng
2. **Không cho xóa tài khoản đang đăng nhập**
3. Xác nhận: `"Xóa tài khoản [Tên đăng nhập]?"`
4. Xóa dòng khỏi bảng
5. Nếu trong `ds_them` → xóa khỏi danh sách
6. Nếu không → thêm `TenDangNhap` vào `ds_xoa`
7. Xóa form + thông báo

---

### Lưu thay đổi (Transaction an toàn)
- **Nút**: `"Lưu"` – màu xanh lá, chữ trắng, font đậm
- **Khi nhấn**:
  1. Hộp thoại: *"Bạn có chắc muốn lưu tất cả thay đổi?"*
  2. Nếu **Có**:
     - Mở **transaction**
     - **Bước 1**: Xóa các tài khoản trong `ds_xoa`
     - **Bước 2**: Thêm các tài khoản trong `ds_them`
     - **Bước 3**: Cập nhật các tài khoản trong `ds_sua`
     - **Thành công**: Commit, tải lại dữ liệu, xóa buffer, thông báo *"Lưu thành công!"*
     - **Lỗi** (trùng tên, ràng buộc...): `rollback()`, giữ buffer, thông báo lỗi chi tiết
  3. Nếu **Không**: Hủy thao tác

---

## 6. CẤU TRÚC BUFFER THAY ĐỔI

| Danh sách   | Cấu trúc |
|-------------|---------|
| `ds_them`   | `(TenDangNhap, MatKhau)` |
| `ds_sua`    | `(TenDangNhap_moi, MatKhau, TenDangNhap_cu)` **hoặc** `(MatKhau, TenDangNhap)` |
| `ds_xoa`    | `(TenDangNhap,)` |

> **Không lưu CSDL** cho đến khi nhấn **Lưu**

---

## 7. XỬ LÝ LỖI & BẢO MẬT

| Trường hợp                        | Thông báo |
|-----------------------------------|----------|
| **Tên đăng nhập trùng**           | `"Tên đăng nhập đã tồn tại!"` |
| **Tên đăng nhập không hợp lệ**    | `"3–20 ký tự, chỉ chữ, số, gạch dưới"` |
| **Mật khẩu yếu**                  | `"Mật khẩu phải ≥ 6 ký tự, có chữ và số"` |
| **Xóa tài khoản đang đăng nhập**  | `"Không thể xóa tài khoản đang đăng nhập!"` |
| **Lỗi CSDL**                      | `rollback()` + `"Lỗi hệ thống, thay đổi đã được hủy"` |
| **Mật khẩu hiển thị**             | Chỉ hiện khi **chọn dòng** (admin) |

---

## 8. HÀM TẢI DỮ LIỆU (`load_data()`)
Gọi khi:
- Vào trang
- Sau khi **Lưu thành công**
- Nhấn **Làm mới**
- Nhấn **Hủy tìm kiếm**

---