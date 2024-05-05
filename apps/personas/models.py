from django.db import models
from apps.core.models import DocTipo

# Create your models here.

class Persona(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=True)
    apellido = models.CharField(max_length=70, null=True, blank=True)
    tipo_doc = models.ForeignKey(DocTipo, on_delete=models.PROTECT, default=1, null=True, blank=True)
    nro_doc = models.CharField(max_length=9, null=True, blank=True)
    fec_nac = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    @property
    def domicilio(self):
        domicilio = self.domicilios.filter(prederterminado=True).first()
        return domicilio.direccion if domicilio else '-'
    
    @property
    def telefono(self):
        telefono = self.telefonos.filter(prederterminado=True).first()
        return telefono.telefono if telefono else '-'
    
    @property
    def email(self):
        email = self.emails.filter(prederterminado=True).first()
        return email.email if email else '-'
    

class PersonaEmail(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField(null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    prederterminado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.email}'
    
    def save(self, *args, **kwargs):
        if self.prederterminado:
            PersonaEmail.objects.filter(persona=self.persona, prederterminado=True).update(prederterminado=False)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'


class PersonaTelefono(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='telefonos')
    telefono = models.CharField(max_length=15, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    prederterminado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.telefono}'
    
    def save(self, *args, **kwargs):
        if self.prederterminado:
            PersonaTelefono.objects.filter(persona=self.persona, prederterminado=True).update(prederterminado=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Telefono'
        verbose_name_plural = 'Telefonos'


class PersonaDomicilio(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='domicilios')
    direccion = models.CharField(max_length=255, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    fecha_upd = models.DateField(auto_now=True)
    prederterminado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.direccion}'
    
    def save(self, *args, **kwargs):
        if self.prederterminado:
            PersonaDomicilio.objects.filter(persona=self.persona, prederterminado=True).update(prederterminado=False)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Domicilio'
        verbose_name_plural = 'Domicilios'