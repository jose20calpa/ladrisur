from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView

# Create your views here.


class InventarioProductos(TemplateView):
    template_name = 'inventario\Productos\inventarioProductos.html'


class InventarioCombustibles(TemplateView):
    template_name = 'inventario\Combustibles\inventarioCombustibles.html'
