# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-13 21:45
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_cargo_DANE', models.CharField(blank=True, max_length=10, unique=True)),
                ('nombre_cargo', models.CharField(max_length=100, unique=True)),
                ('horas_semana', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['nombre_cargo'],
            },
        ),
        migrations.CreateModel(
            name='Combustible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_combustible', models.CharField(max_length=100, unique=True)),
                ('uso', models.CharField(choices=[('Hornos', 'Hornos'), ('Maquinas', 'Maquinas')], max_length=100)),
                ('unidad_combustible', models.CharField(choices=[('Galones', 'Galones'), ('Kilogramos', 'Kilogramos'), ('Metros Cubicos', 'Metros ubicos')], max_length=50)),
                ('cantidad_total_combustible', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['nombre_combustible', 'uso'],
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula_empleado', models.CharField(max_length=12, unique=True)),
                ('nombre_empleado', models.CharField(max_length=100)),
                ('apellido_empleado', models.CharField(max_length=100)),
                ('telefono_empleado', models.CharField(blank=True, max_length=100)),
                ('direccion_empleado', models.CharField(blank=True, max_length=100)),
                ('correo_empleado', models.EmailField(blank=True, max_length=20)),
                ('id_cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.Cargo')),
            ],
            options={
                'ordering': ['apellido_empleado', 'nombre_empleado'],
            },
        ),
        migrations.CreateModel(
            name='Horno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_horno', models.CharField(max_length=20, unique=True)),
                ('numero_bocas', models.IntegerField(null=True)),
                ('estado_horno', models.CharField(default='Inactivo', max_length=15)),
            ],
            options={
                'ordering': ['nombre_horno', '-estado_horno'],
            },
        ),
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca_maquina', models.CharField(blank=True, max_length=20, null=True)),
                ('año_maquina', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(code='invalid number', message='Un año solo tiene 4 digitos!!', regex='^\\d{4}$')])),
                ('modelo_maquina', models.CharField(blank=True, max_length=100)),
                ('tipo_maquina', models.CharField(choices=[('Retroexcavadora', 'Retroexcavadora'), ('Cargador', 'Cargador')], default='No registra', max_length=20)),
            ],
            options={
                'ordering': ['tipo_maquina', 'marca_maquina'],
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=100, unique=True)),
                ('estado_producto', models.CharField(choices=[('Activo', 'Activo'), ('Inactvio', 'Inactvio')], default='Activo', max_length=50)),
                ('rendimiento_producto', models.FloatField(validators=[django.core.validators.MinValueValidator(0.1)])),
                ('alto_producto', models.FloatField(validators=[django.core.validators.MinValueValidator(0.1)])),
                ('ancho_producto', models.FloatField(validators=[django.core.validators.MinValueValidator(0.1)])),
                ('largo_producto', models.FloatField(validators=[django.core.validators.MinValueValidator(0.1)])),
                ('peso_producto', models.FloatField(validators=[django.core.validators.MinValueValidator(0.1)])),
                ('precio_fabrica_primera', models.PositiveIntegerField(default=0)),
                ('precio_obra_primera', models.PositiveIntegerField(default=0)),
                ('precio_fabrica_segunda', models.PositiveIntegerField(default=0)),
                ('precio_obra_segunda', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['nombre_producto'],
            },
        ),
        migrations.CreateModel(
            name='Producto_Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_categoria', models.CharField(blank=True, max_length=50)),
                ('cantidad_producto', models.PositiveIntegerField(default=0)),
                ('id_producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrador.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proveedor', models.CharField(max_length=100, unique=True)),
                ('identificacion_proveedor', models.CharField(max_length=100, unique=True)),
                ('direccion_proveedor', models.CharField(blank=True, max_length=150)),
                ('telefono_proveedor', models.CharField(blank=True, max_length=100)),
                ('correo_proveedor', models.EmailField(blank=True, max_length=254)),
            ],
            options={
                'ordering': ['nombre_proveedor'],
            },
        ),
        migrations.CreateModel(
            name='Secadero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_secadero', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'ordering': ['nombre_secadero'],
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('id_empleado', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrador.Empleado')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca_vehiculo', models.CharField(blank=True, max_length=20, null=True)),
                ('año_vehiculo', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(code='invalid number', message='Un año solo tiene 4 digitos!!', regex='^\\d{4}$')])),
                ('modelo_vehiculo', models.CharField(blank=True, max_length=100)),
                ('matricula_vehiculo', models.CharField(blank=True, max_length=10)),
                ('tipo_vehiculo', models.CharField(choices=[('Camión', 'Camión'), ('Volqueta', 'Volqueta')], default='No registra', max_length=20)),
            ],
            options={
                'ordering': ['marca_vehiculo', 'año_vehiculo'],
            },
        ),
    ]