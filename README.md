# SISTEM INFORMASI PERPUSTAKAAN

## 1. Deskripsi Aplikasi

Sistem Informasi Perpustakaan merupakan aplikasi desktop berbasis Python yang dikembangkan untuk membantu pengelolaan data perpustakaan secara terkomputerisasi. Aplikasi ini bertujuan mempermudah petugas dalam mengelola data buku, data anggota, serta proses autentikasi pengguna sehingga pengelolaan informasi perpustakaan menjadi lebih efektif dan terstruktur.

Aplikasi ini menggunakan arsitektur Model-View-Controller (MVC), database MySQL sebagai penyimpanan data, serta antarmuka desktop berbasis Tkinter atau turunannya.

## 2. Fitur Aplikasi

Beberapa fitur yang tersedia dalam aplikasi Sistem Informasi Perpustakaan meliputi:

- **Login:** Autentikasi pengguna menggunakan username dan password.
- **Registrasi Pengguna:** Pendaftaran akun pengguna baru.
- **Manajemen Buku:** Pengelolaan data buku perpustakaan.
- **Manajemen Anggota:** Pengelolaan data anggota perpustakaan.
- **Hak Akses Pengguna:** Pembagian role pengguna menjadi admin dan anggota.
- **Logout:** Keluar dari aplikasi dan kembali ke halaman login.

## 3. Struktur Direktori

Proyek ini menggunakan pola arsitektur Model-View-Controller (MVC) dengan struktur direktori sebagai berikut:

```text
MODUL3/
│
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml
│
├── config/
│   └── database.py
│
├── controllers/
│   ├── anggota_controller.py
│   ├── auth_controller.py
│   └── buku_controller.py
│
├── models/
│
├── views/
│   ├── anggota_view.py
│   ├── buku_view.py
│   └── login_view.py
│
├── tests/
│
├── build/
├── dist/
├── env/
│
├── main.py
├── main.spec
├── requirements.txt
├── test_anggota.py
├── test_auth.py
├── test_buku.py
└── test_model.py
```

Keterangan:

- **models/**: Mengelola logika data dan interaksi dengan database MySQL.
- **views/**: Mengatur tampilan antarmuka aplikasi.
- **controllers/**: Mengatur alur program dan menghubungkan model dengan tampilan.
- **config/**: Menyimpan konfigurasi koneksi database.
- **.github/workflows/**: Menyimpan konfigurasi otomatisasi CI menggunakan GitHub Actions.
- **build/**: Menyimpan hasil sementara proses pemaketan aplikasi.
- **dist/**: Menyimpan hasil aplikasi yang telah dikemas menggunakan PyInstaller.
- **main.py**: File utama untuk menjalankan aplikasi.
- **requirements.txt**: Daftar dependensi atau pustaka Python yang digunakan.

## 4. Teknologi yang Digunakan

Teknologi dan pustaka yang digunakan dalam pengembangan aplikasi ini adalah:

- Python 3.11
- Tkinter / CustomTkinter
- MySQL
- MySQL Connector
- Pytest
- Flake8
- Git dan GitHub
- GitHub Actions
- PyInstaller
- Laragon
- Visual Studio Code

## 5. Instalasi dan Konfigurasi Database MySQL

### A. Persyaratan Instalasi

Sebelum menjalankan aplikasi, pastikan perangkat telah memiliki:

1. Python versi 3.11.
2. Visual Studio Code.
3. Laragon.
4. MySQL Server.
5. Git (jika mengambil proyek melalui GitHub).

### B. Menjalankan MySQL melalui Laragon

1. Buka aplikasi Laragon.
2. Jalankan layanan MySQL dengan menekan tombol Start All atau menjalankan MySQL secara langsung.
3. Pastikan layanan MySQL dalam keadaan aktif.

### C. Membuat Database

Buka phpMyAdmin atau MySQL melalui Laragon, kemudian jalankan perintah SQL berikut:

```sql
CREATE DATABASE perpustakaan;
```

Database yang digunakan dalam aplikasi bernama `perpustakaan`.

### D. Konfigurasi Koneksi Database

Konfigurasi koneksi database terdapat pada file `config/database.py`.

Pengaturan database yang digunakan adalah:

```python
self.host = "localhost"
self.db_name = "perpustakaan"
self.username = "root"
self.password = ""
```

Keterangan:
- Host: localhost
- Nama database: perpustakaan
- Username: root
- Password: kosong

Pastikan database dan tabel-tabel yang dibutuhkan aplikasi sudah tersedia sebelum menjalankan aplikasi.

## 6. Instalasi Dependensi

Setelah proyek dibuka di Visual Studio Code, buka terminal dan masuk ke direktori proyek.

Buat virtual environment menggunakan perintah:

```bash
python -m venv env
```

Aktifkan virtual environment pada Windows:

```bash
env\Scripts\activate
```

Selanjutnya, instal seluruh dependensi proyek menggunakan perintah:

```bash
pip install -r requirements.txt
```

Perintah tersebut akan menginstal seluruh pustaka yang dibutuhkan aplikasi berdasarkan daftar pada file `requirements.txt`.

## 7. Cara Menjalankan Aplikasi

Pastikan MySQL pada Laragon sudah aktif dan seluruh dependensi berhasil diinstal.

Jalankan aplikasi menggunakan perintah berikut pada terminal:

```bash
python main.py
```

File `main.py` merupakan titik awal eksekusi aplikasi yang akan memanggil `AuthController` untuk menampilkan halaman login.

Setelah aplikasi terbuka, pengguna dapat memasukkan username dan password yang telah terdaftar untuk masuk ke dalam sistem.

## 8. Pengujian Otomatis (Automated Testing)

Pengujian aplikasi dilakukan menggunakan pustaka Pytest untuk memastikan fungsi-fungsi aplikasi berjalan sesuai dengan yang diharapkan.

Jalankan pengujian melalui terminal dengan perintah:

```bash
python -m pytest -v
```

Pengujian juga diintegrasikan dengan GitHub Actions untuk menjalankan pemeriksaan secara otomatis setiap kali terdapat perubahan kode pada repositori.

## 9. Integrasi CI Pipeline

Proyek ini menerapkan Continuous Integration (CI) menggunakan GitHub Actions.

Pipeline menjalankan beberapa tahapan secara otomatis, yaitu:

1. Checkout repository.
2. Setup Python 3.11.
3. Instalasi dependensi proyek.
4. Pemeriksaan kualitas kode menggunakan Flake8.
5. Pengujian unit otomatis menggunakan Pytest.

Pemeriksaan kualitas kode dilakukan menggunakan perintah:

```bash
flake8 models/ controllers/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

Integrasi ini bertujuan mendeteksi kesalahan kode dan memastikan pengujian otomatis berhasil sebelum perubahan kode diterapkan ke repositori utama.

## 10. Pemaketan Aplikasi (Packaging)

Aplikasi dapat dikemas menjadi file executable (.exe) menggunakan PyInstaller agar dapat dijalankan pada komputer Windows tanpa menjalankan perintah Python secara manual.

Instal PyInstaller:

```bash
pip install pyinstaller
```

Kemudian jalankan perintah:

```bash
pyinstaller --noconfirm --onefile --windowed --name "AplikasiPerpustakaan" main.py
```

Setelah proses selesai, file executable akan tersedia pada direktori:

```text
dist/AplikasiPerpustakaan.exe
```

Pastikan MySQL pada Laragon tetap aktif ketika aplikasi dijalankan karena aplikasi masih menggunakan database MySQL lokal.

## 11. Penutup

Sistem Informasi Perpustakaan ini dikembangkan untuk membantu proses pengelolaan data perpustakaan melalui aplikasi desktop berbasis Python dengan arsitektur MVC dan database MySQL.

Penerapan GitHub Actions, Flake8, Pytest, dan PyInstaller merupakan bagian dari implementasi otomasi CI/CD serta pemaketan aplikasi agar kualitas kode dapat diperiksa secara otomatis dan aplikasi dapat didistribusikan kepada pengguna.