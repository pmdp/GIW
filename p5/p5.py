# -*- coding: utf-8 -*-

import urllib, os
from BeautifulSoup import *

urlBase = 'http://trenesytiempos.blogspot.com.es'

################################################################################################

def saveImagesFromUrl(url):
    folderName = url[38:42] + '-' + url[43:45] + '-' + url[46:]
    folderName = folderName[:-5]
    #Directorio actual + separador + carpeta
    path = os.getcwd() + os.sep + folderName + os.sep
    #Si la carpeta no existe, se crea
    if not os.path.exists(path):
        os.makedirs(path)
        print "Carpeta creada:", path
    html = urllib.urlopen(url).read()
    sopa = BeautifulSoup(html)
    etiquetas = sopa('a', {"imageanchor": "1"})
    j = 0
    for i in etiquetas:
        archivo = open(path + "foto" + str(j) + ".jpg", "wb")
        imagen = urllib.urlopen(i.get('href', None))
        while True:
            info = imagen.read(100000)
            if len(info) < 1: break
            archivo.write(info)
        print "Foto descargada:", path + "foto" + str(j) + ".jpg"
        archivo.close()
        j = j + 1

################################################################################################

def getAllPosts(url, year=None, getPostContent=False):
    archives = []
    if not getPostContent:
        posts = []
    else:
        posts = dict()
    home = urllib.urlopen(url).read()
    s = BeautifulSoup(home)
    if(year is not None):
        print "Cogiendo enlaces a posts del año", year
    else:
        print "Cogiendo enlaces a posts de todos los años"
    #Coge todas las etiquetas <a> que contienen enlaces a los posts
    aTags = s('a', {"class":"post-count-link"})
    for aTag in aTags:
        #Si la longitud es menor a 62 (links de periodo de tiempo y no de año)
        # y son del año pasado por argumento o por defecto de cualquier año
        #Se añaden a la lista de archivos
        if year is None and len(aTag['href']) < 62:
            archives.append(aTag['href'])
        elif len(aTag['href']) < 62 and aTag['href'][38:42] == year:
            archives.append(aTag['href'])
    #Por cada enlace (por fecha) del archivo lo carga y accede a él
    # guardando el enlace del título del post o posts que haya
    # si getPostContent == True entonces coge también el contenido de ese post
    for archive in archives:
        htmlArchive = urllib.urlopen(archive).read()
        sp = BeautifulSoup(htmlArchive)
        post = sp.findAll('h3', {"class": "post-title entry-title"})
        for i in range(0, len(post)):
            enlace = post[i].a['href']
            if not getPostContent:
                print "Guardando enlace: ", enlace
                posts.append(enlace)
            else:
                print "Guardando contenido del post: ", enlace
                postt = sp.find('div', {"class": "post-body entry-content"})
                posts[enlace]=postt.
    print "En total: ", len(posts), " enlaces."
    return posts

################################################################################################

def searchForKeys(keys):
    posts = getAllPosts(urlBase, year='2013', getPostContent=True)
    for post in posts:
        print post

########################################_MAIN_#################################################
try:
    print "Accediendo a: ", urlBase, '\n'
    # ok = raw_input("Continuar descargando todas las fotos de los posts del 2016 ? si/no: ")
    # if ok.lower() == 'si':
    #     posts = getAllPosts(urlBase, year='2016')
    #     for post in posts:
    #         saveImagesFromUrl(post)
    keys = raw_input("Introduce las palabras clave a buscar en el blog: ")
    urls = searchForKeys(keys)

    # p = urllib.urlopen('http://trenesytiempos.blogspot.com.es/2016/10/cronicas-de-la-via-estrecha-viii-las.html')
    # soup = BeautifulSoup(p)
    # res = soup.findAll('span', text=re.compile('diesel'))
    # if len(res) > 0:
    #     print "Encontrado"

except Exception, e:
    print "Hubo un error: ", e

#div class="post-body entry-content"
################################################################################################