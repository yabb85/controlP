from logging import getLogger

from gi.repository import Gio, GObject, Gtk  # type: ignore

from ..coremenu import MenuModel

LOGGER = getLogger(__name__)
log_debug = LOGGER.debug


@Gtk.Template(filename='controlP/ui/picturedrow.ui')
class PicturedRow(Gtk.Box):
    __gtype_name__ = 'PicturedRow'

    _picture_row = Gtk.Template.Child()
    _label_row = Gtk.Template.Child()

    def __init__(self, menumodel: MenuModel):
        log_debug('init Pictured row')
        super().__init__()

        self._menumodel = menumodel
        self._picture_row.set_from_pixbuf(self.menumodel.props.pixbuf)
        self._label_row.set_text(self.menumodel.props.text)
        self._menumodel.bind_property('text', self._label_row, 'label')
        self._menumodel.bind_property('pixbuf', self._picture_row, 'pixbuf')
        log_debug('menumodel text: {}'.format(self._menumodel.props.text))
        self.show_all()

    @GObject.Property(type=MenuModel, flags=GObject.ParamFlags.READABLE)
    def menumodel(self):
        return self._menumodel

    def do_destroy(self):
        Gtk.Box.do_destroy(self)
