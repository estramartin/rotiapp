from django.db import models
from apps.agendas.models import Agenda

class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    margen = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
    @property
    def precio_costo(self):
        return round(sum([pi.insumo.precio * pi.cantidad for pi in self.insumos.all()]), 2)
    
        
    @property
    def precio_venta(self):
        categoria = self.categorias.first()
        
        if categoria and categoria.categoria.is_precio_standar:
            return categoria.categoria.precio_standar
        return round(self.precio_costo * (1 + self.margen), 2)
    

    def descuento_promocion(self, promocion):
        return self.precio_venta - (self.precio_venta * promocion.descuento)


class ProductoInsumo(models.Model):
    producto_insumo_id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='insumos')
    insumo = models.ForeignKey('insumos.Insumo', on_delete=models.CASCADE, related_name='productos')
    cantidad = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False)    
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.producto} - {self.insumo}'
    
    @property
    def precio_costo(self):
        if self.cantidad is not None:
            return round(self.insumo.precio * self.cantidad, 2)
        else:
            return 0

    @property
    def insumo_precio(self):
        return round(self.insumo.precio, 2)

    @property
    def insumo_unidad_medida(self):
        return self.insumo.unidad_media
    
    
class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio_standar = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    is_precio_standar = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
    

class CategoriaProducto(models.Model):
    cat_prod_id = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='categorias')
    
    def __str__(self):
        return f'{self.categoria} - {self.producto}'
    
    class Meta:
        unique_together = ('categoria', 'producto')
    

class Promocion(models.Model):
    promocion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    descuento = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    fecha_inicio = models.DateField(auto_now=True)
    fecha_fin = models.DateField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Promoción unica'
        verbose_name_plural = 'Promociones varias'
    

class PromocionProducto(models.Model):

    prom_prod_id = models.AutoField(primary_key=True)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='promociones')
    
    def __str__(self):
        return f'{self.promocion} - {self.producto}'
    
    @property
    def precio_promocion(self):
        return self.producto.precio_venta * (1 - self.promocion.descuento)


class Vianda(models.Model):
    vianda_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    activo = models.BooleanField(default=True)
    agenda = models.ForeignKey(Agenda, related_name='viandas', on_delete=models.CASCADE)
    precio_standar = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Vianda'
        verbose_name_plural = 'Viandas'
        unique_together = ('nombre', 'agenda')

    def __str__(self):
        return self.nombre
    
    @property
    def precio_venta(self):
        if self.precio_standar:
            return self.precio_standar
        return round(sum([p.producto.precio_venta for p in self.productos.all()]), 2)
    
    @property
    def precio_venta_real(self):
        return round(sum([p.producto.precio_venta for p in self.productos.all()]), 2)


class ViandaProducto(models.Model):
    vianda_prod_id = models.AutoField(primary_key=True)
    vianda = models.ForeignKey(Vianda, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='viandas')
    
    def __str__(self):
        return f'{self.vianda} - {self.producto}'
    
    class Meta:
        unique_together = ('vianda', 'producto')
    
    @property
    def precio_venta(self):
        return round(self.producto.precio_venta, 2)
