from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from .models import Kategori, Pemasukan, Pengeluaran, Anggaran

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama')
    search_fields = ('nama',)

@admin.register(Pemasukan)
class PemasukanAdmin(admin.ModelAdmin):
    list_display = ('user', 'kategori', 'jumlah', 'tanggal')
    list_filter = ('tanggal', 'kategori')
    search_fields = ('user__username', 'kategori__nama')
    ordering = ('-tanggal',)

@admin.register(Pengeluaran)
class PengeluaranAdmin(admin.ModelAdmin):
    list_display = ('user', 'kategori', 'jumlah', 'tanggal', 'status_anggaran')
    list_filter = ('tanggal', 'kategori')
    search_fields = ('user__username', 'kategori__nama')
    ordering = ('-tanggal',)

    def status_anggaran(self, obj):
        # Cek apakah pengeluaran melebihi anggaran
        anggaran = Anggaran.objects.filter(user=obj.user, kategori=obj.kategori).first()
        if anggaran and obj.jumlah > anggaran.batas:
            return format_html('<span style="color: red; font-weight: bold;">Melebihi Anggaran</span>')
        return "Aman"
    
    status_anggaran.short_description = "Status Anggaran"

@admin.register(Anggaran)
class AnggaranAdmin(admin.ModelAdmin):
    list_display = ('user', 'kategori', 'batas', 'tanggal_mulai', 'tanggal_selesai')
    list_filter = ('tanggal_mulai', 'tanggal_selesai')
    search_fields = ('user__username', 'kategori__nama')

    def pengguna_terlampaui(self, request, queryset):
        # Menampilkan pengguna yang melebihi anggaran
        terlampaui = []
        for anggaran in queryset:
            total_pengeluaran = Pengeluaran.objects.filter(user=anggaran.user, kategori=anggaran.kategori).aggregate(Sum('jumlah'))['jumlah__sum'] or 0
            if total_pengeluaran > anggaran.batas:
                terlampaui.append(anggaran.user.username)
        
        if terlampaui:
            self.message_user(request, f"Pengguna yang melebihi anggaran: {', '.join(terlampaui)}")
        else:
            self.message_user(request, "Tidak ada pengguna yang melebihi anggaran.")

    actions = [pengguna_terlampaui]

# Laporan Keuangan untuk Administrator
class LaporanKeuanganAdmin(admin.ModelAdmin):
    change_list_template = "admin/laporan_keuangan.html"

    def changelist_view(self, request, extra_context=None):
        total_pemasukan = Pemasukan.objects.aggregate(Sum('jumlah'))['jumlah__sum'] or 0
        total_pengeluaran = Pengeluaran.objects.aggregate(Sum('jumlah'))['jumlah__sum'] or 0
        extra_context = extra_context or {"total_pemasukan": total_pemasukan, "total_pengeluaran": total_pengeluaran}
        return super().changelist_view(request, extra_context=extra_context)


class CustomAdminSite(admin.AdminSite):
    site_header = "Pengelolaan Keuangan Pribadi Admin"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('viewsite/', self.view_site_redirect),  # Custom URL untuk mengarahkan ke dashboard
        ]
        return custom_urls + urls

    def view_site_redirect(self, request):
        # Redirect ke halaman utama (dashboard)
        return HttpResponseRedirect(reverse('home'))

admin_site = CustomAdminSite(name='custom_admin')
admin.site.site_header = "Admin Keuangan Pribadi"
admin.site.site_title = "Keuangan Pribadi Admin"
admin.site.index_title = "Dashboard Pengelolaan Keuangan"
