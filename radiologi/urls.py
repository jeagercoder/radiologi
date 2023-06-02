


from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter(trailing_slash=False)
router.register('layanan-radiologi-list', views.KategoriWithLayananRadiologiViewSet)
router.register('tambah-layanan-radiologi-pasien', views.TambahLayananRadiologiPasienViewSet)
router.register('layanan-radiologi-pasien-list', views.LayananRadiologiPasienViewSet)
router.register('hapus-layanan-radiologi-pasien', views.HapusLayananRadiologiPasienViewSet)

urlpatterns = [] + router.urls
