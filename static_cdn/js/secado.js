$(document).ready(function() {

  //ARRAYS DE combustibles
  var lis_com_val = new Array;
  var lis_com_nom = new Array;
  var lis_can = new Array;
  //contador pasos
  var conagr = 0;

  //tabla
  $("#btn-agr").click(function() {

    var opc_sel_sec = document.getElementById('id_id_secadero').options[document.getElementById('id_id_secadero').selectedIndex].text;

    var sel_com = document.getElementById('id_id_combustible');
    var com = document.getElementById('id_id_combustible').value;
    var can = document.getElementById('id_cantidad_combustible').value;
    if (com == "" || can == "") {
      document.getElementById("diverrP2").style.display = "block";
      document.getElementById("divmsjerrP2").innerHTML = "Por favor revisa que los campos no esten vacios.";
      conagr--;
    }
    else {
      document.getElementById("diverrP2").style.display = "none";

      //mostrar Boton Finalizar

      document.getElementById('btn-fin').style.display = 'block';
      if(ValCombustiblesRep(com)){
        //Nombre del Combustible
        var nom_com = sel_com.options[sel_com.selectedIndex].text;
        //llenamos los arreglos
        lis_com_val.push(com);
        lis_com_nom.push(nom_com);
        lis_can.push(can);
        //limpiamos el formulario
        sel_com.value = "";
        document.getElementById('id_cantidad_combustible').value = '';

        // lis_com_val.forEach(function(item, index, array) {
        //     console.log(item, index);
        // });
        conagr++;
        document.getElementById('hnameTab').innerHTML = "Tabla de Consumos del " + opc_sel_sec;

        mostrarTabla(com, nom_com, can);

      }
      else{
        document.getElementById("diverrP2").style.display = "block";
        document.getElementById("divmsjerrP2").innerHTML = "El Combustible ya ha sido guardado";
        sel_com.value = "";
        document.getElementById('id_cantidad_combustible').value = '';
      }
    }
  });
  function ValCombustiblesRep(combustible){
    for( var i=0; i < lis_com_val.length; i++ ){
      if( lis_com_val[i] == combustible) {
        return false;
        break;
      }
    }
      return true;
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
    cell4.innerHTML = "<input type='hidden'  name='id_combustible_tb' value=" + com + ">";
    cell1.innerHTML = "<input type='hidden' name='nom_pro_tb' value=" + nom_com + "><p>" + nom_com + "</p>";
    cell2.innerHTML = "<input type='hidden' name='cantidad_combustible_tb' value=" + can + "><p>" + can + "</p>";
    cell3.innerHTML = '<a id= "btnBorPro"  class=" btn btn-danger" onclick="eliminarCombustible(' + com + ')"><span class=" glyphicon glyphicon-trash"></span></a> ';


  }

  eliminarCombustible = function(index) { //now has global scope.
    if (conagr == 1){
      conagr--;
    }
    //mostrar agregar
    document.getElementById('btn-agr').style.display = 'block';
    //Eliminar de los array globales
    var strid = String(index);
    var i = lis_com_val.indexOf(strid);
    lis_com_val.splice( i, 1);
    var b = lis_com_nom.indexOf(strid);
    lis_com_nom.splice( b, 1);
    var c = lis_can.indexOf(strid);
    lis_can.splice( c, 1);

    //Elimina la fila
    var parent = document.getElementById(index).parentNode;
    parent.removeChild(document.getElementById(index));
    //Calcula si hay fillas

    var nFilas = $("#tbl-com tr").length;
    var nColumnas = $("#tbl-com tr:last td").length;
    if (nFilas == 1) {
      document.getElementById('btn-fin').style.display = 'none';
        var divTbl = document.getElementById('divTbl');
        divTbl.style.display = "none";
    }
    };

  //BOTON GUARDAR ajax
  var urlact = window.location;
  $("#btn-fin").click(function() {

    if (ValidarStep1()) {
        $.ajax({
          type: 'POST',
          url: urlact,
          data: {
            'id_combustible_tb': id_combustible_tb,
            'cantidad_combustible_tb': cantidad_combustible_tb,
            CSRF: getCSRFTokenValue()
          },
        });

    }
    else {
      document.getElementById("diverrP2").style.display = "block";
      document.getElementById("divmsjerrP2").innerHTML = "Al parecer te Falta un combustible por Agregar. Los campos deben estar vacios.";

      return false

    }});


    function ValidarStep1() {
      var com = document.getElementById('id_id_combustible').value;
      var can = document.getElementById('id_cantidad_combustible').value;
      if (com == "" || can == "") {
        return true;
      }
      return false
    }




});
