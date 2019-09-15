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
        'dac': ('DAC', 13),
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
        'player-get-status-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'player-power-event': (GObject.SIGNAL_RUN_FIRST, None, (bool,)),
        'player-power-status-event': (GObject.SignalFlags.RUN_FIRST, None, (bool,)),
        'player-power-get-status-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'player-input-event': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'player-input-status-event': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        'player-input-get-status-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'player-screen-status-event': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        'player-screen-get-status-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'player-select-line-event': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'player-set-line-event': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'player-return-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'ampli-power-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'ampli-volume-down-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'ampli-volume-up-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__()

        self._coresong = CoreSong()
        self._coresource = CoreSource(self._sources)
        self._coremenu = CoreMenu()
        self._player = Pioneer('192.168.1.100', 8102)

    @GObject.Property(type=CoreSong, flags=GObject.ParamFlags.READABLE)
    def coresong(self):
        return self._coresong

    @GObject.Property(type=CoreSource, flags=GObject.ParamFlags.READABLE)
    def coresource(self):
        return self._coresource

    @GObject.Property(type=CoreMenu, flags=GObject.ParamFlags.READABLE)
    def coremenu(self):
        return self._coremenu

    def do_player_get_status_event(self):
        self.emit('player-power-get-status-event')
        self.emit('player-input-get-status-event')
        self.emit('player-screen-get-status-event')

    def do_player_power_event(self, arg):
        if self._player:
            if arg:
                self._player.power_on()
            else:
                self._player.power_off()

    def do_player_power_status_event(self, arg):
        print('do_player_power_status_event : {}'.format(arg))

    def do_player_power_get_status_event(self):
        log_debug('do_player_power_event')
        status = self._player.power_status()
        log_debug('status : {}'.format(status))
        state = status == 'PWR0'
        log_debug('get_state : {}'.format(state))
        self.emit('player-power-status-event', state)

    def do_player_input_event(self, value):
        self._player.set_input(value)
        self.emit('player-screen-get-status-event')

    def do_player_input_status_event(self, value):
        log_debug('do_input_status_event : {}'.format(value))

    def do_player_input_get_status_event(self):
        status = self._player.input_status()
        self.emit('player-input-status-event', status)

    def do_player_screen_status_event(self, value):
        log_debug('do_screen_status_event : {}'.format(value))

    def do_player_screen_get_status_event(self):
        status = self._player.screen_status()
        # print('do_player_screen_get_status : {}'.format(status))
        # self.emit('player-screen-status-event', dumps(status))
        if status and status.get('type', None) == 2:
            self._coresong.update(status, True)
            self._coremenu.update(status, False)
        else:
            self._coresong.update(status, False)
            self._coremenu.update(status, True)


    def do_player_select_line_event(self, value):
        print(value)
        self._player.select_line(value)
        self.emit('player-screen-get-status-event')
        # sleep(1)
        # self.emit('player-screen-get-status-event')

    def do_player_set_line_event(self, value):
        self._player.set_line(value)
        self.emit('player-screen-get-status-event')
        # sleep(1)
        # self.emit('player-screen-get-status-event')

    def do_player_return_event(self):
        self._player.ret()
        self.emit('player-screen-get-status-event')

    def do_ampli_power_event(self):
        self._player.ampli_power()

    def do_ampli_volume_down_event(self):
        self._player.volume_down()

    def do_ampli_volume_up_event(self):
        self._player.volume_up()
