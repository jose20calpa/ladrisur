$(document).ready(function() {
    //DESHABILITAE ENTER DEL FORMULARIO
    $("#frm_ini_quem").keypress(function(e) { //Para deshabilitar el uso de la tecla "Enter"
        if (e.which == 13) {
            return false;
        }
    });

    //ARRAYS DE productos
    var lis_pro_val = new Array;
    var lis_pro_nom = new Array;
    var lis_can = new Array;
    //contador pasos
    var conpas = 0;

    //ELIMINAR DE LA TABLA AUXILIAR DE PRODUCTOS AGREGADOS
    //de los Array

    //tabla
    $("#btnAgrPro").click(function() {
        var sel_pro = document.getElementById('id_id_producto');
        var pro = document.getElementById('id_id_producto').value;
        var can = document.getElementById('id_cantidad_verde').value;
        if (pro == "" || can == "") {
            document.getElementById("diverrP2").style.display = "block";
            document.getElementById("divmsjerrP2").innerHTML = "Por favor revisa que los campos no esten vacios.";
        } else {
            document.getElementById("diverrP2").style.display = "none";

            //mostrar Boton Finalizar
            document.getElementById('btnProds').style.display = 'block';
            if (ValProductosRep(pro) && ValCantidadesVerdes(pro, can)) {
                //Nombre del Producto
                var nom_pro = sel_pro.options[sel_pro.selectedIndex].text;
                //llenamos los arreglos
                lis_pro_val.push(pro);
                lis_pro_nom.push(nom_pro);
                lis_can.push(can);
                //Limpiamos msj de error anterior
                document.getElementById("diverrP2").style.display = "none";
                //limpiamos el formulario
                sel_pro.value = "";
                document.getElementById('id_cantidad_verde').value = '';
                mostrarTabla(pro, nom_pro, can);

            } else {
                if (!(ValProductosRep(pro))) {
                    document.getElementById("diverrP2").style.display = "block";
                    document.getElementById("divmsjerrP2").innerHTML = "El producto ya ha sido guardado";
                }

                if (!(ValCantidadesVerdes(pro, can))) {
                    document.getElementById("diverrP2").style.display = "block";
                    document.getElementById("divmsjerrP2").innerHTML = "La Cantidad de Productos Quemados Superó a la Cantidad de Inventario Verde o es Negativa";

                }
            }
        }
    });

    function ValProductosRep(producto) {
        for (var i = 0; i < lis_pro_val.length; i++) {
            if (lis_pro_val[i] == producto) {
                return false;
                break;
            }
        }
        return true;
    }

    function ValCantidadesVerdes(pro, can) {
        var pro = document.getElementById('id_id_producto').value;
        var idproinp = "can-" + pro;
        var canVer = document.getElementById(idproinp).value;
        invVer = parseInt(canVer);
        canIng = parseInt(can);

        if (canIng > invVer || can < 0) {
            return false;
        } else {
            return true;
        }

    }



    function mostrarTabla(pro, nom_pro, can) {


        //añadir tabla

        var table = document.getElementById('tbl-pro');
        var divTbl = document.getElementById('divTbl');
        divTbl.style.display = "block";
        var rowCount = table.rows.length;
        var row = table.insertRow(rowCount);
        row.id = pro;
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        cell4.innerHTML = "<input type='hidden' name='id_producto_tb' value=" + pro + ">";
        cell1.innerHTML = "<input type='hidden' name='nom_pro_tb' value=" + nom_pro + "><p>" + nom_pro + "</p>";
        cell2.innerHTML = "<input type='hidden' name='cantidad_verde_tb' value=" + can + "><p>" + can + "</p>";
        cell3.innerHTML = '<a id= "btnBorPro"  class=" btn btn-danger" onclick="eliminarProducto(' + pro + ')"><span class=" glyphicon glyphicon-trash"></span></a> ';


    }
    //eliminar fila de la tabla de productos
    eliminarProducto = function(index) { //now has global scope.
        //mostrar agregar
        document.getElementById('btnAgrPro').style.display = 'block';
        //Eliminar de los array globales
        var strid = String(index);
        var i = lis_pro_val.indexOf(strid);
        lis_pro_val.splice(i, 1);
        var b = lis_pro_val.indexOf(strid);
        lis_pro_nom.splice(b, 1);
        var c = lis_pro_val.indexOf(strid);
        lis_can.splice(c, 1);

        //Elimina la fila
        var parent = document.getElementById(index).parentNode;
        parent.removeChild(document.getElementById(index));
        //Calcula si hay fillas

        var nFilas = $("#tbl-pro tr").length;
        var nColumnas = $("#tbl-pro tr:last td").length;

        if (nFilas == 1) {
            var divTbl = document.getElementById('divTbl');
            divTbl.style.display = "none";
            document.getElementById('btnProds').style.display = 'none';

        }
    };

    //BOTON GUARDAR ajax
    var urlact = window.location;
    $("#btnProds").click(function() {


        if (ValidarStep1()) {
            if (ValidarStep2()) {
                $.ajax({
                    type: 'POST',
                    url: urlact,
                    data: {
                        'id_horno': id_horno,
                        'fecha_encendido': fecha_encendido,
                        'hora_encendido': hora_encendido,
                        'id_producto_tb': id_producto_tb,
                        'cantidad_verde_tb': cantidad_verde_tb,
                        CSRF: getCSRFTokenValue()
                    },
                });
            } else {
                document.getElementById("diverrP2").style.display = "block";
                document.getElementById("divmsjerrP2").innerHTML = "Al parecer te Falta un producto por Agregar. Los campos deben estar vacios.";
                return false
            }

        } else {
            document.getElementById("diverrP2").style.display = "block";
            document.getElementById("divmsjerrP2").innerHTML = "Por favor revisa el Paso 1 'Fecha y Horno'.";

            return false

        }
    });



    function ValidarStep2() {
        var sel_pro = document.getElementById("id_id_producto");
        var can_ver = document.getElementById("id_cantidad_verde");
        if (sel_pro.value == 0 && can_ver.value == "") {
            return true;
        } else {
            return false;
        }
    }

    $("#btnIncioQuema").click(function() {
        location.reload();
    });

    function validarFinalizar() {
        if (lis_pro_val.length > 0 && lis_can.length > 0) {
            //this array is not empty
            alert("lleno");

            return true;
        } else {
            alert("vacio");

            //this array is empty
            return false;
        }
    }

    //Initialize tooltips
    $('.nav-tabs > li a[title]').tooltip();

    //Wizard
    $('a[data-toggle="tab"]').on('show.bs.tab', function(e) {
        var $target = $(e.target);
        if ($target.parent().hasClass('disabled')) {
            return false;
        }
    });

    $(".next-step").click(function(e) {
        if (ValidarStep1()) {
            document.getElementById("diverrP1").style.display = "none";

            var $active = $('.wizard .nav-tabs li.active');
            $active.next().removeClass('disabled');
            nextTab($active);

        } else {
            document.getElementById("diverrP1").style.display = "block";
            document.getElementById("divmsjerrP1").innerHTML = "Por favor revisa que los campos no esten vacios.";

        }
    });

    function ValidarStep1() {
        var horno = document.getElementById("id_id_horno");
        var fecha = document.getElementById("id_fecha_encendido");
        var hora = document.getElementById("id_hora_encendido");

        if (horno.value == 0 || fecha.value == "" || hora.value == "") {

            return false;
        } else {
            return true;
        }
    }



    $(".prev-step").click(function(e) {

        var $active = $('.wizard .nav-tabs li.active');
        prevTab($active);

    });
});

function nextTab(elem) {


    $(elem).next().find('a[data-toggle="tab"]').click();
}

function prevTab(elem) {
    $(elem).prev().find('a[data-toggle="tab"]').click();
}
