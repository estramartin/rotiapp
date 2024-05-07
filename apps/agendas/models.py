from django.db import models


class Agenda(models.Model):
    agenda_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    activo = models.BooleanField(default=True)    
    
    def __str__(self):
        return self.nombre


class AgendaFecha(models.Model):
    vianda_fechas_id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    activo = models.BooleanField(default=True)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, related_name='fechas')
    
    def __str__(self):
        return str(self.fecha)