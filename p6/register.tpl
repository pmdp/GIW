<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <title>Login</title>
  <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Latest compiled and minified CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
</head>
<body>
<div class="container" style="margin-top:20%">
<div class="col-md-4 col-md-offset-4">
<div class="login-panel panel panel-default">
                    <div class="panel-heading">
                        <h3 class="panel-title">Registro</h3>
                    </div>
                    <div class="panel-body">
                        <form action='/register' method="post" role="form">
                            <fieldset>
			    <div class="control-group">
			      <!-- Nombre -->
			      <label class="control-label"  for="nombre">Nombre</label>
			      <div class="controls">
			        <input type="text" id="nombre" name="nombre" placeholder="" class="input-xlarge">
			      </div>
			    </div>
			    <div class="control-group">
			      <!-- Username -->
			      <label class="control-label"  for="apellidos">Apellidos</label>
			      <div class="controls">
			        <input type="text" id="apellidos" name="apellidos" placeholder="" class="input-xlarge">
			      </div>
			    </div>
			    <div class="control-group">
			      <!-- Username -->
			      <label class="control-label"  for="email">Email</label>
			      <div class="controls">
			        <input type="text" id="email" name="email" placeholder="" class="input-xlarge">
			      </div>
			    </div>
			    <div class="control-group">
			      <!-- Username -->
			      <label class="control-label"  for="email">Usuario (para login)</label>
			      <div class="controls">
			        <input type="text" id="usuario" name="usuario" placeholder="" class="input-xlarge">
			      </div>
			    </div>
			    <div class="control-group">
			      <!-- Password-->
			      <label class="control-label" for="password">Password</label>
			      <div class="controls">
			        <input type="password" id="passwd" name="passwd" placeholder="" class="input-xlarge">
			      </div>
			    </div>
			    <p style="color:red">{{msgFail}}</p>
                <p style="color:green">{{msgOK}}</p>
			    <div class="control-group">
			      <!-- Button -->
			      <div class="controls">
			        <button class="btn btn-success" type='submit'>Registrar</button>
			      </div>
			    </div>
			  </fieldset>
                        </form>
                    </div>
                </div>
</div>
</div>