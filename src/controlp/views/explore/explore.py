from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivymd.uix.screen import MDScreen
from pathlib import Path
from .menu import MenuView
from ..bottom import BottomView
from ..top import TopView


class ExploreView(MDScreen):
    top_controller = ObjectProperty()
    top_model = ObjectProperty()
    explore_controller = ObjectProperty()
    explore_model = ObjectProperty()
    amplifier_controller = ObjectProperty()
    amplifier_model = ObjectProperty()
    bottom_controller = ObjectProperty()
    bottom_model = ObjectProperty()
    items = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def android_back_click(self, window, key, *args):
        if key == 27:
            if self.explore_model.top == '0':
                self.explore_controller.back_screen()
            else:
                self.explore_controller.explore_return()
            return True
        return True

    def on_enter(self):
        Window.bind(on_keyboard=self.android_back_click)
        self.top_controller.set_previous('input')
        self.explore_controller.refresh_menu()
        self.explore_controller.start_clock()
        self.bottom_controller.set_screen()

    def on_leave(self):
        Window.unbind(on_keyboard=self.android_back_click)


Builder.load_file(str(Path(__file__).parent.joinpath('explore.kv')))
