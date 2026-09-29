print("=== PERHITUNGAN NILAI MAHASISWA ===")

nama = input("Nama mahasiswa: ")
tugas = float(input("Nilai tugas: "))
uts = float(input("Nilai UTS: "))
uas = float(input("Nilai UAS: "))

nilai_akhir = (tugas * 0.30) + (uts * 0.30) + (uas * 0.40)

print("\nNama:", nama)
print("Nilai akhir:", nilai_akhir)

if nilai_akhir >= 70:
    print("Status: Lulus")
else:
    print("Status: Tidak Lulus")