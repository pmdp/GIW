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
<nav class="navbar navbar-default">
  <div class="container">
    <div class="navbar-header">
      <a class="navbar-brand" href="/">El Concesionario</a>
    </div>
    <div id="navbar" class="">
      <ul class="nav navbar-nav">
        <li><a href="/">Home</a></li>
        <li><a href="/addCar">Añadir</a></li>
        <li><a href="/searchCar">Buscar</a></li>
        <form action='/searchCar' method='post' class="navbar-form navbar-right">
            <input type="text" class="form-control" name='texto' placeholder="Busca un coche...">
        </form>
      </ul>
      <ul class="nav navbar-nav navbar-right">
            <li><a href="/logout">Logout</a></li>
      </ul>
    </div><!--/.nav-collapse -->
  </div>
</nav>
<div class='container'>