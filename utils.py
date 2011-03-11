import random
from gettext import gettext as _

def palabra_aleatoria(nivel):
    """retorna una palabra obtenida del archivo lista_palabras.txt"""
    path = 'resources/nivel%s.palabra' %(nivel)
    archivo = open(path,'r')
    palabras = [palabra.lower() for palabra in archivo.readlines()]
    archivo.close()
              
    return palabras[random.randint(0, len(palabras)-1)].split(',')
