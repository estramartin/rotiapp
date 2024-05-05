from django.db import models

from apps.personas.models import Persona
from apps.productos.models import Producto


class Venta(models.Model):
    venta_id = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    total = models.FloatField(default=0.0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.venta_id)   
                     

class VentaDet(models.Model):
    venta_det_id = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas')
    precio = models.FloatField(default=0.0)
    cantidad = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.venta} - {self.producto}'

    @property
    def sub_total(self):
        return self.precio * self.cantidad
  
    def save(self, *args, **kwargs):
        self.precio = self.producto.precio_venta
        self.venta.total += self.sub_total
        self.venta.save()
        super().save(*args, **kwargs)


