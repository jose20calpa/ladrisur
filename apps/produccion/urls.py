from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from .views import *
from .forms import *

urlpatterns = [
    # PREPRODUCCION
    url(r'^ListaProduccion_verde/$',
        login_required(ListaProduccion_verde.as_view()), name='lis-preprod'),
    url(r'^CrearIngreso_produccion_verde/$',
        login_required(CrearIngreso_produccion_verde.as_view()), name='cre-preprod'),
    url(r'^ModificarProductoVerde/(?P<pk>[0-9]+)$', login_required(
        ModificarProductoVerde.as_view()), name='mod-prodver'),
    url(r'^EliminarProductoVerde/(?P<pk>[0-9]+)$', login_required(
        EliminarIngreso_produccion_verde.as_view()), name='elm-prodver'),


    # PRODUCCION
    # Iniciar Quema WIZARD
    url(r'^CrearInicioQuema/$',
        login_required(CrearInicioQuemaWZ.as_view()), name='cre-quem-wz'),
    # Detalle Quemas Iniciadas
    url(r'^DetalleInicioQuema/(?P<pk>[0-9]+)$',
        login_required(DetalleInicioQuema.as_view()), name='det-ini-quem'),
    # Eliminar Quemas Iniciadas
    url(r'^EliminarInicioQuema/(?P<pk>[0-9]+)$',
        login_required(EliminarInicioQuema.as_view()), name='elm-ini-quem'),
    # modificar datos de quema Iniciadas
    url(r'^ModificarInicioQuema/(?P<pk>[0-9]+)$',
    login_required(ModificarInicioQuema.as_view()), name='mod-ini-quem'),
    # Modificar Productos de Quemas Iniciadas
    url(r'^ModificarProductoEntradaQuema/(?P<pk>[0-9]+)$',
        login_required(ModificarProductoEntradaQuema.as_view()), name='mod-pro-quem'),
    # Eliminar Productos de Quemas Iniciadas
    url(r'^EliminarProductoEntradaQuema/(?P<pk>[0-9]+)$',
        login_required(EliminarProductoEntradaQuema.as_view()), name='elm-pro-quem'),
    # Finalizar Quema
    url(r'^ListarQuemasIniciadas/$',
        login_required(ListarQuemasIniciadas.as_view()), name='lis-quem'),
    url(r'^CrearFinQuema/(?P<pk>[0-9]+)$',
        login_required(CrearFinQuemaWZ.as_view()), name='cre-fin-quem-wz'),
    # Listar Quemas Finalizadas
    url(r'^ListarQuemasFinalizadas/$',
        login_required(ListarQuemasFinalizadas.as_view()), name='lis-quem-fin'),
    # Detalle Quemas Finalizadas
    url(r'^DetalleQuema/(?P<pk>[0-9]+)$',
        login_required(DetalleQuema.as_view()), name='det-fin-quem'),




    # Iniciar Quema WIZARD
    # url(r'^CrearEntrada_quemaWizard/$',
    # login_required(CrearQuemaWizard.as_view([FormularioQuema,
    # FormularioEntrada_quema, FormularioEntrada_quema_producto])),
    # name='cre-quem-wz'),



    # CONSUMOS
    # TANQUEOS MAQUINARA
    url(r'^ListarTanqueosMaquinaria/$',
        login_required(ListaTanqueos.as_view()), name='lis-tan'),
    url(r'^CrearTanqueoMaquinaria/$',
        login_required(CrearTanqueo.as_view()), name='cre-tan'),
    url(r'^ModificarTanqueoMaquinaria/(?P<pk>[0-9]+)$',
        login_required(ModificarTanqueo.as_view()), name='mod-tan'),
    url(r'^EliminarTanqueoMaquinaria/(?P<pk>[0-9]+)$',
        login_required(EliminarTanqueo.as_view()), name='elm-tan'),
    # CONSUMOS SECADEROS
    url(r'^ListarSecados/$',
        login_required(ListaSecados.as_view()), name='lis-sec'),
    url(r'^CrearConsumoSecadero/$',
        login_required(CrearSecado.as_view()), name='cre-con-sec'),
    url(r'^ModificarSecado/(?P<pk>[0-9]+)$',
    login_required(ModificarSecado.as_view()), name='mod-sec'),
    url(r'^ModificarSeacadoCombustible/(?P<pk>[0-9]+)$',
        login_required(ModificarSeacadoCombustible.as_view()), name='mod-sec-com'),
    url(r'^EliminarSecado/(?P<pk>[0-9]+)$',
        login_required(EliminarSecado.as_view()), name='elm-sec'),

    url(r'^EliminarSecadoCombustible/(?P<pk>[0-9]+)$',
        login_required(EliminarSecadoCombustible.as_view()), name='elm-sec-com'),

    url(r'^DetalleSecado/(?P<pk>[0-9]+)$',
        login_required(DetalleSecado.as_view()), name='det-fin-sec'),


]
