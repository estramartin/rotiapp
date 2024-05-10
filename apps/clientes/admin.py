from django.contrib import admin
import datetime

from apps.personas.admin import PersonaAdmin
from .models import Cliente, ClienteVianda


class ClienteViandaadmin(admin.ModelAdmin):
    model = ClienteVianda
    list_display = ('cliente', 'vianda', 'vianda_productos', 'fecha', 'vianda_count' )
    search_fields = ('cliente', 'vianda')
    list_filter = ('fecha',)
    ordering = ('fecha',)

    def get_queryset(self, request):
        today = datetime.date.today()
        qs = super().get_queryset(request).filter(vianda__agenda__fechas__fecha=today)
        return qs.select_related('cliente', 'vianda')

    def vianda_productos(self, obj):
        return ', '.join([p.producto.nombre for p in obj.vianda.productos.all()])
    
    def vianda_count(self, obj):
        return ClienteVianda.vianda_count()
    vianda_count.short_description = 'Vianda Count'
    

class ClienteViandaInline(admin.TabularInline):
    model = ClienteVianda
    extra = 1

    
class ClienteAdmin(PersonaAdmin):
    list_display = ('nombre', 'apellido', 'cuenta_corriente', 'fecha_alta', 'fecha_baja', 'activo')
    search_fields = ('nombre', 'apellido')
    list_filter = ('activo',)
    inlines = [ClienteViandaInline] + PersonaAdmin.inlines.copy()


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(ClienteVianda, ClienteViandaadmin)