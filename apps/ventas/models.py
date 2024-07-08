import uuid
import qrcode
import mercadopago

from io import BytesIO
from django.utils.safestring import mark_safe
from django.core.files import File
from django.db import models
from django.db.models import IntegerChoices
from django.conf import settings

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
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return str(self.venta_id)   

    def save(self, *args, **kwargs):
        if not self.qr_code:
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            preference_data = {
                "items": [
                    {
                        "title": "Nombre del producto o servicio",
                        "quantity": 1,
                        "unit_price": round(float(1000.00), 2),  # Asegúrate de tener un precio en tu modelo Venta
                    }
                ]
            }
            preference_response = sdk.preference().create(preference_data)
            url = preference_response['response']['init_point']
            print(url)
            # url = f"{settings.BASE_URL}/api/v1/ventaqr/{self.code}/process"
            qr = qrcode.make(url)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            file_name = f"{self.code}.png"
            self.qr_code.save(file_name, File(buffer), save=False)
            super().save(*args, **kwargs)

    def qr_code_tag(self):
        if self.qr_code:           
            return mark_safe(f'<img src="{self.qr_code.url}" width="150" height="150" />')
        return "No QR code available"

    qr_code_tag.short_description = 'QR Code'
    qr_code_tag.allow_tags = True

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
