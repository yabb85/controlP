from datetime import timedelta
from threading import Event, Thread

from gi.repository import Gio, GObject, Gtk # type: ignore

from ..coresong import CoreSong


class UpdateTime(Thread):
    """
    Increment time counter each second
    """

    def __init__(self, coresong: CoreSong):
        super().__init__()
        self._coresong = coresong
        self._stop = Event()

    def run(self):
        while not self._stop.wait(1):
            str_elaps_time = self._coresong.props.elapsed_time
            if not str_elaps_time:
                continue
            splitted = str_elaps_time.split(':')
            if len(splitted) != 3:
                continue
            hours = int(splitted[0])
            minutes = int(splitted[1])
            seconds = int(splitted[2])
            new_time = timedelta(
                hours=hours, minutes=minutes, seconds=seconds
            ) + timedelta(seconds=1)
            self._coresong.props.elapsed_time = new_time

    def cancel(self):
        self._stop.set()


@Gtk.Template(filename='controlP/ui/coversong.ui')
class Cover(Gtk.Box):
    """
    Class used to display cover album
    Use coversong.ui template to create panel
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
    _song_cover_image = Gtk.Template.Child()
    _song_info_repeat_image = Gtk.Template.Child()
    _song_info_shuffle_image = Gtk.Template.Child()

    def __init__(self, coresong: CoreSong):
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
        self._coresong.bind_property('pixbuf', self._song_cover_image, 'pixbuf')
        self._coresong.bind_property(
            'repeat', self._song_info_repeat_image, 'icon-name'
        )
        self._coresong.bind_property(
            'shuffle', self._song_info_shuffle_image, 'icon-name'
        )
        self.increment = UpdateTime(self._coresong)
        self.increment.start()

    @GObject.Property(type=CoreSong, flags=GObject.ParamFlags.READABLE)
    def coresong(self):
        return self._coresong

    def do_destroy(self):
        self.increment.cancel()
        Gtk.Box.do_destroy(self)
