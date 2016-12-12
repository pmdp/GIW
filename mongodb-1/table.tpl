<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <title>{{title}}</title>
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
        <h3>{{title}}</h3>
        <table class='table table-striped table-bordered table-hover'>
        <tr>
            <th>Nombre de usuario</th>
            <th>e-mail</th>
            <th>Página web</th>
            <th>Tarjeta de crédito</th>
            <th>Hash de contraseña</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Dirección</th>
            <th>Aficiones</th>
            <th>Fecha de nacimiento</th>
        </tr>
        %for row in rows:
        <tr>
        %for col in row:
            <td>{{col}}</td>
        %end
        </tr>
    %end
        </table>
    </div>
</body>
</html>