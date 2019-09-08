from gi.repository import GObject

from .interface import get_pioneer


class AmpliSignal(GObject.GObject):

    __gsignals__ = {
        'ampli-power-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'ampli-volume-down-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'ampli-volume-up-event': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__()

    def do_ampli_power_event(self):
        get_pioneer().ampli_power()

    def do_ampli_volume_down_event(self):
        get_pioneer().volume_down()

    def do_ampli_volume_up_event(self):
        get_pioneer().volume_up()
