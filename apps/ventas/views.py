from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.core.urlresolvers import reverse_lazy
import json
from django.db.models import Q


import datetime
from datetime import date
from apps.ventas.models import *
from apps.administrador.models import *
from apps.produccion.forms import *
from apps.ventas.forms import *


# Create your views here.
class ListarClientes(ListView):
    context_object_name = 'lista'
    model = Cliente
    template_name = 'ventas/Clientes/lista_Clientes.html'


class CrearCliente(CreateView):
    model = Cliente
    form_class = FormularioCliente
    success_url = reverse_lazy('ventas:lis-cli')
    template_name = 'ventas/Clientes/CrearCliente.html'


class CrearVentaObra(TemplateView):
    template_name = 'ventas/Vender/venta_obra.html'


class CrearVentaPlanta(TemplateView):
    template_name = 'ventas/Vender/venta_planta.html'
    form_class = FormularioVentaPlanta
    con_pro_prim = Producto.objects.raw(
        '''select id, nombre_producto,precio_fabrica_primera from administrador_producto''')
    con_pro_seg = Producto.objects.raw(
        '''select id, nombre_producto,precio_fabrica_segunda from administrador_producto''')

    def get_context_data(self, **kwargs):
        context = super(CrearVentaPlanta,
                        self).get_context_data(**kwargs)
        if 'lista_pro_prim' not in context:
            context['lista_pro_prim'] = self.con_pro_prim
        if 'lista_pro_seg' not in context:
            context['lista_pro_seg'] = self.con_pro_seg
        if 'form' not in context:
            context['form'] = self.form_class(
                self.request.GET or None)
        return context


def find_cliente(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        clientes = Cliente.objects.filter(Q(
            identificacion_cliente__icontains=q[:5]) | Q(nombre_cliente__icontains=q[:5]))
        results = []
        for cliente in clientes:
            cliente_json = {}
            cliente_json['id'] = cliente.id
            cliente_json['label'] = cliente.nombre_cliente + " CC: " + \
                cliente.identificacion_cliente
            cliente_json['value'] = cliente.nombre_cliente + \
                " - cc: " + cliente.identificacion_cliente
            results.append(cliente_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
