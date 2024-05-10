from django.contrib import admin
from .models import Proveedor
from apps.insumos.models import InsumoProveedor
from apps.personas.admin import PersonaAdmin


# Register your models here.

class InsumoProveedorInline(admin.TabularInline):
    model = InsumoProveedor
    autocomplete_fields = ['insumo']
    readonly_fields = ['unidad_medida','notificado']
    raw_id_fields = ['insumo']
    extra = 1


class ProveedorAdmin(PersonaAdmin):
    model = Proveedor
    list_display = ['razon_social', 'domicilio', 'telefono', 'email']
    list_filter = ['razon_social',]
    search_fields = ['razon_social',]
    list_per_page = 50
    inlines = PersonaAdmin.inlines + [InsumoProveedorInline]


admin.site.register(Proveedor, ProveedorAdmin)