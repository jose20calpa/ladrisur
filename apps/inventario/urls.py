from django.conf.urls import url, include
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # INVENTARIOS PRODUCTOS
    url(r'^InventarioProductos/$',
        login_required(InventarioProductos.as_view()), name='inv-prod'),
    # INVENTARIOS COMBUSTIBLES
    url(r'^InventarioCombustibles/$',
        login_required(InventarioCombustibles.as_view()), name='inv-com'),

]
