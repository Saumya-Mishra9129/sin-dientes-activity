from sugar.activity import activity
import gtk
from gettext import gettext as _
import logging

import utils

_logger = logging.getLogger('ahorcado-activity')

class Ahorcado:

    def __init__(self):
        self.palabra = utils.palabra_aleatoria()
        self.puntaje = 0
        self.errores = 0
        self.letras = []

        #ventana
        self.ventana = gtk.Window()
        self.ventana.set_title(_('Ahorcado'))
        self.ventana.connect('key-press-event', self._key_press_cb)
        self.ventana.connect('destroy', self._destroy_cb)
        
        #contenedores
        self.contenedor = gtk.VBox()
        self.ventana.add(self.contenedor)

        self.contenedor_superior = gtk.HBox()
        self.contenedor_inferior= gtk.HBox()

        self.contenedor.pack_start(self.contenedor_superior)
        self.contenedor.pack_start(self.contenedor_inferior, expand=False)

        #interface
        self.palabra_entry = gtk.Entry()
        self.palabra_label = gtk.Label()
        self.puntaje_label = gtk.Label('Puntaje: 0')
        self.ok_btn = gtk.Button(_('Ok'))
        self.ok_btn.connect('clicked', self._ok_btn_clicked_cb, None)
        self.label = gtk.Label()
        self.imagen = gtk.Image()
        
        self._cambiar_imagen(0)
        self._actualizar_palabra()

        #agregando elementos
        self.contenedor_superior.pack_start(self.imagen)
        self.contenedor_superior.pack_start(self.puntaje_label)
        self.contenedor_superior.pack_start(self.palabra_label)

        self.contenedor_inferior.pack_start(self.palabra_entry)
        self.contenedor_inferior.pack_start(self.ok_btn, False)
        
        self.contenedor.show_all()
        self.ventana.show()
        print self.palabra

    def _ok_btn_clicked_cb(self, widget, data=None):
        self._actualizar_palabra()

    def _cambiar_imagen(self, level):
        ruta = 'resources/%s.jpg' % level
        self.imagen.set_from_file(ruta)

    def _key_press_cb(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return':
            self._actualizar_palabra()
        return False

    def read_file(self, filepath):
        pass

    def write_file(self, filepath):
        pass

    def main(self):
        gtk.main()

    def _destroy_cb(self, widget, data=None):
        gtk.main_quit()

    def _actualizar_palabra(self):
        letra_actual = self.palabra_entry.get_text()
        #TODO: Validar que solo introduzca una letra
        if letra_actual != '' and letra_actual in self.palabra:
            self.puntaje += 1
            self.puntaje_label.set_text(_('Puntaje: %s' % self.puntaje))
            self.palabra = utils.palabra_aleatoria()
            self.letras.append(letra_actual)
        elif letra_actual != '':
            self.letras.append(letra_actual)
            self.errores += 1
            self._cambiar_imagen(self.errores)
        else:
            pass #TODO validar letra vacia

        pista = ''
        for letra in self.palabra:
            if letra in self.letras:
                pista += '%s ' % letra
            else:
                pista += '_ '

        self.palabra_label.set_text(pista)
        self.palabra_entry.set_text('')

if __name__ == "__main__":
    foo = Ahorcado()
    foo.main()
