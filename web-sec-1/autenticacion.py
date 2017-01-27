# -*- coding: utf-8 -*-

# Sixto Jansa Sanz,
# Jorge Utrilla Olivera,
# y Jose Miguel Maldonado Del Pozo
# declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal.
# No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie.
# Declaramos además que no hemos realizado de manera deshonesta ninguna otra actividad
# que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.


from bottle import run, post, request
from pymongo import MongoClient, errors
from passlib.hash import argon2  # necesita el backend: argon2-cffi
import onetimepass as otp
import random
import string
from urllib.parse import quote

mongoclient = MongoClient()
db = mongoclient.giw
c = db.users

##############
# APARTADO 1 #
##############
# Después de investigar sobre hasheo de contraseñas hemos elegido Argon2 (https://password-hashing.net/argon2-specs.pdf)
# debido a lo siguiente:
# VENTAJAS y Características:
# - Muy resistente a fuerza bruta realizada con hardware especifico o idóneo para crackear hashes como FPGAs, GPUs, ASIC
# - Dicha resistencia se consigue aumentando la memoria necesaria para calcular el hash,
#       por lo que hace mucho más caro el hardware para crackear en tiempo considerable
# - Diseñado específicamente para hashear contraseñas
# - Generación de hash en un solo sentido, del hash no se puede sacar la clave (al menos sin fuerza bruta)
# - Ganador de la competición de hasheo de contraseñas: https://password-hashing.net
# - Aconsejado por muchos expertos criptograficos en diversos blogs y foros
# - La librería usada (passlib https://passlib.readthedocs.io/en/stable/lib/passlib.hash.argon2.html),
#       permite el uso de Argon2
# - Dicha librería añade la sal aleatoria automáticamente al string resultante,
#       para así evitar hashes iguales para las mismas contraseñas y su correspondiente ataque con rainbow tables
# - También añade el algoritmo usado, la versión, la memoria usada, las iteraciones y la paralelización
# - Al realizar iteraciones se complica proporcionalmente el crackeo del hash
# - Permite ajustar el número de iteraciones para así encontrar el equilibrio entre seguridad y velocidad
# - Diseñado para la arquitectura x86
# - Los parametros configurables son:
#       - Número de iteraciones (t), afecta al coste de tiempo.
#       - Tamaño de la memoria usada (m), afecta al coste de memoria,
#       - Número de hilos (h), afecta al grado de paralelismo.
#
# DESVENTAJAS
# - Al ser un algoritmo relativamente nuevo, no tiene tantos años de pruebas detrás como bcrypt, scrypt o PBKDF2
# - Hambriento de memoria, pudiendo ocupar 1GB de RAM en menos de 1/4 de segundo


########################################################################################################################

# Función que recibe una lista de campos que deberían llegar al servidor por POST
# Valida que lo que ha llegado al servidor es correcto, justo y necesario (campos no requeridos, inexistentes o vacios)
# Devuelve:
#   Booleano : indica si ha cumplido todas las validaciones
#   diccionario (data): con los datos recibidos
#   mensaje: indicando el origen del fallo
def form_data(required_fields):
    data = dict()
    # Si todos las claves del diccionario llegado por POST están en la lista de campos requeridos
    if all(k in request.forms.keys() for k in required_fields):
        # Recorre el diccionario de datos del formulario
        for k, v in request.forms.items():
            # Comprueba que sea un campo válido
            if k in required_fields:
                # Comprueba que ese campo no esté vacio
                if v != '':
                    data[k] = v
                else:
                    return False, data, 'Falta algo por rellenar...'
            else:
                return False, data, u'Hay campos no válidos'
        return True, data, 'OK'
    else:
        return False, data, 'Faltan datos'

########################################################################################################################


# Método que abstrae el proceso de registro para poder usarlo sin y con TOTP
def sign_up(totp=False):
    valid, data, msg = form_data(['nickname', 'name', 'country', 'email', 'password', 'password2'])
    if valid:
        # Cambia la clave nickname a _id para luego insertar el diccionario
        data['_id'] = data['nickname']
        del data['nickname']

        # Comprueba que las dos contraseñas son iguales
        if data['password'] != data['password2']:
            msg = "Las contraseñas no coinciden"
            print(msg)
            return msg
        # Calcula el hash a partir de la contraseña con 500 iteraciones
        h = argon2.using(rounds=500).hash(data['password'])
        # Borra el campo de verificación de contraseña y mete el hash en el campo de contraseña
        del data['password2']
        data['password'] = h
        try:
            # Intenta insertar el usuario,
            #   capturando la excepcion de clave duplicada si hubiese otro usuario con ese _id
            c.insert_one(data)
            print("Usuario insertado:", data)
            msg = "Bienvenido usuario " + data['name']
            print(msg)
            if totp:
                # Genera y guarda la semilla aleatoria
                n = gen_secret()
                c.update_one({'_id': data['_id']}, {'$set': {'totp': n}})
                # Genera la url para mostrar el QR
                url = gen_qrcode_url(gen_gauth_url('GIW_grupo11', data['name'], n))
                print("Semilla creada y guardada, QR en:", url)
                out = '<h3>Nombre de usuario: ' + data['name'] + '</h3>'
                out += '<h3>Semilla: ' + n + '</h3>'
                out += '<img src="' + url + '"/>'
                return out
            return msg
        except errors.DuplicateKeyError:
            msg = "El alias de usuario ya existe"
            print(msg)
            return msg
    else:
        print("Datos inválidos:", msg)
        return "Datos inválidos"

########################################################################################################################


# Método que abstrae el proceso de login para poder usarlo sin y con TOTP
# no deja que un usuario registrado con TOTP (existe el campo totp en la BD) se pueda loguear sin meter el token
def login_(totp=False):
    req_fields = ['nickname', 'password']
    if totp:
        req_fields.append('totp')
    valid, data, msg = form_data(req_fields)
    if valid:
        # busca un usuario con ese id (nickname)
        r = c.find_one({'_id': data['nickname']})
        # Si lo encuentra continua con las comprobaciones
        valid = False
        if r:
            # Verifica la contraseña pasada
            if argon2.verify(data['password'], r['password']):
                # Si ha entrado por /login y en la BD no tiene el campo totp (login normal)
                try:
                    if not totp and not ('totp' in r.keys()):
                        valid = True
                    # Si ha entrado por /login_totp y en la BD existe el campo totp y este es válido (login con totp)
                    elif totp and ('totp' in r.keys()) and otp.valid_totp(token=data['totp'], secret=r['totp']):
                        valid = True
                except KeyError:
                    pass
        if valid:
            msg = "Bienvenido " + r['name']
            print(msg)
            return msg
        else:
            msg = "Usuario o contraseña incorrectos"
            print(msg)
            return msg
    else:
        msg = "Datos inválidos: " + msg
        print(msg)
        return msg

########################################################################################################################


@post('/signup')
def signup():
    return sign_up()


########################################################################################################################


@post('/change_password')
def change_password():
    valid, data, msg = form_data(['nickname', 'old_password', 'new_password'])
    if valid:
        # busca un usuario con ese id (nickname)
        r = c.find_one({'_id': data['nickname']})
        # Si lo encuentra continua con las comprobaciones
        if r:
            # Verifica que la antigua contraseña sea igual que la almacenada en la BD
            if argon2.verify(data['old_password'], r['password']):
                # Genera el hash de la nueva contraseña
                new_password = argon2.using(rounds=500).hash(data['new_password'])
                # Actualiza el valor de la contraseña del usuario con nick pasado
                c.update_one({'_id': data['nickname']}, {'$set': {'password': new_password}})
                msg = "La contraseña del usuario " + r['name'] + " ha sido modificada"
                print(msg)
                return msg
        msg = "Usuario o contraseña incorrectos"
        print(msg)
        return msg
    else:
        msg = "Datos inválidos: " + msg
        print(msg)
        return msg


########################################################################################################################

@post('/login')
def login():
    return login_()


########################################################################################################################


##############
# APARTADO 2 #
##############

# Genera un string de 16 caracteres siendo los posibles [A-Z] y [2-7]
def gen_secret():
    n = 16
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits[2:8]) for _ in range(n))


# Genera la url para Google Authenticator
def gen_gauth_url(app_name, username, secret):
    return 'otpauth://totp/' + username + '?secret=' + secret + '&issuer=' + app_name
        

def gen_qrcode_url(gauth_url):
    # Codifica para poder pasarlo por GET
    gauth_url = quote(gauth_url)
    urlqr = 'https://api.qrserver.com/v1/create-qr-code/?data=' + gauth_url
    return urlqr


@post('/signup_totp')
def signup_totp():
    msg = sign_up(totp=True)
    return msg


@post('/login_totp')        
def login_totp():
    return login_(totp=True)

    
if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost', port=8080, debug=True)