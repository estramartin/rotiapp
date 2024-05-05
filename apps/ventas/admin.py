from django.contrib import admin
from .models import Venta, VentaDet

class VentaDetInline(admin.TabularInline):    
    readonly_fields = ['precio']
    autocomplete_fields = ['producto']
    extra = 1
    model = VentaDet

    
class VentaAdmin(admin.ModelAdmin):
    inlines = [VentaDetInline]
    list_display = ['venta_id', 'persona', 'fecha', 'total', 'activo']
    readonly_fields = ['total']
    list_filter = ['fecha', 'activo']
    search_fields = ['venta_id']    
    list_per_page = 50
    raw_id_fields = ('persona',)


admin.site.register(Venta, VentaAdmin)
