# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-13 21:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrador', '0001_initial'),
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada_quema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_encendido', models.DateField(default=datetime.date.today)),
                ('hora_encendido', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Entrada_quema_producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_verde', models.PositiveIntegerField(blank=True, null=True)),
                ('id_entrada_quema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.Entrada_quema')),
                ('id_producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrador.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Entrega_fabrica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrega_fabrica', models.DateField(default=datetime.date.today)),
                ('codigo_recibo_fabrica', models.CharField(blank=True, max_length=20)),
                ('nombre_recibo_fabrica', models.CharField(blank=True, max_length=100)),
                ('id_venta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.Venta')),
            ],
        ),
        migrations.CreateModel(
            name='Entrega_obra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrega_obra', models.DateField(default=datetime.date.today)),
                ('codigo_recibo_obra', models.CharField(blank=True, max_length=20)),
                ('nombre_recibo_obra', models.CharField(blank=True, max_length=100)),
                ('id_empleado', models.ManyToManyField(blank=True, null=True, to='administrador.Empleado')),
                ('id_vehiculo', models.ManyToManyField(blank=True, null=True, to='administrador.Vehiculo')),
                ('id_venta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.Venta')),
            ],
        ),
        migrations.CreateModel(
            name='Ingreso_produccion_verde',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_producto', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produccion_verde',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_produccion_verde', models.DateField(blank=True, default=datetime.date.today, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_quema', models.CharField(blank=True, default='Iniciada', max_length=100)),
                ('id_horno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.Horno')),
            ],
        ),
        migrations.CreateModel(
            name='Quema_combustible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_combustible', models.IntegerField()),
                ('id_combustible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.Combustible')),
                ('id_quema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.Quema')),
            ],
        ),
        migrations.CreateModel(
            name='Salida_quema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_apagado', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('hora_apagado', models.TimeField(blank=True, null=True)),
                ('id_empleado', models.ManyToManyField(blank=True, null=True, to='administrador.Empleado')),
                ('id_entrada_quema', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='produccion.Entrada_quema')),
            ],
        ),
        migrations.CreateModel(
            name='Salida_quema_producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_primera', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('cantidad_segunda', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('cantidad_crudo', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('cantidad_verde', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('cantidad_dañados', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('id_producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrador.Producto')),
                ('id_salida_quema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.Salida_quema')),
            ],
        ),
        migrations.CreateModel(
            name='Secado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_secado', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('id_secadero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.Secadero')),
            ],
        ),
        migrations.CreateModel(
            name='Secado_combustible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_combustible', models.PositiveIntegerField(blank=True)),
                ('id_combustible', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='administrador.Combustible')),
                ('id_secado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.Secado')),
            ],
        ),
        migrations.CreateModel(
            name='Tanqueo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_tanqueo', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('cantidad_tanqueo', models.PositiveIntegerField(blank=True, null=True)),
                ('id_combustible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrador.Combustible')),
                ('id_maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.Maquina')),
            ],
        ),
        migrations.AddField(
            model_name='ingreso_produccion_verde',
            name='id_produccion_verde',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.Produccion_verde'),
        ),
        migrations.AddField(
            model_name='ingreso_produccion_verde',
            name='id_producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrador.Producto'),
        ),
        migrations.AddField(
            model_name='entrada_quema',
            name='id_quema',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='produccion.Quema'),
        ),
    ]
