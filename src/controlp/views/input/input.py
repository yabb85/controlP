from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from pathlib import Path
from ..top import TopView
from ..bottom import BottomView
from .input_list import InputListView

class InputView(MDScreen):
    top_controller = ObjectProperty()
    top_model = ObjectProperty()
    input_controller = ObjectProperty()
    input_model = ObjectProperty()
    amplifier_controller = ObjectProperty()
    amplifier_model = ObjectProperty()
    bottom_controller = ObjectProperty()
    bottom_model = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def android_back_click(self, window, key, *args):
        if key == 27:
            self.top_controller.back_screen()
            return True

    def on_enter(self):
        Window.bind(on_keyboard=self.android_back_click)
        self.bottom_controller.set_screen()
        self.top_controller.set_previous('home')

    def on_leave(self):
        Window.unbind(on_keyboard=self.android_back_click)


Builder.load_file(str(Path(__file__).parent.joinpath('input.kv')))
