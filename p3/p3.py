# -*- coding: utf-8 -*-

from xml.etree import ElementTree
import urllib
import os

url = ""
nombre = ""
descripcion = ""
latitud = ""
longitud = ""


def practica3():
    try:
        with open('MonumentosZaragoza.xml', 'rt') as f:
            tree = ElementTree.parse(f)


    except:
        print "Archivo no encontrado"

    for monument in tree.iter('PropertyValue'):
        name = monument.get('name')
        if name == "nombre":
            print monument.text

    salir = False
    while not salir:
        m = raw_input("introduce el nombre de un monumento: ")
        sourceEncoding = "iso-8859-1"
        targetEncoding = "utf-8"
        m = unicode(m, sourceEncoding).encode(targetEncoding)

        cont = 0
        encontrado = False
        for monument in tree.iter('PropertyValue'):
            if encontrado == False:
                if monument.text == m.decode('utf-8') or cont > 0:
                    if cont == 0:
                        global nombre
                        nombre = m
                    elif cont == 1:
                        global url
                        url = monument.text
                        encontrado = True
                    cont = cont + 1
        if encontrado:
            # try:
            conexionPagina(url)
            conexionMaps(nombre)
            mostrar()
            # except:
            #    print "No se ha podido conectar a internet"

        else:
            print "No se ha encontrado dicho monumento."

        salida = raw_input("Desea buscar otro monumento? [Si], [No]: ").lower()
        if salida == 'no':
            salir = True
            break


def conexionPagina(url):
    Contenido = urllib.urlopen(url)
    f = Contenido.read()
    sourceEncoding = "iso-8859-1"
    targetEncoding = "utf-8"
    target = open("target.xml", "w")

    target.write(unicode(f, sourceEncoding).encode(targetEncoding))
    target.close()
    a = open("target.xml", "r")
    f = a.read()
    a.close()
    os.remove("target.xml")
    cabecera = "<h3>Descripción</h3>"
    final = "<h3>Enlaces</h3>"
    s = ""
    p = ""
    for i in f:
        s = s + i
        if cabecera in s:
            if final not in s:
                p = p + i
            else:
                p = p + ">"
                break

    estilo = "<strong>Estilo:"
    referencia = "<a href="
    datos = "Más Datos:"
    datosPunto = ".Más Datos:"
    man = "</main"
    manPunto = ".</main"
    z = ""
    for j in p:
        z = z + j
        if estilo in z or referencia in z or datos in z or man in z or manPunto in z or datosPunto in z:
            break

    c = '<h3> Descipción </h3> <div> <p> </p> <a href= <strong> <a> </a> Estilo: </strong> </div> Enlaces '
    borrar = c.split()

    for char in borrar:
        z = z.replace(char, '')

    global descripcion
    descripcion = z


def conexionMaps(nombre):
    serviceurl = 'http://maps.googleapis.com/maps/api/geocode/xml?'
    monumento = nombre

    url = serviceurl + urllib.urlencode({'address': monumento, 'components': 'country:ES'})
    uh = urllib.urlopen(url)
    data = uh.readlines()

    location = "<location>"
    fin = "</location>"
    encontrado = False
    cont = 0
    for loc in data:
        if fin not in loc:
            if location in loc:
                encontrado = True
            elif encontrado:
                if cont == 0:
                    lat = loc
                    cont = cont + 1
                else:
                    lng = loc
        else:
            break
    global latitud
    latitud = quitarLatLng(lat)
    global longitud
    longitud = quitarLatLng(lng)


def quitarLatLng(lat):
    c = "<>/latlng"
    lista = list(c)
    for char in lista:
        lat = lat.replace(char, '')
    return lat


def mostrar():
    print "Nombre del monumento: " + nombre + "\n"
    print "Latitud: " + latitud + "Longitud: " + longitud + "\n"
    print "Página web asociada: " + url + "\n"
    print "Descripcion: " + "\n" + descripcion.replace(descripcion[:1], '')