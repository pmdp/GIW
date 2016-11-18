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
                        <h3 class="panel-title">Log In</h3>
                    </div>
                    <div class="panel-body">
                        <form action='/login' method="post" role="form">
                            <fieldset>
                                <div class="form-group">
                                    <input class="form-control" placeholder="Usuario" name="usuario" type="text" autofocus="">
                                </div>
                                <div class="form-group">
                                    <input class="form-control" placeholder="Password" name="password" type="password" value="">
                                </div>
                                <p style="color:red">{{msgFail}}</p>
                                <p style="color:green">{{msgOK}}</p>
                                <button class="btn btn-success" type='submit'>Login</button>
                                <a class="btn btn-info col-md-offset-6" href="/register">Register</a>
                            </fieldset>
                        </form>
                    </div>
                </div>
</div>
</div>
</div>
</body>
</html>