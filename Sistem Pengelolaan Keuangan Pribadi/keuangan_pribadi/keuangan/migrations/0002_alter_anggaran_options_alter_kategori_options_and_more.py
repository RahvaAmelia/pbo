# Generated by Django 5.1.5 on 2025-02-03 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keuangan', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='anggaran',
            options={'verbose_name_plural': 'Anggaran'},
        ),
        migrations.AlterModelOptions(
            name='kategori',
            options={'verbose_name_plural': 'Kategori'},
        ),
        migrations.AlterModelOptions(
            name='pemasukan',
            options={'verbose_name_plural': 'Pemasukan'},
        ),
        migrations.AlterModelOptions(
            name='pengeluaran',
            options={'ordering': ['-tanggal'], 'verbose_name_plural': 'Pengeluaran'},
        ),
        migrations.AlterField(
            model_name='kategori',
            name='nama',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nama Kategori'),
        ),
    ]
