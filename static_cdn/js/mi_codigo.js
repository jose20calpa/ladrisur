$(document).ready(function() {  

    $("select[name=tipo]").change(function() {
        if ($('select[name=tipo]').val() == 'Retroexcavadora' ||
            $('select[name=tipo]').val() == 'Cargador') {
            document.getElementById("diverr").style.display = 'none';
            document.getElementById("id_placa").value = "No Registra";
            document.getElementById("id_placa").disabled = true;
            document.getElementById("btnGuarMaq").disabled = false;
        } else {
            document.getElementById("id_placa").value = "";
            document.getElementById("id_placa").disabled = false;
        }
    });



    $("input[name=placa]").change(function() {
        var cad = document.getElementById("id_placa").value;
        var expreg = /^[A-Za-z]{3}-\d{3}$/;
        if (!expreg.test(cad)) {
            document.getElementById("diverr").innerHTML = "<strong>Error!</strong> La matrícula  " + cad + " NO es correcta ten en cuenta el Guion Ej. ABC-123";
            document.getElementById("diverr").style.display = 'block';
            document.getElementById("btnGuarMaq").disabled = true;
        } else {
            document.getElementById("diverr").style.display = 'none';
            document.getElementById("btnGuarMaq").disabled = false;
        }
    });
});
