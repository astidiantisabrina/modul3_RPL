import hashlib
from unittest.mock import MagicMock, patch

import pytest

from models.user_model import UserModel


@pytest.fixture
def model():
    """UserModel dengan database palsu, sehingga tes tidak menyentuh MySQL asli."""
    with patch("models.user_model.Database") as mock_database:
        mock_database.return_value.get_connection.return_value = MagicMock()
        user_model = UserModel()

    user_model.conn = MagicMock()
    user_model.mock_cursor = MagicMock()
    user_model.conn.cursor.return_value = user_model.mock_cursor
    return user_model


def hash_sha256(teks):
    return hashlib.sha256(teks.encode("utf-8")).hexdigest()


# ----------------------------------------------------------------------
# HASH PASSWORD
# ----------------------------------------------------------------------
def test_hash_password_konsisten():
    password_asli = "admin123"
    hash_1 = UserModel.hash_password(password_asli)
    hash_2 = UserModel.hash_password(password_asli)

    # Hasil hash tidak berubah untuk plaintext yang sama
    assert hash_1 != password_asli
    assert hash_1 == hash_2
    assert len(hash_1) == 64  # Panjang standar SHA-256 (hex)


def test_hash_password_sesuai_sha256():
    assert UserModel.hash_password("admin123") == hash_sha256("admin123")


def test_hash_password_berbeda_untuk_input_berbeda():
    assert UserModel.hash_password("admin123") != UserModel.hash_password("admin124")


# ----------------------------------------------------------------------
# REGISTER USER (Tugas 1)
# ----------------------------------------------------------------------
def test_register_user_berhasil_dan_password_di_hash(model):
    model.mock_cursor.fetchone.return_value = None  # username belum ada

    berhasil, pesan = model.register_user("petugas", "admin123", "admin")

    assert berhasil is True
    assert "berhasil" in pesan.lower()

    # Query terakhir adalah INSERT, periksa parameter yang disimpan
    query, params = model.mock_cursor.execute.call_args[0]
    assert "INSERT INTO users" in query
    assert params == ("petugas", hash_sha256("admin123"), "admin")
    assert "admin123" not in params  # plaintext tidak boleh tersimpan
    model.conn.commit.assert_called_once()
    model.mock_cursor.close.assert_called()


def test_register_user_role_dan_username_dinormalisasi(model):
    model.mock_cursor.fetchone.return_value = None

    berhasil, _ = model.register_user("  budi  ", "budi123", "ANGGOTA")

    assert berhasil is True
    _, params = model.mock_cursor.execute.call_args[0]
    assert params == ("budi", hash_sha256("budi123"), "anggota")


def test_register_user_username_duplikat_ditolak(model):
    model.mock_cursor.fetchone.return_value = (1,)  # username sudah ada

    berhasil, pesan = model.register_user("petugas", "admin123", "admin")

    assert berhasil is False
    assert "sudah digunakan" in pesan.lower()
    model.conn.commit.assert_not_called()


def test_register_user_role_tidak_valid_ditolak(model):
    berhasil, pesan = model.register_user("petugas", "admin123", "superuser")

    assert berhasil is False
    assert "role" in pesan.lower()
    model.mock_cursor.execute.assert_not_called()
    model.conn.commit.assert_not_called()


@pytest.mark.parametrize("username,password", [("", "abc"), ("abc", ""), ("   ", "abc")])
def test_register_user_input_kosong_ditolak(model, username, password):
    berhasil, _ = model.register_user(username, password, "admin")

    assert berhasil is False
    model.conn.commit.assert_not_called()


def test_register_user_tanpa_koneksi(model):
    model.conn = None

    berhasil, pesan = model.register_user("petugas", "admin123", "admin")

    assert berhasil is False
    assert "koneksi" in pesan.lower()


def test_register_user_rollback_jika_insert_gagal(model):
    # Panggilan pertama (cek username) lolos, panggilan kedua (INSERT) error
    model.mock_cursor.fetchone.return_value = None
    model.mock_cursor.execute.side_effect = [None, Exception("db error")]

    berhasil, pesan = model.register_user("petugas", "admin123", "admin")

    assert berhasil is False
    assert "gagal" in pesan.lower()
    model.conn.rollback.assert_called_once()
    model.conn.commit.assert_not_called()
    model.mock_cursor.close.assert_called()


# ----------------------------------------------------------------------
# AUTENTIKASI
# ----------------------------------------------------------------------
def test_autentikasi_pengguna_berhasil(model):
    # Simulasi data dari database ketika username & password cocok
    model.mock_cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "petugas",
        "role": "admin",
    }

    hasil = model.autentikasi("petugas", "admin123")

    assert hasil is not None
    assert hasil["username"] == "petugas"
    assert hasil["role"] == "admin"


def test_autentikasi_mengirim_password_yang_sudah_di_hash(model):
    model.mock_cursor.fetchone.return_value = None

    model.autentikasi("petugas", "admin123")

    query, params = model.mock_cursor.execute.call_args[0]
    assert "SELECT" in query
    assert params == ("petugas", hash_sha256("admin123"))
    assert "admin123" not in params


def test_autentikasi_gagal_jika_data_tidak_cocok(model):
    model.mock_cursor.fetchone.return_value = None

    hasil = model.autentikasi("petugas", "password_salah")

    assert hasil is None
    model.mock_cursor.close.assert_called()


def test_autentikasi_tanpa_koneksi_mengembalikan_none(model):
    model.conn = None

    assert model.autentikasi("petugas", "admin123") is None