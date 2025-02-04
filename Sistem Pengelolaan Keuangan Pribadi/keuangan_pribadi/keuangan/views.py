from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Pemasukan, Pengeluaran, Kategori, Anggaran, Transaksi
from django.db.models import Sum
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.db import models



@login_required
def dashboard(request):
    total_pemasukan = Pemasukan.objects.filter(user=request.user).aggregate(Sum('jumlah'))['jumlah__sum'] or 0
    total_pengeluaran = Pengeluaran.objects.filter(user=request.user).aggregate(Sum('jumlah'))['jumlah__sum'] or 0
    anggaran_list = Anggaran.objects.filter(user=request.user)  
    kategori_list = Kategori.objects.all()

    for anggaran in anggaran_list:
        anggaran.pengeluaran = anggaran.total_pengeluaran()
        anggaran.sisa = anggaran.sisa_anggaran()

    return render(request, 'dashboard.html', {
        'total_pemasukan': total_pemasukan,
        'total_pengeluaran': total_pengeluaran,
        'anggaran_list': anggaran_list,
        'kategori_list': kategori_list
    })


@login_required
def laporan(request):
    # Mendapatkan tanggal mulai dan selesai dari request
    tanggal_mulai = request.GET.get('tanggal_mulai')
    tanggal_selesai = request.GET.get('tanggal_selesai')

    if tanggal_mulai and tanggal_selesai:
        # Mengubah tanggal menjadi format datetime
        tanggal_mulai = datetime.strptime(tanggal_mulai, '%Y-%m-%d')
        tanggal_selesai = datetime.strptime(tanggal_selesai, '%Y-%m-%d')

        # Mengambil total pemasukan dalam rentang tanggal
        total_pemasukan = Pemasukan.objects.filter(tanggal__range=[tanggal_mulai, tanggal_selesai]) \
            .aggregate(Sum('jumlah'))['jumlah__sum'] or 0

        # Mengambil total pengeluaran dalam rentang tanggal
        total_pengeluaran = Pengeluaran.objects.filter(tanggal__range=[tanggal_mulai, tanggal_selesai]) \
            .aggregate(Sum('jumlah'))['jumlah__sum'] or 0

        # Mengambil data anggaran dalam rentang tanggal
        anggaran_list = Anggaran.objects.filter(tanggal_mulai__lte=tanggal_selesai, tanggal_selesai__gte=tanggal_mulai)

        # Menghitung pengeluaran per anggaran
        for anggaran in anggaran_list:
            anggaran.pengeluaran = anggaran.total_pengeluaran()

        return render(request, 'laporan.html', {
            'tanggal_mulai': tanggal_mulai,
            'tanggal_selesai': tanggal_selesai,
            'total_pemasukan': total_pemasukan,
            'total_pengeluaran': total_pengeluaran,
            'anggaran_list': anggaran_list
        })
    else:
        return render(request, 'laporan.html', {
            'error': 'Silakan pilih rentang tanggal untuk melihat laporan.'
        })

def total_pengeluaran(self):
    total = Pengeluaran.objects.filter(user=self.user, kategori=self.kategori,
                                       tanggal__range=[self.tanggal_mulai, self.tanggal_selesai]
                                      ).aggregate(Sum('jumlah'))['jumlah__sum'] or 0
    return total


@login_required
def tambah_transaksi(request):
    if request.method == 'POST':
        tipe = request.POST.get('tipe')
        kategori_id = request.POST.get('kategori')
        jumlah = request.POST.get('jumlah')
        tanggal = request.POST.get('tanggal')

        kategori = Kategori.objects.get(id=kategori_id)

        if tipe == 'pemasukan':
            Pemasukan.objects.create(user=request.user, kategori=kategori, jumlah=jumlah, tanggal=tanggal)
            messages.success(request, "Pemasukan berhasil ditambahkan!")
        elif tipe == 'pengeluaran':
            Pengeluaran.objects.create(user=request.user, kategori=kategori, jumlah=jumlah, tanggal=tanggal)
            messages.success(request, "Pengeluaran berhasil ditambahkan!")

        return redirect('dashboard')