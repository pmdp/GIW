<h3>{{title}}</h3>
<table class='table table-striped table-bordered table-hover'>
    <tr>
        <th>Id</th>
        <th>Marca</th>
        <th>Modelo</th>
        <th>Año</th>
        <th>Caballos</th>
        <th>Cilindrada</th>
        <th>Combustible</th>
        <th>Consumo</th>
        <th>Acción</th>
    </tr>
    %for row in rows:
        <tr>
        %for col in row:
            <td>{{col}}</td>
        %end
        %id = row[0]
        <td><a class='btn btn-success active' href='/viewCar?id={{id}}'>Ver</a></td>
        %end
        </tr>
    %end
</table>
