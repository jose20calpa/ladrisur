from django.db import models
from apps.administrador.models import Empleado, Producto, Horno, Vehiculo, Maquina, Combustible, Secadero
from apps.ventas.models import Venta
import datetime
from datetime import date

# Create your models here.


class Produccion_verde(models.Model):
    fecha_produccion_verde = models.DateField(
        default=date.today, blank=True, null=True)

    def __str__(self):
        fecha_produccion_verde = self.fecha.strftime("%Y-%m-%d")
        return fecha_produccion_verde


class Ingreso_produccion_verde(models.Model):
    id_producto = models.ForeignKey(
        Producto, blank=True, null=True)
    cantidad_producto = models.PositiveIntegerField(blank=True, null=True)
    id_produccion_verde = models.ForeignKey(Produccion_verde)


class Quema(models.Model):
    id_horno = models.ForeignKey(Horno)
    estado_quema = models.CharField(
        blank=True, default='Iniciada', max_length=100)


class Entrada_quema(models.Model):
    id_quema = models.OneToOneField(Quema)
    fecha_encendido = models.DateField(default=date.today)
    hora_encendido = models.TimeField(blank=True, null=True)


class Entrada_quema_producto(models.Model):
    id_entrada_quema = models.ForeignKey(Entrada_quema)
    id_producto = models.ForeignKey(
        Producto, blank=True, null=True)
    cantidad_verde = models.PositiveIntegerField(blank=True, null=True)


class Salida_quema(models.Model):
    id_entrada_quema = models.OneToOneField(Entrada_quema)
    fecha_apagado = models.DateField(blank=True, null=True, default=date.today)
    hora_apagado = models.TimeField(blank=True, null=True)
    id_empleado = models.ManyToManyField(Empleado, blank=True, null=True)


class Salida_quema_producto(models.Model):
    id_salida_quema = models.ForeignKey(Salida_quema)
    id_producto = models.ForeignKey(
        Producto, null=True)
    cantidad_primera = models.PositiveIntegerField(
        blank=True, null=True, default=0)
    cantidad_segunda = models.PositiveIntegerField(
        blank=True, null=True, default=0)
    cantidad_crudo = models.PositiveIntegerField(
        blank=True, null=True, default=0)
    cantidad_verde = models.PositiveIntegerField(
        blank=True, null=True, default=0)
    cantidad_dañados = models.PositiveIntegerField(
        blank=True, null=True, default=0)


class Quema_combustible(models.Model):
    id_quema = models.ForeignKey(Quema)
    id_combustible = models.ForeignKey(Combustible)
    cantidad_combustible = models.IntegerField()


class Secado(models.Model):
    fecha_secado = models.DateField(blank=True, null=True, default=date.today)
    id_secadero = models.ForeignKey(Secadero)


class Secado_combustible(models.Model):
    id_secado = models.ForeignKey(Secado)
    id_combustible = models.ForeignKey(Combustible, blank=True)
    cantidad_combustible = models.PositiveIntegerField(blank=True)


class Tanqueo (models.Model):
    fecha_tanqueo = models.DateField(default=date.today, blank=True, null=True)
    id_maquina = models.ForeignKey(Maquina)
    id_combustible = models.ForeignKey(Combustible, blank=True, null=True)
    cantidad_tanqueo = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.fecha_tanqueo


class Entrega_obra (models.Model):
    id_empleado = models.ManyToManyField(Empleado, blank=True, null=True,)
    id_vehiculo = models.ManyToManyField(Vehiculo, blank=True, null=True,)
    id_venta = models.ForeignKey(Venta, blank=True, null=True)
    fecha_entrega_obra = models.DateField(default=date.today)
    codigo_recibo_obra = models.CharField(blank=True, max_length=20)
    nombre_recibo_obra = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.codigo_recibo_obra


class Entrega_fabrica (models.Model):
    id_venta = models.ForeignKey(Venta, blank=True, null=True)
    fecha_entrega_fabrica = models.DateField(default=date.today)
    codigo_recibo_fabrica = models.CharField(blank=True, max_length=20)
    nombre_recibo_fabrica = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.codigo_recibo_fabrica
