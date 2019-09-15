from gi.repository import GObject


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
    visible = GObject.Property(type=bool, default=True)

    def update(self, status, visibility):
        self.visible = visibility
        if self.visible:
            lines = status.get('lines', {})
            self.title = lines.get('01', {}).get('value', None)
            self.artist = lines.get('02', {}).get('value', None)
            self.album = lines.get('03', {}).get('value', None)
            self.encoding = lines.get('04', {}).get('value', None)
            self.sampling = lines.get('05', {}).get('value', None)
            self.resolution = lines.get('06', {}).get('value', None)
            self.elapsed_time = lines.get('07', {}).get('value', None)
            self.duration = lines.get('08', {}).get('value', None)
