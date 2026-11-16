import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView


# ASTI DIANTI SABRINA_F52125330104
class BukuController:
    def __init__(self, user_role="admin"):
        self.model = BukuModel()
        self.view = BukuView()
        self.user_role = user_role

        # Hak akses Petugas dan Mahasiswa
        if self.user_role == "admin":
            self.view.btn_simpan.configure(command=self.simpan_data)
            self.view.btn_update.configure(command=self.update_data)
            self.view.btn_hapus.configure(command=self.hapus_data)
        else:
            # Mahasiswa hanya dapat melihat data buku
            self.view.btn_simpan.configure(state="disabled")
            self.view.btn_update.configure(state="disabled")
            self.view.btn_hapus.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_buku = self.model.get_all_buku()

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
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi!"
            )
            return

        berhasil = self.model.create_buku(judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data buku.")

    def update_data(self):
        if self.user_role != "admin":
            return

        if not self.view.selected_id:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data yang ingin diperbarui!"
            )
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi!"
            )
            return

        berhasil = self.model.update_buku(
            self.view.selected_id, judul, penulis, tahun
        )

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.view.kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal memperbarui data.")

    def hapus_data(self):
        if self.user_role != "admin":
            return

        if not self.view.selected_id:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data yang ingin dihapus!"
            )
            return

        if not messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus data ini?"
        ):
            return

        berhasil = self.model.delete_buku(self.view.selected_id)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.view.kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menghapus data.")

    def run(self):
        self.view.mainloop()
