# -*- coding: utf-8 -*-

import os.path

def numPalabras ():
    inputFile = False
    
    while not inputFile:
        archivo = raw_input("introduca el nombre del archivo: ")
        archivo = archivo +'.txt'
        if  os.path.exists(archivo):
            inputFile = True
        else: print "Introduzca un nombre de archivo valido "
        
    repetida = 0;
    f = open(archivo,'r')
    texto = f.readlines()
    f.close()
    output= open('salida.txt','w')
    lista_nueva = []
    for line in texto:
        for word in line.split():
            if(word not in lista_nueva):
                lista_nueva.append(word)
                for linea in texto:
                   for search in linea.split() :
                       if (word == search):
                            repetida = repetida + 1
                      
                out = "la palabra " + str(word) + " se repite " + str(repetida) + " veces\n" 
                repetida = 0
                output.write(out)
    output.close()
