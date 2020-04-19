from logging import debug as log_debug
from gi.repository import Gio, Gtk # type: ignore

from ..coremodel import CoreModel
from ..coresource import CoreSource
from .utils import ListBoxRowSource


@Gtk.Template(filename='controlP/ui/source.ui')
class Source(Gtk.Box):
    """
    Class to display and select source in UI
    """

    __gtype_name__ = 'Source'

    _source_list = Gtk.Template.Child()

    _current_value = None

    def __init__(self, coremodel: CoreModel):
        log_debug('initialize source widget')
        super().__init__()

        self._coremodel = coremodel
        self._model: CoreSource = coremodel.props.coresource
        self._coremodel.connect(
            'network-player-input-status-event', self.on_input_status_event
        )
        self._source_list.bind_model(self._model, self._create_row)
        self._coremodel.emit('network-player-input-get-status-event')
        self.show_all()
        log_debug('source widget initialized')

    def _create_row(self, source_model: CoreSource):
        return ListBoxRowSource(source_model.props.name, source_model.props.val)

    @Gtk.Template.Callback()
    def _on_selected_row_changed(self, listbox):
        row = listbox.get_selected_row()
        if row.value != self._current:
            self._coremodel.emit('network-player-input-event', row.value)
            self._current = row.value

    def on_input_status_event(self, signal, value):
        log_debug('update source selection')
        toto = self._model.props.sources[value]
        for row in self._source_list:
            if row.value == toto.props.val:
                self._current = row.value
                self._source_list.select_row(row)
