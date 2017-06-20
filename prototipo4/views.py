from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION
from django.contrib.contenttypes.models import ContentType

#vistas
#vistas9
=======

class VisaulizarIndex(LoginRequiredMixin, TemplateView):
    login_url = '/ladrisur/login/'
    template_name = 'includes/base.html'


class Login(TemplateView):
    template_name = 'includes/login.html'


def registrarLog(user_id, tipo_objeto, id_objeto, nombre_objeto, accion, mensaje):

    LogEntry.objects.log_action(
        user_id=user_id,
        content_type_id=tipo_objeto,
        object_id=id_objeto,
        object_repr=nombre_objeto,
        action_flag=accion,
        change_message=mensaje
    )
