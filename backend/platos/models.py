from django.db import models
class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=10, default="")  # Emoji o icono
    puntuacion = models.IntegerField(default=0)
    seleccionado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.TextField()
    descripcion = models.TextField()
    puntuacion = models.IntegerField()  # 1 a 10
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    ingredientes = models.ManyToManyField(Ingrediente, related_name='platos')

    def __str__(self):
        return self.nombre