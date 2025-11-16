<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00c6ff,100:0072ff&height=230&section=header&text=Ứng%20Dụng%20Quản%20Lý%20Cửa%20Hàng%20Tivi&fontSize=38&fontColor=ffffff&fontAlignY=40" />
</p><div align="center">
  <p>
    Đồ án môn học Chuyên đề Python (COS525) tại Trường Đại học An Giang (AGU).
  </p>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Project-Quản%20Lý%20Cửa%20Hàng%20Tivi-378cfc?style=for-the-badge" alt="Project Badge">
  <img src="https://img.shields.io/badge/Python-3.x-1565C0?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/UI-Tkinter-42A5F5?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/Database-SQL%20Server-1565C0?style=for-the-badge&logo=microsoftsqlserver" alt="SQL Server">
</p>

---

## 🚀 Giới thiệu

Đây là đồ án môn học **Chuyên đề Python (COS525)** tại **Trường Đại học An Giang (AGU) - Khoa Công nghệ Thông tin**. Ứng dụng này là một hệ thống phần mềm quản lý nội bộ (desktop-based) được phát triển bằng **Python**, sử dụng giao diện **Tkinter** và cơ sở dữ liệu **SQL Server**.

> **Mục tiêu chính**: Tối ưu hóa quy trình quản lý bán lẻ thiết bị điện tử, tự động hóa các nghiệp vụ cơ bản (nhập, xuất, tồn kho) và các quy trình phức tạp (bảo hành, thống kê lợi nhuận), đồng thời cung cấp giao diện trực quan, hiện đại và bảo mật.

---

## ✨ Tính năng chính

Hệ thống được xây dựng trên kiến trúc module hóa chặt chẽ, phân quyền rõ ràng cho hai vai trò **Admin** và **Nhân viên**.

### 1. 🔐 Hệ thống & Bảo mật
* **Form Đăng nhập:** Giao diện xác thực người dùng.
* **Phân quyền động:** Ứng dụng tự động ẩn/hiện các module chức năng dựa trên vai trò (`admin` hay `nhân viên`).
* **Bảo mật mật khẩu:** Mật khẩu người dùng được mã hóa bằng **SHA-256** trước khi lưu và so sánh trong CSDL.

### 2. 🗃️ Quản lý Danh mục (CRUD)
* **Quản lý Sản phẩm (Tivi):** Quản lý chi tiết thông tin Tivi, hỗ trợ tải và lưu trữ **ảnh sản phẩm (BLOB)** vào CSDL.
* **Quản lý Hãng & NCC:** Quản lý danh mục Hãng sản xuất và Nhà cung cấp.
* **Quản lý Khách hàng:** Quản lý thông tin khách hàng.
* **Quản lý Nhân viên:** Quản lý hồ sơ nhân viên, hỗ trợ **ảnh đại diện (BLOB)**.

### 3. 💼 Nghiệp vụ Kinh doanh
* **Bán hàng:** Giao diện tạo hóa đơn bán hàng, tự động tính tổng tiền.
* **Quản lý Hóa đơn:**
    * Xem danh sách, tìm kiếm, và xem chi tiết hóa đơn.
    * Thực hiện **Thanh toán** (tự động trừ tồn kho) hoặc **Hủy hóa đơn**.
* **Nhập hàng:**
    * Giao diện tạo phiếu nhập hàng từ nhà cung cấp.
    * Admin **Duyệt phiếu** (tự động cộng tồn kho) hoặc **Hủy phiếu**.
* **Quản lý Bảo hành:** Theo dõi thông tin bảo hành của các sản phẩm đã bán.

### 4. 📊 Báo cáo & Thống kê
* **Trang Tổng quan (Dashboard):** Giao diện trực quan hiển thị các chỉ số nhanh (tổng NV, KH, SP,...) và **biểu đồ doanh thu** theo năm (sử dụng `matplotlib`).
* **Thống kê Doanh thu:** Phân tích tổng doanh thu và **lợi nhuận gộp** (Doanh thu - Giá vốn) theo khoảng thời gian tùy chọn.
* **Báo cáo Sản phẩm:** Thống kê chi tiết số lượng bán, doanh thu, lợi nhuận và **tỷ lệ bán chạy (%)** của từng sản phẩm.

### 5. 🖨️ Tiện ích
* **In ấn chuyên nghiệp:** Tích hợp thư viện `python-docx` để **xuất Hóa đơn, Phiếu nhập, và Phiếu bảo hành** ra file **Word (.docx)** theo mẫu định sẵn.
* **Giao diện hiện đại:** Sử dụng ảnh nền, icon, và các widget `tkcalendar` (DateEntry) để tăng trải nghiệm người dùng.

---

## 🛠️ Công nghệ sử dụng
* **Ngôn ngữ chính:** Python
* **Giao diện (GUI):** Tkinter
* **Cơ sở dữ liệu:** Microsoft SQL Server
* **Kết nối CSDL:** `pyodbc`
* **Xử lý ảnh:** `Pillow (PIL)`
* **Trực quan hóa (Biểu đồ):** `matplotlib`
* **In ấn (Word):** `python-docx`
* **Chọn ngày (Lịch):** `tkcalendar`
* **Bảo mật:** `hashlib` (cho SHA-256)

---

## 👨‍💻 Tác giả & Phân công
Dự án được thực hiện bởi nhóm sinh viên Khoa Công nghệ Thông tin - AGU:

| STT | Họ tên thành viên | Mã số sinh viên | Công việc thực hiện | Tỷ lệ đóng góp (%) |
|:---:|:---|:---|:---|:---:|
| 1 | **Phan Thanh Hoài** | `DTH235658` | Thiết kế giao diện, form Nhập hàng và Bán hàng,<br>tab Nhập hàng, tab Bán hàng, form Bán Hàng và Hóa đơn,<br>tab Bán hàng, tab Hóa đơn, kết nối CSDL, form App,<br>kiểm thử, sửa lỗi, nội dung báo cáo, file word. | 50% |
| 2 | **Nguyễn Văn Hiền** | `DTH235651` | Thiết kế CSDL, form Quản lý sản phẩm, tab Tivi,<br>tab Nhà cung cấp, tab Hãng sản xuất, tab Bảo hành,<br>form Quản lý nhân viên, form Quản lý khách hàng,<br>form Login, form Hệ thống, form Thống kê và báo cáo,<br>tab Báo cáo sản phẩm, tab Thống kê doanh thu. | 50% |


---

## ⚙️ Cài đặt và Chạy ứng dụng

### 1. Yêu cầu môi trường
* **Python 3.x**
* **Microsoft SQL Server**
* **Microsoft ODBC Driver 17 for SQL Server** (Bắt buộc để `pyodbc` kết nối).

### 2. Cài đặt thư viện
Clone repository này và cài đặt các thư viện cần thiết qua pip:
```bash
pip install pyodbc
pip install tkcalendar
pip install pillow
pip install python-docx
pip install matplotlib
