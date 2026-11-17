import customtkinter as ctk
from tkinter import ttk


class BukuView(ctk.CTkToplevel):

    def __init__(self, master, user_role="admin", on_logout=None):
        super().__init__(master)

        # =========================================
        # PENGATURAN APLIKASI
        # =========================================

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.master = master
        self.user_role = str(user_role).strip().lower()
        self.on_logout = on_logout
        self.selected_id = None

        # Admin dan petugas dapat mengelola data buku
        self.is_admin = self.user_role in ("admin", "petugas")

        # Pengaturan jendela
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("1000x600")
        self.minsize(850, 500)

        # Posisi jendela di tengah layar
        self.update_idletasks()

        lebar = 1000
        tinggi = 600

        x = (self.winfo_screenwidth() - lebar) // 2
        y = (self.winfo_screenheight() - tinggi) // 2

        self.geometry(f"{lebar}x{tinggi}+{x}+{y}")

        # Konfigurasi grid utama
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Membuat komponen
        self._buat_form()
        self._buat_tabel()
        self._terapkan_otorisasi()

        # Jika tombol X ditekan, jalankan logout
        self.protocol("WM_DELETE_WINDOW", self.logout)

        # Tampilkan jendela di depan
        self.transient(master)
        self.lift()
        self.focus_force()

    # =========================================
    # FORM DATA BUKU
    # =========================================

    def _buat_form(self):

        self.frame_kiri = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        self.frame_kiri.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.frame_kiri.grid_columnconfigure(0, weight=1)

        # Judul form
        ctk.CTkLabel(
            self.frame_kiri,
            text="Form Data Buku",
            font=("Arial", 18, "bold")
        ).pack(pady=(25, 20))

        # Input judul buku
        self.entry_judul = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Judul Buku",
            height=38
        )

        self.entry_judul.pack(
            pady=8,
            padx=15,
            fill="x"
        )

        # Input nama penulis
        self.entry_penulis = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Nama Penulis",
            height=38
        )

        self.entry_penulis.pack(
            pady=8,
            padx=15,
            fill="x"
        )

        # Input tahun terbit
        self.entry_tahun = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Tahun Terbit (Misal: 2024)",
            height=38
        )

        self.entry_tahun.pack(
            pady=8,
            padx=15,
            fill="x"
        )

        # Tombol simpan
        self.btn_simpan = ctk.CTkButton(
            self.frame_kiri,
            text="Simpan Data",
            height=38,
            fg_color="green",
            hover_color="darkgreen"
        )

        self.btn_simpan.pack(
            pady=(18, 8),
            padx=15,
            fill="x"
        )

        # Tombol update
        self.btn_update = ctk.CTkButton(
            self.frame_kiri,
            text="Perbarui Data (Update)",
            height=38,
            fg_color="blue",
            hover_color="darkblue"
        )

        self.btn_update.pack(
            pady=8,
            padx=15,
            fill="x"
        )

        # Tombol hapus
        self.btn_hapus = ctk.CTkButton(
            self.frame_kiri,
            text="Hapus Data (Delete)",
            height=38,
            fg_color="red",
            hover_color="darkred"
        )

        self.btn_hapus.pack(
            pady=8,
            padx=15,
            fill="x"
        )

        # Informasi akun
        ctk.CTkLabel(
            self.frame_kiri,
            text=f"Login sebagai: {self.user_role.upper()}",
            font=("Arial", 11)
        ).pack(
            side="bottom",
            pady=(5, 5)
        )

        # Tombol logout
        self.btn_logout = ctk.CTkButton(
            self.frame_kiri,
            text="Logout",
            height=38,
            fg_color="gray40",
            hover_color="gray25",
            command=self.logout
        )

        self.btn_logout.pack(
            side="bottom",
            pady=12,
            padx=15,
            fill="x"
        )

    # =========================================
    # TABEL DATA BUKU
    # =========================================

    def _buat_tabel(self):

        self.frame_kanan = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        self.frame_kanan.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.frame_kanan.grid_rowconfigure(1, weight=1)
        self.frame_kanan.grid_columnconfigure(0, weight=1)

        # Judul tabel
        ctk.CTkLabel(
            self.frame_kanan,
            text="Daftar Koleksi Buku",
            font=("Arial", 18, "bold")
        ).grid(
            row=0,
            column=0,
            pady=18
        )

        # Pengaturan style tabel
        style = ttk.Style(self)

        style.theme_use("clam")

        # Isi tabel
        style.configure(
            "Buku.Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            rowheight=32,
            borderwidth=0,
            font=("Arial", 11)
        )

        # Header tabel
        style.configure(
            "Buku.Treeview.Heading",
            background="#1f538d",
            foreground="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padding=8
        )

        # Warna header ketika disentuh
        style.map(
            "Buku.Treeview.Heading",
            background=[
                ("active", "#164477")
            ],
            foreground=[
                ("active", "white")
            ]
        )

        # Warna baris yang dipilih
        style.map(
            "Buku.Treeview",
            background=[
                ("selected", "#1f538d")
            ],
            foreground=[
                ("selected", "white")
            ]
        )

        # Wadah tabel
        wadah = ctk.CTkFrame(
            self.frame_kanan,
            fg_color="transparent"
        )

        wadah.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="nsew"
        )

        wadah.grid_rowconfigure(0, weight=1)
        wadah.grid_columnconfigure(0, weight=1)

        # Kolom tabel
        kolom = (
            "id",
            "judul",
            "penulis",
            "tahun"
        )

        self.tabel = ttk.Treeview(
            wadah,
            columns=kolom,
            show="headings",
            style="Buku.Treeview"
        )

        # Header tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("tahun", text="Tahun")

        # Ukuran kolom
        self.tabel.column(
            "id",
            width=55,
            minwidth=45,
            anchor="center"
        )

        self.tabel.column(
            "judul",
            width=200,
            minwidth=120,
            anchor="w"
        )

        self.tabel.column(
            "penulis",
            width=150,
            minwidth=100,
            anchor="w"
        )

        self.tabel.column(
            "tahun",
            width=80,
            minwidth=60,
            anchor="center"
        )

        # Scrollbar vertikal
        scrollbar_y = ttk.Scrollbar(
            wadah,
            orient="vertical",
            command=self.tabel.yview
        )

        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(
            wadah,
            orient="horizontal",
            command=self.tabel.xview
        )

        self.tabel.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        # Menampilkan tabel
        self.tabel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # Event ketika baris dipilih
        self.tabel.bind(
            "<<TreeviewSelect>>",
            self.pilih_baris
        )

    # =========================================
    # HAK AKSES PENGGUNA
    # =========================================

    def _terapkan_otorisasi(self):

        if not self.is_admin:

            # Nonaktifkan semua input
            for entry in (
                self.entry_judul,
                self.entry_penulis,
                self.entry_tahun
            ):
                entry.configure(
                    state="disabled"
                )

            # Nonaktifkan tombol CRUD
            for tombol in (
                self.btn_simpan,
                self.btn_update,
                self.btn_hapus
            ):
                tombol.configure(
                    state="disabled",
                    fg_color="gray30",
                    hover_color="gray30"
                )

    # =========================================
    # LOGOUT
    # =========================================

    def logout(self):

        callback = self.on_logout

        self.destroy()

        if callback:
            callback()

    # =========================================
    # MEMILIH DATA BUKU
    # =========================================

    def pilih_baris(self, event=None):

        if not self.is_admin:
            return

        terpilih = self.tabel.selection()

        if not terpilih:
            return

        nilai = self.tabel.item(
            terpilih[0],
            "values"
        )

        if not nilai:
            return

        # Kosongkan form lebih dulu (ini juga me-reset selected_id)
        self.kosongkan_input()

        # Simpan ID SETELAH form dikosongkan
        self.selected_id = nilai[0]

        self.entry_judul.insert(0, nilai[1])
        self.entry_penulis.insert(0, nilai[2])
        self.entry_tahun.insert(0, nilai[3])

    # =========================================
    # MEMBERSIHKAN FORM
    # =========================================

    def kosongkan_input(self):

        if not self.is_admin:
            return

        self.entry_judul.delete(0, "end")
        self.entry_penulis.delete(0, "end")
        self.entry_tahun.delete(0, "end")

        self.selected_id = None

    def kosongkan_form(self):

        self.kosongkan_input()

        for item in self.tabel.selection():
            self.tabel.selection_remove(item)


# =============================================
# PENGUJIAN BUKU VIEW SECARA LANGSUNG
# =============================================

if __name__ == "__main__":

    # Membuat root utama untuk pengujian
    root = ctk.CTk()
    root.withdraw()

    app = BukuView(
        master=root,
        user_role="admin"
    )

    app.mainloop()
    root.destroy()