from django.db import models


# Create your models here.


class Insumo(models.Model):
    insumo_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, null=True, blank=True)
    precio = models.FloatField()
    unidad_media = models.CharField(max_length=255, choices=[('uni', 'unidad'), ('kg', 'kilogramos'), ('l', 'litros')])
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    

class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='stocks')
    cantidad = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    
    def __str__(self):
        return f'{self.insumo} - {self.cantidad}'
    
    @property
    def unidad_medida(self):
        return self.insumo.unidad_media
    

class InsumoProveedor(models.Model):
    insumo_proveedor_id = models.AutoField(primary_key=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='proveedores')
    proveedor = models.ForeignKey('proveedores.Proveedor', on_delete=models.CASCADE, related_name='insumos')
    
    def __str__(self):
        return f'{self.insumo} - {self.proveedor}'
    
    @property
    def unidad_medida(self):
        return self.insumo.unidad_media


