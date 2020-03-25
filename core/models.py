from django.db import models

# Create your models here. 

class Registro(models.Model):
    title = models.CharField(verbose_name="Titulo", max_length=100)
    description = models.TextField(verbose_name="Descripción", null=True, blank=True)
    "Datos de almacenaje"
    irms = models.CharField(verbose_name="Irms", max_length=10, null=True)
    voltaje = models.CharField(verbose_name="Voltaje", max_length=10, null=True)
    watts = models.CharField(verbose_name="Watts", max_length=10, null=True)
    intencidadPico = models.CharField(verbose_name="IntencidadPico", max_length=10, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = "Registros"
        ordering = ['created']

    def __str__(self):
        return self.title