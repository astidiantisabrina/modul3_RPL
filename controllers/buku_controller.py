import tkinter.messagebox as messagebox

from models.buku_model import BukuModel
from views.buku_view import BukuView


# ASTI DIANTI SABRINA_F5212530104


class BukuController:

    def __init__(self, master, user_role="admin", on_logout=None):

        self.model = BukuModel()
        self.user_role = str(user_role).strip().lower()
        self.on_logout = on_logout

        # Role petugas dan admin memiliki hak mengelola buku
        self.is_admin = self.user_role in ("admin", "petugas")

        # Membuat halaman buku sebagai jendela turunan
        self.view = BukuView(
            master=master,
            user_role=self.user_role,
            on_logout=self.logout
        )

        # Hubungkan tombol CRUD dengan fungsi controller
        self.view.btn_simpan.configure(
            command=self.simpan_data
        )

        self.view.btn_update.configure(
            command=self.update_data
        )

        self.view.btn_hapus.configure(
            command=self.hapus_data
        )

        # Muat data buku dari database
        self.muat_data_tabel()

    # =================================
    # MENAMPILKAN PESAN
    # =================================

    def _pesan(self, jenis, judul, isi):
        fungsi = getattr(messagebox, jenis)

        fungsi(
            judul,
            isi,
            parent=self.view
        )

    # =================================
    # VALIDASI HAK AKSES
    # =================================

    def _cek_admin(self):

        if not self.is_admin:
            self._pesan(
                "showerror",
                "Akses Ditolak",
                "Hanya Petugas yang dapat mengelola data buku!"
            )
            return False

        return True

    # =================================
    # VALIDASI INPUT FORM
    # =================================

    def _ambil_input_form(self):

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            self._pesan(
                "showwarning",
                "Peringatan",
                "Semua kolom harus diisi!"
            )
            return None

        if not tahun.isdigit() or len(tahun) != 4:
            self._pesan(
                "showwarning",
                "Peringatan",
                "Tahun terbit harus berupa 4 digit angka!"
            )
            return None

        return judul, penulis, int(tahun)

    # =================================
    # MEMUAT DATA BUKU
    # =================================

    def muat_data_tabel(self):

        try:
            # Bersihkan tabel terlebih dahulu
            for item in self.view.tabel.get_children():
                self.view.tabel.delete(item)

            # Ambil data dari database
            data_buku = self.model.get_all_buku()

            if not data_buku:
                return

            # Masukkan data ke tabel
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

        except Exception as error:

            print("Kesalahan memuat data buku:", error)

            self._pesan(
                "showerror",
                "Gagal Memuat Data",
                f"Data buku tidak dapat ditampilkan:\n{error}"
            )

    # =================================
    # MENYIMPAN DATA BUKU
    # =================================

    def simpan_data(self):

        if not self._cek_admin():
            return

        data = self._ambil_input_form()

        if data is None:
            return

        try:
            judul, penulis, tahun = data

            berhasil = self.model.create_buku(
                judul,
                penulis,
                tahun
            )

            if berhasil:

                self._pesan(
                    "showinfo",
                    "Sukses",
                    "Data buku berhasil disimpan!"
                )

                self.view.kosongkan_form()
                self.muat_data_tabel()

            else:

                self._pesan(
                    "showerror",
                    "Gagal",
                    "Gagal menyimpan data buku!"
                )

        except Exception as error:

            print("Kesalahan simpan buku:", error)

            self._pesan(
                "showerror",
                "Kesalahan",
                str(error)
            )

    # =================================
    # MEMPERBARUI DATA BUKU
    # =================================

    def update_data(self):

        if not self._cek_admin():
            return

        if not self.view.selected_id:
            self._pesan(
                "showwarning",
                "Peringatan",
                "Pilih data buku terlebih dahulu!"
            )
            return

        data = self._ambil_input_form()

        if data is None:
            return

        try:
            judul, penulis, tahun = data

            berhasil = self.model.update_buku(
                self.view.selected_id,
                judul,
                penulis,
                tahun
            )

            if berhasil:

                self._pesan(
                    "showinfo",
                    "Sukses",
                    "Data buku berhasil diperbarui!"
                )

                self.view.kosongkan_form()
                self.muat_data_tabel()

            else:

                self._pesan(
                    "showerror",
                    "Gagal",
                    "Gagal memperbarui data buku!"
                )

        except Exception as error:

            print("Kesalahan update buku:", error)

            self._pesan(
                "showerror",
                "Kesalahan",
                str(error)
            )

    # =================================
    # MENGHAPUS DATA BUKU
    # =================================

    def hapus_data(self):

        if not self._cek_admin():
            return

        if not self.view.selected_id:
            self._pesan(
                "showwarning",
                "Peringatan",
                "Pilih data buku terlebih dahulu!"
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            "Apakah Anda yakin ingin menghapus buku ini?",
            parent=self.view
        )

        if not konfirmasi:
            return

        try:
            berhasil = self.model.delete_buku(
                self.view.selected_id
            )

            if berhasil:

                # Segarkan tampilan lebih dulu agar langsung terlihat
                self.view.kosongkan_form()
                self.muat_data_tabel()

                self._pesan(
                    "showinfo",
                    "Sukses",
                    "Data buku berhasil dihapus!"
                )

                # Reset ID dijalankan terpisah setelah tampilan diperbarui,
                # sehingga kegagalannya tidak membatalkan proses hapus
                self.view.after(100, self._reset_id_aman)

            else:

                self._pesan(
                    "showerror",
                    "Gagal",
                    "Gagal menghapus data buku!"
                )

        except Exception as error:

            print("Kesalahan hapus buku:", error)

            self._pesan(
                "showerror",
                "Kesalahan",
                str(error)
            )

    # =================================
    # RESET ID JIKA TABEL KOSONG
    # =================================

    def _reset_id_aman(self):

        try:
            self.model.reset_id_jika_kosong()

        except Exception as error:

            # Gagal reset ID tidak boleh menghentikan aplikasi
            print("Kesalahan reset ID buku:", error)

    # =================================
    # LOGOUT
    # =================================

    def logout(self):

        callback = self.on_logout

        self.view.destroy()

        if callback:
            callback()

    # =================================
    # MENJALANKAN HALAMAN BUKU
    # =================================

    def run(self):

        self.view.deiconify()
        self.view.lift()
        self.view.focus_force()

        # Tidak memanggil mainloop() lagi.
        # Mainloop utama tetap dijalankan oleh LoginView.