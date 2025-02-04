from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('laporan/', views.laporan, name='laporan'),
    path('tambah-transaksi/', views.tambah_transaksi, name='tambah_transaksi'),
]
