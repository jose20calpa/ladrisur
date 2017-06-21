from django import forms
from django.forms import ModelForm

from apps.ventas.models import Cliente, Venta

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, HTML, ButtonHolder
from crispy_forms.bootstrap import FormActions, StrictButton, PrependedText, InlineRadios

# FORMULARIOS cliente


class FormularioCliente(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-group'

    helper.layout = Layout(
        Div(
            Div(Field('identificacion_cliente', css_class='form-control'),
                css_class='col-lg-6'), css_class='col-lg-12'
        ),

        Div(

            Div(Field('nombre_cliente', css_class='form-control'),
                css_class='col-lg-6'),
            Div(Field('apellido_cliente', css_class='form-control'),
                css_class='col-lg-6'),
            Div(Field('direccion_cliente', css_class='form-control'),
                css_class='col-lg-6'),
            Div(PrependedText('telefono_cliente',
                              '<span class="glyphicon glyphicon-earphone" aria-hidden="true"> </span>'),
                css_class='col-lg-6'),
            Div(PrependedText('correo_cliente', '@',
                              css_class='form-control'), css_class='col-lg-12'),

            css_class='col-lg-12'
        ),
        Div(
            HTML('<hr>'),
            css_class='col-md-12'
        ),
        Div(
            Div(
                FormActions(Submit('guardar', 'Guardar',
                                   css_class='btn-success')),
                css_class='col-lg-3'),
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "ventas:lis-cli" %}>Cancelar</a>'),
                             )),
            css_class='col-sm-offset-3 col-md-12'
        ),
    )

    class Meta:
        model = Cliente

        fields = ['identificacion_cliente', 'nombre_cliente', 'apellido_cliente',
                  'telefono_cliente', 'direccion_cliente', 'correo_cliente']
        labels = {
            'identificacion_cliente': 'Identificación',
            'nombre_cliente': 'Nombre',
            'apellido_cliente': 'Apellido',
            'telefono_cliente': 'Teléfono',
            'direccion_cliente': 'Direccion',
            'correo_cliente': 'Correo',
        }


class FormularioVentaObra(ModelForm):

    class Meta:
        model = Venta
        fields = ['id_cliente', 'domicilio_obra']
        widgets = {'id_cliente': forms.TextInput(attrs={'class': 'form-control'}),
                   'domicilio_obra': forms.TextInput(attrs={'class': 'form-control'}), }


class FormularioVentaPlanta(ModelForm):

    class Meta:
        model = Venta
        fields = ['id_cliente']
        widgets = {'id_cliente': forms.TextInput(
            attrs={'class': 'form-control'})}
        labels = {'id_cliente': 'Buscar Cliente'}
