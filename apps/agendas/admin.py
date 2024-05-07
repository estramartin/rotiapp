from django.contrib import admin
from apps.agendas.models import Agenda, AgendaFecha



class AgendaFechaInline(admin.TabularInline):
    model = AgendaFecha
    extra = 1
    autocomplete_fields = ['agenda']    
    list_display = ['fecha', 'activo']
    list_filter = ['fecha', 'activo']
    search_fields = ['fecha']
    list_per_page = 50


class AgendaAdmin(admin.ModelAdmin):
    model = Agenda
    list_display = [ 'nombre', 'fecha', 'activo']
    list_filter = ['fecha', 'activo']
    search_fields = ['nombre']
    list_per_page = 50
    inlines = [AgendaFechaInline]


admin.site.register(Agenda, AgendaAdmin)