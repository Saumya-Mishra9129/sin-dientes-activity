import random
from gettext import gettext as _

def palabra_aleatoria():
    """retorna una palabra obtenida del archivo lista_palabras.txt"""
    archivo = open(_('resources/lista_palabras.es.txt'),'r')
    palabras = [palabra.strip().lower() for palabra in archivo.readlines() if palabra.strip().isalpha() and len(palabra) > 4]
    archivo.close()
              
    return palabras[random.randint(0, len(palabras)-1)]
