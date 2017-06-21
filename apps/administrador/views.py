from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION, DELETION
from prototipo4.views import registrarLog

import json

from apps.administrador.forms import *
from apps.administrador.models import *
from apps.produccion.models import *
from apps.inventario.models import *


# PRODUCTO


class ListarProdcutos(ListView):
    context_object_name = 'lista'
    model = Producto
    template_name = 'administrador/Productos/lista_Productos.html'


class CrearProdcuto(SuccessMessageMixin, CreateView):
    model = Producto
    form_class = FormularioProducto
    success_url = reverse_lazy('administrador:lis-prod')
    template_name = 'administrador\Productos\CrearProducto.html'
    success_message = 'Registro Agregado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.nombre_producto = producto.nombre_producto.upper()
            producto.save()
            # registramos en la tabla de log la accion realizada
            prod = Producto.objects.all().order_by('-id')[:1]
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Producto).pk,
                prod[0].id,
                prod[0].nombre_producto,
                ADDITION,
                "AGREGO")
            return redirect('/ladrisur/administrador/ListarProductos/')

        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModificarProducto(SuccessMessageMixin, UpdateView):
    model = Producto
    form_class = FormularioProducto
    template_name = 'administrador/Productos/ModificarProducto.html'
    success_url = reverse_lazy('administrador:lis-prod')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        obj = Producto.objects.get(id=self.kwargs['pk'])
        prod = get_object_or_404(Producto, pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=prod)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.nombre_producto = producto.nombre_producto.upper()
            producto.save()

            obj = Producto.objects.get(id=self.kwargs['pk'])
            # registramos en la tabla de log la accion realizada
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Producto).pk,
                obj.id,
                obj.nombre_producto,
                CHANGE,
                "CAMBIO")
            return redirect('/ladrisur/administrador/ListarProductos/')

        else:
            return self.render_to_response(self.get_context_data(form=form))


class EliminarProducto(SuccessMessageMixin, DeleteView):
    model = Producto
    template_name = 'administrador/Productos/EliminarProducto.html'
    success_url = reverse_lazy('administrador:lis-prod')
    success_message = 'Registro Eliminado'

    def post(self, request, *args, **kwargs):
        if Ingreso_produccion_verde.objects.filter(id_producto_id=self.kwargs['pk']).exists():
            print("NO BORRA POR RELACION CON Producto_Categoria")
            return render(request, 'administrador/Productos/EliminarProducto.html', {'msj': 'No se puede eliminar este producto porque tiene relacion con uno o mas registros'})
        else:
            obj = Producto.objects.get(id=self.kwargs['pk'])
            # registramos en la tabla de log la accion realizada
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Producto).pk,
                obj.id,
                obj.nombre_producto,
                DELETION,
                "BORRO")
            super().delete(*args, request, **kwargs)
            return redirect('/ladrisur/administrador/ListarProductos/')

# PROVEEDOR


class ListarProveedores(ListView):
    context_object_name = 'lista'
    # paginate_by = 5
    model = Proveedor
    template_name = 'administrador/Proveedores/lista_Proveedores.html'


class CrearProveedor(SuccessMessageMixin, CreateView):
    model = Proveedor
    form_class = FormularioProveedor
    success_url = reverse_lazy('administrador:lis-prov')
    template_name = 'administrador\Proveedores\CrearProvedor.html'
    success_message = 'Registro Agregado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.nombre_proveedor = proveedor.nombre_proveedor.upper()
            proveedor.direccion_proveedor = proveedor.direccion_proveedor.upper()
            proveedor.save()
            prov = Proveedor.objects.all().order_by('-id')[:1]
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Proveedor).pk,
                prov[0].id,
                prov[0].nombre_proveedor,
                ADDITION,
                "AGREGO")
            return redirect('/ladrisur/administrador/ListarProveedores/')

        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModificarProveedor(SuccessMessageMixin, UpdateView):
    model = Proveedor
    form_class = FormularioProveedor
    template_name = 'administrador/Proveedores/ModificarProveedor.html'
    success_url = reverse_lazy('administrador:lis-prov')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        obj = Proveedor.objects.get(id=self.kwargs['pk'])
        prov = get_object_or_404(Proveedor, pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=prov)
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.nombre_proveedor = proveedor.nombre_proveedor.upper()
            proveedor.direccion_proveedor = proveedor.direccion_proveedor.upper()
            proveedor.save()

            prov = Proveedor.objects.get(id=self.kwargs['pk'])
            # registramos en la tabla de log la accion realizada
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Proveedor).pk,
                prov.id,
                prov.nombre_proveedor,
                CHANGE,
                "CAMBIO")
            return redirect('/ladrisur/administrador/ListarProveedores/')

        else:
            return self.render_to_response(self.get_context_data(form=form))


class EliminarProveedor(SuccessMessageMixin, DeleteView):
    model = Proveedor
    template_name = 'administrador/Proveedores/EliminarProveedor.html'
    success_url = reverse_lazy('administrador:lis-prov')
    success_message = 'Registro Eliminado'

    def post(self, request, *args, **kwargs):
        if Pedido_combustible.objects.filter(id_proveedor=self.kwargs['pk']).exists():
            print(
                "No se puede eliminar este proveedor porque tiene relacion con un pedido combustible")
            return render(request, 'administrador/Proveedores/EliminarProveedor.html', {'msj': 'No se puede eliminar este proveedor porque tiene relacion con uno o mas registros'})
        else:
            obj = Proveedor.objects.get(id=self.kwargs['pk'])
            # registramos en la tabla de log la accion realizada
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Proveedor).pk,
                obj.id,
                obj.nombre_proveedor,
                DELETION,
                "BORRO")
            super().delete(*args, request, **kwargs)
            return redirect('/ladrisur/administrador/ListarProveedores/')

# CARGO


class ListarCargos(ListView):
    context_object_name = 'lista'
    # paginate_by = 5
    model = Cargo
    template_name = 'administrador/Cargos/lista_Cargos.html'


class CrearCargo(SuccessMessageMixin, CreateView):
    model = Cargo
    form_class = FormularioCargo
    success_url = reverse_lazy('administrador:lis-car')
    template_name = 'administrador\Cargos\CrearCargo.html'
    success_message = 'Registro Agregado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.nombre_cargo = cargo.nombre_cargo.upper()
            cargo.save()
            car = Cargo.objects.all().order_by('-id')[:1]
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Cargo).pk,
                car[0].id,
                car[0].nombre_cargo,
                ADDITION,
                "AGREGO")
            return redirect('/ladrisur/administrador/ListarCargos/')

        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModificarCargo(SuccessMessageMixin, UpdateView):
    model = Cargo
    form_class = FormularioCargo
    template_name = 'administrador/Cargos/ModificarCargo.html'
    success_url = reverse_lazy('administrador:lis-car')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        car = get_object_or_404(Cargo, pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=car)
        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.nombre_cargo = cargo.nombre_cargo.upper()
            cargo.save()

            obj = Cargo.objects.get(id=self.kwargs['pk'])
            # registramos en la tabla de log la accion realizada
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Cargo).pk,
                obj.id,
                obj.nombre_cargo,
                CHANGE,
                "CAMBIO")
            return redirect('/ladrisur/administrador/ListarCargos/')

        else:
            return self.render_to_response(self.get_context_data(form=form))


class EliminarCargo(SuccessMessageMixin, DeleteView):
    model = Cargo
    template_name = 'administrador/Cargos/EliminarCargo.html'
    success_url = reverse_lazy('administrador:lis-car')
    success_message = 'Registro Eliminado'

    def post(self, request, *args, **kwargs):
        if Empleado.objects.filter(id_cargo=self.kwargs['pk']).exists():
            print("No se puede eliminar este cargo porque tiene relacion con un Empleado")
            return render(request, 'administrador/Cargos/EliminarCargo.html', {'msj': 'No se puede eliminar este Cargo porque tiene relación con uno o mas registros'})
        else:
            obj = Cargo.objects.get(id=self.kwargs['pk'])
            # registramos en la tabla de log la accion realizada
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Cargo).pk,
                obj.id,
                obj.nombre_cargo,
                DELETION,
                "BORRO")
            super().delete(*args, request, **kwargs)
            return redirect('/ladrisur/administrador/ListarCargos/')

# EMPLEADOS


class ListarEmpleados(ListView):
    context_object_name = 'lista'
    # paginate_by = 3
    model = Empleado
    template_name = 'administrador/Empleados/lista_Empleados.html'


class CrearEmpleado(SuccessMessageMixin, CreateView):
    model = Empleado
    form_class = FormularioEmpleado
    success_url = reverse_lazy('administrador:lis-emp')
    template_name = 'administrador\Empleados\CrearEmpleado.html'
    success_message = 'Registro Agregado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.nombre_empleado = empleado.nombre_empleado.upper()
            empleado.apellido_empleado = empleado.apellido_empleado.upper()
            empleado.direccion_empleado = empleado.direccion_empleado.upper()
            empleado.save()

            emp = Empleado.objects.all().order_by('-id')[:1]
            cad = (emp[0].nombre_empleado + " " +
                   emp[0].apellido_empleado + " " + emp[0].cedula_empleado)
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Empleado).pk,
                emp[0].id,
                cad,
                ADDITION,
                "AGREGO")
            return redirect('/ladrisur/administrador/ListarEmpleados/')

        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModificarEmpleado(SuccessMessageMixin, UpdateView):
    model = Empleado
    form_class = FormularioEmpleado
    template_name = 'administrador/Empleados/ModificarEmpleado.html'
    success_url = reverse_lazy('administrador:lis-emp')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        emp = get_object_or_404(Empleado, pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=emp)
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.nombre_empleado = empleado.nombre_empleado.upper()
            empleado.apellido_empleado = empleado.apellido_empleado.upper()
            empleado.direccion_empleado = empleado.direccion_empleado.upper()
            empleado.save()

            emp = Empleado.objects.get(id=self.kwargs['pk'])
            cad = str(emp.nombre_empleado + " " +
                      emp.apellido_empleado + " " + " " + emp.cedula_empleado)
            # registramos en la tabla de log la accion realizada
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Empleado).pk,
                emp.id,
                cad,
                CHANGE,
                "CAMBIO")

            return redirect('/ladrisur/administrador/ListarEmpleados/')

        else:
            return self.render_to_response(self.get_context_data(form=form))


class EliminarEmpleado(SuccessMessageMixin, DeleteView):
    model = Empleado
    template_name = 'administrador/Empleados/EliminarEmpleado.html'
    success_url = reverse_lazy('administrador:lis-emp')
    success_message = 'Registro Eliminado'

    def post(self, request, *args, **kwargs):
        if Venta.objects.filter(id_empleado=self.kwargs['pk']).exists() or Salida_quema.objects.filter(id_empleado=self.kwargs['pk']).exists() or Entrega_obra.objects.filter(id_empleado=self.kwargs['pk']).exists() or Usuario.objects.filter(id_empleado=self.kwargs['pk']).exists():
            print(
                "No se puede eliminar este Empelado porque tiene relacion con uno o mas registros ")
            return render(request, 'administrador/Empleados/EliminarEmpleado.html', {'msj': 'No se puede eliminar este Empleado porque tiene relacion con uno o mas registros'})
        else:
            emp = Empleado.objects.get(id=self.kwargs['pk'])
            cad = str(emp.nombre_empleado + " " +
                      emp.apellido_empleado + " " + " " + emp.cedula_empleado)
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Empleado).pk,
                emp.id,
                cad,
                DELETION,
                "BORRO")
            super().delete(*args, request, **kwargs)
            return redirect('/ladrisur/administrador/ListarEmpleados/')

# USUARIOS


class ListarUsuarios(ListView):
    context_object_name = 'lista'
    # paginate_by = 5
    model = Usuario
    template_name = 'administrador/Usuarios/lista_Usuarios.html'


class CrearUsuario(CreateView, SuccessMessageMixin):
    model = Usuario
    form_class = FormularioUsuario
    success_message = 'Registro Agregado'
    success_url = reverse_lazy('administrador:lis-usu')
    template_name = 'administrador/Usuarios/CrearUsuario.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)

        if form.is_valid():
            usuario = form.save()
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()

            usu = Usuario.objects.all().order_by('-id')[:1]
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Usuario).pk,
                usu[0].id,
                usu[0].id_empleado,
                ADDITION,
                "AGREGO")

            return redirect('administrador:lis-usu')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModificarUsuario(SuccessMessageMixin, UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'administrador/Usuarios/ModificarUsuario.html'
    success_url = reverse_lazy('administrador:lis-usu')
    success_message = 'Registro modificado'


class EliminarUsuario(SuccessMessageMixin, DeleteView):
    model = Usuario
    template_name = 'administrador/Usuarios/EliminarUsuario.html'
    success_url = reverse_lazy('administrador:lis-usu')
    success_message = 'Registro Eliminado'


def Buscar_empleado(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        empleados = Empleado.objects.filter(Q(
            cedula_empleado__icontains=q[:5]) | Q(nombre_empleado__icontains=q[:5]))
        results = []
        for empleado in empleados:
            empleado_json = {}
            empleado_json['id'] = empleado.id
            empleado_json['label'] = empleado.nombre_empleado + " CC: " + \
                empleado.cedula_empleado
            empleado_json['value'] = empleado.id
            results.append(empleado_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

# COMBUSTIBLES


class ListarCombustibles(ListView):
    context_object_name = 'lista'
    # paginate_by = 5
    model = Combustible
    template_name = 'administrador/Combustibles/lista_Combustibles.html'


class CrearCombustible(SuccessMessageMixin, CreateView):
    model = Combustible
    form_class = FormularioCombustible
    success_url = reverse_lazy('administrador:lis-com')
    template_name = 'administrador/Combustibles/CrearCombustible.html'
    success_message = 'Registro Agregado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            combustible = form.save(commit=False)
            combustible.nombre_combustible = combustible.nombre_combustible.upper()
            combustible.save()

            com = Combustible.objects.all().order_by('-id')[:1]
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Combustible).pk,
                com[0].id,
                com[0].nombre_combustible,
                ADDITION,
                "AGREGO")
            return redirect('/ladrisur/administrador/ListarCombustibles/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModificarCombustible(SuccessMessageMixin, UpdateView):
    model = Combustible
    form_class = FormularioCombustible
    template_name = 'administrador/Combustibles/ModificarCombustible.html'
    success_url = reverse_lazy('administrador:lis-com')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        com = get_object_or_404(Combustible, pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=com)
        if form.is_valid():
            combustible = form.save(commit=False)
            combustible.nombre_combustible = combustible.nombre_combustible.upper()
            combustible.save()

            com = Combustible.objects.get(id=self.kwargs['pk'])
            cad = str(com.nombre_combustible + " " + com.uso +
                      " " + " " + com.unidad_combustible)
            # registramos en la tabla de log la accion realizada
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Combustible).pk,
                com.id,
                cad,
                CHANGE,
                "CAMBIO")
            return redirect('/ladrisur/administrador/ListarCombustibles/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EliminarCombustible(SuccessMessageMixin, DeleteView):
    model = Combustible
    template_name = 'administrador/Combustibles/EliminarCombustible.html'
    success_url = reverse_lazy('administrador:lis-com')
    success_message = 'Registro Eliminado'

    def post(self, request, *args, **kwargs):
        if Tanqueo.objects.filter(id_combustible=self.kwargs['pk']).exists() or Pedido_combustible.objects.filter(id_combustible=self.kwargs['pk']).exists() or Secado_combustible.objects.filter(id_combustible=self.kwargs['pk']).exists() or Quema_combustible.objects.filter(id_combustible=self.kwargs['pk']).exists():
            print(
                "No se puede eliminar este Combustible porque tiene relacion con uno o mas registros ")
            return render(request, 'administrador/Combustibles/EliminarCombustible.html', {'msj': 'No se puede eliminar este Combustible porque tiene relacion con uno o mas registros'})
        else:
            com = Combustible.objects.get(id=self.kwargs['pk'])
            cad = str(com.nombre_combustible + " " + com.uso +
                      " " + " " + com.unidad_combustible)
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Combustible).pk,
                com.id,
                cad,
                DELETION,
                "BORRO")
            super().delete(*args, request, **kwargs)
            return redirect('/ladrisur/administrador/ListarCombustibles/')


# HORNOS


class ListarHornos(ListView):
    context_object_name = 'lista'
    # paginate_by = 5
    model = Horno
    template_name = 'administrador/Hornos_Secadores/Hornos/lista_Hornos.html'


class CrearHorno(SuccessMessageMixin, CreateView):
    model = Horno
    form_class = FormularioHorno
    success_url = reverse_lazy('administrador:lis-hor')
    template_name = 'administrador/Hornos_Secadores/Hornos/CrearHorno.html'
    success_message = 'Registro Agregado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            horno = form.save(commit=False)
            horno.nombre_horno = horno.nombre_horno.upper()
            horno.save()

            hor = Horno.objects.all().order_by('-id')[:1]
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Horno).pk,
                hor[0].id,
                hor[0].nombre_horno,
                ADDITION,
                "AGREGO")
            return redirect('/ladrisur/administrador/ListarHornos/')

        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModificarHorno(SuccessMessageMixin, UpdateView):
    model = Horno
    form_class = FormularioHorno
    template_name = 'administrador/Hornos_Secadores/Hornos/ModificarHorno.html'
    success_url = reverse_lazy('administrador:lis-hor')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        hor = get_object_or_404(Horno, pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=hor)
        if form.is_valid():
            horno = form.save(commit=False)
            horno.nombre_horno = horno.nombre_horno.upper()
            horno.save()

            hor = Horno.objects.get(id=self.kwargs['pk'])

            cad = str(hor.nombre_horno + " " + str(hor.numero_bocas))
            # registramos en la tabla de log la accion realizada
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Horno).pk,
                hor.id,
                cad,
                CHANGE,
                "CAMBIO")
            return redirect('/ladrisur/administrador/ListarCombustibles/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EliminarHorno(SuccessMessageMixin, DeleteView):
    model = Horno
    template_name = 'administrador/Hornos_Secadores/Hornos/EliminarHorno.html'
    success_url = reverse_lazy('administrador:lis-hor')
    success_message = 'Registro Eliminado'

    def post(self, request, *args, **kwargs):
        if Quema.objects.filter(id_horno=self.kwargs['pk']).exists():
            print(
                "No se puede eliminar este Horno porque tiene relacion con uno o mas registros ")
            return render(request, 'administrador/Hornos_Secadores/Hornos/EliminarHorno.html', {'msj': 'No se puede eliminar este Horno porque tiene relacion con uno o mas registros'})
        else:
            hor = Horno.objects.get(id=self.kwargs['pk'])
            cad = str(hor.nombre_horno + " " + str(hor.numero_bocas))
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Horno).pk,
                hor.id,
                cad,
                DELETION,
                "BORRO")
            super().delete(*args, request, **kwargs)
            return redirect('/ladrisur/administrador/ListarHornos/')

# Secaderos


class ListarSecadores(ListView):
    context_object_name = 'lista'
    # paginate_by = 5
    model = Secadero
    template_name = 'administrador/Hornos_Secadores/Secadores/lista_Secadores.html'


class CrearSecadero(SuccessMessageMixin, CreateView):
    model = Secadero
    form_class = FormularioSecadero
    success_url = reverse_lazy('administrador:lis-sec')
    template_name = 'administrador/Hornos_Secadores/Secadores/CrearSecadero.html'
    success_message = 'Registro Agregado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            secadero = form.save(commit=False)
            secadero.nombre_secadero = secadero.nombre_secadero.upper()
            secadero.save()

            sec = Secadero.objects.all().order_by('-id')[:1]
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Secadero).pk,
                sec[0].id,
                sec[0].nombre_secadero,
                ADDITION,
                "AGREGO")
            return redirect('/ladrisur/administrador/ListarSecadores/')

        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModificarSecadero(SuccessMessageMixin, UpdateView):
    model = Secadero
    form_class = FormularioSecadero
    template_name = 'administrador/Hornos_Secadores/Secadores/ModificarSecadero.html'
    success_url = reverse_lazy('administrador:lis-sec')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        sec = get_object_or_404(Secadero, pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=sec)
        if form.is_valid():
            secadero = form.save(commit=False)
            secadero.nombre_secadero = secadero.nombre_secadero.upper()
            secadero.save()

            sec = Secadero.objects.get(id=self.kwargs['pk'])
            # registramos en la tabla de log la accion realizada
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Secadero).pk,
                sec.id,
                sec.nombre_secadero,
                CHANGE,
                "CAMBIO")
            return redirect('/ladrisur/administrador/ListarSecadores/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EliminarSecadero(SuccessMessageMixin, DeleteView):
    model = Secadero
    template_name = 'administrador/Hornos_Secadores/Secadores/EliminarSecadero.html'
    success_url = reverse_lazy('administrador:lis-sec')
    success_message = 'Registro Eliminado'

    def post(self, request, *args, **kwargs):
        if Secado.objects.filter(id_secadero=self.kwargs['pk']).exists():
            print(
                "No se puede eliminar este Secadero porque tiene relacion con uno o mas registros ")
            return render(request, 'administrador/Hornos_Secadores/Secadores/EliminarSecadero.html', {'msj': 'No se puede eliminar este Secadero porque tiene relacion con uno o mas registros'})
        else:
            sec = Secadero.objects.get(id=self.kwargs['pk'])
            # registramos en la tabla de log la accion realizada
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Secadero).pk,
                sec.id,
                sec.nombre_secadero,
                DELETION,
                "BORRO")

            super().delete(*args, request, **kwargs)
            return redirect('/ladrisur/administrador/ListarSecadores/')

# MAQUINAS


class ListarMaquina(ListView):
    context_object_name = 'lista'
    # paginate_by = 5
    model = Maquina
    template_name = 'administrador/Maquinaria-Vehiculos/Maquina/lista_Maquina.html'


class CrearMaquina(SuccessMessageMixin, CreateView):
    model = Maquina
    form_class = FormularioMaquina
    success_url = reverse_lazy('administrador:lis-maq')
    template_name = 'administrador/Maquinaria-Vehiculos/Maquina/CrearMaquina.html'
    success_message = 'Registro Agregado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            maquina = form.save(commit=False)
            maquina.marca_maquina = maquina.marca_maquina.upper()
            maquina.modelo_maquina = maquina.modelo_maquina.upper()
            maquina.save()

            maq = Maquina.objects.all().order_by('-id')[:1]
            cad = str(maq[0].marca_maquina + " " +
                      str(maq[0].año_maquina) + " " + str(maq[0].modelo_maquina))
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Maquina).pk,
                maq[0].id,
                cad,
                ADDITION,
                "AGREGO")
            return redirect('/ladrisur/administrador/ListarMaquina/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModificarMaquina(SuccessMessageMixin, UpdateView):
    model = Maquina
    form_class = FormularioMaquina
    template_name = 'administrador/Maquinaria-Vehiculos/Maquina/ModificarMaquina.html'
    success_url = reverse_lazy('administrador:lis-maq')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        maq = get_object_or_404(Maquina, pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=maq)
        if form.is_valid():
            maquina = form.save(commit=False)
            maquina.marca_maquina = maquina.marca_maquina.upper()
            maquina.modelo_maquina = maquina.modelo_maquina.upper()
            maquina.save()

            maq = Maquina.objects.get(id=self.kwargs['pk'])
            cad = str(maq.marca_maquina + " " +
                      str(maq.año_maquina) + " " + str(maq.modelo_maquina))
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Maquina).pk,
                maq.id,
                cad,
                CHANGE,
                "CAMBIO")
            return redirect('/ladrisur/administrador/ListarMaquina/')


class EliminarMaquina(SuccessMessageMixin, DeleteView):
    model = Maquina
    template_name = 'administrador/Maquinaria-Vehiculos/Maquina/EliminarMaquina.html'
    success_url = reverse_lazy('administrador:lis-maq')
    success_message = 'Registro Eliminado'

    def post(self, request, *args, **kwargs):
        if Tanqueo.objects.filter(id_maquina=self.kwargs['pk']).exists():
            print(
                "No se puede eliminar esta Maquina porque tiene relacion con uno o mas registros ")
            return render(request, 'administrador/Maquinaria-Vehiculos/Maquina/EliminarMaquina.html', {'msj': 'No se puede eliminar esta Maquina porque tiene relacion con uno o mas registros'})
        else:
            maq = Maquina.objects.get(id=self.kwargs['pk'])
            cad = str(maq.marca_maquina + " " +
                      str(maq.año_maquina) + " " + str(maq.modelo_maquina))
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Maquina).pk,
                maq.id,
                cad,
                CHANGE,
                "BORRO")
            super().delete(*args, request, **kwargs)
            return redirect('/ladrisur/administrador/ListarMaquina/')

# VEHICULOS


class ListarVehiculo(ListView):
    context_object_name = 'lista'
    # paginate_by = 5
    model = Vehiculo
    template_name = 'administrador/Maquinaria-Vehiculos/Vehiculo/lista_Vehiculo.html'


class CrearVehiculo(SuccessMessageMixin, CreateView):
    model = Vehiculo
    form_class = FormularioVehiculo
    success_url = reverse_lazy('administrador:lis-veh')
    template_name = 'administrador/Maquinaria-Vehiculos/Vehiculo/CrearVehiculo.html'
    success_message = 'Registro Agregado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.marca_vehiculo = vehiculo.marca_vehiculo.upper()
            vehiculo.modelo_vehiculo = vehiculo.modelo_vehiculo.upper()
            vehiculo.matricula_vehiculo = vehiculo.matricula_vehiculo.upper()

            vehiculo.save()

            veh = Vehiculo.objects.all().order_by('-id')[:1]
            cad = str(veh[0].marca_vehiculo + " " + veh[0].matricula_vehiculo)
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Vehiculo).pk,
                veh[0].id,
                cad,
                ADDITION,
                "AGREGO")
            return redirect('/ladrisur/administrador/ListarVehiculo/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModificarVehiculo(SuccessMessageMixin, UpdateView):
    model = Vehiculo
    form_class = FormularioVehiculo
    template_name = 'administrador/Maquinaria-Vehiculos/Vehiculo/ModificarVehiculo.html'
    success_url = reverse_lazy('administrador:lis-veh')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        veh = get_object_or_404(Vehiculo, pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=veh)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.marca_vehiculo = vehiculo.marca_vehiculo.upper()
            vehiculo.modelo_vehiculo = vehiculo.modelo_vehiculo.upper()
            vehiculo.matricula_vehiculo = vehiculo.matricula_vehiculo.upper()
            vehiculo.save()

            veh = Vehiculo.objects.get(id=self.kwargs['pk'])
            cad = str(veh.marca_vehiculo + " " + veh.matricula_vehiculo)
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Vehiculo).pk,
                veh.id,
                cad,
                CHANGE,
                "CAMBIO")
            return redirect('/ladrisur/administrador/ListarVehiculo/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EliminarVehciulo(SuccessMessageMixin, DeleteView):
    model = Vehiculo
    template_name = 'administrador/Maquinaria-Vehiculos/Vehiculo/EliminarVehiculo.html'
    success_url = reverse_lazy('administrador:lis-veh')
    success_message = 'Registro Eliminado'

    def post(self, request, *args, **kwargs):
        if Entrega_obra.objects.filter(id_vehiculo=self.kwargs['pk']).exists():
            print(
                "No se puede eliminar este Vehiculo porque tiene relacion con uno o mas registros ")
            return render(request, 'administrador/Maquinaria-Vehiculos/Vehiculo/EliminarVehiculo.html', {'msj': 'No se puede eliminar este Vehiculo porque tiene relacion con uno o mas registros'})
        else:
            veh = Vehiculo.objects.get(id=self.kwargs['pk'])
            cad = str(veh.marca_vehiculo + " " + veh.matricula_vehiculo)
            registrarLog(
                request.user.id,
                ContentType.objects.get_for_model(Vehiculo).pk,
                veh.id,
                cad,
                DELETION,
                "BORRO")
            super().delete(*args, request, **kwargs)
            return redirect('/ladrisur/administrador/ListarVehiculo/')
