from django.conf.urls import url, include
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # PRODUCTOS
    url(r'^ListarProductos/$',
        login_required(ListarProdcutos.as_view()), name='lis-prod'),
    url(r'^CrearProducto/$', login_required(CrearProdcuto.as_view()), name='cre-prod'),
    url(r'^ModificarProducto/(?P<pk>[0-9]+)/$',
        login_required(ModificarProducto.as_view()), name='mod-prod'),
    url(r'^EliminarProducto/(?P<pk>[0-9]+)/$',
        login_required(EliminarProducto.as_view()), name='elm-prod'),
    # PROVEEDORES
    url(r'^ListarProveedores/$',
        login_required(ListarProveedores.as_view()), name='lis-prov'),
    url(r'^CrearProveedor/$', login_required(CrearProveedor.as_view()), name='cre-prov'),
    url(r'^ModificarProveedor/(?P<pk>[0-9]+)/$', login_required(
        ModificarProveedor.as_view()), name='mod-prov'),
    url(r'^EliminarProveedor/(?P<pk>[0-9]+)/$',
        login_required(EliminarProveedor.as_view()), name='elm-prov'),
    # CARGOS
    url(r'^ListarCargos/$', login_required(ListarCargos.as_view()), name='lis-car'),
    url(r'^CrearCargo/$', login_required(CrearCargo.as_view()), name='cre-car'),
    url(r'^ModificarCargo/(?P<pk>[0-9]+)/$',
        login_required(ModificarCargo.as_view()), name='mod-car'),
    url(r'^EliminarCargo/(?P<pk>[0-9]+)/$',
        login_required(EliminarCargo.as_view()), name='elm-car'),
    # EMPLEADOS
    url(r'^ListarEmpleados/$',
        login_required(ListarEmpleados.as_view()), name='lis-emp'),
    url(r'^CrearEmpleado/$', login_required(CrearEmpleado.as_view()), name='cre-emp'),
    url(r'^ModificarEmpleado/(?P<pk>[0-9]+)/$',
        login_required(ModificarEmpleado.as_view()), name='mod-emp'),
    url(r'^EliminarEmpleado/(?P<pk>[0-9]+)/$',
        login_required(EliminarEmpleado.as_view()), name='elm-emp'),
    # USUARIOS
    url(r'^ListarUsuarios/$', login_required(ListarUsuarios.as_view()), name='lis-usu'),
    url(r'^CrearUsuario/$', login_required(CrearUsuario.as_view()), name='cre-usu'),
    url(r'^ModificarUsuario/(?P<pk>[0-9]+)/$',
        login_required(ModificarUsuario.as_view()), name='mod-usu'),
    url(r'^EliminarUsuario/(?P<pk>[0-9]+)/$',
        login_required(EliminarUsuario.as_view()), name='elm-usu'),
    url(r'^Buscar_empleado/$', Buscar_empleado, name='bus-emp'),
    # COMBUSTIBLES
    url(r'^ListarCombustibles/$',
        login_required(ListarCombustibles.as_view()), name='lis-com'),
    url(r'^CrearCombustible/$',
        login_required(CrearCombustible.as_view()), name='cre-com'),
    url(r'^ModificarCombustible/(?P<pk>[0-9]+)/$', login_required(
        ModificarCombustible.as_view()), name='mod-com'),
    url(r'^EliminarCombustible/(?P<pk>[0-9]+)/$', login_required(
        EliminarCombustible.as_view()), name='elm-com'),
    # Hornos y Secadores
    url(r'^ListarHornos/$', login_required(ListarHornos.as_view()), name='lis-hor'),
    url(r'^CrearHorno/$', login_required(CrearHorno.as_view()), name='cre-hor'),
    url(r'^ModificarHorno/(?P<pk>[0-9]+)/$',
        login_required(ModificarHorno.as_view()), name='mod-hor'),
    url(r'^EliminarHorno/(?P<pk>[0-9]+)/$',
        login_required(EliminarHorno.as_view()), name='elm-hor'),
    # Secaderos
    url(r'^ListarSecadores/$',
        login_required(ListarSecadores.as_view()), name='lis-sec'),
    url(r'^CrearSecadero/$', login_required(CrearSecadero.as_view()), name='cre-sec'),
    url(r'^ModificarSecadero/(?P<pk>[0-9]+)/$',
        login_required(ModificarSecadero.as_view()), name='mod-sec'),
    url(r'^EliminarSecadero/(?P<pk>[0-9]+)/$',
        login_required(EliminarSecadero.as_view()), name='elm-sec'),
    # MAQUINAS
    url(r'^ListarMaquina/$', login_required(ListarMaquina.as_view()), name='lis-maq'),
    url(r'^CrearMaquina/$', login_required(CrearMaquina.as_view()), name='cre-maq'),
    url(r'^ModificarMaquina/(?P<pk>[0-9]+)/$',
        login_required(ModificarMaquina.as_view()), name='mod-maq'),
    url(r'^EliminarMaquina/(?P<pk>[0-9]+)/$',
        login_required(EliminarMaquina.as_view()), name='elm-maq'),
    # VEHICULOS
    url(r'^ListarVehiculo/$', login_required(ListarVehiculo.as_view()), name='lis-veh'),
    url(r'^CrearVehiculo/$', login_required(CrearVehiculo.as_view()), name='cre-veh'),
    url(r'^ModificarVehiculo/(?P<pk>[0-9]+)/$',
        login_required(ModificarVehiculo.as_view()), name='mod-veh'),
    url(r'^EliminarVehciulo/(?P<pk>[0-9]+)/$',
        login_required(EliminarVehciulo.as_view()), name='elm-veh'),

]
