$(document).ready(function() {

    var grid = $("#grid-basic").bootgrid({
         formatters: {
           "commands": function(column, row)
           {
             return "<center>" +
                    "<button  onclick=\"document.getElementById('delete').style.display='block'\" class=\"btn btn-xs btn-danger command-delete\" data-row-id=\"" + row.id + "\"><span class=\"glyphicon glyphicon-trash\"></span></button> " +
                    "<button  class=\"btn btn-xs btn-warning command-edit\" data-row-id=\"" + row.id + "\"><span class=\"glyphicon glyphicon-edit\"></span></button>" +
                    "</center>";
           }
         }}).on("loaded.rs.jquery.bootgrid", function() {
        /* Executes after data is loaded and rendered */
        grid.find(".command-edit").on("click", function(e) {
            var idproducto = $(this).data("row-id");
            var url = "{% url 'administrador:mod-prod' 0 %}".replace(0, idproducto);
            location.href = url;
        }).end().find(".command-delete").on("click", function(e) {
          var idproducto = $(this).data("row-id");
          var url = "{% url 'administrador:elm-prod' 0 %}".replace(0, idproducto);
          location.href = url;
        });
    });
  });
