from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required


from prototipo4.views import Login

from prototipo4.views import VisaulizarIndex

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', VisaulizarIndex.as_view(), name='index'),

    url(r'^ladrisur/administrador/',
        include('apps.administrador.urls', namespace='administrador')),
    url(r'^ladrisur/produccion/',
        include('apps.produccion.urls', namespace='produccion')),
    url(r'^ladrisur/ventas/',
        include('apps.ventas.urls', namespace='ventas')),
    url(r'^ladrisur/inventario/',
        include('apps.inventario.urls', namespace='inventario')),
    url(r'^ladrisur/login/$', login,
        {'template_name': 'includes/login.html'}, name='entrar'),
    url(r'^ladrisur/logout/$', logout, name='salir'),

]
