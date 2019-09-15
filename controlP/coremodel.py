from gi.repository import GObject
from json import dumps
from logging import debug as log_debug
from time import sleep

from .coremenu import CoreMenu
from .coresong import CoreSong
from .coresource import CoreSource
from .pioneer import Pioneer

class CoreModel(GObject.GObject):

    _sources = {
        'DAC': ('DAC', 13),
        'ipod/usb front': ('USB Front', 17),
        'radio': ('Radio', 38),
        'NAS': ('NAS', 44),
        'favorite': ('Favoris', 45),
        'spotify': ('Spotify', 57),
        'digital input 1': ('Digital Input 1', 59),
        'digital input 2': ('Digital Input 2', 60),
        'ipod/usb rear': ('USB Rear', 61),
    }

    __gsignals__ = {
        'network-player-get-status-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-power-event': (GObject.SIGNAL_RUN_FIRST, None, (bool,)),
        'network-player-power-status-event': (GObject.SignalFlags.RUN_FIRST, None, (bool,)),
        'network-player-power-get-status-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-input-event': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'network-player-input-status-event': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        'network-player-input-get-status-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-screen-status-event': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        'network-player-screen-get-status-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-select-line-event': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'network-player-set-line-event': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'network-player-return-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'ampli-power-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'ampli-volume-down-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'ampli-volume-up-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__()

        self._coresong = CoreSong()
        self._coresource = CoreSource(self._sources)
        self._coremenu = CoreMenu()
        self._network_player = Pioneer('192.168.1.100', 8102)

    @GObject.Property(type=CoreSong, flags=GObject.ParamFlags.READABLE)
    def coresong(self):
        return self._coresong

    @GObject.Property(type=CoreSource, flags=GObject.ParamFlags.READABLE)
    def coresource(self):
        return self._coresource

    @GObject.Property(type=CoreMenu, flags=GObject.ParamFlags.READABLE)
    def coremenu(self):
        return self._coremenu

    def do_network_player_get_status_event(self):
        self.emit('network-player-power-get-status-event')
        self.emit('network-player-input-get-status-event')
        self.emit('network-player-screen-get-status-event')

    def do_network_player_power_event(self, arg):
        if self._network_player:
            if arg:
                self._network_player.power_on()
            else:
                self._network_player.power_off()

    def do_network_player_power_status_event(self, arg):
        print('do_player_power_status_event : {}'.format(arg))

    def do_network_player_power_get_status_event(self):
        log_debug('do_player_power_event')
        status = self._network_player.power_status()
        log_debug('status : {}'.format(status))
        state = status == 'PWR0'
        log_debug('get_state : {}'.format(state))
        self.emit('network-player-power-status-event', state)

    def do_network_player_input_event(self, value):
        self._network_player.set_input(value)
        self.emit('network-player-screen-get-status-event')

    def do_network_player_input_status_event(self, value):
        log_debug('do_input_status_event : {}'.format(value))

    def do_network_player_input_get_status_event(self):
        status = self._network_player.input_status()
        self.emit('network-player-input-status-event', status)

    def do_network_player_screen_status_event(self, value):
        log_debug('do_screen_status_event : {}'.format(value))

    def do_network_player_screen_get_status_event(self):
        status = self._network_player.screen_status()
        if status and status.get('type', None) == 2:
            self._coresong.update(status, True)
            self._coremenu.update(status, False)
        else:
            self._coresong.update(status, False)
            self._coremenu.update(status, True)


    def do_network_player_select_line_event(self, value):
        print(value)
        self._network_player.select_line(value)
        self.emit('network-player-screen-get-status-event')

    def do_network_player_set_line_event(self, value):
        self._network_player.set_line(value)
        self.emit('network-player-screen-get-status-event')

    def do_network_player_return_event(self):
        self._network_player.ret()
        self.emit('network-player-screen-get-status-event')

    def do_ampli_power_event(self):
        self._network_player.ampli_power()

    def do_ampli_volume_down_event(self):
        self._network_player.volume_down()

    def do_ampli_volume_up_event(self):
        self._network_player.volume_up()
