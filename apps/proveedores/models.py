from django.db import models
from apps.personas.models import Persona


class Proveedor(Persona):
    proveedor_id = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
      
