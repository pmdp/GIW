# -*- coding: utf-8 -*-

from bottle import run, get, request, template
from pymongo import MongoClient

mongoclient = MongoClient()
db = mongoclient.giw

########################################################################################################################

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
        return False, u"<p style='color:red'>No se han recibido los argumentos necesarios</p>"


########################################################################################################################

#Función que muestra un mensaje de error con los argumento inválidos
def show_args_error(invalid_args):
    out = u"<p style='color:red'>Argumentos inválidos:</p>\n"
    out += "<ul>"
    for i in invalid_args:
        out += "<li>" + i + "</li>"
    out += "</ul>"
    return out

########################################################################################################################

@get('/top_countries')
# http://localhost:8080/top_countries?n=3
def agg1():
    valid, msg = validate_arguments(['n'], all_needed=True)
    n = 0
    try:
        n = int(request.query.n)
        if n <= 0:
            msg = u"El parametro pasado no es un número positivo"
            valid = False
    except ValueError:
        msg = u"El parametro pasado no es un número"
        valid = False
    if valid:
        c = db.usuarios
        r = c.aggregate([
            {'$group': {'_id': '$pais', 'num': {'$sum': 1}}},
            {'$sort': {'num': -1, '_id': 1}},
            {'$limit': n}
        ])
        data = []
        for e in r:
            print(e)
            row = []
            row.append(e['_id'])
            row.append(e['num'])
            data.append(row)
        return template('table', table_titles=[u'País', u'Nº usuarios'], rows=data)
    else:
        return u"<p style='color:red'>" + msg + "</p>\n"

########################################################################################################################

@get('/products')
# http://localhost:8080/products?min=2.34
def agg2():
    valid, msg = validate_arguments(['min'], all_needed=True)
    min = 0
    try:
        min = float(request.query.min)
    except ValueError:
        msg = u"El parametro pasado no es un número"
        valid = False
    if valid:
        c = db.pedidos
        r = c.aggregate([
            {'$unwind': '$lineas'},
            {'$match': {'lineas.precio': {'$gte': min}}},
            {'$group': {'_id': '$lineas.nombre', 'num': {'$sum': '$lineas.cantidad'},
                        'precio': {'$max': '$lineas.precio'}}}
        ])
        data = []
        for e in r:
            print(e)
            row = []
            row.append(e['_id'])
            row.append(e['num'])
            row.append(e['precio'])
            data.append(row)
        return template('table', table_titles=[u'Nombre producto', u'Nº unidades vendidas', u'Precio unitario'],
                        rows=data)
    else:
        return u"<p style='color:red'>" + msg + "</p>\n"

########################################################################################################################
    
@get('/age_range')
# http://localhost:8080/age_range?min=80
def agg3():
    valid, msg = validate_arguments(['min'], all_needed=True)
    min = 0
    try:
        min = int(request.query.min)
    except ValueError:
        msg = u"El parametro pasado no es un número"
        valid = False
    if valid:
        c = db.usuarios
        r = c.aggregate([
            {'$group': {'_id': '$pais', 'nusuarios': {'$sum': 1}, 'min': {'$min': '$edad'}, 'max': {'$max': '$edad'}}},
            {'$match': {'nusuarios': {'$gt': min}}},
            {'$project': {'rango': {'$add': [{'$multiply': ["$min", -1]}, '$max']}}},
            {'$sort': {'rango': -1, '_id': 1}}
        ])
        data = []
        for e in r:
            print(e)
            row = []
            row.append(e['_id'])
            row.append(e['rango'])
            data.append(row)
        return template('table', table_titles=[u'País', u'Rango de edades'], rows=data)
    else:
        return u"<p style='color:red'>" + msg + "</p>\n"


########################################################################################################################
    
@get('/avg_lines')
# http://localhost:8080/avg_lines
def agg4():
    c = db.pedidos
    r = c.aggregate([
        {'$unwind': '$lineas'},
        {'$group': {'_id': '$_id', 'numLineas': {'$sum': 1}, 'cliente': {'$first': '$cliente'}}},
        {'$lookup': {'from': 'usuarios',
                        'localField': 'cliente',
                        'foreignField': '_id',
                        'as': 'usuario'}},
        {'$group': {'_id': '$usuario.pais', 'numPromLineas': {'$avg': '$numLineas'}}}
    ])
    data = []
    for e in r:
        print(e)
        row = []
        row.append(e['_id'][0])
        row.append(e['numPromLineas'])
        data.append(row)
    return template('table', table_titles=[u'País', u'Nº promedio de líneas de pedido'], rows=data)


########################################################################################################################

@get('/total_country')
# http://localhost:8080/total_country?c=Alemania
def agg5():
    valid, msg = validate_arguments(['c'], all_needed=True)
    country = request.query.c
    if valid:
        #Agregación desde la colección pedidos
        # c = db.pedidos
        # r = c.aggregate([
        #     {'$project': {'cliente': 1, 'total': 1}},
        #     {'$group': {'_id': '$cliente', 'total_cliente': {'$sum': '$total'}}},
        #     {'$lookup': {'from': 'usuarios',
        #                  'localField': '_id',
        #                  'foreignField': '_id',
        #                  'as': 'usuario'}},
        #     {'$match': {'usuario.pais': country}},
        #     {'$group': {'_id': '$usuario.pais', 'total_pais': {'$sum': '$total_cliente'}}}
        # ])
        # Agregación desde la colección usuarios, hemos elegido esta por la eficiencia
        c = db.usuarios
        r = c.aggregate([
            {'$match': {'pais': country}},
            {'$lookup': {'from': 'pedidos',
                         'localField': '_id',
                         'foreignField': 'cliente',
                         'as': 'pedidos'}},
            {'$unwind': '$pedidos'},
            {'$unwind': '$pedidos.lineas'},
            {'$group': {'_id': '$pais', 'total_pais': {'$sum': '$pedidos.lineas.total'}}}
        ])
        data = []
        for e in r:
            print(e)
            row = []
            row.append(e['_id'])
            row.append(e['total_pais'])
            data.append(row)
        return template('table', table_titles=[u'País', u'Total € gastados'], rows=data)
    else:
        return u"<p style='color:red'>" + msg + "</p>\n"

########################################################################################################################
        
if __name__ == "__main__":
    # No cambiar host ni port ni debug
    run(host='localhost',port=8080,debug=True)