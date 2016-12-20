# -*- coding: utf-8 -*-

# Sixto Jansa Sanz,
# Jorge Utrilla Olivera,
# y Jose Miguel Maldonado Del Pozo
# declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal.
# No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie.
# Declaramos además que no hemos realizado de manera deshonesta ninguna otra actividad
# que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from bottle import run, get, request, template
from pymongo import MongoClient
from os import linesep

mongoclient = MongoClient()
db = mongoclient.giw

#Columnas para las tablas de los ejercicios 2, 3, 4, 5 y 7
all_table_data = ['Nombre de usuario', 'e-mail', 'Página web', 'Tarjeta de crédito', 'Hash de contraseña', 'Nombre', 'Apellido', 'Dirección', 'Aficiones', 'Fecha de nacimiento']
#Columnas para el ejercicio 6
mid_table_data = ['id', 'e-mail', 'Fecha de nacimiento']

#Función que recibe un cursor de mongo y prepara una lista para luego mostrarla por html
def get_results_data(c):
    data = []
    #Por cada elemento en el cursor devuelto en la consulta
    for r in c:
        userData = []
        userData.append(r['_id'])
        userData.append(r['email'])
        userData.append(r['webpage'])

        creditCardData = u"Número: " + r['credit_card']['number'] + linesep
        creditCardData += u"Fecha de expiración: " + r['credit_card']['expire']['month'] + '/' + r['credit_card']['expire']['year']
        userData.append(creditCardData)

        userData.append(r['password'])
        userData.append(r['name'])
        userData.append(r['surname'])

        addressData = "Pais: " + r['address']['country'] + linesep
        addressData += "Zip: " + r['address']['zip'] + linesep
        addressData += "Calle: " + r['address']['street'] + linesep
        addressData += "Num: " + r['address']['num']
        userData.append(addressData)

        likesData = ''
        for like in r['likes']:
            likesData += str(like) + linesep
        userData.append(likesData)

        userData.append(r['birthdate'])

        data.append(userData)
    return data


#Función que recibe una lista con los argumentos que deberían haber llegado al servidor
# también recibe un variable que dice si todos los argumentos son obligatorios o no
def validate_arguments(args_list, all_needed=False):
    args = request.query
    invalid_args = []
    valid_args = []
    # Comprueba que todos los argumentos pasados son válidos
    for a in args:
        # Si no es válido lo añade a la lista de argumentos inválidos
        if a not in args_list:
            invalid_args.append(a)
        #Si no lo mete en la lista de argumentos válidos
        else:
            valid_args.append(a)

    if len(invalid_args) != 0:
        return False, show_args_error(invalid_args)
    elif not all_needed and len(valid_args) > 0:
        return True, ''
    elif all_needed and len(valid_args) == len(args) and len(args) > 0:
        return True, ''
    else:
        return False, "<p style='color:red'>No se han recibido los argumentos necesarios</p>"

#Función que muestra un mensaje de error con los argumento inválidos
def show_args_error(invalid_args):
    out = "<p style='color:red'>Argumentos inválidos:</p>\n"
    out += "<ul>"
    for i in invalid_args:
        out += "<li>" + i + "</li>"
    out += "</ul>"
    return out


@get('/find_user')
def find_user():
    # http://localhost:8080/find_user?username=burgoscarla
    valid, msg = validate_arguments(['username'], all_needed=True)
    if valid:
        #Coge el nombre de usuario de la petición GET
        username = request.query.username
        c = db.usuarios
        #Busca todos un único usuario con ese id
        res = c.find_one({"_id":username})
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
    else:
        return msg

@get('/find_users')
def find_users():
    # http://localhost:8080/find_users?name=Luz
    # http://localhost:8080/find_users?name=Luz&surname=Romero
    # http://localhost:8080/find_users?name=Luz&food=hotdog
    valid, msg = validate_arguments(['name', 'surname', 'birthday'])
    if valid:
        #Si no hay ningún elemento inválido procede con la consulta
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
        data = get_results_data(res)
        return template('table', num_results=str(res.count()), table_titles=all_table_data, rows=data)
    else:
        return msg

@get('/find_users_or')
def find_users_or():
    # http://localhost:8080/find_users_or?name=Luz&surname=Corral

    valid, msg = validate_arguments(['name', 'surname', 'birthday'])
    # Si no hay ningún elemento inválido procede con la consulta
    if valid:
        name = request.query.name
        surname = request.query.surname
        birth = request.query.birthday
        # Diccionario donde van a ir los datos a buscar
        data = []
        if name:
            data.append({'name': name})
        if surname:
            data.append({'surname': surname})
        if birth:
            data.append({'birthdate': birth})
        c = db.usuarios
        res = c.find({'$or': data})
        data = get_results_data(res)
        return template('table', num_results=str(res.count()), table_titles=all_table_data, rows=data)
    else:
        return msg
               
@get('/find_like')
def find_like():
    # http://localhost:8080/find_like?like=football
    valid, msg = validate_arguments(['like'], all_needed=True)
    # Si no hay ningún elemento inválido procede con la consulta
    if valid:
        like = request.query.like
        c = db.usuarios
        res = c.find({'likes': like})
        data = get_results_data(res)
        return template('table', num_results=str(res.count()), table_titles=all_table_data, rows=data)
    else:
        return msg

@get('/find_country')
def find_country():
    # http://localhost:8080/find_country?country=Irlanda
    valid, msg = validate_arguments(['country'], all_needed=True)
    # Si no hay ningún elemento inválido procede con la consulta
    if valid:
        country = request.query.country
        c = db.usuarios
        res = c.find({'address.country': country})
        data = get_results_data(res)
        return template('table', num_results=str(res.count()), table_titles=all_table_data, rows=data)
    else:
        return msg


@get('/find_email_birthdate')
def email_birthdate():
    # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31
    valid, msg = validate_arguments(['from', 'to'], all_needed=True)
    # Si no hay ningún elemento inválido procede con la consulta
    if valid:
        from_date = request.query['from']
        to_date = request.query.to
        c = db.usuarios
        # Fecha de nacimiento mayor que fromDate y menor que toDate
        query = {'birthdate': {'$gt': from_date, '$lt': to_date}}
        # query que busca las fechas de nacimiento ordenadas por fecha de nacimiento y por _id
        # y solo proyecta los datos necesarios
        res = c.find(query, {'_id': 1, 'email': 1, 'birthdate': 1 }).sort([('birthdate', 1), ('_id', 1)])
        data = []
        for r in res:
            user_data = []
            user_data.append(r['_id'])
            user_data.append(r['email'])
            user_data.append(r['birthdate'])
            data.append(user_data)
        return template('table', num_results=str(res.count()), table_titles=mid_table_data, rows=data)
    else:
        return msg
    
@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
    # http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc
    valid, msg = validate_arguments(['country', 'likes', 'limit', 'ord'], all_needed=True)
    # Si no hay ningún elemento inválido procede con la consulta
    if valid:
        country = request.query.country
        likes = request.query.likes
        limit = request.query.limit
        order = request.query.ord
        # Almacenamos en una lista todos los likes q se pasan por parametro. Hacemos lista para que $all pueda leer bien.
        gustos = []
        cadena = ""
        for i in likes:
            if i != ',':
                cadena += i
            else:
                gustos.append(cadena)
                cadena = ""
        gustos.append(cadena)
        # en funcion del tipo de ordenacion se le da un valor entero a la variable order
        if order == 'asc':
            order = 1
        elif order == 'desc':
            order = -1

        c = db.usuarios
        query = {'$and': [{'address.country': country}, {'likes': {'$all': gustos}}]}
        # query que busca en funcion de un country y de los gustos ordenando por fechas de nacimiento y con limite = limit
        res = c.find(query).sort('birthdate', int(order)).limit(int(limit))
        data = get_results_data(res)
        return template('table', num_results=str(res.count()), table_titles=all_table_data, rows=data)
    else:
        return msg

    
if __name__ == "__main__":
    # No cambiar host ni port ni debug
    run(host='localhost',port=8080,debug=True)
