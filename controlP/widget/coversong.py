from gi.repository import Gio, GObject, Gtk

from ..coresong import CoreSong


@Gtk.Template(filename='controlP/ui/coversong.ui')
class Cover(Gtk.Box):
    """
    Class to display cover album
    """

    __gtype_name__ = 'CoverSong'

    _song_info_title = Gtk.Template.Child()
    _song_info_artist = Gtk.Template.Child()
    _song_info_album = Gtk.Template.Child()
    _song_info_encoding = Gtk.Template.Child()
    _song_info_sampling = Gtk.Template.Child()
    _song_info_resolution = Gtk.Template.Child()
    _song_info_elapsed_time = Gtk.Template.Child()
    _song_info_duration = Gtk.Template.Child()

    def __init__(self, coresong):
        super().__init__()

        self._coresong = coresong
        self._coresong.bind_property('title', self._song_info_title, 'label')
        self._coresong.bind_property('artist', self._song_info_artist, 'label')
        self._coresong.bind_property('album', self._song_info_album, 'label')
        self._coresong.bind_property('encoding', self._song_info_encoding, 'label')
        self._coresong.bind_property('sampling', self._song_info_sampling, 'label')
        self._coresong.bind_property('resolution', self._song_info_resolution, 'label')
        self._coresong.bind_property(
            'elapsed_time', self._song_info_elapsed_time, 'label'
        )
        self._coresong.bind_property('duration', self._song_info_duration, 'label')
        self._coresong.bind_property('visible', self, 'visible')

    @GObject.Property(type=CoreSong, flags=GObject.ParamFlags.READABLE)
    def coresong(self):
        return self._coresong
