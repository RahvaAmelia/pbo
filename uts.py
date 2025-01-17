class Orang:
    def __init__(self, nama, nomor_identitas):
        self.__nama = nama  
        self.__nomor_identitas = nomor_identitas  

    def tampilkan_info(self):
        return f"Nama: {self.__nama}, Nomor Identitas: {self.__nomor_identitas}"


class Dosen(Orang):
    def __init__(self, nama, nomor_identitas, nidn, mata_kuliah):
        super().__init__(nama, nomor_identitas) 
        self.__nidn = nidn  
        self.__mata_kuliah = mata_kuliah 

    def tampilkan_info(self):
        return f"{super().tampilkan_info()}, NIDN: {self.__nidn}, Mata Kuliah: {self.__mata_kuliah}"


class Mahasiswa(Orang):
    def __init__(self, nama, nomor_identitas, nim):
        super().__init__(nama, nomor_identitas)  
        self.__nim = nim 
        self.__jadwal = []  

    def tambah_jadwal(self, mata_kuliah):
        self.__jadwal.append(mata_kuliah)

    def tampilkan_info(self):
        return f"{super().tampilkan_info()}, NIM: {self.__nim}, Jadwal: {', '.join(self.__jadwal)}"


class MataKuliah:
    def __init__(self, kode, nama, dosen, jadwal_waktu):
        self.__kode = kode 
        self.__nama = nama  
        self.__dosen = dosen  
        self.__jadwal_waktu = jadwal_waktu  

    def tampilkan_info(self):
        return f"Kode: {self.__kode}, Nama: {self.__nama}, Dosen: {self.__dosen.tampilkan_info()}, Jadwal: {self.__jadwal_waktu}"


class SistemAkademik:
    def __init__(self):
        self.__dosen_list = []  
        self.__mahasiswa_list = []  
        self.__mata_kuliah_list = []  

    def tambah_dosen(self, dosen):
        self.__dosen_list.append(dosen)

    def tambah_mahasiswa(self, mahasiswa):
        self.__mahasiswa_list.append(mahasiswa)

    def tambah_mata_kuliah(self, mata_kuliah):
        if mata_kuliah._MataKuliah__dosen in self.__dosen_list:  
            self.__mata_kuliah_list.append(mata_kuliah)
        else:
            print("Dosen tidak terdaftar!")

    def tampilkan_jadwal(self):
        for mk in self.__mata_kuliah_list:
            print(mk.tampilkan_info())


if __name__ == "__main__":
    dosen1 = Dosen("Dr. Budi", "D001", "123456789", "Pendidikan Pancasila")
    dosen2 = Dosen("Dr. Siti", "D002", "987654321", "Pendidikan Agama")

    mahasiswa1 = Mahasiswa("Andi", "M001", "2021001")
    mahasiswa2 = Mahasiswa("Rina", "M002", "2021002")

    mata_kuliah1 = MataKuliah("CS101", "Pendidikan Pancasila", dosen1, "Senin, 10:00-12:00")
    mata_kuliah2 = MataKuliah("CS102", "Pendidikan Agama", dosen2, "Senin, 13.00-15.00")