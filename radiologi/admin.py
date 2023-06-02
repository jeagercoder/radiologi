from django.contrib import admin

from .models import (
    KategoriLayananRadiologi,
    LayananRadiologi,
    LayananRadiologiPasien
)


@admin.register(KategoriLayananRadiologi)
class KategoryLayananRadiologiAdmin(admin.ModelAdmin):
    pass


@admin.register(LayananRadiologi)
class LayananRadiologiAdmin(admin.ModelAdmin):
    pass


@admin.register(LayananRadiologiPasien)
class LayananRadiologiPasienAdin(admin.ModelAdmin):
    pass