<!--
# Sixto Jansa Sanz,
# Jorge Utrilla Olivera,
# y Jose Miguel Maldonado Del Pozo
# declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal.
# No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie.
# Declaramos además que no hemos realizado de manera deshonesta ninguna otra actividad
# que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
-->
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Latest compiled and minified CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
  <style>
    .table td, .table th {
        text-align: center;
    }
  </style>
</head>
<body>
    <div class='container'>
        <table class='table table-striped table-bordered table-hover'>
        <tr>
            %for title in table_titles:
            <th>{{title}}</th>
            %end
        </tr>
        %for row in rows:
        <tr>
            %for col in row:
                <td>{{col}}</td>
            %end
        </tr>
        %end
        </table>
        <h3>Número de resultados: {{len(rows)}}</h3>
    </div>
</body>
</html>