from apps.administrador.models import *
from apps.produccion.models import *

from django.shortcuts import render, redirect, get_object_or_404

# validacion para verificar la cantidad de producto verde disponible


def validar_cantidad_producto(ids_prod, arr_can):
    arr_can_aux = arr_can[:]
    ban = True
    for reg in ids_prod:
        if ban:
            for can in arr_can_aux:
                producto = get_object_or_404(Producto, pk=reg)
                prod_cat = Producto_Categoria.objects.filter(
                    id_producto=producto, nombre_categoria='verde')
                if can < prod_cat[0].cantidad_producto:
                    ban = True
                else:
                    ban = False
                    break
            arr_can_aux.pop(0)
        else:
            break
    return ban

# validacion para buscar un producto en un arreglo


def buscar_producto(consulta, id_prod):
    ban = False
    for i in consulta:
        if i.id_producto == id_prod:
            ban = True
            break
    return ban

# funcion para convertir una hora de formato de 12 horas a formato de 24 horas


def convert_to_24(time):
    if len(str(time)) == 7:
        time = '0' + time
    if time[-2:] == "AM":
        if int(time[:2]) == 12:
            time = time.replace('12', '00')
        return time[0:5]
    else:
        if int(time[:2]) == 12:
            time = time.replace('12', '12')
            return time[0:5]
        else:
            time = time.replace(str(time[:2]), str(int(time[:2]) + 12))
            return time[0:5]

# funcion para validar que la fecha de encendido del horno sea menor
# que la fecha de apagado del horno


def validar_fecha(fecha_apagado, fecha_encendido):
    # se compara la fecha de entrada quema con la fecha de salida
    # quema
    if str(fecha_apagado) > str(fecha_encendido):
        return True
    else:
        return False

# funcion para validar que la suma de ingreso de los productos sea igual a la
# de la entrada en el horno


def validar_salida_de_productos_horno(ids_can_prod, can_prod):
    ban = True
    for i in ids_can_prod:
        if ban:
            for j in range(len(can_prod)):
                objSalQuem = Salida_quema_producto.objects.get(id=i)
                can_dañ = (objSalQuem.cantidad_verde -
                           (can_prod[j] + can_prod[j + 1] + can_prod[j + 2]))
                if(can_dañ < 0):
                    ban = False
                    break
                else:
                    break
            can_prod.pop(0)
            can_prod.pop(0)
            can_prod.pop(0)
        else:
            break
    return ban


def validar_cantidad_combustible(self, ids_com, can_com):
    ban = True
    for reg in ids_com:
        if ban:
            for can in can_com:
                combus = Combustible.objects.get(id=reg)
                if can < combus.cantidad_total_combustible:
                    break
                else:
                    ban = False
                    break
            can_com.pop(0)
        else:
            break
    return ban
