from config.database import Database

class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    def get_all_buku(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result

        return []

    def create_buku(self, judul, penulis, tahun_terbit):
        if self.conn:
            cursor = self.conn.cursor()

            query = f"""
                INSERT INTO {self.table_name}
                (judul, penulis, tahun_terbit)
                VALUES (%s, %s, %s)
            """

            val = (judul, penulis, tahun_terbit)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()

            return True

        return False

    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        if self.conn:
            cursor = self.conn.cursor()

            query = f"""
                UPDATE {self.table_name}
                SET judul=%s, penulis=%s, tahun_terbit=%s
                WHERE id_buku=%s
            """

            values = (judul, penulis, tahun_terbit, id_buku)
            cursor.execute(query, values)
            self.conn.commit()
            cursor.close()

            return True

        return False

    def delete_buku(self, id_buku):
        if self.conn:
            cursor = self.conn.cursor()

            query = f"DELETE FROM {self.table_name} WHERE id_buku=%s"
            cursor.execute(query, (id_buku,))
            self.conn.commit()
            cursor.close()

            return True

        return False

# TEMPEL method ini ke dalam class BukuModel di models/buku_model.py
# (di dalam class, sejajar dengan method delete_buku, termasuk indentasinya)

    def reset_id_jika_kosong(self):
        """Jika tabel buku sudah kosong, ID berikutnya mulai lagi dari 1."""
        if not self.conn:
            return False

        cursor = self.conn.cursor()   # cursor biasa (bukan dictionary)
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            jumlah = cursor.fetchone()[0]

            if jumlah == 0:
                cursor.execute(f"ALTER TABLE {self.table_name} AUTO_INCREMENT = 1")
                self.conn.commit()
                return True
            return False
        except Exception as e:
            print(f"Gagal mereset ID: {e}")
            return False
        finally:
            cursor.close()