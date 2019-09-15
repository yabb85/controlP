from gi.repository import GObject, Gtk

# from ..signal import get_ampli_signal, get_player_signal


@Gtk.Template(filename='controlP/ui/power.ui')
class Power(Gtk.Box):
    __gtype_name__ = 'Power'

    _player_power_switch = Gtk.Template.Child()
    _ampli_power_button = Gtk.Template.Child()

    activated = GObject.Property(
        type=bool, default=False, flags=GObject.ParamFlags.READWRITE
    )

    def __init__(self, model):
        super().__init__()
        self._coremodel = model
        self._coremodel.connect('network-player-power-status-event', self.on_power_status_event)
        self.bind_property('activated', self._player_power_switch, 'active')
        self._coremodel.emit('network-player-get-status-event')

    @Gtk.Template.Callback()
    def _on_ampli_power_clicked(self, button):
        self._coremodel.emit('ampli-power-event')

    @Gtk.Template.Callback()
    def _on_volume_down_clicked(self, button):
        self._coremodel.emit('ampli-volume-down-event')

    @Gtk.Template.Callback()
    def _on_volume_up_clicked(self, button):
        self._coremodel.emit('ampli-volume-up-event')

    @Gtk.Template.Callback()
    def _on_player_power_activated(self, switch, gparam):
        self._coremodel.emit('network-player-power-event', switch.get_active())

    def on_power_status_event(self, signal, val):
        print('on_player_power_status_event : {}'.format(val))
        self.activated = val
