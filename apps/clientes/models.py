from django.db import models
from apps.personas.models import Persona
from apps.productos.models import Vianda
from datetime import datetime


class Cliente(Persona):
    cuenta_corriente = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_alta = models.DateField(auto_now_add=True)
    fecha_baja = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class ClienteVianda(models.Model):
    cliente_vianda_id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='viandas')
    vianda = models.ForeignKey(Vianda, on_delete=models.CASCADE, related_name='clientes')
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.cliente} - {self.vianda}'

    class Meta:
        verbose_name = 'Cliente Vianda'
        verbose_name_plural = 'Clientes Viandas'
        ordering = ['cliente__nombre', 'vianda__nombre']

    @classmethod
    def vianda_count(cls):
        today = datetime.today()
        return cls.objects.filter(vianda__agenda__fechas__fecha=today).count()
