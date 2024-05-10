from django.contrib import admin
from .models import Venta, VentaProducto, VentaPromocion, VentaVianda


class VentaProductoInline(admin.TabularInline):
    model = VentaProducto
    exclude = ['promocion', 'tipo', 'vianda']
    extra = 1
    readonly_fields = ['precio']
    autocomplete_fields = ['producto']
    
    def get_queryset(self, request):
        # Aquí utilizamos el manager específico para productos
        qs = super().get_queryset(request)
        return qs.filter(tipo=1)
    

class VentaPromocionInline(admin.TabularInline):
    model = VentaPromocion
    exclude = ['producto', 'tipo', 'vianda']
    extra = 1
    readonly_fields = ['precio']
    autocomplete_fields = ['promocion']

    def get_queryset(self, request):
        # Aquí utilizamos el manager específico para promociones
        qs = super().get_queryset(request)
        return qs.filter(tipo=2)


class VentaViandaInline(admin.TabularInline):
    model = VentaVianda
    exclude = ['producto', 'tipo', 'promocion']
    extra = 1
    readonly_fields = ['precio']
    autocomplete_fields = ['vianda']


class VentaAdmin(admin.ModelAdmin):
    inlines = [VentaPromocionInline, VentaProductoInline, VentaViandaInline]
    exclude = ('user',)
    list_display = ['venta_id', 'persona', 'fecha', 'total', 'es_promocion']
    readonly_fields = ['total']
    list_filter = ['fecha', 'activo']
    search_fields = ['venta_id']    
    list_per_page = 50
    raw_id_fields = ('persona',)
    
    def es_promocion(self, obj):
        return obj.detalles.filter(tipo=2).exists()
    es_promocion.boolean = True
    es_promocion.short_description = 'Es promoción'


    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Venta, VentaAdmin)
