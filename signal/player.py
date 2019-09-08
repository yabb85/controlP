from json import dumps
from logging import debug as log_debug
from time import sleep

from gi.repository import GObject

from .interface import get_pioneer


class PlayerSignal(GObject.GObject):

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
    }

    def __init__(self):
        super().__init__()

    def do_player_get_status_event(self):
        self.emit('player-power-get-status-event')
        self.emit('player-input-get-status-event')
        self.emit('player-screen-get-status-event')

    def do_player_power_event(self, arg):
        if get_pioneer():
            if arg:
                get_pioneer().power_on()
            else:
                get_pioneer().power_off()

    def do_player_power_status_event(self, arg):
        print('do_player_power_status_event : {}'.format(arg))

    def do_player_power_get_status_event(self):
        log_debug('do_player_power_event')
        status = get_pioneer().power_status()
        log_debug('status : {}'.format(status))
        state = status == 'PWR0'
        log_debug('get_state : {}'.format(state))
        self.emit('player-power-status-event', state)

    def do_player_input_event(self, value):
        get_pioneer().set_input(value)
        self.emit('player-screen-get-status-event')

    def do_player_input_status_event(self, value):
        log_debug('do_input_status_event : {}'.format(value))

    def do_player_input_get_status_event(self):
        status = get_pioneer().input_status()
        self.emit('player-input-status-event', status)

    def do_player_screen_status_event(self, value):
        log_debug('do_screen_status_event : {}'.format(value))

    def do_player_screen_get_status_event(self):
        status = get_pioneer().screen_status()
        # print('do_player_screen_get_status : {}'.format(status))
        self.emit('player-screen-status-event', dumps(status))

    def do_player_select_line_event(self, value):
        print(value)
        get_pioneer().select_line(value)
        self.emit('player-screen-get-status-event')
        # sleep(1)
        # self.emit('player-screen-get-status-event')

    def do_player_set_line_event(self, value):
        get_pioneer().set_line(value)
        self.emit('player-screen-get-status-event')
        # sleep(1)
        # self.emit('player-screen-get-status-event')

    def do_player_return_event(self):
        get_pioneer().ret()
        self.emit('player-screen-get-status-event')
