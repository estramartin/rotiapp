from django.utils import timezone
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from .models import (
    Producto,
    ProductoInsumo,
    CategoriaProducto,
    Categoria,
    Promocion,
    PromocionProducto,
    Vianda,
    ViandaProducto,
    Agenda,
    )


class ProductoInsumoInline(admin.TabularInline):
    fields = ('producto', 'insumo', 'cantidad', 'precio_costo', 'insumo_precio')
    readonly_fields = ('precio_costo', 'insumo_precio', 'insumo_unidad_medida')
    search_fields = ('producto__nombre', 'insumo__nombre')
    autocomplete_fields = ['insumo']
    model = ProductoInsumo
    extra = 1


class CategoriaProductoInline(admin.TabularInline):
    fields = ('categoria', 'producto')
    model = CategoriaProducto
    extra = 1
    max_num = 1


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('pk','nombre', 'fecha_upd', 'precio_costo', 'margen', 'precio_venta', 'get_precio_venta')
    readonly_fields = ('precio_costo', 'precio_venta' )
    search_fields = ('nombre',)
    list_filter = ('categorias__categoria__nombre',)
    ordering = ('nombre',)
    inlines = [CategoriaProductoInline, ProductoInsumoInline]

    def get_precio_venta(self, obj):
        if obj.promociones.exists():
            links = []
            for promocion in obj.promociones.all():
                if promocion.promocion.activo:
                    url = reverse("admin:productos_promocion_change", args=[promocion.promocion.pk])  # Genera la URL para la página de edición de la promoción
                    links.append(format_html('<a href="{}"><span style="">&#10004; {}</span></a>', url, promocion.promocion.nombre))  # tick verde y nombre de la promoción como enlace
            return format_html_join(', ', '{}', ((link,) for link in links))  # Une todos los enlaces con comas
        else:
            return format_html('<span style="color:red;">&#10008;</span>')  # x roja
    # get_precio_venta.boolean = True
    get_precio_venta.short_description = 'En promoción'


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    inlines = [CategoriaProductoInline]


class PromocionProductoInline(admin.TabularInline):
    model = PromocionProducto
    readonly_fields = ('get_precio_costo', 'get_precio_venta', 'precio_promocion', 'promocion',)
    extra = 1
    
    def get_precio_venta(self, obj):
        return obj.producto.precio_venta
    get_precio_venta.short_description = 'Precio de venta'

    def get_precio_costo(self, obj):
        return obj.producto.precio_costo
    get_precio_costo.short_description = 'Precio de costo'


class PromocionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    inlines = [PromocionProductoInline]


class ViandaProductoInline(admin.TabularInline):
    model = ViandaProducto
    extra = 1


class ViandaAdmin(admin.ModelAdmin):
    inlines = [ViandaProductoInline]
    list_display = ('nombre', 'precio_venta_real', 'precio_venta', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        print(request.path)
        if 'autocomplete' in request.path:
            today = timezone.now().date()
            queryset = queryset.filter(agenda__fechas__fecha=today)
        return queryset, use_distinct


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Promocion, PromocionAdmin)
admin.site.register(Vianda, ViandaAdmin)
