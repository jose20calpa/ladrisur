$(document).ready(function() {
  //TABLA DE HORNEROS

  //arreglo de IDS de Horneros seleccionados
  var rowIds = [];
  //contador pasos
  var conpas = 0;
  //ARRAYS DE Combustibles

  var lis_com_val = new Array;
  var lis_com_nom = new Array;
  var lis_can = new Array;

  //WIZZARD
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
    conpas++;
    if (conpas == 1) {
        if (ValidarStep1()) {
            document.getElementById("diverrP1").style.display = "none";
            var $active = $('.wizard .nav-tabs li.active');
            $active.next().removeClass('disabled');
            nextTab($active);
          }
          else {
            conpas--;
            document.getElementById("diverrP1").style.display = "block";
            document.getElementById("divmsjerrP1").innerHTML = "Por favor revisa que los campos no esten vacios y tengas al menos un hornero seleccionado. ";
          }
        }
    else if (conpas == 2) {
      if (ValidarStep2()) {
        document.getElementById("diverrP2").style.display = "none";
        var $active = $('.wizard .nav-tabs li.active');
        $active.next().removeClass('disabled');
        nextTab($active);
      }

      else {
        conpas--;
        document.getElementById("diverrP2").style.display = "block";
        document.getElementById("divmsjerrP2").innerHTML = "Los campos deben ser números enteros y no estar vacios.";
        return false
      }
    }
  });

  function ValidarStep1() {
    var fecha = document.getElementById("id_fecha_apagado");
    var hora = document.getElementById("id_hora_apagado");
    //se valida que los campos esten llenos y al menos un hornero seleccionado
    if (fecha.value == "" || hora.value == "" || rowIds.length == 0) {
      return false;
    }
    else {return true;}
  }

  function ValidarStep2() {
    ban = true;
    can_pro = document.getElementsByName("can_pro");
    for (var i = 0; i < can_pro.length; i++) {
      if (!can_pro[i].checkValidity()) {
          ban = false;
          break;
      }
    }
    return ban;
  }

  $(".prev-step").click(function(e) {
    //contador pasos
    conpas--;
    var $active = $('.wizard .nav-tabs li.active');
    prevTab($active);
  });

  //TABLA DE HORNEROS (SELECT)
  $("#grid-keep-selection").bootgrid({
    selection: true,
    multiSelect: true,
    rowSelect: true,
    keepSelection: true,
  }).on("selected.rs.jquery.bootgrid", function(e, rows) {
    for (var i = 0; i < rows.length; i++) {
      rowIds.push(rows[i].id);
    }
  }).on("deselected.rs.jquery.bootgrid", function(e, rows) {
    for (var i = 0; i < rows.length; i++) {
      rowIds.pop(rows[i].id);
    }
  });

  var frm = $('#frmHornero');
  var urlact = window.location;

  $("#btnHorn").click(function() {
    $.ajax({
      type: 'POST',
      url: urlact,
      data: {
        'select': select,
        CSRF: getCSRFTokenValue()
      }
    });
  });
  //FIN DE TABLA DE HORNEROS

  //COMBUSTIBLES
  //AGRAGA TABLA AUXILIAR DE COMBUSTIBLES USADOS
  $("#btn-agr-com").click(function() {
    var sel_com = document.getElementById('id_id_combustible');
    var com = document.getElementById('id_id_combustible').value;
    var can = document.getElementById('id_cantidad_combustible').value;

    if (com == "" || can == "") {
      document.getElementById("diverrP2").style.display = "block";
      document.getElementById("divmsjerrP2").innerHTML = "Por favor revisa que los campos no esten vacios.";
    }
    else {
      document.getElementById("diverrP2").style.display = "none";
      //mostrar Boton Finalizar
      document.getElementById('btn-fin').style.display = 'block';

      if (ValCombustiblesRep(com) && ValCantidadesInventario(com, can)) {
        //Nombre del Producto
        var nom_com = sel_com.options[sel_com.selectedIndex].text;
        //llenamos los arreglos
        lis_com_val.push(com);
        lis_com_nom.push(nom_com);
        lis_can.push(can);
        //Limpiamos msj de error anterior
        document.getElementById("diverrP3").style.display = "none";
        //limpiamos el formulario
        sel_com.value = "";
        document.getElementById('id_cantidad_combustible').value = '';
        mostrarTabla(com, nom_com, can);
      }
      else {
        if(!(ValCombustiblesRep(com))){
          document.getElementById("diverrP3").style.display = "block";
          document.getElementById("divmsjerrP3").innerHTML = "El Combustible ya ha sido usado en esta quema";
        }

        if(!(ValCantidadesInventario(com, can, canInv))){
          document.getElementById("diverrP3").style.display = "block";
          document.getElementById("divmsjerrP3").innerHTML = "La Cantidad de Combustible Supero a la Cantidad de Inventario o es Negativa";

        }
        //limpiamos el formulario
        sel_com.value = "";
        document.getElementById('id_cantidad_combustible').value = '';


      }
    }
  });

  function ValCombustiblesRep(combustible) {
    for (var i = 0; i < lis_com_val.length; i++) {
      if (lis_com_val[i] == combustible) {
        return false;
        break;
      }
    }
    return true;

  }

  function ValCantidadesInventario(combustible, can) {
    var combustible = document.getElementById('id_id_combustible').value;
    var idcominp = "can-"+ combustible;
    var canInv = document.getElementById(idcominp).value;
    canIng = parseFloat(can);
    invCom = parseFloat(canInv);



    if(canIng > invCom || can < 0){
      return false;
    }
    else{
      return true;
    }

  }

  function mostrarTabla(com, nom_com, can) {
    //añadir tabla
    var table = document.getElementById('tbl-com');
    var divTbl = document.getElementById('divTbl');
    divTbl.style.display = "block";
    var rowCount = table.rows.length;
    var row = table.insertRow(rowCount);
    row.id = com;
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    cell4.innerHTML = "<input type='hidden' name='id_combustible_tb' value=" + com + ">";
    cell1.innerHTML = "<input type='hidden' name='nombre_combustible_tb' value=" + nom_com + "><p>" + nom_com + "</p>";
    cell2.innerHTML = "<input type='hidden' name='cantidad_combustible_tb' value=" + can + "><p>" + can + "</p>";
    cell3.innerHTML = '<a id= "btnBorPro"  class=" btn btn-danger" onclick="eliminarCombustible(' + com + ')"><span class=" glyphicon glyphicon-trash"></span></a> ';
  }

  //eliminar fila de la tabla de productos
  eliminarCombustible = function(index) { //now has global scope.
    //mostrar agregar
    document.getElementById('btn-agr-com').style.display = 'block';
    //Eliminar de los array globales
    var strid = String(index);
    var i = lis_com_val.indexOf(strid);
    lis_com_val.splice(i, 1);
    var b = lis_com_val.indexOf(strid);
    lis_com_nom.splice(b, 1);
    var c = lis_com_val.indexOf(strid);
    lis_can.splice(c, 1);

    //Elimina la fila
    var parent = document.getElementById(index).parentNode;
    parent.removeChild(document.getElementById(index));
    //Calcula si hay fillas

    var nFilas = $("#tbl-com tr").length;
    var nColumnas = $("#tbl-com tr:last td").length;

    if (nFilas == 1) {
        var divTbl = document.getElementById('divTbl');
        divTbl.style.display = "none";
        document.getElementById('btn-fin').style.display = 'none';
    }
  };

  //FIN DE TABLA AUXILIAR DE COMBUSTIBLES USADOS
  //BOTON GUARDAR QUEMA FINALIZADA  AJAX
  var urlact = window.location;
  $("#btn-fin").click(function() {
    if (ValidarStep1()) {
      if (ValidarStep2()) {
        if(validarFinalizar()){
          $.ajax({
            type: 'POST',
            url: urlact,
            data: {
              'select': select,
              'fecha_apagado': fecha_apagado,
              'hora_apagado': hora_apagado,
              'can_pro': can_pro,
              'ids_pro': ids_pro,
              'id_combustible_tb': id_combustible_tb,
              'cantidad_combustible_tb': cantidad_combustible_tb,
              CSRF: getCSRFTokenValue()
            }
          });
        }
        else{
          document.getElementById("diverrP3").style.display = "block";
          document.getElementById("divmsjerrP3").innerHTML = "Al parecer te Falta un Combustible por Agregar. Los campos deben estar vacios.";
          return false
        }
      }
      else {
        document.getElementById("diverrP3").style.display = "block";
        document.getElementById("divmsjerrP3").innerHTML = "STEP 2: La cantidad de Productos deben ser números enteros y no estar vacios.";
        return false
      }
    }
    else {
      document.getElementById("diverrP3").style.display = "block";
      document.getElementById("divmsjerrP3").innerHTML = "Por favor revisa el Paso 1 'Fecha y Horno'.";
      return false
    }
  });

  $("#btnIncioQuema").click(function() {
      location.reload();
  });

  function validarFinalizar() {
    alert("validar");
    var sel_com = document.getElementById("id_id_combustible");
    var can_com = document.getElementById("id_cantidad_combustible");
    alert(sel_com);
    alert(can_com);    

    if (sel_com.value == 0 && can_com.value == "" ) {
      alert("true");
      return true;

    }
    else {
      alert("false");
      return false;
    }
  }


});

function nextTab(elem) {
  $(elem).next().find('a[data-toggle="tab"]').click();
}

function prevTab(elem) {
  $(elem).prev().find('a[data-toggle="tab"]').click();
}
