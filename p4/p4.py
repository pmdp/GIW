# -*- coding: utf-8 -*-

import sqlite3

def practica4():
    try:

        #Initialize BD
        conn = conexionBD()
        cur = conn.cursor()

        #Create tables
        print "- Creando tablas:", '\n'
        tablaCompradores(cur)
        tablaLibros(cur)
        tablaCompras(cur)

        #Insert data
        print "- Insertando datos:", '\n'
        insertCompradores(cur)
        insertLibros(cur)
        insertCompras(cur)
        conn.commit()

        #Consults
        consultas(cur)

        #Commit and close
        conn.commit()

    except Exception as e:
        print "Ocurrió un error: ", e

    finally:
        cur.close()
    
def conexionBD():
    conn = sqlite3.connect('libreria.sqlite3')
    conn.text_factory = str
    return conn

def tablaCompradores(cur):
    cur.execute("DROP TABLE IF EXISTS Compradores")
    cur.execute('''CREATE TABLE Compradores (
    registro INTEGER(4) PRIMARY KEY NOT NULL,
    nombre VARCHAR(35) NOT NULL DEFAULT ' ',
    fecha_nacim DATE NOT NULL DEFAULT '0000-00-00',
    telefono VARCHAR(10) DEFAULT NULL,
    domicilio VARCHAR(35) DEFAULT NULL,
    poblacion VARCHAR(25) DEFAULT NULL,
    anotaciones TEXT)''')
   #cur.close()

def tablaLibros(cur):
    cur.execute("DROP TABLE IF EXISTS Libros")
    cur.execute('''CREATE TABLE Libros (
    registro INTEGER(4) PRIMARY KEY NOT NULL,
    titulo VARCHAR(35) NOT NULL DEFAULT ' ' UNIQUE,
    escritor VARCHAR(35) NOT NULL DEFAULT ' ',
    editorial VARCHAR(20) NOT NULL DEFAULT ' ',
    soporte VARCHAR(35) NOT NULL DEFAULT 'LIBRO',
    fecha_entrada DATE NOT NULL DEFAULT '0000-00-00',
    pais VARCHAR(20) NOT NULL DEFAULT ' ',
    importe DECIMAL(8,2) NOT NULL DEFAULT '0.0',
    anotaciones BLOB)''')

def tablaCompras(cur):
    cur.execute("DROP TABLE IF EXISTS Compras")
    cur.execute('''CREATE TABLE Compras (
    registro INTEGER(4) PRIMARY KEY NOT NULL,
    id_comprador INTEGER(4) NOT NULL DEFAULT ' ',
    id_libro INTEGER(4) NOT NULL DEFAULT ' ')''')

def insertCompradores(cur):
    #Abre el archivo con las filas de la tabla Compradores
    #Inserta fila a fila
    print "- Insertando en Compradores:", '\n'
    compradoresF = open('insertCompradores.txt', 'r')
    for c in compradoresF:
        cols = c.split(';')
        if (cols[6] == ''):
            cols[6] = None
        data = (cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6])
        print "Insertando: ", data, " en tabla Compradores."
        cur.execute('''INSERT INTO Compradores (registro, nombre, fecha_nacim,
            telefono, domicilio, poblacion, anotaciones) VALUES (?,?,?,?,?,?,?)''', data)
    compradoresF.close()

def insertLibros(cur):
    #Abre el archivo con las filas de la tabla Libros
    #Inserta fila a fila
    print '\n', "- Insertando en Libros:", '\n'
    librosF = open('insertLibros.txt', 'r')
    for l in librosF:
        cols = l.split(';')
        if (cols[8] == ''):
            cols[8] = None
        data = (cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7], cols[8])
        print "Insertando: ", data, " en tabla Libros."
        cur.execute('''INSERT INTO Libros (registro, titulo, escritor, editorial, soporte,
            fecha_entrada, pais, importe, anotaciones) VALUES (?,?,?,?,?,?,?,?,?)''', data)
    librosF.close()

def insertCompras(cur):
    #Abre el archivo con las filas de la tabla Libros
    #Inserta fila a fila
    print '\n', "- Insertando en Compras:", '\n'
    comprasF = open('insertCompras.txt', 'r')
    for c in comprasF:
        cols = c.split(';')
        data = (cols[0], cols[1], cols[2])
        print "Insertando: ", data, " en tabla Compras."
        cur.execute('INSERT INTO Compras (registro, id_comprador, id_libro) VALUES (?,?,?)', data)
    comprasF.close()

def consultas(cur):
    #Consulta 1
    print '\n', "- Consultando los paises y sus libros vendidos:", '\n'
    cur.execute('''SELECT pais, COUNT(c.id_libro) AS nventas
        FROM Libros l, Compras c WHERE l.registro = c.id_libro
        GROUP BY pais ORDER BY nventas desc''')
    print '{0:15} {1:15}'.format("Pais", "Número de vendidos"), '\n'
    for (pais,nvendidos) in cur.fetchall():
        print '{0:20} {1:3d}'.format(pais, nvendidos)

    #Consulta 2
    print '\n', "- Consultando la media de gasto por poblaciones:", '\n'
    cur.execute('''SELECT poblacion, AVG(l.importe) as gastoMedio
        FROM Compradores c, Libros l, Compras cp
        WHERE c.registro=cp.id_comprador AND l.registro=cp.id_libro
        GROUP BY poblacion ORDER BY gastoMedio DESC''')
    print '{0:20} {1:15}'.format("Población", "Gasto medio"), '\n'
    for (poblacion, gastoMedio) in cur.fetchall():
        print '{0:20} {1:5f}'.format(poblacion, gastoMedio)

    # Consulta 3
    print '\n', "- Actualizando tabla compras:", '\n'
    cur.execute(
        'UPDATE Compras SET id_libro=3 WHERE registro=10')
    cur.execute(
        'UPDATE Compras SET id_libro=7 WHERE registro=11')

    # Consulta 4
    print '\n', "- Consultando el precio medio de los libros según el soporte:", '\n'
    cur.execute('SELECT soporte, AVG(l.importe) FROM Libros l GROUP BY soporte')
    print '{0:20} {1:15}'.format("Soporte", "Precio medio"), '\n'
    for (soporte, precioMedio) in cur.fetchall():
        print '{0:20} {1:5f}'.format(soporte, precioMedio)

    # Consulta 5
    print '\n', "- Borrando los compradores que nunca han comprado un libro:", '\n'
    cur.execute('SELECT registro FROM Compradores WHERE registro NOT IN (SELECT id_comprador FROM Compras)')
    for registro in cur.fetchall():
        print '{0:30} {1:2}'.format("Borrando comprador con registro=", registro)
        cur.execute('DELETE FROM Compradores WHERE registro=?', registro)

practica4()