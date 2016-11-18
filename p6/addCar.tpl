<div class="row">
<div class="col-md-6 col-md-offset-3">
<div class="panel panel-success">
    <div class="panel-heading">
        <h3 class="panel-title text-center">Nuevo coche</h3>
    </div>
    <div class="panel-body">

        <form action='/addCar' method='post' id='carForm' class="form-horizontal" enctype="multipart/form-data">
           <div class="form-group">
            <label for="inputFoto" class="col-md-2 col-md-offset-3 control-label">Foto</label>
            <div class="col-md-4">
              <input type="file" id="inputFoto" name='foto'>
            </div>
          </div>
          <div class="form-group">
            <label for="inputMarca" class="col-md-2 col-md-offset-3 control-label">Marca</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputMarca" name="marca">
            </div>
          </div>
          <div class="form-group">
            <label for="inputModelo" class="col-md-2 col-md-offset-3 control-label">Modelo</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputModelo" name="modelo">
            </div>
          </div>
          <div class="form-group">
            <label for="inputAnyo" class="col-md-2 col-md-offset-3 control-label">Año</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputAnyo" name="anyo">
            </div>
          </div>
          <div class="form-group">
            <label for="inputCaballos" class="col-md-2 col-md-offset-3 control-label">Caballos</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputCaballos" name="caballos">
            </div>
          </div>
          <div class="form-group">
            <label for="inputCilindrada" class="col-md-2 col-md-offset-3 control-label">Cilindrada</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputCilindrada" name="cilindrada">
            </div>
          </div>
          <div class="form-group">
            <label for="inputCombustible" class="col-md-2 col-md-offset-3 control-label">Combustible</label>
            <div class="col-md-4">
              <select id="inputCombustible" name="combustible" class="form-control">
                    <option>Gasolina</option>
                    <option>Diesel</option>
                    <option>Eléctrico</option>
              </select>
            </div>
           </div>
          <div class="form-group">
            <label for="inputConsumo" class="col-md-2 col-md-offset-3 control-label">Consumo</label>
            <div class="col-md-4">
              <input type="text" class="form-control" id="inputConsumo" name="consumo">
            </div>
          </div>
          <div class="form-group">
            <label for="inputDescripcion" class="col-md-2 control-label">Descripción</label>
            <div class="col-md-12">
                <textarea id="inputDescripcion" class="form-control" name="descripcion" rows="4"></textarea>
            </div>
          </div>
        </form>
        <p style='color:red'>{{msg}}</p>
    </div>

    <div class="panel-footer text-center">
        <script>
            function submitForm() {
                document.getElementById("carForm").submit();
            }
        </script>
        <button type="submit" onclick='submitForm()' class="btn btn-success">Añadir</button>
    </div>
</div>
</div>
</div>