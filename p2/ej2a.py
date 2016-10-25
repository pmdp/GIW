#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

def semaforos():
    try:
        #Lee el archivo con la información
        semFile = open('semaforos.txt','r')
        #Lista que va a contener los distintos objetos json
        jsons = []
        #Diccionario con clave (ubicación) y valor (número de semáforos)
        ubSem = dict()
        #variable con el número de semáforos totales
        numSemTot = 0.0
        
        for linea in semFile:
            #Lee el archivo linea a linea y va metiendo cada una en la lista jsons
            linea = linea.rstrip('\n')
            linea = linea.rstrip(',')
            jsons.append(linea)
        for i in range (5,len(jsons)-2):
            #Recorre toda la lista de jsons omitiendo los 4 primeros y los 2 últimos que no contienen info relevante
            #Para cada ubicación:
            js = json.loads(jsons[i])
            #Coge solo el texto de la descripción
            description = js["properties"]["Description"]
            ubicacion = getInfo(description, u"<b>Ubicación:</b>")
            numSemaforos = toInt(getInfo(description, u"<b>Semáforos:</b>"))
            #Establece como clave la ubicacion y como valor el número de semáforos
            ubSem[ubicacion] = numSemaforos
            #Incrementa el número de semáforos totales
            numSemTot += numSemaforos    
            #print u'{0:50} --> {1:3d}'.format(ubicacion, numSemaforos)
        
        ubis = ubSem.keys()
        for i in ubis:
            ubSem[i] = ubSem[i] / numSemTot
        #print ubSem
        #cont = 0
        #for i in ubis:
        #    cont += ubSem[i]
        #print cont
        #print "Número total de semáforos: ", numSemTot
        outFile = open('outputSemaforos.txt', 'w')
        #for i in ubis:
        #    line = i + ubSem[i] + '\n'
        #    outFile.write(line)
    
    except: print "Hubo algún fallo"
    finally:
        semFile.close()
        outFile.close()

def getInfo(txt, filtro):
    """Función que dado un texto y un filtro saca el dato buscado"""
    posIni = txt.find(filtro) + len(filtro)
    dato = txt[posIni:]
    index = 0
    #Busca el final (termina con <)
    for car in dato:
        if car == '<':
            break
        index += 1
    posFin = posIni + index
    return txt[posIni:posFin]

def toInt(data):
    if data == ' ':
        return 0
    else:
        return int(data)

semaforos()