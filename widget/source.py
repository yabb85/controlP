from gi.repository import Gtk

from ..signal import get_player_signal
from .utils import ListBoxRowSource


class SourceSelector(Gtk.Box):

    _sources = {
        'dac': ListBoxRowSource('DAC', 13),
        'ipod/usb front': ListBoxRowSource('USB Front', 17),
        'radio': ListBoxRowSource('Radio', 38),
        'NAS': ListBoxRowSource('NAS', 44),
        'favorite': ListBoxRowSource('Favoris', 45),
        'spotify': ListBoxRowSource('Spotify', 57),
        'digital input 1': ListBoxRowSource('Digital Input 1', 59),
        'digital input 2': ListBoxRowSource('Digital Input 2', 60),
        'ipod/usb rear': ListBoxRowSource('USB Rear', 61),
    }
    _current = None

    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.player = get_player_signal()
        self.player.connect('player-input-status-event', self.on_input_status_event)

        self.list_source = Gtk.ListBox()
        self.list_source.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.pack_start(self.list_source, True, True, 0)
        for item in self._sources.values():
            self.list_source.add(item)
        self.list_source.connect('row-activated', self.on_row_activated)

    def on_row_activated(self, listbox, row):
        if row.value != self._sources[self._current].value:
            self.player.emit('player-input-event', row.value)

    def on_input_status_event(self, signal, value):
        self._current = value
        self.list_source.select_row(self._sources[value])
