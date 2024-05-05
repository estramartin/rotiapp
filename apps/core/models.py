from django.db import models


class DocTipo(models.Model):
    tipo_doc_id = models.AutoField(primary_key=True)
    sigla = models.CharField(max_length=5, default='DNI')
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion