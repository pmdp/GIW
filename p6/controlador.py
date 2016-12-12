#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import run, request, static_file, get, post, error, response, template, redirect, FileUpload
import os, sqlite3

################################################################################################################

#Por defecto, todas las peticiones van aquí
@get('/')
def enrutador():
    usuario = request.get_cookie("session", secret='claveSecreta')
    # Si el usuario está logueado
    if usuario:
        #parte restringida
        data = getCoches()
        out = getHeader() + template('dash', rows=data, title='Todos los coches del concesionario') + getFooter()
        return out
    else:
        #Si no está logeado, carga el login
        return template('login', msgOK='', msgFail='')

################################################################################################################

@post('/login')
def do_login():
    usuario = request.forms.get('usuario')
    passwd = request.forms.get('password')
    if check_login(usuario, passwd):
        #Si el login es correcto carga la cookie y vuelve a cargar la página (esta vez entrará en el dashboard)
        response.set_cookie("session", usuario, secret='claveSecreta', httponly=True)
        redirect('/')
    else:
        #Si no es correcto, vuelve a cargar el login con el mensaje de error
        return template('login', msgOK='', msgFail='Login incorrecto')

def check_login(usuario, passwd):
    db = conexionBD()
    c = db.cursor()
    c.execute('SELECT * FROM Usuarios WHERE usuario = ?', (usuario,))
    user = c.fetchone()
    db.close()
    if user and user[5] == passwd:
        return True
    else:
        return False

@get('/logout')
def do_logout():
    response.delete_cookie("session")
    redirect('/')

################################################################################################################

@get('/register')
def show_register():
    return template('register', msgOK='', msgFail='')

@post('/register')
def do_register():
    nombre = request.forms.get('nombre')
    apellidos = request.forms.get('apellidos')
    email = request.forms.get('email')
    usuario = request.forms.get('usuario')
    passwd = request.forms.get('passwd')

    #Comprueba que se hayan metido todos los datos
    if nombre and apellidos and email and usuario and passwd:
        user = (nombre, apellidos, email, usuario, passwd)
        db = conexionBD()
        c = db.cursor()
        #Mira a ver si ya hay un usuario registrado con ese nombre
        c.execute('SELECT * FROM Usuarios WHERE usuario = ?', (usuario,))
        if len(c.fetchall()) > 0:
            out = template('register', msgOK='', msgFail='Error de registro: Ya hay un usuario con ese nombre')
        else:
            #Si no lo hay, inserta el nuevo usuario
            c.execute('INSERT INTO Usuarios (nombre, apellidos, email, usuario, passwd) VALUES (?,?,?,?,?)', user)
            print ("Usuario registrado:", user)
            out = template('login', msgOK='Usuario registrado correctamente', msgFail='')
        db.commit()
        db.close()
    else:
        out = template('register', msgOK='', msgFail='Faltan datos (todos los campos son obligatorios)')
    return out

################################################################################################################
#Página de vista de un coche en concreto
@get('/viewCar')
def viewCar():
    id = request.query.id
    coche = getCocheById(id)
    out = getHeader() + template('viewCar', data=coche) + getFooter()
    return out

#Página de edición de un coche
@get('/editCar')
def editCar():
    id = request.query.id
    coche = getCocheById(id)
    out = getHeader() + template('editCar', data=coche) + getFooter()
    return out

@get('/addCar')
def addCar():
    return getHeader() + template('addCar', msg='') + getFooter()

@post('/addCar')
def addCarPost():
    # Coge los valores del formulario
    marca = request.forms.get('marca')
    modelo = request.forms.get('modelo')
    anyo = request.forms.get('anyo')
    caballos = request.forms.get('caballos')
    cilindrada = request.forms.get('cilindrada')
    combustible = request.forms.get('combustible')
    consumo = request.forms.get('consumo')
    descripcion = request.forms.get('descripcion')
    foto = request.files.get('foto')
    if marca and modelo and anyo and caballos and cilindrada and combustible and consumo and descripcion and foto:
        name, ext = os.path.splitext(foto.filename)
        if ext not in ('.png',):
            return getHeader() + template('addCar', msg='Extensión de archivo no permitida') + getFooter()
        foto.save(os.getcwd() + os.sep + 'images')

        db = conexionBD()
        c = db.cursor()
        data = (marca, modelo, anyo, caballos, cilindrada, combustible, consumo, descripcion, foto.filename)
        c.execute('''INSERT INTO Coches (marca, modelo, anyo, caballos,
                    cilindrada, combustible, consumo, descripcion, foto)
                    VALUES (?,?,?,?,?,?,?,?,?)''', data)
        db.commit()
        db.close()
        data = getCoches()
        return getHeader() + template('dash', rows=data, title="Todos los coches del concesionario") + getFooter()
    else:
        return getHeader() + template('addCar', msg='Faltan campos (todos son obligatorios)') + getFooter()

@post('/editCarVal')
def editCarPost():
    #Coge los valores del formulario
    marca = request.forms.get('marca')
    modelo = request.forms.get('modelo')
    anyo = request.forms.get('anyo')
    caballos = request.forms.get('caballos')
    cilindrada = request.forms.get('cilindrada')
    combustible = request.forms.get('combustible')
    consumo = request.forms.get('consumo')
    descripcion = request.forms.get('descripcion')

    #Coge el id del coche a modificar
    id = request.query.id

    data = (marca, modelo, anyo, caballos, cilindrada, combustible, consumo, descripcion, id)
    db = conexionBD()
    c = db.cursor()
    c.execute('''UPDATE Coches SET marca = ?, modelo = ?, anyo = ?,
              caballos = ?, cilindrada = ?, combustible = ?, consumo = ?, descripcion = ?
              WHERE id = ?''', data)
    db.commit()
    db.close()

    #Redirige de nuevo a la página de edición
    redirect('/editCar?id='+id)

@post('/deleteCar')
def deleteCar():
    # Coge el id del coche a eliminar
    id = request.query.id
    db = conexionBD()
    c = db.cursor()
    c.execute('DELETE FROM Coches WHERE id = ?', (id,))
    db.commit()
    db.close()
    data = getCoches()


@post('/searchCar')
def searchCarPost():
    texto = request.forms.get('texto')
    db = conexionBD()
    c = db.cursor()
    consulta = "SELECT id, marca, modelo, anyo, caballos, cilindrada, combustible, consumo FROM Coches WHERE "
    consulta += "(marca LIKE '%" + texto + "%')"
    consulta += ' OR '
    consulta += "(modelo LIKE '%" + texto + "%')"
    consulta += ' OR '
    consulta += "(anyo LIKE '%" + texto + "%')"
    consulta += ' OR '
    consulta += "(combustible LIKE '%" + texto + "%')"
    c.execute(consulta)
    data = c.fetchall()
    if len(data) > 0:
        return getHeader() + template('dash', rows=data, title='Resultados de ' + texto) + getFooter()
    else:
        return getHeader() + template('dash', rows=data, title='No hay resultados con ' + texto) + getFooter()
################################################################################################################
#Imagenes estáticas
@get('/images/<file:re:.*\.png>')
def serve_image(file):
    return static_file(file, root=os.getcwd() + os.sep + 'images', mimetype='image/png')


################################################################################################################

def conexionBD():
    db = sqlite3.connect('concesionario.sqlite3')
    db.text_factory = str
    return db

################################################################################################################

def getCoches():
    db = conexionBD()
    c = db.cursor()
    c.execute('SELECT id, marca, modelo, anyo, caballos, cilindrada, combustible, consumo FROM Coches')
    data = c.fetchall()
    db.close()
    return data

def getCocheById(id):
    db = conexionBD()
    c = db.cursor()
    c.execute("SELECT * FROM Coches WHERE id = ?", (id,))
    return c.fetchone()

def insertCoche(data):
    db = conexionBD()
    db.execute('''INSERT INTO Coches (marca, modelo, anyo, caballos,
                cilindrada, combustible, consumo, descripcion, foto)
                VALUES (?,?,?,?,?,?,?,?,?)''')
    db.commit()
    db.close()


#Si se accede a una ruta no existente
@error(404)
def error404 (error):
    return "Nada por aquí..."

def getHeader():
    return template('header', title="El concesionario")

def getFooter():
    return template('footer')

run(host='localhost', port=8080)