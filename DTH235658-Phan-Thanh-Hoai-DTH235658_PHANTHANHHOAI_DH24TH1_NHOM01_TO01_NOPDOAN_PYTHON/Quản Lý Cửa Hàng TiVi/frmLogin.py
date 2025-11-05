import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import pyodbc
import App

# === BẢNG MÀU ===
PRIMARY_COLOR = "#0D47A1"
SECONDARY_COLOR = "#1565C0"
ACCENT_COLOR = "#42A5F5"
HIGHLIGHT_COLOR = "#BBDEFB"
TEXT_COLOR = "white"

# === LÀM NÉT GIAO DIỆN ===
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ĐĂNG NHẬP HỆ THỐNG QUẢN LÝ NHÂN SỰ")
        self.center_window(850, 500)
        self.resizable(True, True)
        self.configure(bg="white")

        # ==== CHUỖI KẾT NỐI SQL ====
        self.conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-LJVV0KQ;"
            "DATABASE=QLTV;"
            "Trusted_Connection=yes;"
        )

        # === FRAME TRÁI (WELCOME) ===
        left_frame = tk.Frame(self, bg=PRIMARY_COLOR, width=300, height=500)
        left_frame.pack(side="left", fill="y")

        tk.Label(
            left_frame,
            text="Welcome",
            bg=PRIMARY_COLOR,
            fg="white",
            font=("Segoe UI", 22, "bold"),
        ).place(relx=0.5, rely=0.35, anchor="center")
        tk.Label(
            left_frame,
            text="Please Sign in to Continue",
            bg=PRIMARY_COLOR,
            fg="white",
            font=("Segoe UI", 11),
        ).place(relx=0.5, rely=0.42, anchor="center")

        # === FRAME PHẢI (FORM ĐĂNG NHẬP) ===
        right_frame = tk.Frame(self, bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # --- Căn giữa toàn bộ ---
        right_frame.columnconfigure(0, weight=1)

        # --- Avatar ---
        avatar_canvas = tk.Canvas(
            right_frame, width=140, height=140, bg="white", highlightthickness=0
        )
        avatar_canvas.create_oval(
            10, 10, 130, 130, fill=HIGHLIGHT_COLOR, outline=PRIMARY_COLOR, width=3
        )
        avatar_canvas.create_text(
            72, 65, text="👤", font=("Segoe UI Emoji", 50), fill=PRIMARY_COLOR
        )
        avatar_canvas.grid(row=0, column=0, pady=(30, 10))

        # --- SIGNIN ---
        tk.Label(
            right_frame,
            text="SIGNIN",
            bg="white",
            fg=PRIMARY_COLOR,
            font=("Segoe UI", 18, "bold"),
        ).grid(row=1, column=0, pady=(0, 30))

        # --- Tên đăng nhập ---
        user_frame = tk.Frame(right_frame, bg="white")
        user_frame.grid(row=2, column=0, pady=10)
        tk.Label(
            user_frame, text="👤", bg="white", fg=PRIMARY_COLOR, font=("Segoe UI", 12)
        ).pack(side="left", padx=5)

        self.txt_user = ttk.Entry(user_frame, width=30, font=("Segoe UI", 11))
        self.txt_user.pack(side="left")

        # --- Mật khẩu ---
        pass_frame = tk.Frame(right_frame, bg="white")
        pass_frame.grid(row=3, column=0, pady=10)
        tk.Label(
            pass_frame, text="🔒", bg="white", fg=PRIMARY_COLOR, font=("Segoe UI", 12)
        ).pack(side="left", padx=5)

        self.txt_password = ttk.Entry(
            pass_frame, width=27, font=("Segoe UI", 11), show="*"
        )
        self.txt_password.pack(side="left")

        # Nút hiện/ẩn mật khẩu
        self.show_pass = False
        self.eye_btn = tk.Button(
            pass_frame,
            text="👁",
            bg="white",
            bd=0,
            cursor="hand2",
            command=self.toggle_password,
        )
        self.eye_btn.pack(side="left", padx=3)

        # --- Nút đăng nhập & thoát ---
        btn_frame = tk.Frame(right_frame, bg="white")
        btn_frame.grid(row=4, column=0, pady=40)

        self.btn_login = tk.Button(
            btn_frame,
            text="Đăng nhập",
            bg=PRIMARY_COLOR,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=12,
            pady=6,
            bd=0,
            activebackground=HIGHLIGHT_COLOR,
            cursor="hand2",
            command=self.dangnhap,
        )
        self.btn_login.pack(side="left", padx=15)

        self.btn_exit = tk.Button(
            btn_frame,
            text="Thoát",
            bg="#E53935",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=12,
            pady=6,
            bd=0,
            activebackground="#B71C1C",
            cursor="hand2",
            command=self.destroy,
        )
        self.btn_exit.pack(side="left", padx=15)

        # --- Nhãn thông báo ---
        self.lbl_error = tk.Label(
            right_frame, text="", fg="red", bg="white", font=("Segoe UI", 10)
        )
        self.lbl_error.grid(row=5, column=0)

    def center_window(self, w=850, h=500):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def toggle_password(self):
        if self.show_pass:
            self.txt_password.config(show="*")
            self.eye_btn.config(text="👁")
        else:
            self.txt_password.config(show="")
            self.eye_btn.config(text="🚫")
        self.show_pass = not self.show_pass

    def dangnhap(self):
        user = self.txt_user.get().strip()
        pw = self.txt_password.get().strip()

        if not user or not pw:
            self.lbl_error.config(text="Vui lòng nhập tên đăng nhập và mật khẩu!")
            return

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT TenDangNhap, MatKhau FROM TaiKhoan WHERE TenDangNhap = ? AND MatKhau = ?",
            (user, pw),
        )

        row = cursor.fetchone()

        if row:
            self.mo_form(user)
        else:
            self.lbl_error.config(text="Sai tài khoản hoặc mật khẩu!")

    def mo_form(self, user):
        self.destroy()
        main_app = App.App(user)
        main_app.mainloop()


if __name__ == "__main__":
    app = Login()
    app.mainloop()
