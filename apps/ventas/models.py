from django.db import models
from django.db.models import IntegerChoices

from apps.personas.models import Persona
from apps.productos.models import Producto, Promocion, Vianda

from .managers import VentaPromocionManager, VentaProductoManager, VentaViandaManager


class Venta(models.Model):
    venta_id = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_upd = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='ventas')

    def __str__(self):
        return str(self.venta_id)   


class VentaDet(models.Model):
    
    class VentaType(IntegerChoices):
        VENTA = 1
        PROMOCION = 2
        VIANDA = 3
    
    venta_det_id = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas', null=True, blank=True)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, related_name='ventas_promocion', null=True, blank=True)
    vianda = models.ForeignKey(Vianda, on_delete=models.CASCADE, related_name='ventas_vianda', null=True, blank=True)
    tipo = models.SmallIntegerField(choices=VentaType.choices, default=VentaType.VENTA)
    precio = models.DecimalField(max_digits=18, decimal_places=2, default=0)    
    cantidad = models.DecimalField(max_digits=5, decimal_places=3)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_upd = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()  # The default manager.   

    class Meta:
        unique_together = ('venta', 'producto', 'promocion', 'vianda')

    def __str__(self):
        return f'{self.venta} - {self.producto}'

    @property
    def sub_total(self):
        return self.precio * self.cantidad


class VentaProducto(VentaDet):
    
    class Meta:
        proxy = True

    objects = VentaProductoManager()

    def save(self, *args, **kwargs):
        self.tipo = VentaDet.VentaType.VENTA
        self.precio = self.producto.precio_venta
        self.venta.total += self.sub_total
        self.venta.save()
        super().save(*args, **kwargs)


class VentaPromocion(VentaDet):
    
    class Meta:
        proxy = True

    objects = VentaPromocionManager()

    def save(self, *args, **kwargs):        
        self.tipo = VentaDet.VentaType.PROMOCION
        prom_prod = self.promocion.productos.all()

        self.precio = sum([p.producto.descuento_promocion(self.promocion) for p in prom_prod])
        self.venta.total += self.sub_total
        self.venta.save()

        super().save(*args, **kwargs)


class VentaVianda(VentaDet):

    objects = VentaViandaManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.tipo = VentaDet.VentaType.VIANDA
        self.precio = self.vianda.precio_venta
        self.venta.total += self.sub_total
        self.venta.save()

        super().save(*args, **kwargs)
