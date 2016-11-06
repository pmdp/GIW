# -*- coding: utf-8 -*-

import csv

def ejer1Apartado1 ():
    csvFile = open('agua_eprtr_2008_030412.csv')
    print('Eliminando cabeceras de' + str(csvFile) + '...')
    
    # Leer el archivo cvs y saltarse las dos primeras líneas
    
    csvRows = []
    empresas = []
    contaminantes = []
    readerObj = csv.reader(csvFile, delimiter=';')
    for row in readerObj:
        if readerObj.line_num == 1 or readerObj.line_num == 2:
            continue # Saltar primera línea
        csvRows.append(row)
    csvFile.close()
    
    lista = list(csvRows)
    f = open("AguaAgrupada.csv",'w')
    for emp in lista:
        if emp[2] not in contaminantes:
            contaminantes.append(emp[2])        
            for row in lista:
                if row[2] == emp[2]:
                    f.write(row[2]+ ";"+ row[8]+ "\n")
                    
    f.close()
    print empresas
    

def ejer1Apartado2 ():
    csvFile = open('residuos_peligrosos_eprtr_2008_040412.csv')
    print('Eliminando cabeceras de' + str(csvFile) + '...')
    
    # Leer el archivo cvs y saltarse las dos primeras líneas
    
    csvRows = []
    empresas = []
    contaminantes = []
    
    readerObj = csv.reader(csvFile, delimiter=';')
    for row in readerObj:
        if readerObj.line_num == 1 or readerObj.line_num == 2:
            continue # Saltar primera línea
        csvRows.append(row)
    csvFile.close()
    
    lista = list(csvRows)
    numDeLineas = len(csvRows)
    f = open("FrecuenciaResiduos.csv",'w')
    for emp in lista:
        cont = 0
        if emp[2] not in contaminantes:
            contaminantes.append(emp[2])        
            for row in lista:
                if row[2] == emp[2]:
                    cont = cont + 1        
            frecuencia = float(cont) / float(numDeLineas)
            f.write(emp[2]+ ";"+ str(frecuencia * 100)+ "\n")
    f.close()
    print empresas   
    
def ejer1Apartado3 ():
    csvFile = open('aire_eprtr_2008_030412.csv')
    print('Eliminando cabeceras de' + str(csvFile) + '...')
    
    # Leer el archivo cvs y saltarse las dos primeras líneas
    
    csvRows = []
    csvLineas = []
    contaminantes = []
    cantidadKG = []
    
    readerObj = csv.reader(csvFile, delimiter=';')
    for row in readerObj:
        if readerObj.line_num == 1 or readerObj.line_num == 2:
            continue # Saltar primera línea
        csvRows.append(row)
    csvFile.close()
    
    #Escribo en el archivo todosContaminan.csv el nombre de la empresa y la cantidad de Kg con . en lugar de , para hacer la conversion a float
    
    lista = list(csvRows)
    f = open("todosContaminan.csv",'w')
    for emp in lista:
        cont = 0.0
        if emp[2] not in contaminantes:
            contaminantes.append(emp[2])        
            for row in lista:
                if row[2] == emp[2]:
                    cantidad = float(row[10].replace(',','.'))
                    cont = cont + cantidad
            f.write(emp[2]+ ";"+ str(cont)+ "\n")
    f.close()
    
    f = open("todosContaminan.csv")
    reader = csv.reader(f,delimiter=';')
    #leo del archivo creado antes , el nombre y la cantidadKG
    for linea in reader:
        csvLineas.append(linea)
    lista = list(csvLineas)
    #Añado a una lista, todos los KG
    for company in lista:
        cantidadKG.append(float(company[1]))
     #ordeno la lista con la funcion sorted      
    cantidadOrdenada = list(sorted(cantidadKG))
    cont = 1
    f = open("Contaminantes.csv",'w')    
    #busco el mayor valor entre todas las empresas y lo guardo en el archivo
    while cont <= 10:
        maximo = cantidadOrdenada.pop()
        for c in lista:
            if float(c[1]) == float(maximo):
                f.write(c[0]+";"+c[1]+"\n")
                cont = cont + 1 
    f.close()

ejer1Apartado1()
ejer1Apartado2()
ejer1Apartado3()