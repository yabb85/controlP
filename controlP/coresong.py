from datetime import timedelta
from urllib.request import urlopen

from gi.repository import Gdk, Gio, GObject
from gi.repository.GdkPixbuf import Pixbuf


class CoreSong(GObject.GObject):
    title = GObject.Property(
        type=str, default='title', flags=GObject.ParamFlags.READWRITE
    )
    artist = GObject.Property(
        type=str, default='artist', flags=GObject.ParamFlags.READWRITE
    )
    album = GObject.Property(
        type=str, default='album', flags=GObject.ParamFlags.READWRITE
    )
    encoding = GObject.Property(
        type=str, default='encoding', flags=GObject.ParamFlags.READWRITE
    )
    sampling = GObject.Property(type=str)
    resolution = GObject.Property(type=str)
    elapsed_time = GObject.Property(type=str)
    duration = GObject.Property(type=str)
    url = GObject.Property(type=str)
    state = GObject.Property(type=int)
    pixbuf = GObject.Property(type=Pixbuf)
    visible = GObject.Property(type=bool, default=True)
    shuffle = GObject.Property(type=str, default=None)
    repeat = GObject.Property(type=str, default=None)
    play = GObject.Property(type=int)
    play_icon = GObject.Property(type=str)

    _repeat_list = [
        None,
        'media-playlist-repeat-song-symbolic',
        'media-playlist-repeat-symbolic',
    ]

    def update(self, status, visibility):
        self.visible = visibility
        if self.visible:
            shuffle = status.get('shuffle', 0)
            if shuffle:
                self.shuffle = 'media-playlist-shuffle-symbolic'
            else:
                self.shuffle = None
            repeat = status.get('repeat', 0)
            self.repeat = self._repeat_list[repeat]
            self.play = status.get('play', 0)
            if self.play == 2:
                self.play_icon = 'media-playback-pause-symbolic'
            else:
                self.play_icon = 'media-playback-start-symbolic'
            lines = status.get('lines', {})
            self.title = lines.get(1, {}).get('value', None)
            self.artist = lines.get(2, {}).get('value', None)
            self.album = lines.get(3, {}).get('value', None)
            self.encoding = lines.get(4, {}).get('value', None)
            self.sampling = lines.get(5, {}).get('value', None)
            self.resolution = lines.get(6, {}).get('value', None)
            self.elapsed_time = lines.get(7, {}).get('value', None)
            if self.elapsed_time:
                splitted = self.elapsed_time.split(':')
                self.elapsed_time = timedelta(
                    minutes=int(splitted[0]), seconds=int(splitted[1])
                )
            self.duration = lines.get(8, {}).get('value', None)
            if self.duration:
                splitted = self.duration.split(':')
                self.duration = timedelta(
                    minutes=int(splitted[0]), seconds=int(splitted[1])
                )
            url = status.get('url', None)
            if url:
                response = urlopen(url)
                input_stream = Gio.MemoryInputStream.new_from_data(
                    response.read(), None
                )
                self.pixbuf = Pixbuf.new_from_stream(input_stream, None)
            else:
                self.pixbuf = None
