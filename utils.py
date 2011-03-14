import random
import logging
from gettext import gettext as _
log = logging.getLogger('utils')

def palabra_aleatoria(nivel):
    """retorna una palabra obtenida del archivo lista_palabras.txt"""
    path = 'resources/nivel%s.palabra' %(nivel)
    archivo = open(path,'r')
    palabras = [palabra.lower() for palabra in archivo.readlines()]
    archivo.close()
              
    return palabras[random.randint(0, len(palabras)-1)].split(',')

def validar_uri(uri):
    log.debug('validar uri')
    lista = uri.split('.')
    if 'palabra' in lista[1]:
        return 1
    else:
        return 0

def importar_lista_p(uri, nivel):
    '''importa una nueva lista de palabras'''
    if validar_uri(uri):
        log.debug('palabra importada')
        path = 'resources/nivel%s.palabra' %(nivel + 1)
        archivo = open(uri, 'r') #lee el archivo a exportar
        archivo_viejo = open(path, 'r+w')
        texto = archivo.read()
        archivo_viejo.write(texto)
        archivo_viejo.close()
        archivo.close()

