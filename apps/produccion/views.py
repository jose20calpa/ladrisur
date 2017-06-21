from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.detail import DetailView
import datetime
from datetime import date
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart, BarChart, PieChart, ColumnChart
from graphos.renderers import gchart


from apps.administrador.models import *
from apps.produccion.models import *
from apps.produccion.forms import *
from apps.produccion.validations import *


# PREPRODUCCION


class ListaProduccion_verde(ListView):
    context_object_name = 'lista'
    model = Produccion_verde
    template_name = 'produccion/pre-produccion/lista_RegistrosPreproduccion.html'
    # consulta para listar todas las produccion verdes con sus productos
    query = Produccion_verde.objects.raw(
        '''select
        ipv.id  as cod,
        ipv.id_producto_id,
        ipv.id_produccion_verde_id,
        ipv.cantidad_producto,
        pv.id,
        pv.fecha_produccion_verde,
        p.id,p.nombre_producto

        from produccion_produccion_verde as pv join
        produccion_ingreso_produccion_verde as ipv on
        pv.id = ipv.id_produccion_verde_id
        join administrador_producto as p on
        p.id = ipv.id_producto_id
        order by pv.fecha_produccion_verde''')

    def get_context_data(self, **kwargs):
        context = super(ListaProduccion_verde,
                        self).get_context_data(**kwargs)
        if 'lista_prod' not in context:
            context['lista_prod'] = self.query
        return context


class CrearIngreso_produccion_verde(CreateView):
    template_name = 'produccion/pre-produccion/CrearPreproduccion.html'
    form_class = FormularioProduccion_verde
    second_form_class = FormularioIngreso_produccion_verde

    def get_context_data(self, **kwargs):
        context = super(CrearIngreso_produccion_verde,
                        self).get_context_data(**kwargs)
        if len(Producto.objects.all()) > 0:
            if Produccion_verde.objects.filter(fecha_produccion_verde=date.today()).count() == 1:
                produccion_verde = get_object_or_404(
                    Produccion_verde, fecha_produccion_verde=date.today())
                if Ingreso_produccion_verde.objects.filter(id_produccion_verde=produccion_verde).count() < 2:
                    if 'form' not in context:
                        context['form'] = self.form_class(
                            self.request.GET or None)
                    if 'form2' not in context:
                        context['form2'] = self.second_form_class(
                            self.request.GET or None)
                    if 'fecha' not in context:
                        context['fecha'] = date.today()
                else:
                    context[
                        'msj'] = 'lo sentimos ya ha registrado el maximo numero de productos de este dia'

            if Produccion_verde.objects.filter(fecha_produccion_verde=date.today()).count() == 0:
                if 'form' not in context:
                    context['form'] = self.form_class(self.request.GET or None)
                if 'form2' not in context:
                    context['form2'] = self.second_form_class(
                        self.request.GET or None)
                if 'fecha' not in context:
                    context['fecha'] = date.today()
        else:
            if 'msj' not in context:
                context['msj'] = 'lo sentimos no se han registrado productos'
        return context

    def post(self, request, *args, **kwargs):

        if request.is_ajax:
            self.object = self.get_object
            form = self.form_class(request.POST)
            form2 = self.second_form_class()

            # se recupera todos los datos de la entrada quema
            cantidad_verde = request.POST.getlist('cantidad_verde_tb')
            id_producto = request.POST.getlist('id_producto_tb')
            try:
                can_prod = list(map(int, cantidad_verde))
                ids_prod = list(map(int, id_producto))
            except:
                return render(request, 'produccion/pre-produccion/CrearPreproduccion.html', {'msj1': 'Al parecer hay errores en los datos', 'form': form, 'form2': form2})

            arr_can_aux = can_prod[:]

            # se hace la validacion de los datos que no lleguen vacios
            if id_producto and cantidad_verde:
                # se valida que el arreglo de ids sea igual al de cantidades
                if len(ids_prod) == len(can_prod) and len(ids_prod) <= 2:
                    # valida que no se ingresen mas de dos producciones verdes en un
                    # mismo dia
                    if Produccion_verde.objects.filter(fecha_produccion_verde=date.today()).count() == 0:
                        produccion_verde = form.save(commit=False)
                        produccion_verde.fecha_produccion_verde = date.today()
                        produccion_verde.save()

                    prod_ver = Produccion_verde.objects.all(
                    ).order_by('-id')[:1]
                    #
                    if Ingreso_produccion_verde.objects.filter(id_produccion_verde=prod_ver[0]).count() == 1 and len(can_prod) > 1:
                        return render(request, 'produccion/pre-produccion/CrearPreproduccion.html', {'msj1': 'Solo se permite guardar un producto mas en esta fecha', 'form': form, 'form2': form2})
                    else:
                        if len(ids_prod) > 1:
                            for reg in ids_prod:
                                producto = get_object_or_404(Producto, pk=reg)
                                for can in can_prod:
                                    entrada_producto = Ingreso_produccion_verde(
                                        id_produccion_verde=prod_ver[0], id_producto=producto, cantidad_producto=can)
                                    entrada_producto.save()
                                    break
                                can_prod.pop(0)
                        else:
                            if Ingreso_produccion_verde.objects.filter(id_producto=ids_prod[0], id_produccion_verde=prod_ver).exists():
                                return render(request, 'produccion/pre-produccion/CrearPreproduccion.html', {'msj1': 'Este producto ya se encuentra registrado en esta fecha', 'form': form, 'form2': form2})
                            else:
                                for reg in ids_prod:
                                    producto = get_object_or_404(
                                        Producto, pk=reg)
                                    for can in can_prod:
                                        entrada_producto = Ingreso_produccion_verde(
                                            id_produccion_verde=prod_ver[0], id_producto=producto, cantidad_producto=can)
                                        entrada_producto.save()
                                        break
                                        can_prod.pop(0)
                        return redirect('/ladrisur/produccion/ListaProduccion_verde/')
                else:
                    return render(request, 'produccion/pre-produccion/CrearPreproduccion.html', {'msj1': 'Error al guardar la Informacion', 'form': form, 'form2': form2})
            else:
                return render(request, 'produccion/pre-produccion/CrearPreproduccion.html', {'msj': 'Error al guardar la Informacion'})


class ModificarProductoVerde(SuccessMessageMixin, UpdateView):
    model = Ingreso_produccion_verde
    form_class = FormularioModificarIngreso_produccion_verde
    template_name = 'produccion/pre-produccion/modificarProductoVerde.html'
    success_url = reverse_lazy('produccion:lis-preprod')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        obj = Ingreso_produccion_verde.objects.get(id=self.kwargs['pk'])

        if form.is_valid():

            producto_verde = form.save(commit=False)
            categoria = Producto_Categoria.objects.get(
                id_producto=obj.id_producto.id, nombre_categoria='verde')
            cantidad_global = categoria.cantidad_producto
            cantidad_borrada = obj.cantidad_producto
            res = cantidad_global - cantidad_borrada + producto_verde.cantidad_producto
            res2 = cantidad_global - cantidad_borrada
            print("res2" + str(res2))
            print("cantidad global" + str(cantidad_global))
            print("cantidad borrada" + str(cantidad_borrada))
            print("cantidad modificada" + str(producto_verde.cantidad_producto))
            if (obj.id_producto == producto_verde.id_producto):

                if res >= 0:
                    print("ya se modifico 1")
                    producto_verde.id = obj.id
                    producto_verde.id_produccion_verde = obj.id_produccion_verde
                    form.save()
                    return redirect('/ladrisur/produccion/ListaProduccion_verde/')
                else:
                    print("no se pudo modificar" + str(res))
                    return redirect('/ladrisur/produccion/ListaProduccion_verde/')
            else:
                query = Ingreso_produccion_verde.objects.all().filter(
                    id_produccion_verde=obj.id_produccion_verde)
                ban = False
                for i in query:
                    if i.id_producto == producto_verde.id_producto:
                        ban = True
                        break
                if ban == False:
                    if res >= 0 and res2 > 0:
                        print("ya se modifico 2")
                        producto_verde.id = obj.id
                        producto_verde.id_produccion_verde = obj.id_produccion_verde
                        form.save()
                        return redirect('/ladrisur/produccion/ListaProduccion_verde/')
                    else:
                        print("no se pudo modificar" + str(res))
                        return redirect('/ladrisur/produccion/ListaProduccion_verde/')
                else:
                    return render(request, 'produccion/pre-produccion/modificarProductoVerde.html', {'msj': 'Lo sentimos este producto ya ha sido agregado', 'form': form})
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EliminarIngreso_produccion_verde(DeleteView):
    model = Ingreso_produccion_verde
    template_name = 'produccion\pre-produccion\EliminarIngresoProduccionVerde.html'
    success_url = reverse_lazy('produccion:lis-preprod')

    def post(self, request, *args, **kwargs):
        ingreso = Ingreso_produccion_verde.objects.get(
            id=self.kwargs['pk'])
        con_ingresos = Ingreso_produccion_verde.objects.filter(
            id_produccion_verde=ingreso.id_produccion_verde.id).count()
        categoria = Producto_Categoria.objects.get(
            id_producto=ingreso.id_producto.id, nombre_categoria='verde')
        cantidad_global = categoria.cantidad_producto
        cantidad_borrada = ingreso.cantidad_producto
        res = cantidad_global - cantidad_borrada
        if res >= 0:
            if con_ingresos == 1:
                print("se elimina si solo hay un registro  " + str(res))
                produccion_verde = Produccion_verde.objects.get(
                    id=ingreso.id_produccion_verde.id)
                produccion_verde.delete()
            else:
                print("se elimina cuando hay 2 " + str(res))
                super().delete(request, *args, **kwargs)
            return redirect('/ladrisur/produccion/ListaProduccion_verde/')
        else:
            print("no se pudo eliminar " + str(res))
            return redirect('/ladrisur/produccion/ListaProduccion_verde/')


# REGISTROS QUEMAS
# BOOSTRAP wizard

class DetalleInicioQuema(DetailView):
    model = Entrada_quema
    template_name = 'produccion\produccion\InicioQuema\Detalle_InicioQuema.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleInicioQuema, self).get_context_data(**kwargs)
        entrada_quema = Entrada_quema.objects.get(id=self.kwargs['pk'])
        quema = Quema.objects.get(id=entrada_quema.id_quema.id)

        if 'horno' not in context:
            context['horno'] = quema.id_horno
        if 'lista_prod' not in context:
            context['lista_prod'] = Entrada_quema_producto.objects.filter(
                id_entrada_quema=entrada_quema.id)
        if 'fecha_inicio' not in context:
            context['fecha_inicio'] = entrada_quema.fecha_encendido
        if 'hora_inicio' not in context:
            context['hora_inicio'] = entrada_quema.hora_encendido
        return context


class CrearInicioQuemaWZ (CreateView):
    template_name = "produccion/produccion/InicioQuema/bootw.html"
    form_class = FormularioQuema
    second_form_class = FormularioEntrada_quema
    third_form_class = FormularioEntrada_quema_producto
    query_can_prod = Producto.objects.raw('''select ap.id, ap.nombre_producto, pc.cantidad_producto
            from administrador_producto ap
            join administrador_producto_categoria pc
            on ap.id = pc.id_producto_id
            where pc.nombre_categoria like 'verde' order by ap.nombre_producto ''')

    def get_context_data(self, **kwargs):

        context = super(CrearInicioQuemaWZ, self).get_context_data(**kwargs)
        # se cargan los formularios solo si hay hornos disponibles
        if Horno.objects.filter(estado_horno='Inactivo').count() > 0 and len(Producto.objects.all()) > 0:
            if 'form' in context:

                context['form'] = self.form_class(self.request.GET or None)
                # en el campo de horno solo se lista los hornos que esten
                # inactivos
                context['form'].fields['id_horno'].queryset = Horno.objects.all().filter(
                    estado_horno='Inactivo')
            if 'form2' not in context:
                # se carga el formulario dos de la fecha y la hora
                context['form2'] = self.second_form_class(
                    self.request.GET or None)
            if 'form3' not in context:
                # se carga el formulario 3 para el ingesos productos y
                # cantidades
                context['form3'] = self.third_form_class(
                    self.request.GET or None)

            if 'lista_can_prod' not in context:
                context['lista_can_prod'] = self.query_can_prod

        else:
            if Horno.objects.filter(estado_horno='Inactivo').count() == 0 and len(Producto.objects.all()) > 0:
                if 'msj' not in context:
                    context[
                        'msj'] = 'Lo sentimos no hay productos disponibles'
            if Horno.objects.filter(estado_horno='Inactivo').count() > 0 and len(Producto.objects.all()) == 0:
                if 'msj' not in context:
                    context[
                        'msj'] = 'Lo sentimos no hay hornos registrados'
            if Horno.objects.filter(estado_horno='Inactivo').count() == 0 and len(Producto.objects.all()) == 0:
                if 'msj' not in context:
                    context[
                        'msj'] = 'Lo sentimos no hay productos registrados ni hornos disponibles'

        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            self.object = self.get_object
            form = self.form_class(request.POST)
            form2 = self.second_form_class()
            form3 = self.third_form_class()

            # se recupera todos los datos de la entrada quema

            id_horno = request.POST.getlist('id_horno')
            fecha_encendido = request.POST.getlist('fecha_encendido')
            hora_encendido = request.POST.getlist('hora_encendido')
            cantidad_verde = request.POST.getlist('cantidad_verde_tb')
            id_producto = request.POST.getlist('id_producto_tb')
            hora_encendido = datetime.datetime.strptime(
                convert_to_24(hora_encendido[0]), "%H:%M")

            can_prod = list(map(int, cantidad_verde))
            ids_prod = list(map(int, id_producto))

            arr_can_aux = can_prod[:]
            # se hace la validacion de los datos que no lleguen vacios
            if id_horno and fecha_encendido and hora_encendido and id_producto and cantidad_verde:
                    # se valida que el arreglo de ids sea igual al de
                    # cantidades
                if len(ids_prod) == len(can_prod):
                        # se valida que las cantidades ingresadas sean menores a
                        # las disponibles
                    ban = True
                    for reg in ids_prod:
                        if ban:

                            for can in arr_can_aux:
                                if self.verificar_cantidades(reg, can):
                                    break
                                else:
                                    ban = False
                                    break
                            arr_can_aux.pop(0)
                        else:
                            break

                    if ban:
                        # se registra la quema con su horno
                        quema = form.save(commit=False)
                        horno = Horno.objects.get(id=id_horno[0])
                        quema.id_horno = horno
                        quema.save()
                        # se cambia el estado del horno
                        # horno.estado_horno = 'Activo'
                        horno.save()
                        # se agrega la entrada quema con su fecha y hora
                        consulta_quema = Quema.objects.all(
                        ).order_by('-id')[:1]
                        entrada = form2.save(commit=False)
                        entrada.id_quema = consulta_quema[0]
                        entrada.fecha_encendido = fecha_encendido[0]
                        entrada.hora_encendido = hora_encendido
                        entrada.save()
                        # se agrega la entrada quema con su fecha y hora
                        consulta_quema = Quema.objects.all(
                        ).order_by('-id')[:1]
                        entrada = form2.save(commit=False)
                        entrada.id_quema = consulta_quema[0]
                        entrada.fecha_encendido = fecha_encendido[0]
                        entrada.hora_encendido = hora_encendido
                        entrada.save()
                        consulta_entrada = Entrada_quema.objects.all(
                        ).order_by('-id')[:1]
                        # se guarda los porductos con sus cantidades
                        for reg in ids_prod:
                            producto = Producto.objects.get(id=reg)
                            for can in can_prod:
                                entrada_producto = Entrada_quema_producto(id_entrada_quema=consulta_entrada[
                                    0], id_producto=producto, cantidad_verde=can)
                                entrada_producto.save()
                                break
                            can_prod.pop(0)

                        return render(request, 'produccion\produccion\InicioQuema\QuemaGuardada.html', {'msjdetalle': 'Se ha completado satisfactoriamente el registro de la Quema.', 'msjres': 'Quema Guardada!!'})

                    else:
                        return render(request, 'produccion\produccion\InicioQuema\QuemaGuardada.html', {'form': form, 'form2': form2, 'form3': form3, 'msjdetalle': 'La cantidad de producto verde es inferior a la cantidad que se desea quemar', 'msjres': 'ERROR!!'})
                else:
                    return render(request, 'produccion\produccion\InicioQuema\QuemaGuardada.html', {'form': form, 'form2': form2, 'form3': form3, 'msjres': 'ERROR!!', 'msjdetalle': 'Hay campos vacios en el registro'})

    def verificar_cantidades(self, idprod, can):
        producto = Producto.objects.get(id=idprod)
        prod_cat = Producto_Categoria.objects.filter(
            id_producto=producto, nombre_categoria='verde')
        ban = True
        if can < prod_cat[0].cantidad_producto:
            return ban
        else:
            ban = False
            return ban


# FINALIZAR QUEMA:


class ListarQuemasIniciadas(ListView):
    context_object_name = 'lista'
    model = Quema
    template_name = 'produccion\produccion\FinQuema\Lista_Quema.html'
    query = Quema.objects.raw(
        '''
        select
        ah.id,
        ah.nombre_horno,
        pq.id,
        pq.id_horno_id,
        peq.id,
        peq.fecha_encendido,
        peq.hora_encendido,
        peq.id_quema_id,
        psq.id as cod,
        psq.id_entrada_quema_id

        from administrador_horno as ah join
        produccion_quema as
        pq
        on
        ah.id = pq.id_horno_id
        join
        produccion_entrada_quema as
        peq on
        pq.id = peq.id_quema_id
        join produccion_salida_quema as psq on
        peq.id = psq.id_entrada_quema_id
        where pq.estado_quema like 'Iniciada'
        ''')

    def get_context_data(self, **kwargs):
        context = super(ListarQuemasIniciadas,
                        self).get_context_data(**kwargs)

        if 'lista' in context:
            context['lista'] = self.query
        return context

# Vista Wizard FIN QUEMA


class EliminarInicioQuema(DeleteView):
    model = Quema
    template_name = 'produccion\produccion\InicioQuema\EliminarInicioQuema.html'
    success_url = reverse_lazy('produccion:lis-quem')

    def post(self, request, *args, **kwargs):
        if (Quema_combustible.objects.filter(id_quema=self.kwargs['pk'])):
            print("no puede eliminar")
        else:
            print("si puede eliminar")
            super().delete(*args, request, **kwargs)
            return redirect('/ladrisur/produccion/ListarQuemasIniciadas/')


class ModificarInicioQuema(UpdateView):
    model = Quema
    template_name = 'produccion\produccion\InicioQuema\ModificarInicioQuema.html'
    success_url = reverse_lazy('produccion:lis-quem')
    form_class = FormularioQuema
    second_form_class = FormularioEntrada_quema

    def get_context_data(self, **kwargs):
        context = super(ModificarInicioQuema, self).get_context_data(**kwargs)
        # se cargan los formularios solo si hay hornos disponibles

        if Horno.objects.filter(estado_horno='Inactivo').count() > 0:
            quema = get_object_or_404(Quema, pk=self.kwargs['pk'])
            entrada_quema = get_object_or_404(
                Entrada_quema, id_quema=self.kwargs['pk'])

            #quema =Quema.objects.get(id=self.kwargs['pk'])
            form = self.form_class(self.request.GET or None, instance=quema)
            form2 = self.second_form_class(
                self.request.GET or None, instance=entrada_quema)
            if 'form' in context:

                context['form'] = form
                # en el campo de horno solo se lista los hornos que esten
                # inactivos
                context['form'].fields['id_horno'].queryset = Horno.objects.all().filter(
                    estado_horno='Inactivo')
            if 'form2' not in context:
                # se carga el formulario dos de la fecha y la hora
                context['form2'] = form2
        else:
            if Horno.objects.filter(estado_horno='Inactivo').count() > 0 and len(Producto.objects.all()) == 0:
                if 'msj' not in context:
                    context[
                        'msj'] = 'Lo sentimos no hay hornos registrados'
        return context

    def post(self, request, *args, **kwargs):
        print("post")
        if request.is_ajax:
            print("ajax")
            self.object = self.get_object
            form = self.form_class(request.POST)
            form2 = self.second_form_class()

            # se recupera todos los datos de la entrada quema
            id_horno = request.POST.getlist('id_horno')
            fecha_encendido = request.POST.getlist('fecha_encendido')
            hora_encendido = request.POST.getlist('hora_encendido')
            if id_horno and fecha_encendido and hora_encendido:
                hora_encendido = datetime.datetime.strptime(
                    convert_to_24(hora_encendido[0]), "%H:%M")
                quema = form.save(commit=False)
                horno = Horno.objects.get(id=id_horno[0])
                quema.id_horno = horno
                quema.save()

                # se modifica la entrada quema con su fecha y hora
                entrada_quema = get_object_or_404(
                    Entrada_quema, id_quema=self.kwargs['pk'])
                entrada_quema.fecha_encendido = fecha_encendido[0]
                entrada_quema.hora_encendido = hora_encendido
                entrada_quema.save()
                return redirect('/ladrisur/produccion/ListarQuemasIniciadas/')

            else:
                return self.render_to_response(self.get_context_data(form=form))


class EliminarProductoEntradaQuema(DeleteView):
    model = Entrada_quema_producto
    template_name = 'produccion\produccion\InicioQuema\EliminarProductoEntradaQuema.html'
    success_url = reverse_lazy('produccion:lis-quem')

    def get_context_data(self, **kwargs):

        context = super(EliminarProductoEntradaQuema,
                        self).get_context_data(**kwargs)
        entrada_producto = Entrada_quema_producto.objects.get(
            id=self.kwargs['pk'])
        con_ingresos = Entrada_quema_producto.objects.filter(
            id_entrada_quema=entrada_producto.id_entrada_quema.id).count()

        if con_ingresos == 1:
            if 'msj' not in context:
                context[
                    'msj'] = 'Atencion este es el ultimo producto por lo tanto se borrara toda la quema!!!'
        if 'idquemini'not in context:
            context['idquemini'] = entrada_producto.id_entrada_quema.id
        if 'producto' not in context:
            context['producto'] = entrada_producto.id_producto
        if 'cantidad' not in context:
            context['cantidad'] = entrada_producto.cantidad_verde

        return context

    def post(self, request, *args, **kwargs):
        ingreso = Entrada_quema_producto.objects.get(
            id=self.kwargs['pk'])
        con_ingresos = Entrada_quema_producto.objects.filter(
            id_entrada_quema=ingreso.id_entrada_quema.id).count()
        categoria = Producto_Categoria.objects.get(
            id_producto=ingreso.id_producto.id, nombre_categoria='verde')
        cantidad_global = categoria.cantidad_producto
        cantidad_borrada = ingreso.cantidad_verde
        res = cantidad_global - cantidad_borrada
        if res >= 0:
            if con_ingresos == 1:
                print("se elimina si solo hay un registro  " + str(res))
                entrada_quema = Entrada_quema.objects.get(
                    id=ingreso.id_entrada_quema.id)
                quema = Quema.objects.get(
                    id=entrada_quema.id_quema.id)
                quema.delete()
                return redirect('/ladrisur/produccion/ListarQuemasIniciadas/')
            else:
                print("se elimina cuando hay 2 " + str(res))
                super().delete(request, *args, **kwargs)
            return redirect('/ladrisur/produccion/ListarQuemasIniciadas/')
        else:
            print("no se pudo eliminar " + str(res))
            return redirect('/ladrisur/produccion/ListarQuemasIniciadas/')


class ModificarProductoEntradaQuema(SuccessMessageMixin, UpdateView):
    model = Entrada_quema_producto
    form_class = FormularioEntrada_quema_producto
    template_name = 'produccion\produccion\InicioQuema\ModificarProductoEntredaQuema.html'
    success_url = reverse_lazy('produccion:lis-quem')
    success_message = 'Registro modificado'

    def get_context_data(self, **kwargs):

        context = super(ModificarProductoEntradaQuema,
                        self).get_context_data(**kwargs)
        entrada_producto = Entrada_quema_producto.objects.get(
            id=self.kwargs['pk'])

        if 'id_entrada'not in context:
            context['id_entrada'] = entrada_producto.id
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        obj = Entrada_quema_producto.objects.get(id=self.kwargs['pk'])
        entrada_quema_producto = form.save(commit=False)

        if entrada_quema_producto.id_producto and entrada_quema_producto.cantidad_verde:

            categoria = Producto_Categoria.objects.get(
                id_producto=obj.id_producto.id, nombre_categoria='verde')

            cantidad_global = categoria.cantidad_producto
            cantidad_borrada = obj.cantidad_verde
            # la variable res sirve para validar la entrada
            res = cantidad_global + cantidad_borrada - entrada_quema_producto.cantidad_verde
            print("res" + str(res))

            print("cantidad global" + str(cantidad_global))
            print("cantidad borrada" + str(cantidad_borrada))
            print("cantidad modificada" +
                  str(entrada_quema_producto.cantidad_verde))
            # cuando no se cambia el producto
            if (obj.id_producto == entrada_quema_producto.id_producto):

                if res >= 0:
                    print("ya se modifico ")
                    entrada_quema_producto.id = obj.id
                    entrada_quema_producto.id_entrada_quema = obj.id_entrada_quema
                    entrada_quema_producto.save()
                    return redirect('/ladrisur/produccion/DetalleInicioQuema/' + str(obj.id_entrada_quema.id))
                else:
                    print("no se pudo modificar" + str(res))
                    return redirect('/ladrisur/produccion/DetalleInicioQuema/' + str(obj.id_entrada_quema.id))
            else:
                # validacaion para buscar si el producto que cambio ya se
                # encuentra en esa entrada_quema_producto
                query = Entrada_quema_producto.objects.all().filter(
                    id_entrada_quema=obj.id_entrada_quema)
                ban = False
                for i in query:
                    if i.id_producto == entrada_quema_producto.id_producto:
                        ban = True
                        break
                if ban == False:
                    categoria2 = Producto_Categoria.objects.get(
                        id_producto=entrada_quema_producto.id_producto.id, nombre_categoria='verde')
                    cantidad_global2 = categoria2.cantidad_producto
                    # la variable res calcula la diferencia entre la cantidad de producto verde global del producto
                    # nuevo y la cantidad nueva del formulario
                    res2 = cantidad_global2 - entrada_quema_producto.cantidad_verde
                    if res2 >= 0:
                        entrada_quema_producto.id = obj.id
                        entrada_quema_producto.id_entrada_quema = obj.id_entrada_quema
                        entrada_quema_producto.save()
                        return redirect('/ladrisur/produccion/DetalleInicioQuema/' + str(obj.id_entrada_quema.id))
                    else:
                        return redirect('/ladrisur/produccion/DetalleInicioQuema/' +
                                        str(obj.id_entrada_quema.id))
                else:
                    print("error por ingresar un producto ya registrado")
                    return render(request, 'produccion\produccion\InicioQuema\ModificarProductoEntredaQuema.html', {'msjres': 'Este producto ya se ecnuentra en esta Entrada quema !!', 'form': form})
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CrearFinQuemaWZ(CreateView):
    model = Salida_quema
    form_class = FormularioQuema_combustible
    second_form_class = FormularioSalida_quema
    template_name = 'produccion\produccion\FinQuema\Finalizar_Quema.html'

    def get_context_data(self, **kwargs):

        context = super(CrearFinQuemaWZ, self).get_context_data(**kwargs)
        salida_quema = Salida_quema.objects.get(id=self.kwargs['pk'])
        entrada_quema = Entrada_quema.objects.get(
            id=salida_quema.id_entrada_quema.id)

        if Quema_combustible.objects.filter(id_quema=entrada_quema.id_quema.id).exists():
            if 'msj1' not in context:

                context['msj1'] = 'ya ha finalzado esta quema'
        else:
            if 'fecha_inicio' not in context:
                context['fecha_inicio'] = entrada_quema.fecha_encendido
            if 'lista_hor' not in context:
                try:
                    query_cargo = Cargo.objects.get(nombre_cargo='HORNERO')
                    horneros = Empleado.objects.filter(id_cargo=query_cargo)
                    context['lista_hor'] = horneros
                except:
                    context['msj1'] = 'No se encuentra Horneros registrados'
            if 'lista_prod' not in context:
                try:
                    consul_sal_prod = Salida_quema_producto.objects.filter(
                        id_salida_quema=self.kwargs['pk']).order_by('id')
                    context['lista_prod'] = consul_sal_prod
                except:
                    context['msj1'] = ''
            if 'lista_com' not in context:
                try:
                    consul_com = Combustible.objects.all().filter(uso='Hornos')
                    context['lista_com'] = consul_com
                except:
                    context['msj1'] = ''
            if 'formCom' not in context:
                context['formCom'] = self.form_class(self.request.GET or None)
                context['formCom'].fields['id_combustible'].queryset = Combustible.objects.all().filter(
                    uso='Hornos')

            if 'formSal' not in context:
                context['formSal'] = self.second_form_class(
                    self.request.GET or None)

        return context

    def post(self, request, *args, **kwargs):

        if request.is_ajax:
                # se recupera todos los horneros seleccionados
            fecha_apagado = request.POST.getlist('fecha_apagado')
            hora_apagado = request.POST.getlist('hora_apagado')
            ids_horn = request.POST.getlist('select')
            can_prod = request.POST.getlist('can_pro')
            ids_can_prod = request.POST.getlist('ids_pro')
            can_com = request.POST.getlist('cantidad_combustible_tb')
            ids_com = request.POST.getlist('id_combustible_tb')

            if fecha_apagado and hora_apagado and ids_horn and can_prod and ids_can_prod and can_com and ids_com:

                hora_apagado = datetime.datetime.strptime(
                    convert_to_24(hora_apagado[0]), "%H:%M")

                for reg in ids_horn:
                    if(reg == 'all'):
                        ids_horn.remove("all")
                        break
                # Convertir toda la lista a numeros enteros
                ids_horn = list(map(int, ids_horn))
                # ids y cantidades productos
                can_prod = list(map(int, can_prod))
                ids_can_prod = list(map(int, ids_can_prod))
                # ids y cantidades combustibles
                can_com = list(map(int, can_com))
                ids_com = list(map(int, ids_com))

                arr_can_aux = can_prod[:]
                arr_com_aux = can_com[:]

                # obtener la entrada quema para consultar la fecha

                consulta_salida_quema = Salida_quema.objects.filter(
                    id=self.kwargs['pk'])

                entrada_quema = Entrada_quema.objects.get(
                    id=consulta_salida_quema[0].id_entrada_quema.id)
                quema = Quema.objects.get(id=entrada_quema.id_quema.id)
                # validar fecha_apagado
                val_fec = self.validar_fecha(
                    fecha_apagado[0], entrada_quema.fecha_encendido)
                # validar cantidaes de productos
                val_can_prod = self.validate_cant_prod(
                    ids_can_prod, arr_can_aux)

                # validar cantidades de combustibles

                val_can_com = self.validate_cant_combustible(
                    ids_com, arr_com_aux)

                consulta_salida_quema = Salida_quema.objects.get(
                    id=self.kwargs['pk'])
                if val_fec and val_can_prod and val_can_com:
                    # guardamos la fecha y la hora de la salida quema
                    consulta_salida_quema.fecha_apagado = fecha_apagado[0]
                    consulta_salida_quema.hora_apagado = hora_apagado
                    consulta_salida_quema.save()
                    # guardamos los empleados participantes en la salida quema
                    consulta_salida_quema = Salida_quema.objects.filter(
                        id=self.kwargs['pk'])
                    for hornero in consulta_salida_quema:
                        for i in ids_horn:
                            hornero.id_empleado.add(i)
                            # registramos los productos con sus cantidades

                    for i in ids_can_prod:
                        objSalQuem = Salida_quema_producto.objects.get(id=i)

                        for j in range(len(can_prod)):

                            # Asigna Cantidadas
                            objSalQuem.cantidad_primera = can_prod[j]
                            objSalQuem.cantidad_segunda = can_prod[j + 1]
                            objSalQuem.cantidad_crudo = can_prod[j + 2]
                            can_dañ = (
                                objSalQuem.cantidad_verde - (can_prod[j] + can_prod[j + 1] + can_prod[j + 2]))
                            objSalQuem.cantidad_dañados = can_dañ
                            # Asigna nuevos estados
                            objSalQuem2 = Salida_quema.objects.get(
                                id=objSalQuem.id_salida_quema.id)
                            objEnt = Entrada_quema.objects.get(
                                id=objSalQuem2.id_entrada_quema.id)
                            objQuem = Quema.objects.get(
                                id=objEnt.id_quema.id)
                            objQuem.estado_quema = 'Finalizada'
                            objHor = Horno.objects.get(
                                id=objQuem.id_horno.id)
                            objHor.estado_horno = 'Inactivo'
                            # Guardamos
                            objSalQuem.save()
                            objQuem.save()
                            objHor.save()
                            break
                        try:
                            can_prod.pop(0)
                            can_prod.pop(0)
                            can_prod.pop(0)
                        except:
                            break
                    for reg in ids_com:
                        combustible = Combustible.objects.get(id=reg)
                        for can in can_com:
                            quema_combustible = Quema_combustible(
                                id_quema=quema, id_combustible=combustible, cantidad_combustible=can)
                            quema_combustible.save()
                            break
                        can_com.pop(0)

                    return render(request, 'produccion\produccion\FinQuema\QuemaTerminada.html', {'msjdetalle': 'Se ha completado satisfactoriamente la quema.', 'msjres': 'Quema Guardada!!'})

                else:
                    cad = ""
                    if val_fec == False:
                        cad = "Error en Fecha --> debe ser superior o igual a la de inicio  "
                    if val_can_prod == False:
                        cad += "Error en Cantidad Producto--> Las cantidades de los productos que salieron son superiores a las cantidades que entraron  "
                    if val_can_com == False:
                        cad += "Error en Cantidad Combustible--> Las cantidades de los Combustibles que se usaron son superiores a las cantidades de inventario  "

                    return render(request, 'produccion\produccion\FinQuema\QuemaTerminada.html', {'msjdetalle': cad, 'msjres': 'ERROR!!'})

            else:
                return render(request, 'produccion\produccion\FinQuema\QuemaTerminada.html', {'msjdetalle': 'llegaron datos vacios', 'msjres': 'ERROR!!'})

    def validar_fecha(self, fecha_apagado, fecha_encendido):
        # se compara la fecha de entrada quema con la fecha de salida quema
        if str(fecha_apagado) > str(fecha_encendido):
            return True
        else:
            return False

    def validate_cant_prod(self, ids_can_prod, can_prod):
        ban = True
        for i in ids_can_prod:
            if ban:
                for j in range(len(can_prod)):
                    objSalQuem = Salida_quema_producto.objects.get(id=i)
                    can_dañ = (objSalQuem.cantidad_verde -
                               (can_prod[j] + can_prod[j + 1] + can_prod[j + 2]))
                    if(can_dañ < 0):
                        ban = False
                        break
                    else:
                        break
                can_prod.pop(0)
                can_prod.pop(0)
                can_prod.pop(0)
            else:
                break
        return ban

    def validate_cant_combustible(self, ids_com, can_com):
        ban = True

        for reg in ids_com:
            if ban:
                for can in can_com:
                    combus = Combustible.objects.get(id=reg)
                    if can < combus.cantidad_total_combustible:
                        break
                    else:
                        ban = False
                        break
                can_com.pop(0)
            else:
                break
        return ban


# lista de quemas finalizadas


class ListarQuemasFinalizadas(ListView):
    context_object_name = 'lista'
    model = Quema
    template_name = 'produccion\produccion\FinQuema\Lista_Quema_Fin.html'
    query = Quema.objects.raw(
        '''
        select
        pq.id,
        peq.fecha_encendido,
        peq.hora_encendido,
        psq.fecha_apagado,
        psq.id as cod,
        psq.hora_apagado
        from produccion_quema as pq
        join produccion_entrada_quema as peq
        on pq.id = peq.id_quema_id
        join produccion_salida_quema as psq
        on peq.id = psq.id_entrada_quema_id
        where pq.estado_quema like 'Finalizada';
        ''')

    def get_context_data(self, **kwargs):
        context = super(ListarQuemasFinalizadas,
                        self).get_context_data(**kwargs)

        if 'lista' in context:
            context['lista'] = self.query
        return context

# Detalles de quema finalizada


class DetalleQuema(DetailView):
    model = Salida_quema
    template_name = 'produccion\produccion\FinQuema\Detalle_Quema_Fin.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleQuema, self).get_context_data(**kwargs)
        salida_quema = Salida_quema.objects.get(id=self.kwargs['pk'])
        entrada_quema = Entrada_quema.objects.get(
            id=salida_quema.id_entrada_quema.id)
        quema = Quema.objects.get(id=entrada_quema.id_quema.id)

        if 'datos_quema' not in context:
            context['datos_quema'] = query = Quema.objects.raw(
                '''
                select
                peq.fecha_encendido,
                peq.hora_encendido,
                psq.fecha_apagado,
                psq.id,
                psq.hora_apagado
                from produccion_quema as pq
                join produccion_entrada_quema as peq
                on pq.id = peq.id_quema_id
                join produccion_salida_quema as psq
                on peq.id = psq.id_entrada_quema_id
                where pq.estado_quema like 'Finalizada' and pq.id = %s
                ''', [quema.id])

        if 'horno' not in context:
            context['horno'] = quema.id_horno
        if 'lista_prod' not in context:
            context['lista_prod'] = Salida_quema_producto.objects.filter(id_salida_quema=self.kwargs[
                'pk'])
        if 'lista_comb' not in context:
            context['lista_comb'] = Quema_combustible.objects.filter(
                id_quema=quema.id)
        if 'lista_emp' not in context:
            context['lista_emp'] = salida_quema.id_empleado.all()
        return context

# TANQUEO


class ListaTanqueos(ListView):
    context_object_name = 'Lista_tanqueos'
    model = Tanqueo
    template_name = 'produccion/consumo/tanqueo_maquinaria/lista_Tanqueos.html'
    query = Quema.objects.raw(
        '''
        select
        pq.id,
        peq.fecha_encendido,
        peq.hora_encendido,
        psq.fecha_apagado,
        psq.id as cod,
        psq.hora_apagado
        from produccion_quema as pq
        join produccion_entrada_quema as peq
        on pq.id = peq.id_quema_id
        join produccion_salida_quema as psq
        on peq.id = psq.id_entrada_quema_id
        where pq.estado_quema like 'Finalizada';
        ''')


class CrearTanqueo(CreateView):
    model = Tanqueo
    form_class = FormularioTanqueo
    template_name = 'produccion/consumo/tanqueo_maquinaria/CrearTanqueo.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid() and Combustible.objects.filter(nombre_combustible='ACPM').exists():
            combustible = Combustible.objects.get(nombre_combustible='ACPM')
            tanqueo = form.save(commit=False)
            tanqueo.fecha_tanqueo = date.today()
            tanqueo.id_combustible = combustible
            if tanqueo.cantidad_tanqueo <= combustible.cantidad_total_combustible:
                print("si puede guadar")
                tanqueo.save()
                return redirect('/ladrisur/produccion/ListarTanqueosMaquinaria/')
            else:
                print("no puede guadar")
                return render(request, 'produccion/consumo/tanqueo_maquinaria/CrearTanqueo.html', {'msjres': 'No hay suficiente ACPM para completar este registro', 'form': form})
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ModificarTanqueo(SuccessMessageMixin, UpdateView):
    model = Tanqueo
    form_class = FormularioTanqueo
    template_name = 'produccion/consumo/tanqueo_maquinaria/ModificarTanqueo.html'
    success_url = reverse_lazy('produccion:lis-tan')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid() and Combustible.objects.filter(nombre_combustible='ACPM').exists():
            obj = Tanqueo.objects.get(id=self.kwargs['pk'])
            combustible = Combustible.objects.get(nombre_combustible='ACPM')
            tanqueo = form.save(commit=False)
            tanqueo.id = obj.id
            tanqueo.id_combustible = combustible
            res = combustible.cantidad_total_combustible - \
                tanqueo.cantidad_tanqueo + obj.cantidad_tanqueo
            if res >= 0:
                tanqueo.save()
                return redirect('/ladrisur/produccion/ListarTanqueosMaquinaria/')
            else:
                return render(request, 'produccion/consumo/tanqueo_maquinaria/CrearTanqueo.html', {'msjres': 'No hay suficiente ACPM para completar este registro', 'form': form})

        else:
            return self.render_to_response(self.get_context_data(form=form))


class EliminarTanqueo(DeleteView):
    model = Tanqueo
    template_name = 'produccion/consumo/tanqueo_maquinaria/EliminarTanqueo.html'
    success_url = reverse_lazy('produccion:lis-tan')


# CONSUMO SECADEROS


class ListaSecados(ListView):
    context_object_name = 'Lista_secados'
    model = Secado
    template_name = 'produccion/consumo/consumo_secadero/Lista_secados.html'
    query = Secado.objects.raw(
        '''
        select
        ps.id,
        ps.fecha_secado,
        ase.nombre_secadero

        from administrador_secadero as ase join
        produccion_secado as
        ps
        on
        ase.id = ps.id_secadero_id
        ''')

    def get_context_data(self, **kwargs):
        context = super(ListaSecados,
                        self).get_context_data(**kwargs)

        if 'Lista_secados' in context:
            context['Lista_secados'] = self.query
        return context


class CrearSecado(CreateView):
    template_name = 'produccion/consumo/consumo_secadero/CrearSecado.html'
    form_class = FormularioSecado
    second_form_class = FormularioSecado_combustible

    def get_context_data(self, **kwargs):
        combustibles = Combustible.objects.filter(uso='Hornos')
        data = [['', 'Combustible (Galones)']]

        for com in combustibles:
            data.append([str(com.nombre_combustible) + "(" + str(com.cantidad_total_combustible) + ")",
                         com.cantidad_total_combustible])
        # DataSource object
        data_source = SimpleDataSource(data=data)
        # Chart object
        chart = gchart.ColumnChart(data_source, options={'width': 500,
                                                         'height': 240,
                                                         'bar': {'groupWidth': "40%"},
                                                         #'chartArea': {'width': "50%", 'height': "50%"},
                                                         'title': 'Combustibles ',
                                                         'is3D': False,
                                                         #'annotations': {style: 'line'},
                                                         'series': [
                                                             {'color': '#00685c'}]})

        context = super(CrearSecado, self).get_context_data(**kwargs)
        context['chart'] = chart
        if len(Combustible.objects.all()) > 0:
            if 'form' not in context:
                context['form'] = self.form_class(self.request.GET or None)

            if 'form2' not in context:

                context['form2'] = self.second_form_class(
                    self.request.GET or None)
                context['form2'].fields['id_combustible'].queryset = Combustible.objects.all().filter(
                    uso='Hornos')
        else:
            context['msj'] = 'lo sentimos no se han registrado Combustibles'
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            self.object = self.get_object
            form = self.form_class(request.POST)
            form2 = self.second_form_class()

            # se recupera todos los datos de la entrada quema

            secadero = request.POST.getlist('id_secadero')
            fecha_secado = request.POST.getlist('fecha_secado')
            cantidad_combustible = request.POST.getlist(
                'cantidad_combustible_tb')
            id_combustible = request.POST.getlist('id_combustible_tb')

            # se hace la validacion de los datos que no lleguen vacios
            if secadero and fecha_secado and cantidad_combustible and id_combustible:
                can_com = list(map(int, cantidad_combustible))
                id_combustible = list(map(int, id_combustible))
                arr_can_aux = can_com[:]
                # se valida que el arreglo de ids sea igual al de
                # cantidades
                if len(id_combustible) == len(can_com):
                    # se valida que las cantidades ingresadas sean menores a
                    # las disponibles
                    ban = True
                    for reg in id_combustible:
                        if ban:
                            for can in arr_can_aux:
                                if self.verificar_cantidades(reg, can):
                                    break
                                else:
                                    ban = False
                                    break
                            arr_can_aux.pop(0)
                        else:
                            break

                    if ban:
                        secadero = Secadero.objects.get(id=secadero[0])
                        secado = Secado(fecha_secado=fecha_secado[
                            0], id_secadero=secadero)
                        secado.save()
                        consulta_secado = Secado.objects.all(
                        ).order_by('-id')[:1]
                        # se guarda los combustibles con sus cantidades
                        for reg in id_combustible:
                            combustible = Combustible.objects.get(id=reg)
                            for can in can_com:
                                secado_combustible = Secado_combustible(id_secado=consulta_secado[
                                    0], id_combustible=combustible, cantidad_combustible=can)
                                secado_combustible.save()
                                break
                            can_com.pop(0)

                        query = Secado.objects.raw(
                            '''select
                                ps.id,
                                ps.fecha_secado,
                                ase.nombre_secadero

                                from administrador_secadero as ase join
                                produccion_secado as
                                ps
                                on
                                ase.id = ps.id_secadero_id
                                ''')
                        return render(request, 'produccion/consumo/consumo_secadero/lista_secados.html', {'msjdetalle': 'Se ha completado satisfactoriamente el registro del Secado.', 'msjres': 'Secado Guardado!!', 'Lista_secados': query})

                    else:
                        return render(request, 'produccion/consumo/consumo_secadero/CrearSecado.html', {'form': form, 'form2': form2, 'msjdetalle': 'La cantidad de combustible ingresada es mayor  a la cantidad disponible', 'msjres': 'ERROR!!'})
            else:
                return render(request, 'produccion/consumo/consumo_secadero/CrearSecado.html', {'form': form, 'form2': form2, 'msjres': 'ERROR!!', 'msjdetalle': 'Hay campos vacios en el registro'})

    def verificar_cantidades(self, idcom, can):
        combustible = Combustible.objects.get(id=idcom)
        ban = True
        if can < combustible.cantidad_total_combustible:
            return ban
        else:
            ban = False
            return ban


class EliminarSecado(DeleteView):
    model = Secado
    template_name = 'produccion/consumo/consumo_secadero/EliminarSecado.html'
    success_url = reverse_lazy('produccion:lis-sec')


class EliminarSecadoCombustible(DeleteView):
    model = Secado_combustible
    template_name = 'produccion/consumo/consumo_secadero/EliminarSecadoCombustible.html'
    success_url = reverse_lazy('produccion:lis-sec')

    def get_context_data(self, **kwargs):

        context = super(EliminarSecadoCombustible,
                        self).get_context_data(**kwargs)
        secado_combustible = Secado_combustible.objects.get(
            id=self.kwargs['pk'])
        con_secados = Secado_combustible.objects.filter(
            id_secado=secado_combustible.id_secado.id).count()

        if con_secados == 1:
            if 'msj' not in context:
                context[
                    'msj'] = 'Atencion este es el ultimo combustible por lo tanto se borrara toda el secado!!!'
        if 'idsec'not in context:
            context['idsec'] = secado_combustible.id_secado.id
        return context

    def post(self, request, *args, **kwargs):
        secado_combustible = Secado_combustible.objects.get(
            id=self.kwargs['pk'])
        con_secados = Secado_combustible.objects.filter(
            id_secado=secado_combustible.id_secado.id).count()
        secado = Secado.objects.get(id=secado_combustible.id_secado.id)
        if con_secados == 1:
            print("se elimina si solo hay un registro  ")
            secado.delete()
            return redirect('/ladrisur/produccion/ListarSecados/')
        else:
            print("se elimina cuando hay 2 ")
            super().delete(request, *args, **kwargs)
            return redirect('/ladrisur/produccion/DetalleSecado/' + str(secado.id))


class ModificarSecado(UpdateView):
    model = Secado
    template_name = 'produccion\consumo\consumo_secadero\ModificarSecado.html'
    success_url = reverse_lazy('produccion:lis-sec')
    form_class = FormularioSecado


class ModificarSeacadoCombustible(SuccessMessageMixin, UpdateView):
    model = Secado_combustible
    form_class = FormularioSecado_combustible
    template_name = 'produccion\consumo\consumo_secadero\ModificarSecadoCombustible.html'
    success_url = reverse_lazy('produccion:lis-sec')
    success_message = 'Registro modificado'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        obj = Secado_combustible.objects.get(id=self.kwargs['pk'])
        secado_combustible = form.save(commit=False)

        if secado_combustible.id_combustible and secado_combustible.cantidad_combustible:

            combustible = Combustible.objects.get(
                id=obj.id_combustible.id)

            cantidad_global = combustible.cantidad_total_combustible
            cantidad_borrada = obj.cantidad_combustible

            # la variable res sirve para validar la entrada
            res = cantidad_global + cantidad_borrada - \
                secado_combustible.cantidad_combustible
            print("res" + str(res))

            print("cantidad global" + str(cantidad_global))
            print("cantidad borrada" + str(cantidad_borrada))
            print("cantidad modificada" +
                  str(secado_combustible.cantidad_combustible))
            # cuando no se cambia el producto
            if (obj.id_combustible == secado_combustible.id_combustible):

                if res >= 0:
                    print("ya se modifico ")
                    secado_combustible.id = obj.id
                    secado_combustible.id_secado = obj.id_secado
                    secado_combustible.save()
                    return redirect('/ladrisur/produccion/DetalleSecado/' + str(obj.id_secado.id))
                else:
                    print("no se pudo modificar" + str(res))
                    return render(request, 'produccion/consumo/tanqueo_maquinaria/ModificarSeacadoCombustible.html', {'form': form, 'msjres': 'La cantidad de combustible ingresada es mayor  a la cantidad disponible'})
            else:
                # validacaion para buscar si el combustible que cambio ya se
                # encuentra en ese secado
                query = Secado_combustible.objects.all().filter(
                    id_secado=obj.id_secado)
                ban = False
                for i in query:
                    if i.id_combustible == secado_combustible.id_combustible:
                        ban = True
                        break
                if ban == False:
                    print("cuando cambia de combustible")

                    combustible2 = Combustible.objects.get(
                        id=secado_combustible.id_combustible.id)
                    cantidad_global2 = combustible2.cantidad_total_combustible
                    # la variable res calcula la diferencia entre la cantidad de combustible
                    # nuevo y la cantidad nueva del formulario
                    print("cantidad_global2  " + str(cantidad_global2))
                    if cantidad_global2 >= secado_combustible.cantidad_combustible:
                        print("ya se modifico 2")
                        secado_combustible.id = obj.id
                        secado_combustible.id_secado = obj.id_secado
                        secado_combustible.save()
                        return redirect('/ladrisur/produccion/DetalleSecado/' + str(obj.id_secado.id))
                    else:
                        print("no se pudo modificar" + str(res))
                        return render(request, 'produccion/consumo/tanqueo_maquinaria/ModificarSeacadoCombustible.html', {'form': form, 'msjres': 'La cantidad de combustible ingresada es mayor  a la cantidad disponible'})

                else:
                    return render(request, 'produccion/consumo/tanqueo_maquinaria/ModificarSeacadoCombustible.html', {'form': form, 'msjres': 'Este combustible ya ha sido registrado en este secado'})

        else:
            return self.render_to_response(self.get_context_data(form=form))


class DetalleSecado(DetailView):
    model = Secado
    template_name = 'produccion/consumo/consumo_secadero/Detalle_Secado_Fin.html'

    def get(self, request, *args, **kwargs):
        if Secado.objects.filter(id=self.kwargs['pk']).exists():
            secado = Secado.objects.get(id=self.kwargs['pk'])
            secadero = secado.id_secadero
            fecha = secado.fecha_secado
            lista_comb = Secado_combustible.objects.filter(id_secado=secado.id)
            return render(request, self.template_name, {'secado': secado, 'secadero': secadero, 'fecha': fecha, 'lista_comb': lista_comb})

        else:
            msj1 = 'No hay datos para este secado'
            return render(request, self.template_name, {'msj1': msj1})


def convert_to_24(time):
    if len(str(time)) == 7:
        time = '0' + time
    if time[-2:] == "AM":
        if int(time[:2]) == 12:
            time = time.replace('12', '00')
        return time[0:5]
    else:
        if int(time[:2]) == 12:
            time = time.replace('12', '12')
            return time[0:5]
        else:
            time = time.replace(str(time[:2]), str(int(time[:2]) + 12))
            return time[0:5]
