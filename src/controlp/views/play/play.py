from pathlib import Path

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivymd.uix.screen import MDScreen
from .song import SongView
from .control import ControlView
from ..top import TopView


class PlayView(MDScreen):
    top_controller = ObjectProperty()
    top_model = ObjectProperty()
    play_controller = ObjectProperty()
    play_model = ObjectProperty()
    amplifier_controller = ObjectProperty()
    amplifier_model = ObjectProperty()
    bottom_controller = ObjectProperty()
    bottom_model = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        Window.bind(on_keyboard=self.android_back_click)
        self.top_controller.set_previous('explore')
        self.play_controller.start_clock()
        self.bottom_controller.set_screen()

    def on_leave(self):
        self.play_controller.stop_clock()
        Window.unbind(on_keyboard=self.android_back_click)

    def android_back_click(self, window, key, *args):
        if key == 27:
            self.play_controller.back_screen()
            return True


Builder.load_file(str(Path(__file__).parent.joinpath('play.kv')))
