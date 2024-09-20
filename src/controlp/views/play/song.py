from pathlib import Path

from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivymd.uix.stacklayout import MDStackLayout

from .control import ControlView


class SongView(MDStackLayout):
    controller = ObjectProperty()
    model = ObjectProperty()
    img_url = StringProperty()
    title = StringProperty()
    album = StringProperty()
    artist = StringProperty()
    encoding = StringProperty()
    sampling = StringProperty()
    resolution = StringProperty()
    elapsed_time = StringProperty()
    slider_value = NumericProperty()
    duration = StringProperty()
    slider_max = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        """
        Use this call because model and controller are not set during __init__ call
        """
        super().on_kv_post(base_widget)
        self.model.add_observer(self)

    def android_back_click(self, window, key, *args):
        if key == 27:
            return True

    def model_is_changed(self):
        if self.model.img_url:
            self.img_url = self.model.img_url
        self.title = self.model.title
        self.album = self.model.album
        self.artist = self.model.artist
        self.encoding = self.model.encoding
        self.sampling = self.model.sampling
        self.resolution = self.model.resolution
        self.elapsed_time = self.model.elapsed_time
        self.slider_value = self.model.elapsed_time_s.total_seconds()
        self.duration = self.model.duration
        self.slider_max = self.model.duration_s.total_seconds()


Builder.load_file(str(Path(__file__).parent.joinpath('song.kv')))
