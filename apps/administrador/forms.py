from django import forms
from django.forms import ModelForm, PasswordInput
from django.core.validators import RegexValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, HTML, ButtonHolder
from crispy_forms.bootstrap import FormActions, StrictButton, PrependedText, InlineRadios


from apps.administrador.models import Producto, Cargo, Proveedor, Usuario, \
    Empleado, Combustible, Horno, Maquina, Vehiculo, Secadero


class FormularioProducto(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    helper.layout = Layout(

        Div(
            Div(Field('nombre_producto', css_class='form-control'),
                css_class='col-lg-12'),
        ),

        Div(
            Div(Field('rendimiento_producto', css_class='form-control'),
                css_class='col-lg-4'),

            Div(Field('ancho_producto', css_class='input-sm'), css_class='col-lg-4'),
            Div(Field('alto_producto', css_class='input-sm'), css_class='col-lg-4'),
            Div(Field('largo_producto', css_class='input-sm'), css_class='col-lg-4'),
            Div(Field('peso_producto', css_class='input-sm'), css_class='col-lg-4'),
            css_class='col-lg-12 panel panel-default',
        ),  # EEEEEE
        Div(
            Div(PrependedText('precio_fabrica_primera', '$',
                              css_class='input-sm'), css_class='col-lg-6'),
            Div(PrependedText('precio_obra_primera', '$',
                              css_class='input-sm'), css_class='col-lg-6'),
            css_class='col-lg-6 panel panel-default',


        ),
        Div(
            Div(PrependedText('precio_fabrica_segunda', '$',
                              css_class='input-sm'), css_class='col-lg-6'),
            Div(PrependedText('precio_obra_segunda', '$',
                              css_class='input-sm'), css_class='col-lg-6'),
            css_class='col-lg-6 panel panel-default',


        ),

        Div(
            HTML('<hr>'),
            css_class='col-md-12'
        ),
        Div(
            Div(
                FormActions(Submit('guardar', 'Guardar',
                                   css_class='btn-success')),
                css_class='col-lg-4'),
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "administrador:lis-prod" %}>Cancelar</a>'),
                             )),
            css_class='col-sm-offset-3 col-md-12'
        ),
    )

    def clean_nombre_producto(self):
        nombre = self.cleaned_data['nombre_producto']
        if len(nombre) > 40:
            raise forms.ValidationError(
                "El nombre n    o debe superar los 40 caracteres")
        return nombre

    class Meta:
        model = Producto

        fields = ['nombre_producto', 'rendimiento_producto', 'ancho_producto',
                  'alto_producto', 'largo_producto', 'peso_producto', 'precio_fabrica_primera',
                  'precio_obra_primera', 'precio_fabrica_segunda', 'precio_obra_segunda']

        labels = {
            'rendimiento_producto': 'Rendimiento',
            'ancho_producto': 'Ancho (cm)',
            'alto_producto': 'Alto (cm)',
            'largo_producto': 'Largo (cm)',
            'peso_producto': 'Peso (kg)',
            'precio_fabrica_primera': '$ Fabrica 1ra',
            'precio_obra_primera': '$ Obra 1ra',
            'precio_fabrica_segunda': '$ Fabrica 2da',
            'precio_obra_segunda': '$ Obra 2da',
        }


class FormularioCargo(ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-group'

    helper.layout = Layout(
        Div(
            Div(PrependedText('nombre_cargo', '<i class="fa fa-id-card" aria-hidden="true"></i>',
                              css_class='input-sm'), css_class='col-lg-12'),
        ),
        Div(
            Div(Field('codigo_cargo_DANE', css_class='input-sm'),
                css_class='col-lg-6'),
            Div(PrependedText('horas_semana',
                              '<i class="fa fa-hourglass-half" aria-hidden="true"> </i>',
                              css_class='input-sm'), css_class='col-lg-6'),
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
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "administrador:lis-car" %}>Cancelar</a>'),
                             )),
        ),
    )

    class Meta:
        model = Cargo
        fields = ['codigo_cargo_DANE', 'nombre_cargo',
                  'horas_semana']
        labels = {
            'codigo_cargo_DANE': 'Codigo DANE',
            'nombre_cargo': 'Cargo',
            'horas_semana': 'No. Hrs por Semana',
        }


class FormularioProveedor(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-group'

    helper.layout = Layout(
        Div(
            Div(Field('identificacion_proveedor', css_class='form-control'),
                css_class='col-lg-4'),
            Div(PrependedText('nombre_proveedor', '<span class="glyphicon glyphicon-user" aria-hidden="true"> </span>', css_class='form-control'),
                css_class='col-lg-8'),
            Div(Field('direccion_proveedor', css_class='form-control'),
                css_class='col-lg-6'),
            Div(PrependedText('telefono_proveedor',
                              '<span class="glyphicon glyphicon-earphone" aria-hidden="true"> </span>'),
                css_class='col-lg-6'),
            Div(PrependedText('correo_proveedor', '@',
                              css_class='form-control'), css_class='col-lg-12'),
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
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "administrador:lis-prov" %}>Cancelar</a>'),
                             )),
            css_class='col-sm-offset-3 col-md-12'),

    )

    # def clean_identificacion_proveedor(self):
    #     id_prov = self.cleaned_data['identificacion_proveedor']
    #     if id_prov.find("-"):
    #         res = id_prov[len(id_prov) - 1:]
    #         id_prov_aux = id_prov[:-2]
    #         print(id_prov_aux)
    #         raise forms.ValidationError(
    #             'es Cedula')
    #     return id_prov

    class Meta:
        model = Proveedor
        fields = ['nombre_proveedor', 'identificacion_proveedor',
                  'direccion_proveedor', 'telefono_proveedor', 'correo_proveedor']

        widgets = {'identificacion_proveedor': forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text',  'pattern': '.[0-9-]{8,15}', }), }
        labels = {
            'nombre_proveedor': 'Proveedor',
            'identificacion_proveedor': 'CC. ó Nit',
            'direccion_proveedor': 'Dirección',
            'telefono_proveedor': 'Teléfono',
            'correo_proveedor': 'Correo',
        }


class FormularioUsuario(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-group'

    helper.layout = Layout(
        Div(
            Div(Field('id_empleado', css_class='form-control'),
                css_class='col-lg-6 ui-widget'),

            Div(Field('username', css_class='form-control'),
                css_class='col-lg-6'),
            Div(
                Div(PrependedText(
                    'password',
                    '<i class="fa fa-key"></i>',
                    placeholder='Contraseña'),
                    css_class='col-lg-6'
                    ),

                Div(
                    PrependedText(
                        'password',
                        '<i class="fa fa-key"></i>',
                        placeholder='Contraseña'),
                    css_class='col-lg-6'
                ),
                css_class='col-lg-12'),

            Div(Field('groups', css_class='form-control'),
                css_class='col-lg-6'),


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
                css_class='col-xs-3'),
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "administrador:lis-usu" %}>Cancelar</a><br>'),
                             ), css_class='col-xs-offset-3 col-md-offset-1 col-xs-3'),
            css_class='col-md-offset-3 col-xs-12'
        ),
    )

    # el form usuario usa username password y groups heredados del modelos
    # auth_user
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'groups', 'id_empleado']
        help_texts = {
            'username': None,
            'groups': None,
        }
        widgets = {'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
                   'id_empleado': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
                   }
        labels = {
            'groups': 'Rol',
            'id_empleado': 'C.C Empleado',
        }


class FormularioEmpleado(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-group'

    helper.layout = Layout(
        Div(
            Div(Field('cedula_empleado', css_class='form-control'),
                css_class='col-lg-6'), css_class='col-lg-12'
        ),

        Div(

            Div(Field('nombre_empleado', css_class='form-control'),
                css_class='col-lg-6'),
            Div(Field('apellido_empleado', css_class='form-control'),
                css_class='col-lg-6'),
            Div(Field('id_cargo', css_class='form-control'),
                css_class='col-lg-12'),
            Div(Field('direccion_empleado', css_class='form-control'),
                css_class='col-lg-6'),
            Div(PrependedText('telefono_empleado',
                              '<span class="glyphicon glyphicon-earphone" aria-hidden="true"> </span>'),
                css_class='col-lg-6'),
            Div(PrependedText('correo_empleado', '@',
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
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "administrador:lis-emp" %}>Cancelar</a>'),
                             )),
            css_class='col-sm-offset-3 col-md-12'
        ),
    )

    class Meta:
        model = Empleado

        fields = ['cedula_empleado', 'nombre_empleado', 'apellido_empleado',
                  'telefono_empleado', 'direccion_empleado', 'correo_empleado', 'id_cargo']
        labels = {
            'cedula_empleado': 'Identificación',
            'nombre_empleado': 'Nombre',
            'apellido_empleado': 'Apellido',
            'telefono_empleado': 'Teléfono',
            'direccion_empleado': 'Direccion',
            'correo_empleado': 'Correo',
            'id_cargo': 'Cargo',
        }


class FormularioCombustible(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-group'

    helper.layout = Layout(
        Div(

            Div(Field('nombre_combustible', css_class='form-control'),
                css_class='col-lg-12'),
            css_class='col-lg-12'
        ),
        Div(

            Div(Field('unidad_combustible', css_class='form-control'),
                css_class='col-lg-6'),
            Div(Field('uso', css_class='form-control'),
                css_class='col-lg-6'),

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
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "administrador:lis-com" %}>Cancelar</a>'),
                             )),
            css_class='col-sm-offset-3 col-md-12'
        ),
    )

    class Meta:
        model = Combustible
        fields = ['nombre_combustible', 'unidad_combustible', 'uso']
        labels = {
            'nombre_combustible': 'Combustible',
            'unidad_combustible': 'Unidad',
            'uso': 'Uso',
        }


class FormularioHorno(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    helper.layout = Layout(
        Div(
            Div(Field('nombre_horno', css_class='form-control'),
                css_class='col-lg-6'),
            Div(Field('numero_bocas', css_class='form-control'),
                css_class='col-lg-6'),
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
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "administrador:lis-hor" %}>Cancelar</a>'),
                             )),
            css_class='col-sm-offset-3 col-md-12'
        ),
    )

    class Meta:
        model = Horno
        fields = ['nombre_horno', 'numero_bocas']
        widgets = {'nombre_horno': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
                   'numero_bocas': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'})}
        labels = {
            'numero_bocas': 'Numero de Bocas',
        }


class FormularioSecadero(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    helper.layout = Layout(
        Div(
            Div(Field('nombre_secadero', css_class='form-control'),
                css_class='col-lg-6 col-sm-offset-3'),
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
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "administrador:lis-sec" %}>Cancelar</a>'),
                             )),
            css_class='col-sm-offset-3 col-md-12'
        ),
    )

    class Meta:
        model = Secadero
        fields = ['nombre_secadero']
        widgets = {'nombre_secadero': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
                   }
        labels = {
            'nombre_secadero': 'Nombre Secadero',
        }


class FormularioVehiculo(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    helper.layout = Layout(
        Div(
            Div(Field('tipo_vehiculo', css_class='form-control'),
                css_class='col-lg-6'),
            Div(Field('matricula_vehiculo', css_class='form-control', placeholder='ej. ABC-123', patter='^[A-Za-z]{3}-\d{3}$',  title="Revisa el Formato de Placa ABC-123   "),
                css_class='col-lg-6'),
            Div(Field('marca_vehiculo', css_class='form-control'),
                css_class='col-lg-4'),
            Div(Field('modelo_vehiculo', css_class='form-control'),
                css_class='col-lg-4'),
            Div(Field('año_vehiculo', css_class='form-control'),
                css_class='col-lg-4'),
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
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "administrador:lis-veh" %}>Cancelar</a>'),
                             )),
            css_class='col-sm-offset-3 col-md-12'
        ),
    )

    class Meta:
        model = Vehiculo

        fields = ['tipo_vehiculo', 'matricula_vehiculo',
                  'marca_vehiculo', 'modelo_vehiculo', 'año_vehiculo']
        widgets = {

            'año': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'max': '4'})
        }


class FormularioMaquina(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    helper.layout = Layout(
        Div(
            Div(Field('tipo_maquina', css_class='form-control'),
                css_class='col-lg-5'),
            css_class='col-lg-12'
        ),
        Div(
            Div(Field('marca_maquina', css_class='form-control'),
                css_class='col-lg-4'),
            Div(Field('modelo_maquina', css_class='form-control'),
                css_class='col-lg-4'),
            Div(Field('año_maquina', css_class='form-control'),
                css_class='col-lg-3'),
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
            Div(ButtonHolder(HTML('<a class="btn btn-default" href={% url "administrador:lis-maq" %}>Cancelar</a>'),
                             )),
            css_class='col-sm-offset-3 col-md-12'
        ),
    )

    class Meta:
        model = Maquina

        fields = ['tipo_maquina', 'marca_maquina',
                  'modelo_maquina', 'año_maquina']
        widgets = {

            'año': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'max': '4'})
        }

        labels = {
            'tipo_maquina': 'Tipo',
            'marca_maquina': 'Marca',
            'modelo_maquina': 'Modelo',
            'año_maquina': 'Año',
        }
