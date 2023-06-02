from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import (
    KategoriLayananRadiologi,
    LayananRadiologi,
    LayananRadiologiPasien,
    Tracer
)
from .choices import (
    KodeLayananChoices
)
from antrian.models import (
    Antrian
)
from kasir.models import (
    Invoice
)
from kasir.serializers import (
    InvoiceSerializer
)

class LayananRadiologiSerializer(serializers.ModelSerializer):

    class Meta:
        model = LayananRadiologi
        fields = [
            'id',
            'nama',
            'kategori',
            'harga'
        ]


class KatogoriWithLayananRadiologiSerializer(serializers.ModelSerializer):
    layanan_radiologi = serializers.SerializerMethodField()

    class Meta:
        model = KategoriLayananRadiologi
        fields = [
            'nama',
            'layanan_radiologi'
        ]

    def get_layanan_radiologi(self, obj):
        return LayananRadiologiSerializer(obj.layananradiologi_set.all(), many=True).data


class TambahLayananRadiologiPasienSerializer(serializers.Serializer):
    antrian = serializers.IntegerField()
    layanan_radiologi = serializers.ListField(child=serializers.IntegerField(), min_length=1)
    diagnosa = serializers.CharField()

    @transaction.atomic
    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        pendaftaran = antrian.pendaftaran
        pasien = pendaftaran.pasien
        dokter = self.context.get('request').user
        for layanan_id in data.get('layanan_radiologi'):
            layanan_radiologi = get_object_or_404(LayananRadiologi, id=layanan_id)
            harga = layanan_radiologi.harga
            kuantitas = 1
            total_harga = harga * kuantitas

            invoice = Invoice()
            invoice.kode_layanan = KodeLayananChoices.RADIOLOGI
            invoice.nama_layanan = layanan_radiologi.nama
            invoice.harga = harga
            invoice.kuantitas = kuantitas
            invoice.total_harga = total_harga
            invoice.hutang = total_harga
            invoice.pasien = pasien
            invoice.pendaftaran = pendaftaran
            invoice.antrian = antrian
            invoice.dokter = dokter
            invoice.summary_invoice = pendaftaran.invoice.summary_invoice
            invoice.save()
            if pendaftaran.asuransi == "BPJS":
                invoice.total_harga = 0
                invoice.hutang = 0
                invoice.save()

            layanan_radiologi_pasien = LayananRadiologiPasien()
            layanan_radiologi_pasien.layanan_radiologi = layanan_radiologi
            layanan_radiologi_pasien.pasien = pasien
            layanan_radiologi_pasien.pendaftaran = pendaftaran
            layanan_radiologi_pasien.antrian = antrian
            layanan_radiologi_pasien.dokter = dokter
            layanan_radiologi_pasien.invoice = invoice
            layanan_radiologi_pasien.diagnosa = data.get('diagnosa')
            layanan_radiologi_pasien.save()

        return layanan_radiologi_pasien

    def to_representation(self, instance):
        return {
            'success': True
        }


class TracerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tracer
        fields = '__all__'


class LayananRadiologiPasienSerializer(serializers.ModelSerializer):
    tracer = serializers.SerializerMethodField()
    invoice = serializers.SerializerMethodField()

    class Meta:
        model = LayananRadiologiPasien
        fields = [
            'id',
            'pasien',
            'pendaftaran',
            'antrian',
            'dokter',
            'petugas_radiologi',
            'layanan_radiologi',
            'status_layanan',
            'tracer',
            'invoice'
        ]

    def get_tracer(self, obj):
        tracer = Tracer.objects.filter(layanan_radiologi_pasien=obj)
        if tracer.exists():
            return tracer.last().url
        return None

    def get_invoice(self, obj):
        return InvoiceSerializer(obj.invoice).data


class HasilLayananRadiologiPasienSerializer(serializers.ModelSerializer):
    tracer = serializers.FileField()

    class Meta:
        model = LayananRadiologiPasien
        fields = [
            'catatan',
            'tracer'
        ]

    @transaction.atomic
    def update(self, instance, data):
        for obj in Tracer.objects.filter(layanan_radiologi_pasien=instance):
            obj.delete()

        tracer = Tracer()
        tracer.file = data.get('tracer')
        tracer.save()

        instance.catatan = data.get('catatan')
        instance.save()

        return instance

    def to_representation(self, instance):
        return {
            'success': True
        }


