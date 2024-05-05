from django.contrib import admin
from apps.personas.models import Persona, PersonaEmail, PersonaTelefono, PersonaDomicilio

# Register your models here.


class PersonaMailInline(admin.TabularInline):
    model = PersonaEmail
    extra = 1
    max_num = 3


class PersonaTelefonoInline(admin.TabularInline):
    model = PersonaTelefono
    extra = 1
    max_num = 3


class PersonaDomicilioInline(admin.TabularInline):
    model = PersonaDomicilio
    extra = 1
    max_num = 3


class PersonaAdmin(admin.ModelAdmin):
    model = Persona
    list_display = ['pk', 'nombre', 'apellido', 'tipo_doc', 'nro_doc', 'fec_nac']
    list_filter = ['tipo_doc',]
    search_fields = ['nombre', 'apellido', 'nro_doc']
    list_per_page = 50
    inlines = [
        PersonaMailInline,
        PersonaTelefonoInline,
        PersonaDomicilioInline,
    ]

admin.site.register(Persona, PersonaAdmin)