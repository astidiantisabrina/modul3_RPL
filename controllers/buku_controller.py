import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

# ASTI DIANTI SABRINA_F52125330104
class BukuController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = BukuModel()
        self.view = BukuView()

        # Binding (mengikat) tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_hapus.configure(command=self.hapus_data)

        # Memuat data ke tabel saat aplikasi pertama kali dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengosongkan isi tabel di View terlebih dahulu
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        # Mengambil data dari Model (database)
        data_buku = self.model.get_all_buku()

        # Memasukkan data baru ke dalam tabel View
        for buku in data_buku:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    buku['id_buku'],
                    buku['judul'],
                    buku['penulis'],
                    buku['tahun_terbit']
                )
            )

    def simpan_data(self):
        # Mengambil teks dari kotak input di View
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        # Validasi Form Kosong
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        # Mengirim data ke Model untuk disimpan
        berhasil = self.model.create_buku(judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def update_data(self):
        # Harus ada baris yang dipilih di tabel
        if not self.view.selected_id:
            messagebox.showwarning("Peringatan", "Pilih dulu data di tabel yang mau diperbarui!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_buku(self.view.selected_id, judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.view.kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def hapus_data(self):
        # Harus ada baris yang dipilih di tabel
        if not self.view.selected_id:
            messagebox.showwarning("Peringatan", "Pilih dulu data di tabel yang mau dihapus!")
            return

        # Konfirmasi sebelum menghapus
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            return

        berhasil = self.model.delete_buku(self.view.selected_id)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.view.kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    # Fungsi untuk menyalakan aplikasi
    def run(self):
        self.view.mainloop()