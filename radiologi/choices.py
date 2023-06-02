from django.db import models
from django.utils.translation import gettext_lazy as _


class KodeLayananChoices(models.TextChoices):
    RADIOLOGI = 'RADIOLOGI', _('Radiologi')


class StatusPembayaranChoices(models.TextChoices):
    BELUM_BAYAR = 'BELUM_BAYAR', _('Belum Bayar')
    DIBAYAR = 'DIBAYAR', _('Dibayar')
    LUNAS = 'LUNAS', _('Lunas')


class StatusLayananChoices(models.TextChoices):
    MENUNGGU = 'MENUNGGU', _('Menunggu')
    DILAYANI = 'DILAYANI', _('Dilayani')
    BATAL = 'BATAL', _('Batal')
