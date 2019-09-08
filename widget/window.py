from gi.repository import Gtk

from .ampli import Ampli
from .network_player import NetworkPlayer
from .headerbar import HeaderBar


class PioneerWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Pioneer')
        self.set_border_width(10)
        self.set_default_size(800, 600)

        # stack
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        player = NetworkPlayer()
        stack.add_titled(player, 'player', 'Player')
        ampli = Ampli()
        stack.add_titled(ampli, 'ampli', 'ampli')

        # create header bar
        self.hb = HeaderBar(stack)
        self.set_titlebar(self.hb)
        self.add(stack)


