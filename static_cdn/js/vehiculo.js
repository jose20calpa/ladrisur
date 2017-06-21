$(document).ready(function() {
    $("#submit-id-guardar").click(function() {
      alert("asdf");
      var cad = document.getElementById("id_placa").value;
      var expreg = /^[A-Za-z]{3}-\d{3}$/;
      if (!expreg.test(cad)) {
        document.getElementById("diverr").innerHTML = "<strong>Error!</strong> La matrícula  " + cad + " NO es correcta ten en cuenta el Guion Ej. ABC-123";
        document.getElementById("diverr").style.display = 'block';
        document.getElementById("btnGuarMaq").disabled = true;
        return false;
      } else {
        document.getElementById("diverr").style.display = 'none';
        document.getElementById("btnGuarMaq").disabled = false;
        return true;

      }

    });

});
