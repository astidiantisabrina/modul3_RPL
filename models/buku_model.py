from config.database import Database


class BukuModel:

    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    # =================================
    # MENGAMBIL SEMUA DATA BUKU
    # =================================

    def get_all_buku(self):
        if not self.conn:
            return []

        cursor = self.conn.cursor(dictionary=True)

        try:
            cursor.execute(f"SELECT * FROM {self.table_name}")
            return cursor.fetchall()

        finally:
            cursor.close()

            # Akhiri transaksi baca agar tidak menahan metadata lock
            # pada tabel buku (penyebab ALTER TABLE menggantung).
            self.conn.commit()

    # =================================
    # MENAMBAH DATA BUKU
    # =================================

    def create_buku(self, judul, penulis, tahun_terbit):
        if not self.conn:
            return False

        cursor = self.conn.cursor()

        try:
            query = f"""
                INSERT INTO {self.table_name}
                (judul, penulis, tahun_terbit)
                VALUES (%s, %s, %s)
            """

            cursor.execute(query, (judul, penulis, tahun_terbit))
            self.conn.commit()
            return True

        except Exception:
            self.conn.rollback()
            raise

        finally:
            cursor.close()

    # =================================
    # MEMPERBARUI DATA BUKU
    # =================================

    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        if not self.conn:
            return False

        cursor = self.conn.cursor()

        try:
            query = f"""
                UPDATE {self.table_name}
                SET judul=%s, penulis=%s, tahun_terbit=%s
                WHERE id_buku=%s
            """

            cursor.execute(
                query,
                (judul, penulis, tahun_terbit, id_buku)
            )
            self.conn.commit()
            return True

        except Exception:
            self.conn.rollback()
            raise

        finally:
            cursor.close()

    # =================================
    # MENGHAPUS DATA BUKU
    # =================================

    def delete_buku(self, id_buku):
        if not self.conn:
            return False

        cursor = self.conn.cursor()

        try:
            query = f"DELETE FROM {self.table_name} WHERE id_buku=%s"

            cursor.execute(query, (id_buku,))
            self.conn.commit()
            return True

        except Exception:
            self.conn.rollback()
            raise

        finally:
            cursor.close()

    # =================================
    # RESET ID JIKA TABEL KOSONG
    # =================================

    def reset_id_jika_kosong(self):
        """Jika tabel buku sudah kosong, ID berikutnya mulai lagi dari 1."""
        if not self.conn:
            return False

        cursor = self.conn.cursor()

        try:
            # Batasi waktu tunggu lock 3 detik. Tanpa ini, ALTER TABLE
            # bisa menunggu sangat lama jika ada koneksi lain yang
            # masih menahan tabel buku, dan aplikasi terlihat membeku.
            cursor.execute("SET SESSION lock_wait_timeout = 3")

            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            jumlah = cursor.fetchone()[0]

            # Akhiri transaksi baca sebelum menjalankan perintah DDL
            self.conn.commit()

            if jumlah == 0:
                cursor.execute(
                    f"ALTER TABLE {self.table_name} AUTO_INCREMENT = 1"
                )
                self.conn.commit()
                return True

            return False

        except Exception as error:
            print(f"Gagal mereset ID: {error}")
            self.conn.rollback()
            return False

        finally:
            cursor.close()