from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Kategori(models.Model):
    nama = models.CharField(max_length=100, unique=True, verbose_name="Nama Kategori")

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Kategori"

class Pemasukan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal = models.DateField()

    def __str__(self):
        return f"Pemasukan {self.jumlah} oleh {self.user.username}"

    class Meta:
        verbose_name_plural = "Pemasukan"

class Pengeluaran(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal = models.DateField()

    def __str__(self):
        return f"Pengeluaran {self.jumlah} oleh {self.user.username}"

    class Meta:
        verbose_name_plural = "Pengeluaran"
        ordering = ['-tanggal']

class Anggaran(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    batas = models.DecimalField(max_digits=10, decimal_places=2)
    pengeluaran = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()

    def total_pengeluaran(self):
        total = Pengeluaran.objects.filter(user=self.user, kategori=self.kategori,
                                           tanggal__range=[self.tanggal_mulai, self.tanggal_selesai]
                                          ).aggregate(Sum('jumlah'))['jumlah__sum'] or 0
        return total

    def sisa_anggaran(self):
        return self.batas - self.total_pengeluaran()

    class Meta:
        verbose_name_plural = "Anggaran"

    def __str__(self):
        return f"Anggaran {self.kategori.nama} untuk {self.user.username}"

class Transaksi(models.Model):
    tipe = models.CharField(max_length=20, choices=[('pemasukan', 'Pemasukan'), ('pengeluaran', 'Pengeluaran')])
    kategori = models.CharField(max_length=100)
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal = models.DateField()

    def __str__(self):
        return f"{self.kategori} - {self.jumlah}"