from django.contrib import admin
from apps.core import models


class DocTipoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'sigla')
    search_fields = ('descripcion', 'sigla')
    ordering = ('descripcion', 'sigla')

    def has_module_permission(self, request):
        return request.user.is_superuser


admin.site.register(models.DocTipo, DocTipoAdmin)
