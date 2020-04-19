from logging import getLogger

from gi.repository import Gtk  # type: ignore

from ..coremodel import CoreModel
from ..coremenu import MenuModel
from .utils import ListBoxRowEmpty
from .picturedrow import PicturedRow

LOGGER = getLogger(__name__)
log_debug = LOGGER.debug


@Gtk.Template(filename='controlP/ui/menulist.ui')
class MenuList(Gtk.Box):
    """
    Create a menu to display elements in list
    """

    __gtype_name__ = 'MenuList'

    _up_button = Gtk.Template.Child()
    _menu_list = Gtk.Template.Child()
    _down_button = Gtk.Template.Child()

    def __init__(self, coremodel: CoreModel):
        super().__init__()

        self._coremodel = coremodel
        self._coremenu = coremodel.props.coremenu
        self._menu_list.bind_model(self._coremenu, self._create_row)
        self._menu_list.connect('row-activated', self._on_row_activated)
        self._coremenu.bind_property('visible', self, 'visible')
        self._coremenu.bind_property('up_visible', self._up_button, 'visible')
        self._coremenu.bind_property('down_visible', self._down_button, 'visible')

    def _create_row(self, menu_model: MenuModel):
        log_debug('MenuList _create_row model: {}'.format(menu_model))
        row = ListBoxRowEmpty(menu_model)
        widget = PicturedRow(menu_model)
        log_debug('widget label: {}'.format(widget.menumodel.text))
        row.add(widget)
        if menu_model.props.line_idx == self._coremenu.highlight:
            self._menu_list.select_row(row)
        row.show_all()
        return row

    def _on_row_activated(self, listbox, row):
        self._coremodel.emit('network-player-set-line-event', int(row.value))

    @Gtk.Template.Callback()
    def _on_up_button_clicked(self, button):
        value = max(self._coremenu.props.begin - 20, 1)
        self._coremodel.emit('network-player-select-line-event', value)

    @Gtk.Template.Callback()
    def _on_down_button_clicked(self, button):
        value = min(self._coremenu.props.end + 1, self._coremenu.props.total)
        self._coremodel.emit('network-player-select-line-event', value)
