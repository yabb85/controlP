from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, BooleanProperty
from pathlib import Path
from .amplifier import AmplifierLayout
from .cd_player import CDPlayerLayout


class OtherDevicesView(MDScreen):
    amplifier_controller = ObjectProperty()
    amplifier_model = ObjectProperty()
    cd_player_controller = ObjectProperty()
    cd_player_model = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def android_back_click(self, window, key, *args):
        if key == 27:
            self.amplifier_controller.back_screen()
            return True

    def on_enter(self):
        Window.bind(on_keyboard=self.android_back_click)
        self.cd_player_controller.load()

    def on_leave(self):
        Window.unbind(on_keyboard=self.android_back_click)


Builder.load_file(str(Path(__file__).parent.joinpath('other_devices.kv')))
