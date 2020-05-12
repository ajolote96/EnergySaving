from django.db import models

# Create your models here. 

class RegistroMinuto(models.Model):
    irms = models.CharField(verbose_name="Irms", max_length=10, null=True)
    voltaje = models.CharField(verbose_name="Voltaje", max_length=10, null=True)
    watts = models.CharField(verbose_name="Watts", max_length=10, null=True)
    intencidadPico = models.CharField(verbose_name="IntencidadPico", max_length=10, null=True)
    fecha = models.DateField(verbose_name='Fecha de creación', null=True)
    hora = models.TimeField(verbose_name='Hora de creación', null=True)

    class Meta:
        verbose_name = 'RegistroMinuto'
        verbose_name_plural = "RegistrosMinuto"
        ordering = ['-fecha']

    def __str__(self):
        return str(self.fecha)

class AutonomoConfig(models.Model):
    horaInicio = models.IntegerField(verbose_name="Hora de inicio", null=False)
    horaFin = models.IntegerField(verbose_name="Hora de fin", null=False)
    activado =  models.BooleanField(verbose_name="Activado", null=False)

    class Meta:
        verbose_name = "Configuracion del la Autonomia"
    
    def __str__(self):
        return "Configuracion de Autonomia"
