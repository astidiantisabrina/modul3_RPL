import customtkinter as ctk
from tkinter import ttk


class BukuView(ctk.CTk):
    def __init__(self, user_role="admin", on_logout=None):
        super().__init__()

        self.user_role = user_role
        self.on_logout = on_logout  # callback untuk kembali ke LoginView
        self.selected_id = None

        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("850x500")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self._buat_form()
        self._buat_tabel()
        self._terapkan_otorisasi()

    # ------------------------------------------------------------------
    # FORM (kiri)
    # ------------------------------------------------------------------
    def _buat_form(self):
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kiri,
            text="Form Data Buku",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        self.entry_judul = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Judul Buku"
        )
        self.entry_judul.pack(pady=8, padx=15, fill="x")

        self.entry_penulis = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Nama Penulis"
        )
        self.entry_penulis.pack(pady=8, padx=15, fill="x")

        self.entry_tahun = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Tahun Terbit (Misal: 2024)"
        )
        self.entry_tahun.pack(pady=8, padx=15, fill="x")

        self.btn_simpan = ctk.CTkButton(
            self.frame_kiri,
            text="Simpan Data",
            fg_color="green"
        )
        self.btn_simpan.pack(pady=8, padx=15, fill="x")

        self.btn_update = ctk.CTkButton(
            self.frame_kiri,
            text="Perbarui Data (Update)",
            fg_color="blue"
        )
        self.btn_update.pack(pady=8, padx=15, fill="x")

        self.btn_hapus = ctk.CTkButton(
            self.frame_kiri,
            text="Hapus Data (Delete)",
            fg_color="red"
        )
        self.btn_hapus.pack(pady=8, padx=15, fill="x")

        # Tombol Logout di bagian bawah form
        self.btn_logout = ctk.CTkButton(
            self.frame_kiri,
            text="Logout",
            fg_color="gray40",
            hover_color="gray30",
            command=self.logout
        )
        self.btn_logout.pack(side="bottom", pady=15, padx=15, fill="x")

    # ------------------------------------------------------------------
    # TABEL (kanan)
    # ------------------------------------------------------------------
    def _buat_tabel(self):
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kanan,
            text="Daftar Koleksi Buku",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Gaya tabel agar serasi dengan tema gelap dan teks tidak terpotong
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Buku.Treeview",
            background="#2b2b2b",
            fieldbackground="#2b2b2b",
            foreground="white",
            rowheight=28,
            borderwidth=0,
            font=("Arial", 11)
        )
        style.configure(
            "Buku.Treeview.Heading",
            background="#1f538d",
            foreground="white",
            font=("Arial", 11, "bold"),
            relief="flat"
        )
        style.map(
            "Buku.Treeview",
            background=[("selected", "#1f538d")],
            foreground=[("selected", "white")]
        )

        wadah = ctk.CTkFrame(self.frame_kanan, fg_color="transparent")
        wadah.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        kolom = ("id", "judul", "penulis", "tahun")

        self.tabel = ttk.Treeview(
            wadah,
            columns=kolom,
            show="headings",
            height=15,
            style="Buku.Treeview"
        )

        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("tahun", text="Tahun")

        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("judul", width=170)
        self.tabel.column("penulis", width=130)
        self.tabel.column("tahun", width=70, anchor="center")

        scrollbar = ttk.Scrollbar(wadah, orient="vertical", command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=scrollbar.set)

        self.tabel.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

    # ------------------------------------------------------------------
    # OTORISASI
    # ------------------------------------------------------------------
    def _terapkan_otorisasi(self):
        # Admin (petugas): semua fitur aktif.
        # Selain admin (misalnya "anggota"): hanya bisa melihat daftar buku
        # dan menekan Logout. Form dan tombol Simpan/Update/Delete dikunci.
        if self.user_role != "admin":
            for entry in (self.entry_judul, self.entry_penulis, self.entry_tahun):
                entry.configure(state="disabled")

            for tombol in (self.btn_simpan, self.btn_update, self.btn_hapus):
                tombol.configure(state="disabled", fg_color="gray30")

    # ------------------------------------------------------------------
    # LOGOUT
    # ------------------------------------------------------------------
    def logout(self):
        """Tutup jendela perpustakaan lalu kembali ke LoginView."""
        callback = self.on_logout
        self.destroy()
        if callback:
            callback()

    # ------------------------------------------------------------------
    # HELPER FORM
    # ------------------------------------------------------------------
    def pilih_baris(self, event=None):
        if self.user_role != "admin":
            return

        terpilih = self.tabel.selection()

        if not terpilih:
            return

        nilai = self.tabel.item(terpilih[0], "values")

        self.selected_id = nilai[0]

        self.entry_judul.delete(0, "end")
        self.entry_judul.insert(0, nilai[1])

        self.entry_penulis.delete(0, "end")
        self.entry_penulis.insert(0, nilai[2])

        self.entry_tahun.delete(0, "end")
        self.entry_tahun.insert(0, nilai[3])

    def kosongkan_form(self):
        if self.user_role != "admin":
            return

        self.entry_judul.delete(0, "end")
        self.entry_penulis.delete(0, "end")
        self.entry_tahun.delete(0, "end")

        self.selected_id = None

        # Hilangkan pilihan baris di tabel
        for item in self.tabel.selection():
            self.tabel.selection_remove(item)


if __name__ == "__main__":
    # Ganti "admin" menjadi "anggota" untuk menguji tombol terkunci
    app = BukuView(user_role="anggota", on_logout=lambda: print("Kembali ke LoginView"))
    app.mainloop()