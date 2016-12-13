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
  <title>{{title}}</title>
  <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
</head>
<body>
    <div class='container'>
        <h3>{{title}}</h3>
        <ul>
            %for d in simple_data:
                <li>{{d}}</li>
            %end
            <li>Credit card:</li>
            <ul>
                %for c in credit_card:
                    <li>{{c}}</li>
                %end
            </ul>
            <li>Address:</li>
            <ul>
                %for a in address:
                    <li>{{a}}</li>
                %end
            </ul>
            <li>Likes:</li>
            <ul>
                %for l in likes:
                    <li>{{l}}</li>
                %end
            </ul>
        </ul>
    </div>
</body>
</html>