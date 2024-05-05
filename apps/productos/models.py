from django.db import models


class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    margen = models.FloatField(default=0.3)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
    @property
    def precio_costo(self):
        return sum([pi.insumo.precio * pi.cantidad for pi in self.insumos.all()])
    
    @property
    def precio_venta(self):
        categoria = self.categorias.first()
        
        if categoria and categoria.categoria.is_precio_standar:
            return categoria.categoria.precio_standar
        return self.precio_costo * (1 + self.margen)
    

class ProductoInsumo(models.Model):
    producto_insumo_id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='insumos')
    insumo = models.ForeignKey('insumos.Insumo', on_delete=models.CASCADE, related_name='productos')
    cantidad = models.FloatField(blank=False, null=False)    
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.producto} - {self.insumo}'
    
    @property
    def precio_costo(self):
        if self.cantidad is not None:
            return self.insumo.precio * self.cantidad
        else:
            return 0
    
    @property
    def insumo_precio(self):
        return self.insumo.precio
    
    @property
    def insumo_unidad_medida(self):
        return self.insumo.unidad_media
    
    
class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio_standar = models.FloatField(null=True, blank=True)
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
    descuento = models.FloatField()
    fecha_inicio = models.DateField(auto_now=True)
    fecha_fin = models.DateField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    

class PromocionProducto(models.Model):

    prom_prod_id = models.AutoField(primary_key=True)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='promociones')
    
    def __str__(self):
        return f'{self.promocion} - {self.producto}'
    
    @property
    def precio_promocion(self):
        return self.producto.precio_venta * (1 - self.promocion.descuento)