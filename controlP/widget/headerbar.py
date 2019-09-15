from gi.repository import Gtk


@Gtk.Template(filename='controlP/ui/headerbar.ui')
class HeaderBar(Gtk.HeaderBar):
    __gtype_name__ = 'HeaderBar'

    def __init__(self, model):
        super().__init__()
        self._coremodel = model

    @Gtk.Template.Callback()
    def _on_ret_button_clicked(self, button):
        self._coremodel.emit('player-return-event')
