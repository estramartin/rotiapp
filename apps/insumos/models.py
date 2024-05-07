from django.db import models
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.conf import settings

from apps.ventas.models import VentaDet, VentaProducto, VentaPromocion, VentaVianda
from apps.core.tasks import send_mail


class Insumo(models.Model):
    insumo_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, null=True, blank=True)
    precio = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    unidad_media = models.CharField(max_length=255, choices=[('uni', 'unidad'), ('kg', 'kilogramos'), ('l', 'litros')])
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    

class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='stocks')
    cantidad = models.DecimalField(max_digits=18, decimal_places=2)
    minimo = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    notificar = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    
    
    def __str__(self):
        return f'{self.insumo} - {self.cantidad}'
    
    @property
    def unidad_medida(self):
        return self.insumo.unidad_media
    
    def save(self, *args, **kwargs):
        if self.cantidad > self.minimo and self.notificar:
            self.notificado = False
           
        super().save(*args, **kwargs)
    

class InsumoProveedor(models.Model):
    insumo_proveedor_id = models.AutoField(primary_key=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='proveedores')
    proveedor = models.ForeignKey('proveedores.Proveedor', on_delete=models.CASCADE, related_name='insumos')
    mensaje = models.TextField(null=True, blank=True)
    predeterminado = models.BooleanField(default=False)
    notificado = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.insumo} - {self.proveedor}'
    
    @property
    def unidad_medida(self):
        return self.insumo.unidad_media
    
    class Meta:
        unique_together = ('insumo', 'proveedor')


def send_notification(pi):
    pro_in = pi.insumo.proveedores.filter(predeterminado=True).first()
    if pro_in and not pro_in.notificado:
        send_mail(
            subject=f'Stock mínimo alcanzado de {pi.insumo.nombre}',
            message=pro_in.mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[pro_in.proveedor.email],
            fail_silently=False,
            html_message=None
        )
        pro_in.notificado = True
        pro_in.save()


def handle_created_instance(instance, pi, stock):
    stock.cantidad -= pi.cantidad * instance.cantidad
    if stock.cantidad < stock.minimo and stock.notificar:
        send_notification(pi)


def handle_updated_instance(instance, pi, stock):
    old_cantidad = getattr(instance, '_old_cantidad', instance.cantidad)
    difference = old_cantidad - instance.cantidad
    stock.cantidad += difference * pi.cantidad

@receiver(post_save, sender=VentaVianda)
@receiver(pre_save, sender=VentaProducto)
@receiver(pre_save, sender=VentaPromocion)
def store_old_quantity(sender, instance, **kwargs):    
    try:
        old_instance = VentaDet.objects.get(pk=instance.pk)
        instance._old_cantidad = old_instance.cantidad        
    except Exception:
        pass

@receiver(pre_save, sender=VentaProducto)
def update_stock(sender, instance, **kwargs):  
    prod_insumos = instance.producto.insumos.all()
    is_created = instance._state.adding
    for pi in prod_insumos:
        stock = Stock.objects.filter(insumo=pi.insumo).first()
        print(stock)
        if stock:
            if is_created:
                handle_created_instance(instance, pi, stock)
            else:
                handle_updated_instance(instance, pi, stock)
            stock.save()
    return True


@receiver(pre_save, sender=VentaPromocion)
def update_stock_promo(sender, instance, **kwargs):   
    productos_promo = instance.promocion.productos.all()
    is_created = instance._state.adding
    for producto_promo in productos_promo:
        prod_insumos = producto_promo.producto.insumos.all()
        for pi in prod_insumos:
            stock = Stock.objects.filter(insumo=pi.insumo).first()            
            if stock:
                if is_created:
                    handle_created_instance(instance, pi, stock)
                else:
                    handle_updated_instance(instance, pi, stock)
                stock.save()   
    return True

@receiver(pre_save, sender=VentaVianda)
def update_stock_vianda(sender, instance, **kwargs):   
    productos_vianda = instance.vianda.productos.all()
    is_created = instance._state.adding
    for producto_vianda in productos_vianda:
        prod_insumos = producto_vianda.producto.insumos.all()
        for pi in prod_insumos:
            stock = Stock.objects.filter(insumo=pi.insumo).first()            
            if stock:
                if is_created:
                    handle_created_instance(instance, pi, stock)
                else:
                    handle_updated_instance(instance, pi, stock)
                stock.save()   
    return True


@receiver(pre_delete, sender=VentaDet)
def restore_stock(sender, instance, **kwargs):
    tipo_to_attr = {1: 'producto', 2: 'promocion', 3: 'vianda'} 
    if instance.tipo != 1:
        attr = tipo_to_attr.get(instance.tipo)
        productos_instance = getattr(instance, attr).productos.all() if attr else []
        
        for producto_instance in productos_instance:
            insumos = producto_instance.producto.insumos.all()
            for pi in insumos:
                stock = Stock.objects.filter(insumo=pi.insumo).first()
                if stock:
                    stock.cantidad += pi.cantidad * instance.cantidad
                    stock.save()
    else:
        insumos = instance.producto.insumos.all()    
        for pi in insumos:
            stock = Stock.objects.filter(insumo=pi.insumo).first()
            if stock:
                stock.cantidad += pi.cantidad * instance.cantidad
                stock.save()
    return True
