from sugar.activity import activity
import gtk
from gettext import gettext as _
import logging

_logger = logging.getLogger('ahorcado-activity')

class Ahorcado(activity.Activity):

    def __init__(self, handle):
        super(Ahorcado, self).__init__(handle)

        self.set_title(_(Ahorcado))

        barra = activity.ActivityToolbox(self)
        self.set_toolbox(barra)
        barra.show()

        self.contenedor = gtk.VBox()
        self.set_canvas(contenedor)
        self.connect('key-press-event', self._key_press_cb)

        #interface
        self.palabra_entry = gtk.Entry()
        self.puntaje_entry = gtk.Entry()
        self.ok_btn = gtk.Button(_('Ok'))
        self.ok_btn.connect('clicked', self._ok_btn_clicked_cb, None)
        self.imagen = gtk.Image()
        self.label = gtk.Label()

    def _ok_btn_clicked_cb(self, widget, data=None):
        pass

    def _cambiar_imagen(self, level):
        ruta = 'resources/%s.jpg' % level
        self.imagen.set_from_file(ruta)

    def _key_press_cb(self, widget, event):
        #keyname = gtk.gdk.keyval_name(event.keyval)
        #if keyname == 'Enter':
        pass

    def read_file(self, filepath):
        pass

    def write_file(self, filepath):
        pass


