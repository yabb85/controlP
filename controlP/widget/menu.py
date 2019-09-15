from json import loads
from logging import debug as log_debug
from logging import error as log_error

from gi.repository import Gtk

from .coversong import Cover
from .menulist import MenuList
from .utils import ListBoxRowSource


class Menu(Gtk.Box):
    def __init__(self, model):
        super().__init__(model)
        self._coremodel = model
        self.menu_list = MenuList(self._coremodel)
        self.pack_start(self.menu_list, True, True, 0)
        self.cover = Cover(self._coremodel.props.coresong)
        self.pack_start(self.cover, True, True, 0)
        self._coremodel.emit('network-player-screen-get-status-event')
