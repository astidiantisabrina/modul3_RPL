
import traceback
import tkinter.messagebox as messagebox

from models.user_model import UserModel
from views.login_view import LoginView
from controllers.buku_controller import BukuController


# ASTI DIANTI SABRINA_F5212530104


class AuthController:

    def __init__(self):

        # Inisialisasi model dan halaman login
        self.model = UserModel()
        self.view = LoginView()

        # Menyimpan controller halaman utama
        self.app_utama = None

        # Hubungkan tombol login
        self.view.btn_login.configure(
            command=self.proses_login
        )

    # =========================================
    # PROSES LOGIN
    # =========================================

    def proses_login(self):

        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get()

        # Validasi input
        if not username or not password:

            messagebox.showwarning(
                "Peringatan",
                "Username dan Password wajib diisi!",
                parent=self.view
            )
            return

        try:

            # Periksa koneksi database
            if not self.model.conn:

                messagebox.showerror(
                    "Koneksi Gagal",
                    "Tidak dapat terhubung ke database. "
                    "Pastikan MySQL sudah berjalan.",
                    parent=self.view
                )
                return

            # Proses autentikasi
            user = self.model.autentikasi(
                username,
                password
            )

            # Jika username atau password salah
            if not user:

                messagebox.showerror(
                    "Login Gagal",
                    "Username atau Password salah!",
                    parent=self.view
                )

                self.view.entry_password.delete(0, "end")
                self.view.entry_password.focus()

                return

            # Ambil informasi pengguna
            user_role = user["role"]
            nama_user = user["username"]

            # Tampilkan pesan berhasil
            messagebox.showinfo(
                "Login Berhasil",
                f"Selamat datang, {nama_user} ({user_role})!",
                parent=self.view
            )

            # Nonaktifkan tombol login sementara
            self.view.btn_login.configure(
                state="disabled"
            )

            # Sembunyikan halaman login
            # Jangan menghancurkan root utama
            self.view.withdraw()

            # Buka halaman utama setelah dialog selesai
            self.view.after(
                100,
                lambda: self.buka_halaman_utama(user_role)
            )

        except Exception:

            detail = traceback.format_exc()

            print("ERROR LOGIN:")
            print(detail)

            messagebox.showerror(
                "Kesalahan Login",
                detail[-1000:],
                parent=self.view
            )

    # =========================================
    # MEMBUKA HALAMAN UTAMA
    # =========================================

    def buka_halaman_utama(self, user_role):

        try:

            # Membuat halaman utama menggunakan
            # LoginView sebagai master/root
            self.app_utama = BukuController(
                master=self.view,
                user_role=user_role,
                on_logout=self.kembali_ke_login
            )

            # Tampilkan jendela utama perpustakaan
            self.app_utama.run()

        except Exception:

            detail = traceback.format_exc()

            print("ERROR MEMBUKA HALAMAN UTAMA:")
            print(detail)

            # Tampilkan kembali halaman login
            if self.view.winfo_exists():

                self.view.deiconify()

                self.view.btn_login.configure(
                    state="normal"
                )

            messagebox.showerror(
                "Gagal Membuka Halaman Utama",
                "Halaman perpustakaan gagal dibuka.\n\n"
                + detail[-1000:],
                parent=self.view
            )

            self.app_utama = None

    # =========================================
    # KEMBALI KE LOGIN SETELAH LOGOUT
    # =========================================

    def kembali_ke_login(self):

        # Hapus referensi controller halaman utama
        self.app_utama = None

        # Tampilkan kembali jendela login
        if self.view.winfo_exists():

            self.view.deiconify()
            self.view.lift()
            self.view.focus_force()

            # Bersihkan password sebelumnya
            self.view.entry_password.delete(0, "end")

            # Aktifkan kembali tombol login
            self.view.btn_login.configure(
                state="normal"
            )

            self.view.entry_username.focus()

    # =========================================
    # MENJALANKAN APLIKASI
    # =========================================

    def run(self):

        # Hanya satu mainloop untuk seluruh aplikasi
        self.view.mainloop()


# =============================================
# MENJALANKAN AUTH CONTROLLER
# =============================================

if __name__ == "__main__":

    app = AuthController()
    app.run()
