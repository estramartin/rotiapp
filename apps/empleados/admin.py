from django.contrib import admin
from apps.empleados import models
from apps.personas.admin import PersonaAdmin


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'valor_antiguedad', 'aportes')
    search_fields = ('nombre', 'descripcion',)
    ordering = ('nombre', 'descripcion',)


class EmpleadoCategodriaInline(admin.TabularInline):
    model = models.EmpleadoCategoria
    readonly_fields = ('valor_antiguedad',)
    extra = 1
    max_num = 1


class EmpleadoAdmin(PersonaAdmin):
    list_display = ('nombre', 'apellido', 'nro_doc', 'fec_nac', 'fecha_ingreso', 'fecha_egreso', 'activo')
    search_fields = ('nombre', 'apellido', 'nro_doc')
    list_filter = ('activo',)
    ordering = ('nombre', 'apellido', 'nro_doc')
    inlines = [EmpleadoCategodriaInline] + PersonaAdmin.inlines.copy()


admin .site.register(models.Categoria, CategoriaAdmin)
admin.site.register(models.Empleado, EmpleadoAdmin)
