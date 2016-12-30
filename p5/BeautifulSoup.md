## BeautifulSoup

```python
from BeautifulSoup import *

```



#### Funciones:

- **BeautifulSoup()**: genera un objeto que tiene un conjunto de metodos para **imprimir**, **parsear** o **analizar** un documento html.

- **Métodos para imprimir**:

  - **str()**:muestra el documento como una cadena, pero no elimina nodos que solo tengan un espacio en blanco ni añade espacios en blanco entre los nodos.
  - **unicode()**: igual que la anterior pero con cadena unicode.
  - **prettify()**: Añade nuevas líneas y espacios para mostrar la estructura del documento html, y elimina nodoso que solo tengan espacios en blanco.
  - **renderContents**: muestra el documento como una cadena en la codificación dada, y si no se indica se muestra como una cadena unicode.
  - Cuando se usan str() y renderContents() sobre una etiqueta no muestran lo mismo, en el caso de renderContents muestra solo el contenido dentro de la etiqueta.
  - Al llamar a estas funciones se puede pasar la codificación, ejemplo: ```soup.__str__("ISO-8859-1")```

- **Análisis**:

  - Los objetos del tipo Tag pueden tener atributos asociados ```soup.p```pero los NavigableString no.

  - Métodos y atributos:

    - **parent**: accede al objeto que representa la etiqueta padre.

    - **contents**: lista ordenada de los objetos Tag y NavigableString contenidos dentro de un elemento.

    - **string**: Si un Tag solo tiene un nodo hijo y se trata de una cadena, entonces se puede acceder al mismo mediante tag.string o mediante tag.contents[0]. Cuando existen hijos, y se trata de acceder al atributo string, devuelve como resultado el valor None.

    - **nextSibling y previousSibling**: Accede al elemento anterior o posterior al mismo nivel del objeto considerado.

    - **next y previous**: Permite navegar en el árbol de procesamiento sobre los objetos en el orden en el que fueron procesados en vez del orden dado por el árbol.

    - **findAll y find**: Permite buscar en el árbol. Solo disponible en el objeto que representa el árbol y en los Tag pero no en el NavigableString. 

      ```python
      findAll(name, attrs, recursive, text, limit)
      #Name: nombre de la etiqueta
      #attrs: pares atributo-valor para buscar por los atributos de las etiquetas
      #text: permite buscar objetos NavigableString, y puede tomar valores como cadema, expresión regular, lista o diccionario, True o None. Si se usa este argumento, las restricciones sobre nombre o atributo no se tienen en cuenta.
      #recursive: True(defecto) o False

      #Ejemplos
      soup.findAll('b') #Nombre de etiqueta
      soup.findAll(re.compile('^b')) #Reg. Expr.
      soup.findAll(['title', 'p']) #Lista
      soup.findAll({'title':True,'p':True}) #Diccionario
      soup.findAll(True) #Todos los objetos tag
      soup.findAll(lambda tag : len(tag.name)==1 and not tag.attrs) #Etiquetas con longitud de 1 y que no tengan atributos, ej: <b>
      soup.findAll(align='center')
      soup.findAll(id=re.compile("parra$"))
      soup.findAll(align=["center","blah"])
      soup.findAll(align=None) #etiquetas sin valor para el atributo align
      soup.findAll('p',{'align':'center'}) #Combinar búsuqeda por nombre y por atributo

      ```

      ```python
      find(name, attrs, recursive, text)
      #Similar a findAll solo que devuelve solo una coincidencia, es findAll con limit = 1
      ```

      ​

    - **findNextSiblings y findNextSibling**:

      ``` Python
      findNextSiblings(name, attrs, text, limit)
      findNextSibling(name, attrs, text)
      #Devuelve el nodo/s hermano/s más cercanos a la etiqueta dada que coincida con los criterios de búsqueda y que aparece después de la etiqueta considerada.
      ```

    - **findAllNext y findNext**:

      ```Python
      findAllNext(name, attrs, text, limit)
      findNext(name, attrs, text):
      #Devuelve todos los elementos(el elemento) que coincida con los criterios de búsqueda y que aparece después de la etiqueta considerada.
      ```

    - **findAllPrevious y findPrevious**:

      ```python
      findAllPrevious(name,attrs,text,limit)
      findPrevious(name,attrs,text)
      #Devuelve todos los elementos(el elemento) que coincida con los criterios de búsqueda y que aparece antes de la etiqueta considerada.
      ```

      ​

    - **findParents y findParent**:

      ```Python
      findParents(name, attrs, limit)
      findParent(name, attrs)
      #Devuelve los padres de la etiqueta considerada que coinciden con los criterios de búsqueda.
      ```

- **Modificación del árbol de procesamiento**: