<div class="row">
<div class="col-md-6 col-md-offset-3">
<div class="panel panel-success">
    <div class="panel-heading">
        <h3 class="panel-title text-center">{{data[1]}} {{data[2]}}</h3>
    </div>
    <div class="panel-body">
        <img src="/images/{{data[9]}}" class="img-responsive" alt="{{data[9]}}">

        <form action='/editCarVal?id={{data[0]}}' method='post' id='carForm' class="form-horizontal">
          <div class="form-group">
            <label for="inputMarca" class="col-md-2 col-md-offset-3 control-label">Marca</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputMarca" name="marca" value="{{data[1]}}">
            </div>
          </div>
          <div class="form-group">
            <label for="inputModelo" class="col-md-2 col-md-offset-3 control-label">Modelo</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputModelo" name="modelo" value="{{data[2]}}">
            </div>
          </div>
          <div class="form-group">
            <label for="inputAnyo" class="col-md-2 col-md-offset-3 control-label">Año</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputAnyo" name="anyo" value="{{data[3]}}">
            </div>
          </div>
          <div class="form-group">
            <label for="inputCaballos" class="col-md-2 col-md-offset-3 control-label">Caballos</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputCaballos" name="caballos" value="{{data[4]}}">
            </div>
          </div>
          <div class="form-group">
            <label for="inputCilindrada" class="col-md-2 col-md-offset-3 control-label">Cilindrada</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputCilindrada" name="cilindrada" value="{{data[5]}}">
            </div>
          </div>
          <div class="form-group">
            <label for="inputCombustible" class="col-md-2 col-md-offset-3 control-label">Combustible</label>
            <div class="col-md-4">
              <select id="inputCombustible" name="combustible" class="form-control">
                  %if data[6] == 'Gasolina':
                    <option>Gasolina</option>
                    <option>Diesel</option>
                    <option>Eléctrico</option>
                  %elif data[6] == 'Diesel':
                    <option>Diesel</option>
                    <option>Gasolina</option>
                    <option>Eléctrico</option>
                  %elif data[6] == 'Eléctrico':
                    <option>Eléctrico</option>
                    <option>Gasolina</option>
                    <option>Diesel</option>
                  %end
              </select>
            </div>
           </div>
          <div class="form-group">
            <label for="inputConsumo" class="col-md-2 col-md-offset-3 control-label">Consumo</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputConsumo" name="consumo" value="{{data[7]}}">
            </div>
          </div>
          <div class="form-group">
            <label for="inputDescripcion" class="col-md-2 control-label">Descripción</label>
            <div class="col-md-12">
                <textarea id="inputDescripcion" class="form-control" name="descripcion" rows="4">{{data[8]}}</textarea>
            </div>
          </div>
        </form>
    </div>

    <div class="panel-footer text-center">
        <script>
            function submitForm() {
                document.getElementById("carForm").submit();
            }
        </script>
        <button type="submit" onclick='submitForm()' class="btn btn-success">Guardar</button>
    </div>
</div>
</div>
</div>