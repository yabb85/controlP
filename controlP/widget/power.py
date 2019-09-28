from logging import debug as log_debug
from gi.repository import GObject, Gtk


@Gtk.Template(filename='controlP/ui/power.ui')
class Power(Gtk.Box):
    __gtype_name__ = 'Power'

    _network_player_power_switch = Gtk.Template.Child()
    _ampli_power_button = Gtk.Template.Child()

    def __init__(self, coremodel):
        log_debug('initialize power widget')
        super().__init__()
        self._coremodel = coremodel
        self._corepower = coremodel.props.corepower
        self._corepower.bind_property('network_player_active', self._network_player_power_switch, 'active')
        self._coremodel.emit('network-player-power-get-status-event')
        log_debug('power widget initialized')

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
    def _on_network_player_power_activated(self, switch, gparam):
        log_debug('on_network_player_power_activated : {}'.format(switch.get_active()))
        self._coremodel.emit('network-player-power-event', switch.get_active())
