import hashlib
from config.database import Database


class UserModel:
    # Role yang diizinkan di sistem
    ALLOWED_ROLES = ("admin", "anggota")

    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "users"

    @staticmethod
    def hash_password(password):
        # Mengubah plain text password menjadi hash SHA-256 (64 karakter hex)
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def username_exists(self, username):
        # Cek apakah username sudah terdaftar
        if not self.conn:
            return False
        cursor = self.conn.cursor()
        try:
            query = f"SELECT 1 FROM {self.table_name} WHERE username = %s LIMIT 1"
            cursor.execute(query, (username,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def register_user(self, username, password, role):
        """
        Mendaftarkan user baru. Password otomatis di-hash SHA-256
        sebelum disimpan ke tabel users.
        Return: (True/False, pesan)
        """
        if not self.conn:
            return False, "Koneksi database tidak tersedia."

        username = (username or "").strip()
        role = (role or "").strip().lower()

        if not username or not password:
            return False, "Username dan password tidak boleh kosong."

        if role not in self.ALLOWED_ROLES:
            return False, f"Role tidak valid. Pilih salah satu: {', '.join(self.ALLOWED_ROLES)}."

        if self.username_exists(username):
            return False, "Username sudah digunakan."

        password_hash = self.hash_password(password)

        cursor = self.conn.cursor()
        try:
            # Parameterized Query untuk mencegah SQL Injection
            query = f"INSERT INTO {self.table_name} (username, password, role) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password_hash, role))
            self.conn.commit()
            return True, "User berhasil didaftarkan."
        except Exception as e:
            self.conn.rollback()
            return False, f"Gagal mendaftarkan user: {e}"
        finally:
            cursor.close()

    def autentikasi(self, username, password):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            try:
                password_hash = self.hash_password(password)

                # Parameterized Query untuk mencegah SQL Injection
                query = f"SELECT id_user, username, role FROM {self.table_name} WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password_hash))
                return cursor.fetchone()
            finally:
                cursor.close()
        return None