# -*- coding: utf-8 -*-

# Sixto Jansa Sanz,
# Jorge Utrilla Olivera,
# y Jose Miguel Maldonado Del Pozo
# declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal.
# No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie.
# Declaramos además que no hemos realizado de manera deshonesta ninguna otra actividad
# que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import bottle
from bottle import run, get, request
from beaker.middleware import SessionMiddleware
import requests
from urllib.parse import urlencode
import time
import hashlib
import os

# Inicialización del middleware para tener sesiones en bottle
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)


# Credenciales. 
# https://developers.google.com/identity/protocols/OpenIDConnect#appsetup
# Copiar los valores adecuados.
CLIENT_ID     = "260757421774-iuvl1e2uv9gmif77mf4bmbru41mv41u1.apps.googleusercontent.com"
CLIENT_SECRET = "LXm_U_pyZpscf2DOQSNwKABg"
REDIRECT_URI  = "http://localhost:8080/token"


# Fichero de descubrimiento para obtener el 'authorization endpoint' y el 
# 'token endpoint'
# https://developers.google.com/identity/protocols/OpenIDConnect#authenticatingtheuser
DISCOVERY_DOC = "https://accounts.google.com/.well-known/openid-configuration"

r = requests.get(DISCOVERY_DOC)

AUTH_ENDPOINT = r.json()['authorization_endpoint']
# Token validation endpoint para decodificar JWT
# https://developers.google.com/identity/protocols/OpenIDConnect#validatinganidtoken
TOKEN_VALIDATION_ENDPOINT = r.json()['token_endpoint']
TOKEN_INFO = "https://www.googleapis.com/oauth2/v3/tokeninfo"


@get('/login_google')
def login_google():
    session = bottle.request.environ.get('beaker.session')
    # Genera el anti-forgery state token para asegurar que todas las peticiones son legitimas
    state_csrf = hashlib.sha256(os.urandom(1024)).hexdigest()
    # Guarda el token en la sesion
    session['anti-CSRF'] = state_csrf
    session.save()
    params = {'client_id': CLIENT_ID, 'response_type': 'code', 'scope': 'openid email', 'redirect_uri': REDIRECT_URI,
              'state': state_csrf}
    return '<a href="' + AUTH_ENDPOINT + '?' + urlencode(params) + '">Login con Google</a>'


@get('/token')
def token():
    # Coge el codigo temporal creado por Google al redirigir a /token
    code = request.query.code
    # token anti-CSRF llegado de Google
    state = request.query.state

    # Coge el token anti-CSRF de la sesion
    session = bottle.request.environ.get('beaker.session')
    state_csrf = session['anti-CSRF']
    # Comprueba que el token anti-CSRF llegado de Google sea el miso que el guardado en el servidor
    if state == state_csrf:
        params = {'code': code, 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'redirect_uri': REDIRECT_URI,
                  'grant_type': 'authorization_code'}
        # Hace una petición para intercambiar el código temporal por el id_token y access_token
        r = requests.post(TOKEN_VALIDATION_ENDPOINT, params=params)
        id_token = r.json()['id_token']

        params = {'id_token': id_token}
        # Petición para descifrar el id_token
        r = requests.get(TOKEN_INFO, params=params)
        # Se realizan las comprobaciones de validación del id_token
        valid = True
        if r.status_code == 200:
            if r.json()['iss'] not in ['https://accounts.google.com', 'accounts.google.com']:
                valid = False
            if r.json()['aud'] != CLIENT_ID:
                valid = False
            if int(r.json()['exp']) < int(time.time()):
                valid = False
        else:
            valid = False
        if valid:
            email = r.json()['email']
            return u"Bienvenido " + email
        else:
            return u"Fallo al validar el id_token"
    else:
        return u"Petición ilegítima"


if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost',port=8080,debug=True, app=app)
