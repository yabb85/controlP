from gi.repository import Gtk

from ..signal import get_ampli_signal


class Ampli(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.apower = get_ampli_signal()

        power_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(power_box, False, False, 10)
        power_label = Gtk.Label('power', xalign=0)
        power_box.pack_start(power_label, False, False, 10)
        self.power = Gtk.Button('A', halign=Gtk.Align.CENTER)
        self.power.connect('clicked', self.on_power_activated)
        power_box.pack_start(self.power, False, False, 0)

        vol_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(vol_box, True, True, 0)
        min_vol = Gtk.Button('a')
        min_vol.connect('clicked', self.on_volume_down_activated)
        vol_box.pack_start(min_vol, True, True, 0)
        max_vol = Gtk.Button('b')
        max_vol.connect('clicked', self.on_volume_up_activated)
        vol_box.pack_start(max_vol, True, True, 0)

    def on_power_activated(self, button):
        self.apower.emit('ampli-power-event')

    def on_volume_down_activated(self, button):
        self.apower.emit('ampli-volume-down-event')

    def on_volume_up_activated(self, button):
        self.apower.emit('ampli-volume-up-event')
