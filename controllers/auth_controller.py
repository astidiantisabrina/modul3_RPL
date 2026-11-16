import tkinter.messagebox as messagebox
from models.user_model import UserModel
from views.login_view import LoginView
from controllers.buku_controller import BukuController


class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = None
        self.user_login = None        # data user yang berhasil login
        self.logout_diminta = False   # True jika pengguna menekan tombol Logout

    # ------------------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------------------
    def _buat_login_view(self):
        self.view = LoginView()
        self.view.btn_login.configure(command=self.proses_login)
        # Tekan Enter untuk login
        self.view.bind("<Return>", lambda event: self.proses_login())

    def proses_login(self):
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        user = self.model.autentikasi(username, password)

        if user:
            messagebox.showinfo(
                "Login Berhasil",
                f"Selamat datang, {user['username']} ({user['role']})!"
            )
            self.user_login = user
            # Tutup jendela Login. Alur dilanjutkan oleh run()
            self.view.destroy()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    # ------------------------------------------------------------------
    # LOGOUT
    # ------------------------------------------------------------------
    def proses_logout(self):
        # Dipanggil oleh BukuView setelah jendela perpustakaan ditutup
        self.logout_diminta = True

    # ------------------------------------------------------------------
    # ALUR UTAMA
    # ------------------------------------------------------------------
    def run(self):
        while True:
            self.user_login = None
            self.logout_diminta = False

            # 1. Tampilkan jendela Login
            self._buat_login_view()
            self.view.mainloop()

            # Jendela Login ditutup tanpa login berhasil -> keluar aplikasi
            if not self.user_login:
                break

            # 2. Buka jendela Perpustakaan sesuai role pengguna
            app_utama = BukuController(
                user_role=self.user_login["role"],
                on_logout=self.proses_logout
            )
            app_utama.run()

            # 3. Jika bukan karena Logout (jendela ditutup dengan tombol X) -> keluar
            if not self.logout_diminta:
                break