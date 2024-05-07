from datetime import date
from django.db import models
from apps.agendas.models import Agenda
from apps.productos.models import Vianda


class VentaPromocionManager(models.Manager):
    def get_queryset(self):        
        return super().get_queryset().filter(tipo=2)
    

class VentaProductoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo=1)
    

class VentaViandaManager(models.Manager):
    def get_queryset(self):         
        return super().get_queryset().filter(tipo=3)