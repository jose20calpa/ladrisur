from django.db import models
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator

from django.core.validators import MinValueValidator

#from apps.produccion.models import Ingreso_produccion_verde


class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100, unique=True)
    estado_producto = models.CharField(default='Activo', max_length=50, choices=(
        ('Activo', 'Activo'), ('Inactvio', 'Inactvio')))
    rendimiento_producto = models.FloatField(
        validators=[MinValueValidator(0.1)])
    alto_producto = models.FloatField(validators=[MinValueValidator(0.1)])
    ancho_producto = models.FloatField(validators=[MinValueValidator(0.1)])
    largo_producto = models.FloatField(validators=[MinValueValidator(0.1)])
    peso_producto = models.FloatField(validators=[MinValueValidator(0.1)])
    precio_fabrica_primera = models.PositiveIntegerField(default=0)
    precio_obra_primera = models.PositiveIntegerField(default=0)
    precio_fabrica_segunda = models.PositiveIntegerField(default=0)
    precio_obra_segunda = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['nombre_producto']

    def __str__(self):
        return self.nombre_producto

    def get_absolute_url(self):
        return reverse('mod-emp', kwargs={'pk': self.id})


class Producto_Categoria(models.Model):
    nombre_categoria = models.CharField(blank=True, max_length=50)
    id_producto = models.ForeignKey(
        Producto, null=True, )
    cantidad_producto = models.PositiveIntegerField(default=0)


class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100, unique=True)
    identificacion_proveedor = models.CharField(max_length=100, unique=True)
    direccion_proveedor = models.CharField(blank=True, max_length=150)
    telefono_proveedor = models.CharField(blank=True, max_length=100)
    correo_proveedor = models.EmailField(blank=True)

    class Meta:
        ordering = ['nombre_proveedor']


class Cargo(models.Model):
    codigo_cargo_DANE = models.CharField(
        blank=True, max_length=10, unique=True)
    nombre_cargo = models.CharField(max_length=100, unique=True)
    horas_semana = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['nombre_cargo']

    def __str__(self):
        return self.nombre_cargo


class Empleado(models.Model):
    cedula_empleado = models.CharField(max_length=12, unique=True)
    nombre_empleado = models.CharField(max_length=100)
    apellido_empleado = models.CharField(max_length=100)
    telefono_empleado = models.CharField(blank=True, max_length=100)
    direccion_empleado = models.CharField(blank=True, max_length=100)
    correo_empleado = models.EmailField(blank=True, max_length=20)
    id_cargo = models.ForeignKey(Cargo)

    class Meta:
        ordering = ['apellido_empleado', 'nombre_empleado']

    def __str__(self):
        return self.nombre_empleado

# El Modelo Usuario se relaciona con User o auth.user el cual es un modelo
# de django


class Usuario(User):
    id_empleado = models.OneToOneField(Empleado, blank=True, null=True)


class Combustible(models.Model):
    nombre_combustible = models.CharField(max_length=100, unique=True)
    uso = models.CharField(max_length=100, choices=(
        ('Hornos', 'Hornos'), ('Maquinas', 'Maquinas')))
    unidad_combustible = models.CharField(max_length=50, choices=(
        ('Galones', 'Galones'), ('Kilogramos', 'Kilogramos'), ('Metros Cubicos', 'Metros ubicos')))
    cantidad_total_combustible = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['nombre_combustible', 'uso']

    def __str__(self):
        return self.nombre_combustible


class Horno(models.Model):
    nombre_horno = models.CharField(max_length=20, unique=True)
    numero_bocas = models.IntegerField(null=True)
    estado_horno = models.CharField(default='Inactivo', max_length=15)

    class Meta:
        ordering = ['nombre_horno', '-estado_horno']

    def __str__(self):
        return self.nombre_horno


class Secadero(models.Model):
    nombre_secadero = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['nombre_secadero']

    def __str__(self):
        return self.nombre_secadero


class Maquina(models.Model):
    marca_maquina = models.CharField(max_length=20, null=True, blank=True)
    año_maquina = models.IntegerField(blank=True, null=True, validators=[
        RegexValidator(regex='^\d{4}$', message='Un año solo tiene 4 digitos!!', code='invalid number')])
    modelo_maquina = models.CharField(blank=True, max_length=100)
    tipo_maquina = models.CharField(default='No registra', max_length=20, choices=(
        ('Retroexcavadora', 'Retroexcavadora'), ('Cargador', 'Cargador')))

    class Meta:
        ordering = ['tipo_maquina', 'marca_maquina']

    def __str__(self):
        return self.marca_maquina


class Vehiculo(models.Model):
    marca_vehiculo = models.CharField(max_length=20, null=True, blank=True)
    año_vehiculo = models.IntegerField(blank=True, null=True, validators=[
        RegexValidator(regex='^\d{4}$', message='Un año solo tiene 4 digitos!!', code='invalid number')])
    modelo_vehiculo = models.CharField(blank=True, max_length=100)
    matricula_vehiculo = models.CharField(blank=True, max_length=10,)
    tipo_vehiculo = models.CharField(default='No registra', max_length=20, choices=(
        ('Camión', 'Camión'), ('Volqueta', 'Volqueta'),
    ))

    class Meta:
        ordering = ['marca_vehiculo', 'año_vehiculo']

    def __str__(self):
        return self.marca_vehiculo
