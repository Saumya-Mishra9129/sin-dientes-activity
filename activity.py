# -*- coding: UTF-8 -*-
from sugar.activity import activity
import gtk
import logging
from gettext import gettext as _
from os.path import exists
from datetime import datetime
import pickle
import utils

_logger = logging.getLogger('chintano-activity')
_logger.setLevel(logging.DEBUG)

class Chintano(activity.Activity):

    def __init__(self, handle):
        super(Chintano, self).__init__(handle)
        #ventana
        self.set_title(_('Sin Dientes'))
        self.connect('key-press-event', self._key_press_cb)

        #Barra de herramientas sugar
        barra_herramientas = activity.ActivityToolbox(self)
        self.set_toolbox(barra_herramientas)
        barra_herramientas.show()

        #contenedores
        self.contenedor = gtk.VBox()
        self.contenedor_superior = gtk.HBox()
        self.contenedor_inferior= gtk.HBox()
        self.contenedor.pack_start(self.contenedor_superior)
        self.contenedor.pack_start(self.contenedor_inferior, expand=False)
        self.subcontenedor= gtk.VBox()
        self.contenedor_nivel = gtk.VBox()

        #interface instrucciones
        self.contenedor_instruc = gtk.VBox()
        self.contenedor_instruc_1 = gtk.HBox()
        self.contenedor_instruc_2 = gtk.HBox()
        self.imagen_1 = gtk.Image()
        self.imagen_1.set_from_file('resources/sindiente1.png')
        self.instruc = gtk.Label(_('Instrucciones'))
        self.instruc_1 = gtk.Label(_('Oprime el botón “Nuevo Juego” para empezar a jugar.'))
        self.instruc_2 = gtk.Label(_('La lineas representan las letras de las palabras que están ocultas. Cuenta las letras se compone la palabra.'))
        self.instruc_3 = gtk.Label(_('Ingresa una letra en el espacio en blanco y oprime el botón “Ingresar”. Si descubres una letra esta aparecerá sobre la linea y ganarás un punto. Pero si fallas, tu amigo perderá un diente.'))
        self.instruc_4 = gtk.Label(_('Las letras que ya han sido ingresadas no podrán ser usada de nuevo y aparecerán en el área de \“Letras Usadas\”'))
        self.contenedor_instruc_1.pack_start(self.instruc_1)
        self.contenedor_instruc_1.pack_start(self.imagen_1)
        self.contenedor_instruc.pack_start(self.instruc)
        self.contenedor_instruc.pack_start(self.contenedor_instruc_1)
        #self.contenedor_instruc.pack_start(self.contenedor_instruc_2)
        
        
        #interface menu 
        self.nivel_1 = gtk.Button(_('Nivel 1'))
        self.nivel_1.connect('clicked', self._nivel_uno_cb, None)
        self.nivel_2 = gtk.Button(_('Nivel 2'))
        self.nivel_2.connect('clicked', self._nivel_dos_cb, None)
        self.nivel_3 = gtk.Button(_('Nivel 3'))
        self.nivel_3.connect('clicked', self._nivel_tres_cb, None)
        self.instrucciones = gtk.Button(_('Instrucciones'))
        self.instrucciones.connect('clicked', self._instrucciones_cb, None)
        self.importar_btn = gtk.Button(_('Agregar palabras'))
        self.importar_btn.connect('clicked', self._importar_cb, None)
        self.bienvenida = gtk.Label(_('Bienvenido a \"Sin Diente\"'))

        #interface juego
        self.imagen = gtk.Image()
        self.instrucciones_label = gtk.Label()
        self.instrucciones_label.set_justify(gtk.JUSTIFY_FILL)
        self.instrucciones_label.set_line_wrap(gtk.TRUE)
        self.aciertos_label = gtk.Label('Puntaje: 0')
        self.errores_label = gtk.Label()
        self.palabra_label = gtk.Label()
        self.letrasusadas_label = gtk.Label(_('Letras Usadas: '))
        self.palabra_entry = gtk.Entry()
        self.ok_btn = gtk.Button(_('Ingresar'))
        self.ok_btn.connect('clicked', self._ok_btn_clicked_cb, None)
        self.nuevojuego_btn = gtk.Button(_('Nuevo Juego'))
        self.nuevojuego_btn.connect('clicked', self._nuevojuego_btn_clicked_cb, None)
        self.atras_btn = gtk.Button(_('Atras'))
        self.atras_btn.connect('clicked', self._atras_cb)
        self._cambiar_imagen(0)
        self.palabra_entry.set_sensitive(False)
        self.ok_btn.set_sensitive(False)         
        self.aciertos = 0 #Cuenta los aciertos de letras en la palabra secreta
        self.lista_record = self._load_puntaje()

        #agregando elementos juego
        self.marco = gtk.Frame(_("Instrucciones"))
        self.marco.set_size_request(350, -1)
        self.contenedor_superior.pack_start(self.imagen)
        self.contenedor_superior.pack_start(self.marco)
     
        self.subcontenedor.pack_start(self.instrucciones_label)
        self.subcontenedor.pack_start(self.aciertos_label)
        self.subcontenedor.pack_start(self.errores_label)
        self.subcontenedor.pack_start(self.letrasusadas_label)
        self.subcontenedor.pack_start(self.palabra_label)
        self.marco.add(self.subcontenedor)

        self.contenedor_inferior.pack_start(self.atras_btn, False, padding = 6)
        self.contenedor_inferior.pack_start(self.palabra_entry, padding = 1)
        self.contenedor_inferior.pack_start(self.ok_btn, False, padding = 1)
        self.contenedor_inferior.pack_start(self.nuevojuego_btn, False, padding = 1)
                
        #agregando elementos de menú
        self.contenedor_nivel_h = gtk.HBox()
        self.contenedor_nivel_h.pack_start(self.contenedor_nivel, padding = 100)
        self.contenedor_nivel.pack_start(self.bienvenida, False, padding = 90)
        self.contenedor_nivel.pack_start(self.nivel_1, False, padding = 10)
        self.contenedor_nivel.pack_start(self.nivel_2, False, padding = 10)
        self.contenedor_nivel.pack_start(self.nivel_3, False, padding = 10)
        self.contenedor_nivel.pack_start(self.instrucciones, False, padding = 10)
        self.contenedor_nivel.pack_start(self.importar_btn, False, padding = 10)
        self.contenedor_nivel_h.show_all()
        self.set_canvas(self.contenedor_nivel_h)
        
        self.show()

    def _creacion(self, nuevo=True):
        '''Crea las variables necesarias para el comienzo del juego'''
        if nuevo:
            self.palabra, self.significado = utils.palabra_aleatoria()
            self.l_aciertos = []
            self.l_errores= []
            self.errores = 0
            self._cambiar_imagen(0)
        else:
            self._cambiar_imagen(self.errores)
        
        self._actualizar_labels(_('El juego ha empezado'))
        self._pintar_palabra()

    def _atras_cb(self, widget, data=None):
        self.set_canvas(self.contenedor_nivel_h)

    def _nivel_uno_cb(self, widget, data=None):
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _nivel_dos_cb(self, widget, data=None):
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _nivel_tres_cb(self, widget, data=None):
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _instrucciones_cb(self, widget, data=None):
        self.contenedor_instruc.show_all()
        self.set_canvas(self.contenedor_instruc)

    def _importar_cb(self, widget, data=None):
        pass

    def _ok_btn_clicked_cb(self, widget, data=None):
        self._actualizar_palabra()

    def _nuevojuego_btn_clicked_cb(self, widget, data=None):
        self.palabra_entry.set_sensitive(True) #Activa la caja de texto
        self.ok_btn.set_sensitive(True) #Activa el botón ok
        self._creacion()
        
    def _cambiar_imagen(self, level):
        ruta = 'resources/%s.png' % level
        _logger.debug('level: %s' % level)
        self.imagen.set_from_file(ruta)

    def _key_press_cb(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        _logger.debug('keyname: %s' % keyname)
        if keyname == 'Return' or keyname == "KP_Enter":
            
            self._actualizar_palabra()
        return False

    def main(self):
        gtk.main()

    def _load_puntaje(self):
        if exists("data/puntaje.pck"):
            f_read = open("data/puntaje.pck", "rb")
            x = pickle.load(f_read)
            f_read.close()
            return x
        else:
            return []

    def _guardar_puntaje(self):
        f_write = open("data/puntaje.pck", "ab")
        info_gamer = (self.aciertos, datetime.now())
        self.lista_record.append(info_gamer)
        pickle.dump(self.lista_record, f_write)
        f_write.close()

    def _actualizar_palabra(self):

        #Convierte la letra a minuscula
        letra_actual = self.palabra_entry.get_text().lower()
        _logger.debug('letra_actual: %s' % letra_actual)

        #Evalua si se escribio mas de 1 letra o esta vacio
        if (len(letra_actual) is not 1 or letra_actual == " "): 
            self.palabra_entry.set_text('')
            _logger.debug('mas de una letra o vacio')
            self.instrucciones_label.set_text(_("Introduzca solo una letra!"))
        
        #Evalua si letra esta dentro de palabra
        elif (letra_actual in self.palabra and letra_actual not in self.l_aciertos):
            self.l_aciertos.append(letra_actual)
            
            for i in range(len(self.palabra)):
                if (letra_actual == self.palabra[i]):
                    self.aciertos += 1
            
            _logger.debug('letra dentro de palabra, aciertos: %s, errores: %s' %(self.aciertos, self.errores))
            self._actualizar_labels("Letra dentro de palabra secreta!")
            
            #Evalua si se acerto la palabra y temina el juego
            if (self.aciertos == len(self.palabra)): 
                _logger.debug('acerto palabra')
                self.instrucciones_label.set_text(_('Acertastes la palabra secreta, ' \
                                                    'FELICIDADES! \n su significado es: %s' % self.significado))
                self.nuevojuego_btn.show() # muestra el boton para comenzar el juego

        #Evalua si letra es repetida y esta dentro de palabra
        elif (letra_actual in self.palabra and letra_actual in self.l_aciertos): 
            _logger.debug('letra repetida y dentro de palabra, aciertos: %s, errores: %s' %(self.aciertos, self.errores))
            self._actualizar_labels("Letra repetida y dentro de palabra secreta!")

        #Evalua si letra no esta dentro de palabra
        elif (letra_actual not in self.palabra and letra_actual not in self.l_errores):
            self.l_errores.append(letra_actual)
            self.errores += 1
            self._cambiar_imagen(self.errores)
            _logger.debug('letra fuera de palabra, aciertos: %s, errores: %s' %(self.aciertos, self.errores))
            self._actualizar_labels("Letra fuera de palabra secreta!")
            
            #Evalua si se completo el ahorcado y temina el juego            
            if (self.errores >= 8):
                _logger.debug('fin del juego')
                self.instrucciones_label.set_text(_('La palabra secreta era %s, ' \
                                                    'Fin del juego! x( su significado es %s' % 
                                                    (self.palabra, self.significado)) )
                self.aciertos = 0
                self.palabra_entry.set_sensitive(False) #Activa la caja de texto
                self.ok_btn.set_sensitive(False) #Inactiva el botón ok una vez que pierde
                

        #Evalua si letra es repetida y no dentro de palabra
        elif (letra_actual not in self.palabra and letra_actual in self.l_errores): 
            _logger.debug('letra repetida y fuera de palabra, aciertos: %s, errores: %s' %(self.aciertos, self.errores))
            self._actualizar_labels("Letra repetida y fuera de palabra secreta!")

        self._pintar_palabra()
        
    def _actualizar_labels(self, instrucciones):
        '''Actualiza labels segun instrucciones'''
        self.palabra_entry.set_text('')
        self.instrucciones_label.set_text(_(instrucciones))
        self.aciertos_label.set_text(_('Puntaje: %s' % self.aciertos))
        letras = ', '.join(letra for letra in self.l_aciertos)
        letras2 = ', '.join(letra for letra in self.l_errores)
        self.letrasusadas_label.set_text(_('Letras Usadas: %s %s' % (letras,letras2)))
        self.errores_label.set_text(_('Errores: %s' % self.errores))

    def _pintar_palabra(self):
        '''Pinta las lineas de la palabra'''
        pista = ''
        for letra in self.palabra:
            if letra in self.l_aciertos:
                pista += '%s ' % letra
            else:
                pista += '_ '
        self.palabra_label.set_text(pista)

    def read_file(self, filepath):
        pass

    def write_file(self, filepath):
        pass

    def close(self, skip_save=False):
        '''override the close to jump the journal'''
        activity.Activity.close(self, True)
