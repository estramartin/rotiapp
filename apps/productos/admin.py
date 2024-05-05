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
                url = reverse("admin:productos_promocion_change", args=[promocion.promocion.pk])  # Genera la URL para la página de edición de la promoción
                links.append(format_html('<a href="{}"><span style="">&#10004; {}</span></a>', url, promocion.promocion.nombre))  # tick verde y nombre de la promoción como enlace
            return format_html_join(', ', '{}', ((link,) for link in links))  # Une todos los enlaces con comas
        else:
            return format_html('<span style="color:red;">&#10008;</span>')  # x roja
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


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Promocion, PromocionAdmin)