from gi.repository import Gtk

from .utils import ListBoxRowSource

@Gtk.Template(filename='controlP/ui/menulist.ui')
class MenuList(Gtk.Box):
    __gtype_name__ = 'MenuList'

    _up_button = Gtk.Template.Child()
    _menu_list = Gtk.Template.Child()
    _down_button = Gtk.Template.Child()

    def __init__(self, coremodel):
        super().__init__()

        self._coremodel = coremodel
        self._coremenu = coremodel.props.coremenu
        self._menu_list.bind_model(self._coremenu, self._create_row)
        self._menu_list.connect('row-activated', self._on_row_activated)
        self._coremenu.bind_property('visible', self, 'visible')
        self._coremenu.bind_property('up_visible', self._up_button, 'visible')
        self._coremenu.bind_property('down_visible', self._down_button, 'visible')

    def _create_row(self, menu_model):
        row = ListBoxRowSource(menu_model.props.text, menu_model.props.line_idx)
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
