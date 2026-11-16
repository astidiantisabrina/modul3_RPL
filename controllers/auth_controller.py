import traceback
import tkinter.messagebox as messagebox
from models.user_model import UserModel
from views.login_view import LoginView
from controllers.buku_controller import BukuController


class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.view.btn_login.configure(command=self.proses_login)

    def proses_login(self):
        username = self.view.entry_username.get()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        user = self.model.autentikasi(username, password)

        if user:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {user['username']} ({user['role']})!")

            # Sembunyikan jendela Login lebih dulu (belum dihancurkan)
            self.view.withdraw()

            try:
                # Siapkan jendela Utama Perpustakaan dengan mengirimkan role pengguna
                # on_logout dipanggil saat tombol Logout di BukuView diklik
                app_utama = BukuController(
                    user_role=user['role'],
                    on_logout=self.kembali_ke_login
                )
            except Exception:
                # Jika jendela utama gagal dibuat, jendela Login ditampilkan lagi
                # dan penyebab errornya ditampilkan agar mudah dicari
                detail = traceback.format_exc()
                print(detail)
                self.view.deiconify()
                messagebox.showerror(
                    "Gagal Membuka Halaman Utama",
                    detail[-800:]
                )
                return

            # Jendela utama berhasil dibuat -> tutup jendela Login dan tampilkan
            self.view.destroy()
            app_utama.run()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    def kembali_ke_login(self):
        # Dipanggil setelah jendela perpustakaan ditutup lewat tombol Logout.
        # Membuat ulang jendela Login (LoginView tidak diubah sama sekali).
        self.view = LoginView()
        self.view.btn_login.configure(command=self.proses_login)
        self.view.mainloop()

    def run(self):
        self.view.mainloop()