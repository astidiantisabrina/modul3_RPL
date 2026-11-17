
import customtkinter as ctk


class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pengaturan tampilan aplikasi
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Login - Sistem Perpustakaan")
        self.geometry("380x350")
        self.resizable(False, False)

        # Mengatur posisi jendela di tengah layar
        lebar = 380
        tinggi = 350

        x = (self.winfo_screenwidth() - lebar) // 2
        y = (self.winfo_screenheight() - tinggi) // 2

        self.geometry(f"{lebar}x{tinggi}+{x}+{y}")

        # Frame utama
        self.frame = ctk.CTkFrame(
            self,
            corner_radius=12
        )
        self.frame.pack(
            pady=20,
            padx=20,
            fill="both",
            expand=True
        )

        # Judul login
        self.label_judul = ctk.CTkLabel(
            self.frame,
            text="LOGIN SISTEM",
            font=("Arial", 20, "bold")
        )
        self.label_judul.pack(pady=(25, 20))

        # Input username
        self.entry_username = ctk.CTkEntry(
            self.frame,
            placeholder_text="Username",
            height=38,
            corner_radius=8
        )
        self.entry_username.pack(
            pady=10,
            padx=25,
            fill="x"
        )

        # Input password
        self.entry_password = ctk.CTkEntry(
            self.frame,
            placeholder_text="Password",
            show="*",
            height=38,
            corner_radius=8
        )
        self.entry_password.pack(
            pady=10,
            padx=25,
            fill="x"
        )

        # Tombol login
        self.btn_login = ctk.CTkButton(
            self.frame,
            text="Masuk",
            height=40,
            corner_radius=8,
            fg_color="blue",
            hover_color="#0000AA"
        )
        self.btn_login.pack(
            pady=22,
            padx=25,
            fill="x"
        )

        # Enter untuk menjalankan login
        self.bind(
            "<Return>",
            lambda event: self.btn_login.invoke()
        )

        # Fokus awal pada username
        self.entry_username.focus_set()
