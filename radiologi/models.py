from django.db import models

from user.models import User
from pasien.models import (
    Pasien,
    Pendaftaran
)
from .choices import (
    StatusLayananChoices,
    StatusPembayaranChoices,
)
from kasir.models import (
    Invoice
)


class KategoriLayananRadiologi(models.Model):
    nama = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama


class LayananRadiologi(models.Model):
    nama = models.CharField(max_length=250, blank=True, null=True)
    kategori = models.ForeignKey(KategoriLayananRadiologi, on_delete=models.SET_NULL, blank=True, null=True)
    harga = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama


class LayananRadiologiPasien(models.Model):
    pasien = models.ForeignKey(Pasien, on_delete=models.SET_NULL, blank=True, null=True)
    pendaftaran = models.ForeignKey(Pendaftaran, on_delete=models.SET_NULL, blank=True, null=True)
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='radiologi_dokter')
    petugas_radiologi = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                          related_name='radiologi_petugas')
    layanan_radiologi = models.ForeignKey(LayananRadiologi, on_delete=models.SET_NULL, blank=True, null=True)
    status_layanan = models.CharField(max_length=30, choices=StatusLayananChoices.choices,
                                      default=StatusLayananChoices.MENUNGGU)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    diagnosa = models.TextField(blank=True, null=True)
    catatan = models.TextField(blank=True, null=True)


class Tracer(models.Model):
    layanan_radiologi_pasien = models.ForeignKey(LayananRadiologiPasien,
                                                 on_delete=models.SET_NULL,
                                                 blank=True, null=True)
    file = models.FileField(upload_to='radiologi/')
