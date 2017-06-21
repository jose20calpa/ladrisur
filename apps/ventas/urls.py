from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    # CLIENTES
    url(r'^ListarCliente/$',
        login_required(ListarClientes.as_view()), name='lis-cli'),
    url(r'^CrearCliente/$', login_required(CrearCliente.as_view()), name='cre-cli'),
    url(r'^Buscar_cliente/$', find_cliente, name='bus-cli'),
    # url(r'^ModificarCliente/(?P<pk>[0-9]+)/$',
    #     login_required(ModificarCliente.as_view()), name='mod-cli'),
    # url(r'^EliminarCliente/(?P<pk>[0-9]+)/$',
    #     login_required(EliminarCliente.as_view()), name='elm-cli'),
    # VENTAS
    # VENDER
    url(r'^VenderObra/$',
        login_required(CrearVentaObra.as_view()), name='cre-ven-obr'),
    url(r'^VenderPlanta/$',
        login_required(CrearVentaPlanta.as_view()), name='cre-ven-pla'),

]
