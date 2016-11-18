#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

#Conexión a Base de Datos
db = sqlite3.connect('concesionario.sqlite3')
db.text_factory = 'utf-8'

#Tabla usuaios
db.execute("DROP TABLE IF EXISTS Usuarios")
db.execute("""CREATE TABLE Usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(30) NOT NULL,
        apellidos VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        usuario VARCHAR(20) NOT NULL,
        passwd VARCHAR(20) NOT NULL
        )""")
admin = (1, 'admin', 'admin', 'admin@admin.com', 'admin', 'admin')
print '\n', "Insertando ", admin, "en tabla Usuaios", '\n'
db.execute('''INSERT INTO Usuarios (id, nombre, apellidos, email,
            usuario, passwd) VALUES (?,?,?,?,?,?)''', admin)

#Tabla Coches
db.execute("DROP TABLE IF EXISTS Coches")
db.execute("""CREATE TABLE Coches (
        id INTEGER PRIMARY KEY,
        marca VARCHAR(30) NOT NULL,
        modelo VARCHAR(30) NOT NULL,
        anyo CHAR(5) NOT NULL,
        caballos INTEGER NOT NULL,
        cilindrada FLOAT NOT NULL,
        combustible VARCHAR(10) NOT NULL,
        consumo FLOAT NOT NULL,
        descripcion TEXT DEFUALT '',
        foto VARCHAR(20) DEFAULT 'coche.png'
        )""")

#Abre el archivo con las filas de la tabla Coches
#Inserta fila a fila
print '\n', "Insertando Coches:", '\n'
cochesF = open('insertCoches.txt', 'r')
for c in cochesF:
    cols = c.split(';')
    #se salta la primera línea del archivo que contiene un comentario de los campos de la tabla
    if cols[0] != '#':
        data = (cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7], cols[8], cols[9])
        print "Insertando: ", data, " en tabla Coches."
        db.execute('''INSERT INTO Coches (id, marca, modelo, anyo, caballos,
            cilindrada, combustible, consumo, descripcion, foto)
            VALUES (?,?,?,?,?,?,?,?,?,?)''', data)
cochesF.close()

#Guarda los cambios
db.commit()
db.close()