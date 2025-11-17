<<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00c6ff,100:0072ff&height=230&section=header&text=ỨNG%20DỤNG%20QUẢN%20LÝ%20CỬA%20HÀNG%20TIVI&fontSize=38&fontColor=ffffff&fontAlignY=40" />
</p>

<br>

<p align="center">
  <img src="https://img.shields.io/badge/Project-Quản%20Lý%20Cửa%20Hàng%20Tivi-007bff?style=for-the-badge&logo=buffer&logoColor=white" />
  <img src="https://img.shields.io/badge/Nhóm-10-0ba5e6?style=for-the-badge&logo=people&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Tkinter-GUI-00a8ff?style=for-the-badge&logo=windowsterminal&logoColor=white" />
  <img src="https://img.shields.io/badge/SQL%20Server-Database-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" />
  <img src="https://img.shields.io/badge/Word-Export-2b579a?style=for-the-badge&logo=microsoftword&logoColor=white" />
  <img src="https://img.shields.io/badge/Matplotlib-Charts-013243?style=for-the-badge&logo=plotly&logoColor=white" />
</p>

---

## **GIỚI THIỆU**

<p align="center">
  <img src="https://img.shields.io/badge/Môn%20học-Chuyên%20Đề%20Python%20(COS525)-007bff?style=for-the-badge&logo=book&logoColor=white" />
  <img src="https://img.shields.io/badge/Trường-Đại%20Học%20An%20Giang%20(AGU)-28a745?style=for-the-badge&logo=school&logoColor=white" />
  <img src="https://img.shields.io/badge/Khoa-CNTT-17a2b8?style=for-the-badge&logo=code&logoColor=white" />
</p>

Ứng dụng **Quản lý Cửa hàng Tivi** là một phần mềm **desktop-based** được phát triển bằng  
✔ **Python**  
✔ **Tkinter (GUI)**  
✔ **SQL Server (CSDL chính)**  

Phần mềm mô phỏng đầy đủ quy trình nghiệp vụ vận hành một cửa hàng tivi thực tế — từ quản lý sản phẩm, khách hàng, hóa đơn, nhập hàng cho đến bảo hành và thống kê doanh thu.

<div align="center">
  <img src="https://img.shields.io/badge/Mục%20tiêu-Dự%20án%20học%20phần-ffc107?style=for-the-badge&logo=target&logoColor=black" />
</div>

### **MỤC TIÊU ĐỒ ÁN**

- Tối ưu hóa quy trình quản lý bán lẻ thiết bị điện tử  
- Tự động hóa nghiệp vụ **nhập – xuất – tồn kho**  
- Quản lý hóa đơn & bảo hành thông minh  
- Cung cấp UI trực quan, dễ sử dụng  
- Tăng cường bảo mật dữ liệu (SHA-256, phân quyền)  
- Tích hợp thống kê doanh thu – lợi nhuận theo thời gian  
- Mô phỏng hệ thống quản lý thực tế dành cho doanh nghiệp nhỏ

> **Đồ án hướng đến khả năng ứng dụng thực tế**, đồng thời là cơ hội giúp sinh viên AGU rèn luyện kỹ năng lập trình Python, giao diện Tkinter và thiết kế CSDL chuyên nghiệp.

---
## Tính năng chính

Hệ thống được xây dựng theo kiến trúc module hóa, có phân quyền rõ ràng cho hai vai trò **Admin** và **Nhân viên**.  
Dưới đây là các nhóm chức năng nổi bật:

---

### <img src="https://img.shields.io/badge/-Hệ%20thống%20%26%20Bảo%20mật-0a84ff?style=for-the-badge&logo=shield&logoColor=white" />

- **Form Đăng nhập**: Giao diện xác thực người dùng.  
- **Phân quyền động**: Ẩn/hiện menu & chức năng theo vai trò (`admin` / `nhân viên`).  
- **Mã hóa mật khẩu SHA-256**: Tăng cường bảo mật tài khoản.  

---

### <img src="https://img.shields.io/badge/-Quản%20lý%20Danh%20mục%20(CRUD)-34c759?style=for-the-badge&logo=data&logoColor=white" />

- **Tivi**: Lưu trữ thông tin, hình ảnh (BLOB), nhà cung cấp, hãng sản xuất.  
- **Hãng & Nhà cung cấp**: Quản lý danh mục, ràng buộc logic dữ liệu.  
- **Khách hàng**: Quản lý hồ sơ khách hàng mua hàng.  
- **Nhân viên**: Thông tin + ảnh đại diện (BLOB).  

---

### <img src="https://img.shields.io/badge/-Nghiệp%20vụ%20Kinh%20doanh-ff9f0a?style=for-the-badge&logo=briefcase&logoColor=white" />

#### **Bán hàng**
- Giao diện tạo hóa đơn bán hàng.  
- Tự động tính tổng tiền theo số lượng & giá bán.  
- Trừ tồn kho khi thanh toán.  

#### **Quản lý hóa đơn**
- Tìm kiếm theo ngày, nhân viên, khách hàng.  
- Xem chi tiết hóa đơn.  
- Hủy hóa đơn (rollback tồn kho).  

#### **Nhập hàng**
- Tạo phiếu nhập từ nhà cung cấp.  
- **Admin duyệt phiếu** → tự động cộng tồn kho.  
- Hủy phiếu → rollback tồn kho.  

#### **Bảo hành**
- Tự động tính hạn bảo hành.  
- Theo dõi chi tiết từng sản phẩm đã bán.  

---

### <img src="https://img.shields.io/badge/-Báo%20cáo%20%26%20Thống%20kê-af52de?style=for-the-badge&logo=bar-chart&logoColor=white" />

- **Dashboard tổng quan**: Tổng số NV, KH, SP, hóa đơn,…  
- **Biểu đồ doanh thu theo năm** (matplotlib).  
- **Phân tích doanh thu – lợi nhuận gộp** theo khoảng thời gian.  
- **Báo cáo sản phẩm**: Số lượng bán, doanh thu, lợi nhuận, tỷ lệ bán chạy (%).  

---

### <img src="https://img.shields.io/badge/-Tiện%20ích%20Hỗ%20trợ-5856d6?style=for-the-badge&logo=sparkles&logoColor=white" />

- **Xuất file Word (Hóa đơn, Phiếu nhập, Phiếu bảo hành)** bằng `python-docx`.  
- **Giao diện hiện đại**: icon, màu nền, layout thân thiện.  
- **tkcalendar (DateEntry)** giúp chọn ngày chính xác & nhanh chóng.

---
## **SƠ ĐỒ QUAN HỆ**
<p align="center">
  <img src="https://img.shields.io/badge/Database-SQL%20Server-cc2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" />
  <img src="https://img.shields.io/badge/Model-ERD%20Design-0ba5e6?style=for-the-badge&logo=databricks&logoColor=white" />
  <img src="https://img.shields.io/badge/Normalization-3NF-success?style=for-the-badge&logo=checkmarx&logoColor=white" />
  <img src="https://raw.githubusercontent.com/DTH235658-Phan-Thanh-Hoai/DoAn_Python.NhomDoAn10.DH24TH1_NhomTH1_ToTH1/master/diagram%20tivi.jpg" alt="ERD Diagram" width="800"> 
</p>
</p> <p align="center">
  <b> Sơ đồ quan hệ - Hệ thống Quản lý cửa hàng Tivi </b>
</p>

## **CÔNG NGHỆ SỬ DỤNG**

<p align="center">

  <!-- PYTHON -->
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />

  <!-- TKINTER -->
  <img src="https://img.shields.io/badge/Tkinter-GUI-00a8ff?style=for-the-badge&logo=windowsterminal&logoColor=white" />

  <!-- SQL SERVER -->
  <img src="https://img.shields.io/badge/SQL%20Server-Database-b7312f?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" />

  <!-- PYODBC -->
  <img src="https://img.shields.io/badge/pyodbc-Connector-6c5ce7?style=for-the-badge&logo=plug&logoColor=white" />

  <!-- PIL -->
  <img src="https://img.shields.io/badge/Pillow-Image%20Processing-009688?style=for-the-badge&logo=imagej&logoColor=white" />

  <!-- MATPLOTLIB -->
  <img src="https://img.shields.io/badge/Matplotlib-Chart-013243?style=for-the-badge&logo=chartdotjs&logoColor=white" />

  <!-- PYTHON DOCX -->
  <img src="https://img.shields.io/badge/python--docx-File%20Export-2b579a?style=for-the-badge&logo=microsoftword&logoColor=white" />

  <!-- TKCALENDAR -->
  <img src="https://img.shields.io/badge/tkcalendar-Date%20Picker-34c759?style=for-the-badge&logo=googlecalendar&logoColor=white" />

  <!-- HASHLIB -->
  <img src="https://img.shields.io/badge/hashlib-SHA--256%20Security-ff9f0a?style=for-the-badge&logo=secure&logoColor=white" />

</p>

## **TÁC GIẢI VÀ PHÂN CÔNG**

<p align="center">
  <img src="https://img.shields.io/badge/Team-Nhóm%2010-0ba5e6?style=for-the-badge&logo=people&logoColor=white" />
</p>

Dự án được thực hiện bởi **Nhóm 10**.  
Mỗi thành viên chịu trách nhiệm các module riêng, kết hợp thành một hệ thống hoàn chỉnh.

---

### **THÀNH VIÊN THỰC HIỆN**

<table align="center">
  <tr>
    <th style="text-align:center;">STT</th>
    <th style="text-align:center;">Thành viên</th>
    <th style="text-align:center;">MSSV</th>
    <th style="text-align:center;">Công việc</th>
    <th style="text-align:center;">Đóng góp</th>
  </tr>

  <tr>
    <td align="center">1</td>
    <td><b>Phan Thanh Hoài</b></td>
    <td align="center"><code>DTH235658</code></td>
    <td>
      Thiết kế giao diện • Form Nhập hàng • Form Bán hàng •  
      Tab Nhập hàng • Tab Bán hàng • Form Hóa đơn •  
      Kết nối CSDL • Form App • Kiểm thử & sửa lỗi •  
      Viết báo cáo • Xuất file Word.
    </td>
    <td align="center"><b>50%</b></td>
  </tr>

  <tr>
    <td align="center">2</td>
    <td><b>Nguyễn Văn Hiền</b></td>
    <td align="center"><code>DTH235651</code></td>
    <td>
      Thiết kế CSDL • Form Quản lý sản phẩm •  
      Tab Tivi • Tab Hãng • Tab Nhà cung cấp •  
      Tab Bảo hành • Form Nhân viên • Form Khách hàng •  
      Form Login • Hệ thống • Thống kê & Báo cáo •  
      Báo cáo sản phẩm • Thống kê doanh thu.
    </td>
    <td align="center"><b>50%</b></td>
  </tr>

</table>

## **CÀI ĐẶT VÀ CHẠY ỨNG DỤNG**

Để chạy được ứng dụng, bạn cần chuẩn bị môi trường gồm Python, SQL Server và các thư viện liên quan.

---

### <img src="https://img.shields.io/badge/Yêu%20cầu%20môi%20trường-00a8ff?style=for-the-badge&logo=gear&logoColor=white" />

- **Python 3.x**
- **Microsoft SQL Server**
- **ODBC Driver 17 for SQL Server** (bắt buộc cho `pyodbc`)
- Hệ điều hành đề xuất: **Windows 10/11**

---

### <img src="https://img.shields.io/badge/Cài%20đặt%20thư%20viện-34c759?style=for-the-badge&logo=pypi&logoColor=white" />

Chạy lệnh sau để cài đặt đầy đủ thư viện:

▼bash
pip install pyodbc pillow python-docx matplotlib tkcalendar
▼

---

## 💖 LỜI CẢM ƠN

<div align="center">
  <table width="85%" style="border-radius: 15px; padding: 20px; border: 1px solid #e4e4e4; background: #fafafa;">
    <tr>
      <td>

<p align="center">
  <img src="https://img.shields.io/badge/Trân%20trọng%20cảm%20ơn-ThS.%20Nguyễn%20Ngọc%20Minh-e63946?style=for-the-badge&logo=heart&logoColor=white" />
</p>

<p align="center">
  Nhóm <b>10</b> xin gửi lời cảm ơn chân thành và sâu sắc đến<br>
  <b>ThS. Nguyễn Ngọc Minh</b>, giảng viên phụ trách môn<br>
  <b>Chuyên đề Python (COS525)</b>.
</p>

<p align="center">
  Thầy đã tận tình hướng dẫn, hỗ trợ và tạo điều kiện thuận lợi trong suốt quá trình thực hiện đồ án.
  Những nhận xét và góp ý quý báu của Thầy đã giúp nhóm nâng cao hiểu biết về:
</p>

<ul>
  <li>Phương pháp xây dựng một ứng dụng Python hoàn chỉnh</li>
  <li>Thiết kế và tối ưu hóa giao diện Tkinter</li>
  <li>Phân tích và mô hình hóa cơ sở dữ liệu SQL Server</li>
  <li>Tư duy lập trình theo hướng dự án thực tế</li>
</ul>

<p align="center">
  Nhờ sự dẫn dắt tận tâm của Thầy, nhóm đã có thể hoàn thiện đồ án một cách nghiêm túc, khoa học và hiệu quả.
</p>

<p align="center">
  <b>Xin gửi đến Thầy lời cảm ơn trân trọng nhất!</b>
</p>
  </table>
</div>

---
