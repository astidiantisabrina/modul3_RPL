import tkinter.messagebox as messagebox

from models.buku_model import BukuModel
from views.buku_view import BukuView


# ASTI DIANTI SABRINA_F5212530104

class BukuController:

    def __init__(self, user_role="admin", on_logout=None):

        # Inisialisasi Model dan View
        self.model = BukuModel()
        self.user_role = user_role

        # on_logout diteruskan ke View agar tombol Logout bisa
        # mengembalikan pengguna ke jendela Login
        self.view = BukuView(
            user_role=self.user_role,
            on_logout=on_logout
        )

        # Menghubungkan tombol. Tombol Simpan, Update, dan Delete sudah
        # dikunci (state="disabled") oleh View untuk role selain admin,
        # dan method-nya juga tetap memeriksa role sebagai lapisan kedua.
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_hapus.configure(command=self.hapus_data)

        # Memuat data buku
        self.muat_data_tabel()

    # =================================
    # VALIDASI INPUT FORM
    # =================================
    def _ambil_input_form(self):
        """Mengambil dan memvalidasi isi form.
        Mengembalikan (judul, penulis, tahun) atau None jika tidak valid."""
        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi!"
            )
            return None

        if not tahun.isdigit() or len(tahun) != 4:
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa 4 digit angka (misal: 2024)!"
            )
            return None

        return judul, penulis, tahun

    # =================================
    # MENAMPILKAN DATA BUKU
    # =================================
    def muat_data_tabel(self):

        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_buku = self.model.get_all_buku()

        for buku in data_buku:

            self.view.tabel.insert(
                "",
                "end",
                values=(
                    buku["id_buku"],
                    buku["judul"],
                    buku["penulis"],
                    buku["tahun_terbit"]
                )
            )

    # =================================
    # MENYIMPAN DATA BUKU
    # (khusus admin)
    # =================================
    def simpan_data(self):

        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Hanya Petugas yang dapat menambah buku!"
            )
            return

        data = self._ambil_input_form()
        if data is None:
            return

        judul, penulis, tahun = data

        berhasil = self.model.create_buku(
            judul,
            penulis,
            tahun
        )

        if berhasil:

            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil disimpan!"
            )

            self.view.kosongkan_form()
            self.muat_data_tabel()

        else:

            messagebox.showerror(
                "Error",
                "Gagal menyimpan data buku!"
            )

    # =================================
    # MEMPERBARUI DATA BUKU
    # (khusus admin)
    # =================================
    def update_data(self):

        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Hanya Petugas yang dapat memperbarui buku!"
            )
            return

        if not self.view.selected_id:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku terlebih dahulu!"
            )
            return

        data = self._ambil_input_form()
        if data is None:
            return

        judul, penulis, tahun = data

        berhasil = self.model.update_buku(
            self.view.selected_id,
            judul,
            penulis,
            tahun
        )

        if berhasil:

            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil diperbarui!"
            )

            self.view.kosongkan_form()
            self.muat_data_tabel()

        else:

            messagebox.showerror(
                "Error",
                "Gagal memperbarui data buku!"
            )

    # =================================
    # MENGHAPUS DATA BUKU
    # (khusus admin)
    # =================================
    def hapus_data(self):

        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Hanya Petugas yang dapat menghapus buku!"
            )
            return

        if not self.view.selected_id:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku terlebih dahulu!"
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            "Apakah kamu yakin ingin menghapus buku ini?"
        )

        if not konfirmasi:
            return

        berhasil = self.model.delete_buku(
            self.view.selected_id
        )

        if berhasil:

            # Jika semua buku sudah terhapus, ID berikutnya mulai dari 1 lagi
            self.model.reset_id_jika_kosong()

            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil dihapus!"
            )

            self.view.kosongkan_form()
            self.muat_data_tabel()

        else:

            messagebox.showerror(
                "Error",
                "Gagal menghapus data buku!"
            )

    # =================================
    # MENJALANKAN APLIKASI
    # =================================
    def run(self):
        # Pastikan jendela tampil di depan (tidak tertutup jendela VS Code)
        self.view.lift()
        self.view.focus_force()
        self.view.mainloop()