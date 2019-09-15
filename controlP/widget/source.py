from gi.repository import Gio, Gtk

from ..coresource import CoreSource
# from ..signal import get_player_signal
from .utils import ListBoxRowSource


@Gtk.Template(filename='controlP/ui/source.ui')
class Source(Gtk.Box):
    """
    Class to display and select source in UI
    """

    __gtype_name__ = 'Source'

    _source_list = Gtk.Template.Child()

    _current_value = None

    def __init__(self, coremodel):
        super().__init__()

        self._coremodel = coremodel
        self._model = coremodel.props.coresource
        self._coremodel.connect('player-input-status-event', self.on_input_status_event)
        self._source_list.bind_model(self._model, self._create_row)
        self._coremodel.emit('player-input-get-status-event')
        self.show_all()

    def _create_row(self, source_model):
        return ListBoxRowSource(source_model.props.name, source_model.props.val)

    @Gtk.Template.Callback()
    def _on_selected_row_changed(self, listbox):
        row = listbox.get_selected_row()
        if row.value != self._model.props.sources[self._current].val:
            self._coremodel.emit('player-input-event', row.value)

    def on_input_status_event(self, signal, value):
        self._current = value
        toto = self._model.props.sources[value]
        for row in self._source_list:
            if row.value == toto.props.val:
                self._source_list.select_row(row)
