from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

class Evento(models.Model):
  tituloEvento = models.CharField("Evento", max_length=255, default="Evento")
  fechaEvento = models.DateField("Fecha del evento")
  activo = models.BooleanField("Activo", default=True)
  apuntados = models.JSONField(null=True, blank=True)
  siguienteEvento = models.ForeignKey('self', on_delete=SET_NULL, null=True, blank=True, verbose_name="Siguiente evento")
  permitirAlergenos = models.BooleanField(default=False, verbose_name="Permitir alérgenos")
  alergenos = models.JSONField(null=True, blank=True, verbose_name="Lista de alérgenos")

  def __str__(self):
    return self.tituloEvento

class Usuario(models.Model):
  dni = models.CharField(max_length=15, verbose_name="DNI", primary_key=True)
  nombre = models.CharField(max_length=255, verbose_name="Nombre")
  apellidos = models.CharField(max_length=255, verbose_name="Apellidos")

  def __str__(self):
    return self.nombre

class Seleccion(models.Model):
  idEvento = models.ForeignKey(Evento, on_delete=CASCADE)
  cena = models.CharField(max_length=100, verbose_name="Evento")
  recuento = models.IntegerField(default=0)
  usuarios = models.JSONField(null=True, blank=True)

  def __str__(self):
    return self.cena
