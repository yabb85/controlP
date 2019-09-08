from gi.repository import Gtk

from ..signal import get_player_signal
from .menu import Menu
from .source import SourceSelector


class NetworkPlayer(Gtk.Box):
    def __init__(self):
        super().__init__()
        # vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.player = get_player_signal()
        self.player.connect('player-power-status-event', self.on_power_status_event)

        self.set_orientation(Gtk.Orientation.VERTICAL)

        # create power button
        hbox_power = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(hbox_power, False, True, 10)
        label = Gtk.Label('power', xalign=0)
        hbox_power.pack_start(label, False, True, 10)
        self.power = Gtk.Switch(halign=Gtk.Align.CENTER)
        self.power.connect('notify::active', self.on_power_activated)
        # self.power.set_active(self.player.get_state())
        self.power.set_active(False)
        hbox_power.pack_start(self.power, False, True, 0)

        hbox_menu = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(hbox_menu, True, True, 0)
        source = SourceSelector()
        hbox_menu.pack_start(source, False, True, 0)
        menu = Menu()
        hbox_menu.pack_start(menu, True, True, 0)
        self.player.emit('player-get-status-event')

    def on_power_activated(self, switch, gparam):
        self.player.emit('player-power-event', switch.get_active())

    def on_power_status_event(self, signal, val):
        print('on_player_power_status_event : {}'.format(val))
        self.power.set_active(val)
