from django.contrib import admin
from apps.insumos.models import Insumo, Stock


class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'precio', 'unidad_media', 'fecha_upd', 'get_cantidad')
    search_fields = ('nombre', 'marca')
    list_filter = ('marca', 'unidad_media')
    ordering = ('nombre', 'marca', 'precio')

    def get_cantidad(self, obj):
        return obj.stocks.first().cantidad if obj.stocks.first() else 'sin información'


class StockAdmin(admin.ModelAdmin):
    list_display = ('insumo', 'cantidad', 'fecha_upd', 'unidad_medida')
    readonly_fields = ('unidad_medida',)
    search_fields = ('insumo', 'cantidad')
    autocomplete_fields = ('insumo',)
    list_filter = ('insumo', 'fecha')
    ordering = ('insumo', 'fecha')


admin.site.register(Insumo, InsumoAdmin)
admin.site.register(Stock, StockAdmin)
