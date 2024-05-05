from django.contrib import admin
from apps.insumos.models import Insumo


class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'precio', 'unidad_media', 'fecha_upd')
    search_fields = ('nombre', 'marca')
    list_filter = ('marca', 'unidad_media')
    ordering = ('nombre', 'marca', 'precio')


admin.site.register(Insumo, InsumoAdmin)
