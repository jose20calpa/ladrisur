from django import forms
from django.forms import ModelForm

from apps.produccion.models import *
from apps.administrador.models import Producto, Empleado, Combustible, Horno

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, HTML, ButtonHolder
from crispy_forms.bootstrap import FormActions, StrictButton, PrependedText, InlineRadios


# FORMULARIOS PRODUCCION VERDE
class FormularioProduccion_verde(ModelForm):

    class Meta:
        model = Produccion_verde
        fields = ['fecha_produccion_verde']
        widgets = {'fecha_produccion_verde': forms.TextInput(
            attrs={'class': 'form-control', 'type': 'hidden', 'disabled': 'yes'})}


class FormularioIngreso_produccion_verde(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    helper.layout = Layout(

        Div(
            Div(Field('id_producto', css_class='form-control'),
                css_class='col-lg-12'),
            Div(Field('cantidad_producto', css_class='form-control'),
                css_class='col-lg-12'),

        ),
        Div(
            HTML('<hr>'),
            css_class='col-md-12'
        ),


    )

    class Meta:
        model = Ingreso_produccion_verde
        fields = ['id_producto', 'cantidad_producto']
        widgets = {'id_producto': forms.Select(attrs={'class': 'form-control', 'data-query': 'Producto'}),
                   'cantidad_producto': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
                   }
        labels = {'id_producto': 'Seleccione un Producto', 'cantidad_producto': 'Cantidad Verde'
                  }


class FormularioModificarIngreso_produccion_verde(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(

        Div(
            Div(Field('id_producto', css_class='form-control'),
                css_class='col-lg-12'),
            Div(Field('cantidad_producto', css_class='form-control'),
                css_class='col-lg-12'),

        ),
        Div(
            HTML('<hr>'),
            css_class='col-md-12'
        ),

        Div(
            Div(
                FormActions(Submit('modificar', 'modificar',
                                   css_class='btn-success')),
                css_class='col-lg-3'),
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "produccion:lis-preprod" %}>Cancelar</a>'),
                             )),
        ),


    )

    class Meta:
        model = Ingreso_produccion_verde
        fields = ['id_producto', 'cantidad_producto']
        widgets = {'id_producto': forms.Select(attrs={'class': 'form-control', 'data-query': 'Producto'}),
                   'cantidad_producto': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
                   }
        labels = {'id_producto': 'Seleccione un Producto', 'cantidad_producto': 'Cantidad Verde'
                  }

# FORMULARIOS QUEMAS


class FormularioQuema(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    class Meta:
        model = Quema
        fields = ['id_horno']
        widgets = {'id_horno': forms.Select(
            attrs={'class': 'form-control', 'data-query': 'Horno'})}
        labels = {'id_horno': 'Seleccione un Horno'}


class FormularioEntrada_quema(ModelForm):

    class Meta:
        model = Entrada_quema
        fields = ['fecha_encendido', 'hora_encendido']
        widgets = {'fecha_encendido': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
                   'hora_encendido': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', })
                   }


class FormularioEntrada_quema_producto(ModelForm):

    class Meta:
        model = Entrada_quema_producto
        fields = ['id_producto', 'cantidad_verde']
        widgets = {'id_producto': forms.Select(attrs={'class': 'form-control', 'data-query': 'Producto'}),
                   'cantidad_verde': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'})}
        labels = {'id_producto': 'Seleccione un Producto'}


class FormularioSalida_quema(ModelForm):

    class Meta:
        model = Salida_quema
        fields = ['fecha_apagado', 'hora_apagado']
        widgets = {'fecha_apagado': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'readonly': 'true', 'style': 'background-color: white;'}),
                   'hora_apagado': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'})
                   }


class FormularioSalida_quema_producto(ModelForm):

    class Meta:
        model = Salida_quema_producto
        fields = ['id_producto', 'cantidad_primera',
                  'cantidad_segunda', 'cantidad_crudo', 'cantidad_dañados']
        widgets = {'id_producto': forms.Select(attrs={'class': 'form-control', 'data-query': 'Producto'}),
                   'cantidad_primera': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
                   'cantidad_segunda': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
                   'cantidad_crudo': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
                   'cantidad_dañados': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'})}
        labels = {'id_producto': 'Seleccione un Producto'}


class FormularioQuema_combustible(ModelForm):

    class Meta:
        model = Quema_combustible
        fields = ['id_combustible', 'cantidad_combustible']
        widgets = {'id_combustible': forms.Select(attrs={'class': 'form-control', 'data-query': 'Combustible'}),
                   'cantidad_combustible': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'})}
        labels = {'id_combustible': 'Seleccione un combustible'}

 # FORMULARIO HORNERO SALIDA QUEMA


class FormularioHorneroSalida(ModelForm):

    class Meta:
        model = Salida_quema
        fields = ['id_empleado']


####################### FORMULARIOS CONSUMO ##############################

 # FORMULARIOS TANQUEO


class FormularioTanqueo(forms.ModelForm):

    class Meta:
        model = Tanqueo
        fields = ['id_combustible', 'id_maquina',
                  'cantidad_tanqueo', 'fecha_tanqueo']
        widgets = {'id_combustible': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'si', 'type': 'text', 'placeholder': 'ACPM'}),
                   'id_maquina': forms.Select(attrs={'class': 'form-control', 'data-query': 'Maquina'}),
                   'cantidad_tanqueo': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
                   'fecha_tanqueo': forms.TextInput(attrs={'class': 'form-control', 'data-date-format': 'mm/dd/yyyy'})}
        labels = {'id_combustible': 'Combustible',
                  'id_maquina': 'Seleccione una maquina'}

# FORMULARIOS CONSUMO SECADERO


class FormularioSecado(ModelForm):

    class Meta:
        model = Secado
        fields = ['fecha_secado', 'id_secadero']
        widgets = {'fecha_secado': forms.TextInput(attrs={'class': 'form-control'}),
                   'id_secadero': forms.Select(attrs={'class': 'form-control', 'data-query': 'Secadero'})}
        labels = {'id_secadero': 'Seleccione un Secadero', }


class FormularioSecado_combustible(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    helper.layout = Layout(

        Div(
            Div(Field('id_combustible', css_class='form-control'),
                css_class='col-lg-12'),
            Div(Field('cantidad_combustible', css_class='form-control'),
                css_class='col-lg-12'),

        ),
        Div(
            HTML('<hr>'),
            css_class='col-md-12'
        ),


    )

    class Meta:
        model = Secado_combustible
        fields = ['id_combustible', 'cantidad_combustible']
        widgets = {'id_combustible': forms.Select(attrs={'class': 'form-control', 'data-query': 'Combustible'}),
                   'cantidad_combustible': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
                   }
        labels = {'id_combustible': 'Seleccione un combustible', 'cantidad_combustible': 'Cantidad consumida'
                  }
