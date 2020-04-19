from gi.repository import Gtk # type: ignore


@Gtk.Template(filename='controlP/ui/player.ui')
class Player(Gtk.Box):
    __gtype_name__ = 'Player'

    _player_play_image = Gtk.Template.Child()

    def __init__(self, coremodel):
        super().__init__()

        self._coremodel = coremodel
        self._coresong = coremodel.props.coresong

    @Gtk.Template.Callback()
    def _on_previous_clicked(self, button):
        self._coremodel.emit('network-player-previous-event')

    @Gtk.Template.Callback()
    def _on_play_clicked(self, button):
        if self._coresong.props.play == 2:
            self._coremodel.emit('network-player-pause-event')
        else:
            self._coremodel.emit('network-player-play-event')

    @Gtk.Template.Callback()
    def _on_stop_clicked(self, button):
        self._coremodel.emit('network-player-stop-event')

    @Gtk.Template.Callback()
    def _on_next_clicked(self, button):
        self._coremodel.emit('network-player-next-event')

    @Gtk.Template.Callback()
    def _on_shuffle_clicked(self, button):
        self._coremodel.emit('network-player-shuffle-event')

    @Gtk.Template.Callback()
    def _on_repeat_clicked(self, button):
        self._coremodel.emit('network-player-repeat-event')

