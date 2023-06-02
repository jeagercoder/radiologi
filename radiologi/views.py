from django.shortcuts import render, get_object_or_404
from django.db import transaction

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status


from .models import (
    KategoriLayananRadiologi,
    LayananRadiologi,
    LayananRadiologiPasien
)
from .serializers import (
    KatogoriWithLayananRadiologiSerializer,
    TambahLayananRadiologiPasienSerializer,
    LayananRadiologiPasienSerializer
)


class KategoriWithLayananRadiologiViewSet(GenericViewSet):
    queryset = KategoriLayananRadiologi.objects.all()
    serializer_class = KatogoriWithLayananRadiologiSerializer

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TambahLayananRadiologiPasienViewSet(GenericViewSet):
    queryset = LayananRadiologiPasien.objects.all()
    serializer_class = TambahLayananRadiologiPasienSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LayananRadiologiPasienViewSet(GenericViewSet):
    queryset = LayananRadiologiPasien.objects.all()
    serializer_class = LayananRadiologiPasienSerializer

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(antrian__id=self.request.query_params.get('antrian_id'))
        return super(LayananRadiologiPasienViewSet, self).get_queryset()

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HapusLayananRadiologiPasienViewSet(GenericViewSet):
    queryset = LayananRadiologiPasien.objects.all()
    lookup_field = 'pk'

    @transaction.atomic
    def destroy(self, request, pk):
        obj = self.get_object()
        obj.invoice.delete()
        obj.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)

