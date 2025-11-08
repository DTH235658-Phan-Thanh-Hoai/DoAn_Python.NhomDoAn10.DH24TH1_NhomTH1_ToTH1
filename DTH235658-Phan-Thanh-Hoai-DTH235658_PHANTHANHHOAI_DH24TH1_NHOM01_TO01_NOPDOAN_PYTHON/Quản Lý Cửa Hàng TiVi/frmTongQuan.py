import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


class TongQuan(tk.Frame):
    def __init__(self, parent, controller, conn, user):
        super().__init__(parent)
        self.conn = conn
        self.configure(bg="#f5f9ff")

        lbl_title = tk.Label(
            self,
            text="TRANG TỔNG QUAN HỆ THỐNG",
            font=("Segoe UI", 16, "bold"),
            fg="#003366",
            bg="#f5f9ff",
        )
        lbl_title.pack(pady=15)

        frame_cards = tk.Frame(self, bg="#f5f9ff")
        frame_cards.pack(pady=10)

        self.cards = {
            "nv": self.create_card(frame_cards, "👤 Tổng nhân viên", "0"),
            "kh": self.create_card(frame_cards, "👤 Tổng khách hàng", "0"),
            "hsx": self.create_card(frame_cards, "🏭 Hãng sản xuất", "0"),
            "ncc": self.create_card(frame_cards, "🏢 Nhà cung cấp", "0"),
            "sp": self.create_card(frame_cards, "📺 Sản phẩm", "0"),
            "pn": self.create_card(frame_cards, "📦 Phiếu nhập hàng", "0"),
        }

        self.load_data()

        self.frame_chart = tk.Frame(self, bg="#f5f9ff")
        self.frame_chart.pack(pady=20)

        self.ve_bieu_do()

    def ve_bieu_do(self):
        try:
            cursor = self.conn.cursor()

            query = """
                SELECT 
                    MONTH(NgayBan) AS Thang,
                    SUM(TongTien) AS DoanhThu
                FROM HoaDonBan
                WHERE TrangThai = N'Đã thanh toán'
                GROUP BY MONTH(NgayBan)
                ORDER BY Thang;
            """

            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()

            thang = [row[0] for row in data]
            doanh_thu = [float(row[1]) for row in data]

            if not thang:
                thang = list(range(1, 12 + 1))
                doanh_thu = [0] * 12

            def format_tien(x, pos):
                return f"{int(x):,}".replace(",", ".")

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.bar(thang, doanh_thu)

            ax.yaxis.set_major_formatter(FuncFormatter(format_tien))

            ax.set_title("Biểu đồ doanh thu theo tháng", fontsize=12, fontweight="bold")
            ax.set_xlabel("Tháng", fontsize=11)
            ax.set_ylabel("Doanh thu (VNĐ)", fontsize=11)
            ax.set_xticks(range(1, 13))

            fig.tight_layout()

            for widget in self.frame_chart.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.frame_chart)
            canvas.draw()
            canvas.get_tk_widget().pack()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải biểu đồ:\n{e}")

    def create_card(self, parent, title, value):
        card = tk.Frame(
            parent, bg="#d6eaff", width=180, height=100, relief="ridge", bd=2
        )
        card.pack(side="left", padx=10, pady=5)
        card.pack_propagate(False)

        lbl_title = tk.Label(
            card, text=title, font=("Segoe UI", 10, "bold"), fg="#003366", bg="#d6eaff"
        )
        lbl_title.pack(pady=(10, 0))

        lbl_value = tk.Label(
            card, text=value, font=("Segoe UI", 20, "bold"), fg="#002b80", bg="#d6eaff"
        )
        lbl_value.pack(pady=(5, 0))

        return lbl_value

    def load_data(self):
        try:
            cursor = self.conn.cursor()

            queries = {
                "nv": "SELECT COUNT(*) FROM NhanVien",
                "kh": "SELECT COUNT(*) FROM KHACHHANG",
                "hsx": "SELECT COUNT(*) FROM HangSanXuat",
                "ncc": "SELECT COUNT(*) FROM NhaCungCap",
                "sp": "SELECT COUNT(*) FROM Tivi",
                "pn": "SELECT COUNT(*) FROM PhieuNhapHang",
            }

            for key, query in queries.items():
                cursor.execute(query)
                count = cursor.fetchone()[0]
                self.cards[key].config(text=str(count))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu tổng quan:\n{e}")
