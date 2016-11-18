<div class="row">
<div class="col-md-6 col-md-offset-3">
<div class="panel panel-success">
    <div class="panel-heading">
        <h3 class="panel-title text-center">{{data[1]}} {{data[2]}}</h3>
    </div>
    <div class="panel-body">
        <img src="/images/{{data[9]}}" class="img-responsive" alt="{{data[9]}}">
        <ul class="list-group">
            <li class="list-group-item">
                <span class="badge">{{data[3]}}</span>
                Año
            </li>
            <li class="list-group-item">
                <span class="badge">{{data[4]}} cv</span>
                Caballos
            </li>
            <li class="list-group-item">
                <span class="badge">{{data[5]}} cc</span>
                Cilindrada
            </li>
            <li class="list-group-item">
                <span class="badge">{{data[6]}}</span>
                Combustible
            </li>
            <li class="list-group-item">
                <span class="badge">{{data[7]}} l/100km</span>
                Consumo
            </li>
        </ul>
        <div class="panel panel-default">
            <div class="panel-heading">Descripción</div>
            <div class="panel-body">
                <p>{{data[8]}}</p>
            </div>
        </div>

    </div>
    <div class="panel-footer text-center">
        <a href="/editCar?id={{data[0]}}" class="btn btn-primary active" role="button">Modificar</a>
        <button onclick="modalDelete()" class="btn btn-danger active">Eliminar</button>
        <script>
            function modalDelete() {
                if (confirm("Seguro que desea eliminar?") == true) {
                    var xmlHttp = new XMLHttpRequest();
                    xmlHttp.open( "POST", "/deleteCar?id={{data[0]}}", false ); // false for synchronous request
                    xmlHttp.send( null );
                    window.location = "/";
                }
            }
</script>
    </div>
</div>
</div>
</div>