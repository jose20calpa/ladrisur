from django.db import models
from apps.administrador.models import Proveedor, Combustible
import datetime
from datetime import date


class Pedido_combustible(models.Model):
    fecha_pedido = models.DateField(default=date.today)
    id_proveedor = models.ForeignKey(Proveedor)
    id_combustible = models.ForeignKey(Combustible)
    cantidad_pedido = models.PositiveIntegerField(blank=True, null=True)
    precio_pedido = models.PositiveIntegerField(blank=True, null=True)
    estado_pedido = models.CharField(default='Pendiente', max_length=20)


class Ingreso_combustible(models.Model):
    fecha_ingreso = models.DateField(default=datetime.datetime.today)
    id_pedido_combustible = models.ForeignKey(Pedido_combustible)
    cantidad_ingreso = models.IntegerField()
