# -*- coding: utf-8 -*-
 
# Sixto Jansa Sanz, 
# Jorge Utrilla Olivera, 
# y José Miguel Maldonado Del Pozo
# declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. 
# No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. 
# Declaramos además que no hemos realizado de manera deshonesta ninguna otra actividad
# que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from bottle import run, get, request, template
from pymongo import MongoClient

mongoclient = MongoClient()
db = mongoclient.giw


def getResultsData(c):
    data = []
    #Por cada elemento en el cursor devuelto en la consulta
    for r in c:
        userData = []
        userData.append(r['_id'])
        userData.append(r['email'])
        userData.append(r['webpage'])

        creditCardData = "Número: " + r['credit_card']['number'] + '\n'
        creditCardData += "Fecha de expiración: " + r['credit_card']['expire']['month'] + '/' + \
                          r['credit_card']['expire']['year']
        userData.append(creditCardData)

        userData.append(r['password'])
        userData.append(r['name'])
        userData.append(r['surname'])

        addressData = "Pais: " + r['address']['country'] + '\n'
        addressData += "Zip: " + r['address']['zip'] + '\n'
        addressData += "Calle: " + r['address']['street'] + '\n'
        addressData += "Num: " + r['address']['num']
        userData.append(addressData)

        likesData = ''
        for like in r['likes']:
            likesData += str(like) + '\n'
        userData.append(likesData)

        userData.append(r['birthdate'])

        data.append(userData)
    return data


def validateParameters(argsList):
    args = request.query
    invalidArgs = []
    # Comprueba que todos los argumentos pasados son válidos
    for a in args:
        # Si no es válido lo añade a la lista de argumentos inválidos
        if a not in argsList:
            invalidArgs.append(a)
    return invalidArgs


def showArgsError(invalidArgs):
    out = "<p style='color:red'>Argumentos inválidos:</p>\n"
    out += "<ul>"
    for i in invalidArgs:
        out += "<li>" + i + "</li>"
    out += "</ul>"
    return out


@get('/find_user')
def find_user():
    # http://localhost:8080/find_user?username=burgoscarla
    #Coge el nombre de usuario de la petición GET
    username = request.query.username
    c = db.usuarios
    user = {"_id":username}
    #Busca todos un único usuario con ese id
    res = c.find_one(user)
    #Si existe dicho usuario rellena las listas con los datos de la BD
    if res:
        #Lista para datos simples
        simple_data = list()
        #Lista para todos los datos de dirección
        address = list()
        #Lista para todos los datos de la tarjeta de crédito
        credit_card = list()
        #Lista de todo lo que le gusta al usuario
        likes = list()
        for key, value in res.items():
            if key == 'credit_card':
                credit_card.append('month : ' + value['expire']['month'])
                credit_card.append('year : ' + value['expire']['year'])
                credit_card.append('number : ' + value['number'])
            elif key == 'address':
                for k, v in value.items():
                    address.append(k + ' : ' + v)
            elif key == 'likes':
                for l in value:
                    likes.append(l)
            else:
                simple_data.append(key + ' : ' + value)
        return template('datos', title=username, simple_data=simple_data,
                        address=address, credit_card=credit_card, likes=likes)
    #Si no existe devuelve un error
    else:
        return "<p style='color:red'>El usuario <strong>" + username + " </strong> no existe en la BD.</p>"


@get('/find_users')
def find_users():
    # http://localhost:8080/find_users?name=Luz
    # http://localhost:8080/find_users?name=Luz&surname=Romero
    # http://localhost:8080/find_users?name=Luz&food=hotdog

    invalidArgs = validateParameters(('name', 'surname', 'birthday'))
    #Si no hay ningún elemento inválido procede con la consulta
    if len(invalidArgs) == 0:
        name = request.query.name
        surname = request.query.surname
        birth = request.query.birthday
        #Diccionario donde van a ir los datos a buscar
        data = dict()
        if name:
            data['name'] = name
        if surname:
            data['surname'] = surname
        if birth:
            data['birthdate'] = birth
        c = db.usuarios
        res = c.find(data)
        data = getResultsData(res)
        return template('table', title="Número de resultados: " + str(res.count()), rows=data)
    #Si hay alguno inválido muestra el error
    else:
        return showArgsError(invalidArgs)

@get('/find_users_or')
def find_users_or():
    # http://localhost:8080/find_users_or?name=Luz&surname=Corral
    invalidArgs = validateParameters(('name', 'surname', 'birthday'))
    # Si no hay ningún elemento inválido procede con la consulta
    if len(invalidArgs) == 0:
        name = request.query.name
        surname = request.query.surname
        birth = request.query.birthday
        # Diccionario donde van a ir los datos a buscar
        data = dict()
        if name:
            data['name'] = name
        if surname:
            data['surname'] = surname
        if birth:
            data['birthdate'] = birth
        c = db.usuarios
        res = c.find({'$or', data})
        data = getResultsData(res)
        return template('table', title="Número de resultados: " + str(res.count()), rows=data)
    # Si hay alguno inválido muestra el error
    else:
        return showArgsError(invalidArgs)
               
@get('/find_like')
def find_like():
    # http://localhost:8080/find_like?like=football
    pass


@get('/find_country')
def find_country():
    # http://localhost:8080/find_country?country=Irlanda
    pass
    
    
@get('/find_email_birthdate')
def email_birthdate():
    # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31
    pass
    
    
@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
    # http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc
    pass

    
if __name__ == "__main__":
    # No cambiar host ni port ni debug
    run(host='localhost',port=8080,debug=True)
