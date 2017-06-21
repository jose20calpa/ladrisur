from django.contrib import admin
from apps.administrador.models import *
import datetime
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
#
# # Register your models here.


admin.site.register(Producto)
admin.site.register(Producto_Categoria)
admin.site.register(Proveedor)
admin.site.register(Cargo)
admin.site.register(Empleado)
admin.site.register(Usuario)
admin.site.register(Combustible)
admin.site.register(Horno)
admin.site.register(Secadero)
admin.site.register(Maquina)
admin.site.register(Vehiculo)
