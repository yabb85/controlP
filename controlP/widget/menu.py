from json import loads
from logging import debug as log_debug
from logging import error as log_error

from gi.repository import Gdk, Gtk  # type: ignore

from ..coremodel import CoreModel
from .coversong import Cover
from .menulist import MenuList
from .player import Player
from .utils import ListBoxRowSource


class Menu(Gtk.Box):
    """
    Contains the list/cover song and player
    """
    def __init__(self, model: CoreModel):
        super().__init__(model)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.props.homogeneous = False
        self.display_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.pack_start(self.display_box, True, True, 0)
        self._coremodel = model
        self.menu_list = MenuList(self._coremodel)
        self.display_box.pack_start(self.menu_list, True, True, 0)
        self.cover = Cover(self._coremodel.props.coresong)
        self.display_box.pack_start(self.cover, True, True, 0)

        self.player = Player(self._coremodel)
        self.pack_end(self.player, False, False, 10)

        self.display_box.show()
        self.player.show_all()

        self._coremodel.emit('network-player-screen-get-status-event')
