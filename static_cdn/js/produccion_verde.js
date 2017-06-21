$(document).ready(function() {

  //ARRAYS DE productos
  var lis_pro_val = new Array;
  var lis_pro_nom = new Array;
  var lis_can = new Array;
  //contador pasos
  var conagr = 0;

  //tabla
  $("#btn-agr").click(function() {
    conagr++;

    var sel_pro = document.getElementById('id_id_producto');
    var pro = document.getElementById('id_id_producto').value;
    var can = document.getElementById('id_cantidad_producto').value;
    if (pro == "" || can == "") {
      document.getElementById("diverrP2").style.display = "block";
      document.getElementById("divmsjerrP2").innerHTML = "Por favor revisa que los campos no esten vacios.";
      conagr--;
    }
    else {
      document.getElementById("diverrP2").style.display = "none";

      //mostrar Boton Finalizar

      document.getElementById('btn-fin').style.display = 'block';
      if(ValProductosRep(pro)){
        //Nombre del Producto
        var nom_pro = sel_pro.options[sel_pro.selectedIndex].text;
        //llenamos los arreglos
        lis_pro_val.push(pro);
        lis_pro_nom.push(nom_pro);
        lis_can.push(can);
        //limpiamos el formulario
        sel_pro.value = "";
        document.getElementById('id_cantidad_producto').value = '';

        // lis_pro_val.forEach(function(item, index, array) {
        //     console.log(item, index);
        // });
        mostrarTabla(pro, nom_pro, can);

      }
      else{
        console.log(lis_pro_val)
        conagr--;
        document.getElementById("diverrP2").style.display = "block";
        document.getElementById("divmsjerrP2").innerHTML = "El producto ya ha sido guardado";
        sel_pro.value = "";
        document.getElementById('id_cantidad_producto').value = '';
      }
      if(conagr==2){
        document.getElementById('btn-agr').style.display = 'none';
      }



    }
  });
  function ValProductosRep(producto){
    for( var i=0; i < lis_pro_val.length; i++ ){
      if( lis_pro_val[i] == producto) {
        return false;
        break;
      }
    }
      return true;
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
    cell4.innerHTML = "<input type='hidden'  name='id_producto_tb' value=" + pro + ">";
    cell1.innerHTML = "<input type='hidden' name='nom_pro_tb' value=" + nom_pro + "><p>" + nom_pro + "</p>";
    cell2.innerHTML = "<input type='hidden' name='cantidad_verde_tb' value=" + can + "><p>" + can + "</p>";
    cell3.innerHTML = '<a id= "btnBorPro"  class=" btn btn-danger" onclick="eliminarProducto(' + pro + ')"><span class=" glyphicon glyphicon-trash"></span></a> ';


  }

  eliminarProducto = function(index) { //now has global scope.
    if (conagr == 1){
      conagr--;
    }
    //mostrar agregar
    document.getElementById('btn-agr').style.display = 'block';
    //Eliminar de los array globales
    var strid = String(index);
    var i = lis_pro_val.indexOf(strid);
    lis_pro_val.splice( i, 1);
    var b = lis_pro_nom.indexOf(strid);
    lis_pro_nom.splice( b, 1);
    var c = lis_can.indexOf(strid);
    lis_can.splice( c, 1);

    //Elimina la fila
    var parent = document.getElementById(index).parentNode;
    parent.removeChild(document.getElementById(index));
    //Calcula si hay fillas

    var nFilas = $("#tbl-pro tr").length;
    var nColumnas = $("#tbl-pro tr:last td").length;
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
            'id_producto_tb': id_producto_tb,
            'cantidad_verde_tb': cantidad_verde_tb,
            CSRF: getCSRFTokenValue()
          },
        });

    }
    else {
      document.getElementById("diverrP2").style.display = "block";
      document.getElementById("divmsjerrP2").innerHTML = "Al parecer te Falta un producto por Agregar. Los campos deben estar vacios.";

      return false

    }});


    function ValidarStep1() {
      var pro = document.getElementById('id_id_producto').value;
      var can = document.getElementById('id_cantidad_producto').value;
      if (pro == "" || can == "") {
        return true;
      }
      return false
    }




});
