#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle,route,run,request
import sqlite3

@route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="usuario" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" name='login' type="submit" />
            <input value="Register" name='register' type="submit" />
        </form>'''

@route('/login',method='POST')
def do_login():
    username = request.forms.get('usuario')
    password = request.forms.get('password')
    lo = request.forms.get('login')
    if lo:
        if username=="antonio" and password=="antonio":
            return "<p>Login correcto: </p>"
        else:
            return "<p>Login incorrecto.</p>"
    else:
        do_register()


def do_register():
    return "<p>Registrando.</p>"


if __name__ == "__main___":
    run(host='localhost', port=8080)