from django.db import models
from datetime import datetime
from apps.personas.models import Persona



class Empleado(Persona):
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField(null=True, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)   
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    

class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2)
    valor_antiguedad = models.DecimalField(max_digits=10, decimal_places=2)
    aportes = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class EmpleadoCategoria(models.Model):
    emp_cat_id = models.AutoField(primary_key=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='empleados')
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.empleado} - {self.categoria}'
       
    @property
    def antiguedad(self):
        fecha_ingreso = self.empleado.fecha_ingreso
        return self.fecha.year - fecha_ingreso.year - ((self.fecha.month, self.fecha.day) < (fecha_ingreso.month, fecha_ingreso.day))
    
    @property
    def valor_antiguedad(self):
        return self.categoria.valor_antiguedad * self.antiguedad
    
    def valor_total_mensual(self, horas_trabajadas, antiguedad=True, semanal=None):
        sueldo = (self.categoria.valor_hora * horas_trabajadas)
        if not antiguedad:
            return sueldo
        
        valor_antiguedad = self.valor_antiguedad if not semanal else self.valor_antiguedad / 4
        bruto = sueldo + valor_antiguedad
        aportes = bruto * (self.categoria.aportes / 100)
        neto = bruto - aportes
        return neto
    
    def diario_minutos_sin_antiguedad(self, minutos):
        return self.valor_total_mensual(minutos / 60, antiguedad=False)
    
    def valor_total_semanal(self, horas_trabajadas):
        return self.valor_total_mensual(horas_trabajadas, antiguedad=True, semanal=True)