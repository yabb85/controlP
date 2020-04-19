from gi.repository import Gtk # type: ignore

from ..coremodel import CoreModel


@Gtk.Template(filename='controlP/ui/headerbar.ui')
class HeaderBar(Gtk.HeaderBar):
    """
    Create header bar with button to return previous menu and menu with about and quit
    button
    """

    __gtype_name__ = 'HeaderBar'

    def __init__(self, model: CoreModel):
        super().__init__()
        self._coremodel = model

    @Gtk.Template.Callback()
    def _on_ret_button_clicked(self, button):
        self._coremodel.emit('network-player-return-event')
