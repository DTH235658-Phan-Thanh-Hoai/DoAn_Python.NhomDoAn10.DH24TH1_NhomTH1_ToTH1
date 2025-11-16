import tkinter as tk
from tkinter import ttk
import ctypes
import pyodbc
import App
import os
import sys
from PIL import Image, ImageTk

# === BẢNG MÀU ===
PRIMARY_COLOR = "#378cfc"
SECONDARY_COLOR = "#1565C0"
ACCENT_COLOR = "#42A5F5"
HIGHLIGHT_COLOR = "#BBDEFB"
TEXT_COLOR = "white"

# Hien: LAPTOP-IFECMD9V
# Hoai: DESKTOP-LJVV0KQ

# === LÀM NÉT GIAO DIỆN ===
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ĐĂNG NHẬP HỆ THỐNG QUẢN LÝ NHÂN SỰ")
        self.center_window(850, 580)
        self.resizable(False, False)
        self.configure(bg="white")

        # ==== CHUỖI KẾT NỐI SQL ====
        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LAPTOP-IFECMD9V;"
            "DATABASE=QLTV;"
            "Trusted_Connection=yes;")
        
        # === LẤY ĐƯỜNG DẪN CHO ẢNH === 
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        image_dir = os.path.join(base_dir, "images")

        icon_path = os.path.join(image_dir, 'icon_tivi.ico')
        self.iconbitmap(icon_path)

        # === FRAME TRÁI (WELCOME) ===
        left_frame = tk.Frame(self, width=300, height=500)
        left_frame.pack(side="left", fill="y")
        
        # --- XỬ LÝ VÀ ĐẶT HÌNH ẢNH NỀN ---
        image_path = os.path.join(image_dir, "nen_python.png")
           
        original_image = Image.open(image_path)
        resized_image = original_image.resize((300, 580), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
            
        background_label = tk.Label(left_frame, image=self.bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
            

        # === FRAME PHẢI (FORM ĐĂNG NHẬP) ===
        right_frame = tk.Frame(self, bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # --- Căn giữa toàn bộ ---
        right_frame.columnconfigure(0, weight=1)

        # --- Avatar ---
        user_icon_path = os.path.join(image_dir, "user.png") 
        
        original_user_image = Image.open(user_icon_path)
        resized_user_image = original_user_image.resize((120, 120), Image.Resampling.LANCZOS) 
        self.user_image_tk = ImageTk.PhotoImage(resized_user_image)

        user_avatar_label = tk.Label(right_frame, image=self.user_image_tk, bg="white")
        user_avatar_label.grid(row=0, column=0, pady=(30, 10))


        # --- SIGNIN ---
        tk.Label(right_frame, text="SIGNIN", bg="white", fg=PRIMARY_COLOR, font=("Segoe UI", 18, "bold")).grid(row=1, column=0, pady=(0, 30))

        # --- Tên đăng nhập ---
        user_frame = tk.Frame(right_frame, bg="white")
        user_frame.grid(row=2, column=0, pady=10)
        tk.Label(user_frame, text="👤", bg="white", fg=PRIMARY_COLOR, font=("Segoe UI", 12)).pack(side="left", padx=5)

        self.txt_user = ttk.Entry(user_frame, width=30, font=("Segoe UI", 11))
        self.txt_user.pack(side="left")
        self.txt_user.focus()
        self.txt_user.bind("<Return>", self.dangnhap)

        # --- Mật khẩu ---
        pass_frame = tk.Frame(right_frame, bg="white")
        pass_frame.grid(row=3, column=0, pady=10)
        tk.Label(pass_frame, text="🔒", bg="white", fg=PRIMARY_COLOR, font=("Segoe UI", 12)).pack(side="left", padx=5)

        self.txt_password = ttk.Entry(pass_frame, width=27, font=("Segoe UI", 11), show="●")
        self.txt_password.pack(side="left")
        self.txt_password.bind("<Return>", self.dangnhap)

        # Nút hiện/ẩn mật khẩu
        self.show_pass = False
        self.eye_btn = tk.Button(pass_frame, text="👁", bg="white", bd=0, cursor="hand2", command=self.toggle_password)
        self.eye_btn.pack(side="left", padx=3)

        # --- Nút đăng nhập & thoát ---
        btn_frame = tk.Frame(right_frame, bg="white")
        btn_frame.grid(row=4, column=0, pady=40)

        self.btn_login = tk.Button(btn_frame, text="Đăng nhập", bg=PRIMARY_COLOR, fg="white", font=("Segoe UI", 11, "bold"), width=12, pady=6, bd=0, activebackground=HIGHLIGHT_COLOR, cursor="hand2", command=self.dangnhap)
        self.btn_login.pack(side="left", padx=15)

        self.btn_exit = tk.Button(btn_frame, text="Thoát", bg="#E53935", fg="white", font=("Segoe UI", 11, "bold"), width=12, pady=6, bd=0, activebackground="#B71C1C", cursor="hand2", command=self.destroy)
        self.btn_exit.pack(side="left", padx=15)

        # --- Nhãn thông báo ---
        self.lbl_error = tk.Label(right_frame, text="", fg="red", bg="white", font=("Segoe UI", 10))
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

    def dangnhap(self, event=None):
        user = self.txt_user.get().strip()
        pw = self.txt_password.get().strip()

        if not user or not pw:
            self.lbl_error.config(text="Vui lòng nhập tên đăng nhập và mật khẩu!")
            return

        cursor = self.conn.cursor()
        cursor.execute("SELECT TenDangNhap, MatKhau FROM TaiKhoan WHERE TenDangNhap = ? AND MatKhau = ?", (user, pw),)

        row = cursor.fetchone()

        if row:
            self.mo_form(user)
        else:
            self.lbl_error.config(text="Sai tài khoản hoặc mật khẩu!")

    def mo_form(self, user):
        self.destroy()
        App.App(user)

if __name__ == "__main__":
    app = Login()
    app.mainloop()
