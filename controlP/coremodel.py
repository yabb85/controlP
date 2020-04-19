from json import dumps
from logging import getLogger
from threading import RLock
from time import sleep

from gi.repository import GObject  # type: ignore

from .coremenu import CoreMenu
from .corepower import CorePower
from .coresong import CoreSong
from .coresource import CoreSource
from .pioneer import Pioneer

LOGGER = getLogger(__name__)
log_debug = LOGGER.debug


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
        'network-player-power-status-event': (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (bool,),
        ),
        'network-player-power-get-status-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-input-event': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'network-player-input-status-event': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        'network-player-input-get-status-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-screen-status-event': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        'network-player-screen-get-status-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-select-line-event': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'network-player-set-line-event': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'network-player-return-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-previous-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-play-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-pause-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-stop-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-next-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-shuffle-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'network-player-repeat-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'ampli-power-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'ampli-volume-down-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'ampli-volume-up-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__()

        self._coresong = CoreSong()
        self._coresource = CoreSource(self._sources)
        self._coremenu = CoreMenu()
        self._corepower = CorePower()
        self._network_player = Pioneer('192.168.1.100', 8102)
        self.locker = RLock()

    @GObject.Property(type=CoreSong, flags=GObject.ParamFlags.READABLE)
    def coresong(self):
        return self._coresong

    @GObject.Property(type=CoreSource, flags=GObject.ParamFlags.READABLE)
    def coresource(self):
        return self._coresource

    @GObject.Property(type=CoreMenu, flags=GObject.ParamFlags.READABLE)
    def coremenu(self):
        return self._coremenu

    @GObject.Property(type=CorePower, flags=GObject.ParamFlags.READABLE)
    def corepower(self):
        return self._corepower

    def do_network_player_get_status_event(self):
        log_debug('do_network_player_get_status_event')
        self.emit('network-player-power-get-status-event')
        self.emit('network-player-input-get-status-event')
        self.emit('network-player-screen-get-status-event')

    def do_network_player_power_event(self, arg):
        log_debug('do_network_player_power_event : {}'.format(arg))
        if self._network_player:
            if arg:
                self._network_player.power_on()
                self._corepower.props.network_player_active = True
            else:
                self._network_player.power_off()
                self._corepower.props.network_player_active = False

    def do_network_player_power_get_status_event(self):
        log_debug('do_player_power_event')
        status = self._network_player.power_status()
        log_debug('power status : {}'.format(status))
        state = status == 'PWR0'
        log_debug('power get_state : {}'.format(state))
        self._corepower.props.network_player_active = state

    def do_network_player_input_event(self, value):
        self._network_player.set_input(value)
        self.emit('network-player-screen-get-status-event')

    def do_network_player_input_status_event(self, value):
        log_debug('do_input_status_event : {}'.format(value))

    def do_network_player_input_get_status_event(self):
        log_debug('do_network_player_input_get_status_event')
        status = self._network_player.input_status()
        self.emit('network-player-input-status-event', status)

    def do_network_player_screen_status_event(self, value):
        log_debug('do_screen_status_event : {}'.format(value))

    def do_network_player_screen_get_status_event(self):
        log_debug('do_network_player_screen_get_status_event')
        with self.locker:
            log_debug(
                'network player powered : {}'.format(
                    self.props.corepower.props.network_player_active
                )
            )
            if not self._corepower.props.network_player_active:
                self._coresong.update(None, False)
                self._coremenu.update(None, False)
                return
            status = self._network_player.screen_status()
            log_debug('screen status : {}'.format(status))
            if not status:
                self._coresong.update(None, False)
                self._coremenu.update(None, False)
                return
            view_type = status.get('type', None)
            if view_type and (view_type == '02' or view_type == '03'):
                img_url = self._network_player.img_status()
                status.update(img_url)
                self._coresong.update(status, True)
                self._coremenu.update(status, False)
            elif view_type and view_type == '01':
                log_debug('begin_disp: {}'.format(status['begin_disp']))
                log_debug('end_disp: {}'.format(status['end_disp']))
                log_debug('total_line: {}'.format(status['total_line']))
                limit = min(20, status['total_line'] - status['begin_disp'] + 1)
                log_debug('limit: {}'.format(limit))
                new_lines = self._network_player.directory_status(
                    status['begin_disp'], limit
                )
                status['lines'].update(new_lines)
                status['end_disp'] = status['begin_disp'] + len(new_lines) - 1
                log_debug('new end_disp: {}'.format(status['end_disp']))
                self._coresong.update(status, False)
                self._coremenu.update(status, True)
            else:
                self._coresong.update(None, False)
                self._coremenu.update(None, False)
        log_debug('do_network_player_input_get_status_event release lock')

    def do_network_player_select_line_event(self, value):
        self._network_player.select_line(value)
        self.emit('network-player-screen-get-status-event')

    def do_network_player_set_line_event(self, value):
        self._network_player.set_line(value)
        self.emit('network-player-screen-get-status-event')

    def do_network_player_return_event(self):
        self._network_player.ret()
        self.emit('network-player-screen-get-status-event')

    def do_network_player_previous_event(self):
        self._network_player.previous()
        self.emit('network-player-screen-get-status-event')

    def do_network_player_play_event(self):
        self._network_player.play()
        self.emit('network-player-screen-get-status-event')

    def do_network_player_pause_event(self):
        self._network_player.pause()
        self.emit('network-player-screen-get-status-event')

    def do_network_player_stop_event(self):
        self._network_player.stop()
        self.emit('network-player-screen-get-status-event')

    def do_network_player_next_event(self):
        self._network_player.next()
        self.emit('network-player-screen-get-status-event')

    def do_network_player_shuffle_event(self):
        self._network_player.shuffle()
        self.emit('network-player-screen-get-status-event')

    def do_network_player_repeat_event(self):
        self._network_player.repeat()
        self.emit('network-player-screen-get-status-event')

    def do_ampli_power_event(self):
        self._network_player.ampli_power()

    def do_ampli_volume_down_event(self):
        self._network_player.volume_down()

    def do_ampli_volume_up_event(self):
        self._network_player.volume_up()
