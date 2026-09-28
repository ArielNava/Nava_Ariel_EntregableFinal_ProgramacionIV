from django.db import models
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=50, default='computadora')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_existente = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=3)
    descripcion = models.TextField(blank=True, default='', verbose_name="Descripción corta")
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
class ConsultaIA(models.Model):
    pregunta = models.TextField()
    respuesta = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
