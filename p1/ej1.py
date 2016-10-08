# -*- coding: utf-8 -*-

def cifrado(): 
    minus = map(chr, range(97, 123))
    mayus = map(chr, range(65, 91))
    texto = raw_input("Introduce el texto: ")
    palabras = texto.split( )
    salidaTexto = ""
    
    salir = False
    while not salir:    
        try:
           desL = raw_input("Introduce la rotación de las letras: ")
           entL = int(desL)
           salir = True
        except:
            print "Introduce un numero"
    salir = False    
    while not salir:  
        try:
            desP = raw_input("Introduce la rotación de las palabras: ")
            entP = int(desP)
            salir = True
        except:
             print "Introduce un numero"
    #Mayusculas 65-90 , minusculas 97-122
    aux = [None] * len(palabras)
    for index,p in enumerate(palabras):
        aux[(index + entP) % len(palabras)] = palabras[index]
        
    palabras = aux
    for palabra in palabras:
        for letra in palabra:
            if letra in minus:#comprobacion si es minuscula
                pos = minus.index(letra)
                salidaTexto = salidaTexto + minus[(pos+entL)%26]
               
            elif letra in mayus:#comprobacion si es mayuscula
                pos = mayus.index(letra)
                salidaTexto = salidaTexto + mayus[(pos+entL)%26]
                
            else :#si no es ni minus ni mayus se queda igual
                 salidaTexto = salidaTexto + letra
        salidaTexto = salidaTexto + " "
        
    
    salidaTexto = salidaTexto + "\n"
    print salidaTexto
