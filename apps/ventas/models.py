from django.db import models
from apps.administrador.models import Empleado, Producto
import datetime

# Create your models here


class Cliente(models.Model):
    identificacion_cliente = models.CharField(max_length=50, unique=True)
    nombre_cliente = models.CharField(max_length=50,)
    apellido_cliente = models.CharField(max_length=50, blank=True)
    direccion_cliente = models.CharField(max_length=50, blank=True)
    telefono_cliente = models.CharField(max_length=50, blank=True)
    correo_cliente = models.EmailField(blank=True)


class Venta(models.Model):
    fecha_venta = models.DateField(default=datetime.datetime.today)
    fecha_hora = models.DateTimeField(blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente)
    id_empleado = models.ForeignKey(Empleado)
    domicilio_obra = models.CharField(blank=True, max_length=100)
    estado_venta = models.CharField(default="Pendiente",  max_length=100)
    tipo_venta = models.CharField(blank=True, max_length=100)
    total_venta = models.PositiveIntegerField()


class Venta_producto(models.Model):
    id_venta = models.ForeignKey(Venta)
    id_producto = models.ForeignKey(Producto)
    cantidad_producto = models.PositiveIntegerField()
    precio_producto = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
